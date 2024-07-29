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

import lasso_module

spritePath = os.path.join('..', 'sprites')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
        # These are the player's dimensions in pixels.
        self.width = 64
        self.height = 64

        self.hitbox = (self.x, self.y, self.width, self.height)

        # This is how many pixels the player can move per frame.
        self.velocity = 5

        # These represent the direction the player is moving.
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.hitbox = (x, y, self.width, self.height)

        # This represents an index in the walking sprites lists * 3 (why * 3, I don't know).
        # You have to divide by 3 every time you access one of the sprite lists.
        self.walkCyclePosition = 0

        self.walkUpSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "up_arrow.png"))]

        self.walkDownSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "down_arrow.png"))]

        # This is a list of sprites in the player's right walking cycle.
        self.walkRightSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "right_arrow.png"))]

        # This is a list of sprites in the player's left walking cycle.
        self.walkLeftSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "left_arrow.png"))]

        self.lassoIsThrown = False

        self.lasso = lasso_module.Lasso(x, y)


    # This draws the player on the screen
    def draw(self, window):
        if self.walkCyclePosition + 1 >= 0:
            self.walkCyclePosition = 0

        if self.left:
            window.blit(self.walkLeftSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        elif self.right:
            window.blit(self.walkRightSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        elif self.up:
            window.blit(self.walkUpSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        else:
            window.blit(self.walkDownSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2);

        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

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

            
    def caughtCat(self, cat) -> bool:
        if not self.lassoIsThrown:
            return False
        else:
            return self.lasso.y < cat.y + cat.height and self.lasso.y + self.lasso.spriteHeight > self.y and self.lasso.x + self.lasso.spriteWidth > self.x and self.lasso.x < self.x + self.width
