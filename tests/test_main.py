# -*- coding: utf-8 -*-
from unittest import mock

import pytest

import pytube
from pytube import YouTube
from pytube.exceptions import RegexMatchError


@mock.patch("pytube.__main__.YouTube")
def test_prefetch_deferred(youtube):
    instance = youtube.return_value
    instance.prefetch_descramble.return_value = None
    YouTube("https://www.youtube.com/watch?v=9bZkp7q19f0", True)
    assert not instance.prefetch_descramble.called


@mock.patch("urllib.request.install_opener")
def test_install_proxy(opener):
    proxies = {"http": "http://www.example.com:3128/"}
    YouTube(
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
        proxies=proxies,
    )
    opener.assert_called()


@mock.patch("pytube.request.get")
def test_video_unavailable(get):
    get.return_value = ""
    youtube = YouTube("https://www.youtube.com/watch?v=9bZkp7q19f0")
    with pytest.raises(RegexMatchError):
        youtube.check_availability()


def test_video_keywords(cipher_signature):
    expected = [
        'Rewind', 'Rewind 2019',
        'youtube rewind 2019', '#YouTubeRewind',
        'MrBeast', 'PewDiePie', 'James Charles',
        'Shane Dawson', 'CaseyNeistat', 'RiceGum',
        'Simone Giertz', 'JennaMarbles', 'Lilly Singh',
        'emma chamberlain', 'The Try Guys', 'Fortnite',
        'Minecraft', 'Roblox', 'Marshmello',
        'Garena Free Fire', 'GTA V', 'Lachlan',
        'Anaysa', 'jeffreestar', 'Noah Schnapp',
        'Jennelle Eliana', 'T-Series', 'Azzyland',
        'LazarBeam', 'Dude Perfect', 'David Dobrik',
        'KSI', 'NikkieTutorials', 'Kurzgesagt',
        'Jelly', 'Ariana Grande', 'Billie Eilish',
        'BLACKPINK', 'Year in Review'
    ]
    assert cipher_signature.keywords == expected


def test_js_caching(cipher_signature):
    assert pytube.__js__ is not None
    assert pytube.__js_url__ is not None
    assert pytube.__js__ == cipher_signature.js
    assert pytube.__js_url__ == cipher_signature.js_url
