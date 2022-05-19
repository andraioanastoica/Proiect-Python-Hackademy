import pygame
import sys
import random

pygame.init()

words = list(open('five-letter-words/sgb-words.txt').read().split())

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
WHITE = "#ffffff"

#globals 

WIDTH = 1150
HEIGHT = 1600
CORRECT_WORD = random.choice(words)
SQUARE_LENGTH = 200
SPACING = 10
TOP_SPACE = 50

class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (self.bg_x, self.bg_y, SQUARE_LENGTH, SQUARE_LENGTH)
        self.text = text
        self.text_position = (self.bg_x + 80, self.bg_position[1] + 80)
        self.text_surface = pygame.font.Font(None, 50).render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)
        pass
    pass

class Wordle:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Wordle!')
        self.letters = [[]] * 6
        self.guesses = 0
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = ""
        self.key_pressed = ""
        self.current_letter_bg_x = TOP_SPACE
        pass

    def run(self):
        self.draw()
        while True:
            self.input()
            self.update()

    def input(self):
        if self.game_result != "":
            self.play_again()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_result != "":
                        self.reset() 
                    else:
                        if len(self.current_guess_string) == 5 and self.current_guess_string.lower() in words:
                            self.check_guess()
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.current_guess_string) > 0:
                        self.delete_letter()
                else:
                    self.key_pressed = event.unicode.upper()
                    if self.key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and self.key_pressed != "":
                        if len(self.current_guess_string) < 5:
                            self.create_new_letter()
            pass
        pass

    def update(self):
        pass

    def draw(self):
        self.window.fill(WHITE)
        
        for i in range(6):
            for j in range(5):
                pygame.draw.rect(self.window, GREY, pygame.Rect([TOP_SPACE + SQUARE_LENGTH*j + SPACING*j, TOP_SPACE + SQUARE_LENGTH*i + SPACING*i], [SQUARE_LENGTH, SQUARE_LENGTH]), 1)
                pass

        pygame.display.update()
        pass

    def reset(self):
        # resets all game variables to the initial values
        self.window.fill(WHITE)
        for i in range(6):
            for j in range(5):
                pygame.draw.rect(self.window, GREY, pygame.Rect([TOP_SPACE + SQUARE_LENGTH * j + SPACING * j, TOP_SPACE + SQUARE_LENGTH * i + SPACING * i], [SQUARE_LENGTH, SQUARE_LENGTH]), 1)
                pass
        CORRECT_WORD = random.choice(words)
        self.letters = [[]] * 6
        self.guesses = 0
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = ""
        pygame.display.update()
        pass

    def play_again(self):
        # displays the correct word and a play again message
        play_again_font = pygame.font.Font(None, 50)
        play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
        play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 1400))
        word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
        word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 1350))
        self.window.blit(word_was_text, word_was_rect)
        self.window.blit(play_again_text, play_again_rect)
        pygame.display.update()
        pass

    def check_guess(self):
        game_decided = False
        for i in range(5):
            # checks letter objects and modifies attributes according to the legend
            #   green = letter is present in the word and in the required position
            #   yellow = letter is present in the word but is in a different position
            #   grey = letter is not present in the word
            lowercase_letter = self.current_guess[i].text.lower()
            if lowercase_letter in CORRECT_WORD:
                if lowercase_letter == CORRECT_WORD[i]:
                    self.current_guess[i].bg_color = GREEN
                    self.current_guess[i].text_color = "white"
                    if not game_decided:
                        self.game_result = "W"
                else:
                    self.current_guess[i].bg_color = YELLOW
                    self.current_guess[i].text_color = "white"
                    self.game_result = ""
                    game_decided = True
            else:
                self.current_guess[i].bg_color = GREY
                self.current_guess[i].text_color = "white"
                self.game_result = ""
                game_decided = True
            # overrides the squares with colored ones
            pygame.draw.rect(self.window, self.current_guess[i].bg_color, pygame.Rect(self.current_guess[i].bg_rect))
            if self.current_guess[i].bg_color == "white":
                pygame.draw.rect(self.window, self.current_guess[i].bg_color, pygame.Rect(self.current_guess[i].bg_rect), 3)
            self.current_guess[i].text_surface = pygame.font.Font(None, 100).render(self.current_guess[i].text, True, self.current_guess[i].text_color)
            self.window.blit(self.current_guess[i].text_surface, self.current_guess[i].text_rect)
            pygame.display.update()
        
        self.guesses += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = TOP_SPACE

        if self.guesses == 6 and self.game_result == "":
            self.game_result = "L"
        pass

    def delete_letter(self):
        # deletes letter from list
        self.letters[self.guesses].pop()
        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()
        self.current_letter_bg_x -= (SQUARE_LENGTH + SPACING)
        # overrides filled square with an empty square
        pygame.draw.rect(self.window, WHITE, pygame.Rect([self.current_letter_bg_x, TOP_SPACE + self.guesses * SQUARE_LENGTH + self.guesses * SPACING], [SQUARE_LENGTH, SQUARE_LENGTH]))
        pygame.draw.rect(self.window, GREY, pygame.Rect([self.current_letter_bg_x, TOP_SPACE + self.guesses * SQUARE_LENGTH + self.guesses * SPACING], [SQUARE_LENGTH, SQUARE_LENGTH]), 1)
        pygame.display.update()
        pass

    def create_new_letter(self):
        # creates letter object and adds it to the list
        self.current_guess_string += self.key_pressed
        new_letter = Letter(self.key_pressed, (self.current_letter_bg_x, TOP_SPACE + self.guesses * SQUARE_LENGTH + self.guesses * SPACING))
        self.current_letter_bg_x += (SQUARE_LENGTH + SPACING)
        self.letters[self.guesses].append(new_letter)
        self.current_guess.append(new_letter)
        # draws letter
        pygame.draw.rect(self.window, new_letter.bg_color, pygame.Rect(new_letter.bg_rect))
        if new_letter.bg_color == "white":
            pygame.draw.rect(self.window, new_letter.bg_color, pygame.Rect(new_letter.bg_rect), 3)
            pygame.draw.rect(self.window, GREY, pygame.Rect(new_letter.bg_rect), 1)
        new_letter.text_surface = pygame.font.Font(None, 100).render(new_letter.text, True, new_letter.text_color)
        self.window.blit(new_letter.text_surface, new_letter.text_rect)
        pygame.display.update()
        pass
    pass


def main():
    wordle = Wordle()
    wordle.run()

main()