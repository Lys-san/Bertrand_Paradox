"""
This module contains informations about geometry objects like a point, a line
or a circle and useful functions to use on such objects.
"""

__author__    = "Lysandre Macke"
__credits__   = ["Lysandre Macke"]
__version__   = "0.0.3"
__email__     = "lysandre.macke@edu.univ-eiffel.fr"

import sys
import math
import random
import time
from upemtk import * #credits : Arnaud Carayol, Cyril Nicaud, Carine Pivoteau

### global variables

windowWidth  = 1000
windowHeight = 1000
INFTY        = 2**1000

### class

class Point:
    """
    This class is designed for a point from a plan, represented by its
    coordonates x and y, and a name (optionnal).
    """
    def __init__(self, x, y, name = 0):
        self.x = x
        self.y = y
        self.name = name if name else ""


    def __str__(self):
        return self.name + "(" + str(self.x) + ", " + str(self.y) + ")"


    def draw(self, color = "red", radius = 1):
        """
        Graphic display of the current Point.
        Returns the objet identifier.
        """
        texte(self.x - 5, self.y - 20, self.name, couleur = "red", taille = 6)
        return cercle(self.x, self.y, radius, color, color)


    def symetric(self, symetryCenter):
        """
        Returns the symetrical point according to the given symetry center
        (which must be a Point).
        """
        x = 2*symetryCenter.x - self.x
        y = 2*symetryCenter.y - self.y

        return Point(x, y)


    def equals(self, point):
        """
        Returns true if the specified point has the same coordinates as the
        current Point.
        """
        return round(self.x) == round(point.x) and \
                round(self.y) == round(point.y)


class Triangle:
    """
    This class is designed for a triangle, represented by its 3 vertices (which
    must be a Point object.
    """
    def __init__(self, a, b, c, name = 0):
        self.a = a # first vertex
        self.b = b # secnd vertex
        self.c = c # third vertex
        self.name = name if name else a.name + b.name + c.name


    def __str__(self):
        return self.name + " : " + self.a.__str__() + " " + self.b.__str__() \
                + self.c.__str__()


    def draw(self, color = "grey77"):
        """
        Graphic display of the current Triangle.
        Returns the object identifier.
        """
        pointList = [(self.a.x, self.a.y),
                     (self.b.x, self.b.y), \
                     (self.c.x, self.c.y)]

        return polygone(pointList, color);

    def sideLen(self):
        """
        Considering that all sides have same lengths.
        Returns the length of the ab vertex.
        """
        return Line(self.a, self.b).length()

class Circle:
    """
    This class is designed for a circle, represented by its center (which must
    be a Point object) and its radius.
    """
    def __init__(self, center, radius, name = 0):
        if radius <= 0:
            sys.exit("Error while creating Circle object :" \
            +"radius must be stricly positive (given radius " + str(radius) + " is <= 0).")

        self.center = center #must be a Point
        self.radius = radius
        self.name = name if name else ""

    def __str__(self):
        return self.name + " center : " + self.center.__str__() + ", radius : " + str(self.radius)


    def draw(self):
        """
        Graphic display of the current Circle.
        Returns the objet identifier.
        """
        return cercle(self.center.x, self.center.y, self.radius)


    def contains(self, p):
        """
        Returns true if the p point is inside of the current Cirlce,
        otherwise returns false.
        """
        return round(Line(self.center, p).length()) <= self.radius


    def perimeterContains(self, p):
        """
        Returns true if the p point is on the border of the current Circle,
        otherwise returns fase.
        """
        return round(Line(self.center, p).length()) == self.radius


    def randomPointFromPerimeter(self):
        """
        Returns a randomly generated point from the border of the Circle.
        """

        theta = math.radians(random.randint(0, 360))
        return Point(round(self.center.x + self.radius*math.cos(theta)), \
            round(self.center.y + self.radius*math.sin(theta)))


    def randomPointFromArea(self):
        """
        Returns a randomly generated point from the inside of the Circle.
        """
        p = randomPoint(self.center.x - self.radius, self.center.x + self.radius, \
                        self.center.y - self.radius, self.center.y + self.radius)

        while not self.contains(p):
            p = randomPoint(self.center.x - self.radius, self.center.x + self.radius, \
                            self.center.y - self.radius, self.center.y + self.radius)
        return p

    def randomRadius(self):
        return Line(self.center, self.randomPointFromPerimeter())

    def verticalRadius(self):
        point = Point(self.center.x, self.center.y + self.radius)
        return Line(self.center, point)

    def equilateralTriangle(self):
        """
        Returns an equilateral triangle inscribed in the current circle.
        """
        a = Point(self.center.x + self.radius, self.center.y)
        b = Point(self.center.x + math.cos(math.radians(120))*self.radius, \
         self.center.y + math.sin(math.radians(120))*self.radius)
        c = Point(self.center.x + math.cos(math.radians(-120))*self.radius, \
         self.center.y + math.sin(math.radians(-120))*self.radius)

        return Triangle(a, b, c)


    def randomChord_1(self):
        """
        Returns a chord generated from 2 random points.
        """

        chord = Line(self.randomPointFromPerimeter(), self.randomPointFromPerimeter())
        while(chord.length() == 0):
            chord = Line(self.randomPointFromPerimeter(), self.randomPointFromPerimeter())
        mise_a_jour()
        return chord

    def randomChord_2(self, drawTmpLine = False):
        """
        Returns a chord genereted with the second method (cf wikipedia).
        """
        # random radius
        tmp = self.randomRadius()
        # random point from the radius
        p = tmp.randomPoint()

        if(drawTmpLine):
            tmp.draw("gray90")
            p.draw()
            mise_a_jour()

        return self.chordOfMiddle(p)


    def randomChord_3(self):
        """
        Returns a chord generated with the third method (cf wikipedia).
        """
        p = self.randomPointFromArea()
        return self.chordOfMiddle(p)


    def chordFrom(self, point, slope):
        """
        Returns a chord crossing a given point and having a given slope.
        """
        x, y = point.x, point.y
        a = Point(x, y)
        while(self.contains(a)):
            a.x += 1
            a.y = point.y + round(slope*(a.x - point.x))
        b = a.symetric(point)

        return Line(a, b)


    def chordOfMiddle(self, middlePoint):
        """
        Returns the chord of a given middle point, which must be a Point.
        """

        if(not self.contains(middlePoint)):
            sys.exit("The given point isn't inside of the circle.")


        tmpLine = Line(self.center, middlePoint)
        radius = self.verticalRadius()

        s1 = tmpLine.slope()
        s2 = radius.slope()

        # finding theta angle between tmpLine and vertical axis
        tanTheta = (s1 - s2)/(1 + s1*s2)
        theta = math.atan(tanTheta)

        theta = math.degrees(theta)

        # tmp is perpandicular to tmpLine
        tmp = Point(radius.b.x + self.radius*math.cos(math.radians(theta)), radius.b.y + self.radius*math.sin(math.radians(theta)), "tmp")

        a = self.center
        b = tmp
        lastTmp = Line(a, b)

        s3 = lastTmp.slope()
        chord = self.chordFrom(middlePoint, s3)

        return chord



