'''
Usage: python simple_slideshow.py [image_folder] [display_time]
e.g.
>>> python simple_slideshow.py
>>> python simple_slideshow.py static/archive 2

image_folder : str
    Path to images. Deafult is static/live-slideshow.

display_time : int
    Time in seconds to display each picture for. Default is 60.
    Image are cycled continuously until script is terminated. Press
    escape key to stop slideshow.
'''

import os
import sys
import glob
import pyglet

# Define parameters / parse arguments
try:
    image_folder = sys.argv[1]
except:
    image_folder = os.path.join('static', 'live-slideshow')
try:
    display_time = int(sys.argv[2])
except:
    display_time = 60

def main():
    global window
    global sprite
    global imgs

    window = pyglet.window.Window(fullscreen=True)

    @window.event
    def on_draw():
        sprite.draw()

    imgs = load_images()

    img = pyglet.image.load(next(imgs))
    sprite = pyglet.sprite.Sprite(img)
    scale = get_scale(img)
    sprite.scale = scale
    sprite.set_position(**center_coordinates(img, scale))

    pyglet.clock.schedule_interval(update_image, 2.0)

    pyglet.app.run()

def get_scale(image):
    if image.width > image.height:
        return window.width / image.width
    else:
        return window.height / image.height

def center_coordinates(image, scale):
    position = {}
    position['x'] = window.width/2 - scale*image.width/2
    position['y'] = window.height/2 - scale*image.height/2
    return position

def load_images():
    dir_files = glob.glob(os.path.join(image_folder, '*')
    dir_imgs = [img for img in dir_files
                if img.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    return iter(dir_imgs)

def update_image(dt):
    global imgs
    try:
        img = pyglet.image.load(next(imgs))
    except StopIteration:
        # Re-load images
        imgs = load_images()
        img = pyglet.image.load(next(imgs))
    sprite.image = img
    scale = get_scale(img)
    sprite.scale = scale
    sprite.set_position(**center_coordinates(img, scale))
    window.clear()

if __name__ == '__main__':
    main()
