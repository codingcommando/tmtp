#!/usr/bin/python
#
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011 Susan Spencer and Steve Conklin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import math
import json

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *

from constants import *
from patternbase import pBase
from support import boundingBox, transformBoundingBox

# ---- Pattern Classes ----------------------------------------

class Pattern(pBase):
    """
    Create an instance of Pattern class, eg - jacket, pants, corset, which will contain the set of pattern piece objects - eg  jacket.back, pants.frontPocket, corset.stayCover
    A pattern does not generate any svg itself, output is only generated by children objects
    """
    def __init__(self, name):
        self.name = name
        pBase.__init__(self)

    def autolayout(self):
        """
        find out the bounding box for each pattern piece in this pattern, then make them fit within the
        width of the paper we're using
        """

        # get a collection of all the parts, we'll sort them before layout
        parts = {}
        for chld in self.children:
            if isinstance(chld, PatternPiece):
                xlo, ylo, xhi, yhi = chld.boundingBox()
                parts[chld] = {}
                parts[chld]['xlo'] = xlo
                parts[chld]['ylo'] = ylo
                parts[chld]['xhi'] = xhi
                parts[chld]['yhi'] = yhi

        # our available paper width is reduced by twice the border
        pg_width = self.cfg['paper_width'] - (2 * self.cfg['border'])
        if 'verbose' in self.cfg:
            print 'Autolayout:'
            print '    total paperwidth = ', self.cfg['paper_width']
            print '    border width = ', self.cfg['border']
            print '    available paperwidth = ', pg_width
            print '    pattern offset = ', PATTERN_OFFSET

        next_x = 0
        # -spc- FIX Figure out how to leave room for the title block!
        next_y = 6.0 * in_to_pt # this should be zero
        max_y_this_row = 0
        # a very simple algorithm

        # we want to process these in alphabetical order of part letters
        index_by_letter = {}
        letters = []
        for pp, info in parts.items():
            letter = pp.letter
            if letter in index_by_letter:
                raise ValueError('The same Pattern Piece letter <%s> is used on more than one pattern piece' % letter)
            index_by_letter[letter] = pp
            letters.append(letter)

        # sort the list
        letters.sort()

        for thisletter in letters:
            pp = index_by_letter[thisletter]
            info = parts[pp]
            pp_width = info['xhi'] - info['xlo']
            pp_height = info['yhi'] - info['ylo']

            if 'verbose' in self.cfg:
                print '      Part letter: ', thisletter
                print '        part width = ', pp_width
                print '        part height = ', pp_height
                print '        next_x = ', next_x
                print '        next_y = ', next_y

            if pp_width > pg_width:
                print 'Error: Pattern piece <%s> is too wide to print on page width' % pp.name
                # figure out something smarter
                raise

            if next_x + pp_width > pg_width:
                # start a new row
                if 'verbose' in self.cfg:
                    print '        Starting new row, right side of piece would have been = ', next_x + pp_width
                next_y = max_y_this_row + PATTERN_OFFSET
                max_y_this_row = 0
                next_x = 0
            else:
                if pp_height > max_y_this_row:
                    max_y_this_row = pp_height

            # now set up a transform to move this part to next_x, next_y
            xtrans = (next_x - info['xlo'])
            ytrans = (next_y - info['ylo'])
            pp.attrs['transform'] = pp.attrs['transform'] + (' translate(%f,%f)' % (xtrans, ytrans))

            next_x = next_x + pp_width + PATTERN_OFFSET
        if 'verbose' in self.cfg:
            print 'Autolayout END'
        return

    def svg(self):
        self.autolayout()
        return pBase.svg(self)



