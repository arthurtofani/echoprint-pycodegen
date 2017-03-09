##
## "To improve robustness against varyiable OTA channel
## characteristics, the signal is “whitened” prior to the analysis
## above. A 40-pole LPC filter is estimated from the autocorrelation
## of 1 sec blocks of the signal, smoothed with an 8
## sec decay constant. The inverse (FIR) filter is applied to the
## signal to achieve whitening."

## checar de usar audiolazy - http://pythonhosted.org/audiolazy/lazy_lpc.html

import numpy
import scipy.io.wavfile as wavfile
import struct
import array
import wave
import pyaudio
#from spectrum import LEVINSON

BLOCK_LENGTH = 10000
T = 8
ALPHA = 1.0/T

class Whitening:
  def __init__(self, audio):
    # audio is a scipy.io.wavfile
    # TODO: isso aqui não dá pra sempre puxar direto do audio?
    # audio = wave.open("../samples/vida_marvada_44100.wav")

    self.audio = audio
    self.sample_rate = audio[0]
    # TODO: isso deve estar pra fora da classe
    self.samples = list(map(lambda x: x / 32768.0, audio[1]))
    self.num_samples = len(audio[1])

    # init parameters and coeficients
    self._p = 40
    self.R = [0.0] * (self._p+1)
    self.R[0] = 0.001
    self.x0 = [0.0] * (self._p+1)
    self.ai = [None] * (self._p+1)
    self.whitened = [None] * self.num_samples

  def compute(self):
    for i in range(self.num_samples)[:self.num_samples:BLOCK_LENGTH]:
      self.compute_block(i)

  def compute_block(self, start):
    print(start)
    block = self.samples[start:(BLOCK_LENGTH+start):]
    block_size = len(block)
    self.calculate_block_autocorrelation(start, block_size)
    self.calculate_new_filter_coefficients()
    self.calculate_new_output(start, block_size)
    return

  def calculate_block_autocorrelation(self, start, block_size):
    for i in range(self._p+1):
      acc = 0
      for j in range(i, block_size):
        acc += self.samples[j+start] * self.samples[j-i+start]
      self.R[i] += ALPHA * (acc - self.R[i])

  def calculate_new_filter_coefficients(self):
    # ver rlevinson@
    E = self.R[0]
    for i in range(1, self._p + 1):
      sumalphaR = 0.0
      for j in range(1, i):
        sumalphaR += self.ai[j] * self.R[i-j]
      ki = (self.R[i] - sumalphaR)/E
      self.ai[i] = ki
      for j in range(1, (i//2)+1):
        aj = self.ai[j]
        aimj = self.ai[i-j]
        self.ai[j] = aj - ki * aimj
        self.ai[i-j] = aimj - ki * aj
      E = (1 - ki * ki) * E

  def calculate_new_output(self, start, block_size):
    # calculate new output
    for i in range(block_size):
      acc = self.samples[i+start]
      minip = min(i, self._p)
      for j in range(i+1, self._p+1):
        acc -= self.ai[j]*self.x0[self._p + i-j]
      #for j in range(1, minip+1):
      #  acc -= self.ai[j]*self.samples[i-j+start]
      self.whitened[i+start] = acc

    #save last few frames of input
    for i in range(self._p + 1):
      self.x0[i] = self.samples[block_size-1-self._p+i+start]

  def save_preview(self, filename):
    #whitened = numpy.array(self.whitened, dtype=numpy.int16)
    w = list(map(lambda x: x * 32768.0, self.whitened))
    whitened = numpy.array(w, dtype=numpy.int16)
    wavfile.write(filename, 11025, whitened)
    numpy.array(self.whitened)
