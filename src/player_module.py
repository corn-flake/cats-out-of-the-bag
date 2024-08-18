#    Cats Out of the Bag, a fun game about herding cats or solving problems, whichever resonates with you more.
#    This file contains the code for the player
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
import lasso_module

spritePath = os.path.join('..', 'sprites', 'player_sprites')


class Player(movable_class.Movable):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 64, 64, 5,
                         [[os.path.join(spritePath, "left_arrow.png")],
                          [os.path.join(spritePath, "right_arrow.png")],
                          [os.path.join(spritePath, "up_arrow.png")],
                          [os.path.join(spritePath, "down_arrow.png")]])

        self.lassoIsThrown = False
        self.lasso = lasso_module.Lasso(x, y)

    # This draws the player on the screen
    def draw(self, window):
        super().draw(window)

        if self.lassoIsThrown:
            self.lasso.counter -= 1

        if self.lasso.counter == 0:
            self.lassoIsThrown = False
        else:
            self.throwLasso(window)

    def throwLasso(self, window):
        if self.left:
            lassoX = self.x - self.lasso.spriteWidth
            lassoY = self.y
            self.lasso.x = lassoX
            self.lasso.y = lassoY
            self.lasso.left = True
            self.lasso.right = False
            self.lasso.up = False
            self.lasso.down = False
        elif self.right:
            lassoX = self.x + self.width
            lassoY = self.y
            self.lasso.x = lassoX
            self.lasso.y = lassoY
            self.lasso.right = True
            self.lasso.left = False
            self.lasso.up = False
            self.lasso.down = False
        elif self.up:
            lassoX = self.x
            lassoY = self.y - self.lasso.spriteHeight
            self.lasso.x = lassoX
            self.lasso.y = lassoY
            self.lasso.up = True
            self.lasso.down = False
            self.lasso.right = False
            self.lasso.left = False
        else:
            lassoX = self.x
            lassoY = self.y + self.height
            self.lasso.x = lassoX
            self.lasso.y = lassoY
            self.lasso.down = True
            self.lasso.up = False
            self.lasso.right = False
            self.lasso.left = False

        self.lasso.draw(window)

        if not self.lassoIsThrown:
            self.lassoIsThrown = True
            self.lasso.counter = self.lasso.counterMax

    def caught_cat(self, cat) -> bool:
        if not self.lassoIsThrown:
            return False
        else:
            return self.lasso.y < cat.y + cat.height and self.lasso.y + self.lasso.spriteHeight > self.y and self.lasso.x + self.lasso.spriteWidth > self.x and self.lasso.x < self.x + self.width
