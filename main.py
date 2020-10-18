from random import shuffle
from typing import List

import pygame

import pygame_textinput
from data_structures import Rolling_hash


def main():
    # init all packages
    pygame.init()

    # screen
    screen_x = 930
    screen_y = 700
    screen = pygame.display.set_mode((screen_x, screen_y))

    clock = pygame.time.Clock()

    # Title and game icon
    pygame.display.set_caption("Pygame Typing Challenge")
    icon = pygame.image.load("images/profanity.png")
    pygame.display.set_icon(icon)

    # Create TextInput-object
    textinput = pygame_textinput.TextInput()
    text_input_x = 7
    text_input_y = screen_y - 77

    # font
    font = pygame.font.Font("FE.ttf", 32)
    heading_font = pygame.font.Font("CQ.ttf", 40)
    end_font = pygame.font.Font("Mallvirra.ttf", 75)
    win_font = pygame.font.Font("Mallvirra.ttf", 50)

    # number of words to be displayed, score and timer

    number_of_words = 20
    score = 0
    total_time = 60 * 1000  # in milliseconds
    rem_time = total_time

    score_x, score_y = 10, 20
    time_x, time_y = screen_x - 167, 20

    valid_characters = set()
    # add all alphanumeric to valid_characters
    for i in range(26):
        ch = chr(ord("a") + i)
        caps = ch.upper()

        valid_characters.add(ch)
        valid_characters.add(caps)

    for num in range(10):
        valid_characters.add(num)

    # load the word_corpus and get the word_list
    with open("words_corpus.txt", "r") as f:
        raw_word_list = f.readlines()

    raw_word_list = list(map(lambda x: x.strip(), raw_word_list))
    raw_word_list = list(filter(lambda x: x.isalnum(), raw_word_list))
    shuffle(raw_word_list)

    word_list = raw_word_list[:number_of_words]

    word_clear = [False for _ in range(len(word_list))]
    word_grid = []

    for x in [15, 250, 500, 750]:
        for y in range(100, text_input_y - 50, 100):
            word_grid.append((x, y))

    def draw_headers():
        score_text = heading_font.render(
            "Score: " + str(score), True, (0, 0, 0)
        )
        time_text = heading_font.render(
            "Timer: " + str(rem_time // 1000), True, (0, 0, 0)
        )

        screen.blit(score_text, (score_x, score_y))
        screen.blit(time_text, (time_x, time_y))

    def draw_words(word_list: List[str], word_clear: List[bool]):
        index = 0

        for word_index, word in enumerate(word_list):
            if word_clear[word_index]:
                continue

            word_pos = word_grid[index]

            word_text = font.render(str(word), True, (0, 0, 0))
            screen.blit(word_text, word_pos)

            index += 1

    # Hash object
    hash_object = Rolling_hash(word_list)

    running = True
    time_over = False
    win = False

    # Game loop
    while running:
        if win:
            screen.fill((175, 141, 19))

            win_text_first_line = win_font.render(
                "None are so empty as those",
                True,
                (0, 0, 0),
            )
            screen.blit(win_text_first_line, (200, screen_y // 2 - 100))

            win_text_second_line = win_font.render(
                "who are full of themselves",
                True,
                (0, 0, 0),
            )
            screen.blit(win_text_second_line, (200, screen_y // 2 - 50))

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
            clock.tick(30)

            continue

        if time_over:
            screen.fill((227, 30, 30))

            end_text = end_font.render("SORRY TIME OVER!!", True, (0, 0, 0))
            screen.blit(end_text, (50, screen_y // 2 - 100))

            score_text = heading_font.render(
                "Score is: " + str(score), True, (10, 40, 200)
            )
            screen.blit(score_text, (325, screen_y // 2 + 100))

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
            clock.tick(30)

            continue

        is_backspace = False
        is_left = False
        is_right = False
        is_alphanum = False
        invalid_move = False

        screen.fill((198, 199, 199))

        rem_time = total_time - pygame.time.get_ticks()

        if rem_time <= 0:
            time_over = True

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    is_backspace = True

                elif event.key == pygame.K_LEFT:
                    is_left = True

                elif event.key == pygame.K_RIGHT:
                    is_right = True

                else:
                    try:
                        ch = event.unicode
                        if ch in valid_characters:
                            is_alphanum = True
                        else:
                            invalid_move = True
                    except Exception:
                        invalid_move = True

        ret_index = -1

        if is_backspace:
            ret_index = hash_object.add_backspace()

        elif is_left:
            hash_object.add_left_movement()

        elif is_right:
            hash_object.add_right_movement()

        elif is_alphanum:
            ret_index = hash_object.add_character(ch)

        # Feed it with events every frame
        if not invalid_move:
            textinput.update(events)

        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (text_input_x, text_input_y))

        # Check if the current string matches any in the list
        if ret_index != -1:
            word_clear[ret_index] = True
            textinput.clear_text()
            score += 1

        win = (score == len(word_list))

        draw_headers()
        draw_words(word_list, word_clear)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
