#    Cats Out of the Bag, a fun game about herding cats or solving problems, whichever resonates with you more.
#    This is the main code file for the game. It contains the loop that runs every frame
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
import random
import os

import cat_module
import player_module
import lasso_module

#---------------------Global Variables and Game Window Setup-----------------------------#


# This sets up the game window.
screenWidth = 500
screenHeight = 480

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Cats Out of the Bag")

score = 0

#---------------------Functions---------------------------#

def redrawGameWindow():
    window.blit(backgroundImage, (0, 0))

    player.draw(window)

    for cat in cats:

        if player.caughtCat(cat):
            cat.hit()
            cat.isCaught = True

        if cat.isCaught:
            if cat.isTouchingPlayer(player):
                cats.remove(cat)
            else:
                cat.pullTowardPlayer(player)

        cat.draw(window)
        cat.move(cat.endX, cat.endY)

    pygame.display.update()


#---------------------Instantiate Game Objects, Background Images, and Game Clock-------------------------#
player = player_module.Player(0, 0)

cats = []
for i in range(10):
    cats.append(cat_module.Cat(screenWidth // 2, screenHeight // 2, random.randint(0, screenWidth), random.randint(0, screenHeight)))

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

    if keys[pygame.K_SPACE] and not player.lassoIsThrown:
        player.throwLasso(window)

    if keys[pygame.K_a] and player.x - player.velocity >= 0:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.up = False
        player.down = False

    elif keys[pygame.K_d] and player.x + player.width < screenWidth:
        player.x += player.velocity
        player.left = False
        player.right = True
        player.up = False
        player.down = False

    elif keys[pygame.K_s] and player.y + player.height < screenHeight:
        player.y += player.velocity
        player.left = False
        player.right = False
        player.up = False 
        player.down = True

    elif keys[pygame.K_w] and player.y - player.velocity >= 0:
        player.y -= player.velocity
        player.left = False
        player.right = False
        player.up = True
        player.down = False

    else:
        player.walkCyclePosition = 0

    redrawGameWindow()

pygame.quit()
