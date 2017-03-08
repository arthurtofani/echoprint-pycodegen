import numpy
import scipy.io.wavfile as wavfile
import struct
import array
import wave
import pyaudio
from spectrum import LEVINSON

BLOCK_LENGTH = 10000
T = 8

class Whitening:
  def __init__(self, audio):
    # audio is a scipy.io.wavfile
    # TODO: isso aqui não dá pra sempre puxar direto do audio?
    # audio = wave.open("../samples/vida_marvada_44100.wav")

    self.audio = audio
    self.sample_rate = audio[0]
    self.samples = audio[1]
    self.num_samples = len(audio[1])

    # init parameters and coeficients
    self.P = 40
    self.alpha = 1.0/T
    self.x0 = [0.0] * self.P
    self.ai = [None] * self.P
    self.whitened = [None] * self.num_samples


  def compute(self):
    for i in range(self.num_samples)[:self.num_samples:BLOCK_LENGTH]:
      self.compute_block(i)

  def compute_block(self, start):
    print(start)
    block = self.samples[start:(BLOCK_LENGTH+start):]
    self.R = self.calculate_block_autocorrelation(block)
    E = self.calculate_new_filter_coefficients()
    self.calculate_new_output(block)
    return

  def calculate_block_autocorrelation(self, block):
    r = [0.0] * self.P
    r[0] = 0.001
    for i in range(self.P):
      acc = 0
      for j in range(len(block)):
        acc += block[j] * block[j-i]
      r[i] += self.alpha * (acc - r[i])
    return r

  def calculate_new_filter_coefficients(self):
    # ver rlevinson@
    E = self.R[0]
    for i in range(1, self.P):
      sumalphaR = 0.0
      for j in range(1, i-1):
        sumalphaR += self.ai[j] * self.R[i-j]
      ki = (self.R[i] - sumalphaR)/E
      self.ai[i] = ki
      for j in range(1, i//2): # is this actually the same??
        aj = self.ai[j]
        aimj = self.ai[i-j]
        self.ai[j] = aj - ki * aimj
        self.ai[i-j] = aimj - ki * aj
      E = (1 - ki * ki) * E
    return E, self.ai

  def calculate_new_output(self, block):
    for i in range(len(block)-1):
      acc = block[i]
      minip = min(i, self.P)
      for j in range(i+1, self.P):
        acc -= self.ai[j]*self.x0[self.P + i-j]
      for j in range(1, minip):
        acc -= self.ai[j]*block[i-j]
      self.whitened[i] = acc
    for i in range(self.P):
      self.x0[i] = block[len(block)-1-self.P+i]
    return self.whitened

  def save(self, filename):
    output = wave.open(filename, 'w')
    output.setnchannels(self.audio.getnchannels())
    output.setsampwidth(self.audio.getsampwidth())
    output.setframerate(self.audio.getframerate())
    for value in range(0, len(self.whitened)-1):
      packed_value = struct.pack('h', value)
      output.writeframes(packed_value)
