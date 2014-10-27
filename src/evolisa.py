from PIL import Image
from PIL import ImageDraw
import random
import tempfile
import signal
import sys

BACKGROUND = (255, 255, 255, 255)
# BACKGROUND = (0, 0, 0, 255)

# 0) Setup a random DNA string  (application start)
# 
# 1) Copy the current DNA sequence and mutate it slightly
# 2) Use the new DNA to render polygons onto a canvas
# 3) Compare the canvas to the source image
# 4) If the new painting looks more like the source image than the
#    previous painting did, then overwrite the current DNA with the new DNA
# 5) repeat from 1

POLYGONS = 200
GO = True
SHOW_EVERY = 5
LIMIT = 100000
ALPHA = 256
MOAR = 20
SAVED = None
# SAVED = [([(180, 211), (395, 376), (111, 182), (220, 270)], (67, 243, 131, 152)), ([(377, 128), (90, 100), (80, -5), (297, 375)], (59, 43, 107, 147)), ([(38, 141), (400, 10), (71, 185), (74, 144)], (197, 95, 175, 174)), ([(510, 22), (172, 126), (145, 302), (530, 330)], (43, 165, 57, 67)), ([(524, 373), (392, 57), (84, 144), (536, 292)], (207, 140, 97, 82)), ([(447, 243), (511, -17), (82, 157), (182, 56)], (239, 116, 9, 228)), ([(370, 33), (33, 176), (438, 164), (41, 181)], (127, 40, 18, 22)), ([(137, 237), (265, 399), (387, 411), (64, 360)], (13, 88, 158, 229)), ([(510, 234), (366, 65), (347, 392), (458, 156)], (29, 76, 151, 125)), ([(385, -17), (82, 43), (346, 341), (55, 94)], (222, 61, 148, 147)), ([(-1, 351), (219, 371), (234, 262), (164, 78)], (176, 216, 136, 235)), ([(487, 21), (339, 129), (81, 420), (73, 77)], (165, 156, 204, 243)), ([(526, 248), (1, -12), (493, 5), (487, 233)], (127, 161, 78, 245)), ([(117, 133), (117, 121), (410, 282), (130, 229)], (178, 197, 231, 133)), ([(553, 310), (95, 317), (280, 338), (504, 71)], (82, 32, 118, 212)), ([(269, 332), (186, 212), (458, 335), (294, 14)], (34, 223, 202, 148)), ([(510, 403), (129, 132), (327, 31), (73, 58)], (73, 220, 247, 81)), ([(536, 411), (276, 123), (375, 223), (272, 384)], (18, 23, 53, 212)), ([(30, 63), (427, 237), (417, 357), (-18, 332)], (52, 118, 205, 228)), ([(50, 14), (363, 198), (117, -5), (229, 199)], (74, 213, 210, 30)), ([(-18, 419), (380, 401), (487, 111), (142, 247)], (74, 28, 20, 226)), ([(548, 352), (288, 144), (95, 98), (346, 187)], (144, 68, 113, 241)), ([(172, 332), (206, 367), (535, 322), (424, -20)], (136, 211, 59, 221)), ([(308, 263), (244, 68), (216, 150), (63, 410)], (100, 115, 143, 3)), ([(-10, -14), (223, 28), (115, 295), (18, 284)], (124, 34, 19, 197)), ([(321, 281), (550, 84), (391, 319), (263, 238)], (226, 148, 124, 53)), ([(544, 388), (331, 31), (256, -1), (93, 233)], (17, 141, 17, 220)), ([(478, 336), (552, 40), (351, 62), (102, 361)], (93, 107, 17, 252)), ([(245, 6), (300, 281), (371, 247), (74, 110)], (84, 103, 65, 57)), ([(253, 348), (349, 285), (349, 248), (211, 418)], (104, 168, 3, 34))]

def generate_dna(img_size):
    dna = []
    for i in range(POLYGONS):
        points = []
        for j in range(4):
            points.append((random.randrange(0 - MOAR, img_size[0] + MOAR, 1),
                           random.randrange(0 - MOAR, img_size[1] + MOAR, 1)))
        fill = (random.randrange(0, 256, 1),
                random.randrange(0, 256, 1),
                random.randrange(0, 256, 1), ALPHA)
        fill = (0, 0, 0, random.randrange(0, 256))
        points = sorted(points)
        dna.append((points, fill))

    return dna

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
    # image = Image.open('src/ml.jpg')
    # image = Image.open('src/ml2.jpg')
    image = Image.open('src/bs2.jpg')
    image.show()
    size = image.size

    # step 0
    if SAVED is None:
        dna = generate_dna(size)
    else:
        dna = SAVED
    # print dna
    img = convert_image_to_rgb(generate_image(size, dna))
    if not GO:
        img.show()

    # step 1 - copy and mutate current dna seq
    step = 0
    current = img
    while step < LIMIT and GO:
        if step % 10 == 0:
            print "Generation %d" % step
        dna_mut = mutate(image.size, dna)
        img_mut = generate_image(image.size, dna_mut)
        img_rgb = convert_image_to_rgb(img_mut)

        fit_1 = fitness(image, current)
        fit_2 = fitness(image, img_rgb)

        if  fit_1 < fit_2:
            pass
        else:
            dna = dna_mut[:]
            current = img_rgb
            img_rgb.show()
            print dna
            print "\n"

        step = step + 1
        # if step % SHOW_EVERY == 0:
        #     current.show()
        #     # print dna

def mutate(size, dna):
    dna_mut = [mutate_part(size, x) for x in dna]
    # for i in range(len(dna)):
    #     print dna[i], dna_mut[i]
    #     if dna[i] != dna_mut[i]:
    #         print "X"
    return dna_mut

def mutate_part(size, part):
    points = part[0]
    colour = part[1]

    rnd = random.randrange(0, 1000, 1) / 1000.0
    if rnd > 0.500:
        # do nothing
        return (points, colour)

    points_mut = []
    for j in range(4):
        points_mut.append((random.randrange(0 - MOAR, size[0] + MOAR, 1),
                           random.randrange(0 - MOAR, size[1] + MOAR, 1)))

    if rnd < 0.450:
        # mutate colour
        colour = (random.randrange(0, 256),
                  random.randrange(0, 256),
                  random.randrange(0, 256),
                  random.randrange(0, ALPHA))

    return (points_mut, colour)

def fitness(img_1, img_2):
    fitness = 0
    for y in range(0, img_1.size[1]):
        for x in range(0, img_1.size[0]):
            r1, g1, b1 = img_1.getpixel((x, y))
            r2, g2, b2 = img_2.getpixel((x, y))
            # get delta per color
            d_r = r1 - r2
            d_b = b1 - b2
            d_g = g1 - g2
            # measure the distance between the colors in 3D space
            pixel_fitness = d_r * d_r + d_g * d_g + d_b * d_b 
            # add the pixel fitness to the total fitness (lower is better)
            fitness += pixel_fitness
    return fitness

if __name__ == "__main__":
    main()
