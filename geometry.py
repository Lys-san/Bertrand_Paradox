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


    def draw(self):
        """
        Graphic display of the current Triangle.
        Returns the object identifier.
        """
        pointList = [(self.a.x, self.a.y),
                     (self.b.x, self.b.y), \
                     (self.c.x, self.c.y)]

        return polygone(pointList);

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
        p = randomPoint(self.center.x - self.radius, self.center.x + self.radius, \
                        self.center.y - self.radius, self.center.y + self.radius)

        while not self.perimeterContains(p):
            p = randomPoint(self.center.x - self.radius, self.center.x + self.radius, \
                            self.center.y - self.radius, self.center.y + self.radius)
        return p


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


    def equilateralTriangle(self, startPoint = 0):
        """
        Returns an equilateral triangle inscribed in the current circle.
        If no start point is given, it will be randomly generated.
        """
        a = startPoint if startPoint else self.randomPointFromPerimeter() #ref point
        # symetric
        tmp = a.symetric(self.center)

        # cet algo fait le taff mais est horrible (la complexité ahhhh, plus de
        # 5 secondes avant d'avoir le résultat)
        # A REVOIR PLUS TARD

        b = self.randomPointFromPerimeter()
        while(round(Line(tmp, b).length()) != self.radius):
            b = self.randomPointFromPerimeter()

        c = self.randomPointFromPerimeter()
        while(round(Line(tmp, c).length()) != self.radius or c.equals(b)):
            c = self.randomPointFromPerimeter()

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

    def randomChord_2(self):
        """
        Returns a chord genereted with the second method (cf wikipedia).
        """
        # random radius
        tmp = Line(self.center, self.randomPointFromPerimeter())

        # random point from the radius
        p = tmp.randomPoint()

        return self.chordOfMiddle(p)


    def randomChord_3(self):
        """
        Returns a chord generated with the third method (cf wikipedia).
        """
        p = self.randomPointFromArea()
        return self.chordOfMiddle(p)


    def chordOfMiddle(self, middlePoint):
        """
        Returns the chord of a given middle, which must be a Point.
        """

        print(">>> Searching chord based of given middle point...")
        if(not self.contains(middlePoint)):
            sys.exit("The given point isn't inside of the circle.")

        tmp = Line(self.center, middlePoint).length()
        chordLen = math.sqrt((self.radius)**2 - tmp**2)

        # circle equation formula
        (self.radius)**2 = (x - self.center.x)**2 + (y - self.center.y)**2

        print("> Chord found. Returning object.")
        return chord


class Line:
    """
    This class is designed for a line from a plan, represented by two Point
    objects.
    """
    def __init__(self, a, b, name = 0):
        self.a = a  # first point
        self.b = b  # second point
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
        # constructing the linear equation
        a = (self.b.y - self.a.y)/(self.b.x - self.a.x)
        b = self.a.y - a * self.a.x

        #constructing the point
        x_min = self.a.x if self.a.x < self.b.x else self.b.x
        x_max = self.a.x if self.a.x > self.b.x else self.b.x

        x = random.randint(x_min, x_max)
        return Point(x, a*x + b)


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


### tests

def geometryTest():
    random.seed(time.time()) # initialising random seed

    # initialising objects
    A = Point(windowWidth/2, windowHeight/2, "A")
    print(A)
    B = Point(4, 6, "B")
    print(B)
    C = randomPoint(name = "C")
    print(C)
    AB = Line(A, B)
    print(AB)

    radius = 400
    circle = Circle(A, radius, "C")
    print(circle)

    #equi = circle.equilateralTriangle()
    #print(equi)

    # display
    cree_fenetre(windowWidth, windowHeight)
    A.draw()
    B.draw()
    C.draw()
    circle.draw()
    #equi.draw()

    n = 10 #number of chords in the circle
    chordList        = []
    randomPointsList = []

    print("Generating chords, please wait...")
    for i in range (n):
        chordList.append(circle.randomChord_3())
        chordList[i].draw("light blue")

    circle.draw()
    A.draw()


    print("END.")
    attend_ev()
    ferme_fenetre()


geometryTest()