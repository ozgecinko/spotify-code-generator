"""Spotify Code Generator."""

from .core import (
    SpotifyCodeError,
    build_code_url,
    download_code,
    parse_spotify_input,
    to_spotify_uri,
)

__all__ = [
    "SpotifyCodeError",
    "build_code_url",
    "download_code",
    "parse_spotify_input",
    "to_spotify_uri",
]

__version__ = "0.1.0"
