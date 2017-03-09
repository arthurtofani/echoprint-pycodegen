import numpy
import math
import scipy.io.wavfile as wavfile
import struct
import array
import wave
import pyaudio
#from spectrum import LEVINSON

C_LEN = 128
SUBBANDS = 8
M_ROWS = 8
M_COLS = 16

C = [0.000000477,  0.000000954,  0.000001431,  0.000002384,  0.000003815,  0.000006199,  0.000009060,  0.000013828, \
  0.000019550,  0.000027657,  0.000037670,  0.000049591,  0.000062943,  0.000076771,  0.000090599,  0.000101566, \
  -0.000108242, -0.000106812, -0.000095367, -0.000069618, -0.000027180,  0.000034332,  0.000116348,  0.000218868, \
  0.000339031,  0.000472546,  0.000611782,  0.000747204,  0.000866413,  0.000954151,  0.000994205,  0.000971317, \
  -0.000868797, -0.000674248, -0.000378609,  0.000021458,  0.000522137,  0.001111031,  0.001766682,  0.002457142, \
  0.003141880,  0.003771782,  0.004290581,  0.004638195,  0.004752159,  0.004573822,  0.004049301,  0.003134727, \
  -0.001800537, -0.000033379,  0.002161503,  0.004756451,  0.007703304,  0.010933399,  0.014358521,  0.017876148, \
  0.021372318,  0.024725437,  0.027815342,  0.030526638,  0.032754898,  0.034412861,  0.035435200,  0.035780907, \
  -0.035435200, -0.034412861, -0.032754898, -0.030526638, -0.027815342, -0.024725437, -0.021372318, -0.017876148, \
  -0.014358521, -0.010933399, -0.007703304, -0.004756451, -0.002161503,  0.000033379,  0.001800537,  0.003134727, \
  -0.004049301, -0.004573822, -0.004752159, -0.004638195, -0.004290581, -0.003771782, -0.003141880, -0.002457142, \
  -0.001766682, -0.001111031, -0.000522137, -0.000021458,  0.000378609,  0.000674248,  0.000868797,  0.000971317, \
  -0.000994205, -0.000954151, -0.000866413, -0.000747204, -0.000611782, -0.000472546, -0.000339031, -0.000218868, \
  -0.000116348, -0.000034332,  0.000027180,  0.000069618,  0.000095367,  0.000106812,  0.000108242,  0.000101566, \
  -0.000090599, -0.000076771, -0.000062943, -0.000049591, -0.000037670, -0.000027657, -0.000019550, -0.000013828, \
  -0.000009060, -0.000006199, -0.000003815, -0.000002384, -0.000001431, -0.000000954, -0.000000477, 0]

class SubbandAnalysis:

  def __init__(self, samples):
    # TODO: this can be refactored
    self.samples = samples
    self.num_samples = len(self.samples)
    self.calculate_coefficients()
    self.data = None

  def calculate_coefficients(self):
    # Calculate the analysis filter bank coefficients
    f_cos = lambda i, k : math.cos((2*i + 1)*(k-4)*(math.pi/16.0))
    f_sin = lambda i, k : math.sin((2*i + 1)*(k-4)*(math.pi/16.0))
    self.Mr = [[f_cos(i, k) for k in range(M_COLS)] for i in range(M_ROWS)]
    self.Mi = [[f_sin(i, k) for k in range(M_COLS)] for i in range(M_ROWS)]

  def compute(self):
    z = [0.0] * C_LEN
    y = [0.0] * M_COLS
    num_frames = (self.num_samples - C_LEN + 1)//SUBBANDS
    self.data = [[0.0 for i in range(num_frames)] for k in range(SUBBANDS)]
    for t in range(num_frames):
      for i in range(C_LEN):
        z[i] = self.samples[t * SUBBANDS + i] * C[i]
      for i in range(M_COLS):
        y[i] = z[i]
      for i in range(M_COLS):
        for j in range(1, M_ROWS):
          y[i] += z[i + M_COLS * j]
      for i in range(M_ROWS):
        dr, di = 0.0, 0.0
        for j in range(M_COLS):
          dr += self.Mr[i][j] * y[j]
          di += self.Mi[i][j] * y[j]
        self.data[i][t] = dr*dr + di*di
