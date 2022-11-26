from inspect import cleandoc
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from emojisearcher.preferences import load_preferences
from emojisearcher.script import (clean_non_emoji_characters,
                                  get_matching_emojis,
                                  get_emojis_for_word,
                                  user_select_emoji)

PREFERENCE_FILE_CONTENT = """
ninja:🥷  # missing (and much needed)
# overrides
eyes:😍  # replaces default 😁
heart:❤️   # replaces default 💓
hearts:💕  # replaces default 💞
# easier to remember
idea:💡  # also matches "bulb"
# trying to fix non-working emojis
bliksem:⚡️  # this is Dutch
faster:🏃
"""


@pytest.fixture(scope="session")
def add_preferences():
    prefs_file = os.environ.get("EMOJI_PREFERENCES")
    assert prefs_file is not None

    prefs_file = Path(prefs_file)
    prefs_file.write_text(PREFERENCE_FILE_CONTENT)

    yield

    prefs_file.unlink()


@pytest.mark.parametrize("word, expected", [
    ("🤽\u200d♂️'", "🤽"),
    ("12🤽34", "🤽"),
    ("abc🤽ñ=)", "🤽"),
])
def test_clean_non_emoji_characters(word, expected):
    assert clean_non_emoji_characters(word) == expected


@pytest.mark.parametrize("words, matches", [
    ("heart snake beer", ['💓', '🐍', '🍺']),
    ("hand scream angry", ['👌', '😱', '😠']),
    ("struck dog", ['🤩', '🐶']),
    ("slee tree fire water cat", ['😴', '🎄', '🔥', '🤽', '🈸']),
    ("ninja", []),  # following do work with *with_preferences :)
    ("eyes", ["😁"]),
    ("bliksem", []),  # this is Dutch, we use it as preference below
    ("faster", []),
])
def test_get_matching_emojis(words, matches):
    assert get_matching_emojis(words.split(), preferences={}) == matches


@pytest.mark.parametrize("words, matches", [
    ("ninja", ['🥷']),
    ("eyes", ['😍']),
    ("hearts idea", ['💕', '💡']),  # prefs work with 2 as well
    ("faster", ['🏃']),
])
def test_user_preferences(add_preferences, words, matches):
    preferences = load_preferences()
    assert get_matching_emojis(words.split(), preferences=preferences) == matches


@patch("emojisearcher.script.user_select_emoji", side_effect=['💓'])
def test_get_emojis_for_word_with_user_input(mock_user_inp):
    matches = get_matching_emojis(["heart"], preferences={}, interactive=True)
    assert matches[0] == '💓'


@patch("emojisearcher.script.user_select_emoji", side_effect=[None])
def test_get_emojis_for_word_with_user_cancelling(mock_user_inp):
    assert get_matching_emojis(["heart"], preferences={}, interactive=True) == []


def test_user_prefs_with_larger_emoji(add_preferences):
    preferences = load_preferences()
    matches = get_matching_emojis(["bliksem"], preferences=preferences)
    encoded_actual_emoji = matches[0].encode('unicode-escape')
    assert len(encoded_actual_emoji) == 6
    encoded_expected_emoji = '⚡️'.encode('unicode-escape')
    assert len(encoded_expected_emoji) == 12
    assert encoded_actual_emoji in encoded_actual_emoji


@pytest.mark.parametrize("word, num_results, emoji", [
    ("heart", 36, '💓'),
    ("snake", 1, '🐍'),
    ("grin", 9, '😺'),
])
def test_get_emojis_for_word(word, num_results, emoji):
    result = get_emojis_for_word(word)
    assert len(result) == num_results
    assert result[0] == emoji


@patch("builtins.input", side_effect=['a', 10, 2, 'q'])
def test_user_selects_tree_emoji(mock_input, capfd):
    trees = ['🎄', '🌳', '🌲', '🌴', '🎋']
    ret = user_select_emoji(trees)
    assert ret == "🌳"
    actual = capfd.readouterr()[0].strip()
    expected = cleandoc("""
    1 🎄
    2 🌳
    3 🌲
    4 🌴
    5 🎋
    a is not an integer.
    1 🎄
    2 🌳
    3 🌲
    4 🌴
    5 🎋
    10 is not a valid option.
    1 🎄
    2 🌳
    3 🌲
    4 🌴
    5 🎋
    """)
    assert actual == expected


def test_load_empty_file():
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv('EMOJI_PREFERENCES', 'non-existent-prefs-file')
        assert load_preferences() == {}
