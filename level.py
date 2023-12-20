import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import player
import math

class Level:
    def __init__(self,level_data,surface): # this is to pass new levels

        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0 # to detect that if our x is positive or negative after colliding
        # Bullets and guns
        self.gun = pygame.image.load('5_1.png').convert_alpha()
        self.angle_degrees = 0  # Initialize angle_degrees
        self.ammo = 1
        self.image_ammo = pygame.image.load('5.png')
        self.bullet_speed = 5
        #player position
        self.player_pos = player((0,0))


    def setup_level(self,layout): # we need to draw the level on the screen
        self.tiles = pygame.sprite.Group() # make it group because we are gonna handle more than one
        self.player = pygame.sprite.GroupSingle() # because only one player

        for row_index,row in enumerate(layout): # this tells us what element consist in the position of list
            for col_index,cell in enumerate(row):
                x = col_index * tile_size  # its multiply by the tile size
                y = row_index * tile_size
                if cell == "x": # if we find x inside the matrix change it into a cube
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile) # basically where are putting this into the one in run
                if cell == "s":
                    Player = player((x,y))
                    self.player.add(Player)


    def scroll_x(self):
        player = self.player.sprite # getting the player
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x < 0: # this basically means if our player is moving to the left and position of our player is below 100 the world will move
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0: # screenwidth/4 makes it responsive or whenever we change the screen width we dont need to change manually
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed  # we multiply so no need to change manually one by one

        for sprite in self.tiles.sprites(): # takes all of the tiles and put it inside sprite
            if sprite.rect.colliderect(player.rect): # checks collision if there is
                if player.direction.x < 0: # checks if player moving left
                    player.rect.left = sprite.rect.right # what this code does is set the player rect exactly right next to the right (sincce its left) of the object
                    #player.on_left = True
                    self.current_x = player.rect.left # this will tell us if we are colliding with the wall
                elif player.direction.x > 0: # checks if player moving right
                    player.rect.right = sprite.rect.left
                    #player.on_right = True # after we jump over the wall this will still set to true
                    self.current_x = player.rect.right # this will tell us if we are colliding with the wall


        #very confusing
        # if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0): # if we touch the wall to the left then start moving left or right we know that we arent touching the wall
        #     player.on_left = False
        # if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
        #     player.on_right = False


    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity() # this will keep on incrementing

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # we collide rect instead of sprite collision because we want to have access to each rectangle to the tiles
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # this statement fix the gravity issue
                    player.on_ground = True # this alone wont be enough because no matter what even if the character is not jumping or falling it still detect if its on the groun
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # again fix the gravity issue so that the player wont get stuck as it hit a ceiling
                    player.on_ceiling = True

        # very confusing
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: # if player is on the floor and jumping or falling
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0: # watch again
            player.on_ceiling = False
    # gun section
    def track_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        gun_rect = self.gun.get_rect(center=(self.player_pos.rect.center))
        angle = math.atan2(mouse_pos[1] - gun_rect.centery, mouse_pos[0] - gun_rect.centerx)
        self.angle_degrees = math.degrees(angle)
        self.transformed_gun = pygame.transform.rotate(self.gun, -self.angle_degrees)
        self.gun_rect = self.transformed_gun.get_rect(center=gun_rect.center)
        return self.transformed_gun, self.gun_rect.topleft

    def create_bullet(self):
        muzzle_offset = 1
        angle = math.radians(self.angle_degrees)
        bullet_x = self.gun_rect.x + muzzle_offset * math.cos(angle)
        bullet_y = self.gun_rect.y + muzzle_offset * math.sin(angle)
        self.ammo = 0
        return bullet_x, bullet_y, angle # add to the bullet class

    def show_gun(self):
        self.display_surface.blit(self.transformed_gun,self.gun_rect)

    def bullet_path(self,bullet_x, bullet_y, angle):
        # make bullet path the same

        self.rect_ammo = self.image_ammo.get_rect(center=(600,350))
        self.rect_ammo.x += self.bullet_speed * math.cos(angle)
        self.rect_ammo.y += self.bullet_speed * math.sin(angle)
        if self.rect_ammo.x >= 1000 or self.rect_ammo.x <= 0: # remove bullet when out of the boundary
            self.kill()
        elif self.rect_ammo.y >= 600 or self.rect_ammo.y <= 0:
            self.kill()

    def run(self):
        #level tiles
        self.tiles.update(self.world_shift) # since self.tiles is one group it will move the entire cube
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.track_mouse()
        self.show_gun()
        print(self.player_pos.rect.center)


