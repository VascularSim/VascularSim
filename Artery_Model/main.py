from ecg import ecg_simulate_ecgsyn
import numpy as np
from scipy.integrate import solve_ivp
import scipy.signal as signal
import sqlite3 as sql
import time
from collections import deque


def pulsegen(t, x, clock, it):
    i1 = np.interp(t, clock, it)
    xdot = [[0.0], [0.0]]
    xdot[0] = -10 * x[0] + 10 * i1
    xdot[1] = -0.99 * x[1] + 1.0989 * i1
    return xdot

def system_simulator(t, x, Vin, clock):

    connection = sql.connect("vascularsim.db")
    cursor = connection.cursor()
    cursor.execute("SELECT STENOSIS_FLAG FROM HPN WHERE ID = 1")
    rows = cursor.fetchone()
    stenosis_flag = rows[0]
    connection.close()
    
    if stenosis_flag == 0:
        RLC = np.genfromtxt('Artery_Model/Data/ARTERY_RLC.txt', delimiter=',')
    else: 
        RLC = np.genfromtxt('Artery_Model/Data/STENOSIS_RLC.txt', delimiter=',')
    
    Rs = RLC[:, 0]
    L = RLC[:, 1]
    C = RLC[:, 2]
    Rp = RLC[:, 3]
    Vin = np.interp(t, clock, Vin)
    xdot = np.zeros(256, dtype=np.float64)

    # Aortic subsystem
    xdot[0] = Vin / L[0] - x[0] * Rs[0] / L[0] - x[1] / L[0]
    xdot[1] = x[0] / C[0] - x[2] / C[0]
    xdot[2] = x[1] / L[1] - x[2] * Rs[1] / L[1] - x[3] / L[1]
    xdot[3] = x[2] / C[1] - x[52] / C[1] - x[4] / C[1] - x[28] / C[1] - x[110] / C[1]

    # to upper_extreme,lower_extreme,left hand, right hand,etc......
    # left hand
    xdot[4] = x[3] / L[2] - Rs[2] * x[4] / L[2] - x[5] / L[2]
    xdot[5] = x[4] / C[2] - x[12] / C[2] - x[14] / C[2] - x[6] / C[2]
    xdot[6] = x[5] / L[7] - Rs[7] * x[6] / L[7] - x[7] / L[7]
    xdot[7] = x[6] / C[7] - x[16] / C[7] - x[18] / C[7] - x[20] / C[7] - x[8] / C[7]
    xdot[8] = x[7] / L[16] - Rs[16] * x[8] / L[16] - x[9] / L[16]
    xdot[9] = x[8] / C[16] - x[22] / C[16] - x[24] / C[16] - x[26] / C[16] - x[10] / C[16]
    xdot[10] = x[9] / L[27] - Rs[27] * x[10] / L[27] - x[11] / L[27]
    xdot[11] = x[10] / C[27] - x[204] / C[27]  # to 42 brachial from axiliary
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

    # right hand
    xdot[28] = x[3] / L[5] - Rs[5] * x[28] / L[5] - x[29] / L[5]
    xdot[29] = x[28] / C[5] - x[36] / C[5] - x[38] / C[5] - x[30] / C[5] - x[82] / C[5]

    # to brachiocepahlic
    xdot[30] = x[29] / L[13] - Rs[13] * x[30] / L[13] - x[31] / L[13]
    xdot[31] = x[30] / C[13] - x[40] / C[13] - x[42] / C[13] - x[44] / C[13] - x[32] / C[13]
    xdot[32] = x[31] / L[24] - Rs[24] * x[32] / L[24] - x[33] / L[24]
    xdot[33] = x[32] / C[24] - x[46] / C[24] - x[48] / C[24] - x[50] / C[24] - x[34] / C[24]
    xdot[34] = x[33] / L[39] - Rs[39] * x[34] / L[39] - x[35] / L[39]
    xdot[35] = x[34] / C[39] - x[206] / C[39]  # to 57 brachial
    xdot[36] = x[29] / L[14] - x[36] * Rs[14] / L[14] - x[37] / L[14]
    xdot[37] = x[36] / C[14] - x[37] / [C[14] * Rp[14]]
    xdot[38] = x[29] / L[12] - x[38] * Rs[12] / L[12] - x[39] / L[12]
    xdot[39] = x[38] / C[12] - x[39] / [C[12] * Rp[12]]
    xdot[40] = x[31] / L[22] - x[50] * Rs[22] / L[22] - x[41] / L[22]
    xdot[41] = x[40] / C[22] - x[41] / [C[22] * Rp[22]]
    xdot[42] = x[31] / L[23] - x[42] * Rs[23] / L[23] - x[43] / L[23]
    xdot[43] = x[42] / C[23] - x[43] / [C[23] * Rp[23]]
    xdot[44] = x[31] / L[25] - x[44] * Rs[25] / L[25] - x[45] / L[25]
    xdot[45] = x[44] / C[25] - x[45] / [C[25] * Rp[25]]
    xdot[46] = x[33] / L[40] - x[46] * Rs[40] / L[40] - x[47] / L[40]
    xdot[47] = x[46] / C[40] - x[47] / [C[40] * Rp[40]]
    xdot[48] = x[33] / L[38] - x[48] * Rs[38] / L[38] - x[49] / L[38]
    xdot[49] = x[48] / C[38] - x[49] / [C[38] * Rp[38]]
    xdot[50] = x[33] / L[37] - x[50] * Rs[29] / L[37] - x[51] / L[37]
    xdot[51] = x[50] / C[37] - x[51] / [C[37] * Rp[37]]

    # upper left extreme
    xdot[52] = x[3] / L[3] - x[52] * Rs[3] / L[3] - x[53] / L[3]
    xdot[53] = x[52] / C[3] - x[54] / C[3]
    xdot[54] = x[53] / L[9] - x[54] * Rs[9] / L[9] - x[55] / L[9]
    xdot[55] = x[54] / C[9] - x[56] / C[9]
    xdot[56] = x[55] / L[19] - x[56] * Rs[19] / L[19] - x[57] / L[19]
    xdot[57] = x[56] / C[19] - x[58] / C[19] - x[68] / C[19] - x[70] / C[19]
    xdot[58] = x[57] / L[30] - x[58] * Rs[30] / L[30] - x[59] / L[30]
    xdot[59] = x[58] / C[30] - x[60] / C[30] - x[80] / C[30] - x[78] / C[30]
    xdot[60] = x[59] / L[43] - x[60] * Rs[43] / L[43] - x[61] / L[43]
    xdot[61] = x[60] / C[43] - x[62] / C[43]
    xdot[62] = x[61] / L[59] - x[62] * Rs[59] / L[59] - x[63] / L[59]
    xdot[63] = x[62] / C[59] - x[64] / C[59] - x[66] / C[59]
    xdot[64] = x[63] / L[72] - x[64] * Rs[72] / L[72] - x[65] / L[72]
    xdot[65] = x[64] / C[72] - x[65] / [C[72] * Rp[72]]
    xdot[66] = x[63] / L[73] - x[66] * Rs[73] / L[73] - x[67] / L[73]
    xdot[67] = x[66] / C[73] - x[67] / [C[73] * Rp[73]]
    xdot[68] = x[57] / L[32] - x[68] * Rs[32] / L[32] - x[69] / L[32]
    xdot[69] = x[68] / C[32] - x[69] / [C[32] * Rp[32]]
    xdot[70] = x[57] / L[31] - x[70] * Rs[31] / L[31] - x[71] / L[31]
    xdot[71] = x[70] / C[31] - x[72] / C[31] - x[74] / C[31] - x[76] / C[31]
    xdot[72] = x[71] / L[45] - x[72] * Rs[45] / L[45] - x[73] / L[45]
    xdot[73] = x[72] / C[45] - x[73] / [C[45] * Rp[45]]
    xdot[74] = x[71] / L[46] - x[74] * Rs[46] / L[46] - x[75] / L[46]
    xdot[75] = x[74] / C[46] - x[75] / [C[46] * Rp[46]]
    xdot[76] = x[71] / L[47] - x[76] * Rs[47] / L[47] - x[77] / L[47]
    xdot[77] = x[76] / C[47] - x[77] / [C[47] * Rp[47]]
    xdot[78] = x[59] / L[44] - x[78] * Rs[44] / L[44] - x[79] / L[44]
    xdot[79] = x[78] / C[44] - x[79] / [C[44] * Rp[44]]
    xdot[80] = x[59] / L[42] - x[80] * Rs[42] / L[42] - x[81] / L[42]
    xdot[81] = x[80] / C[42] - x[81] / [C[42] * Rp[42]]

    # upper right extreme
    xdot[82] = x[29] / L[11] - x[82] * Rs[11] / L[11] - x[83] / L[11]
    xdot[83] = x[82] / C[11] - x[84] / C[11]
    xdot[84] = x[83] / L[21] - x[84] * Rs[21] / L[21] - x[85] / L[21]
    xdot[85] = x[84] / C[21] - x[86] / C[21] - x[96] / C[21] - x[98] / C[21]
    xdot[86] = x[85] / L[36] - x[86] * Rs[36] / L[36] - x[87] / L[36]
    xdot[87] = x[86] / C[36] - x[88] / C[36] - x[108] / C[36] - x[106] / C[36]
    xdot[88] = x[87] / L[54] - x[88] * Rs[54] / L[54] - x[89] / L[54]
    xdot[89] = x[88] / C[54] - x[90] / C[54]
    xdot[90] = x[89] / L[67] - x[90] * Rs[67] / L[67] - x[91] / L[67]
    xdot[91] = x[90] / C[67] - x[92] / C[67] - x[94] / C[67]
    xdot[92] = x[91] / L[76] - x[92] * Rs[76] / L[76] - x[93] / L[76]
    xdot[93] = x[92] / C[76] - x[93] / [C[76] * Rp[76]]
    xdot[94] = x[91] / L[75] - x[94] * Rs[75] / L[75] - x[95] / L[75]
    xdot[95] = x[94] / C[75] - x[95] / [C[75] * Rp[75]]
    xdot[96] = x[85] / L[34] - x[96] * Rs[34] / L[34] - x[87] / L[34]
    xdot[97] = x[96] / C[34] - x[97] / [C[34] * Rp[34]]
    xdot[98] = x[85] / L[35] - x[98] * Rs[35] / L[35] - x[99] / L[35]
    xdot[99] = x[98] / C[35] - x[100] / C[35] - x[102] / C[35] - x[104] / C[35]
    xdot[100] = x[99] / L[50] - x[100] * Rs[50] / L[50] - x[101] / L[50]
    xdot[101] = x[100] / C[50] - x[101] / [C[50] * Rp[50]]
    xdot[102] = x[99] / L[51] - x[102] * Rs[51] / L[51] - x[103] / L[51]
    xdot[103] = x[102] / C[51] - x[103] / [C[51] * Rp[51]]
    xdot[104] = x[99] / L[52] - x[104] * Rs[52] / L[52] - x[105] / L[52]
    xdot[105] = x[104] / C[52] - x[105] / [C[52] * Rp[52]]
    xdot[106] = x[87] / L[53] - x[106] * Rs[53] / L[53] - x[107] / L[53]
    xdot[107] = x[106] / C[53] - x[107] / [C[53] * Rp[53]]
    xdot[108] = x[87] / L[55] - x[108] * Rs[55] / L[55] - x[109] / L[55]
    xdot[109] = x[108] / C[55] - x[109] / [C[55] * Rp[55]]

    # lower extreme minus legs
    xdot[110] = x[3] / L[4] - x[110] * Rs[4] / L[4] - x[111] / L[4]
    xdot[111] = x[110] / C[4] - x[112] / C[4]
    xdot[112] = x[111] / L[10] - x[112] * Rs[10] / L[10] - x[113] / L[10]
    xdot[113] = x[112] / C[10] - x[114] / C[10]
    xdot[114] = x[113] / L[20] - x[114] * Rs[20] / L[20] - x[115] / L[20]
    xdot[115] = x[114] / C[20] - x[116] / C[20]
    xdot[116] = x[115] / L[33] - x[116] * Rs[33] / L[33] - x[117] / L[33]
    xdot[117] = x[116] / C[33] - x[124] / C[33] - x[118] / C[33]  # connection
    xdot[118] = x[117] / L[49] - x[118] * Rs[49] / L[49] - x[119] / L[49]
    xdot[119] = x[118] / C[49] - x[120] / C[49] - x[132] / C[49] - x[134] / C[49] - x[136] / C[49]

    # connection
    xdot[120] = x[119] / L[64] - x[120] * Rs[64] / L[64] - x[121] / L[64]
    xdot[121] = x[120] / C[64] - x[122] / C[64]
    xdot[122] = x[121] / L[74] - x[122] * Rs[74] / L[74] - x[123] / L[74]
    xdot[123] = x[122] / C[74] - x[138] / C[74] - x[140] / C[74] - x[172] / C[74]  # to left and right leg

    # branches
    xdot[124] = x[117] / L[48] - x[124] * Rs[48] / L[48] - x[125] / L[48]
    xdot[125] = x[124] / C[48] - x[126] / C[48] - x[128] / C[48] - x[130] / C[48]

    # terminals
    xdot[126] = x[125] / L[60] - x[126] * Rs[60] / L[60] - x[127] / L[60]
    xdot[127] = x[126] / C[60] - x[127] / [C[60] * Rp[60]]
    xdot[128] = x[125] / L[61] - x[128] * Rs[61] / L[61] - x[129] / L[61]
    xdot[129] = x[128] / C[61] - x[129] / [C[61] * Rp[61]]
    xdot[130] = x[125] / L[62] - x[130] * Rs[62] / L[62] - x[131] / L[62]
    xdot[131] = x[130] / C[62] - x[131] / [C[62] * Rp[62]]
    xdot[132] = x[119] / L[63] - x[132] * Rs[63] / L[63] - x[133] / L[63]
    xdot[133] = x[132] / C[63] - x[133] / [C[63] * Rp[63]]
    xdot[134] = x[119] / L[65] - x[134] * Rs[65] / L[65] - x[135] / L[65]
    xdot[135] = x[134] / C[65] - x[135] / [C[65] * Rp[65]]
    xdot[136] = x[119] / L[66] - x[136] * Rs[66] / L[66] - x[137] / L[66]
    xdot[137] = x[136] / C[66] - x[137] / [C[66] * Rp[66]]
    xdot[138] = x[123] / L[82] - x[138] * Rs[82] / L[82] - x[139] / L[82]
    xdot[139] = x[138] / C[82] - x[139] / [C[82] * Rp[82]]

    # left leg
    xdot[140] = x[123] / L[81] - x[140] * Rs[81] / L[81] - x[141] / L[81]
    xdot[141] = x[140] / C[81] - x[162] / C[81] - x[142] / C[81]
    xdot[142] = x[141] / L[88] - x[142] * Rs[88] / L[88] - x[143] / L[88]
    xdot[143] = x[142] / C[88] - x[144] / C[88]
    xdot[144] = x[143] / L[97] - x[144] * Rs[97] / L[97] - x[145] / L[97]
    xdot[145] = x[144] / C[97] - x[146] / C[97] - x[164] / C[97]
    xdot[146] = x[145] / L[103] - x[146] * Rs[103] / L[103] - x[147] / L[103]
    xdot[147] = x[146] / C[103] - x[148] / C[103]
    xdot[148] = x[147] / L[108] - x[148] * Rs[108] / L[108] - x[149] / L[108]
    xdot[149] = x[148] / C[108] - x[150] / C[108]
    xdot[150] = x[149] / L[110] - x[150] * Rs[110] / L[110] - x[151] / L[110]
    xdot[151] = x[150] / C[110] - x[152] / C[110]
    xdot[152] = x[151] / L[112] - x[152] * Rs[112] / L[112] - x[153] / L[112]
    xdot[153] = x[152] / C[112] - x[154] / C[112] - x[158] / C[112]
    xdot[154] = x[153] / L[114] - x[154] * Rs[114] / L[114] - x[155] / L[114]
    xdot[155] = x[154] / C[114] - x[156] / C[114] - x[160] / C[114]
    xdot[156] = x[155] / L[118] - x[156] * Rs[118] / L[118] - x[157] / L[118]
    xdot[157] = x[156] / C[118] - x[168] / C[118]
    xdot[158] = x[153] / L[115] - x[158] * Rs[115] / L[115] - x[159] / L[115]
    xdot[159] = x[158] / C[115] - x[166] / C[115]
    xdot[160] = x[155] / L[119] - x[160] * Rs[119] / L[119] - x[161] / L[119]
    xdot[161] = x[160] / C[119] - x[170] / C[119]
    xdot[162] = x[141] / L[89] - x[162] * Rs[89] / L[89] - x[163] / L[89]
    xdot[163] = x[162] / C[89] - x[163] / [C[89] * Rp[89]]
    xdot[164] = x[145] / L[104] - x[164] * Rs[104] / L[104] - x[165] / L[104]
    xdot[165] = x[164] / C[104] - x[165] / [C[104] * Rp[104]]
    xdot[166] = x[159] / L[120] - x[166] * Rs[120] / L[120] - x[167] / L[120]
    xdot[167] = x[166] / C[120] - x[167] / [C[120] * Rp[120]]
    xdot[168] = x[157] / L[124] - x[168] * Rs[124] / L[124] - x[169] / L[124]
    xdot[169] = x[168] / C[124] - x[169] / [C[124] * Rp[124]]
    xdot[170] = x[161] / L[125] - x[170] * Rs[125] / L[125] - x[171] / L[125]
    xdot[171] = x[170] / C[125] - x[171] / [C[125] * Rp[125]]

    # right leg
    xdot[172] = x[123] / L[83] - x[172] * Rs[83] / L[83] - x[173] / L[83]
    xdot[173] = x[172] / C[83] - x[194] / C[83] - x[174] / C[83]
    xdot[174] = x[173] / L[91] - x[174] * Rs[91] / L[91] - x[175] / L[91]
    xdot[175] = x[174] / C[91] - x[176] / C[91]
    xdot[176] = x[175] / L[98] - x[176] * Rs[98] / L[98] - x[177] / L[98]
    xdot[177] = x[176] / C[98] - x[178] / C[98] - x[196] / C[98]
    xdot[178] = x[177] / L[106] - x[178] * Rs[106] / L[106] - x[179] / L[106]
    xdot[179] = x[178] / C[106] - x[180] / C[106]
    xdot[180] = x[179] / L[109] - x[180] * Rs[109] / L[109] - x[181] / L[109]
    xdot[181] = x[180] / C[109] - x[182] / C[109]
    xdot[182] = x[181] / L[111] - x[182] * Rs[111] / L[111] - x[183] / L[111]
    xdot[183] = x[182] / C[111] - x[184] / C[111]
    xdot[184] = x[183] / L[113] - x[184] * Rs[113] / L[113] - x[185] / L[113]
    xdot[185] = x[184] / C[113] - x[186] / C[113] - x[190] / C[113]
    xdot[186] = x[185] / L[117] - x[186] * Rs[117] / L[117] - x[187] / L[117]
    xdot[187] = x[186] / C[117] - x[188] / C[117] - x[192] / C[117]
    xdot[188] = x[187] / L[123] - x[188] * Rs[123] / L[123] - x[189] / L[123]
    xdot[189] = x[188] / C[123] - x[200] / C[123]
    xdot[190] = x[185] / L[116] - x[190] * Rs[115] / L[116] - x[191] / L[116]
    xdot[191] = x[190] / C[116] - x[198] / C[116]
    xdot[192] = x[187] / L[122] - x[192] * Rs[122] / L[122] - x[193] / L[122]
    xdot[193] = x[192] / C[122] - x[202] / C[122]
    xdot[194] = x[173] / L[90] - x[194] * Rs[90] / L[90] - x[195] / L[90]
    xdot[195] = x[194] / C[90] - x[195] / [C[90] * Rp[90]]
    xdot[196] = x[177] / L[105] - x[196] * Rs[105] / L[105] - x[197] / L[105]
    xdot[197] = x[196] / C[105] - x[197] / [C[105] * Rp[105]]
    xdot[198] = x[191] / L[121] - x[198] * Rs[121] / L[121] - x[199] / L[121]
    xdot[199] = x[198] / C[121] - x[199] / [C[121] * Rp[121]]
    xdot[200] = x[188] / L[127] - x[200] * Rs[127] / L[127] - x[201] / L[127]
    xdot[201] = x[200] / C[127] - x[201] / [C[127] * Rp[127]]
    xdot[202] = x[193] / L[126] - x[202] * Rs[126] / L[126] - x[203] / L[126]
    xdot[203] = x[202] / C[126] - x[203] / [C[126] * Rp[126]]

    # brachial arteries
    xdot[204] = x[11] / L[41] - x[204] * Rs[41] / L[41] - x[205] / L[41]
    xdot[205] = x[204] / C[41] - x[208] / C[41] - x[218] / C[41]  # To lower left arm
    xdot[206] = x[35] / L[56] - x[206] * Rs[56] / L[56] - x[207] / L[56]
    xdot[207] = x[206] / C[56] - x[228] / C[58] - x[238] / C[56]  # To lower right arm

    # lower left arm
    xdot[208] = x[205] / L[58] - Rs[58] * x[208] / L[58] - x[209] / L[58]
    xdot[209] = x[208] / C[58] - x[220] / C[58] - x[210] / C[58]
    xdot[210] = x[209] / L[70] - Rs[70] * x[210] / L[70] - x[211] / L[70]
    xdot[211] = x[210] / C[70] - x[222] / C[70] - x[212] / C[70]
    xdot[212] = x[211] / L[80] - Rs[80] * x[212] / L[80] - x[213] / L[80]
    xdot[213] = x[212] / C[80] - x[224] / C[80] - x[214] / C[80]
    xdot[214] = x[213] / L[86] - Rs[86] * x[214] / L[86] - x[215] / L[86]
    xdot[215] = x[214] / C[86] - x[216] / C[86] - x[226] / C[86]
    xdot[216] = x[215] / L[94] - x[216] * Rs[94] / L[94] - x[217] / L[94]
    xdot[217] = x[216] / C[94] - x[248] / C[94]  # to 103 ulnar 3
    xdot[218] = x[205] / L[57] - x[218] * Rs[57] / L[57] - x[219] / L[57]
    xdot[219] = x[218] / C[57] - x[219] / [C[57] * Rp[57]]
    xdot[220] = x[209] / L[71] - x[220] * Rs[71] / L[71] - x[221] / L[71]
    xdot[221] = x[220] / C[71] - x[221] / [C[71] * Rp[71]]
    xdot[222] = x[211] / L[79] - x[222] * Rs[79] / L[79] - x[223] / L[79]
    xdot[223] = x[222] / C[79] - x[223] / [C[79] * Rp[79]]
    xdot[224] = x[213] / L[87] - x[224] * Rs[87] / L[87] - x[225] / L[87]
    xdot[225] = x[224] / C[87] - x[250] / C[87]  # to 97 radial 2
    xdot[226] = x[215] / L[95] - x[226] * Rs[95] / L[95] - x[227] / L[95]
    xdot[227] = x[226] / C[95] - x[227] / [C[95] * Rp[95]]

    # lower right arm
    xdot[228] = x[207] / L[68] - Rs[68] * x[228] / L[68] - x[229] / L[68]
    xdot[229] = x[228] / C[68] - x[240] / C[68] - x[230] / C[68]
    xdot[230] = x[229] / L[78] - Rs[78] * x[230] / L[78] - x[231] / L[78]
    xdot[231] = x[230] / C[78] - x[242] / C[78] - x[232] / C[78]
    xdot[232] = x[231] / L[84] - Rs[84] * x[232] / L[84] - x[233] / L[84]
    xdot[233] = x[232] / C[84] - x[244] / C[84] - x[234] / C[84]
    xdot[234] = x[233] / L[93] - Rs[93] * x[234] / L[93] - x[235] / L[93]
    xdot[235] = x[234] / C[93] - x[236] / C[93] - x[246] / C[93]
    xdot[236] = x[235] / L[101] - x[236] * Rs[101] / L[101] - x[237] / L[101]
    xdot[237] = x[236] / C[101] - x[252] / C[101]  # to 103 ulnar 3
    xdot[238] = x[207] / L[69] - x[238] * Rs[69] / L[69] - x[239] / L[69]
    xdot[239] = x[238] / C[69] - x[239] / [C[69] * Rp[69]]
    xdot[240] = x[229] / L[71] - x[240] * Rs[71] / L[71] - x[241] / L[71]
    xdot[241] = x[240] / C[71] - x[241] / [C[71] * Rp[71]]
    xdot[242] = x[231] / L[85] - x[242] * Rs[85] / L[85] - x[243] / L[85]
    xdot[243] = x[242] / C[85] - x[243] / [C[85] * Rp[85]]
    xdot[244] = x[233] / L[92] - x[224] * Rs[92] / L[92] - x[225] / L[92]
    xdot[245] = x[244] / C[92] - x[254] / C[92]  # to 97 radial 2
    xdot[246] = x[235] / L[100] - x[246] * Rs[100] / L[100] - x[247] / L[100]
    xdot[247] = x[246] / C[100] - x[247] / [C[100] * Rp[100]]

    # to 103 ulnar 3
    xdot[248] = x[217] / L[102] - x[248] * Rs[102] / L[102] - x[249] / L[102]
    xdot[249] = x[248] / C[102] - x[249] / [C[102] * Rp[102]]

    # to 97 radial 2
    xdot[250] = x[225] / L[96] - x[250] * Rs[96] / L[96] - x[251] / L[96]
    xdot[251] = x[250] / C[96] - x[251] / [C[96] * Rp[96]]

    # 108 ulnar
    xdot[252] = x[237] / L[107] - x[252] * Rs[107] / L[107] - x[253] / L[107]
    xdot[253] = x[252] / C[107] - x[253] / [C[107] * Rp[107]]

    # 100 radial
    xdot[254] = x[245] / L[99] - x[254] * Rs[99] / L[99] - x[255] / L[99]
    xdot[255] = x[254] / C[99] - x[255] / [C[99] * Rp[99]]

    return xdot



