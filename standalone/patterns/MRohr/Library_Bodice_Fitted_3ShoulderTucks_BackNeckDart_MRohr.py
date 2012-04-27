#!/usr/bin/env python
# Library_Bodice_Fitted_3ShoulderTucks_BackNeckDart_MRohr.py
# pattern no. 111 B3
# Based on Library_Bodice_Fitted_3WaistDarts_MRohr.py pattern no. 111 B1
# & Library_Bodice_Fitted_BackNeckDart_MRohr.py pattern no. 111 B2
# This is a library block
# to be used to make other patterns.
# There is no ease added to any measurement
# Garments made directly from this pattern will not fit
# Ease must be added in design pattern

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
        patternNumber = '#111 B3' # mandatory
        # 1 --> group --> {1:women, 2:men, 3:girls, 4:boys, 5:babies, 6:home, 7: accessories, 7:crafts, 8:home,0:other }      
        # 2 --> category --> {1:daywear, 2:outerwear, 3:underwear, 4:pajamas, 5:eveningwear, 6:swimwear, 9:costumes ,0:other}
        # 3 --> item --> 11:{1:top, 2:pants, 3:dress, 4:skirt, 5:jacket, 0:other}, 12:{jacket,coat,cape}, 13:{1:bra, 2:panties, 3:undershirt, 4:slip}
        # 4 --> usage --> A:pattern block,B:library pattern,C:designer pattern - A & B read-only except for authorized super-users, C read-only except for designer-owner
        # 5 --> sequential number for items added to group &1234


        doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)

        # pattern object
        bodice = Pattern('bodice')
        bodice.styledefs.update(self.styledefs)
        bodice.markerdefs.update(self.markerdefs)
        doc.add(bodice)

        # bodice Front A
        bodice.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
        A = bodice.front
        #pattern points
        a = rPoint(A, 'a', 0.0, 0.0) # center neck
        b = rPoint(A, 'b', 0., cd.front_waist_length) # center waist
        c = rPoint(A, 'c',  0., cd.front_waist_length/5.0) # center chest narrow
        d = rPoint(A, 'd', a.x + cd.front_chest_narrow_width/2.0, c.y) # side chest narrow - armscye narrowest point
        e = rPoint(A, 'e', 0., b.y - cd.front_shoulder_height)
        #f = rPoint(A, 'f', lineLengthP(c, d)+ 0.5*IN, e.y)
        f = rPoint(A, 'f', a.x + cd.front_shoulder_width/2.0, e.y) # changed f formula to accommodate my shoulders - Improvement
        h = rPoint(A, 'h', a.x + cd.neck_width/2.0, e.y) # side necks
        height = abs(lineLengthP(h, f))
        hypoteneuse = cd.shoulder
        base = (abs(hypoteneuse**2.0 - height**2.0))**0.5
        g = rPoint(A, 'g', f.x, f.y + base)
        j = rPoint(A, 'j', 0., b.y - cd.side - (11/8.0)*IN)
        k = rPoint(A, 'k', a.x + cd.front_bust_width/2.0, j.y)    
        l = rPoint(A, 'l', k.x, k.y + cd.side)
        m = rPoint(A, 'm', d.x, k.y)
        pnt = pntFromDistanceAndAngleP(m, 1*IN, angleOfDegree(315.0)) # TODO - add dictionary for distance to use based on the customer's chest size
        n = rPointP(A, 'n', pnt)
        o = rPoint(A, 'o', 0., c.y + lineLengthP(c, b)/2.0)
        p = rPoint(A, 'p', a.x + lineLengthP(e, f)/2.0, o.y)
        q = rPoint(A, 'q', p.x - 0.5*IN, b.y)
        length1 = lineLengthP(p, q)
        length2 = cd.front_waist_arc - lineLengthP(b, q)
        Pnts = pntIntersectCircleCircleP(p, length1, l, length2)
        if (Pnts.intersections != 0):
            if (Pnts.p1.y > p.y):
                pnt = Pnts.p1
            else:
                pnt = Pnts.p2
        else:
            print 'no intersection found'
        r = rPointP(A, 'r', pnt)
        #neck control points
        angle = angleOfLineP(h, g)+angleOfDegree(90)
        pnt = pPoint(a.x + 500, a.y) # arbitrary point to create horizontal calculation for h_c1
        h_c2 = cPointP(A, 'h_c2', pntFromDistanceAndAngleP(h, lineLengthP(a, h)/3.0, angle))
        h_c1 = cPointP(A, 'h_c1', pntIntersectLinesP(a, pnt, h, h_c2)) # control point is horizontal to a, and on line created by h-to-h_c2. Creates smooth neckline preserving 90degree seam at neck side, and 180degree seam at neck front
        # armscye control points
        d_c2 = cPointP(A, 'd_c2', pntFromDistanceAndAngleP(d, lineLengthP(d, g)/3.0, angleOfLineP(n, g)))
        d_c1 = cPointP(A, 'd_c1', pntFromDistanceAndAngleP(g, lineLengthP(d, g)/3.0, angleOfLineP(g, d_c2)))
        n_c1 = cPointP(A, 'n_c1', pntFromDistanceAndAngleP(d, lineLengthP(d, n)/3.0, angleOfLineP(g, n)))
        n_c2 = cPointP(A, 'n_c2', pntFromDistanceAndAngleP(n, lineLengthP(d, n)/3.0, angleOfLineP(k, d)))           
        k_c1 = cPointP(A, 'k_c1', pntFromDistanceAndAngleP(n, lineLengthP(n, k)/3.0, angleOfLineP(d, k)))         
        k_c2 = cPoint(A, 'k_c2', k.x - lineLengthP(n, k)/3.0, k.y) # b/w n & k, horizontal with k.y     
      
        # 3 shoulder tucks adjustments:
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
        #slash & spread the angle of the lower darts at each d1.m, d2.m, d3.m points   along shoulder. 
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
            
            
        #grainline points
        Ag1 = rPoint(A,  'Ag1', a.x + 2*IN, a.y + 2*IN)
        Ag2 = rPoint(A, 'Ag2', Ag1.x, b.y - 2*IN)
        # label points
        A.label_x,  A.label_y = h.x, h.y + 2*IN
        # gridline
        grid = path()
        addToPath(grid, 'M', b, 'L', e, 'L', f, 'L', g, 'M', c, 'L', d, 'M', j, 'L', k, 'M', o, 'L', p,  'M', m, 'L', n,  'M', m, 'L', d)
        addToPath(grid, 'M', j, 'L', k, 'M', o, 'L', p,  'M', m, 'L', n,  'M', m, 'L', d)
        # dartline
        dartLine = path()
        addToPath(dartLine, 'M', d1.i, 'L', d1.a, 'L', d1.o.r, 'M', d2.i.r, 'L', d2.a, 'L', d2.o.r, 'M', d3.i.r, 'L', d3.a, 'L', d3.o.r) # lower darts - draw tucks using original non-rotated d1.a, d2.a, d3.a points
        addToPath(dartLine, 'M', d1.m1, 'L', d1.a, 'L', d1.m2.r) # d1.a & d1.m1  & d1.i were not rotated Rotated points are denoted <pnt>.r
        addToPath(dartLine, 'M', d2.m1.r, 'L', d2.a.r,  'L',d2.m2.r)
        addToPath(dartLine, 'M', d3.m1.r, 'L', d3.a.r, 'L', d3.m2.r)
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
        bodice.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
        B = bodice.back
        #pattern points
        aa = rPoint(B, 'aa', 0., 0.)
        bb = rPoint(B, 'bb', 0., cd.back_waist_length)
        cc = rPoint(B, 'cc', 0., cd.back_waist_length/4.0)
        dd = rPoint(B, 'dd', aa.x - cd.back_chest_narrow_width/2.0, cc.y)
        ee = rPoint(B, 'ee', 0.,  bb.y - cd.back_shoulder_height)
        #ff = rPoint(B, 'ff', dd.x - .25*IN, ee.y)
        ff = rPoint(B, 'ff', aa.x - cd.back_shoulder_width/2.0, ee.y) #changed ff formula to accommodate my shoulders - Improvement
        hh = rPoint(B, 'hh', aa.x - cd.neck_width/2.0, ee.y)
        height = abs(lineLengthP(hh, ff))
        hypoteneuse = cd.shoulder
        base = (abs(hypoteneuse**2.0 - height**2.0))**0.5
        gg = rPoint(B, 'gg', ff.x, ff.y + base) 
        jj = rPoint(B, 'jj', 0., bb.y - cd.side + .25*IN)
        kk = rPoint(B, 'kk', aa.x - cd.back_bust_width/2.0, jj.y)
        ll = rPoint(B, 'll', kk.x, kk.y + cd.side)
        mm = rPoint(B, 'mm', ll.x + .75*IN, ll.y)
        nn = rPoint(B, 'nn', aa.x - lineLengthP(jj, kk)/2.0, bb.y)
        oo = rPoint(B, 'oo', dd.x, jj.y)
        pp = rPointP(B, 'pp', pntFromDistanceAndAngleP(oo, (9/8.)*IN, angleOfDegree(225))) # TODO - add dictionary for distance to use based on the customer's chest size
        qq = rPoint(B, 'qq', aa.x - (cd.back_waist_arc - lineLengthP(mm, nn)), bb.y)
        rr = rPoint(B, 'rr',  nn.x + lineLengthP(nn, qq)/2.0, jj.y)
        length1 = lineLengthP(pp, qq) # dart leg 
        length2 = cd.back_waist_arc - lineLengthP(bb, qq)
        #neck control points
        hh_c1 =  cPoint(B, 'hh_c1', aa.x - lineLengthP(aa, hh)/2.0,  a.y)
        hh_c2 =  cPointP(B, 'hh_c2', pntOnLineP(hh, hh_c1, lineLengthP(hh, hh_c1)/2.0))
        # armscye control points   
        pnts = pointList(gg, dd, pp, kk)
        c1, c2 = controlPoints('BackArmscye', pnts)
        dd_c1, dd_c2 = cPointP(B, 'dd_c1', c1[0]), cPointP(B, 'dd_c2', c2[0])
        pp_c1, pp_c2 = cPointP(B, 'pp_c1', c1[1]), cPointP(B, 'pp_c2', c2[1])
        kk_c1, kk_c2 = cPointP(B, 'kk_c1', c1[2]), cPointP(B, 'kk_c2', c2[2]) 
        #adjustments for back neck dart
        bb2 = rPoint(B, 'bb2', bb.x - .5*IN,  bb.y)
        aa2 = rPoint(B, 'aa2', aa.x + .25*IN, aa.y)
        Pnts = pntIntersectCircleCircleP(kk, cd.side, bb2, cd.back_waist_arc)
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

