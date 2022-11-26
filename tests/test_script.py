from inspect import cleandoc
from unittest.mock import patch

import pytest

from emojisearcher.script import (clean_non_emoji_characters,
                                  get_matching_emojis,
                                  get_emojis_for_word,
                                  user_select_emoji)


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
])
def test_get_matching_emojis(words, matches):
    assert get_matching_emojis(
        words.split(), preferences={}
    ) == matches


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
