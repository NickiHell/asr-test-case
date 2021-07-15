from typing import Iterable

from apps.user.models import User


class EmailServiceUseCase(object):
    def __init__(self, text: str) -> None:
        self._text: str = text

    def execute(self):
        emails: Iterable = self._get_all_users_emails()
        self._send_emails_to_users(emails)

    @staticmethod
    def _get_all_users_emails() -> Iterable:
        emails: Iterable = User.objects.values_list('email')
        return emails

    @staticmethod
    def _send_emails_to_users(_):
        return True
