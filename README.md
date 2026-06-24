## Emoji Searcher

I have been googling emojis and manually copying them to my clipboard.

Except for Slack + GitHub, there the `:` + autocomplete works great. For other tools, for example Facebook or plain blog / email writing, I needed a better way.

So here is a tool to look up emojis by text from the command line and automatically copy matching ones to the clipboard (using the awesome [pyperclip](https://pyperclip.readthedocs.io/en/latest/) tool).

By default it takes the first match in case there are multiple matching emojis. However if you append a dot (.) to a word you get to choose which emoji gets copied. You can also use a `.preferences` file to store overriding emojis or ones this tool does not provide.

I hope you enjoy this tool; open an issue (or PR) if you see an opportunity for improvements.

### How to install and run it

It's published on [PyPI](https://pypi.org/project/emojisearcher/), so the easiest way to run it is with [`uvx`](https://docs.astral.sh/uv/) — no clone, no virtualenv:

```
# search from the cli (copies the match to your clipboard)
$ uvx --from emojisearcher emo bicep
Copied 💪 to clipboard

$ uvx --from emojisearcher emo snake
Copied 🐍 to clipboard

$ uvx --from emojisearcher emo tada
Copied 🎉 to clipboard
```

Run it without arguments for interactive mode (handy when there are multiple matches and you want to pick one):

```
$ uvx --from emojisearcher emo

------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a . if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
> snake
Copied 🐍 to clipboard

> grin.
1 😺
2 😸
3 😀
4 😃
5 😄
6 😅
7 😆
8 😀
9 😁
Select the number of the emoji you want: 4
Copied 😃 to clipboard

> q
Bye
```

### Ease of use: make a shell alias

Typing `uvx --from emojisearcher emo` every time is a mouthful, so wrap it in a shell alias (same idea as `uvx --from pybites-search search`):

```
# .zshrc
function emo {
    uvx --from emojisearcher emo "$@"
}
```

```
$ source ~/.zshrc
$ emo snake
Copied 🐍 to clipboard

# or get multiple emojis at once
$ emo snake bicep tada heart fire
Copied 🐍 💪 🎉 💓 🔥 to clipboard
```

After sourcing your `.zshrc` you can get emojis copied to your clipboard fast using `emo bicep`, `emo tada` etc.

### Preferred emojis

Sometimes you don't get a match:

```
$ emo ninja
No matches for ninja
```

Or you get way too many:

```
$ emo heart.
1 💓
2 🖤
...
...
35 😻
36 😍
Select the number of the emoji you want: 36
Copied 😍 to clipboard
```

For these cases you can create a `.preferences` file to map words to specific emojis — missing ones, or overrides that take precedence over the default match.

Since you run the tool with `uvx` from any directory, point the `EMOJI_PREFERENCES` environment variable at an absolute path:

```
$ export EMOJI_PREFERENCES=$HOME/.emoji_preferences
```

A preferences file looks like this:

```
$ cat $EMOJI_PREFERENCES
ninja:🥷  # missing (and much needed)
# overrides
eyes:😍  # replaces default 😁
heart:❤️   # replaces default 💓
hearts:💕  # replaces default 💞
# easier to remember
idea:💡  # also matches "bulb"
# words in another language
bliksem:⚡️  # this is Dutch
faster:🏃
```

Note that you can use (inline) comments.

Now with the preferences in place your shiny new emojis kick in first 🎉

```
$ emo heart
Copied ❤️ to clipboard

(no more 💓)
```

Enjoy!

### Running the tests and other tools

To hack on the code, clone the repo and use [uv](https://docs.astral.sh/uv/):

```
$ git clone git@github.com:bbelderbos/emojisearcher.git
$ cd emojisearcher
$ uv run pytest
$ uv run ruff format .
$ uv run ruff check .
$ uv run ty check .
```

### Rich

Around 0.0.5 we started using `rich` to retrieve the list of emojis, it seems a bit more accurate (e.g. our beloved tada 🎉 emoji was missing before!).

### OS alternatives

While sharing this [on Twitter](https://twitter.com/bbelderbos/status/1374414940988043264) I learned about other ways to get emojis (thanks Matt Harrison):

- Windows: Windows logo key + . (period)

- Mac: CTRL + CMD + Space

Trying this on Mac, this does require the mouse though and it does not copy the emoji to your clipboard.
