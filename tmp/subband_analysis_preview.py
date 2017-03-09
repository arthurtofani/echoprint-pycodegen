import numpy as np
import scipy.io.wavfile as wavfile
from subband_analysis import SubbandAnalysis
audio = wavfile.read("../samples/whitened/come_together_01.wav")
sba = SubbandAnalysis(list(map(lambda x: x / 32768.0, audio[1])))
sba.compute()

