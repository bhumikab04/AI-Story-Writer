from gtts import gTTS

def create_audio(text):

    tts = gTTS(text=text)

    file_name = "story.mp3"

    tts.save(file_name)

    return file_name