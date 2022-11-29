import re
import sys

from rich._emoji_codes import EMOJI as EMOJI_MAPPING
from pyperclip import copy

from .preferences import load_preferences

QUIT = 'q'
SIGNAL_CHAR = '.'
PROMPT = f"""
------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a {SIGNAL_CHAR} if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
> """
NON_EMOJI_CHARS = re.compile('[^\U00010000-\U0010ffff]',
                             flags=re.UNICODE)


def clean_non_emoji_characters(emoji: str) -> str:
    return NON_EMOJI_CHARS.sub(r'', emoji)


def get_matching_emojis(
    words: list[str],
    *,
    preferences: dict[str, str] | None = None,
    interactive: bool = False
) -> list[str]:
    """
    Traverse words list finding matching emojis.

    If a preference emoji is set that takes precedence.

    If there are multiple matches take the first one unless
    interactive is set to True or the word ends with a SIGNAL_CHAR,
    which means user specified desire for interactive lookup.

    Making preferences "injectable" makes it testable and the
    existence of a .preferences does not mess with the tests.
    """
    if preferences is None:
        preferences = load_preferences()

    matches = []
    is_preference_emoji = False
    for word in words:
        if word in preferences:
            emojis = [preferences[word]]
            is_preference_emoji = True
        else:
            emojis = get_emojis_for_word(word.rstrip(SIGNAL_CHAR))
            if len(emojis) == 0:
                continue

        interactive_mode = word.endswith(SIGNAL_CHAR) or interactive
        if len(emojis) > 1 and interactive_mode:
            selected_emoji = user_select_emoji(emojis)
            if selected_emoji is None:
                continue
        else:
            selected_emoji = emojis[0]

        matches.append(
            selected_emoji if is_preference_emoji else
            clean_non_emoji_characters(selected_emoji)
        )

    return matches


def get_emojis_for_word(
    word: str, emoji_mapping: dict[str, str] = EMOJI_MAPPING
) -> list[str]:
    return [emo for name, emo in emoji_mapping.items() if word in name]


def user_select_emoji(emojis: list[str]) -> str | None:
    while True:
        try:
            for i, emo in enumerate(emojis, start=1):
                print(i, emo)
            user_input = input("Select the number of the emoji you want: ")
            idx = int(user_input)
            return emojis[idx - 1]
        except ValueError:
            print(f"{user_input} is not an integer.")
            continue
        except IndexError:
            print(f"{user_input} is not a valid option.")
            continue
        except KeyboardInterrupt:
            print(" Exiting selection menu.\n")
            return None


def copy_emojis_to_clipboard(matches: list[str]) -> None:
    all_matching_emojis = ' '.join(matches)
    print(f"Copied {all_matching_emojis} to clipboard")
    copy(all_matching_emojis)


def _match_emojis(text):
    words = text.split()
    matches = get_matching_emojis(words)
    if matches:
        copy_emojis_to_clipboard(matches)
    else:
        print(f"No matches for {text}")


def main(args):  # pragma: no cover
    if not args:
        while True:
            user_input = input(PROMPT)
            user_input = user_input.lower()
            if user_input == QUIT:
                print('Bye')
                break

            _match_emojis(user_input)
    else:
        text = " ".join(args)
        _match_emojis(text)


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
