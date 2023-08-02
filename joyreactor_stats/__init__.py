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

        self.post_id_template = re.compile('<a title="ссылка на пост" class="link" href="/post/(\\d*)">ссылка</a>')
        self.page_count_template = re.compile(f"<a href='/user/{self.account}/(\\d*)'")
        self.post_title_template = re.compile('<div class="post_content"><div><h3>([\w\s\d\.\,\-]*)</h3>([[\w\s\d\.\,\-]*]*)</div>')

        self.post_id = list()
        self.post_title = list()
        self.post_text = list()
        self.post_date = list()
        self.post_comments = list()
        self.post_likes = list()
        self.post_url = list()

    def work(self) -> None:
        page_count = self.get_page_count()

        # TODO: for page in range(1, page_count + 1):
        page = 1
        self.print_progress(page, page_count)
        self.scrap_page(page)
        sleep(10)

    def get_page_count(self) -> int:
        first_url = f'https://joyreactor.cc/user/{self.account}'

        html = self.get_site_html(first_url)

        page_count_list = self.page_count_template.findall(html)
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
        page_url = f'https://joyreactor.cc/user/{self.account}/{page}'
        html = self.get_site_html(page_url)

        post_id_list = self.post_id_template.findall(html)
        if len(post_id_list) == 0:
            self.print_msg('\t... что-то пошло не так. Похоже неверный аккаунт.')
            exit(2)

        for post_id in post_id_list:
            self.scrap_post(post_id)
            sleep(10)

    def scrap_post(self, post_id: int) -> None:
        self.post_id.append(post_id)

        post_url = f'https://joyreactor.cc/post/{post_id}'

        self.post_url.append(post_url)

        html = self.get_site_html(post_url)

        post_title_list = self.post_title_template.findall(html)
        if len(post_title_list) == 0:
            self.print_msg('\t... не удалось получить данные со страницы')
            return

        self.post_title.append(post_title_list[0][0])
        self.post_text.append(post_title_list[0][1])

        self.print_msg(post_title_list[0][0])

    def get_site_html(self, url: str) -> str:
        self.print_msg(f'\t\tGet {url}')

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
