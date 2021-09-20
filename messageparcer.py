import voicetotext as vtt

class messageparcer:

    __message_raw = None
    VOICE_ANSWER_MESSAGE_HEADER ='В присланном голосовом сообщении было сказано:\n'
    VOICE_MESSAGE_RECIVED_MESSAGE = 'Обратываею присланное голосовое сообщение, это может занять некторое время...'

    def getMessageContentType(self):
        return self.__message_raw.content_type
    

    def getMessageVoiceAttachment(self, bot):
     
        if self.__message_raw.content_type == 'voice':
            file_info = bot.get_file(self.__message_raw.voice.file_id)
            file_info = file_info.wait()
            #print(file_info.file_path)
            downloaded_file = bot.download_file(file_info.file_path)
            downloaded_file = downloaded_file.wait()
            downloaded_file_name = str(self.__message_raw.voice.file_id)+'.ogg'
            with open(downloaded_file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
                return(downloaded_file_name)
        
        return None

    def __init__(self, message, bot):
        self.__message_raw = message
        # print(f"[>] \'{self.getMessageContentType()}\' from {message.from_user.username}  {message.from_user.language_code} {message}")
        self.getMessageContentType()
        voice_file = self.getMessageVoiceAttachment(bot)
        if voice_file is not None:
            bot.reply_to(message, self.VOICE_MESSAGE_RECIVED_MESSAGE)
            answer = f'{self.VOICE_ANSWER_MESSAGE_HEADER} {vtt.speechToText(vtt.oggToWav(voice_file), vtt.getLanguageCode(self.__message_raw.from_user.language_code))}'
            bot.reply_to(message, answer)
        else:
            bot.reply_to(message, f'You\'re sent me {self.getMessageContentType()}')
        return
        
