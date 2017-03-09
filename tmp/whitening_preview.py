import numpy as np
import scipy.io.wavfile as wavfile
import whitening
audio = wavfile.read("../samples/come_together_01.wav")
w = whitening.Whitening(audio)
w.compute()
w.save_preview("../samples/whitened/come_together_01.wav")


# import scipy.io.wavfile as wavfile
# wavfile.read("../samples/canto.wav")
# audio = wavfile.read("../samples/canto-tetrico-11025Hz_mono_16-bit.wav")

#ffmpeg -i come_together.mp3 -acodec pcm_s16le -ac 1 -ar 11025 come_together_full.wav

#/home/arthur/tmp/echoprint/echoprint-pycodegen/samples/come_together_full.wav


ffmpeg -i come_together_01.wav -acodec pcm_s16le -ac 1 -ar 11025 come_together_01b.wav
