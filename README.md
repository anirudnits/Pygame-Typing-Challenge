# Pygame-Typing-Challenge

A minimalistic and austere typing game in pygame wherein you have to type a given set of words before the timer expires.

![Screenshot](https://github.com/anirudnits/Pygame-Typing-Challenge/blob/master/images/screenshot.PNG)

The part where I concentrated was to maintain a minimal time complexity for string matching per keystroke.

### Requirements:
- The input string should be matched with the set of words for each *valid* keystroke, not when the player hits enter.
- The algorithm should accomodate:
  - inserting an alphanumeric character
  - backspace, or deleting the immediate left character to the cursor
  - moving the cursor left
  - moving the cursor right
  
### Trie Approach

My initial approach was to use the Trie datastructure, building a prefix tree from the list of words and then use this tree to check if the current *player string* matches with any word on the list. With the conventional Trie approach it is possible to ascertain a **O(1)** time complexity for string matching per insertion operation and with a space augmented Trie, it is also possible to incorporate the backspace functionality, increasing the space complexity to **O(len(string))** but restricting the time complexity to **O(1)** https://github.com/anirudnits/Pygame-Typing-Challenge/blob/4b79ea29dfac1e086c64848bb94daea03657f0b9/data_structures.py#L25

### Rolling hash + Deque Approach

My second approach was to use hashing for checking if the *player string* matches with any word on the list and rolling hash was the obvious choice as I needed to process each character at a time. The *deques* are used to store characters relative to the current cursor positions, that is either to the right or left. This approach maintains a time complexity of **O(log(mod))** per *valid* keystroke, where mod is the modulo used in calculating the hash values of the strings. For this instance I used a modulo closer to ~10^10.
https://github.com/anirudnits/Pygame-Typing-Challenge/blob/4b79ea29dfac1e086c64848bb94daea03657f0b9/data_structures.py#L64

### Playing the game locally:
- requires python3.7, pygame doesn't support python3.8+ yet :(
- clone the repository
- cd to the cloned repository
- `python main.py`

### Work to be done:
- Add levels to the game.
- Add sounds.
- Stylize the winning and losing windows.

~ Thanks
