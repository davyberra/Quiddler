# Quiddler Card Game

## Description

A card game for two players based on the popular game Quiddler. Players take turns drawing and discarding cards, trying
to make words from the letters in their hands. Each letter is worth a certain amount of points, and the hand size
increases by one each round. Whoever has the most points at the end of the game wins!

This was created using the Arcade module for Python, with the art/music created by myself.
I do not claim to own any rights to this game.

## Gameplay Demo
![Gameplay Video](/doc/quiddler_demo.gif)
## How to Install
Requires: Python, Arcade

Clone/Download the source code to your computer, then install Arcade with the following command:
```bash
pip install arcade
```
In the "/src" directory, run "main.py" to play the game.
```bash
python two_player.py
```

## How to Play
(Instructions can also be found in-game through the main/pause menus)

### Overview
Quiddler is a game for two players where each player takes turns trying to make words out of the cards in their hands.
Each round a player is dealt between 3-10 cards (depending on the round) and must use all the cards in their hand to go down.
Once one player goes down, the other player has one more turn to make words using as many cards as they can before the scores
for the round are tallied and the round ends. The goal is to have the most points at the end of the game.

### Gameplay
On the first round, each player is dealt three cards. Each round, the number of cards increases by one, up to a total of 10
cards on round 8. For a half-game, the game ends after round 8, but a full game counts back down from 10 cards to 3 for a total
of 16 rounds.

On a player's turn, they must draw once (either from the face-down pile or the discard pile) and discard once.
To go down, the player must try to make a word or multiple words using all of the cards in their hand 
(not including the card to be discarded - the player must always have a discard.)
Players can make words in multiple ways, with only a couple of caveats:
<li>Words must be <strong>at least 2-letters</strong> long</li>
<li>Words must use <strong>at least 2 cards</strong> (some cards have two letters instead of just one and can't be used on their own to make a word)</li>
<li>You can use your cards to make <strong>as many words as you like</strong>, as long as each word fits the above criteria</li>
<br>
Once a player is able to successfully go down, play moves on to the other player, who has one full turn to make whatever
words they can before the round ends. In this case, the player doesn't have to use all their cards - they can go down with
whatever they have, and any leftover cards will count against them when tallying the score for the round.

Once the scores have been added up, the next round begins, with Player Two going first this time. The person to play first
alternates each round in this manner.

### Scoring
Each card has a point value assigned to it, and are worth that value towards your point total when scoring for the round.
Conversely, if there are any cards left unused at the end of the round, those cards count <strong>against</strong> your
total points for their assigned value.

Additionally, there is a <strong>bonus</strong> at the end of each round for the longest word played worth an additional 
<strong>10 points</strong>. These points can add up fast, so players are encouraged to come up with as long of words as possible!

### Game End
After the last round (round 8 in a half-game, round 16 in a full-game) the player with the highest total score wins!
If their score makes it into the top 10 high scores (saved locally on their computer) it will be added to the leaderboard 
of high scores that can be accessed from the Main Menu.

## Controls
<li>Left-click on the face-down/discard piles to draw</li>
<li>Left-click on a card in your hand to place it into the center pile when creating a word</li>
<li>Alternatively, use your keyboard to type the letters when placing cards into the center pile</li>
<li>Click "Save Word" to add the word in the center pile into your go-down pile 
(If the word isn't valid, the game will return the cards to your hand)
</li>
<li>Once you've created words using all of the cards in your hand, click "Go Down" to play your words and
go down for the round</li>
<li>Right-click on a card in your hand to discard</li>
<li>Click "Next Turn" to pass play onto the next player</li>
<li>Click "Recall" to return all saved words back into your hand</li>
<li>Click "Undo" to undo a draw/discard move (Only works if you haven't made any moves since the draw/discard)</li>
<br>
Hope you enjoy, and let me know of any issues you may encounter!