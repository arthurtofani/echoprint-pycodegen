from unittest import TestCase
import whitening

class TestWhitening(unittest.TestCase):

#    def setUp(self):
#      pass

  def test_upper(self):
    #print self
    self.assertEqual('foo'.upper(), 'FOO')