class PatternPiece(pBase):
    """
    Create an instance of the PatternPiece class, eg jacket.back, pants.frontPocket, corset.stayCover will contain the set of seams and all other pattern piece info,
    eg - jacket.back.seam.shoulder, jacket.back.grainline,  jacket.back.interfacing
    """
    def __init__(self, group, name, letter = '?', fabric = 0, interfacing = 0, lining = 0):
        self.name = name
        self.groupname = group
        self.width = 0
        self.height = 0
        self.labelx = 0
        self.labely = 0
        self.letter = letter
        self.fabric = fabric
        self.interfacing = interfacing
        self.lining = lining
        self.attrs = {}
        self.attrs['transform'] = ''
        pBase.__init__(self)

    def svg(self):
        """
        generate the svg for this item and return it as a pysvg object
        """
        if self.debug:
            print 'svg() called for PatternPiece ID ', self.id

        self.makeLabel()

        # We pass back everything but our layer untouched
        # For our layer, we bundle up all the children's SVG
        # and place it within a group that has our id

        childlist = pBase.svg(self) # returns all children

        for child_group, members in childlist.items():
            #print 'Group ', child_group, ' in PatternPiece->svg'

            my_group = g()

            grpid = self.id + '.' + child_group
            my_group.set_id(grpid)
            for attrname, attrvalue in self.attrs.items():
                my_group.setAttribute(attrname, attrvalue)

            for cgitem in childlist[child_group]:
                my_group.addElement(cgitem)

            # now we replace the list of items in that group that we got
            # from the children with our one svg item, which is a group
            # that contains them all
            my_group_list = []
            my_group_list.append(my_group)
            childlist[child_group] = my_group_list

        return childlist

    def makeLabel(self):
        """
        Create a label block for display on the pattern piece, which contains
        information like pattern number, designer name, logo, etc
        """
        text = []
        mi = self.cfg['metainfo']

        text.append(mi['companyName'])

        text.append('Designer: %s' % mi['designerName'])
        text.append('Client: %s' % self.cfg['clientdata'].customername)
        text.append(mi['patternNumber'])
        text.append('Pattern Piece %s' % self.letter)
        if self.fabric > 0:
            text.append('Cut %d Fabric' % self.fabric)
        if self.interfacing > 0:
            text.append('Cut %d Interfacing' % self.interfacing)

        tb = TextBlock('pattern', 'info', 'Headline', self.label_x, self.label_y, text, 'default_textblock_text_style', 'textblock_box_style')
        self.add(tb)

        return

    def boundingBox(self, grouplist = None):
        """
        Return two points which define a bounding box around the object
        """
        # get all the children
        xmin, ymin, xmax, ymax =  pBase.boundingBox(self, grouplist)
        #print "Pattern BoundingBox before = ", xmin, ymin, xmax, ymax
        xmin, ymin, xmax, ymax =  transformBoundingBox(xmin, ymin, xmax, ymax, self.attrs['transform'])
        #print "Pattern BoundingBox after = ", xmin, ymin, xmax, ymax
        return xmin, ymin, xmax, ymax

class Node(pBase):
    """
    Create an instance which is only intended to be a holder for other objects
    """
    def __init__(self, name):
        self.name = name
        pBase.__init__(self)

class Point(pBase):
    """
    Creates instance of Python class Point
    """
    def __init__(self, group, name, x,  y, styledef = 'default', transform = '') :

        self.groupname = group
        self.name = name
        self.textid = False # for debugging TODO make this available
        self.sdef = styledef
        self.x         = x
        self.y         = y
        self.attrs = {}
        self.attrs['transform'] = transform
        self.size      = 5
        self.coords   = str(x) + "," + str(y)
        pBase.__init__(self)

    def add(self, obj):
        # Points don't have children. If this changes, change the svg and boundingbox methods also.
        raise RuntimeError('The Point class can not have children')

    def svg(self):
        """
        generate the svg for this item and return it as a pysvg object
        """
        if self.debug:
            print 'svg() called for Point ID ', self.id

        # an empty dict to hold our svg elements
        md = self.mkgroupdict()

        pstyle = StyleBuilder(self.styledefs[self.sdef])
        p = circle(self.x, self.y, self.size)
        p.set_style(pstyle.getStyle())
        p.set_id(self.id)
        p.set_onmouseover('ShowTooltip(evt)')
        p.set_onmouseout('HideTooltip(evt)')

        for attrname, attrvalue in self.attrs.items():
            p.setAttribute(attrname, attrvalue)
        md[self.groupname].append(p)

        if self.textid:
            txtlabel = self.id + '.text'
            txttxt = self.name
            txt = self.generateText(self.x+3, self.y, txtlabel, txttxt, 'point_text_style')
            md[self.groupname].append(txt)

        return md

    def boundingBox(self, grouplist = None):
        """
        Return two points which define a bounding box around the object
        """
        if grouplist is None:
            grouplist = self.groups.keys()
        if self.groupname in grouplist:
            return (self.x - (self.size/2), self.y - (self.size/2), self.x + (self.size/2), self.y + (self.size/2))
        else:
            return None, None, None, None

