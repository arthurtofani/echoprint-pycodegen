import unittest
import wave
import whitening

class TestWhitening(unittest.TestCase):

  def setUp(self):
    self.audio = wave.open("../samples/small.wav")
    self.obj = whitening.Whitening(self.audio)

  def test_compute(self):
    self.obj.compute()
    self.assertEqual(1, 1)

  def test_compute_block(self):
    block = self.audio.readframes(whitening.BLOCK_LENGTH)
    self.obj.compute_block(block)
