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

    def work(self) -> None:
        page_count = self.get_page_count()

        for page in range(1, page_count + 1):
            self.print_progress(page, page_count)
            self.scrap_page(page)

    def get_page_count(self) -> int:
        first_url = f'https://joyreactor.cc/user/{self.account}'

        html = self.get_site_html(first_url)

        page_count_template = re.compile(f"<a href='/user/{self.account}/(\\d*)'")
        page_count_list = page_count_template.findall(html)
        if len(page_count_list) == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        page_count = int(page_count_list[0])

        if page_count == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        self.print_msg(f'Количество страниц со статьями: {page_count}')

        return page_count

    def scrap_page(self, page: int) -> None:
        pass

    def scrap_post(self):
        pass

    def get_site_html(self, url: str) -> str:
        self.print_msg(f'Get {url}')

        try:
            response = request.urlopen(url)
        except error.HTTPError as e:
            self.print_msg('... страница недоступна')
            exit(1)

        html = response.read().decode(response.headers.get_content_charset())

        return html

    def print_msg(self, msg: str) -> None:
        """
        Print message
        :param msg:
        :return: None
        """

        if not self.quiet and self.show_progress:
            print(f'{msg}')

    def print_progress(self, cur_page: int, page_count: int) -> None:
        """
        Print progress
        :param cur_page:
        :param page_count:
        :return: None
        """

        self.print_msg(f'[{cur_page}/{page_count}]')

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
