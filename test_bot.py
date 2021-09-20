from bot import botToken
import unittest


def test_bot():
    assert str(botToken(token_file='test_bot.token').getToken(
    )) == '1111111111:TeStTaPiToKeN', 'Loading token from file is wrong'
