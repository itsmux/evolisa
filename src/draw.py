from PIL import Image
from PIL import ImageDraw
import random
import tempfile
import signal
import sys

BACKGROUND = (255, 255, 255, 255)


def generate_image(size, dna):
    img = Image.new('RGBA', size, BACKGROUND)

    for (points, colour) in dna:
        draw = Image.new('RGBA', size)
        pdraw = ImageDraw.Draw(draw)

        outline = (colour[0], colour[1], colour[2], colour[3])
        for p in points:

            pdraw.polygon(points,
                          fill=colour,
                          outline=outline)

        img.paste(draw, mask=draw)
    return img


def convert_image_to_rgb(img):
    temp_dir = tempfile.gettempdir()
    # png = Image.open(object.logo.path)
    # png.load() # required for png.split()
    img.load()
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3]) # 3 is the alpha channel

    tf = tempfile.NamedTemporaryFile(delete=False)
    tf_name = "%s.jpg" % tf.name
    bg.save(tf_name, 'JPEG', quality=100)
    # tmp = Image.open(tf_name)
    return bg


def main():
    # step 1:
    # figure out how to draw transparent polygons on top of each other
    size = (512, 512)
    # base image might need to be rgb, not rgba!
    # (https://stackoverflow.com/questions/359706/how-do-you-draw-transparent-polygons-with-python)
    img = Image.new('RGBA', size, (255, 255, 255, 0))

    draw = Image.new('RGBA', size)
    pdraw = ImageDraw.Draw(draw)
    colour = (128, 0, 0, 128)
    points = [(64, 64), (128, 64), (128, 128), (64, 128), ]
    pdraw.polygon(points, fill=colour, outline=colour)
    img.paste(draw, mask=draw)

    colour = (64, 64, 64, 64)
    points = [(96, 96), (160, 96), (160, 160), (96, 160), ]
    pdraw.polygon(points, fill=colour, outline=colour)
    img.paste(draw, mask=draw)

    colour = (0, 196, 0, 128)
    points = [(256, 256), (320, 256), (320, 320), (256, 320), ]
    pdraw.polygon(points, fill=colour, outline=colour)
    img.paste(draw, mask=draw)

    colour = (0, 0, 196, 64)
    points = [(192, 192), (384, 192), (384, 384), (192, 384), ]
    pdraw.polygon(points, fill=colour, outline=colour)
    img.paste(draw, mask=draw)

    colour = (128, 0, 0, 96)
    points = [(224, 224), (352, 224), (352, 352), (224, 352), ]
    pdraw.polygon(points, fill=colour, outline=colour)
    img.paste(draw, mask=draw)

    # read one pixel value
    r, g, b, a = img.getpixel((192, 192))
    print r, g, b, a
    # img = convert_image_to_rgb(img)

    img.show()


if __name__ == "__main__":
    main()
