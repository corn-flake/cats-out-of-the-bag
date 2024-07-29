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

spritePath = os.path.join('..', 'sprites')

class Cat:
    def __init__(self, x, y, endX, endY):
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.endX = endX
        self.endY = endY

        self.height = 64
        self.width = 64


        self.hitbox = (x, y, self.width, self.height)

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.walkUpSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "up_arrow.png"))]
        self.walkDownSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "down_arrow.png"))]
        self.walkRightSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "right_arrow.png"))]
        self.walkLeftSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "left_arrow.png"))]

        self.velocity = 5

        self.walkCyclePosition = 0

        self.isAtEnd = False

        self.isCaught = False

    def draw(self, window):
            
        if self.walkCyclePosition + 1 <= 3:
            self.walkCyclePosition = 0

        if self.down:
            window.blit(self.walkDownSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        elif self.right:
            window.blit(self.walkRightSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        elif self.up:
            window.blit(self.walkUpSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1
        # Cat must be moving left
        else:
            window.blit(self.walkLeftSprites[self.walkCyclePosition // 3], (self.x, self.y))
            self.walkCyclePosition += 1

        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        

    def move(self, endX, endY):
        if self.isAtEnd:
           # The cat is at the end of it's path.
           # It needs to go back to the start, so we can swap the starts and ends
            temp = self.startX
            self.startX = self.endX
            self.endX = temp

            temp = self.startY
            self.startY = self.endY
            self.endY = temp
            self.isAtEnd = False
        else:
            if self.x - self.velocity >= endX:
                self.x -= self.velocity
                self.left = True
                self.right = False
                self.up = False
                self.down = False
                self.isAtEnd = False

            elif self.x + self.width < endX:
                self.x += self.velocity
                self.left = False
                self.right = True
                self.up = False
                self.down = False
                self.isAtEnd = False

            elif self.y + self.height < endY: 
                self.y += self.velocity
                self.left = False
                self.right = False
                self.up = False 
                self.down = True
                self.isAtEnd = False

            elif self.y - self.velocity >= endY:
                self.y -= self.velocity
                self.left = False
                self.right = False
                self.up = True
                self.down = False
                self.isAtEnd = False

            else:
                self.walkCyclePosition = 0
                self.isAtEnd = True

    def hit(self):
        print("caught")

    def pullTowardPlayer(self, player):
        self.endX = player.x
        self.endY = player.y
        self.velocity = player.velocity + 3
        

    def isTouchingPlayer(self, player):
        return player.y <= self.y + self.height and player.y + player.height >= self.y and player.x + player.width >= self.x and player.x <= self.x + self.width

