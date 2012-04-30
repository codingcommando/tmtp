#!/usr/bin/env python
# block_Bodice_Fitted_SingleDart_MRohr.py
# pattern no. 111A 1
# This is a pattern block to be used to make other patterns.

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.client   import Client
from tmtpl.curves  import GetCurveControlPoints

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *


def pattern(doc, A, B, cd):
    
    # bodice Front A
    #pattern points
    a = rPoint(A, 'a', 0.0, 0.0) # center neck
    b = rPoint(A, 'b', 0., cd.front_waist_length) # center waist
    c = rPoint(A, 'c',  0., a.y + cd.front_waist_length/5.0) # center chest narrow
    d = rPoint(A, 'd', a.x + cd.front_across_chest_width/2.0, c.y) # side chest narrow - armscye narrowest point
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
    length2 = cd.front_waist_width/2.0 - lineLengthP(b, q)
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
    
    # bodice Back B
    #pattern points
    aa = rPoint(B, 'aa', 0., 0.)
    bb = rPoint(B, 'bb', 0., cd.back_waist_length)
    cc = rPoint(B, 'cc', 0., cd.back_waist_length/4.0)
    dd = rPoint(B, 'dd', aa.x - cd.back_across_chest_width/2.0, cc.y)
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
    qq = rPoint(B, 'qq', aa.x - (cd.back_waist_width/2.0 - lineLengthP(mm, nn)), bb.y)
    rr = rPoint(B, 'rr',  nn.x + lineLengthP(nn, qq)/2.0, jj.y)
    length1 = lineLengthP(pp, qq) # dart leg 
    length2 = cd.back_waist_width/2.0 - lineLengthP(bb, qq)
    #neck control points
    hh_c1 =  cPoint(B, 'hh_c1', aa.x - lineLengthP(aa, hh)/2.0,  a.y)
    hh_c2 =  cPointP(B, 'hh_c2', pntOnLineP(hh, hh_c1, lineLengthP(hh, hh_c1)/2.0))
    # armscye control points   
    pnts = pointList(gg, dd, pp, kk)
    c1, c2 = controlPoints('BackArmscye', pnts)
    dd_c1, dd_c2 = cPointP(B, 'dd_c1', c1[0]), cPointP(B, 'dd_c2', c2[0])
    pp_c1, pp_c2 = cPointP(B, 'pp_c1', c1[1]), cPointP(B, 'pp_c2', c2[1])
    kk_c1, kk_c2 = cPointP(B, 'kk_c1', c1[2]), cPointP(B, 'kk_c2', c2[2]) 

    # return all variables to the calling program
    return locals()

# vi:set ts=4 sw=4 expandtab:

