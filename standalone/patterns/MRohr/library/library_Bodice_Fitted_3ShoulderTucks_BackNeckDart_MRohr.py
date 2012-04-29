#!/usr/bin/env python
# library_Bodice_Fitted_3ShoulderTucks_BackNeckDart_MRohr.py
# pattern no. 111 B3
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

import patterns.MRohr.blocks.block_Bodice_Fitted_SingleDart_MRohr as BB


"""
library_Bodice_Fitted_3ShoulderTucks_BackNeckDart_MRohr.py
pattern no. 111 B3
Based on:
1. library_Bodice_Fitted_3WaistDarts_MRohr.p,  pattern no. 111 B1
2. library_Bodice_Fitted_BackNeckDart_MRohr.py,  pattern no. 111 B2
This is a library block to be used to make other patterns
This program called by including it in the command line parameters for the ./mkpattern shell file
This program imports lib_Block_Bodice_Fitted_SingleDart_MRohr as BB
The BB.pattern() function is called to define variables used to create this pattern.
The BB.pattern() variables are returned to this program and are further modified to create the Tucks & Back Neck Dart.
Doc.draw() is called at the end of the program to create the SVG output file named as a parameter for ./mkpattern.
After ./mkpattern completes execution, run Inkscape to add seam allowances, remove the reference layer to the SVG file, export as a .PDF, and print
The tmtp shell file executes a script which .calls /mkpattern, then opens Inkscape with parameters to automatically add seam allowances, remove the reference layer, save, then export as a .PDF

        Pattern numbering:
        1 --> group --> {1:women, 2:men, 3:girls, 4:boys, 5:babies, 6:home, 7: accessories, 7:crafts, 8:home,0:other }      
        2 --> category --> {1:daywear, 2:outerwear, 3:underwear, 4:pajamas, 5:eveningwear, 6:swimwear, 9:costumes ,0:other}
        3 --> item --> 11:{1:top, 2:pants, 3:dress, 4:skirt, 5:jacket, 0:other}, 12:{jacket,coat,cape}, 13:{1:bra, 2:panties, 3:undershirt, 4:slip}
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
        designerName = 'MRohr' # mandatory
        patternmakerName = 'Susan Spencer'
        patternName = 'Library - Bodice/Fitted/3ShoulderTucks-BackNeckDart/MRohr' # mandatory
        patternNumber = '111 B3' # mandatory
        
        # create document
        doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)
        # create pattern object, add to document
        bodice = Pattern('bodice')
        bodice.styledefs.update(self.styledefs)
        bodice.markerdefs.update(self.markerdefs)
        doc.add(bodice)
        # create pattern pieces, add to pattern object
        bodice.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
        bodice.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))      
        A = bodice.front 
        B = bodice.back  
        
        # call bodice block function in library_Block_Bodice_Fitted_SingleDart_MRohr. Update locals() with values from BB.pattern()
        BB_locals = BB.pattern(doc, A, B, cd)
        globals().update(BB_locals)  # read vars from BB.pattern as vars in this program
 
        # bodice Front A 
        
        # Bodice Front Variables:
        #a : 'center neck',
        #b : 'center waist',
        #c : 'center chest narrow',
        #d : 'side chest narrow ',
        #e : 'front shoulder height',
        #f : 'front shoulder width',
        #h : 'side neck',
        #g : 'shoulder tip',
        #j : 'center chest',
        #k : 'side chest',
        #l : 'side waist',
        #m : 'armscye corner',
        #n : 'armscye curve',
        #o : 'center dart apex height',
        #p : 'dart apex',
        #q : 'dart leg inside at waist',
        #r : 'dart leg outside at waist',
        #h_c2 : 'neck control point',
        #h_c1 : 'neck control point',
        #d_c2 : 'armscye across chest control point',
        #d_c1 : 'armscye across chest control point',
        #n_c1 : 'armscye curve control point',
        #n_c2 : 'armscye curve control point',
        #k_c1 : 'armscye end control point',
        #k_c2 : 'armscye end control point'        

        # adjustments for 3 shoulder tucks
        midpoint = pMidpointP(q, r) # midpoint of original dart at waist
        dartwidth = lineLengthP(q, r)/3.0 # dart width is 1/3 of original waist dart
        dartwidth_half = dartwidth/2.0        
        d1, d2, d3 = Pnt(),  Pnt(),  Pnt() # 3 darts, each with .p, .i, .o  (apex,inside,outside points)
        d1.a, d2.a, d3.a = rPoint(A, 'd1.a', p.x, p.y), rPoint(A, 'd2.a', p.x + 1*IN, p.y),  rPoint(A, 'd3.a', p.x + 2*IN, p.y) # d#.p is object for dart-apex coordinates - d#.p.x, d#.p.y
        d1.i = rPointP(A, 'd1.i', q )
        d1.o = rPoint(A, 'd1.o', q.x + dartwidth, q.y) # i = inside leg, o = outside leg
        d2.i = rPoint(A, 'd2.i', d1.o.x + .75*IN, midpoint.y)
        d2.o = rPoint(A, 'd2.o', d2.i.x + dartwidth,  d2.i.y)
        d3.i = rPoint(A, 'd3.i', d2.o.x + .75*IN, r.y)
        d3.o = rPoint(A, 'd3.o', d3.i.x + dartwidth, d3.i.y)
        # slash & spread the angle of the lower darts at each d1.m, d2.m, d3.m points   along shoulder. 
        # 1st create two svg points at end of each slashline
        d2.m1 = rPointP(A, 'd2.m1', pMidpointP(h, g)) # slashline = d2.a to d2.m1 & m2
        d2.m2 = rPointP(A, 'd2.m2', d2.m1)
        d1.m1 = rPointP(A, 'd1.m1', pntOnLineP(d2.m1, h, 1*IN)) # d1.a to d1.m1 & m2
        d1.m2 = rPointP(A, 'd1.m2', d1.m1)
        d3.m1 = rPointP(A, 'd3.m1', pntOnLineP(d2.m1, g, 1*IN)) # d3.a to d3.m1 & m2
        d3.m2 = rPointP(A, 'd3.m2', d3.m1)        
        # get the angle (or amount) to spread each slashline
        d1.angle = angleOfVectorP(d1.i, d1.a, d1.o)  # angle of lower dart to be removed & replaced by upper tuck
        #d2.angle = angleOfVectorP(d2.i, d2.a, d2.o) # ""
        d3.angle = angleOfVectorP(d3.i, d3.a, d3.o) # ""
        # rotate around d1.a
        for pnt in (d1.m2, d2.a, d2.m1, d2.m2, d3.a, d3.m1, d3.m2, g, d_c1, d_c2, d, n_c1, n_c2, n, k_c1, m, k_c2, k, l, d3.o, d3.i, d2.o, d2.i, d1.o):
            #  rotate about d1.a all points that are to the right of d1.a, d1.m1, & d1.i
            distance = lineLengthP(d1.a, pnt)
            pnt.r = rPointP(A, pnt.name + '.r', pntFromDistanceAndAngleP(d1.a, distance, angleOfLineP(d1.a, pnt) + d1.angle )) # Add = spread towards right. Subtract = spread towards left.  (y-axis increases downwards, so compass rotates upside down)
        # rotate around d2.a.r
        d2.angle = angleOfVectorP(d2.i.r, d2.a.r, d2.o.r)  #angle of lower dart to be removed & replaced by upper tuck    
        for pnt in (d2.m2, d3.a, d3.m1, d3.m2, g, d_c1, d_c2, d, n_c1, n_c2, n, k_c1, m, k_c2, k, l, d3.o, d3.i, d2.o):
            #  rotate about d2.a.r all points that are to the right of d2.a.r, d2.m1.r, & d2.i.r
            distance = lineLengthP(d2.a.r, pnt.r)
            temp = pntFromDistanceAndAngleP(d2.a.r, distance, angleOfLineP(d2.a.r, pnt.r) + d2.angle)
            pnt.r.x, pnt.r.y =  temp.x, temp.y # Add = spread towards right. Subtract = spread towards left.       
        d3.angle = angleOfVectorP(d3.i.r, d3.a.r, d3.o.r)  #angle of lower dart to be removed & replaced by upper tuck    
        for pnt in (d3.m2, g, d_c1, d_c2, d, n_c1, n_c2, n, k_c1, m, k_c2, k, l, d3.o):
            #  rotate about d3.a.r all points that are to the right of d3.a.r, d3.m1.r, & d3.i.r
            distance = lineLengthP(d3.a.r, pnt.r)
            temp = pntFromDistanceAndAngleP(d3.a.r, distance, angleOfLineP(d3.a.r, pnt.r) + d3.angle)
            pnt.r.x, pnt.r.y =  temp.x, temp.y # Add = spread towards right. Subtract = spread towards left.
        # find points where dart lines intersect 'across chest' line to determine where tucks end
        tuckline2 = rPointP(A, 'tuckline2', pMidpointP(g, d)) # halfway between shoulder tip & side 'across chest '
        tuckline1 = rPoint(A, 'tuckline1', a.x, tuckline2.y)
        d1.h1 = rPointP(A, 'd1.h1', pntIntersectLinesP(d1.m1, d1.a, tuckline1, tuckline2))
        d1.h2 = rPointP(A, 'd1.h2', pntOnLineP(d1.m2.r, d1.a, lineLengthP(d1.m1, d1.h1)))
        d2.h1 = rPointP(A, 'd2.h1', pntIntersectLinesP(d2.m1.r, d2.a.r, tuckline1, tuckline2))
        d2.h2 = rPointP(A, 'd2.h2', pntOnLineP(d2.m2.r, d2.a.r, lineLengthP(d2.m1.r, d2.h1)))
        d3.h1 = rPointP(A, 'd3.h1', pntIntersectLinesP(d3.m1.r, d3.a.r, tuckline1, tuckline2))
        d3.h2 = rPointP(A, 'd3.h2', pntOnLineP(d3.m2.r, d3.a.r, lineLengthP(d3.m1.r, d3.h1)))
            
        #grainline points
        Ag1 = rPoint(A,  'Ag1', a.x + 2*IN, a.y + 2*IN)
        Ag2 = rPoint(A, 'Ag2', Ag1.x, b.y - 2*IN)
        # label points
        A.label_x,  A.label_y = h.x, h.y + 2*IN
        # gridline
        grid = path()
        addToPath(grid, 'M', b, 'L', e, 'L', f, 'L', g, 'M', c, 'L', d, 'M', j, 'L', k, 'M', o, 'L', p,  'M', m, 'L', n,  'M', m, 'L', d, 'M', tuckline1, 'L',  tuckline2)
        addToPath(grid, 'M', j, 'L', k, 'M', o, 'L', p,  'M', m, 'L', n,  'M', m, 'L', d)
        # dartline
        dartLine = path()
        addToPath(dartLine, 'M', d1.m1, 'L', d1.h1, 'M', d1.m2.r, 'L', d1.h2)
        addToPath(dartLine, 'M', d2.m1.r, 'L', d2.h1, 'M', d2.m2.r,  'L', d2.h2)
        addToPath(dartLine, 'M', d3.m1.r, 'L', d3.h1, 'M', d3.m2.r, 'L', d3.h2) 
        #seamline & cuttingline
        seamLine = path()
        cuttingLine = path()
        for P in seamLine, cuttingLine:
            addToPath(P, 'M', a, 'C', h_c1, h_c2, h)
            addToPath(P,'L', d1.m1, 'L', d1.m2.r, 'L', d2.m1.r, 'L', d2.m2.r, 'L', d3.m1.r, 'L', d3.m2.r)
            addToPath(P, 'L', g.r, 'C', d_c1.r, d_c2.r, d.r, 'C',  n_c1.r, n_c2.r,  n.r, 'C', k_c1.r, k_c2.r, k.r) 
            addToPath(P, 'L', l.r, 'L', b, 'L', a)     
        # add grid, grainline, seamline & cuttingline paths to pattern
        addGrainLine(A, Ag1, Ag2)
        addGridLine(A, grid)
        addDartLine(A, dartLine)
        addSeamLine(A, seamLine)            
        addCuttingLine(A, cuttingLine)
        
        # bodice Back B
        
        # Bodice Back variables
        #aa: nape, 
        #bb: center waist, 
        #cc: center across back, 
        #dd: side across back, 
        #ee: center shoulder height, 
        #ff : side shoulder width, 
        #hh: side neck, 
        #gg: shoulder tip, 
        #jj: center chest, 
        #kk: side chest, 
        #ll: side waist marker, 
        #mm: side waist, 
        #nn: dart legt outside, 
        #oo: armscye corner, 
        #pp: armscye curve, 
        #qq: dart leg inside, 
        #rr: dart apex, 
        #hh_c1, hh_c2: neck control points, 
        #dd_c1, dd_c2: armscye 'across back' control points, 
        #pp_c1, pp_c2: armscye curve control points, 
        #kk_c1, kk_c2: armscye end control points

        # adjustments for back neck dart
        bb2 = rPoint(B, 'bb2', bb.x - .5*IN,  bb.y)
        aa2 = rPoint(B, 'aa2', aa.x + .25*IN, aa.y)
        Pnts = pntIntersectCircleCircleP(kk, cd.side, bb2, cd.back_waist_width*0.5)
        if (Pnts.intersections != 0):
            if (Pnts.p1.x < Pnts.p2.x):
                pnt = Pnts.p1
            else:
                pnt = Pnts.p2
            mm2 = rPointP(B, 'mm2', pnt)                
        else:
            print 'no intersection found' # TODO - make this more robust, or have a better fail mechanism
        dart1 = Pnt() # group to hold all dart points, dart name = dart1
        dart1.i = rPoint(B, 'dart1.i', aa2.x - 1.25*IN, aa2.y)
        dart1.o = rPoint(B, 'dart1.o', dart1.i.x - .25*IN, aa2.y )
        dart1.a = rPoint(B, 'dart1.a', dart1.i.x - .25/2.*IN, dart1.i.y + 3*IN)
        
        #grainline points
        Bg1 = rPoint(B,  'Bg1', aa.x - 2*IN, aa.y + 2*IN)
        Bg2 = rPoint(B, 'Bg2', Bg1.x, bb.y - 2*IN)
        # label points 
        B.label_x,  B.label_y = hh.x, hh.y + 2*IN
        # dartline
        dartLine = path()
        addToPath(dartLine, 'M', dart1.i, 'L', dart1.a, 'L', dart1.o)
        # grid
        grid = path()
        addToPath(grid, 'M', bb, 'L', ee, 'L', ff, 'L', gg, 'M', cc, 'L', dd, 'M', jj, 'L', kk, 'M', oo, 'L', pp,  'M', oo, 'L', dd,  'M', kk, 'L', ll, 'L', mm)
        # seamline, cuttingline
        seamLine = path()
        cuttingLine = path()
        for P in seamLine, cuttingLine:
            addToPath(P, 'M', aa2, 'C', hh_c1, hh_c2, hh, 'L', gg, 'C', dd_c1, dd_c2, dd,  'C',  pp_c1, pp_c2,  pp, 'C', kk_c1, kk_c2,  kk) 
            addToPath(P, 'L', mm2, 'L', bb2, 'L', aa2)
        # add grid, grainline, seamline & cuttingline paths to pattern
        addGrainLine(B, Bg1, Bg2)
        addGridLine(B, grid)
        addDartLine(B, dartLine)
        addSeamLine(B, seamLine)
        addCuttingLine(B, cuttingLine)

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

