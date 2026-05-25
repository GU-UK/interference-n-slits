import argparse

from src.animation import DEFAULT_PARAMETERS, export_animation
from src.interactive import run_interactive


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Моделирование интерференции от N щелей",
    )

    subparsers = parser.add_subparsers(dest="command")

    gif_parser = subparsers.add_parser(
        "gif",
        help="Экспортировать GIF-анимацию",
    )

    gif_parser.add_argument(
        "--parameter",
        required=True,
        choices=list(DEFAULT_PARAMETERS.keys()),
        help="Параметр, который будет изменяться",
    )

    gif_parser.add_argument(
        "--start",
        required=True,
        type=float,
        help="Начальное значение параметра",
    )

    gif_parser.add_argument(
        "--end",
        required=True,
        type=float,
        help="Конечное значение параметра",
    )

    gif_parser.add_argument(
        "--duration",
        default=5.0,
        type=float,
        help="Длительность GIF в секундах",
    )

    gif_parser.add_argument(
        "--frames",
        default=40,
        type=int,
        help="Количество кадров",
    )

    gif_parser.add_argument(
        "--output",
        default="assets/interference.gif",
        help="Путь для сохранения GIF",
    )

    args = parser.parse_args()

    if args.command == "gif":
        export_animation(
            parameter=args.parameter,
            start=args.start,
            end=args.end,
            duration=args.duration,
            filename=args.output,
            frame_count=args.frames,
        )
    else:
        run_interactive()


if __name__ == "__main__":
    main()