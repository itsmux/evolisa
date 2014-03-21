from PIL import Image
from PIL import ImageDraw
import random

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

POLYGONS = 50
GO = True
SHOW_EVERY = 10
LIMIT = 5000
ALPHA = 127

def generate_dna(img_size):
    dna = []
    for i in range(POLYGONS):
        points = []
        for j in range(5):
            points.append((random.randrange(0, img_size[0], 1),
                           random.randrange(0, img_size[1], 1)))
        fill = (random.randrange(0, 256, 1),
                random.randrange(0, 256, 1),
                random.randrange(0, 256, 1), ALPHA)
        # fill = (0, 0, 0, ALPHA)
        dna.append((points, fill))

    return dna

def generate_image(size, dna):
    img = Image.new('RGBA', size, BACKGROUND)

    for (points, colour) in dna:
        draw = Image.new('RGBA', size)
        pdraw = ImageDraw.Draw(draw)

        outline = (colour[0], colour[1], colour[2], ALPHA)
        for p in points:

            pdraw.polygon(points,
                          fill=colour,
                          outline=outline)

        img.paste(draw, mask=draw)
    return img

def main():
    # image = Image.open('src/mlbig.png')
    # image = Image.open('src/mlbig2.png')
    image = Image.open('src/ml2.png')
    size = image.size

    # step 0
    dna = generate_dna(size)
    # print dna
    img = generate_image(size, dna)
    if not GO:
        img.show()

    # step 1 - copy and mutate current dna seq
    # dna_mut = mutate(size, dna)
    # print dna_mut
    step = 0
    current = img
    while step < LIMIT and GO:
        if step % 20 == 0:
            print "Step %d" % step

        dna_mut = mutate(image.size, dna)
        img_mut = generate_image(image.size, dna_mut)

        if fitness(image, current) < fitness(image, img_mut):
            dna = dna
            current = current
        else:
            dna = dna_mut
            current = img_mut

        step = step + 1
        if step % SHOW_EVERY == 0:
            current.show()
            # print dna

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
    # chance to mutate
    rnd = random.randrange(0, 1000, 1) / 1000.0
    if rnd > 0.650:
        # do nothing
        return (points, colour)

    # mutate points
    points_mut = []
    # try changing only one point in the polygon
    rnd_idx = random.randrange(0, len(points))
    p = points[rnd_idx]
    # for p in points:
    rnd_val_x = random.randrange(0, 11, 1)
    rnd_val_y = random.randrange(0, 11, 1)
    if random.randint(0, 1) == 1:
        rnd_val_x = rnd_val_x * -1
    if random.randint(0, 1) == 1:
        rnd_val_y = rnd_val_y * -1
    x = p[0] + rnd_val_x
    y = p[1] + rnd_val_y
    if x < 0:
        x = 0
    if x > size[0]:
        x = size[0]
    if y < 0:
        y = 0
    if y > size[1]:
        y = size[1]
        # points_mut.append((x, y))
    points(rnd_idx) = (x, y)
    points_mut = points

    if rnd < 0.350:
        # mutate colour
        r = random.randrange(0, 11, 1)
        g = random.randrange(0, 11, 1)
        b = random.randrange(0, 11, 1)
        if random.randint(0, 1) == 1:
            r = r * -1
        if random.randint(0, 1) == 1:
            g = g * -1
        if random.randint(0, 1) == 1:
            b = b * -1
        r = colour[0] + r
        g = colour[1] + g
        b = colour[2] + b
        if r > 255:
            r = 255 - r
        if r < 0:
            r = 0
        if g > 255:
            g = 255 - g
        if g < 0:
            g = 0
        if b > 255:
            b = 255 - b
        if b < 0:
            b = 0
        colour = (r, g, b, ALPHA)

    return (points_mut, colour)

def fitness(img_1, img_2):
    fitness = 0
    for y in range(0, img_1.size[1]):
        for x in range(0, img_1.size[0]):
            r1, g1, b1, a = img_1.getpixel((x, y)) # TODO ALPHA MODE?
            r2, g2, b2, a = img_2.getpixel((x, y))
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