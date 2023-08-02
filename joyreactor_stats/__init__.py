from urllib import request, error
from time import sleep
import re


class JoyreactorStats:

    def __init__(self,
                 account: str,
                 show_progress: bool = True,
                 quiet: bool = False
                 ):
        """
        Init class
        :param account:
        :param show_progress:
        :param quiet:
        """

        self.account = account
        self.show_progress = show_progress
        self.quiet = quiet
        self.page_count = 0

    def work(self) -> None:
        self.get_first_page()

    def get_first_page(self) -> None:
        first_url = f'https://joyreactor.cc/user/{self.account}'

        self.print_msg(f'Get {first_url}')

        try:
            response = request.urlopen(first_url)
        except error.HTTPError as e:
            self.print_msg('... страница недоступна')
            exit(1)

        html = response.read().decode(response.headers.get_content_charset())
        page_count = self.get_page_count(html)
        if page_count == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        self.print_msg(f'Количество страниц со статьями: {page_count}')

        self.page_count = page_count

    def scrap_page(self, url: str) -> None:
        pass

    def get_page_count(self, html: str) -> int:
        page_count_template = re.compile(f"<a href='/user/{self.account}/(\\d*)'")
        page_count_list = page_count_template.findall(html)
        if len(page_count_list) == 0:
            return 0

        return page_count_list[0]

    def print_msg(self, msg: str) -> None:
        """
        Print progress
        :param msg:
        :return: None
        """

        if not self.quiet and self.show_progress:
            print(f'{msg}')

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, account: str):
        self.__account = account

    @property
    def quiet(self) -> bool:
        return self.__quiet

    @quiet.setter
    def quiet(self, quiet: bool):
        self.__quiet = quiet

    @property
    def show_progress(self) -> bool:
        return self.__show_progress

    @show_progress.setter
    def show_progress(self, show_progress: bool):
        self.__show_progress = show_progress

    @property
    def page_count(self) -> int:
        return self.__page_count

    @page_count.setter
    def page_count(self, page_count: int):
        self.__page_count = page_count
