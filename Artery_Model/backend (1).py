import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math
import time

def pulsegen(t, x, R1, L, R2, C, clock, it):
    i1 = np.interp(t, clock, it)
    xdot = [[0.0], [0.0]]
    xdot[0] = -R1 / L * x[0] + R1 * i1 / L
    xdot[1] = -x[1] / (R2 * C) + i1 / C
    return xdot

def integrated_ode(t, x, Vin, clock):
    rlcnewval = np.genfromtxt('pycall/Datas/rlcnewval.txt', delimiter=',')
    Rs = rlcnewval[:, 0]
    L = rlcnewval[:, 1]
    C = rlcnewval[:, 2]
    Rp = rlcnewval[:, 3]
    Vin = np.interp(t, clock, Vin)
    xdot = np.zeros(126, dtype=np.float64)

    # Aortic Segment
    xdot[0] = Vin / L[0] - x[0] * Rs[0] / L[0] - x[1] / L[0]
    xdot[1] = x[0] / C[0] - x[2] / C[0]
    xdot[2] = x[1] / L[1] - x[2] * Rs[1] / L[1] - x[3] / L[1]
    xdot[3] = x[2] / C[1] - x[52] / C[1] - x[4] / C[1] - x[28] / C[1] - x[110] / C[1]

    # left hand
    xdot[4] = x[3] / L[2] - Rs[2] * x[4] / L[2] - x[5] / L[2]
    xdot[5] = x[4] / C[2] - x[12] / C[2] - x[14] / C[2] - x[6] / C[2]
    xdot[6] = x[5] / L[7] - Rs[7] * x[6] / L[7] - x[7] / L[7]
    xdot[7] = x[6] / C[7] - x[16] / C[7] - x[18] / C[7] - x[20] / C[7] - x[8] / C[7]
    xdot[8] = x[7] / L[16] - Rs[16] * x[8] / L[16] - x[9] / L[16]
    xdot[9] = x[8] / C[16] - x[22] / C[16] - x[24] / C[16] - x[26] / C[16] - x[10] / C[16]
    xdot[10] = x[9] / L[27] - Rs[27] * x[10] / L[27] - x[11] / L[27]
    xdot[11] = x[10] / C[27] - x[100] / C[27]  # to 42 brachial from axiliary
    xdot[12] = x[5] / L[6] - x[12] * Rs[6] / L[6] - x[13] / L[6]
    xdot[13] = x[12] / C[6] - x[13] / [C[6] * Rp[6]]
    xdot[14] = x[5] / L[8] - x[14] * Rs[8] / L[8] - x[15] / L[8]
    xdot[15] = x[14] / C[8] - x[15] / [C[8] * Rp[8]]
    xdot[16] = x[7] / L[18] - x[16] * Rs[18] / L[18] - x[17] / L[18]
    xdot[17] = x[16] / C[18] - x[17] / [C[18] * Rp[18]]
    xdot[18] = x[7] / L[17] - x[18] * Rs[17] / L[17] - x[19] / L[17]
    xdot[19] = x[18] / C[17] - x[19] / [C[17] * Rp[17]]
    xdot[20] = x[7] / L[15] - x[20] * Rs[15] / L[15] - x[21] / L[15]
    xdot[21] = x[20] / C[15] - x[21] / [C[15] * Rp[15]]
    xdot[22] = x[9] / L[26] - x[22] * Rs[26] / L[26] - x[23] / L[26]
    xdot[23] = x[22] / C[26] - x[23] / [C[26] * Rp[26]]
    xdot[24] = x[9] / L[28] - x[24] * Rs[28] / L[28] - x[25] / L[28]
    xdot[25] = x[24] / C[28] - x[25] / [C[28] * Rp[28]]
    xdot[26] = x[9] / L[29] - x[26] * Rs[29] / L[29] - x[27] / L[29]
    xdot[27] = x[26] / C[29] - x[27] / [C[29] * Rp[29]]

    # upper left extreme
    xdot[28] = x[3] / L[3] - x[28] * Rs[3] / L[3] - x[29] / L[3]
    xdot[29] = x[28] / C[3] - x[54] / C[3]
    xdot[30] = x[29] / L[9] - x[54] * Rs[9] / L[9] - x[31] / L[9]
    xdot[31] = x[54] / C[9] - x[32] / C[9]
    xdot[32] = x[31] / L[19] - x[32] * Rs[19] / L[19] - x[33] / L[19]
    xdot[33] = x[32] / C[19] - x[34] / C[19] - x[44] / C[19] - x[46] / C[19]
    xdot[34] = x[33] / L[30] - x[34] * Rs[30] / L[30] - x[35] / L[30]
    xdot[35] = x[34] / C[30] - x[36] / C[30] - x[56] / C[30] - x[54] / C[30]
    xdot[36] = x[35] / L[43] - x[36] * Rs[43] / L[43] - x[37] / L[43]
    xdot[37] = x[36] / C[43] - x[38] / C[43]
    xdot[38] = x[37] / L[59] - x[38] * Rs[59] / L[59] - x[39] / L[59]
    xdot[39] = x[38] / C[59] - x[40] / C[59] - x[42] / C[59]
    xdot[40] = x[39] / L[72] - x[40] * Rs[72] / L[72] - x[41] / L[72]
    xdot[41] = x[40] / C[72] - x[41] / [C[72] * Rp[72]]
    xdot[42] = x[39] / L[73] - x[42] * Rs[73] / L[73] - x[43] / L[73]
    xdot[43] = x[42] / C[73] - x[43] / [C[73] * Rp[73]]
    xdot[44] = x[33] / L[32] - x[44] * Rs[32] / L[32] - x[45] / L[32]
    xdot[45] = x[44] / C[32] - x[45] / [C[32] * Rp[32]]
    xdot[46] = x[33] / L[31] - x[46] * Rs[31] / L[31] - x[47] / L[31]
    xdot[47] = x[46] / C[31] - x[48] / C[31] - x[50] / C[31] - x[52] / C[31]
    xdot[48] = x[47] / L[45] - x[48] * Rs[45] / L[45] - x[49] / L[45]
    xdot[49] = x[48] / C[45] - x[49] / [C[45] * Rp[45]]
    xdot[50] = x[47] / L[46] - x[50] * Rs[46] / L[46] - x[51] / L[46]
    xdot[51] = x[50] / C[46] - x[51] / [C[46] * Rp[46]]
    xdot[52] = x[47] / L[47] - x[52] * Rs[47] / L[47] - x[53] / L[47]
    xdot[53] = x[52] / C[47] - x[53] / [C[47] * Rp[47]]
    xdot[54] = x[35] / L[44] - x[54] * Rs[44] / L[44] - x[55] / L[44]
    xdot[55] = x[54] / C[44] - x[55] / [C[44] * Rp[44]]
    xdot[56] = x[35] / L[42] - x[56] * Rs[42] / L[42] - x[57] / L[42]
    xdot[57] = x[56] / C[42] - x[57] / [C[42] * Rp[42]]

    #lower extreme minus legs
    xdot[58] = x[3] / L[4] - x[58] * Rs[4] / L[4] - x[59] / L[4]
    xdot[59] = x[58] / C[4] - x[60] / C[4]
    xdot[60] = x[59] / L[10] - x[60] * Rs[10] / L[10] - x[61] / L[10]
    xdot[61] = x[60] / C[10] - x[62] / C[10]
    xdot[62] = x[61] / L[20] - x[62] * Rs[20] / L[20] - x[63] / L[20]
    xdot[63] = x[62] / C[20] - x[64] / C[20]
    xdot[64] = x[63] / L[33] - x[64] * Rs[33] / L[33] - x[65] / L[33]
    xdot[65] = x[64] / C[33] - x[124] / C[33] - x[66] / C[33]  # connection
    xdot[66] = x[65] / L[49] - x[66] * Rs[49] / L[49] - x[67] / L[49]
    xdot[67] = x[66] / C[49] - x[120] / C[49]

    #left-leg
    xdot[68] = x[123] / L[83] - x[68] * Rs[83] / L[83] - x[69] / L[83]
    xdot[69] = x[68] / C[83] - x[90] / C[83] - x[70] / C[83]
    xdot[70] = x[69] / L[91] - x[70] * Rs[91] / L[91] - x[71] / L[91]
    xdot[71] = x[70] / C[91] - x[72] / C[91]
    xdot[72] = x[71] / L[98] - x[72] * Rs[98] / L[98] - x[73] / L[98]
    xdot[73] = x[72] / C[98] - x[74] / C[98] - x[92] / C[98]
    xdot[74] = x[73] / L[106] - x[74] * Rs[106] / L[106] - x[75] / L[106]
    xdot[75] = x[74] / C[106] - x[76] / C[106]
    xdot[76] = x[75] / L[109] - x[76] * Rs[109] / L[109] - x[77] / L[109]
    xdot[77] = x[76] / C[109] - x[78] / C[109]
    xdot[78] = x[77] / L[111] - x[78] * Rs[111] / L[111] - x[79] / L[111]
    xdot[79] = x[78] / C[111] - x[80] / C[111]
    xdot[80] = x[79] / L[113] - x[80] * Rs[113] / L[113] - x[81] / L[113]
    xdot[81] = x[80] / C[113] - x[82] / C[113] - x[86] / C[113]
    xdot[82] = x[81] / L[117] - x[82] * Rs[117] / L[117] - x[83] / L[117]
    xdot[83] = x[82] / C[117] - x[84] / C[117] - x[88] / C[117]
    xdot[84] = x[83] / L[123] - x[84] * Rs[123] / L[123] - x[85] / L[123]
    xdot[85] = x[84] / C[123] - x[96] / C[123]
    xdot[86] = x[81] / L[116] - x[86] * Rs[115] / L[116] - x[87] / L[116]
    xdot[87] = x[86] / C[116] - x[94] / C[116]
    xdot[88] = x[83] / L[122] - x[88] * Rs[122] / L[122] - x[89] / L[122]
    xdot[89] = x[88] / C[122] - x[98] / C[122]
    xdot[90] = x[69] / L[90] - x[90] * Rs[90] / L[90] - x[91] / L[90]
    xdot[91] = x[90] / C[90] - x[91] / [C[90] * Rp[90]]
    xdot[92] = x[73] / L[105] - x[92] * Rs[105] / L[105] - x[93] / L[105]
    xdot[93] = x[92] / C[105] - x[93] / [C[105] * Rp[105]]
    xdot[94] = x[87] / L[121] - x[94] * Rs[121] / L[121] - x[95] / L[121]
    xdot[95] = x[94] / C[121] - x[95] / [C[121] * Rp[121]]
    xdot[96] = x[84] / L[127] - x[96] * Rs[127] / L[127] - x[97] / L[127]
    xdot[97] = x[96] / C[127] - x[97] / [C[127] * Rp[127]]
    xdot[98] = x[89] / L[126] - x[98] * Rs[126] / L[126] - x[99] / L[126]
    xdot[99] = x[98] / C[126] - x[99] / [C[126] * Rp[126]]

    #lower left arm
    xdot[100] = x[11] / L[41] - x[100] * Rs[41] / L[41] - x[101] / L[41]
    xdot[101] = x[100] / C[41] - x[102] / C[41] - x[112] / C[41]

    xdot[102] = x[101] / L[58] - Rs[58] * x[102] / L[58] - x[103] / L[58]
    xdot[103] = x[102] / C[58] - x[114] / C[58] - x[104] / C[58]
    xdot[104] = x[103] / L[70] - Rs[70] * x[104] / L[70] - x[105] / L[70]
    xdot[105] = x[104] / C[70] - x[116] / C[70] - x[106] / C[70]

    xdot[106] = x[105] / L[80] - Rs[80] * x[106] / L[80] - x[107] / L[80]
    xdot[107] = x[106] / C[80] - x[118] / C[80] - x[108] / C[80]

    xdot[108] = x[107] / L[86] - Rs[86] * x[108] / L[86] - x[109] / L[86]
    xdot[109] = x[108] / C[86] - x[110] / C[86] - x[120] / C[86]

    xdot[110] = x[109] / L[94] - x[110] * Rs[94] / L[94] - x[111] / L[94]
    xdot[111] = x[110] / C[94] - x[122] / C[94]  # to 103 ulnar 3

    xdot[112] = x[101] / L[57] - x[112] * Rs[57] / L[57] - x[113] / L[57]
    xdot[113] = x[112] / C[57] - x[113] / [C[57] * Rp[57]]

    xdot[114] = x[103] / L[71] - x[114] * Rs[71] / L[71] - x[115] / L[71]
    xdot[115] = x[114] / C[71] - x[115] / [C[71] * Rp[71]]
    xdot[116] = x[105] / L[79] - x[116] * Rs[79] / L[79] - x[117] / L[79]
    xdot[117] = x[116] / C[79] - x[117] / [C[79] * Rp[79]]

    xdot[118] = x[107] / L[87] - x[118] * Rs[87] / L[87] - x[119] / L[87]
    xdot[119] = x[118] / C[87] - x[124] / C[87]  # to 97 radial 2

    xdot[120] = x[109] / L[95] - x[120] * Rs[95] / L[95] - x[121] / L[95]
    xdot[121] = x[120] / C[95] - x[121] / [C[95] * Rp[95]]

    # to 103 ulnar 3
    xdot[122] = x[111] / L[102] - x[122] * Rs[102] / L[102] - x[123] / L[102]
    xdot[123] = x[122] / C[102] - x[123] / [C[102] * Rp[102]]
    # to 97 radial 2
    xdot[124] = x[119] / L[96] - x[124] * Rs[96] / L[96] - x[125] / L[96]
    xdot[125] = x[124] / C[96] - x[125] / [C[96] * Rp[96]]

    return xdot

