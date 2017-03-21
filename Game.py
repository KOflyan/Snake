"""Snake."""


import pygame
import time
import random

from pygame.locals import KEYDOWN, K_LEFT, K_UP, K_DOWN, K_RIGHT, K_b, K_g, K_l, K_r, K_q, K_e, K_n, K_s


class Apple:
    """Drawing an apple to the board."""

    def __init__(self, thick, width, height):
        """Class constructor."""
        # Setting random coordinates for apple to appear (with boundaries)
        self.randx = round(random.choice(range(thick, width - thick)))
        self.randy = round(random.choice(range(thick, height - thick)))

    def draw_apple(self, surf, s_color):
        """Drawing an apple."""
        interface = GameInterface()

        # Drawing an apple at the board
        # Changing apple color depending on user's background choice
        if s_color == interface.color_choose("drd"):
            pygame.draw.circle(surf, interface.color_choose("bl"), [self.randx, self.randy], 5)
        elif s_color == interface.color_choose("bl") or s_color == interface.color_choose("blue"):
            pygame.draw.circle(surf, interface.color_choose("wh"), [self.randx, self.randy], 5)
        else:
            pygame.draw.circle(surf, interface.color_choose("rd"), [self.randx, self.randy], 5)

    def check_if_eaten(self, x, y, cross_p_1, cross_p_2):
        """Yeah. All the checking."""
        #  hard to explain
        return x in range(self.randx - 10, self.randx + 10) and y in range(self.randy - 10, self.randy + 10) \
            or cross_p_2[0] in range(self.randx - 10, self.randx + 10) and cross_p_2[1] \
            in range(self.randy - 10, self.randy + 10) \
            or cross_p_1[0] in range(self.randx - 10, self.randx + 10) and cross_p_1[1] \
            in range(self.randy - 10, self.randy + 10)