############################################################################################
                                    #AVOLIO SIMULATION PARAMETERS
############################################################################################

# Set peak flow
PF = 450

# Set step size
dt = 0.002

# Array to store 1st iteration values to calculate dt
system_dt = np.empty(11)

# Array to store all the peak values to calculate dt
peak_arteries_index = np.empty(11)

# Array containing all the artery numbers
artery_index = [1, 3, 7, 57, 117, 75, 123, 205, 217, 147, 225] 

# Array containing the distance of all the arteries from aortic arch in cm
artery_distance = [3, 0, 10.2, 17.8, 14.3, 38.6, 24.9, 21.9, 42, 57.8, 39.1]        # {1-ascending aorta, 2-aortic arch, 3-subclavian, 4-carotid 5-thoracic, 
                                                                                    # 6-cereberal, 7-abdominal, 8-brachial, 9-ulnar, 10-Femoral, 11-Radial}

# Initial value for pulse generator
pulse_init = np.zeros(2)

# Array to store 1st iteration values to calculate dt
system_pwv = np.empty(11)

# Array to store all the peak values to calculate dt
pwv_arteries_index = np.empty(11)

# Initial value for Avolio model
system_init = np.zeros(256)

# Loop parameters
n = 100
i = 0
ind = [0, 0]

# FOR CHECKNG PREV VALUE & NXT VALUE IS SAME 
heart_rate_check = deque([0, 0], maxlen=2)


