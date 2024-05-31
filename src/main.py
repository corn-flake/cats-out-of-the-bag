#    Cats Out of the Bag, a fun game about herding cats or solving problems, whichever resonates with you more.
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


#---------------------Import Libraries----------------------------#
import pygame
import os
import random
import time

#---------------------Game Window Setup-----------------------------#
spritePath = os.path.join('..', 'sprites')

# This sets up the game window.
screenWidth = 500
screenHeight = 480

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Cats Out of the Bag")

#---------------------Game Object Classes----------------------------#
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # These are the player's dimensions in pixels.
    width = 64
    height = 64

    # This is how many pixels the player can move per frame.
    velocity = 5

    # These represent the direction the player is moving.
    left = False
    right = False
    up = False
    down = False

    standing = True
    # This represents an index in the walking sprites lists * 3 (why * 3, I don't know).
    # You have to divide by 3 every time you access one of the sprite lists.
    walkCyclePosition = 0

    walkUpSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "up_arrow.png"))]

    walkDownSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "down_arrow.png"))]

    # This is a list of sprites in the player's right walking cycle.
    walkRightSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "right_arrow.png"))]

    # This is a list of sprites in the player's left walking cycle.
    walkLeftSprites = [pygame.image.load(os.path.join(spritePath, "player_sprites", "left_arrow.png"))]

    # This draws the player on the screen
    def draw(self, window):
        if self.walkCyclePosition + 1 >= 0:
            self.walkCyclePosition = 0

        if not (self.standing):
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
        else:
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

class Cat:
    standing = False

    up = False
    down = False
    left = False
    right = False

    height = 64
    width = 64

    walkUpSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "up_arrow.png"))]
    walkDownSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "down_arrow.png"))]
    walkRightSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "right_arrow.png"))]
    walkLeftSprites = [pygame.image.load(os.path.join(spritePath, "cat_sprites", "left_arrow.png"))]

    velocity = 10

    walkCyclePosition = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def draw(self, window):
        if self.walkCyclePosition + 1 >= 0:
            self.walkCyclePosition = 0

        if not (self.standing):
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
        else:
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

    

#---------------------Functions---------------------------#
def redrawGameWindow():
    window.blit(backgroundImage, (0, 0))

    player.draw(window)

    for cat in cats:
        cat.draw(window)

    pygame.display.update()


#---------------------Instantiate Game Objects, Background Images, and Game Clock-------------------------#
player = Player(0, 0)

cats = []
for i in range(4):
    cats.append(Cat(0, 0))
    cats[i].x = random.randint(0, screenWidth - cats[i].width)
    cats[i].y = random.randint(0, screenHeight - cats[i].height)

# Load background image
backgroundImage = pygame.image.load(os.path.join('..', 'bg.jpg'))

clock = pygame.time.Clock()


#---------------------Main Loop------------------------#
run = True

# Main loop
while run:
    # Set frame rate to 27 fps
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # If W key is pressed and so on
    if keys[pygame.K_SPACE]:
        if player.left:
            facing = -1
        else:
            facing = 1

    if keys[pygame.K_a] and player.x - player.velocity >= 0:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.up = False
        player.down = False
        player.standing = False

    elif keys[pygame.K_d] and player.x + player.width < screenWidth:
        player.x += player.velocity
        player.left = False
        player.right = True
        player.up = False
        player.down = False
        player.standing = False

    elif keys[pygame.K_s] and player.y + player.height < screenHeight:
        player.y += player.velocity
        player.left = False
        player.right = False
        player.up = False 
        player.down = True
        player.standing = False

    elif keys[pygame.K_w] and player.y - player.velocity >= 0:
        player.y -= player.velocity
        player.left = False
        player.right = False
        player.up = True
        player.down = False
        player.standing = False

    else:
        player.walkCyclePosition = 0
        player.standing = True

    redrawGameWindow()

pygame.quit()