def p_wav(x,a_pwav,d_pwav,t_pwav,li):
    l=li
    a=a_pwav
    x=x+t_pwav
    b=(2*l)/d_pwav
    n=100
    p1=1/l
    p2=0
    for i in range(1,n):
        harm1=(((np.sin((math.pi/(2*b))*(b-(2*i))))/(b-(2*i))+(np.sin((math.pi/(2*b))*(b+(2*i))))/(b+(2*i)))*(2/math.pi))*np.cos((i*math.pi*x)/l)
        p2=p2+harm1

    pwav1=p1+p2
    pwav=a*pwav1

    return [pwav]

def qrs_wav(x,a_qrswav,d_qrswav,li):
    l=li
    a=a_qrswav
    b=(2*l)/d_qrswav
    n=100
    qrs1=(a/(2*b))*(2-b)
    qrs2=0

    for i in range(1,n):
        harm=(((2*b*a)/(i*i*math.pi*math.pi))*(1-np.cos((i*math.pi)/b)))*np.cos((i*math.pi*x)/l)
        qrs2=qrs2+harm

    qrswav=qrs1+qrs2

    return [qrswav]

def q_wav(x,a_qwav,d_qwav,t_qwav,li):
    l=li
    x=x+t_qwav
    a=a_qwav
    b=(2*l)/d_qwav
    n=100
    q1=(a/(2*b))*(2-b)
    q2=0
    for i in range(1,n):
        harm5=(((2*b*a)/(i*i*math.pi*math.pi))*(1-np.cos((i*math.pi)/b)))*np.cos((i*math.pi*x)/l)
        q2=q2+harm5

    qwav=-1*(q1+q2)

    return [qwav]