while i < n:
    # FETCH HR VALUE FROM DATABASE
    connection = sql.connect("vascularsim.db")
    cursor = connection.cursor()
    cursor.execute("SELECT HR FROM HPN WHERE ID = 1")
    rows = cursor.fetchone()
    HR = rows[0]
    
    
    
    # APPEND HEART RATE FOR CHECKING
    heart_rate_check.append(HR)

    # GET NEW ECG VALUE IF HEART RATE IS NOT SAME
    if heart_rate_check[0] != heart_rate_check[1]:
        ecg_index = 40
        duration = 10
        approx_number_of_beats = int(np.round(duration * (HR / 60)))
        ecg = ecg_simulate_ecgsyn( sfecg=1/dt, N=approx_number_of_beats , Anoise=0, hrmean = HR, hrstd=1, lfhfratio=0.5, sfint=1/dt, ti=(-70, -15, 0, 15, 100), ai=(1.2, -5, 30, -7.5, 0.75), bi=(0.25, 0.1, 0.1, 0.1, 0.4) )
        for hr_val_update in range(1, 8000):
            ind[0] = ind[0] + 1
            if ecg_index == 8000:
                ecg_index = 1
            cursor.execute('UPDATE BUFFER SET "twelve" = ? WHERE id = ?', (ecg[ecg_index], ind[0]) )
            ecg_index += 1
    connection.commit()
    connection.close()
    
    # Time axis for each iteration
    clock = np.arange(i, i+1, dt)

    # Function to be given for interpolation (fp)
    it = np.multiply((1 - np.floor((np.multiply(((clock / (60 / HR)) - np.floor(clock / (60 / HR))), (60 / HR))) + 0.7)), (PF * (np.square(np.sin(3.14 * (np.multiply(((clock / (60 / HR)) - np.floor(clock / (60 / HR))), (60 / HR))) / 0.3)))))    
    
    # Pulse generator output which is to be given as input to the Avolio model
    pulse_output = (solve_ivp(pulsegen, [i, i+1], pulse_init, args=(clock, it), method='Radau', t_eval=clock)).y

    # Update the initial value to be given to the solver as the last value of the previous iteration
    pulse_init = [pulse_output[0,-1], pulse_output[1,-1]]    

    # Convert 2d output to 1-d
    pu = it.transpose()

    # This is the output (1D) to be given to the system
    pulse = (pu - pulse_output[0, :]) * 0.11 + pulse_output[1, :]

    # Solving the Avolio model using Radau method
    simulation_output = (solve_ivp(system_simulator, [i, i+1], system_init, args=(pulse, clock), method='Radau', t_eval=clock, first_step = 0.01, rtol = 1e-1, atol = 1e-1)).y
    # Update the initial value to be given to the solver as the last value of the previous iteration
    system_init = simulation_output[:,-1] 
    
    # UPDATE THE PRESSURE/FLOW VALUE FOR EACH ITERATIONS
    connection = sql.connect("vascularsim.db")
    cursor = connection.cursor()    
    for j in range( len(simulation_output[0])):
        ind[1] = ind[1] + 1
        cursor.execute('UPDATE BUFFER SET "one" = ?, "two" = ?, "three" = ?, "four" = ?, "five" = ?, "six" = ?, "seven" = ?, "eight" = ?, "nine" = ?, "ten" = ?, "eleven" = ? WHERE id = ?', (simulation_output[1,j], simulation_output[3,j], simulation_output[7,j], simulation_output[57,j], simulation_output[117,j], simulation_output[75,j], simulation_output[123,j], simulation_output[205,j], simulation_output[217,j], simulation_output[147,j], simulation_output[225,j], ind[1] ) )
    connection.commit()
    connection.close()
    
    if ind[1] == 8000:
        ind[1] = 0
    
    # Store the first iteration value for calculating dt
    if i == 1:
        # Calculate the dt by identifying the qrs wave
        peak_ecg_index = np.where(ecg[40:540] == np.amax(ecg[40:540]))[0][0]
        # Identify the second peak of Avolio model
        for j in range(11):
            peak_arteries_index[j] = np.add(np.where(simulation_output[artery_index[j],:] == np.amin(simulation_output[artery_index[j],:]))[0][0], (500*i))
            #Calculate dt
            system_dt[j] = np.multiply((peak_arteries_index[j] - peak_ecg_index),4)
        connection = sql.connect("vascularsim.db")
        cursor = connection.cursor()
        cursor.execute('UPDATE HPN SET FLAG = 1, PEP_1 = ?,  PEP_2 = ?, PEP_3 = ?, PEP_4 = ?, PEP_5 = ?, PEP_6 = ?, PEP_7 = ?, PEP_8 = ?, PEP_9 = ?, PEP_10 = ?, PEP_11 = ? WHERE id = 1', (system_dt[0], system_dt[1], system_dt[2], system_dt[3], system_dt[4], system_dt[5], system_dt[6], system_dt[7], system_dt[8], system_dt[9], system_dt[10] ) )
        connection.commit()
        connection.close()
    
    if i == 0:
        
        for k in range(11):
            pwv_arteries_index[k] = np.multiply(np.where(simulation_output[artery_index[k], :] > 0.9)[0][0], 2)
            system_pwv[k] = (artery_distance[k] / pwv_arteries_index[k]) * 1000
            system_pwv = np.round(system_pwv, 2)
    
        # UPDATE FLAG FOR PLOTTING AND PEP VALUE
        connection = sql.connect("vascularsim.db")
        cursor = connection.cursor()
        cursor.execute('UPDATE HPN SET PWV_1 = ?,  PWV_2 = ?, PWV_3 = ?, PWV_4 = ?, PWV_5 = ?, PWV_6 = ?, PWV_7 = ?, PWV_8 = ?, PWV_9 = ?, PWV_10 = ?, PWV_11 = ? WHERE id = 1', (system_pwv[0], system_pwv[1], system_pwv[2], system_pwv[3], system_pwv[4], system_pwv[5], system_pwv[6], system_pwv[7], system_pwv[8], system_pwv[9], system_pwv[10] ) )
        connection.commit()
        connection.close()
    
    i = i + 1

