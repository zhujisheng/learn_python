import pyaudio
import wave

WAVE_FILE = 'audio/example0.wav'

p = pyaudio.PyAudio()

wf = wave.open(WAVE_FILE, 'rb')

print("Channels: ", wf.getnchannels())
print("Sample Rate: ", wf.getframerate())
print("Sample Format: ", wf.getsampwidth(), 'bytes')
print("Sample Count: ", wf.getnframes())


stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

while True:
    data = wf.readframes(1024)
    if len(data)==0:
        break
    stream.write(data)

wf.close()
stream.stop_stream()
stream.close()
p.terminate()
