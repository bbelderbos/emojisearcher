## Emoji Searcher

Automate the boring stuff: I have been googling emojis and manually copying them to my clipboard (it's especially painful when posting to Facebook).

So it was time to write a script to look up emojis by text from the command line and copy them to the clipboard.

By default it takes the first match in case there are multiple matching emojis. However if you append a dot (.) to a word you get to choose which emoji gets copied.

### How to install and run it

```
$ git clone git@github.com:bbelderbos/emojisearcher.git
$ cd emojisearcher
$ python3.10 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

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
many more
...
35 😻
36 😍
Select the number of the emoji you want: 36
Copied 😍 to clipboard
```

And some don't work for some reason:

```
$ emo question
Copied  to clipboard
```

Since 0.6.0 you can create a `.preferences` file to create a mapping of missing / preferred emojis which will take precedence (you can use comments, they will be ignored):

```
$ cat .preferences
ninja:🥷 # missing (and much needed)
# overrides
eyes:😍 # replaces default 😁
heart:❤️  # replaces default 💓
hearts:💕 # replaces default 💞
# easier to remember
idea:💡 # also matches "bulb"
# trying to fix non-working emojis
question:❓
```

Without this file:

```
$ emo heart
Copied 💓 to clipboard
$ emo cool
Copied 🆒 to clipboard
```

Now with the preferences in place:

```
$ emo heart
Copied ❤️ to clipboard
$ emo cool
Copied 😎 to clipboard
```

💡 I was considering making this file updatable via the app, but it adds extra complexity and command line arguments. I like to keep it simple for now and it's easy enough to update the preferences file in your editor.

### Running the tests

```
(venv) $ pip install -r requirements-dev.txt
(venv) $ pytest
```


### Rich

Update: I am using `rich` now to retrieve a list of emojis, it seems a bit more accurate (e.g. our beloved 🎉 emoji). I will be enhancing the cli interface with this awesome library ...

### Other ways

While sharing this on social media I learned about some useful OS shortcuts to retrieve emojis, [thanks Matt!](https://twitter.com/bbelderbos/status/1374414940988043264)
