#!/usr/bin/env python3
# ./word-randomizer.py --help
# ./word-randomizer.py --word foobar --number 5

import sys
import random
import argparse
from enum import Enum
from typing import List

VOWELS = ["a", "e", "i", "o", "u", "y"]
HARD_CONSONANTS = ["b", "c", "d", "g", "j", "k", "p", "q", "t", "x"]
SOFT_CONSONANTS = ["f", "h", "l", "m", "n", "r", "s", "v", "w", "z"]


class Strategy(Enum):
    ROTATE_RANDOM_LETTER = "rotate-random-letter"
    ROTATE_WORD = "rotate-word"
    RANDOMIZE_WORD = "randomize-word"
    RANDOMIZE_RANDOM_LETTER = "randomize-random-letter"


class ConfigService:
    word: str
    suffix: str
    prefix: str
    number: int
    exclude: List[str]
    strategy: str

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--word",
            required=True,
            metavar="",
            type=str,
        )
        parser.add_argument(
            "--suffix",
            default="",
            metavar="",
            type=str,
        )
        parser.add_argument(
            "--prefix",
            default="",
            metavar="",
            type=str,
        )
        parser.add_argument(
            "--number",
            default=100,
            metavar="",
            type=int,
            help="how many word to generate",
        )
        parser.add_argument(
            "--exclude",
            default="",
            metavar="LIST",
            type=list,
            help='which letters to not consider, for example "abcd"',
        )
        parser.add_argument(
            "--strategy",
            default=Strategy.RANDOMIZE_RANDOM_LETTER.value,
            metavar="",
            type=str,
            help=(
                'one of "rotate-random-letter", "rotate-word", "randomize-word" or '
                '"randomize-random-letter" (default)'
            ),
        )

        args = parser.parse_args()
        self.word = args.word
        self.suffix = args.suffix
        self.prefix = args.prefix
        self.number = args.number
        self.exclude = args.exclude
        self.strategy = args.strategy


class Main:
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def main(self):
        word = self.config_service.word
        strategy = self.config_service.strategy

        for _ in range(self.config_service.number):
            if strategy == Strategy.ROTATE_WORD.value:
                word = self._rotate_word(word)
            elif strategy == Strategy.ROTATE_RANDOM_LETTER.value:
                word = self._rotate_random_letter(word)
            elif strategy == Strategy.RANDOMIZE_RANDOM_LETTER.value:
                word = self._randomize_random_letter(word)
            elif strategy == Strategy.RANDOMIZE_WORD.value:
                word = self._randomize_word(word)
            else:
                raise Exception(f'Unknown strategy "{strategy}"')

            sys.stdout.write(self.config_service.prefix)
            sys.stdout.write(word)
            sys.stdout.write(self.config_service.suffix)
            sys.stdout.write(" ")

        sys.stdout.write("\n")

    def _get_related_letters(self, letter: str) -> List[str]:
        letters = HARD_CONSONANTS
        if letter in VOWELS:
            letters = VOWELS
        if letter in SOFT_CONSONANTS:
            letters = SOFT_CONSONANTS
        return letters

    def _rotate_letter(self, letter: str) -> str:
        letters = self._get_related_letters(letter)

        new_letter = letters[(letters.index(letter) + 1) % len(letters)]
        while new_letter in self.config_service.exclude:
            new_letter = letters[(letters.index(new_letter) + 1) % len(letters)]

            if new_letter == letter:
                raise Exception(f'Failed to find a new letter to replace "{letter}"')

        return new_letter

    def _pick_random_letter(self, letter: str) -> str:
        letters = self._get_related_letters(letter)

        return random.choice(
            [letter for letter in letters if letter not in self.config_service.exclude]
        )

    def _rotate_word(self, word: str) -> str:
        return "".join([self._rotate_letter(letter) for letter in word])

    def _randomize_word(self, word: str) -> str:
        return "".join([self._pick_random_letter(letter) for letter in word])

    def _rotate_random_letter(self, word: str) -> str:
        index = random.randint(0, len(word) - 1)
        return word[:index] + self._rotate_letter(word[index]) + word[index + 1 :]

    def _randomize_random_letter(self, word: str) -> str:
        index = random.randint(0, len(word) - 1)
        return word[:index] + self._pick_random_letter(word[index]) + word[index + 1 :]


if __name__ == "__main__":
    Main(ConfigService()).main()
