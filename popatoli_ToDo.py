#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/Wmanns/popatoli
#
# popatoli_ToDo.py
#
# pocket-paper-ToDo-list aka 'popatoli'!
#   if you prefer
# paper-pocket-ToDo-list aka 'papotoli'!
#
# Use scribus to create a pocket-paper-ToDo-list.
#
# Not quick but dirty programming!
#
# Works with:
#    Scribus 1.5.4
#
# Parts of this program from scribus documentation
#
# License cc-by-sa-4.0
#
# Scribus has obviously some pecularities when executing Python scrips - at least when executing the script in the terminal:
# - it doesn't like void lines within functions => a void line has to be a comment.
# - it doesn't like tabs (at least no mixture of tabs and spaces).
#

import sys
import os
import ConfigParser  # https://pymotw.com/2/ConfigParser/index.html

try:
    from scribus import *  # I know ...
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

# change to {PAPER_A0 | ... | PAPER_B0 ... | PAPER_C5E | PAPER_EXECUTIVE | PAPER_FOLIO | PAPER_LEDGER | PAPER_LEGAL | PAPER_LETTER | PAPER_TABLOID}
paper_format = PAPER_A4

# Path of text file to import; default is the 'document' path in scribus
# (Scribus vs 1.5.4: File > Preferences > Paths > Documents:'
popatoli_txt_file_path = r"__popatoli_include_text.txt"