class Line:
    """
    This class is designed for a line from a plan, represented by two Point
    objects.
    """
    def __init__(self, a, b, name = 0):
        if(a.x < b.x):
            self.a = a
            self.b = b
        else:
            self.a = b
            self.b = a
        self.name = name if name else a.name + b.name

    def __str__(self):
        left = self.name if self.name == " " else "length"
        return left + " = " + str(self.length())


    def draw(self, color = "black"):
        """
        Graphic display of the current Line.
        Returns the object identifier.
        """
        return ligne(self.a.x, self.a.y, self.b.x, self.b.y, couleur = color)


    def length(self):
        """
        Returns the length of the Line.
        """
        return math.sqrt((self.b.x - self.a.x)**2 + (self.b.y - self.a.y)**2);


    def longerThan(self, line):
        """
        Returns true if the current Line is longer than an other specified Line.
        """
        return self.length() > line.length()


    def middle(self):
        """
        Returns the middle Point of the Line.
        """
        return Point((self.a.x + self.b.x)/ 2, (self.a.y + self.b.y)/ 2)


    def randomPoint(self):
        """
        Returns a randomly generated Point on the given Line.
        """
        # if line is vertical
        if(self.b.x == self.a.x):
            y_min = self.a.y if self.a.y < self.b.y else self.b.y
            y_max = self.a.y if self.a.y > self.b.y else self.b.y
            return Point(self.b.x, random.randint(y_min, y_max))

        # constructing the linear equation
        a = (self.b.y - self.a.y)/(self.b.x - self.a.x)
        b = self.a.y - a * self.a.x

        #constructing the point
        x_min = self.a.x if self.a.x < self.b.x else self.b.x
        x_max = self.a.x if self.a.x > self.b.x else self.b.x

        x = random.randint(x_min, x_max)
        return Point(x, a*x + b)

    def slope(self):
        """
        Returns the slope of the Line.
        """
        if(self.a.x == self.b.x):
            return INFTY
        return (self.b.y - self.a.y)/(self.b.x - self.a.x)


### functions

def randomPoint(xMin = 0, xMax = windowWidth, yMin = 0, yMax = windowHeight, name = 0):
    """
    Generates and returns a random point beetween given coordonates (optionnal).
    """
    return Point(random.randint(xMin, xMax), random.randint(yMin, yMax), name if name else "")


def upperLeftPoint(points):
    """
    Returns the upper left point from a given point list.
    """
    if(len(points) <= 0):
        sys.exit("Please enter a list with at least one Point.")

    ul = points[0]

    for i in range(1, len(points)):
        if(points[i].x < ul.x and points[i].y < ul.y):
            ul = points[i]

    return ul
    print("p =", success/n)


### tests

def geometryTest():
    random.seed(time.time()) # initialising random seed

    # initializing objects
    A = Point(windowWidth/2, windowHeight/2, "A")
    print(A)
    B = Point(4, 6, "B")
    print(B)
    C = randomPoint(name = "C")
    print(C)
    AB = Line(A, B)
    print(AB)

    radius = 300
    circle = Circle(A, radius, "C")
    print(circle)

    equi = circle.equilateralTriangle()
    #print(equi)

    # display
    cree_fenetre(windowWidth, windowHeight)
    # A.draw()
    # B.draw()
    # C.draw()
    circle.draw()
    equi.draw()

    # tests starts here
    # test = circle.chordFrom(circle.center, 0)
    # test.draw("red")
    # test2 = circle.chordFrom(circle.center, 9990)
    # test2.draw("blue")
    # remove when finished

    n = 60 #number of chords in the circle
    chordList        = []
    randomPointsList = []

    success = 0 # number of chords that are > to equi side length

    A.draw()

    mise_a_jour()

    print("Generating chords, please wait...")

    for i in range (n):
        chordList.append(circle.randomChord_2())
        currentChord = chordList[i]
        if(currentChord.length() > equi.sideLen()):
            currentChord.draw("sky blue")
            success += 1
        else:
            currentChord.draw("orange")
        print("p =", success/(i + 1))


    A.draw()
    circle.draw()

    print("END.")
    attend_ev()
    ferme_fenetre()


geometryTest()