## Pybites Emoji Searcher

I have been googling emojis and manually copying them to my clipboard.

Except for Slack + GitHub, there the `:` + autocomplete works great. For other tools, for example Facebook or plain blog / email writing, I needed a better way.

So here is a tool to look up emojis by text from the command line and automatically copy matching ones to the clipboard (using the awesome [pyperclip](https://pyperclip.readthedocs.io/en/latest/) tool).

By default it takes the first match in case there are multiple matching emojis. However if you append a dot (.) to a word you get to choose which emoji gets copied. You can also use a `.preferences` file to store overriding emojis or ones this tool does not provide.

I hope you enjoy this tool and don't hesitate to reach out to me by email: bob@pybit.es or just open an issues / open a PR if you see any opportunity for improvements.

### How to install and run it

```
$ git clone git@github.com:bbelderbos/emojisearcher.git
$ cd emojisearcher
$ python3.10 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

# or in one command
$ make setup

# search from cli
(venv) $ python -m emojisearcher.script bicep
Copied 💪 to clipboard

(venv) $ python -m emojisearcher.script snake
Copied 🐍 to clipboard

(venv) $ python -m emojisearcher.script tada
Copied 🎉 to clipboard

# search interactively (specially useful if there are multiple matches, you can choose)

(venv) $ python -m emojisearcher.script


------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a . if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
> snake
Copied 🐍 to clipboard

------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a . if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
> grin
Copied 😺 to clipboard

------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a . if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
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

------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a . if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
> q
Bye
```

### Easy of use: make a shell alias

Using a shell alias can be really convenient for this (assuming you have the project cloned in `~/code`):

```
# .zshrc
function emo {
    # subshell so you don't stay in the virtual env after running it
    (cd $HOME/code/emojisearcher && source venv/bin/activate && python -m emojisearcher.script "$@")
}

$ source ~/.zshrc
$ emo snake
Copied 🐍 to clipboard

# or get multiple emojis at once
$ emo snake bicep tada heart fire
Copied 🐍 💪 🎉 💓 🔥 to clipboard
```

After sourcing your .zshrc you can now get emojis copied to your clipboard fast using `emo bicep`, `emo tada` etc.

### Preferred emojis

_This section uses the shell alias I created in the previous step._

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

And some don't work (not sure why yet ...):

```
$ emo question
Copied  to clipboard
```

Since 0.6.0 you can create a `.preferences` file to create a mapping of missing / preferred emojis which will take precedence.

You can create this file in the root folder of the project or use the `EMOJI_PREFERENCES` environment variable to store it somewhere else:

```
$ export EMOJI_PREFERENCES=/Users/bbelderbos/.emoji_preferences
```

Let's look at this in action. Normally the tool would work like this:

```
$ emo heart
Copied 💓 to clipboard
$ emo cool
Copied 🆒 to clipboard
```

Say you added a preferences file like this:

```
$ cat .preferences
ninja:🥷  # missing (and much needed)
# overrides
eyes:😍  # replaces default 😁
heart:❤️   # replaces default 💓
hearts:💕  # replaces default 💞
# easier to remember
idea:💡  # also matches "bulb"
# trying to fix non-matching emojis
bliksem:⚡️  # this is Dutch
faster:🏃
```

Note that you can use (inline) comments.

Now with the preferences in place your shiny new emojis kick in first 🎉

```
$ emo heart
Copied ❤️ to clipboard

(no more 💓)

$ emo cool
Copied 😎 to clipboard

(no more 🆒)
```

Enjoy!

### Running the tests and other tools

```
(venv) $ pytest
# or
(venv) $ make cov

# run flake8 and mypy
(venv) $ make lint
(venv) $ make typing
```

### Rich

Originally Around 0.0.5 we started `rich` now to retrieve a list of emojis, it seems a bit more accurate (e.g. our beloved tada 🎉 emoji was missing!)

### OS alternatives

While sharing this [On Twitter](https://twitter.com/bbelderbos/status/1374414940988043264) I learned about other ways to get emojis (thanks Matt Harrison):

- Windows: Windows logo key  + . (period)

- Mac: CTRL + CMD + Space

Trying this on Mac, this does require the mouse though and it does not copy the emoji to your clipboard.
