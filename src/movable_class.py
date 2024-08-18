import pygame

def sprite_path_lists_to_pygame_image_list(sprite_path_lists):
    return_lst = []
    for lst in sprite_path_lists:
        return_lst.append([pygame.image.load(sprite) for sprite in lst])

    return return_lst



class Movable:
    def __init__(self, x: int, y: int, height: int, width: int, speed: int, sprite_paths: list[list[str]]) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.walk_cycle_position = 0
        self.direction = "left"
        self.sprites = sprite_path_lists_to_pygame_image_list(sprite_paths)
        self.speed = speed
        self.walk_cycle_position = 0

    def direction_to_sprites_two_d_array_index(self, direction):
        match self.direction:
            case "left":
                return 0

            case "right":
                return 1

            case "up":
                return 2

            case "down":
                return 3

    def draw(self, window) -> None:
        if self.walk_cycle_position + 1 >= len(self.sprites[0]):
            self.walk_cycle_position = 0

        window.blit(self.sprites[self.direction_to_sprites_two_d_array_index(self.direction)][self.walk_cycle_position], (self.x, self.y))
        self.walk_cycle_position += 1
        return

    def move_forward(self):
        match self.direction:
            case "left":
                self.x -= self.speed

            case "right":
                self.x += self.speed

            case "up":
                self.y -= self.speed

            case "down":
                self.y += self.speed

    def face(self, direction):
        if direction not in ["left", "right", "up", "down"]:
            raise ValueError("Direction must be one of the following: 'left', 'right', 'up', 'down'")
        else:
            self.direction = direction
