"""
This module contains display fonctions to use in the Bertrand Paradow program.
"""

__author__    = "Lysandre Macke"
__credits__   = ["Lysandre Macke"]
__version__   = "0.0.0"
__email__     = "lysandre.macke@edu.univ-eiffel.fr"

from upemtk import * #credits : Arnaud Carayol, Cyril Nicaud, Carine Pivoteau

###global variables

windowWidth = 200
windowHeight = 200

###functions declaration

def test():
    """
    tmp test function. Not to be called in the main program.
    """
    cree_fenetre(windowWidth, windowHeight) # cree_fenetre and ferme_fenetre must \
                                             #be used like this in the main
    attend_ev()
    ferme_fenetre()

test()
