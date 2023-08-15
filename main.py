import argparse

from joyreactor_stats import JoyreactorStats


version = '1.1.0'


def parse_args():
    parser = argparse.ArgumentParser(
        prog='joyreactor_stats',
        description='Get Joyreactor stats v.%s' % version + ' (c) 2023 Genzo (https://github.com/Genzo4/joyreactor_stats)',
        add_help=False
        )

    parser.add_argument(
        dest='account',
        type=str,
        help='Аккаунт на Joyrector, для которого собирается статистика'
    )

    parser.add_argument(
        '-pi',
        '--post_id',
        dest='post_id',
        type=int,
        default=0,
        help='id отслеживаемого поста'
    )

    parser.add_argument(
        '-d',
        '--delay',
        dest='delay',
        type=int,
        default=10,
        choices=range(10, 1441, 10),
        help='Задержка проверки поста (в мин.)'
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

    joy_stats = JoyreactorStats(
        args.account,
        show_progress=not args.no_progress,
        open_xls=not args.dont_open,
        quiet=args.quiet
        )

    if args.post_id == 0:
        joy_stats.work()
    else:
        joy_stats.post_traking(args.post_id, args.delay)


if __name__ == '__main__':
    main()
