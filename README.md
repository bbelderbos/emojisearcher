## Emoji Searcher

Automate the boring stuff: I have been googling emojis and manually copying them to my clipboard.

So it was time to write a script to look up emojis by text from the command line and copy them to the clipboard.

By default it takes the first match in case there are multiple matching emojis. However if you append a dot (.) to a word you get to choose which emoji gets copied.

### How to run it

```
git clone git@github.com:bbelderbos/emojisearcher.git
cd emojisearcher
poetry install
poetry run emo
```

(New to `poetry`? [Start here](https://python-poetry.org/docs/).)

You can also make a shell alias:

```
# .bashrc
alias emo="cd $HOME/code/emojisearcher && poetry run emo"
```

### Other ways

While sharing this on social media I learned about some useful OS shortcuts to retrieve emojis, [thanks Matt!](https://twitter.com/bbelderbos/status/1374414940988043264)
