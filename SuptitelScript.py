#
#
import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.0.10-Q16\magick.exe"

from moviepy.editor import *
from moviepy.video.VideoClip import TextClip, VideoClip

import speech_recognition as sr
from os import path
from pydub import AudioSegment

import speech_recognition as sr
from os import path
from pydub import AudioSegment
#
import textwrap

from moviepy.video.tools.subtitles import SubtitlesClip

#
#Extract Audio from video
extract_audio = False
#Traspose .mp3 to .wav
transpose_wav = True
#Recognize Speach and transpose to Text
recognize_speech = True
#Translate speech parts
translate = True
#Merge Subtitel and video
merge_subtitel = True

video = VideoFileClip("xxx")


if extract_audio:
        print("Extract Audio from Video ") # 2.
        audio = video.audio # 3.
        audio.write_audiofile("data/audio.mp3") # 4.
        #
        print("Extract from Video done")

#
if transpose_wav:
        print("Start Transcription from .mp3 to .wav")

        sound = AudioSegment.from_mp3("data/audio.mp3")
        ten_seconds = 10 * 1000

        #sound  = sound[ten_seconds:2*ten_seconds]

        sound.export("data/transcript.wav", format="wav")

        print("Done Transcription from .mp3 to .wav")

if recognize_speech:
        print("Start Transcription")

        # I mannully figure out sequences where text and workds should shown together.
        # Then extract that soundpart und translate it

        sequences = [
                (10,14),
                (14,25),
                (37,55),
                (55,59)
        ]
        audio_object = AudioSegment.from_wav("data/transcript.wav")
        print("Load Audio (.wav) done")
        # use the audio file as the audio source
        r = sr.Recognizer()
        subtitels_text = list()
        for idx,seq in enumerate(sequences):
                #wav Object count in milliseconds
                start_seq = seq[0] * 1000
                end_seq = seq[1] * 1000
                sound = audio_object[start_seq:end_seq]
                file_ = "data/tmp/{}.wav".format(idx)
                sound.export(file_, format="wav")
                print("Sequence Prepared and stored in tmp")
                with sr.AudioFile(file_) as source:
                        try:
                                audio = r.record(source)  # read the entire audio file
                                translation = r.recognize_google(audio, language="de-DE")
                                sub_text = (seq, translation)
                                subtitels_text.append(sub_text)
                                print("Google thinks you said: " , sub_text)
                                # r.recognize_google(audio, language="de-DE",show_all=True)
                                # print("Sphinx thinks you said: " + r.recognize_sphinx(audio,language="de-DE"))
                        except sr.UnknownValueError:
                                print("Google could not understand audio")
                        except sr.RequestError as e:
                                #Need to build in an redo
                                print("Goole error; {0}".format(e))


        print(subtitels_text)

if translate:
        print('Translate')
        from googletrans import Translator
        t = Translator()
        subtitels_text = [(x[0], t.translate(x[1], dest='en', src='de').text) for x in subtitels_text]

if merge_subtitel:
        print('Subtitels')
        #check()

        subtitels_text_ = [(x[0], '\n'.join(textwrap.wrap(x[1], 100))) for x in subtitels_text]


        subtitles = SubtitlesClip(subtitels_text_)\
                .set_pos(('center','top'))

        myvideo = video.subclip(0,59)

        final = CompositeVideoClip([myvideo, subtitles])
        final.write_videofile("data/final.mp4")#, fps=myvideo.fps)