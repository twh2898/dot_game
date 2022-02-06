#!/usr/bin/env python3

import pyglet
from random import random

radius = 5
dot_color = (255, 0, 0)
guess_color = (0, 255, 0)
shuffle_dots = True
show_s = 1
score_curve = 6  # Exponent which is >= 0

HELP_TEXT_1 = 'Click to place each point'
HELP_TEXT_2 = 'Click to start again'


class App(pyglet.window.Window):
    def __init__(self, width, height, n_dots):
        assert n_dots > 0

        super().__init__(width, height, caption='Dot Game')
        self.n_dots = n_dots

        self._label = pyglet.text.Label(f'{n_dots} dots', x=10, y=10)
        self._score = pyglet.text.Label('', x=10, y=30)
        self._help_text = pyglet.text.Label(
            HELP_TEXT_1, x=10, y=self.height-30)

        self.half_width = self.width // 2
        self.half_height = self.height // 2

        self.show_dots = True

        self._dots = []
        self._dots_labels = []
        self._guess = []
        self._guess_labels = []

        self._max_dist_sqr = 0
        self._gen_dots()
        self.reset()

    def _gen_dots(self):
        self._dots.clear()
        self._dots_labels.clear()
        self._max_dist_sqr = 0
        for i in range(self.n_dots):
            x, y = random() * self.width, random() * self.height
            d_x = max(x, self.width - x)
            d_y = max(y, self.height - y)
            self._max_dist_sqr += d_x ** 2 + d_y ** 2
            dot = pyglet.shapes.Circle(
                x, y, radius, color=dot_color)
            self._dots.append(dot)
            l = pyglet.text.Label(str(i), x=x + 10, y=y, anchor_y='center')
            self._dots_labels.append(l)

    def hide(self, dt):
        self.show_dots = False

    def reset(self):
        self._guess.clear()
        self._guess_labels.clear()
        self._score.text = ''
        self._help_text.text = HELP_TEXT_1
        if shuffle_dots:
            self._gen_dots()
        self.show_dots = True
        pyglet.clock.schedule_once(self.hide, show_s)

    def on_mouse_press(self, x, y, button, mods):
        if len(self._guess) == self.n_dots:
            self.reset()
            return
        if self.show_dots:
            return
        dot = pyglet.shapes.Circle(x, y, radius,
                                   color=guess_color)
        self._guess.append(dot)
        l = pyglet.text.Label(str(len(self._guess_labels)),
                              x=x + 10, y=y, anchor_y='center')
        self._guess_labels.append(l)

        if len(self._guess) == self.n_dots:
            self.calc_score()
            self.show_dots = True
            self._help_text.text = HELP_TEXT_2

    def on_draw(self):
        self.clear()
        self._label.draw()
        self._score.draw()
        self._help_text.draw()
        if self.show_dots:
            for dot in self._dots:
                dot.draw()
            for label in self._dots_labels:
                label.draw()
        for guess in self._guess:
            guess.draw()
        for label in self._guess_labels:
            label.draw()

    def calc_score(self):
        dist_sqr = 0
        for dot, guess in zip(self._dots, self._guess):
            d_x = abs(dot.x - guess.x)
            d_y = abs(dot.y - guess.y)
            dist_sqr += d_x ** 2 + d_y ** 2
        score = 1 - dist_sqr / self._max_dist_sqr
        score = (100 * score ** score_curve)
        self._score.text = f'Score: {score}%'


app = App(800, 600, 3)

if __name__ == '__main__':
    pyglet.app.run()