class Line(pBase):
    """
    Creates instance of Python class Line
    """
    def __init__(self, group, name, label, xstart,  ystart, xend, yend, styledef='default', transform = '') :

        self.groupname = group
        self.name = name
        self.sdef = styledef
        self.label = label
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.attrs = {}
        self.attrs['transform'] = transform

        pBase.__init__(self)

    def add(self, obj):
        # Lines don't have children. If this changes, change the svg method also.
        raise RuntimeError('The Line class can not have children')

    def svg(self):
        """
        generate the svg for this item and return it as a pysvg object
        """
        if self.debug:
            print 'svg() called for Line ID ', self.id

        # an empty dict to hold our svg elements
        md = self.mkgroupdict()

        pstyle = StyleBuilder(self.styledefs[self.sdef])
        p = line(self.xstart, self.ystart, self.xend, self.yend)
        p.set_style(pstyle.getStyle())
        p.set_id(self.id)
        for attrname, attrvalue in self.attrs.items():
            p.setAttribute(attrname, attrvalue)
        md[self.groupname].append(p)

        return md

    def boundingBox(self, grouplist = None):
        """
        Return two points which define a bounding box around the object
        """
        if grouplist is None:
            grouplist = self.groups.keys()
        if self.groupname in grouplist:
            return (min(self.xstart, self.xend), min(self.ystart, self.yend), max(self.xstart, self.xend), max(self.ystart, self.yend))
        else:
            return None, None, None, None

class Path(pBase):
    """
    Creates instance of Python class Path
    Holds a path object and applies grouping, styles, etc when drawn
    """
    def __init__(self, group, name, label, pathSVG, styledef = 'default', transform = '') :

        self.groupname = group
        self.name = name
        self.label = label
        self.sdef = styledef
        self.pathSVG = pathSVG
        self.attrs = {}
        self.attrs['transform'] = transform

        pBase.__init__(self)

    def add(self, obj):
        # Paths don't have children. If this changes, change the svg method also.
        raise RuntimeError('The Path class can not have children')

    def svg(self):
        """
        generate the svg for this item and return it as a pysvg object
        """
        if self.debug:
            print 'svg() called for Line ID ', self.id

        try:
            # an empty dict to hold our svg elements
            md = self.mkgroupdict()

            pstyle = StyleBuilder(self.styledefs[self.sdef])

            self.pathSVG.set_id(self.id)
            self.pathSVG.set_style(pstyle.getStyle())
            for attrname, attrvalue in self.attrs.items():
                self.pathSVG.setAttribute(attrname, attrvalue)
            md[self.groupname].append(self.pathSVG)
        except:
            print '************************'
            print 'Exception in element', self.id
            print '************************'
            raise

        return md

    def boundingBox(self, grouplist = None):
        """
        Return two points which define a bounding box around the object
        """
        # This is not elegant, should perhaps be redone
        if grouplist is None:
            grouplist = self.groups.keys()
        if self.groupname in grouplist:
            dd = self.pathSVG.get_d()
            xmin, ymin, xmax, ymax =  boundingBox(dd)
            #print "BoundingBox = ", xmin, ymin, xmax, ymax
            return xmin, ymin, xmax, ymax
        else:
            return None, None, None, None


class TextBlock(pBase):
    """
    Creates instance of Python class TextBlock
    """
    def __init__(self, group, name, headline, x, y, text, textstyledef = 'default_textblock_text_style', boxstyledef = None, transform = ''):
        self.groupname = group
        self.name = name
        self.text = text
        self.textsdef = textstyledef
        self.boxsdef = boxstyledef
        self.headline = headline
        self.x = x
        self.y = y
        self.attrs = {}
        self.attrs['transform'] = transform

        pBase.__init__(self)

    def add(self, obj):
        # Text Blocks don't have children. If this changes, change the svg method also.
        raise RuntimeError('The TextBlock class can not have children')

    def svg(self):
        """
        generate the svg for this item and return it as a pysvg object
        """
        if self.debug:
            print 'svg() called for TextBlock ID ', self.id

        # an empty dict to hold our svg elements
        md = self.mkgroupdict()

        # create the text first
        tg = g()
        tg.set_id(self.id)
        x = self.x
        y = self.y
        # this is a bit cheesy
        spacing  =  ( int(self.styledefs[self.textsdef]['font-size']) * 1.2 )
        line = 1
        for line in self.text:
            label = self.id + '.line' + str(line)
            txt = self.generateText(x, y, label, line, self.textsdef)
            y = y + spacing
            tg.addElement(txt)

        # TODO getting element sizes is note yet supported in pySVG,
        # so we'll do the outline box and headline later
        for attrname, attrvalue in self.attrs.items():
            tg.setAttribute(attrname, attrvalue)
        md[self.groupname].append(tg)

        return md
