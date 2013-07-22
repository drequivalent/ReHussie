#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Homestuck Russian Translation Project
#  <xmpp:homestuck@conference.jabber.ru>
#  dr.Equivalent the Incredible <doctor@equivalent.me>

import urllib
import os.path
import os
import fnmatch

def get_hussies_page(pagenum):
    """Gets a specified page from mspaintadventures.com by specified pagenumber and normalizes Andrew Hussie's EOLs. Returns a string with clean page text, that can be fed to parse_page()"""
    hussieresponse = urllib.urlopen("http://www.mspaintadventures.com/6/" + pagenum + ".txt")
    readhussie = hussieresponse.read()
    return "\n".join(readhussie.splitlines())

def parse_page(text):
    """Parses the page, no matter Andrew Hussie's or Translated. Returns a list, containing the following:
    0. The Caption
    1. Some weird hash
    2. The time this page is created
    3. Links to the visual/interactive content
    4. The text content
    5. The link (links) to the next page (pages)
    It takes a string with page's text as an argument."""
    reslist = text.split("\n###\n")
    dirty = reslist[5]
    reslist[5] = dirty.strip("\nX")
    return reslist

def locate_trans_page(pagenumber, root = os.curdir):
    """Locates an absolute path to the specified page. Takes the full page number, returns the path as a string."""
    pattern = pagenumber + ".txt"    
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            return os.path.join(path, filename)

def get_trans_page_from_path(path):
    """Gets the Translated page from path specified in the argument. Returns a string with the page text, that can be fed to parse_page()."""
    trans_page = open(path)
    return trans_page.read()
        

def get_trans_page(pagenum):
    """Gets the Translated page by specified pagenumber. Returns a string with page text, that can be fed to parse_page()"""
    return get_trans_page_from_path(locate_trans_page(pagenum))

def get_parsed_hussies_page(pagenum):
    """Gets a specified page from mspaintadventures.com by specified pagenumber, normalizes Andrew Hussie's EOLs and feeds it to the parse_page(). Returns a list. For description of the contained data, see parse_page()."""
    return parse_page(get_hussies_page(pagenum))

def get_parsed_trans_page(pagenum):
    """Gets the Translated page from path specified in the argument and feeds it to the parse_page(). Returns a list. For description of the contained data, see parse_page()."""
    return parse_page(get_trans_page(pagenum))

def reset_field(translist, hussielist, fieldnumber):
    """Resets the field of Translated page's parsed list to the value from Andrew Hussie. Takes the Translated page's list, the list from Ahnrew Hussie's page and the number of field to reset. Returns a list with the reset value. For the description of fields and their numbers, see parse_page(). If set to -1, it scratches the whole page."""
    if fieldnumber == -1:
        translist = hussielist
    else:
        translist[fieldnumber] = hussielist[fieldnumber]
    return translist

def assemble_page(parsedlist, markx = True, onlyfilenames = True):
    """Assembles the page from the list given as the argument. Returns a string with page text. Optionally, it can be told not to append the Newline and X symbol. This option is reserved for future use. It also reduces the links in Hussie's page to filenames by default."""
    if markx == True:
        if parsedlist[5] != "":
            parsedlist[5] = parsedlist[5] + "\nX"
        else:
            parsedlist[5] = parsedlist[5] + "X"
    if onlyfilenames == True:
        links = parsedlist[3].split("\n")
        newlinks = []        
        for element in links:
            newlinks.append(element.split('/')[-1])
        parsedlist[3] = "\n".join(newlinks)
    return "\n###\n".join(parsedlist)

def reset_and_assemble(translist, hussielist, fieldnumber, markx = True):
    """Resets the field of Translated page's parsed list to the value from Andrew Hussie and assembles the page. Takes the Translated page's list, the list from Ahnrew Hussie's page and the number of field to reset. Returns a string with page text. For the description of fields and their numbers, see parse_page(). If set to -1, it scratches the whole page. Optionally, it can be told not to append the Newline and X symbol. This option is reserved for future use."""
    return assemble_page(reset_field(translist, hussielist, fieldnumber), markx)

###############################################################
#DANGER ZONE: this thing writes to real files. Handle with care
###############################################################

def write_page(pagenumber, page):
    """Writes the assembled page into the Translated page's file. Takes a page number and a string with page's text. Returns nothing, but writes into file."""
    trans_page = open(locate_trans_page(pagenumber), "w")
    trans_page.write(page)
    trans_page.close()

###############################################################
#SUPER DANGER ZONE: this should be only used by cli parser
###############################################################

def run_page_reset(pagenumber, fieldnumber):
    """Just a function that kicks the whole thing into action. Takes a number of page and number of field to reset. Returns nothing."""
    pdtrans = get_parsed_trans_page(pagenumber)
    pdhussie = get_parsed_hussies_page(pagenumber)
    newpagetext = reset_and_assemble(pdtrans, pdhussie, fieldnumber)
    write_page (pagenumber, newpagetext)
    

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(prog = 'rehussie', description = 'ReHussie: An emergency tool for resetting the Homestuck Translation Project\nfiles fields to their original values from MS Paint Adventures website.\nFor example:\n> rehussie link 001959\nwill reset a link to the next page on the page number 001959.\nIn order for it to work, you must be in the root directory of the repository.', formatter_class=argparse.RawTextHelpFormatter, epilog = 'COPYRIGHT NOTICE: MS Paint Adventures website and Homestuck belong to Andrew Hussie\nand MS Paint Adventures team. The author of this program makes\nabsolutely no profit from it, and distributes it freely. Anyone can grab it\nand do pretty much what they desire with it, within pretty broad limits of the GPL\nlicense.\nMade with love by dr. Equivalent the Incredible II and the Homestuck (Russian)\nTranslation Project.')
    
    parser.add_argument("field", choices = ["caption", "hash", "time", "images", "text", "link", "all"], metavar = "field", help = "choose a field to reset. May be set to 'caption', 'hash', 'time',\n'images', 'text', 'link', 'all'. If set to 'all', resets all fields")
    parser.add_argument("page", nargs = "+", help = "full 6-digit number or numbers of page or pages to reset")
    args = parser.parse_args()
    if args.field == "all":
        fieldnumber = -1
    elif args.field == "caption":
        fieldnumber = 0
    elif args.field == "hash":
        fieldnumber = 1
    elif args.field == "time":
        filednumber = 2
    elif args.field == "images":
        fieldnumber = 3
    elif args.field == "text":
        fieldnumber = 4
    elif args.field == "link":
        fieldnumber = 5
    for element in args.page:
        try:        
            run_page_reset(element, fieldnumber)
        except TypeError:
            sys.stderr.write("rehussie: 404: Make sure that the page "+ element +" actually exists or if you are actually in a Homestuck Translation Project repository. \n")
