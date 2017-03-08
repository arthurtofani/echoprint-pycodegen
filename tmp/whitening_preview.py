import scipy.io.wavfile as wavfile
import whitening
audio = wavfile.read("../samples/canto-tetrico-11025Hz_mono_16-bit.wav")
w = whitening.Whitening(audio)
w.compute()
w.save("./whitened.wav")

# import scipy.io.wavfile as wavfile
# wavfile.read("../samples/canto.wav")
# audio = wavfile.read("../samples/canto-tetrico-11025Hz_mono_16-bit.wav")
