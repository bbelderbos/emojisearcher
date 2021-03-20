import pytest

from fastemoji.script import (clean_non_emoji_characters,
                              get_matching_emojis,
                              get_emojis_for_word)


@pytest.mark.parametrize("word, expected", [
    ("🤽\u200d♂️'", "🤽"),
    ("12🤽34", "🤽"),
    ("abc🤽ñ=)", "🤽"),
])
def test_clean_non_emoji_characters(word, expected):
    assert clean_non_emoji_characters(word) == expected


@pytest.mark.parametrize("words, matches", [
    ("heart snake beer", ['🫀', '🐍', '🍺']),
    ("hand scream angry", ['👌', '😱', '😠']),
    ("struck dog", ['🤩', '🐕']),
    ("slee tree fire water cat", ['😴', '🎄', '🔥', '🤽', '🈸']),
])
def test_get_matching_emojis(words, matches):
    assert get_matching_emojis(words.split()) == matches


@pytest.mark.parametrize("word, num_results, emoji", [
    ("heart", 130, '🫀'),
    ("snake", 1, '🐍'),
    ("grin", 7, '😺'),
])
def test_get_emojis_for_word(word, num_results, emoji):
    result = get_emojis_for_word(word)
    assert len(result) == num_results
    assert result[0] == emoji
