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

        self.lasso = Lasso(x, y)


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
<<<<<<< HEAD
        
=======
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        
            
>>>>>>> d2ea21a (Delete artifacts from merge conflict)

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

        
    

#---------------------Functions---------------------------#

def catIsTouchingPlayer(player, cat):
    return player.y <= cat.y + cat.height and player.y + player.height >= cat.y and player.x + player.width >= cat.x and player.x <= cat.x + cat.width

def playerCaughtCat(player, cat) -> bool:
    if not player.lassoIsThrown:
        return False
    else:
        return player.lasso.y < cat.y + cat.height and player.lasso.y + player.lasso.spriteHeight > cat.y and player.lasso.x + player.lasso.spriteWidth > cat.x and player.lasso.x < cat.x + cat.width


def redrawGameWindow():
    window.blit(backgroundImage, (0, 0))

    player.draw(window)

    for cat in cats:

        if playerCaughtCat(player, cat):
            cat.hit()
            cat.isCaught = True

        if cat.isCaught:
            if catIsTouchingPlayer(player, cat):
                cats.remove(cat)
            else:
                cat.pullTowardPlayer(player)

        cat.draw(window)
        cat.move(cat.endX, cat.endY)

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
