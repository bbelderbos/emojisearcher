from pathlib import Path
import re
from typing import Union

PREFERENCES_FILE = ".preferences"
MATCH_PREF_RE = re.compile(r"(\S+):(\S).*$")  # discard everything after emoji


def _is_comment(line: str) -> bool:
    return line.startswith("#")


def _load_preferences_file() -> Union[str, None]:
    try:
        return Path(PREFERENCES_FILE).read_text()
    except FileNotFoundError:
        return None


def load_preferences() -> dict[str, str]:
    preferences: dict[str, str] = {}
    content = _load_preferences_file()
    if content is None:
        return preferences

    for line in content.splitlines():
        if _is_comment(line):
            continue

        # could do a dictcomp but want to graciously ignore non matches
        match_ = MATCH_PREF_RE.match(line)
        if match_:
            description, emoji = match_.groups()
            # not lowercasing the description here, that is making
            # preferences case sensitive so user can have different
            # emojis for Ninja, NINJA and ninja
            preferences[description] = emoji

    print(preferences)
    return preferences
