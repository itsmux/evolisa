import copy
import json
import math
import random
import sys
import tempfile

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter


COLOUR_BLACK = (0, 0, 0, 255)
COLOUR_WHITE = (255, 255, 255, 255)
OFFSET = 10
POLYGONS = 50
POLY_MIN_POINTS = 3
POLY_MAX_POINTS = 5


class Polygon(object):
    """Polygon"""
    def __init__(self, colour=None, points=[]):
        self.colour = colour
        self.points = points

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u"{}, {}".format(self.points, self.colour)

    def mutate(self, size):
        """
        mutate either colour or points.
        """
        rand = random.random()
        if rand <= 0.5:
            print u"changing colour"
            idx = random.randrange(0, 4)
            value = random.randrange(0, 256)
            colour = list(self.colour)
            colour[idx] = value
            self.colour = tuple(colour)
        else:
            print u"changing point"
            idx = random.randrange(0, len(self.points))
            point = generate_point(size[0], size[1])
            self.points[idx] = point


class DNA(object):
    """DNA"""
    def __init__(self, img_size, polygons=[]):
        self.img_size = img_size
        self.polygons = polygons
        self.generation = 0

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u"{}".format(self.polygons)

    def print_polygons(self):
        """
        debug function to print all DNA polygon info.
        """
        for polygon in self.polygons:
            print polygon

    def draw(self, background=COLOUR_BLACK, show=False, save=False,
             generation=None):
        """
        paint all DNA polygons onto an Image and show it.
        """
        size = self.img_size
        img = Image.new('RGB', size, background)
        draw = Image.new('RGBA', size)
        pdraw = ImageDraw.Draw(draw)
        for polygon in self.polygons:
            colour = polygon.colour
            points = polygon.points
            pdraw.polygon(points, fill=colour, outline=colour)
            img.paste(draw, mask=draw)

        if show:
            img.show()

        if save:
            # TODO use self.generation
            temp_dir = tempfile.gettempdir()
            temp_name = u"0000000000{}".format(generation)[-10:]
            out_path = u"{}/{}.png".format(temp_dir, temp_name)
            img = img.filter(ImageFilter.GaussianBlur(radius=3))
            img.save(out_path)
            print u"saving image to {}".format(out_path)

        return img

    def mutate(self):
        """
        mutate the dna.
        """
        # pick a random polygon
        polygons = copy.deepcopy(self.polygons)
        rand = random.randrange(0, len(polygons))
        random_polygon = polygons[rand]
        random_polygon.mutate(self.img_size)

        return DNA(self.img_size, polygons)


def fitness(img_1, img_2):
    """
    fitness funtcion determines how much alike 2 images are.
    """
    fitness = 0.0
    for y in range(0, img_1.size[1]):
        for x in range(0, img_1.size[0]):
            r1, g1, b1 = img_1.getpixel((x, y))
            r2, g2, b2 = img_2.getpixel((x, y))
            # get delta per color
            d_r = r1 - r2
            d_b = b1 - b2
            d_g = g1 - g2
            # measure the distance between the colors in 3D space
            pixel_fitness = math.sqrt(d_r * d_r + d_g * d_g + d_b * d_b )
            # add the pixel fitness to the total fitness (lower is better)
            fitness += pixel_fitness
    return fitness


def generate_point(width, height):
    """
    generate random (x,y) coordinates in given range (+offset).
    """
    x = random.randrange(0 - OFFSET, width + OFFSET, 1)
    y = random.randrange(0 - OFFSET, height + OFFSET, 1)
    return (x, y)


def generate_colour():
    """
    generate random (r,g,b,a) colour.
    """
    red = random.randrange(0, 256)
    green = random.randrange(0, 256)
    blue = random.randrange(0, 256)
    alpha = random.randrange(0, 256)
    return (red, green, blue, alpha)


def generate_dna(img_size, dna_size=POLYGONS, fixed_colour=False):
    """
    generate dna string consisting of polygons.
    """
    dna = None
    polygons = []
    (width, height) = img_size

    for i in range(POLYGONS):
        nr_of_points = random.randrange(POLY_MIN_POINTS, POLY_MAX_POINTS + 1)
        points = []
        for j in range(nr_of_points):
            # generate a point (x,y) in 2D space and append it to points.
            point = generate_point(width, height)
            points.append(point)

        # generate colour (r,g,b,a) for polygon
        # colour = COLOUR_BLACK if fixed_colour else generate_colour()
        colour = COLOUR_WHITE if fixed_colour else generate_colour()
        polygon = Polygon(colour, points)
        polygons.append(polygon)

    dna = DNA(img_size, polygons)
    return dna


def load_image(path):
    img = Image.open(path)
    return img


def main(argv):
    """
    call with bin/python generate.py <path_to_image>
    """
    if len(argv) != 2:
        sys.exit(0)

    path = argv[1]
    img = load_image(path)
    img_size = img.size
    dna = generate_dna(img_size, dna_size=POLYGONS, fixed_colour=True)
    # dna.print_polygons()
    parent = dna.draw(show=False)
    fitness_parent = fitness(img, parent)

    generations = pic_nr = 0
    while True:
        dna_mutated = dna.mutate()
        child = dna_mutated.draw()
        fitness_child = fitness(img, child)
        if fitness_child < fitness_parent:
            dna = dna_mutated
            fitness_parent = fitness_child
            print u"picking child w. fitness: {}".format(fitness_child)

        generations += 1
        if generations % 100 == 0:
            print u"showing generation {}".format(generations)
            pic_nr += 1
            dna.draw(show=False, save=True, generation=pic_nr)
            # with open('dna.txt', 'w') as outfile:
            #     json.dump(dna, outfile)

    return sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
