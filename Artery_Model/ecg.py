import numpy as np
import scipy.ndimage
import scipy.signal
import math

# ipeaks: labels for PQRST peaks: P(1), Q(2), R(3), S(4), T(5)
# A zero lablel is output otherwise ... use R=find(ipeaks==3); 
# to find the R peaks s(R), etc. 

# Operation uses the following parameters (default values in []s):
# sfecg: ECG sampling frequency [256 Hertz]
# N: approximate number of heart beats [256]
# Anoise: Additive uniformly distributed measurement noise [0 mV]
# hrmean: Mean heart rate [60 beats per minute]
# hrstd: Standard deviation of heart rate [1 beat per minute]
# lfhfratio: LF/HF ratio [0.5]
# sfint: Internal sampling frequency [256 Hertz]
# Order of extrema: [P Q R S T]
# ti = angles of extrema [-70 -15 0 15 100] degrees
# ai = z-position of extrema [1.2 -5 30 -7.5 0.75]
# bi = Gaussian width of peaks [0.25 0.1 0.1 0.1 0.4]

def signal_resample( signal, desired_length=None, sampling_rate=None, desired_sampling_rate=None, method="interpolation"):
    if desired_length is None:
        desired_length = int(np.round(len(signal) * desired_sampling_rate / sampling_rate))

    # Sanity checks
    if len(signal) == desired_length:
        return signal

    # Resample
    resampled = scipy.ndimage.zoom(signal, desired_length / len(signal))

    return resampled

def ecg_simulate_rrprocess( flo=0.1, fhi=0.25, flostd=0.01, fhistd=0.01, lfhfratio=0.5, hrmean=60, hrstd=1, sfrr=1, n=256):
    w1 = 2 * np.pi * flo
    w2 = 2 * np.pi * fhi
    c1 = 2 * np.pi * flostd
    c2 = 2 * np.pi * fhistd
    sig2 = 1
    sig1 = lfhfratio
    rrmean = 60 / hrmean
    rrstd = 60 * hrstd / (hrmean * hrmean)

    df = sfrr / n
    w = np.arange(n) * 2 * np.pi * df
    dw1 = w - w1
    dw2 = w - w2

    Hw1 = sig1 * np.exp(-0.5 * (dw1 / c1) ** 2) / np.sqrt(2 * np.pi * c1 ** 2)
    Hw2 = sig2 * np.exp(-0.5 * (dw2 / c2) ** 2) / np.sqrt(2 * np.pi * c2 ** 2)
    Hw = Hw1 + Hw2
    Hw0 = np.concatenate((Hw[0 : int(n / 2)], Hw[int(n / 2) - 1 :: -1]))
    Sw = (sfrr / 2) * np.sqrt(Hw0)

    ph0 = 2 * np.pi * np.random.uniform(size=int(n / 2 - 1))
    ph = np.concatenate([[0], ph0, [0], -np.flipud(ph0)])
    SwC = Sw * np.exp(1j * ph)
    x = (1 / n) * np.real(np.fft.ifft(SwC))

    xstd = np.std(x)
    ratio = rrstd / xstd
    return rrmean + x * ratio  # Return RR

def ecg_simulate_derivsecgsyn(t, x, rr, ti, sfint, ai, bi):
    ta = math.atan2(x[1], x[0])
    r0 = 1
    a0 = 1.0 - np.sqrt(x[0] ** 2 + x[1] ** 2) / r0

    ip = np.floor(t * sfint).astype(int)
    w0 = 2 * np.pi / rr[min(ip, len(rr) - 1)]
    # w0 = 2*np.pi/rr[ip[ip <= np.max(rr)]]

    fresp = 0.25
    zbase = 0.005 * np.sin(2 * np.pi * fresp * t)

    dx1dt = a0 * x[0] - w0 * x[1]
    dx2dt = a0 * x[1] + w0 * x[0]

    # matlab rem and numpy rem are different
    # dti = np.remainder(ta - ti, 2*np.pi)
    dti = (ta - ti) - np.round((ta - ti) / 2 / np.pi) * 2 * np.pi
    dx3dt = -np.sum(ai * dti * np.exp(-0.5 * (dti / bi) ** 2)) - 1 * (x[2] - zbase)

    dxdt = np.array([dx1dt, dx2dt, dx3dt])
    return dxdt 

