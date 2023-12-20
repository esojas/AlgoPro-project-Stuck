import pygame
from support import import_folder


class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0 # will take one of the picture from the keys inside dict
        self.animation_speed = 0.15
        self.image = self.animation['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        # player movement
        self.direction = pygame.math.Vector2(0,0) # we use vector2 is a list that contains x,y
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        #player status
        self.player_status = 'idle'
        self.face_right = True # seeing if char look left or right
        #quite cofusing
        self.on_ground = False
        self.on_ceiling = False
        # self.on_left = False
        # self.on_right = False





    def import_character_assets(self):
        character_path = 'img/player/'
        self.animation = {'idle':[],'run':[],'jump':[],'fall':[],'shooting':[]} # these dicts keys name have to be the same

        for animation in self.animation.keys():
            full_path = character_path + animation # this loop access the key and attach it at the end of character path
            self.animation[animation] = import_folder(full_path)

    # def position_gun(self):
    #     Gun((self.direction.x,self.direction.y))



    def animate(self):
        animation = self.animation[self.player_status]

        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): # this basically checks if the counter is more than the list
            self.frame_index = 0 # we reset the counter back to zero

        image = animation[int(self.frame_index)]
        if self.face_right: # makes the image flip
            self.image = image
        else:
            flipped_img = pygame.transform.flip(image,True,False)
            self.image = flipped_img

        #set the rect
        # if self.on_ground and self.on_right: # if player is on the ground and touching something on the right
        #     self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        # elif self.on_ground and self.on_left:
        #     self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        # if self.on_ground:
        #     self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.on_ceiling and self.on_right:
        #     self.rect = self.image.get_rect(topright = self.rect.topright)
        # elif self.on_ceiling and self.on_left:
        #     self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # else:
        #     self.rect = self.image.get_rect(center = self.rect.center)



    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.face_right = True
            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.face_right = False
            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        # equipt gun
        # elif keys[pygame.K_s]:
        #
        else:
            self.direction.x = 0
        return self.direction.x, self.direction.y

    def getstatus(self):
        #jumping
        if self.direction.y < 0:
            self.player_status = 'jump'
        #fall
        elif self.direction.y > 1: #make it bigger than gravity because our program keep cycling trhough gravity and 0 from the level setting
            self.player_status = 'fall'
        else: # because of that cycle the animation keep cycling through idle and fall even when not jump or falling
            if self.direction.x == 0:
                self.player_status = 'idle'
            else:
                self.player_status = 'run'





# still not sure how gravity works
    def apply_gravity(self):
        self.direction.y += self.gravity # propels the player to ground
        self.rect.y += self.direction.y # using the rectangle player ensures a smooth vertical movement

    def jump(self):
        self.direction.y = self.jump_speed

    # def shoot(self):
    #     self.gun = pygame.sprite.Group()
    #     self.bullet = pygame.sprite.Group()
    #     bullet = Bullet()
    #     weapon = Gun((self.direction.x,self.direction.y))
    #     self.gun.add(weapon)
    #     self.bullet.add(bullet)
    #     self.gun.update()
    #     self.bullet.update()
    #     # Blit the rotated gun onto the screen
    #     self.gun.draw(weapon)
    #     self.bullet.draw(screen)


    def update(self):
        # self.track_mouse()
        self.get_input()
        self.getstatus()
        self.animate()
        print(self.rect.center)
