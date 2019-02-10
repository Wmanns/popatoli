#!/usr/bin/env python
# -*- coding: utf-8 -*-


# popatoli_ToDo.py
#
# pocket-paper-ToDo-list aka 'popatoli'!
# Use with scribus to create a pocket-paper-ToDo-list.
#
# Not quick but really dirty and really bad programming!
#
# Works with: 
#	Scribus 1.5.4 
#	Language German (!)
# 	Ignore error messages.
#
# parts of this program from scribus documentation
#
# License cc-by-sa-4.0

import sys

try:
	# Please do not use 'from scribus import *' . If you must use a 'from import',
	# Do so _after_ the 'import scribus' and only import the names you need, such
	# as commonly used constants.
#	import scribus
	from scribus import *
except ImportError,err:
	print "This Python script is written for the Scribus scripting interface."
	print "It can only be run from within Scribus."
	sys.exit(1)

#########################
# YOUR IMPORTS GO HERE  #
#########################

# change to {PAPER_A0 | ... | PAPER_B0 ... | PAPER_C5E | PAPER_EXECUTIVE | PAPER_FOLIO | PAPER_LEDGER | PAPER_LEGAL | PAPER_LETTER | PAPER_TABLOID}
paper_format = PAPER_A4


def make_document():
#	newDocument(PAPER_A4, (0.0  , 0.0  , 0.0  , 0.0  ), LANDSCAPE, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1) 
#	play arround with marigins to fit size to your printer ...
	newDocument(PAPER_A4, (4.111, 4.111, 4.111, 4.111), LANDSCAPE, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1) 
	setInfo("author", "popatoli", "pocket-paper-ToDo-list")
	lr, rr, tr, br = 0.0, 0.0, 0.0, 0.0
	setMargins(lr, rr, tr, br)
	zoomDocument(-100.0)


