#!/usr/bin/env python
# library_Mens_Classic_Shirt_Aldrich.py
# pattern no. 211 B1
# This is a library pattern to be used to make other patterns

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.client   import Client
from tmtpl.curves    import GetCurveControlPoints

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *

import patterns.Aldrich.blocks.block_Mens_Classic_Shirt_Aldrich as CS


"""
library_Mens_Classic_Shirt_Aldrich.py
pattern no. 211 B1
Based on:
1. block_Mens_Classic_Shirt_Aldrich.py,  pattern no. 211 B1
This is a library block to be used to make other patterns
This program called by including it in the command line parameters for the ./mkpattern shell file
        Pattern numbering:
        1 --> group --> {1:women, 2:men, 3:girls, 4:boys, 5:babies, 6:home, 7: accessories, 7:crafts, 8:home,0:other }      
        2 --> category --> {1:daywear, 2:outerwear, 3:underwear, 4:pajamas, 5:eveningwear, 6:swimwear, 9:costumes ,0:other}
        3 --> item --> 11:{1:shirt/top/blouse, 2:pants, 3:dress, 4:skirt, 5:jacket, 0:other}, 12:{jacket,coat,cape}, 13:{1:bra, 2:panties, 3:undershirt, 4:slip}
        4 --> usage --> A:pattern block,B:library pattern,C:designer pattern - A & B read-only except for authorized super-users, C read-only except for designer-owner
        5 --> sequential number for items added to group &1234
"""

class PatternDesign():
    
    def __init__(self):
        self.styledefs = {}
        self.markerdefs = {}
        return

    def pattern(self):
        """
        Method defining a pattern design. This is where the designer places
        all elements of the design definition
        """
        # All measurements are converted to pixels
        # x increases towards right, y increases towards bottom of drawing - Quadrant is 'upside down'
        # All angles are in radians
        # angles start with 0 at '3:00', & move clockwise b/c quadrant is 'upside down'
        cd = self.cd    #client data is prefaced with cd
        printer = '36" wide carriage plotter'
        companyName = 'Seamly Patterns'  # mandatory
        designerName = 'Aldrich' # mandatory
        patternmakerName = 'Susan Spencer'
        patternName = 'Library - Mens/ClassicShirt/Aldrich' # mandatory
        patternNumber = '211 B1' # mandatory
         
        # create document
        doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)
        # create pattern object, add to document
        shirt = Pattern('shirt')
        shirt.styledefs.update(self.styledefs)
        shirt.markerdefs.update(self.markerdefs)
        doc.add(shirt)
        # create pattern pieces, add to pattern object
        shirt.add(PatternPiece('pattern', 'yoke', letter='A', fabric=2, interfacing=0, lining=0))
        shirt.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0)) 
        shirt.add(PatternPiece('pattern', 'front', letter='C', fabric=2, interfacing=0, lining=0))
        shirt.add(PatternPiece('pattern', 'sleeve', letter='D', fabric=2, interfacing=0, lining=0))
        shirt.add(PatternPiece('pattern', 'cuff', letter='E', fabric=2, interfacing=0, lining=0))
        shirt.add(PatternPiece('pattern', 'collarstand', letter='F', fabric=2, interfacing=0, lining=0))
        shirt.add(PatternPiece('pattern', 'collar', letter='G', fabric=2, interfacing=0, lining=0))
        A = shirt.yoke
        B = shirt.back
        C = shirt.front
        D = shirt.sleeve
        E = shirt.cuff
        F = shirt.collarstand
        G = shirt.collar
        
        CS_locals = CS.pattern(doc, A, B, C, D, E, F, G, cd) # call shirt block function in library_Mens_Classic_Shirt_Aldrich 
        globals().update(CS_locals)  # update locals() with values from CS.pattern()
 
        # shirt Yoke A 
        #grainline points
        Ag1 = rPoint(A,  'Ag1', h.x + 1*CM, h.y - 1*CM)
        Ag2 = rPoint(A, 'Ag2', Ag1.x, j.y - 1*CM)
        # label points
        A.label_x,  A.label_y = Ag1.x + 1*CM, Ag1.y 
        # gridline
        grid = path()
        addToPath(grid, 'M', a, 'L', j, 'L', o, 'L', k, 'L', m, 'L', i, 'L', a)
        #seamline & cuttingline
        seamLine = path()
        cuttingLine = path()
        for P in seamLine, cuttingLine:          
            addToPath(P, 'M', a, 'L', j, 'L', o, 'L', k, 'L', m, 'L', i, 'L', a)
        # add grid, grainline, seamline & cuttingline paths to pattern
        addGrainLine(A, Ag1, Ag2)
        addGridLine(A, grid)
        addSeamLine(A, seamLine)            
        addCuttingLine(A, cuttingLine)
        

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

