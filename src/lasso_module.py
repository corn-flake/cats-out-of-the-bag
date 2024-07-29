#    Cats Out of the Bag, a fun game about herding cats or solving problems, whichever resonates with you more.
#    This file contains the code for the lasso the player throws
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

class Lasso:

    def __init__(self, x, y):
        self.x = 0
        self.y = 0

        self.upSprites = [pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_up1.png")),
                          pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_up2.png")),
                          pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_up3.png")),
                          pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_up4.png")),
                          pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_up5.png"))]

        self.downSprites = [pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_down1.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_down2.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_down3.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_down4.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_down5.png"))]

        self.leftSprites = [pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_left1.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_left2.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_left3.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_left4.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_left5.png"))]

        self.rightSprites = [pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_right1.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_right2.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_right3.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_right4.png")),
                            pygame.image.load(os.path.join(spritePath, "lasso_sprites", "lasso_right5.png"))]


        self.counter = 0
        self.counterMax = 20
        self.spriteWidth = 64
        self.spriteHeight = 64

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        
    def draw(self, window):
        # I want to use the counter to index into the sprite lists, but it's counting down and I want it to count up
        # This lookup table uses the counter as an index and stores the value I want from 20 -> 0, 19 -> 1, 18 -> 2, etc.
        # It changes the counter which is counting down to counting up
        numberSwapLookupTable = [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

        # Then we can integer divide by 4 so that we get 4 of the same number in the correct order like this:
        # 0 -> 0
        # 1 -> 0
        # 2 -> 0
        # 3 -> 0
        # 4 -> 1
        # 5 -> 1
        # ...
        # The final number is correct index into the sprite lists
        currentImageIndex = numberSwapLookupTable[self.counter - 1] // 4

        if self.up:
            window.blit(self.upSprites[currentImageIndex], (self.x, self.y))
            self.spriteWidth = 64
            self.spriteHeight = (currentImageIndex + 1) * 21
        elif self.down:
            window.blit(self.downSprites[currentImageIndex], (self.x, self.y))
            self.spriteWidth = 64
            self.spriteHeight = (currentImageIndex + 1) * 21
        elif self.left:
            self.spriteWidth = (currentImageIndex + 1) * 21
            self.spriteHeight = 64
            window.blit(self.leftSprites[currentImageIndex], (self.x, self.y))
        else:
            window.blit(self.rightSprites[currentImageIndex], (self.x, self.y))
            self.spriteWidth = (currentImageIndex + 1) * 21
            self.spriteHeight = 64

        
    
