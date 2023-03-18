"""ТЕСТИ ДЛЯ HAPPY BOT"""

from aiogram import Bot
from django.test import TestCase

from unittest.mock import patch, AsyncMock, MagicMock

from happy_bday.settings import TELEGRAM_BOT_TOKEN, ADMIN_ID
from happy_bot.core.handlers.basic import stop_bot, get_users


class TestStopBotHandler(TestCase):
    def setUp(self) -> None:
        """
        The setUp function is called before each test function.
        It creates a new bot instance and sets the admin_id to the value of ADMIN_ID.

        :param self: Represent the instance of the class
        :return: None
        """
        self.bot = Bot(TELEGRAM_BOT_TOKEN)
        self.admin_id = ADMIN_ID

    async def test_stop_bot_handler(self):
        """
        The test_stop_bot_handler function tests the stop_bot function.
        It does so by mocking a bot object and calling the stop_bot function with it as an argument.
        The mocked bot's send_message method is then checked to see if it was called once with the admin id and text 'Бот зупинено.'.

        :param self: Represent the instance of the class
        :return: The bot_mock
        """
        bot_mock = MagicMock(spec=Bot)
        bot_mock.send_message = AsyncMock()

        await stop_bot(bot_mock)

        bot_mock.send_message.assert_called_once_with(self.admin_id, text='Бот зупинено.')


class TestGetUsers(TestCase):
    async def test_get_users_no_users(self):
        """
        The test_get_users_no_users function tests the get_users function when there are no users in the database.
        It does this by mocking out Profile.objects.all() to return an empty list, and then asserts that get_users returns an empty list.

        :param self: Access the class attributes and methods
        :return: An empty list if there are no users
        """
        with patch('happy_bot.core.handlers.basic.Profile.objects.all') as mock_get_users:
            mock_get_users.return_value = []
            users = await get_users()
            self.assertEqual(users, [])

    async def test_get_users_with_users(self):
        """
        The test_get_users_with_users function tests the get_users function.
        It does this by mocking the Profile.objects.all() method and returning a list of one mock profile object with a telegram chat id of 12345, then calling get_users().
        The test asserts that there is only one user in the returned list, and that it has a telegram chat id of 12345.

        :param self: Represent the instance of the object that is using this method
        :return: A list of users
        """
        with patch('happy_bot.core.handlers.basic.Profile.objects.all') as mock_get_users:
            mock_profile = MagicMock()
            mock_profile.telegram_chat_id = '12345'
            mock_get_users.return_value = [mock_profile]
            users = await get_users()
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].telegram_chat_id, '12345')
