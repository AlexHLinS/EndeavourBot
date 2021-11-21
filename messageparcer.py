import voicetotext as vtt

import botcommands
import dbworker
import filetools


class messageparcer:

    __message_raw = None
    VOICE_ANSWER_MESSAGE_HEADER = 'В присланном голосовом сообщении было сказано:\n'
    VOICE_MESSAGE_RECIVED_MESSAGE = 'Обрабатываю присланное голосовое сообщение, это может занять некторое время...'

    def isCommand(self, text):
        result = False
        cmd_template = r''

        return result

    def getMessageContentType(self):
        return self.__message_raw.content_type

    def getMessageVoiceAttachment(self, bot):

        if self.__message_raw.content_type in ['voice'] :
            file_info = bot.get_file(self.__message_raw.voice.file_id)
            file_info = file_info.wait()
            # print(file_info.file_path)
            downloaded_file = bot.download_file(file_info.file_path)
            downloaded_file = downloaded_file.wait()
            downloaded_file_name = str(self.__message_raw.voice.file_id)+'.ogg'
            with open(downloaded_file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
                return(downloaded_file_name)

        if self.__message_raw.content_type in ['audio'] :
            file_info = bot.get_file(self.__message_raw.audio.file_id)
            file_info = file_info.wait()
            # print(file_info.file_path)
            downloaded_file = bot.download_file(file_info.file_path)
            downloaded_file = downloaded_file.wait()
            downloaded_file_name = str(self.__message_raw.audio.file_id)+'.m4a'
            with open(downloaded_file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
                return(downloaded_file_name)


        return None

    def __init__(self, message, bot, database):
        self.__message_raw = message
        print(f"[>] \'{self.getMessageContentType()}\' from {message.from_user.username}  {message.from_user.language_code} {message}")
        database.addUser(user_id=message.from_user.id,
                         user_name=message.from_user.username, alias_name='')
        self.getMessageContentType()
        voice_file = self.getMessageVoiceAttachment(bot)
        if voice_file is not None:
            bot.reply_to(message, self.VOICE_MESSAGE_RECIVED_MESSAGE)

            crc = filetools.getMD5(voice_file)
            if database.isTranscribationResultExist(md5hash=crc):
                answer = database.getTranscribationResult(crc)
            else:
                if voice_file[-3:] == 'ogg':
                    #answer = f'{vtt.speechToText(vtt.oggToWav(voice_file), vtt.getLanguageCode(self.__message_raw.from_user.language_code))}'
                    wav_file = vtt.oggToWav(voice_file)
                elif voice_file[-3:] == 'm4a':
                    #answer = f'{vtt.speechToText(vtt.m4aToWav(voice_file), vtt.getLanguageCode(self.__message_raw.from_user.language_code))}'
                    wav_file = vtt.m4aToWav(voice_file)
                else:
                    return
                res = vtt.speechToText(wav_file_name=wav_file,language='ru-RU')
                answer = f'{res}'
                database.addTranscribationResult(
                    md5hash=crc, content_text=answer)
                answer = f'{self.VOICE_ANSWER_MESSAGE_HEADER}'+answer

            try:
                forw_from = message.forward_from.id
            except Exception:
                forw_from = message.from_user.id

            database.addTranscribationRequest(
                user_id=message.from_user.id, md5hash=crc, forward_from=forw_from)

            bot.reply_to(message, answer)
        elif message.entities:
            cmd = botcommands.BotCommand(message.text)
            bot.reply_to(message, cmd.getData())
        else:
            bot.reply_to(
                message, f'К сожалению я пока еще слишком юн и зелен чтобы ответить на это сообщение, но буду стараться развиваться активнее в этом направлении! )')
        return