def ecg_simulate_ecgsyn( sfecg=256, N=256, Anoise=0, hrmean=60, hrstd=1, lfhfratio=0.5, sfint=512, ti=(-70, -15, 0, 15, 100),  ai=(1.2, -5, 30, -7.5, 0.75), bi=(0.25, 0.1, 0.1, 0.1, 0.4) ):
    
    if not isinstance(ti, np.ndarray):
        ti = np.array(ti)
    if not isinstance(ai, np.ndarray):
        ai = np.array(ai)
    if not isinstance(bi, np.ndarray):
        bi = np.array(bi)

    ti = ti * np.pi / 180

    # Adjust extrema parameters for mean heart rate
    hrfact = np.sqrt(hrmean / 60)
    hrfact2 = np.sqrt(hrfact)
    bi = hrfact * bi
    ti = np.array([hrfact2, hrfact, 1, hrfact, hrfact2]) * ti

    # Check that sfint is an integer multiple of sfecg
    q = np.round(sfint / sfecg)
    qd = sfint / sfecg
    if q != qd:
        raise ValueError(
            "Internal sampling frequency (sfint) must be an integer multiple of the ECG sampling frequency"
            " (sfecg). Your current choices are: sfecg = " + str(sfecg) + " and sfint = " + str(sfint) + "."
        )

    # Define frequency parameters for rr process
    # flo and fhi correspond to the Mayer waves and respiratory rate respectively
    flo = 0.1
    fhi = 0.25
    flostd = 0.01
    fhistd = 0.01

    # Calculate time scales for rr and total output
    sfrr = 1
    trr = 1 / sfrr
    rrmean = 60 / hrmean
    n = 2 ** (np.ceil(np.log2(N * rrmean / trr)))

    rr0 = ecg_simulate_rrprocess(flo, fhi, flostd, fhistd, lfhfratio, hrmean, hrstd, sfrr, n)

    # Upsample rr time series from 1 Hz to sfint Hz
    rr = signal_resample(rr0, sampling_rate=1, desired_sampling_rate=sfint)

    # Make the rrn time series
    dt = 1 / sfint
    rrn = np.zeros(len(rr))
    tecg = 0
    i = 0
    while i < len(rr):
        tecg += rr[i]
        ip = int(np.round(tecg / dt))
        rrn[i:ip] = rr[i]
        i = ip
    Nt = ip

    # Integrate system using fourth order Runge-Kutta
    x0 = np.array([1, 0, 0.04])

    # tspan is a tuple of (min, max) which defines the lower and upper bound of t in ODE
    # t_eval is the list of desired t points for ODE
    # in Matlab, ode45 can accepts both tspan and t_eval in one argument
    Tspan = [0, (Nt - 1) * dt]
    t_eval = np.linspace(0, (Nt - 1) * dt, Nt)

    # as passing extra arguments to derivative function is not supported yet in solve_ivp
    # lambda function is used to serve the purpose
    result = scipy.integrate.solve_ivp( lambda t, x: ecg_simulate_derivsecgsyn(t, x, rrn, ti, sfint, ai, bi), Tspan, x0, t_eval=t_eval )
    X0 = result.y

    # downsample to required sfecg
    X = X0[:, np.arange(0, X0.shape[1], q).astype(int)]

    # Scale signal to lie between -0.4 and 1.2 mV
    z = X[2, :].copy()
    zmin = np.min(z)
    zmax = np.max(z)
    zrange = zmax - zmin
    z = (z - zmin) * 1.6 / zrange - 0.4

    # include additive uniformly distributed measurement noise
    eta = 2 * np.random.uniform(len(z)) - 1
    return z + Anoise * eta  # Return signal

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sampling_rate= 5

    length = 10
    duration = None

    if length is None:
        length = duration * sampling_rate
    if duration is None:
        duration = length / sampling_rate

    n = [60, 160]

    for i in n:
        heart_rate = i
        # Run appropriate method
        approx_number_of_beats = int(np.round(duration * (heart_rate / 60)))
        ecg = ecg_simulate_ecgsyn( sfecg=500, N=approx_number_of_beats, Anoise=0, hrmean=heart_rate, hrstd=1, lfhfratio=0.5, sfint=500, ti=(-70, -15, 0, 15, 100), ai=(1.2, -5, 30, -7.5, 0.75), bi=(0.25, 0.1, 0.1, 0.1, 0.4) )
        #print(len(ecg))
        plt.plot(ecg)
        plt.show()