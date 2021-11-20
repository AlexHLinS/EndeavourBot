import parcerforcovidinfo


class BotCommandsHandler:

    def getHelp(*args):
        help_message = 'Добро пожаловать!\nОсновной моей задачей \
                        является сохранение Вашего душевного спокойствия путем \
                        снятия напряжения при получении от кого-то из контактов\
                        ненависных голосовых сообщений.\nКак это работает: Вы получаете голосовое сообщение, но вместо того,\
                        чтобы гневаться и проклинать того, кто его прислал - пересылаете мне,\
                        после чего, используя всю мощь и достижение науки и техники, перевожу\
                             его в текстовое сообщение и присылаю Вам )'
        
        return help_message

    def getInfo(*args):
        return "Info message!"

    def getCovidInfo(*args):
        url = 'https://www.worldometers.info/coronavirus/'
        if len(args) == 1:
            data = parcerforcovidinfo.getDataForCountry('russia')
            url = f'{data} \n' + f'Info got from {url} '+str(*args[0])

            

        return url


class BotCommand:

    __commands_list = {'help': BotCommandsHandler.getHelp,
                       'info': BotCommandsHandler.getHelp,
                       'covidinfo': BotCommandsHandler.getCovidInfo}

    __help_text = 'This is the help text for this bot'

    def __sendInfoMessage(self):
        return self.__help_text

    def getData(self):
        UNKNOWN_COMMAND_TEXT = f' Неизвестная команда, для подробной информации воспользуйтесь помощью (командой /help) '

        command = self.__command_text.split()[0][1:]
        params = self.__command_text.split()[1:]

        if  command in self.__commands_list.keys():
            return self.__commands_list[command](params)
        else:
            return UNKNOWN_COMMAND_TEXT

        return ' smth '

    def __init__(self, command_text):
        self.__command_text = command_text
        pass
