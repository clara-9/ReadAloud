
from google.cloud import texttospeech
from itertools import chain


def list_languages():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices
    languages = unique_languages_from_voices(voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="" if i % 5 < 4 else "\n")


def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

list_voices("es")

def text_to_wav(voice_name, text, filename):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"{filename}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')

def wav_from_file(filename):
    text = open(f'{filename}.txt', 'r').read()
    if len(text)<500:
        text_to_wav("es-ES-Wavenet-B",text,filename)
    else:
        j=0
        for i in chain(range(5000, len(text),5000), [len(text)]):
            filename_num=f"{filename}_{i}"
            text_n=text[j:i]
            print(i)
            print(text_n)
            text_to_wav("es-ES-Wavenet-B",text_n,filename_num)
            j=i
    return

wav_from_file("nanomedicina")
