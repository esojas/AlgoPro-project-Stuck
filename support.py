from os import walk

import pygame


# the os walk will give three thing inside tuple (directory path, directory name, filenames)
# we only be using filenames only though

def import_folder(path):
    img_list = []
    for _,__,img_file in walk(path):
        for image in img_file:
            full_path = path + '/' + image
            load_img = pygame.image.load(full_path).convert_alpha()
            resize = pygame.transform.scale(load_img,(64,128))
            img_list.append(resize)

    return img_list



