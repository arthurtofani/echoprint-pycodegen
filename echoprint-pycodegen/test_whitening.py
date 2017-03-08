import unittest
import wave
import scipy.io.wavfile as wavfile
import whitening

class TestWhitening(unittest.TestCase):

  def setUp(self):
    self.audio = wavfile.read("../samples/canto-tetrico-11025Hz_mono_16-bit.wav")
    self.obj = whitening.Whitening(self.audio)

  def test_compute(self):
    self.obj.compute()
    self.assertEqual(1, 1)

  def test_compute_block(self):
    block = self.audio.readframes(whitening.BLOCK_LENGTH)
    self.obj.compute_block(block)

  def test_calculate_block_autocorrelation(self):
    block = self.audio.readframes(whitening.BLOCK_LENGTH)
    while block != '':
      r = self.obj.calculate_block_autocorrelation(block)
      self.assertEqual(len(r), self.obj.P)
      self.assertNotEqual(r[0], 0)
      block = self.audio.readframes(whitening.BLOCK_LENGTH)

  def test_calculate_new_filter_coefficients(self):
      block = self.audio.readframes(whitening.BLOCK_LENGTH)
      self.obj.R = self.obj.calculate_block_autocorrelation(block)
      E = self.obj.calculate_new_filter_coefficients()

  def test_calculate_new_output(self):
    print("todo")
