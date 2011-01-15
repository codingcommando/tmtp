#!/usr/bin/python

import sys, copy

# define directory where this script and frontbodice.inx are located
sys.path.append('/usr/share/inkscape/extensions')

import inkex
import re
import simplestyle
import simplepath
import simpletransform
import math
from lxml import etree


class DrawFrontBodice(inkex.Effect):
    def __init__(self):
          inkex.Effect.__init__(self)        
          # Store measurements from BackBodice.inx into object 'self'    
          self.OptionParser.add_option('-n', '--neck_circumference', action='store', type='float', dest='neck_circumference', default=1.0, help='Neck-circumference in inches')
          self.OptionParser.add_option('--shoulder_width', action='store', type='float', dest='shoulder_width', default=1.0, help='Shoulder-width in inches')
          self.OptionParser.add_option('--front_armpit_distance', action='store', type='float', dest='front_armpit_distance', default=1.0, help='Front-armpit-distance in inches')
          self.OptionParser.add_option('--back_armpit_distance', action='store', type='float', dest='back_armpit_distance', default=1.0, help='Back-armpit-distance in inches')
          self.OptionParser.add_option('--bust_circumference', action='store', type='float', dest='bust_circumference', default=1.0, help='Bust-circumference in inches')
          self.OptionParser.add_option('--bust_points_distance', action='store', type='float', dest='bust_points_distance', default=1.0, help='Bust-points-distance in inches')
          self.OptionParser.add_option('--bust_length', action='store', type='float', dest='bust_length', default=1.0, help='Bust-length in inches')
          self.OptionParser.add_option('--front_bodice_length', action='store', type='float', dest='front_bodice_length', default=1.0, help='Front-bodice-length in inches')
          self.OptionParser.add_option('--back_bodice_length', action='store', type='float', dest='back_bodice_length', default=1.0, help='Back-bodice-length in inches')
          self.OptionParser.add_option('--waist_circumference', action='store', type='float', dest='waist_circumference', default=1.0, help='Waist-circumference in inches')
          self.OptionParser.add_option('--upper_hip_circumference', action='store', type='float', dest='upper_hip_circumference', default=1.0, help='Upper-hip-circumference in inches')
          self.OptionParser.add_option('--lower_hip_circumference', action='store', type='float', dest='lower_hip_circumference', default=1.0, help='Lower-hip-circumference in inches')
          self.OptionParser.add_option('--side_seam_length', action='store', type='float', dest='side_seam_length', default=1.0, help='Side-seam-length in inches')

          
    def DrawMyLine(self,mylayer,X1,Y1,X2,Y2,mycolor,mywidth,myid):
           mystyle = { 'stroke': mycolor,'stroke-width': mywidth,'id':myid}
           myattribs = { 'style' : simplestyle.formatStyle(mystyle),
                              'x1' : str(X1),
                              'y1' : str(Y1),
                              'x2' : str(X2),
                              'y2' : str(Y2)}
           inkex.etree.SubElement(mylayer,inkex.addNS('line','svg'),myattribs)

    def DrawMyDot(self,mylayer,X1,Y1,myradius,mycolor,mywidth,myfill,myid):
           mystyle = { 'stroke' : mycolor, 'stroke-width' : mywidth, 'fill' : myfill}
           myattribs = {'style' : simplestyle.formatStyle(mystyle),
                        inkex.addNS('id','inkscape') : myid,
                        'cx': str(X1),
                        'cy': str(Y1),
                        'r' : str(myradius)}
           inkex.etree.SubElement(mylayer,inkex.addNS('circle','svg'),myattribs)

    def DrawMyQCurve(self,mylayer,X1,Y1,X2,Y2,C1,C2,mycolor,mywidth,myid):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px',  'fill': 'none', 'id' : myid}
           mypathattribs = {'d': 'M '+str(X1)+', '+str(Y1)+'  Q '+str(C1)+', '+str(C2)+'  '+str(X2)+', '+str(Y2), 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)

    def DrawMyCurve(self,mylayer,mypathdefinition,mycolor,mywidth,myid):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px',  'fill': 'none', 'id' : myid}
           mypathattribs = {'d': mypathdefinition, 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)
          

    def GetCoordsFromSlope(self,mylayer,x2,y2,myslope,mylength):
           # !!!!!!!!!Fix this later to make dart to end at individual's back distance
           # line slope formula:     m = (y2-y1)/(x2-x1)
           #                        (y2-y1) = m(x2-x1)                         /* we'll use this in circle formula
           #                         y1 = y2-m(x2-x1)                          /* we'll use this after we solve circle formula
           # circle radius formula: (x2-x1)^2 + (y2-y1)^2 = r^2                /* see (y2-y1) ?
           #                        (x2-x1)^2 + (m(x2-x1))^2 = r^2             /* substitute m(x2-x1) for (y2-y1) from line slope formula 
           #                        (x2-x1)^2 + (m^2)(x2-x1)^2 = r^2           /* 
           #                        (1 + m^2)(x2-x1)^2 = r^2                   /* pull out common term (x2-x1)^2 - advanced algebra ding!
           #                        (x2-x1)^2 = (r^2)/(1+m^2)
           #                        (x2-x1) = r/((1+(m^2))^(.5))
           #                         x1 = x2-(r/((1+(m^2))^(.5)))
           # solve for (x1,y1)
           m=myslope
           r=mylength
           x1= x2-(r/((1+(m**2))**(.5)))
           y1= y2-m*(x2-x1)
           return (x1,y1)

    

           
           #______________


 

    def effect(self):
           convert_to_pixels=(90)                    #convert inches to pixels - 90px/in
           convert_to_inches=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           nc=self.options.neck_circumference*convert_to_pixels
           sw=self.options.shoulder_width*convert_to_pixels
           fad=self.options.front_armpit_distance*convert_to_pixels
           bad=self.options.back_armpit_distance*convert_to_pixels
           bc=self.options.bust_circumference*convert_to_pixels
           bpd=self.options.bust_points_distance*convert_to_pixels
           fbusl=self.options.bust_length*convert_to_pixels
           fbl=(self.options.front_bodice_length+1)*convert_to_pixels
           bbl=self.options.back_bodice_length*convert_to_pixels
           wc=self.options.waist_circumference*convert_to_pixels
           uhc=self.options.upper_hip_circumference*convert_to_pixels
           lhc=self.options.lower_hip_circumference*convert_to_pixels
           ssl=self.options.side_seam_length*convert_to_pixels
           begin_pattern_x=30*convert_to_pixels               #Pattern begins in upper left corner x=3"
           begin_pattern_y=3*convert_to_pixels               # same...y=3" 
           referenceline_color='gray'
           referenceline_width='7'
           referenceline_fill='gray'
           patternline_color='black'
           patternline_width='10'
           patternline_fill='black'
           dot_radius = .15*convert_to_pixels                #pattern dot markers are .15" radius
           dot_color = 'red'
           dot_width = .15
           dot_fill = 'red'
           dartline_color = 'black'
           dartline_width = '10'
           dartline_fill = 'black'
           dartdot_radius = .10*convert_to_pixels
           dartdot_color = 'black'
           dartdot_width = .10
           dartdot_fill='black'
           

           # Create a special layer to draw the pattern.
           my_rootlayer = self.document.getroot()
           self.layer = inkex.etree.SubElement(my_rootlayer, 'g')
           self.layer.set(inkex.addNS('groupmode', 'inkscape'), 'Bodice Block 2')
           self.layer.set(inkex.addNS('label', 'inkscape'), 'Front Bodice Block')

           my_layer=self.layer
           #_______________
           # Create vertical line AB as Back Reference Line starting in upper left corner.
           # Point A is (Ax,Ay), point B is (Bx,By).  
           Ax=begin_pattern_x
           Ay=begin_pattern_y
           Bx=Ax
           By=Ay+fbl
           self.DrawMyLine(my_layer,Ax,Ay,Bx,By,referenceline_color,referenceline_width,'FB_AB')
           self.DrawMyDot(my_layer,Ax,Ay,dot_radius,dot_color,dot_width,dot_fill,'FB_A')
           self.DrawMyDot(my_layer,Bx,By,dot_radius,dot_color,dot_width,dot_fill,'FB_B')
           # Create bust-line point C along AB, measuring from A, at length = front-bodice-length/2. 
           Cx=Ax
           Cy=Ay+(fbl/2)
           self.DrawMyDot(my_layer,Cx,Cy,dot_radius,dot_color,dot_width,dot_fill,'FB_C') 
           #_______________
           # Create armpit-line point D along AB, measuring from A, at length = front-bodice-length/3. 
           Dx=Ax
           Dy=Ay+(fbl/3)
           self.DrawMyDot(my_layer,Dx,Dy,dot_radius,dot_color,dot_width,dot_fill,'FB_D')    
           #_______________                
           #At A, draw line length = shoulderwidth/2 , perpendicular to AB. Mark endpoint as G. No shoulder dart in front bodice.
           Gx=Ax-(sw/2)  # subtract sw/2 because front bodice is drawn right to left
           Gy=Ay
           self.DrawMyLine(my_layer,Ax,Ay,Gx,Gy,referenceline_color,referenceline_width,'FB_AG')
           self.DrawMyDot(my_layer,Gx,Gy,dot_radius,dot_color,dot_width,dot_fill,'FB_G') 
           #_______________
           #On AG, measuring from A, mark point E at length = (neck-circumference/6 + .5cm. E marks point for Neck opening.         
           Ex=Ax-((nc/6)+(.5*convert_to_inches*convert_to_pixels))
           Ey=Ay
           self.DrawMyDot(my_layer,Ex,Ey,dot_radius,dot_color,dot_width,dot_fill,'FB_E')  
           #_______________
           #On AB, measuring from A, mark point F at nc/6+.5cm. F marks point for Neck depth.
           Fx=Ax
           Fy=Ay+((nc/6)+(.5*convert_to_pixels))
           controlx=Ex
           controly=Fy
           self.DrawMyQCurve(my_layer,Fx,Fy,Ex,Ey,controlx,controly,patternline_color,patternline_width,'FB_FE')
           self.DrawMyDot(my_layer,Fx,Fy,dot_radius,dot_color,dot_width,dot_fill,'FB_F')           
           #_______________
           #At G, draw line: length = 3cm, perpendicular to AG. Mark endpoint as H. (3cm is average depth of front shoulder slope)
           #!!!!Fix this later to an individual's actual shoulder slope
           Hx=Gx
           Hy=Gy+(3*convert_to_inches)*(convert_to_pixels)
           self.DrawMyLine(my_layer,Gx,Gy,Hx,Hy,referenceline_color,referenceline_width,'FB_GH')
           #_______________
           #Draw line from E to H. Creates sloped shoulder line EH.
           self.DrawMyLine(my_layer,Ex,Ey,Hx,Hy,patternline_color,patternline_width,'FB_EH')
           self.DrawMyDot(my_layer,Hx,Hy,dot_radius,dot_color,dot_width,dot_fill,'FB_H') 
           #_______________
           # Create Armpit reference line
           Ix=(Dx-(fad/2))
           Iy=Dy
           self.DrawMyLine(my_layer,Ix,Iy,Dx,Dy,referenceline_color,referenceline_width,'FB_DI')
           self.DrawMyDot(my_layer,Ix,Iy,dot_radius,dot_color,dot_width,dot_fill,'FB_I')
           # Create Bust reference line
           #Jx=(Cx-(bc/4))
           #Jy=Cy
           #self.DrawMyLine(my_layer,Jx,Jy,Cx,Cy,referenceline_color,referenceline_width,'FB_CJ')
           #self.DrawMyDot(my_layer,Jx,Jy,dot_radius,dot_color,dot_width,dot_fill,'FB_J')
           #_______________
           # Create Waist Reference Line 
           # Find Dart Intake Size - this measurement is in relationship to the dart size for the skirt
           # Take widest hip circumference, subtract waist size, divide by 9.  
           # Waist Line reference line = (wc/4)+(2*dartdepth)+1cm
           if (uhc > lhc):
                hip_minus_waist = (uhc-wc)
           else:
                hip_minus_waist = (lhc-wc)
           my_dartdepth=(hip_minus_waist/9)
           Px=Bx-((wc/4)+(2*my_dartdepth)+(1*convert_to_inches*convert_to_pixels))   # subtract -- drawing from right to left--add 1cm - we took out 1cm from back
           Py=By                                                                     # BP is a horizontal line
           self.DrawMyLine(my_layer,Bx,By,Px,Py,referenceline_color,referenceline_width,'FB_BP')         
           self.DrawMyDot(my_layer,Px,Py,dot_radius,dot_color,dot_width,dot_fill,'FB_P')
           #_______________
           # Create Waist Dart
           #dart midpoint = bust point distance/2
           
      

	   
my_effect = DrawFrontBodice()
my_effect.affect()