def make_document():
    #   play arround with margins to fit page to your printer ...
    newDocument(PAPER_A4, (4.111, 4.111, 4.111, 4.111), LANDSCAPE, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
    setInfo("author", "popatoli", "pocket-paper-ToDo-list")
    lr, rr, tr, br = 0.0, 0.0, 0.0, 0.0
    setMargins(lr, rr, tr, br)
    zoomDocument(-100.0)

def make_folding_lines(pg_height, pg_width):
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
    # vertical lines
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
    objects_list = [hrz_line_1, hrz_line_2, hrz_line_3, vrt_line_1, vrt_line_2, vrt_line_3 ]
    tmp_name = groupObjects(objects_list)
    setNewName("Folding_lines", tmp_name)
    #

def set_Font(text_field):
    setFont("Calibri Bold", text_field)
    fontsize = 44
    setFontSize(fontsize, text_field)

def make_folding_markers(pg_height, pg_width):
    x1, y1 = pg_height // 2 , 5
    out_middle_marker = createText(x1, y1, 30, 30, 'out_middle_marker')  #
    set_Font(out_middle_marker)
    insertText(r" o", -1, out_middle_marker)
    #
    x1, y1 = (pg_height // 4), 10
    in_left_marker = createText(x1, y1, 30, 30, 'in_left_marker')  #
    set_Font(in_left_marker)
    insertText(r" I", -1, in_left_marker)
    #
    x1, y1 = pg_height - (pg_height // 4), 10
    in_right_marker = createText(x1, y1, 30, 30, 'in_right_marker')  #
    set_Font(in_right_marker)
    insertText(r" I", -1, in_right_marker)
    #
    x1, y1 = 0, pg_width // 2
    out_horz_marker = createText(x1, y1, 30, 30, 'out_horz_marker')  #
    set_Font(out_horz_marker)
    insertText(r" o", -1, out_horz_marker)
    #
    tmp_name = groupObjects([out_middle_marker, in_left_marker, in_right_marker, out_horz_marker])
    setNewName("Folding_markers", tmp_name)
    #

def make_single_field(pg_height, pg_width, title_height, title_width, dx, dy):
    """ Each popatoli is made by 8 ToDo-fields; this function makes one of them.
        Each field consists of a title, a text field and some delimiting lines.
        The function returns a list of all elements of this field.
    """
    #
    # Text - Head
    #
    x  = dx + 0 * (pg_height // 4)                # pg_height, pg_width = 842.0 595.0
    y  = dy + pg_width // 2
    #
    title = createText(x, y, title_width, title_height, 'title')  # title
    setFont("Calibri Bold", title)
    font_size = 66
    setFontSize(font_size, title)
    # Underline Text - Head
    title_line = createLine(x + 2, y  + title_height - dy, x - 2 + title_width, y + title_height - dy, 'title_line')  # title_line
    setLineWidth(8, title_line)
    setLineCap(CAP_ROUND, title_line)
    #
    # Text - Body
    #
    dy2 = title_height + (dy // 3) * 2
    body_width  = title_width
    body_height = title_height * 8
    body_height = ((pg_width // 2) * 8 ) // 10
    body = createText(x, y + dy2, body_width, body_height, 'body')  # body
    setFont("Calibri Bold", body)
    font_size = 69
    setFontSize(font_size, body)
    setLineSpacing(font_size, body)
    #
    # insert points
    #
    insertText(r"· ", -1, body)
    for i in range(8):
        insertText("\n· ", -1, body)
    #
    # Text - Body - Corner
    # horizontal line
    #
    setLineWidth_corner = 3
    right_corner_x = x - 2 + title_width
    right_corner_y = y + title_height - dy  + body_height
    right_corner_y = y + title_height       + body_height
    bottom_line_horz = createLine(right_corner_x - 80, right_corner_y , right_corner_x, right_corner_y, 'bottom_line_horz')  # bottom_line: horizontal
    setLineWidth(setLineWidth_corner, bottom_line_horz)
    setLineCap(CAP_ROUND, bottom_line_horz)
    #
    # vertical line
    bottom_line_vert = createLine(right_corner_x, right_corner_y, right_corner_x, right_corner_y - 40, 'bottom_line_vert')  # bottom_line: vertical
    setLineWidth(setLineWidth_corner, bottom_line_vert)
    setLineCap(CAP_ROUND, bottom_line_vert)
    #
    objects_list = [title, title_line, body, bottom_line_horz, bottom_line_vert]
    return objects_list
    #

def set_title(field_name, title_text, objects_list):
    """ set title of a single field """
    #
    selectObject(field_name)
    unGroupObject(field_name)
    selectObject("title")
    insertText(title_text, -1, "title")
    deselectAll()
    tmp_name = groupObjects(objects_list)
    setNewName(field_name, tmp_name)
    #

def clear_text(field_name, objects_list):
    """ clears text of body of a single field """
    selectObject(field_name)
    unGroupObject(field_name)
    deleteText("body")
    deselectAll()
    tmp_name = groupObjects(objects_list)
    setNewName(field_name, tmp_name)
    #

def set_text(field_name, body_text, objects_list):
    """ set text of body of a single field """
    #
    selectObject(field_name)
    unGroupObject(field_name)
    #selectObject("body")
    deleteText("body")
    #
    setFont("Calibri Bold", "body")
    font_size = 40
    setFontSize(font_size, "body")
    setLineSpacing(font_size, "body")
    #
    insertText("\n· " + body_text, -1, "body")
    deselectAll()
    tmp_name = groupObjects(objects_list)
    setNewName(field_name, tmp_name)
    #

def add_text(field_name, body_text, objects_list):
    """ set text of body of a single field """
    #
    selectObject(field_name)
    unGroupObject(field_name)
    #
    setFont("Calibri Bold", "body")
    font_size = 40
    setFontSize(font_size, "body")
    setLineSpacing(font_size, "body")
    #
    insertText("\n· " + body_text, -1, "body")
    deselectAll()
    tmp_name = groupObjects(objects_list)
    setNewName(field_name, tmp_name)
    #

def set_titles(objects_list):
    set_title(field_name="Field_4", title_text="  ToDo", objects_list = objects_list)
    set_title(field_name="Field_7", title_text="  Praxis", objects_list = objects_list)
    set_title(field_name="Field_8", title_text="  Clara", objects_list = objects_list)

def set_texts(objects_list):
    #clear_text('Field_5', objects_list)
    #add_text(field_name="Field_5", body_text="!  Rundsägeblatt", objects_list = objects_list)
    #add_text(field_name="Field_5", body_text="!  Halogenlampe 20 W G9 230 V", objects_list = objects_list)
    #
    parser = ConfigParser.SafeConfigParser()
    exists = os.path.isfile(popatoli_txt_file_path)
    if not exists:
        scribus.messageBox("File does not exist!", popatoli_txt_file_path,scribus.ICON_WARNING,scribus.BUTTON_OK)
        # Store configuration file values
    # else:
        # Keep presets
    parser.read(popatoli_txt_file_path)
    #
    body_str = parser.get('Field_5', 'body')
    clear_text('Field_5', objects_list)
    for substr in body_str.splitlines():
        add_text('Field_5', substr, objects_list)
        pass

def make_folding(pg_height, pg_width):
    make_folding_lines(pg_height, pg_width)
    make_folding_markers(pg_height, pg_width)


def main(argv):
    """This is a documentation string. """
    if haveDoc():
        closeDoc()
    make_document()
    #
    # page_height, page_width = 842.0 595.0  == obwohl horizontal dargestellt: Höhe > Breite !
    pg_height, pg_width = getPageSize()
    title_height = pg_width // 19
    title_width  = ((pg_height // 4) * 93 ) // 100
    dx =  8
    dy = 12
    #
    # make one single ToDo field:
    objects_list = make_single_field(pg_height, pg_width, title_height, title_width, dx, dy)
    # objects_list = [title, title_line_1, body_1, bottom_line_horz, bottom_line_vert]
    #
    # Copy this object 7 times
    #
    tmp_name = groupObjects(objects_list)
    setNewName("Field_1", tmp_name)
    #
    selectObject('Field_1')
    #
    duplicateObject()
    moveObject((pg_height // 4), 0)
    setNewName("Field_2")
    #
    duplicateObject()
    moveObject((pg_height // 4), 0)
    setNewName("Field_3")
    #
    duplicateObject()
    moveObject((pg_height // 4), 0)
    setNewName("Field_4")
    #
    selectObject('Field_1')
    duplicateObject('Field_1')
    rotateObject(180.0)
    moveObject(title_width, 0)
    moveObject(0, -3 * dx)
    setNewName("Field_5")
    #
    duplicateObject()
    moveObject((pg_height // 4), 0)
    setNewName("Field_6")
    #
    duplicateObject()
    moveObject((pg_height // 4), 0)
    setNewName("Field_7")
    #
    duplicateObject()
    moveObject((pg_height // 4), 0)
    setNewName("Field_8")
    #
    setNewName("Field_1", 'Field_1')
    #
    set_titles(objects_list)
    #
    set_texts(objects_list)
    #
    make_folding(pg_height, pg_width)
    #
    # scribus.messageBox("ok","everything ok.",scribus.ICON_WARNING,scribus.BUTTON_OK)
    #


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
