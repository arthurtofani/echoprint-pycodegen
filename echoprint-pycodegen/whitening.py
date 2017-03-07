import numpy
import array
import wave
import pyaudio
from spectrum import LEVINSON

BLOCK_LENGTH = 10000
T = 8

class Whitening:
  def __init__(self, audio):
    # audio is a wave audio
    # TODO: isso aqui não dá pra sempre puxar direto do audio?
    # audio = wave.open("../samples/vida_marvada_44100.wav")
    self.audio = audio
    self.samples = audio.getnframes()
    self.num_samples = audio.getnframes()

    self.P = 40
    self.alpha = 1.0/T
    self.x0 = [0.0] * self.P
    self.ai = [None] * self.P
    self._whitened = [None] * self.num_samples


  def compute(self):
    block = self.audio.readframes(BLOCK_LENGTH)
    self.compute_block(block)
    while block != '':
      self.compute_block(block)
      block = self.audio.readframes(BLOCK_LENGTH)


  def compute_block(self, block_bytes):
    block = array.array('h', block_bytes)
    self.R = self.calculate_block_autocorration(block)
    E = self.R[0]
    for i in range(self.P):
      sumalphaR = 0.0;
      for j in range(i):
        sumalphaR += self.ai[j] * self.R[i-j]
      ki = (self.R[i] - sumalphaR)/E
      self.ai[i] = ki
      for j in range(1, i//2): # is this actually the same??
        aj = self.ai[j]
        aimj = self.ai[i-j]
        self.ai[j] = aj - ki * aimj
        self.ai[i-j] = aimj - ki * aj
      E = (1 - ki * ki) * E
      print(E)
      # getsampwidth()https://gist.github.com/rpls/3760188
      # here comes the magic for each block
    return

  def calculate_block_autocorration(self, block):
    r = [0.0] * self.P
    r[0] = 0.001
    for i in range(self.P):
      acc = 0
      for j in range(len(block)):
        acc += block[j] * block[j-i]
      r[i] += self.alpha * (acc - r[i])
    return r

  def new_filter_coefficients(self):
    return
    # ver rlevinson
