

import pygame
import random


from pygame.locals import *


class GameInterface:
    """User interface."""

    def __init__(self):
        pass

    def message(self, surf, s_color, f_color):
        pass

    def score(self, surf, s_color, f_color):
        pass

    def lives_left(self, surf, s_color, f_color):
        pass

    def difficulty_choice(self, surf, s_color, f_color):
        pass

    def over(self, surf, s_color, f_color):
        pass


class Ball:
    """Drawing a ball."""

    def __init__(self):
        """Defining radius."""
        self.rad = 8

    def draw_a_ball(self, surf, xy, s_color):
        """Drawing the ball."""
        pygame.draw.circle(surf, s_color, xy, self.rad)


class Bricks:
    """Composing bricks."""

    def __init__(self):
        """Defining coordinates."""
        self.coordinates = []

    def brick_coordinates(self, amount):
        """Computing brick coordinates."""
        x = 120
        y = 10
        step_x = 0
        step_y = 0

        for j in range(amount):
            if step_y >= 250:
                break
            for i in range(7):  # loop in loop: y, x
                self.coordinates.append(list([x + step_x, y + step_y]))
                step_x += 80
            step_y += 30
            step_x = 0
        return self.coordinates

    def draw_bricks(self, surf, s_color, length, thick):
        """Drawing bricks at the screen."""
        for i in self.coordinates:
            pygame.draw.rect(surf, s_color, (i[0], i[1], length, thick))


class Game:
    """Executing game."""

    def __init__(self):
        """Defining variables."""
        pygame.init()

        self.width = 800
        self.height = 600
        self.thick = 75
        self.surf = pygame.display.set_mode((self.width, self.height))

        self.colors = {"or": (217, 97, 44), "bl": (0, 0, 0), "wh": (255, 255, 255), "gr": (0, 149, 70),
                       "rd": (240, 0, 0), "lgr": (37, 84, 42), "blue": (0, 0, 70)}

        pygame.display.set_caption("Break a Brick")

        self.x_b = int(self.width / 2)
        self.y_b = self.height - 30
        self.x = int(self.width / 2 - self.thick / 2)
        self.y = self.height - 20

        self.ball = Ball()
        self.brick = Bricks()
        self.change_x_b = 0
        self.change_y_b = 0
        self.ball_speed = 3
        self.speed = 5
        self.s_color = "or"
        self.f_color = "wh"
        self.change_x = 0
        self.exit = False
        self.start = False
        self.clock = pygame.time.Clock()

        self.length = 70
        self.thick_2 = 10
        self.borders = 50

    def choose_color(self, s_color):
        """Choosing colors."""
        return self.colors[s_color]

    def draw_borders(self, s_color, width, height):
        """Drawing borders on the right and left."""
        pygame.draw.rect(self.surf, s_color, (0, 0, self.borders, height))
        pygame.draw.rect(self.surf, s_color, (width - self.borders, 0, self.borders, height))

    def game_controls(self):
        """Defining game controls."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self.exit = True

            elif event.type == KEYDOWN:  # depending on a key pressed subtract or add points to x or y
                if event.key == K_LEFT:
                    self.change_x = -self.speed

                elif event.key == K_RIGHT:
                    self.change_x = self.speed

                elif event.key == K_q:
                    raise SystemExit

                if not self.start:  # Initial state
                    if event.key == K_SPACE:
                        self.change_y_b = -self.ball_speed
                        self.change_x_b = random.choice(range(-self.ball_speed, self.ball_speed))
                        self.start = True

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    self.change_x = 0

    def platform_borders(self):
        """Defining platform borders."""
        if self.x <= self.borders:
            self.change_x = 0
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.change_x = self.speed

        elif self.x >= self.width - (self.borders + self.thick):
            self.change_x = 0
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.change_x = -self.speed
        else:
            self.game_controls()

    def ball_borders(self):
        """Defining ball borders."""
        if not self.start:
            self.x_b = self.x + int(self.thick / 2)
            self.y_b = self.y - self.ball.rad

        if self.x_b >= self.width - (self.borders + self.ball.rad):
            self.change_x_b = -self.ball_speed
        elif self.x_b <= self.borders + self.ball.rad:
            self.change_x_b = self.ball_speed
        elif self.y_b <= self.ball.rad:
            self.change_y_b = self.ball_speed

    def ball_movement(self):
        """Setting ball movement schematics."""
        if self.start:
            if self.x_b in range(self.x + 40, self.x + 60) and self.y_b in range(self.y - self.ball.rad, self.y):
                self.change_y_b = -self.ball_speed

            elif self.x_b in range(self.x, self.x + 40) and self.y_b in range(self.y - self.ball.rad, self.y):
                self.change_y_b = -self.ball_speed
                self.change_x_b = -self.ball_speed

            elif self.x_b in range(self.x + 60, self.x + 100) and self.y_b in range(self.y - self.ball.rad, self.y):
                self.change_y_b = -self.ball_speed
                self.change_x_b = self.ball_speed

            elif self.y_b >= self.height:
                self.x_b = self.x + int(self.thick / 2) + self.change_x
                self.y_b = self.y - self.ball.rad  # rad
                self.change_x_b = self.change_x
                self.change_y_b = 0
                self.start = False

    def brick_remove(self):
        """Removing the brick from the screen in case of collision."""
        for i in self.brick.coordinates:
            rect = pygame.Rect(i[0], i[1], self.length, self.thick_2)
            if rect.collidepoint(self.x_b + self.ball.rad, self.y_b) or \
                    rect.collidepoint(self.x_b - self.ball.rad, self.y_b) or \
                    rect.collidepoint(self.x_b, self.y_b + self.ball.rad) or \
                    rect.collidepoint(self.x_b, self.y_b - self.ball.rad) or \
                    rect.collidepoint(self.x_b + self.ball.rad, self.y_b + self.ball.rad) or \
                    rect.collidepoint(self.x_b - self.ball.rad, self.y_b - self.ball.rad):

                self.brick.coordinates.remove(i)
                if self.change_y_b == self.ball_speed:
                    self.change_y_b = -self.ball_speed
                else:
                    self.change_y_b = self.ball_speed

    def game_run(self):
        """Main game loop."""
        amount = 10
        self.brick.brick_coordinates(amount)

        while not self.exit:
            self.ball.rad = 9  # Нужна корректировка для больших радиусов (50)
            self.platform_borders()
            self.ball_borders()
            self.ball_movement()

            self.x += self.change_x  # platform move

            self.x_b += self.change_x_b  # ball move
            self.y_b += self.change_y_b

            self.surf.fill(self.colors["bl"])  # re-filling the background, so rectangle stays as one piece
            self.ball.draw_a_ball(self.surf, [self.x_b, self.y_b], self.choose_color(self.s_color))

            pygame.draw.rect(self.surf, self.choose_color(self.s_color), (self.x, self.y, self.thick, 10))  # x, y, width, height

            self.draw_borders(self.choose_color(self.s_color), self.width, self.height)  # Border pillars at the corners

            self.brick.draw_bricks(self.surf, self.choose_color(self.s_color), self.length, self.thick_2)  # Bricks

            self.brick_remove()

            pygame.display.update()

            self.clock.tick(100)  # frames per second

game = Game()
game.game_run()
