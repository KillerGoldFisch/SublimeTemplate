#!/usr/bin/env python

import sublime, sublime_plugin, re, template, djencoding

global selections
selections = []
global viewport
viewport = None#sublime.active_window().active_view().viewport_position()


def isTemplateView(view):
    return (view.file_name().endswith(".t"))

def saveSelection():
    global selections
    selections = [[item.a, item.b] for item in sublime.active_window().active_view().sel()]
    global viewport
    viewport = sublime.active_window().active_view().viewport_position()
    #print "Viewport: "+str(viewport)

def restoreSelection():
    global selections
    sublime.active_window().active_view().sel().clear()
    for item in selections:
        region = sublime.Region(item[0], item[1])
        sublime.active_window().active_view().sel().add(region)
        sublime.active_window().active_view().show_at_center(region)
    global viewport
    sublime.active_window().active_view().set_viewport_position(viewport)
    #print "Viewport: "+str(viewport)

def getFullRegion(view):
    return sublime.Region(0, view.size())

def readLines(view):
    region = getFullRegion(view)
    text = view.substr(region)
    line_endings = "\n" #view.line_endings()
    return text.split(line_endings)

def readText(view):
    region = getFullRegion(view)
    text = view.substr(region)
    return text

def writeLines(view, edit, lines):
    region = getFullRegion(view)
    line_endings = "\n" #view.line_endings()
    text = line_endings.join(lines)
    view.replace(edit, region, text)

def newViewWithContent(content):
    x = sublime.active_window().new_file()
    edit = x.begin_edit() 
    x.insert(edit, 0, content)
    x.end_edit(edit)
    return x
	
def enc(s):
    return djencoding.smart_str(s)

def render(view):
    return template.render(content=enc(readText(view))).decode('utf-8')

def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
