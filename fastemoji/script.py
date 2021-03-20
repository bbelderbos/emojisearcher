import emoji
import pyperclip

LANGUAGE = 'en'
QUIT = 'q'


def get_emojis(word: str, lang: str = LANGUAGE) -> list[str]:
    return [emo for name, emo in emoji.EMOJI_UNICODE[lang].items()
            if word in name]


def select_emoji(emojis: list[str]) -> str:
    while True:
        try:
            for i, emo in enumerate(emojis, start=1):
                print(i, emo)
            user_input = input("Select which emoji you want? ")
            idx = int(user_input)
            return emojis[idx - 1]
        except ValueError:
            print(f"{user_input} is not an integer: ")
            continue


def main():
    while True:
        user_input = input("Type one or more emoji related words (type 'q' for exit): ")
        user_input = user_input.lower()
        if user_input == QUIT:
            print('Bye')
            break

        matches = []
        words = user_input.split()
        for word in words:
            emojis = get_emojis(word)
            if len(emojis) == 0:
                continue

            selected_emoji = emojis[0] if len(emojis) == 1 else select_emoji(emojis)
            matches.append(selected_emoji)

        all_matching_emojis = ' '.join(matches)
        print(f"Copying {all_matching_emojis} to clipboard")
        pyperclip.copy(all_matching_emojis)


if __name__ == "__main__":
    main()