def main(argv):
	"""This is a documentation string. """
	if haveDoc():
		closeDoc()
	make_document()
	#
	pg_height, pg_width = getPageSize()   # page_height, page_width = 842.0 595.0  == obwohl horizontal dargestellt: Höhe > Breite !
	#
	line_width = 4
	#
	x1, y1, x2, y2 = pg_height // 4 , 0, pg_height // 4 , pg_width
	hrz_line_1 = createLine(x1, y1, x2, y2, 'hrz_line_1')
	setLineWidth(line_width, 'hrz_line_1') 
	#
	x1, y1, x2, y2 = pg_height // 2 , 0, pg_height // 2 , pg_width
	hrz_line_2 = createLine(x1, y1, x2, y2, 'hrz_line_2')
	setLineWidth(line_width, 'hrz_line_2') 
	#
	x1, y1, x2, y2 = pg_height - (pg_height // 4) , 0, pg_height - (pg_height // 4) , pg_width
	hrz_line_3 = createLine(x1, y1, x2, y2, 'hrz_line_3')
	setLineWidth(line_width, 'hrz_line_3') 
	#
	x1, y1, x2, y2 = 0, pg_width // 2 , pg_height // 4, pg_width // 2
	vrt_line_1 = createLine(x1, y1, x2, y2, 'vrt_line_1')
	setLineWidth(line_width, 'vrt_line_1') 
	#
	x1, y1, x2, y2 = pg_height // 4, pg_width // 2, pg_height - (pg_height // 4), pg_width // 2
	vrt_line_2 = createLine(x1, y1, x2, y2, 'vrt_line_2')
	setLineWidth(line_width, 'vrt_line_2') 
	setLineStyle(LINE_DOT, 'vrt_line_2') 
	#
	x1, y1, x2, y2 = pg_height - (pg_height // 4), pg_width // 2, pg_height , pg_width // 2
	vrt_line_3 = createLine(x1, y1, x2, y2, 'vrt_line_3')
	setLineWidth(line_width, 'vrt_line_3') 
	#
	# Text - Head
	# 
	head_height= pg_width // 19
	head_width = ((pg_height // 4) * 93 ) // 100
	dx = 8
	x  = dx + 0 * (pg_height // 4)                # pg_height, pg_width = 842.0 595.0
	dy = 12
	y  = dy + pg_width // 2
	head_1 = createText(x, y, head_width, head_height, 'head_1')  # head_1
	setFont("Calibri Bold", head_1)
	font_size = 66
	setFontSize(font_size, head_1)
	# insertText("  ToDo", -1, head_1) 
	# Underline Text - Head
	head_line_1 = createLine(x + 2, y  + head_height - dy, x - 2 + head_width, y + head_height - dy, 'head_line_1')  # head_line_1 
	setLineWidth(8, head_line_1) 
	setLineCap(CAP_ROUND, head_line_1) 
	#
	# Text - Body
	#
	dy2 = head_height + (dy // 3) * 2
	body_width  = head_width 
	body_height = head_height * 8
	body_height = ((pg_width // 2) * 8 ) // 10
	body_1 = createText(x, y + dy2, body_width, body_height, 'body_1')  # body_1 
	setFont("Calibri Bold", body_1)
	font_size = 69
	setFontSize(font_size, body_1)
	setLineSpacing(font_size, body_1)
	
	insertText("· ", -1, body_1) 
	for i in range(8):
		# insertText("\n· " + str (i+2), -1, body_1) 
		insertText("\n· ", -1, body_1) 
	#
	# Text - Body - Corner
	# horizontal line
	#
	setLineWidth_corner = 3
	right_corner_x = x - 2 + head_width
	right_corner_y = y + head_height - dy  + body_height
	right_corner_y = y + head_height       + body_height
	bottom_line_horz = createLine(right_corner_x - 80, right_corner_y , right_corner_x, right_corner_y, 'bottom_line_horz')  # bottom_line: horizontal
	setLineWidth(setLineWidth_corner, bottom_line_horz) 
	setLineCap(CAP_ROUND, bottom_line_horz) 
	#
	# vertical line
	bottom_line_vert = createLine(right_corner_x, right_corner_y, right_corner_x, right_corner_y - 40, 'bottom_line_vert')  # bottom_line: vertical
	setLineWidth(setLineWidth_corner, bottom_line_vert) 
	setLineCap(CAP_ROUND, bottom_line_vert) 
	#
	#
	# Copy this object 7 times
	#
	#
	groupObjects([head_1, head_line_1, body_1, bottom_line_horz, bottom_line_vert])
	selectObject('Gruppe1') 
	dpl = duplicateObject()
	moveObject((pg_height // 4), 0)
	#
	selectObject('Gruppe1') 
	dpl = duplicateObject()
	moveObject((pg_height // 4), 0)
	#
	selectObject('Gruppe1') 
	dpl = duplicateObject()
	moveObject((pg_height // 4), 0)
	#
	#
	#
	unGroupObject('Gruppe1')
	selectObject(head_1)
	#insertText("  ToDo", -1, head_1) 
	#
	groupObjects([head_1, head_line_1, body_1, bottom_line_horz, bottom_line_vert])
	selectObject('Gruppe5') 
	dpl = duplicateObject('Gruppe5')
	rotateObject(180.0)
	moveObject(head_width, 0)
	moveObject(0, -3 * dx)
	#
	dpl = duplicateObject()
	moveObject((pg_height // 4), 0)
	#
	dpl = duplicateObject()
	moveObject((pg_height // 4), 0)
	#
	dpl = duplicateObject()
	moveObject((pg_height // 4), 0)
	#
	#
	#
	unGroupObject('Gruppe5')
	selectObject(head_1)
	insertText("  ToDo", -1, head_1) 



def main_wrapper(argv):
	"""The main_wrapper() function disables redrawing, sets a sensible generic
	status bar message, and optionally sets up the progress bar. It then runs
	the main() function. Once everything finishes it cleans up after the main()
	function, making sure everything is sane before the script terminates."""
	try:
		scribus.statusMessage("Running script: popatoli_ToDo.py: begin ")
		scribus.progressReset()
		main(argv)
	finally:
		# Exit neatly even if the script terminated with an exception,
		# so we leave the progress bar and status bar blank and make sure
		# drawing is enabled.
		if scribus.haveDoc():
			scribus.setRedraw(True)
		scribus.statusMessage("popatoli_ToDo.py: end")
		scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.

if __name__ == '__main__':
	main_wrapper(sys.argv)
	
	