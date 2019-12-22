import pyaudio

p = pyaudio.PyAudio()


#########
# 录音  #
#########
print("开始录音")
stream_in = p.open(input_device_index=None,
                   format=pyaudio.paInt16,
                   channels=2,
                   rate=16000,
                   input=True)
data=b''
for i in range(5):
    data = data + stream_in.read(16000)

stream_in.stop_stream()
stream_in.close()


#########
# 播放  #
#########
print("开始播放")
stream_out = p.open(output_device_index=None,
                    format=pyaudio.paInt16,
                    channels=2,
                    rate=16000,
                    output=True)
stream_out.write(data)
stream_out.stop_stream()
stream_out.close()


p.terminate()