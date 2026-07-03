from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlparse

import requests


SUPPORTED_TYPES = {
    "track",
    "album",
    "artist",
    "playlist",
    "show",
    "episode",
    "user",
}

SUPPORTED_FORMATS = {"png", "jpeg", "svg"}
SUPPORTED_CODE_COLORS = {"white", "black"}


class SpotifyCodeError(ValueError):
    """Raised when a Spotify URL, URI, or code option is invalid."""


@dataclass(frozen=True)
class SpotifyResource:
    """Normalized Spotify resource information."""

    resource_type: str
    resource_id: str

    @property
    def uri(self) -> str:
        return f"spotify:{self.resource_type}:{self.resource_id}"


def _validate_resource(resource_type: str, resource_id: str) -> SpotifyResource:
    resource_type = resource_type.lower().strip()
    resource_id = resource_id.strip().split("?")[0]

    if resource_type not in SUPPORTED_TYPES:
        supported = ", ".join(sorted(SUPPORTED_TYPES))
        raise SpotifyCodeError(
            f"Unsupported Spotify resource type: {resource_type}. "
            f"Supported types: {supported}."
        )

    if not resource_id:
        raise SpotifyCodeError("Spotify resource ID cannot be empty.")

    # Spotify IDs are typically base62 strings. User IDs can be more varied,
    # so we allow a conservative set of URL-safe characters.
    if not re.fullmatch(r"[A-Za-z0-9._-]+", resource_id):
        raise SpotifyCodeError("Invalid Spotify resource ID.")

    return SpotifyResource(resource_type=resource_type, resource_id=resource_id)


def parse_spotify_input(value: str) -> SpotifyResource:
    """
    Parse a Spotify URL or URI into a normalized SpotifyResource.

    Supported examples:
        spotify:track:6rqhFgbbKwnb9MLmUQDhG6
        https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6
        https://open.spotify.com/intl-tr/track/6rqhFgbbKwnb9MLmUQDhG6
    """
    value = value.strip()

    if not value:
        raise SpotifyCodeError("Input cannot be empty.")

    if value.startswith("spotify:"):
        parts = value.split(":")
        if len(parts) < 3:
            raise SpotifyCodeError("Invalid Spotify URI. Expected spotify:type:id.")
        return _validate_resource(parts[1], parts[2])

    parsed = urlparse(value)

    if parsed.scheme not in {"http", "https"}:
        raise SpotifyCodeError("Input must be a Spotify URI or open.spotify.com URL.")

    if parsed.netloc not in {"open.spotify.com", "www.open.spotify.com"}:
        raise SpotifyCodeError("Only open.spotify.com URLs are supported.")

    path_parts = [part for part in parsed.path.split("/") if part]

    if not path_parts:
        raise SpotifyCodeError("Spotify URL must include a resource type and ID.")

    # Spotify sometimes includes locale prefixes such as /intl-tr/track/{id}.
    if path_parts[0].startswith("intl-"):
        path_parts = path_parts[1:]

    if len(path_parts) < 2:
        raise SpotifyCodeError("Spotify URL must include a resource type and ID.")

    return _validate_resource(path_parts[0], path_parts[1])


def to_spotify_uri(value: str) -> str:
    """Convert a Spotify URL or URI into canonical spotify:type:id format."""
    return parse_spotify_input(value).uri


def _normalize_hex_color(value: str) -> str:
    value = value.strip().replace("#", "")

    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise SpotifyCodeError("background_color must be a 6-digit hex color.")

    return value.upper()


def build_code_url(
    spotify_input: str,
    image_format: str = "png",
    background_color: str = "000000",
    code_color: str = "white",
    size: int = 640,
) -> str:
    """
    Build a Spotify Code image URL from a Spotify URL or URI.

    URL format:
    https://scannables.scdn.co/uri/plain/{format}/{background}/{color}/{size}/{spotify_uri}
    """
    spotify_uri = to_spotify_uri(spotify_input)
    image_format = image_format.lower().strip()
    code_color = code_color.lower().strip()
    background_color = _normalize_hex_color(background_color)

    if image_format not in SUPPORTED_FORMATS:
        supported = ", ".join(sorted(SUPPORTED_FORMATS))
        raise SpotifyCodeError(f"image_format must be one of: {supported}.")

    if code_color not in SUPPORTED_CODE_COLORS:
        supported = ", ".join(sorted(SUPPORTED_CODE_COLORS))
        raise SpotifyCodeError(f"code_color must be one of: {supported}.")

    if not 80 <= size <= 4096:
        raise SpotifyCodeError("size must be between 80 and 4096 pixels.")

    # Keep ':' unescaped because Spotify's scannables endpoint accepts the URI
    # in canonical spotify:type:id form.
    encoded_uri = quote(spotify_uri, safe=":")

    return (
        "https://scannables.scdn.co/uri/plain/"
        f"{image_format}/{background_color}/{code_color}/{size}/{encoded_uri}"
    )


def markdown_image(code_url: str, alt_text: str = "Spotify Code") -> str:
    """Return a Markdown image snippet for a Spotify Code URL."""
    return f"![{alt_text}]({code_url})"


def html_image(code_url: str, alt_text: str = "Spotify Code") -> str:
    """Return an HTML image snippet for a Spotify Code URL."""
    return f'<img src="{code_url}" alt="{alt_text}" />'


def download_code(
    spotify_input: str,
    output_path: str | Path,
    image_format: str = "png",
    background_color: str = "000000",
    code_color: str = "white",
    size: int = 640,
) -> Path:
    """Download a Spotify Code image to disk."""
    url = build_code_url(
        spotify_input=spotify_input,
        image_format=image_format,
        background_color=background_color,
        code_color=code_color,
        size=size,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    output_path.write_bytes(response.content)
    return output_path
