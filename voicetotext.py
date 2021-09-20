import speech_recognition as sr
from os import fspath, remove
from pydub import AudioSegment


OGG_FILE_NAME = 'example.ogg'
M4A_FILE_NAME = 'example.m4a'

ERROR_MESSAGE_SPEECH_TO_TEXT = "Can't recognize this ((("

languages = {'ru':'ru-RU'}


def getLanguageCode(language_string):
    return languages[language_string]



def oggToWav(ogg_file_name):
    
    try:
        print(f'[oggToWav] received {ogg_file_name}')
        
        result_file_name = fspath(ogg_file_name + '.wav')
        
        print(f'[oggToWav] {ogg_file_name} converted to {result_file_name}')
        print(f'[oggToWav] load audio segment from {ogg_file_name} ...', end='') 
        
        phrase = AudioSegment.from_ogg(ogg_file_name)
        print('Done!')
        print(f'[oggToWav] export from {ogg_file_name} to {result_file_name} ...', end='') 
        
        phrase.export(result_file_name, format='wav')
        
        print('Done!')   
        
        remove(ogg_file_name)
    except Exception:
        return None
    return result_file_name

def speechToText(wav_file_name, language):
    if wav_file_name == None:
        return ERROR_MESSAGE_SPEECH_TO_TEXT
    result_text = ''
    print(f'[speechToText] received {wav_file_name}')
    
    print(f'[speechToText] init speech_recognition module ...', end='') 
    voice_record = sr.Recognizer()
    print('Done!')
    
    print(f'[speechToText] trying to load file ...', end='') 
    with sr.AudioFile(wav_file_name) as audio_file:
        print('recording...', end='')
        audio = voice_record.record(audio_file)
        print('Done!')
        
    try:
        print(f'[speechToText] sending {audio.sample_width} to cloud ...', end='')
        result_text = voice_record.recognize_google(audio, language=language)
        print('Done!')
        remove(wav_file_name)
        
    except Exception:
        print('Smth goes wrong...')
        return ''
    
    return result_text

def remVoiceFiles(filenames):
    for filename in filenames:
        try:
            remove(filename)
        except Exception:
            continue
    return 0
        

def main():
    
    wav_file = oggToWav(OGG_FILE_NAME)
    
    result = speechToText(wav_file, "ru-RU")
    
    print(result)
    
        
    return


if __name__ == "__main__":
    main()