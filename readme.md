# Word Randomizer

You can use this to generate potentially made-up words, for example for nicknames and such.

The output will have somewhat of a similar feel to the input.

```bash
./word-randomizer.py --help
```

## Examples

```
./word-randomizer.py --word github --number 5 --strategy randomize-word
doksyc tajrig jagvyx getzuk betvuq
```

```
./word-randomizer.py --word foobar --number 5 --prefix a --suffix b --strategy randomize-random-letter
asoobarb asoobafb asoibafb asoicafb asoicanb
```
