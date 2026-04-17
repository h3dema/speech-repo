# Speech Commands Data Set v0.02

This is repo contains simple notebook that extract from .wav files it amplitude representation and the corresponding [spectrogram](https://en.wikipedia.org/wiki/Spectrogram).
The audio files come from [Pete Warden's dataset](https://petewarden.com/2018/04/11/speech-commands-is-now-larger-and-cleaner/).
Here we tested only two files that contain yes and no words.


## Download all audios

```bash
mkdir speech
cd speech
wget http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz
tar zxvf speech_commands_v0.02.tar.gz
```
