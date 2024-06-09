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

#---------------------Global Variables and Game Window Setup-----------------------------#
spritePath = os.path.join('..', 'sprites')

# This sets up the game window.
screenWidth = 500
screenHeight = 480

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Cats Out of the Bag")

score = 0

#---------------------Game Object Classes----------------------------#
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, self.width, self.height)
    
        # These are the player's dimensions in pixels.
        self.width = 64
        self.height = 64

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

    lassoUpSprite = pygame.image.load(os.path.join(spritePath, "player_sprites", "lasso_up.png"))
    lassoDownSprite = pygame.image.load(os.path.join(spritePath, "player_sprites", "lasso_down.png"))
    lassoLeftSprite = pygame.image.load(os.path.join(spritePath, "player_sprites", "lasso_left.png"))
    lassoRightSprite = pygame.image.load(os.path.join(spritePath, "player_sprites", "lasso_right.png"))

    lassoCounter = 0
    lassoCounterMax = 20
    lassoSpriteWidth = 64
    lassoSpriteHeight = 64
    lassoIsThrown = False

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
            if self.left:
                window.blit(self.lassoLeftSprite, (self.x - self.lassoSpriteWidth, self.y))
            elif self.right:
                window.blit(self.lassoRightSprite, (self.x + self.width, self.y))
            elif self.up:
                window.blit(self.lassoUpSprite, (self.x, self.y - self.lassoSpriteHeight))
            else:
                window.blit(self.lassoDownSprite, (self.x, self.y + self.height))

            if self.lassoCounter > 1:
                self.lassoCounter -= 1
            else:
                self.lassoCounter = 0
                self.lassoIsThrown = False

    def throwLasso(self, window):
        self.lassoCounter = self.lassoCounterMax
        self.lassoIsThrown = True
        


class Cat:
    def __init__(self, x, y, endX, endY):
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.endX = endX
        self.endY = endY
        self.hitbox = (self.x, self.y, self.width, self.height)

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
    

    def draw(self, window):
        if self.isAtEnd:
            if self.move(self.startX, self.startY):
                self.isAtEnd = False
        else:
            self.isAtEnd = self.move(self.endX, self.endY)
            
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
<<<<<<< HEAD

        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
=======
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        
>>>>>>> dfcc7942affd64bf6b63894a776d5f5e316f112e
            

    def move(self, endX, endY):
        if self.x - self.velocity >= endX:
            self.x -= self.velocity
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            return False

        elif self.x + self.width < endX:
            self.x += self.velocity
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            return False

        elif self.y + self.height < endY: 
            self.y += self.velocity
            self.left = False
            self.right = False
            self.up = False 
            self.down = True
            return False

        elif self.y - self.velocity >= endY:
            self.y -= self.velocity
            self.left = False
            self.right = False
            self.up = True
            self.down = False
            return False
        else:
            self.walkCyclePosition = 0
            return True

    def hit(self):
        print("hit")
        pass


    def hit(self):
        print("hit")
        pass


#---------------------Functions---------------------------#

def areColliding(player, cat) -> bool:
    return player.y < cat.y + cat.height and player.y + player.height > cat.y and player.x + player.width > cat.x and player.x < cat.x + cat.width


def redrawGameWindow():
    window.blit(backgroundImage, (0, 0))

    player.draw(window)
<<<<<<< HEAD
    for cat in cats:

        if areColliding(player, cat):
            cat.hit()
            cats.remove(cat)

=======
    for i, cat in enumerate(cats):

        if abs(player.x - cat.x) < 64 and abs(player.y - cat.y) < 64:
            print(f"Cat {i}")
            cat.hit()
        
>>>>>>> dfcc7942affd64bf6b63894a776d5f5e316f112e
        cat.draw(window)

    pygame.display.update()




#---------------------Instantiate Game Objects, Background Images, and Game Clock-------------------------#
player = Player(0, 0)

cats = []
for i in range(10):
    cats.append(Cat(screenWidth // 2, screenHeight // 2, random.randint(0, screenWidth), random.randint(0, screenHeight)))

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
