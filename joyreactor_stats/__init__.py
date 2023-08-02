from urllib import request, error
from time import sleep
import re


class JoyreactorStats:

    def __init__(self,
                 account: str):
        """
        Init class
        :param account:
        """

        self.account = account

    def get_first_page(self):
        first_url = f'https://joyreactor.cc/user/{self.account}'

        self.print_progress(first_url)

        try:
            response = request.urlopen(first_url)
        except error.HTTPError as e:
            pass
        else:
            html = response.read().decode(response.headers.get_content_charset())
            print(html)
            page_count = self.get_page_count(html)
            print(page_count)

    def get_page_count(self, html: str) -> int:
        page_count_template = re.compile(f"<a href='/user/{self.account}/(\\d*)'")
        page_count_list = page_count_template.findall(html)
        if len(page_count_list) == 0:
            return 0

        return page_count_list[0]

    def print_progress(self, site: str) -> None:
        """
        Print progress
        :param site: Current site url
        :return: None
        """
        print(f'{site}')


    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, account: str):
        self.__account = account
