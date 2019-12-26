import pyaudio
import wave

WAVE_FILE = 'audio/my_audio.wav'
CHANNELS = 2
SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2

wf = wave.open(WAVE_FILE, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(SAMPLE_WIDTH)
wf.setframerate(SAMPLE_RATE)

p = pyaudio.PyAudio()
stream_in = p.open(format=p.get_format_from_width(SAMPLE_WIDTH),
                   channels=CHANNELS,
                   rate=SAMPLE_RATE,
                   input=True)


print("开始录音")
while True:
    try:
        print('.', end='')
        buffer = stream_in.read(1024)
        wf.writeframes( buffer )
    except KeyboardInterrupt:
        break

wf.close()
stream_in.stop_stream()
stream_in.close()
p.terminate()
