import os
import argparse

from .subset_font import subset_font, set_quiet

SUPPORTED_FORMATS = ["woff", "woff2"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=str, help="font path")
    parser.add_argument("-q", "--quiet", help="do not print logs", action="store_true")
    parser.add_argument(
        "--output-dir", type=str, help="fonts output dir", default="./output/"
    )
    parser.add_argument(
        "--noexport-css",
        help="do not generate CSS file with this flag",
        action="store_true",
    )
    parser.add_argument(
        "--font-url", type=str, help="font URL to be written on .css file", default=""
    )
    parser.add_argument("--family", type=str, help="font family")
    parser.add_argument(
        "--style",
        choices=["normal", "italic", "oblique"],
        default="normal",
        help="font style",
    )
    parser.add_argument(
        "--weight",
        default=400,
        help="font weight (100-900, normal, bold, lighter, bolder, inherit, initial, unset)",
    )
    parser.add_argument(
        "--format", type=str, help="delimited output formats", default="woff2"
    )

    args = parser.parse_args()

    if not os.path.exists(args.font):
        raise (Exception(f"{args.font} not exists"))
    if (
        args.weight
        not in [
            "normal",
            "bold",
            "lighter",
            "bolder",
            "inherit",
            "initial",
            "unset",
        ]
        and int(args.weight) not in range(100, 1000, 100)
    ):
        raise (Exception("argument --weight: not compatible"))
    formats = args.format.split(",")
    for format in formats:
        if format not in SUPPORTED_FORMATS:
            raise (Exception(f"format {format} is not a supported format"))

    if args.quiet:
        set_quiet()

    subset_font(
        args.font,
        output_dir=args.output_dir,
        noexport_css=args.noexport_css,
        font_url=args.font_url,
        formats=formats,
        family=args.family,
        style=args.style,
        weight=args.weight,
    )


if __name__ == "__main__":
    main()