def s_wav(x,a_swav,d_swav,t_swav,li):
    l=li
    x=x-t_swav
    a=a_swav
    b=(2*l)/d_swav
    n=100
    s1=(a/(2*b))*(2-b)
    s2=0
    for i in range(1,n):
        harm3=(((2*b*a)/(i*i*math.pi*math.pi))*(1-np.cos((i*math.pi)/b)))*np.cos((i*math.pi*x)/l)
        s2=s2+harm3

    swav=-1*(s1+s2)

    return [swav]

def t_wav(x,a_twav,d_twav,t_twav,li):
    l=li
    a=a_twav
    x=x-t_twav-0.045
    b=(2*l)/d_twav
    n=100
    t1=1/l
    t2=0
    for i in range(1,n):
        harm2=(((np.sin((math.pi/(2*b))*(b-(2*i))))/(b-(2*i))+(np.sin((math.pi/(2*b))*(b+(2*i))))/(b+(2*i)))*(2/math.pi))*np.cos((i*math.pi*x)/l)
        t2=t2+harm2

    twav1=t1+t2
    twav=a*twav1

    return [twav]

def u_wav(x,a_uwav,d_uwav,t_uwav,li):
    l=li
    a=a_uwav
    x=x-t_uwav
    b=(2*l)/d_uwav
    n=100
    u1=1/l
    u2=0
    for i in range(1,n):
        harm4=(((np.sin((math.pi/(2*b))*(b-(2*i))))/(b-(2*i))+(np.sin((math.pi/(2*b))*(b+(2*i))))/(b+(2*i)))*(2/math.pi))*np.cos((i*math.pi*x)/l)
        u2=u2+harm4

    uwav1=u1+u2
    uwav=a*uwav1

    return [uwav]





