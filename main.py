import argparse


version = '1.0.0'


def parse_args():
    parser = argparse.ArgumentParser(
        prog='joyreactor_stats',
        description='Get Joyreactor stats v.%s' % version + ' (c) 2023 Genzo',
        add_help=False
        )

    parser.add_argument(
        dest='account',
        type=str,
        help='Аккаунт на Joyrector, для которого собирается статистика'
    )

    parser.add_argument(
        '-no',
        '--dont_open',
        action='store_true',
        help='Не открывать найденный результат в excel'
    )

    parser.add_argument(
        '-np',
        '--no_progress',
        action='store_true',
        help='Не выводить прогресс поиска'
    )

    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='Ничего не выводить на экран'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        help='Показать версию',
        version='%(prog)s v.{}'.format(version)
    )

    parser.add_argument(
        '-h', '-?',
        '--help',
        action='help',
        help='Показать помощь и выйти из программы'
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_args()


if __name__ == '__main__':
    main()