#!/usr/bin/env python
#!/usr/bin/env python
# block_Bodice_Fitted_SingleDart_Revised_MRohr.py
# pattern no. 111A 2
# This is a pattern block to be used to make other patterns.


#  This pattern block is constructed by combining:
#  1. "Pattern Drafting & Grading Women's and Misses' Garment Design" by M. Rohr revised 1968 edition
#  2. eSewing Workshop Bodice Block
#  3. my secret sauce

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
    
    """
    This bodice block  has a single waist dart, and allows 4in. ease at bust for 36in. bust & 1" ease at waist for 28in. waist
    Adjustments to ease are made according to actual measurements
    """

    # bodice pattern points 
    SHOULDER_WIDTH_EASE = ((3/8.0)*IN)* (cd.back_shoulder_width*0.5/(7.5*IN))
    SHOULDER_SEAM_EASE = (.25*IN)*(cd.shoulder/(5.25*IN))
    FRONT_SHOULDER_HEIGHT_EASE = (2.0*IN)*(cd.front_shoulder_height/(18.0*IN))  
    WAIST_WIDTH_EASE = (1.0*IN)*(cd.waist_circumference/(28.0*IN))
    BUST_POINT_ADJUSTMENT = (0.5*IN)*(cd.bust_circumference/(36.0*IN))
    BUST_HEIGHT_EASE = (.75*IN)*(cd.back_waist_length/(16.5*IN))
    BUST_WIDTH_EASE = (4.0*IN)*(cd.bust_circumference/(36.0*IN))
    print 'BUST_WIDTH_EASE', BUST_WIDTH_EASE
    FRONT_BREAST_WIDTH_EASE = ((3/8.0)*IN)*(cd.bust_circumference/(36.0*IN))
    print 'FRONT_BREAST_WIDTH_EASE', FRONT_BREAST_WIDTH_EASE
    FRONT_BREAST_HEIGHT_ADJUSTMENT = (2.0*IN)*(cd.front_shoulder_height/(18.0*IN))    
    BACK_ARMSCYE_CURVE_DEPTH = (1.25*IN)*(cd.bust_circumference/(36.0*IN))
    FRONT_ARMSCYE_CURVE_DEPTH = (1.0*IN)*(cd.bust_circumference/(36.0*IN))    
    NECK_DEPTH = (0.5*IN)*(cd.neck_width/(2.5*IN)) 
    
    ee = rPoint(B, 'ee', 0.,  0.) # back center shoulder height 
    bb = rPoint(B, 'bb', 0., cd.back_shoulder_height)  # back center waist
    aa = rPoint(B, 'aa', 0.,  bb.y - cd.back_waist_length) # nape
    ff = rPoint(B, 'ff', ee.x - (cd.back_shoulder_width/2.0 + SHOULDER_WIDTH_EASE),  ee.y) # back shoulder width. Improved
    hh = rPoint(B, 'hh', aa.x - cd.neck_width/2.0, ee.y) # back neck width. Improved
    height = abs(lineLengthP(hh, ff))
    hypoteneuse = cd.shoulder + SHOULDER_SEAM_EASE
    base = (abs(hypoteneuse**2.0 - height**2.0))**0.5
    gg = rPoint(B, 'gg', ff.x, ff.y + base) # back shoulder tip. Improved
    jj = rPoint(B, 'jj', 0., aa.y + lineLengthP(aa, bb)/2.0 + BUST_HEIGHT_EASE) # back center bust. Improved
    j = rPoint(A, 'j', jj.x - (cd.bust_circumference + BUST_WIDTH_EASE)/2.0,  jj.y) # front center bust. Improved
    cc = rPoint(B, 'cc', 0., aa.y + lineLengthP(aa, jj)/2.0) # back across back height
    dd = rPoint(B, 'dd', cc.x - cd.back_across_chest_width/2.0, cc.y) # back across back width
    kk = rPoint(B, 'kk', jj.x - (cd.back_bust_width + BUST_WIDTH_EASE/2.0)/2.0, jj.y ) # back bust width. Improved
    k = rPoint(A, 'k', j.x + (cd.front_bust_width + BUST_WIDTH_EASE/2.0)/2.0, j.y) # front bust width
    oo = rPoint(B, 'oo', dd.x, jj.y) # back armscye corner
    pp = rPointP(B, 'pp', pntFromDistanceAndAngleP(oo, BACK_ARMSCYE_CURVE_DEPTH, angleOfDegree(225))) # back armscye curve
    v = rPoint(A, 'v', j.x, ee.y) # front center reference point
    b = rPoint(A, 'b', v.x, v.y + cd.front_shoulder_height + FRONT_SHOULDER_HEIGHT_EASE) # front center waist. Improved
    e = rPoint(A, 'e', v.x, b.y - cd.front_shoulder_height) # front shoulder height
    f = rPoint(A, 'f', e.x + cd.front_shoulder_width/2.0, e.y) # front shoulder width. Improved
    h = rPoint(A, 'h', e.x + cd.neck_width/2.0, e.y) # front neck width. Improved    
    height = abs(lineLengthP(h, f))
    hypoteneuse = cd.shoulder # no shoulder seam ease for the front shoulder
    base = (abs(hypoteneuse**2.0 - height**2.0))**0.5
    g = rPoint(A, 'g', f.x, f.y + base) # front shoulder tip
    a = rPoint(A, 'a',  e.x, b.y - cd.front_waist_length) # front neck height
    u = rPointP(A, 'u', pntFromDistanceAndAngleP(e, NECK_DEPTH, angleOfDegree(45))) # front neck curve
    c = rPointP(A, 'c', pMidpointP(a, j)) # front across chest height
    d = rPoint(A, 'd', c.x + cd.front_across_chest_width/2.0, c.y) # front across chest width
    m = rPoint(A, 'm', d.x, j.y) # front armscye corner
    n = rPointP(A, 'n', pntFromDistanceAndAngleP(m, FRONT_ARMSCYE_CURVE_DEPTH, (-45))) # front armscye curve
    o = rPoint(A, 'o', j.x, j.y + FRONT_BREAST_HEIGHT_ADJUSTMENT) # front breast height
    p = rPoint(A, 'p', o.x + lineLengthP(c, d)/2.0 + BUST_POINT_ADJUSTMENT, o.y) # front dart apex
    t = rPoint(A, 't', k.x + FRONT_BREAST_WIDTH_EASE, o.y) # front breast width
    l = rPointP(A, 'l', pntOnLineP(k, t, cd.side)) # front waist width
    s = rPoint(A, 's', p.x + (17/8.0)*IN, b.y) # front waist dart midpoint, offset from dart apex by 2-1/8
    FRONT_DART_WIDTH = abs((lineLengthP(b, s) + lineLengthP(s, l)) - (cd.front_waist_width + WAIST_WIDTH_EASE/2.0))
    q = rPoint(A, 'q', s.x - FRONT_DART_WIDTH/2.0, b.y) # front waist dart inside    
    r = rPointP(A, 'r', pntOnLineP(s, l, FRONT_DART_WIDTH/2.0))
    rr = rPointP(B, 'rr', pntOnLineP(jj, kk, lineLengthP(cc, dd)/2.0)) # back waist dart apex
    ss = rPoint(B, 'ss', rr.x, bb.y) # back waist dart midpoint   
    BACK_DART_WIDTH = (1.0*IN)
    qq = rPoint(B, 'qq', rr.x + BACK_DART_WIDTH/2.0, bb.y) # back waist dart leg inside
    nn = rPoint(B, 'nn', rr.x - BACK_DART_WIDTH/2.0, bb.y) # back waist dart leg outside
    pnts = pntIntersectCircleCircleP(kk, cd.side, nn, (cd.back_waist + WAIST_WIDTH_EASE)/2.0 - lineLengthP(bb, qq))   
    if (pnts.p1.x < nn.x):
        mm = rPointP(B, 'mm', pnts.p1)
    else:
        mm= rPointP(B, 'tt', pnts.p2)

    #front neck control points
    angle = angleOfLineP(h, g)+angleOfDegree(90)
    pnt = pPoint(a.x + 500, a.y) # arbitrary point to create horizontal calculation for h_c1
    h_c2 = cPointP(A, 'h_c2', pntFromDistanceAndAngleP(h, lineLengthP(a, h)/3.0, angle))
    h_c1 = cPointP(A, 'h_c1', pntIntersectLinesP(a, pnt, h, h_c2)) # control point is horizontal to a, and on line created by h-to-h_c2. Creates smooth neckline preserving 90degree seam at neck side, and 180degree seam at neck front
    # front armscye control points
    d_c2 = cPointP(A, 'd_c2', pntFromDistanceAndAngleP(d, lineLengthP(d, g)/3.0, angleOfLineP(n, g)))
    d_c1 = cPointP(A, 'd_c1', pntFromDistanceAndAngleP(g, lineLengthP(d, g)/3.0, angleOfLineP(g, d_c2)))
    n_c1 = cPointP(A, 'n_c1', pntFromDistanceAndAngleP(d, lineLengthP(d, n)/3.0, angleOfLineP(g, n)))
    n_c2 = cPointP(A, 'n_c2', pntFromDistanceAndAngleP(n, lineLengthP(d, n)/3.0, angleOfLineP(k, d)))           
    k_c1 = cPointP(A, 'k_c1', pntFromDistanceAndAngleP(n, lineLengthP(n, k)/3.0, angleOfLineP(d, k)))         
    k_c2 = cPoint(A, 'k_c2', k.x - lineLengthP(n, k)/3.0, k.y) # b/w n & k, horizontal with k.y               

    #back neck control points
    hh_c1 =  cPoint(B, 'hh_c1', aa.x - lineLengthP(aa, hh)/2.0,  aa.y)
    hh_c2 =  cPointP(B, 'hh_c2', pntOnLineP(hh, hh_c1, lineLengthP(hh, hh_c1)/2.0))
    # back armscye control points   
    pnts = pointList(gg, dd, pp, kk)
    c1, c2 = controlPoints('BackArmscye', pnts)
    dd_c1, dd_c2 = cPointP(B, 'dd_c1', c1[0]), cPointP(B, 'dd_c2', c2[0])
    pp_c1, pp_c2 = cPointP(B, 'pp_c1', c1[1]), cPointP(B, 'pp_c2', c2[1])
    kk_c1, kk_c2 = cPointP(B, 'kk_c1', c1[2]), cPointP(B, 'kk_c2', c2[2]) 
    
    # adjust kk_c1 & pp_c2 to smooth out armscye back curve:
    pnt1 = pntOnLineP(pp, kk_c2, lineLengthP(pp, kk_c1))
    kk_c1.x, kk_c1.y = pnt1.x, pnt1.y
    pnt2 = pntFromDistanceAndAngleP(pp, lineLengthP(pp, pp_c2), angleOfLineP(kk_c1, pp))
    
    for letter in (a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, q, r, s, t, u, v):
        print letter.x, letter.y
    print '****'
    for letter in (aa, bb, cc, dd, ee, ff, gg, hh, jj, kk, mm, nn, oo, pp, qq, rr):
        print letter.x, letter.y

    # return all variables to the calling program
    return locals()

# vi:set ts=4 sw=4 expandtab:

