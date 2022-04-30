## Emoji Searcher

Automate the boring stuff: I have been googling emojis and manually copying them to my clipboard (it's especially painful when posting to Facebook).

So it was time to write a script to look up emojis by text from the command line and copy them to the clipboard.

By default it takes the first match in case there are multiple matching emojis. However if you append a dot (.) to a word you get to choose which emoji gets copied.

### How to run it

```
$ git clone git@github.com:bbelderbos/emojisearcher.git
$ cd emojisearcher
$ python3.10 -m venv venv
$ pip install -r requirements.txt
$ source venv/bin/activate

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


# running the tests
(venv) $ pip install -r requirements-dev.txt
(venv) $ pytest
```

Using a shell alias can be really convenient for this:

```
# .zshrc
function emo {
    cd $HOME/code/emojisearcher && ae && python -m emojisearcher.script "$1"
}
```

After sourcing your .zshrc you can now get emojis copied to your clipboard fast using `emo bicep`, `emo tada` etc.

### Rich

Update: I am using `rich` now to retrieve a list of emojis, it seems a bit more accurate (e.g. our beloved 🎉 emoji). I will be enhancing the cli interface with this awesome library ...

### Other ways

While sharing this on social media I learned about some useful OS shortcuts to retrieve emojis, [thanks Matt!](https://twitter.com/bbelderbos/status/1374414940988043264)