stecg = 0.60008
etecg = 1.4
dtecg = 0.00008
ecg = []

path = 'pycall/Datas/rlcnewval.txt'
rlctru = np.genfromtxt(path, delimiter=',')
Rs = rlctru[:, 0]
L = rlctru[:, 1]
C = rlctru[:, 2]
Rp = rlctru[:, 3]
dt = 0.002

# All dynamic values
pgen = np.zeros(shape=(2,1))
sgen = np.zeros(126)
i = 0
st = 0
et = 1

n = 2

while i < n:

    HR = 72
    PF = 450

    #############################################################

    ecgClock = np.arange(0, 1, dtecg)

    li = 30 / HR

    a_pwav = 0.25
    d_pwav = 0.09
    t_pwav = 0.16

    a_qwav = 0.025
    d_qwav = 0.066
    t_qwav = 0.166

    a_qrswav = 1.6
    d_qrswav = 0.11

    a_swav = 0.25
    d_swav = 0.066
    t_swav = 0.09

    a_twav = 0.35
    d_twav = 0.142
    t_twav = 0.2

    a_uwav = 0.035
    d_uwav = 0.0476/ 40
    t_uwav = 0.433 / 100

    pwav = p_wav(ecgClock, a_pwav, d_pwav, t_pwav, li)

    qwav = q_wav(ecgClock, a_qwav, d_qwav, t_qwav, li)

    qrswav = qrs_wav(ecgClock, a_qrswav, d_qrswav, li)

    swav = s_wav(ecgClock, a_swav, d_swav, t_swav, li)

    twav = t_wav(ecgClock, a_twav, d_twav, t_twav, li)

    uwav = u_wav(ecgClock, a_uwav, d_uwav, t_uwav, li)

    temp = np.add(pwav, qrswav)
    temp = np.add(temp, twav)
    temp = np.add(temp, swav)
    temp = np.add(temp, qwav)
    temp = np.add(temp, uwav)

    ecg = np.append(ecg, temp)

    stecg = stecg + 0.79992
    etecg = etecg + 0.79992

    #############################################################



    T = 60 / HR
    clock = np.arange(0, et, dt)
    t1 = clock / T
    t2 = t1 - np.floor(t1)
    t3 = np.multiply(T, t2)
    x1 = PF * (np.square(np.sin(3.14 * t3 / 0.3)))
    x2 = np.floor(t3 + 0.7)
    R1 = 0.11
    L = 0.011
    R2 = 1.11
    C = 0.91
    it = np.multiply((1 - x2), x1)

    srt = time.time()

    pulse_generator = lambda t, x: pulsegen(t, x, R1, L, R2, C, clock, it)
    output_pulse = solve_ivp(pulse_generator, [st, et], [pgen[0, -1], pgen[1, -1]], method='Radau',
                             t_eval=np.arange(st,et,dt))

    x = output_pulse.y

    if i == 0:
        pgen = np.delete(pgen, 0, 1)

    pgen = np.append(pgen, x, axis=1)
    pu = it.transpose()

    pulse = (pu - pgen[0, :]) * R1 + pgen[1, :]

    system_finder = lambda t, x: integrated_ode(t, x, pulse, clock)

    if i == 0:
        sol = solve_ivp(system_finder, [st, et], sgen, method='Radau', t_eval=np.arange(st,et,dt))
        xo = sol.y
    else:
        sol = solve_ivp(system_finder, [st, et], sgen[:, -1], method='Radau', t_eval=np.arange(st,et,dt))
        xo = sol.y

    if i == 0:
        sgen = xo
    else:
        sgen = np.append(sgen, xo, axis=1)

    ent = time.time()

    print(ent-srt)

    st = st+1
    et = et+1
    i = i+1


plt.figure(1)
plt.subplot(211)
plt.plot(np.arange(np.size(ecg)-5083), ecg[5083:])
plt.subplot(212)
plt.plot(clock, sgen[1,:])

plt.show()




#plt.plot(clock, sgen[1,:])
#plt.show()