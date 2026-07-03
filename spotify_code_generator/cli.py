from __future__ import annotations

import argparse

from spotify_code_generator.core import (
    SpotifyCodeError,
    build_code_url,
    download_code,
    html_image,
    markdown_image,
    to_spotify_uri,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spotify-code",
        description="Generate Spotify Code URLs and images from Spotify links or URIs.",
    )

    parser.add_argument("spotify_input", help="Spotify URL or URI")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output path. If provided, the Spotify Code image is downloaded.",
    )
    parser.add_argument("--format", choices=["png", "jpeg", "svg"], default="png")
    parser.add_argument(
        "--background",
        default="000000",
        help="Background color as hex, e.g. 000000 or FFFFFF.",
    )
    parser.add_argument("--color", choices=["white", "black"], default="white")
    parser.add_argument("--size", type=int, default=640, help="Image size in pixels.")
    parser.add_argument(
        "--snippets",
        action="store_true",
        help="Print Markdown and HTML snippets.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        uri = to_spotify_uri(args.spotify_input)
        code_url = build_code_url(
            spotify_input=args.spotify_input,
            image_format=args.format,
            background_color=args.background,
            code_color=args.color,
            size=args.size,
        )

        print(f"Spotify URI: {uri}")
        print(f"Spotify Code URL: {code_url}")

        if args.snippets:
            print("\nMarkdown:")
            print(markdown_image(code_url))
            print("\nHTML:")
            print(html_image(code_url))

        if args.output:
            output_path = download_code(
                spotify_input=args.spotify_input,
                output_path=args.output,
                image_format=args.format,
                background_color=args.background,
                code_color=args.color,
                size=args.size,
            )
            print(f"\nDownloaded to: {output_path}")

    except SpotifyCodeError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
