from __future__ import annotations

import streamlit as st

from spotify_code_generator.core import (
    SpotifyCodeError,
    build_code_url,
    html_image,
    markdown_image,
    to_spotify_uri,
)


st.set_page_config(page_title="Spotify Code Generator", page_icon="🎧")

st.title("Spotify Code Generator")
st.write("Generate Spotify Code URLs from Spotify links or Spotify URIs.")

spotify_input = st.text_input(
    "Spotify URL or URI",
    placeholder="https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6",
)

col1, col2 = st.columns(2)

with col1:
    image_format = st.selectbox("Image format", ["png", "jpeg", "svg"])
    code_color = st.selectbox("Code color", ["white", "black"])

with col2:
    background_color = st.color_picker("Background color", "#000000")
    size = st.slider("Size", min_value=80, max_value=4096, value=640, step=80)

if st.button("Generate", type="primary"):
    try:
        spotify_uri = to_spotify_uri(spotify_input)
        code_url = build_code_url(
            spotify_input=spotify_input,
            image_format=image_format,
            background_color=background_color,
            code_color=code_color,
            size=size,
        )

        st.subheader("Spotify URI")
        st.code(spotify_uri)

        st.subheader("Spotify Code URL")
        st.code(code_url)

        st.subheader("Preview")
        if image_format in {"png", "jpeg"}:
            st.image(code_url)
        else:
            st.markdown(f"[Open SVG]({code_url})")

        st.subheader("Markdown")
        st.code(markdown_image(code_url))

        st.subheader("HTML")
        st.code(html_image(code_url))

    except SpotifyCodeError as error:
        st.error(str(error))
