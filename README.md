# Spotify Code Generator

Generate Spotify Code image URLs from Spotify links or Spotify URIs. The project
includes a small Python package, a command-line interface, and a Streamlit app.

The original version started in 2021 after I saw people drawing Spotify Codes by
hand. In 2026, I revisited the project and cleaned it up into a reusable tool.

![Spotify Code Generator preview](https://user-images.githubusercontent.com/58422765/131919943-727f5632-8852-4446-b285-5c16701e766d.png)

I also wrote a blog post about the first version:
[Spotify Kodlarini Inceleyelim](https://ozgecinko.medium.com/spotify-kodlar%C4%B1n%C4%B1-i%CC%87nceleyelim-af4a96d7f434)

## Features

- Convert Spotify URLs into canonical Spotify URIs
- Generate Spotify Code URLs for tracks, albums, artists, playlists, shows,
  episodes, and users
- Choose image format: `png`, `jpeg`, or `svg`
- Customize background color, code color, and image size
- Download generated codes from the CLI
- Use either the command line or the Streamlit web interface

## Installation

Clone the repository:

```bash
git clone https://github.com/ozgecinko/SpotifyCodeGenerator.git
cd SpotifyCodeGenerator
```

Create and activate a virtual environment:

```bash
python -m venv .env
source .env/bin/activate
```

Install the project:

```bash
pip install -e .
```

For the Streamlit app and development tools, install the optional dependencies:

```bash
pip install -e ".[app,dev]"
```

If you prefer using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## CLI Usage

Generate a Spotify Code URL:

```bash
spotify-code "https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6"
```

Download the generated image:

```bash
spotify-code "spotify:track:6rqhFgbbKwnb9MLmUQDhG6" \
  --output code.png \
  --format png \
  --background 000000 \
  --color white \
  --size 640
```

Print Markdown and HTML snippets:

```bash
spotify-code "https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6" --snippets
```

## Streamlit App

Run the web interface:

```bash
streamlit run app.py
```

Then paste a Spotify URL or URI, choose the output settings, and generate the
Spotify Code URL and preview.

## Python Usage

```python
from spotify_code_generator.core import build_code_url, to_spotify_uri

spotify_input = "https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6"

print(to_spotify_uri(spotify_input))
print(build_code_url(spotify_input, image_format="png", background_color="000000"))
```

## Supported Inputs

```text
spotify:track:6rqhFgbbKwnb9MLmUQDhG6
https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6
https://open.spotify.com/intl-tr/track/6rqhFgbbKwnb9MLmUQDhG6?si=example
```

Supported Spotify resource types:

- `track`
- `album`
- `artist`
- `playlist`
- `show`
- `episode`
- `user`

## Tests

Run the test suite:

```bash
pytest
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