class GameInterface:
    """Creating user interface to interact with."""

    def __init__(self):
        """Defining colors. RGB range."""
        self.colors = {"or": (255, 60, 0), "bl": (0, 0, 0), "wh": (255, 255, 255), "gr": (16, 104, 0),
                       "rd": (240, 0, 0,), "lgr": (37, 84, 42), "blue": (0, 0, 70), "drd": (148, 0, 44)}

    def color_choose(self, s_color):
        """Allow to fill a figure with a specific color."""
        return self.colors[s_color]

    @staticmethod
    def message(message, xy, surf, f_color):
        """Setting font size, quality and color for future messages."""
        font = pygame.font.SysFont(None, 35)

        screen_text = font.render(message, True, f_color)
        surf.blit(screen_text, xy)  # Adjusting font settings

    def start_menu(self, surf, s_color, f_color):
        """Creating start menu with user interface."""
        x = 50
        y = 130

        surf.fill(s_color)  # First filling, then putting text to use
        self.message("Select your difficulty: ", [x, y], surf, f_color)
        self.message("\'S\'     for slooooow", [x, y + 100], surf, f_color)
        self.message("\'E\'     for experienced", [x, y + 150], surf, f_color)
        self.message("\'N\'     for nightmare", [x, y + 200], surf, f_color)
        self.message("... or press Q to exit.", [x, y + 300], surf, f_color)
        pygame.display.update()

    def start_menu_colors(self, surf, s_color, f_color):
        """Setting user interface for choosing background colors."""
        x = 50
        y = 130
        surf.fill(s_color)
        self.message("Select your background color: ", [x, y], surf, f_color)
        self.message("G - for green", [x, y + 100], surf, f_color)
        self.message("B - for black", [x, y + 150], surf, f_color)
        self.message("L - for blue", [x, y + 200], surf, f_color)
        self.message("R - for red", [x, y + 250], surf, f_color)
        self.message("... or press Q to exit.", [x, y + 300], surf, f_color)
        pygame.display.update()

    def end_choice(self, surf, s_color, f_color, score):
        """End menu user interface."""
        x = 50
        y = 100
        game_st = Game()  # Creating game class object
        surf.fill(s_color)
        self.message("You lost!", [x, y], surf, f_color)
        self.message("Press Space to try again! Or Q to quit.", [x, y + 300], surf, f_color)
        self.end_score(surf, f_color, score, 50, 200)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:  # If the key is pressed
                if event.key == pygame.K_q:
                    surf.fill(s_color)
                    self.message("Bye", [x, y + 200], surf, f_color)
                    pygame.display.update()
                    time.sleep(0.2)
                    raise SystemExit
                elif event.key == pygame.K_SPACE:
                    game_st.game_loop()  # Starting over

    def excellent(self, surf, s_color, f_color, score):
        """For pros only."""
        game_st = Game()
        surf.fill(s_color)
        image = pygame.image.load("img.jpg")
        surf.blit(image, (25, 200))
        self.message("Wow! You\'re a pro!", [290, 150], surf, f_color)
        self.message("Space - continue", [590, 300], surf, f_color)
        self.message("Q - exit", [590, 350], surf, f_color)
        self.end_score(surf, f_color, score, 50, 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    self.exit(surf, s_color, f_color)
                elif event.key == pygame.K_SPACE:
                    game_st.game_loop()

    def exit(self, surf, s_color, f_color):
        """Display exit message (Bye)."""
        surf.fill(s_color)
        self.message("Bye", [50, 300], surf, f_color)
        pygame.display.update()
        time.sleep(0.2)
        raise SystemExit

    def score(self, surf, f_color, score):
        """Display score count onto the screen."""
        self.message("Your score: " + str(score), [25, 25], surf, f_color)

    def end_score(self, surf, f_color, score, x, y):
        """Get score message at the end."""
        scores = UserSettings()
        if scores.compare_scores(score) and score > 0:  # If the highest score is beaten - get your congratz
            self.message("You just beat the highest score!", [x, y], surf, f_color)
            self.message("Your max score: " + str(score), [x, y + 100], surf, f_color)
        else:
            self.message("Your max score: " + str(score), [x, y + 100], surf, f_color)  # If not - well, another time

    def lives_message(self, surf, f_color, lives):
        """Display lives left."""
        self.message("Lives left: " + str(lives), [25, 75], surf, f_color)


class UserSettings:
    """Saving user choices."""

    def __init__(self):
        """Class constructor. Inverting original dict of colors."""
        # was forced to invert original dict due to pygame module behaviour
        # (could not read from file colors in RGB format) ...
        interface = GameInterface()
        self.inv_colors = {}
        for k, v in interface.colors.items():
            self.inv_colors[v] = k

    @staticmethod
    def read_background():
        """Read data from file and appends it to list."""
        data = ""
        for i in open("back.txt"):
            data += i
        if len(data) >= 1:  # Appending data to list and checking if it is empty
            return data
        return None

    @staticmethod
    def write_to_file(data):
        """Write a data to file."""
        if str(data).isdigit():
            open("score.txt", "a").write(str(data) + '\n')  # 2 files for background choices and scores
        else:
            open("back.txt", "w").write(data)

    @staticmethod
    def read_scores():
        """Read scores from file."""
        data = []
        for i in open("score.txt"):
            data.append(int(i.rstrip('\n')))  # Appending scores to list in int-format
        return data

    def compare_scores(self, score):
        """Check if score is higher than previous ones."""
        if self.read_scores() is []:  # If list is empty, first score will be the highest one automatically
            return True
        else:
            return score == max(self.read_scores())  # Otherwise we'll need to check if it is


class Game:
    """Executing game and putting it all together."""

    def __init__(self):
        """Class constructor."""
        pygame.init()
        self.interface = GameInterface()
        self.background = UserSettings()

        self.clock = pygame.time.Clock()
        self.width = 800
        self.height = 600
        self.thick = 20
        self.surf = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.apple = Apple(self.thick, self.width, self.height)

        self.change_x = 0
        self.change_y = 0
        self.speed = 0

        self.s_color = self.interface.color_choose("lgr")
        self.f_color = self.interface.color_choose("or")

        self.start = True
        self.start2 = True
        self.over = False
        self.g_exit = False
        self.wrote = False

        self.snake_body = []
        self.score_list = []
        self.snake_len = 1

        self.lives = 3
        self.score = 0

        self.x = int(self.width / 2)
        self.y = int(self.height / 2)

        pygame.display.set_caption("Get early access now!")  # Left top

    def snake_segments(self, snake_body, thick, body_color):
        """Adding segments to the snake."""
        for xy in snake_body:  # adding segments
            pygame.draw.rect(self.surf, body_color, (xy[0], xy[1], thick, thick))

    def snake_draw(self, snake_body):
        """Draw a snake."""
        interface = GameInterface()  # Change the snake color dependent on user background choice
        if self.s_color == interface.color_choose("drd"):
            self.snake_segments(snake_body, self.thick, interface.colors["bl"])  # draw a snake
        elif self.s_color == interface.color_choose("bl") or self.s_color == interface.color_choose("blue"):
            self.snake_segments(snake_body, self.thick, interface.colors["wh"])
        else:
            self.snake_segments(snake_body, self.thick, interface.colors["rd"])

    def snake_controls(self):
        """Setting snake movement controls."""
        interface = GameInterface()
        for event in pygame.event.get():
            # Adjusting controls
            if event.type == KEYDOWN:
                if event.key == K_UP and self.change_y != self.speed:
                    self.change_y = -self.speed
                    self.change_x = 0  # Only right, left, up or down straight
                elif event.key == K_DOWN and self.change_y != -self.speed:  # Snake cannot move backwards
                    self.change_y = self.speed
                    self.change_x = 0
                elif event.key == K_LEFT and self.change_x != self.speed:
                    self.change_x = -self.speed
                    self.change_y = 0
                elif event.key == K_RIGHT and self.change_x != -self.speed:
                    self.change_x = self.speed
                    self.change_y = 0
                elif event.key == K_q:
                    interface.exit(self.surf, self.s_color, self.f_color)

    def start_choice(self):
        """Background choice."""
        while self.start:
            # Color choice
            self.interface.start_menu_colors(self.surf, self.s_color, self.f_color)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_g:
                        self.s_color = self.interface.color_choose("lgr")
                        self.f_color = self.interface.color_choose("or")
                    elif event.key == K_b:
                        self.s_color = self.interface.color_choose("bl")
                        self.f_color = self.interface.color_choose("wh")
                    elif event.key == K_r:
                        self.s_color = self.interface.color_choose("drd")
                        self.f_color = self.interface.color_choose("bl")
                    elif event.key == K_l:
                        self.s_color = self.interface.color_choose("blue")
                        self.f_color = self.interface.color_choose("wh")
                    elif event.key == K_q:
                        self.interface.exit(self.surf, self.s_color, self.f_color)
                    else:
                        continue
                    # writing choices to the file
                    self.background.write_to_file(self.background.inv_colors[self.s_color] + '\t' +
                                                  self.background.inv_colors[self.f_color])
                    self.start = False

    def difficulty_choice(self):
        """Difficulty choice."""
        while self.start2:
            self.interface.start_menu(self.surf, self.s_color, self.f_color)  # displaying start choice and message
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        self.speed = 2
                    elif event.key == K_e:
                        self.speed = 4
                    elif event.key == K_n:
                        self.speed = 8
                    elif event.key == K_q:
                        self.interface.exit(self.surf, self.s_color, self.f_color)
                    else:
                        continue
                    self.start2 = False

    def game_over(self):
        """Displaying game over screen."""
        while self.over and self.lives == 0:
            # SimpleBattleship results and messages
            if not self.wrote and max(self.score_list) > 0:  # We need that to be executed only once
                self.background.write_to_file(str(max(self.score_list)))
                self.wrote = True
            if max(self.score_list) > 35:
                # Alt game over message
                self.interface.excellent(self.surf, self.s_color, self.f_color, max(self.score_list))  # Alternative
            else:
                self.interface.end_choice(self.surf, self.s_color, self.f_color, max(self.score_list))  # Regular

    def start_again(self):
        """Starting again."""
        self.snake_len = 1
        self.x = int(self.width / 2)
        self.y = int(self.height / 2)
        self.change_x = 0
        self.change_y = 0
        self.score_list.append(self.score)
        self.snake_body = []
        self.score = 0
        self.snake_draw(self.snake_body)
        self.over = True
        self.lives -= 1

    def apple_reset(self):
        """Re-drawing the apple."""
        while True:
            self.apple.randx = round(random.choice(range(self.thick, self.width - self.thick)))
            self.apple.randy = round(random.choice(range(self.thick, self.height - self.thick)))
            #  We don't want the apple to appear under stats text, do we?
            if self.apple.randx in range(0, 200) and self.apple.randy in range(0, 100):
                continue
            break

    def read_settings(self):
        """Reading user settings from file."""
        if UserSettings.read_background() is not None:  # If list is empty setting default colors
            c = UserSettings.read_background().split('\t')[0]  # Otherwise setting preferred by user
            self.s_color = self.interface.color_choose(c)
            f = self.background.read_background().split('\t')[1]
            self.f_color = self.interface.color_choose(f)

    def game_loop(self):
        """Putting all together."""
        self.read_settings()
        while not self.g_exit:

            self.start_choice()
            self.difficulty_choice()
            self.game_over()
            self.snake_controls()

            # setting borders around the screen, i.e. collision case
            if self.x < 0 or self.x >= self.width - self.thick or self.y < 0 or self.y >= self.height - self.thick:
                self.start_again()

            self.x += self.change_x  # incrementing speed to coordinates
            self.y += self.change_y

            cross_p_1 = [self.x, self.y + self.thick]  # Adding two more points
            cross_p_2 = [self.x + self.thick, self.y]
            snake_head = list([self.x, self.y])  # Point, at which current rectangle is located

            self.snake_body.append(snake_head)  # Appending point to snake list

            self.surf.fill(self.s_color)  # Re-filling background every time, so rectangle stays in desired size

            if len(self.snake_body) > self.snake_len:  # a limit, so snake doesn't grow by itself
                self.snake_body.remove(self.snake_body[0])

            for segment in self.snake_body[1:len(self.snake_body) - 1]:  # collision with snake itself
                if segment == snake_head:
                    self.start_again()
                    break

            # Changing snake color depending on user's background choice
            self.snake_draw(self.snake_body)
            self.surf.fill(self.s_color, [25, 25, 170, 25])
            self.surf.fill(self.s_color, [25, 75, 150, 25])  # score/lives left text should be at foreground
            self.interface.score(self.surf, self.f_color, self.score)  # adding score count to the screen
            self.interface.lives_message(self.surf, self.f_color, self.lives)

            self.apple.draw_apple(self.surf, self.s_color)
            pygame.display.update()  # Screen update

            # re-setting the apple coordinates if snake eats previous one, thus drawing new apple
            if self.apple.check_if_eaten(self.x, self.y, cross_p_1, cross_p_2):
                self.apple_reset()  # adjusting new limit, thus drawing 1 additional segment when snake eats an apple
                self.snake_len += 3
                self.score = int(self.snake_len / 3)

            self.clock.tick(90)  # frequency of screen update, i.e. main while-loop repeating speed

game = Game()
game.game_loop()