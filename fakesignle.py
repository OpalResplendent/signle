#!/usr/bin/python3.9
# Copyright (c) 2021 MobileCoin Inc.
# Copyright (c) 2021 The Forest Team


# for testing
import sys
from typing import TypedDict

from words import acceptable_words, wordlist
import random

# TODO: better accepted guess list, seem to be missing lots of -ing and -ed, etc

additional_words = {
    "goblin",
    "kobold",
    "ferret",
    "kitten",
    "karkat",
    "signle"
}
wordlist.update(additional_words)
acceptable_words.update(wordlist)

# palette: 🟩🟨⬛🆒

class Message:
    timestamp: int
    text: str
    attachments: list[dict[str, str]]
    quoted_text: str
    mentions: list[dict[str, str]]
    source: str
    uuid: str
    payment: dict
    arg0: str

# actual gamestate
class Game:
    word = ''
    tries = 0
    wins = 0
    guesshistory = []
    resulthistory = []
    correctletters = {}
    correctpositions = []

    def reset(self):
        self.word = random.choice(tuple(wordlist))
        self.tries = 0
        self.guesshistory.clear()
        self.resulthistory.clear()
        self.correctletters.clear()
        self.correctpositions.clear()
        return

    def guess(self, guess: str):
        output = ''

        if guess == self.word:
            output = ''.join(self.resulthistory)
            output += '🆒🆒🆒🆒🆒🆒\n'
            output += 'correct word was: ' + self.word
            self.reset()
            return output

        if len(guess) != 6: return 'guess must be 6 letters'
        if guess not in acceptable_words: return 'must be an english word'
        if guess in self.guesshistory: return 'already guessed that'

        for i in range(6):
            if guess[i] == self.word[i]:
                output += '🟩'
            else:
                found = False
                for j in range(6):
                    if guess[i] == self.word[j]:
                        output += '🟨'
                        found = True
                        break
                if found == False: 
                    output += '⬛'
        
        count = 0
        for i in range(6):
            if guess[i] != '🟩':
                break
        if count == 6: output = '🆒🆒🆒🆒🆒🆒'

        self.guesshistory.append(guess)
        output += '\n'
        self.resulthistory.append(output)
        output = ''.join(self.resulthistory)
        # tries remaining
        output.join(self.correctletters)

        return output

    async def render(self) -> str:
        output = ''
        # for self.tries:
        
        return output

    def __init__(self):
        self.reset()
        self.wins = 0
        return None




# TODO: eventually make this modal
class main():
    games = {str: Game} # phone number : gamestate
    phone_number = "+19595551312"
    testnum = "+19595551312"
    altnum = "+5555555555"

    running = True

    while running:
        user_input = input("> ")

        if user_input == "changenum":
            if phone_number == testnum:
                phone_number = altnum
                print("newnum:" + phone_number)
                continue
            else: 
                phone_number = testnum
                print("newnum:" + phone_number)
                continue

        if phone_number not in games:
            # games += { phone_number: blankgame }
            games[phone_number] = Game()
        
        game = games.get(phone_number)
        
        if game.word == '':
            games[phone_number].word = random.choice(tuple(wordlist))

        if user_input == "retry":
            games[phone_number].reset()
            print("restrting")
            continue
        if user_input == "answer":
            print(games[phone_number].word)
            continue
        if user_input == "exit":
            print("exiting")
            break

        print(games[phone_number].guess(user_input))
    
    print("exited")


if __name__ == "__main__":
    sys.exit(main())
