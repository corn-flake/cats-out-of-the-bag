#    Cats Out of the Bag, a fun game about herding cats or solving problems, whichever resonates with you more.
#    This file contains the code for the cats
#    Copyright (C) 2024  Evan Cooney
#    Contact me at evancooney71@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>
#    or write to the Free Software Foundation,
#    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import pygame
import os

import movable_class

spritePath = os.path.join('..', 'sprites')


class Cat(movable_class.Movable):
    def __init__(self, x, y, endX, endY):
        super().__init__(x, y, 64, 64, 5, [[os.path.join(spritePath, "cat_sprites", "left_arrow.png")],
                                           [os.path.join(spritePath, "cat_sprites", "right_arrow.png")],
                                           [os.path.join(spritePath, "cat_sprites", "up_arrow.png")],
                                           [os.path.join(spritePath, "cat_sprites", "down_arrow.png")]])

        self.start_x = x
        self.start_y = y
        self.end_x = endX
        self.end_y = endY

        self.isCaught = False

    def draw(self, window):
        super().draw(window)

    def advance_on_path(self) -> None:
        x_range_to_stop_in = range(self.end_x - self.speed, self.end_x + self.speed + 1)
        y_range_to_stop_in = range(self.end_y - self.speed, self.end_y + self.speed + 1)

        # This checks to see whether the cat is at the end / is about to pass it with the next move
        # It returns because the function just needs to switch the variables if the cat is at the end, nothing else
        if self.x in x_range_to_stop_in and self.y in y_range_to_stop_in:
            temp = self.start_x
            self.start_x = self.end_x
            self.end_x = temp

            temp = self.start_y
            self.start_y = self.end_y
            self.end_y = temp
            return

        elif self.x in x_range_to_stop_in:
            if self.y > y_range_to_stop_in[len(y_range_to_stop_in) - 1]:
                self.face("up")
            else:
                self.face("down")

        elif self.y in y_range_to_stop_in:
            if self.x > x_range_to_stop_in[len(x_range_to_stop_in) - 1]:
                self.face("left")
            else:
                self.face("right")

        else:
            if self.x > x_range_to_stop_in[len(x_range_to_stop_in) - 1]:
                self.face("left")
            else:
                self.face("right")

        self.move_forward()
        return

    def hit(self):
        print("caught")

    def pull_toward_player(self, player):
        self.endX = player.x
        self.endY = player.y
        self.speed = player.speed + 3

    def is_touching_player(self, player):
        return (player.y <= self.y + self.height and
                player.y + player.height >= self.y and
                player.x + player.width >= self.x and
                player.x <= self.x + self.width)
