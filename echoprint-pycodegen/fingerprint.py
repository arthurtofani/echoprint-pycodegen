import numpy
import math
import scipy.io.wavfile as wavfile
import struct
import array
import wave
import pyaudio

HASH_SEED = 0x9ea5fa36
QUANTIZE_DT_S = (256.0/11025.0)
QUANTIZE_A_S = (256.0/11025.0)
HASH_BITMASK = 0x000fffff
SUBBANDS = 8

class Fingerprint:
  def __init__(self, subband_analysis, offset):
    self.subband_analysis = subband_analysis
    self.offset = offset

  def adaptive_onsets(self, ttarg, out, onset_counter_for_band):
    deadtime = 128
    overfact = 1.1
    onset_counter = 0

    E = subband_analysis.data
    hop = 4
    nsm = 8
    for i in range(nsm):
      ham[i] = 0.5 - 0.5*math.cos((2.*math.pi/(nsm-1))*i)
    nc =  math.floor(len(E[0]) / float(hop)) - (math.floor(float(nsm) / float(hop)) -1);
    Eb = [[0.0 for k in range(8)] for i in range(nc)]
    for i in range(nc):
      for j in range(SUBBANDS):
        for k in range(nsm):
          Eb[i][j] = Eb[i][j] + (E[j][(i * hop) + k] * ham[k])
    frames = len(Eb)
    bands = len(Eb[0])
    return

  def quantized_time_for_frame_delta(frame_delta):
    return

  def quantized_time_for_frame_absolute(frame_delta):
    return

  def compute(self):
    return

