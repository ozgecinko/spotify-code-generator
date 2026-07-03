import pytest

from spotify_code_generator.core import (
    SpotifyCodeError,
    build_code_url,
    html_image,
    markdown_image,
    parse_spotify_input,
    to_spotify_uri,
)


def test_parse_track_url():
    result = parse_spotify_input("https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6")

    assert result.resource_type == "track"
    assert result.resource_id == "6rqhFgbbKwnb9MLmUQDhG6"
    assert result.uri == "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"


def test_parse_localized_track_url():
    result = parse_spotify_input(
        "https://open.spotify.com/intl-tr/track/6rqhFgbbKwnb9MLmUQDhG6?si=abc"
    )

    assert result.uri == "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"


def test_to_spotify_uri_from_uri():
    assert (
        to_spotify_uri("spotify:album:1ATL5GLyefJaxhQzSPVrLX")
        == "spotify:album:1ATL5GLyefJaxhQzSPVrLX"
    )


def test_build_code_url():
    url = build_code_url(
        "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
        image_format="png",
        background_color="#000000",
        code_color="white",
        size=640,
    )

    assert url == (
        "https://scannables.scdn.co/uri/plain/"
        "png/000000/white/640/spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
    )


def test_snippets():
    url = "https://example.com/code.png"
    assert markdown_image(url) == "![Spotify Code](https://example.com/code.png)"
    assert html_image(url) == '<img src="https://example.com/code.png" alt="Spotify Code" />'


def test_invalid_input():
    with pytest.raises(SpotifyCodeError):
        to_spotify_uri("https://example.com/track/abc")


def test_invalid_color():
    with pytest.raises(SpotifyCodeError):
        build_code_url(
            "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
            background_color="not-a-color",
        )
