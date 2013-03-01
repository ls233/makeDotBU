from gvgen import *
import string
#import rgbTr.py
import math

def floatRgb(mag, cmin, cmax):
    """
    Return a tuple of floats between 0 and 1 for the red, green and
    blue amplitudes.
    """

    try:
        # normalize to [0,1]
        x = float(mag - cmin) / float(cmax - cmin)
    except:
        # cmax = cmin
        x = 0.5
    blue = min((max((4 * (0.75 - x), 0.)), 1.))
    red = min((max((4 * (x - 0.25), 0.)), 1.))
    green = min((max((4 * math.fabs(x - 0.5) - 1., 0.)), 1.))
    return (red, green, blue)
   
def rgb(mag, cmin, cmax):
    """
    Return a tuple of integers.
    """

    red, green, blue = floatRgb(mag, cmin, cmax)
    return (int(red * 255), int(green * 255), int(blue * 255))
   
def htmlRgb(mag, cmin, cmax):
    """
    Return the rgb representation for html
    """
    
    return "#%02x%02x%02x" % rgb(mag, cmin, cmax)
    
def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def str2num(s):
    """ convert string to int """
    
    return "." in s and float(s) or int(s)

def sortedDictValues1(adict):
    """ returnes values of a dict sorted """
    
    items = adict.items()
    items.sort()
    return [value for value in items]

def _rstrip(line, JUNK='\n \t'):
    """Return line stripped of trailing spaces, tabs, newlines.

    Note that line.rstrip() instead also strips sundry control characters,
    but at least one known Emacs user expects to keep junk like that, not
    mentioning Barry by name or anything <wink>.
    """

    i = len(line)
    while i > 0 and line[i - 1] in JUNK:
        i -= 1
    return line[:i]

def add_pr_link(graph, name1, name2, nodes):
    """ adds forward links to graph
    
    Note the click event is appended """
    mylink = graph.newLink(nodes[name1], nodes[name2])
    graph.propertyAppend(mylink, "label", name1)
    graph.propertyAppend(mylink, "name", "edge")
    graph.propertyAppend(mylink, "fontcolor", "none")        
    graph.propertyAppend(mylink, "URL", "javascript:top.onClick=alert('info about...')")
    graph.styleApply('fLink', mylink)

def add_prb_link(graph, name1, name2, nodes):
    """ adds back links to graph """
    mylink = graph.newLink(nodes[name1], nodes[name2])
    graph.styleApply('bLink', mylink)    

def add_Dpr_link(graph, name1, name2, nodes):
    """ adds bi links to graph """    
    mylink = graph.newLink(nodes[name2], nodes[name1])
    graph.styleApply('BiLink', mylink)    
    mylink1 = graph.newLink(nodes[name1], nodes[name2])
    graph.styleApply('BiLink', mylink1)    
    
def addTohashOfArrays(adict, time, name):
    adict.setdefault(time, []).append(name)
def addEntry(adict, time, name):
    adict[time] = name

def main():        
    disp = { 'pr': add_pr_link,
          'Dpr': add_prb_link,
          'prb': add_prb_link}
    
    theEntries = {}
    #f = open('tempa_output/up_NDV_005_hmc_2.8_0.05_time', 'r')
    f = open('tempa_output1/up_MV_1_hmc_2.8_2link_0.05_time', 'r')
    for line in f:
            if 'TimeActive' in line:
                continue
    #        line = line.rstrip()
            name, sep, time = line.partition('=')    
            time.strip()               
            time = _rstrip(time)
            i = string.index(time, 'hours')
            ns = time[0:i]    
            ns.strip()
            time = str2num(ns)   
            name = _rstrip(name)        
            addTohashOfArrays(theEntries, time, name);
    f.close()
    
    theLebels = {}
    #f = open('tempa_output/up_NDV_005_hmc_2.8_0.05_labels', 'r')
    f = open('tempa_output1/up_MV_1_hmc_2.8_2link_0.05_labels', 'r')
    for line in f:
            name, sep, time = line.partition('=')    
            name = name.strip()
            time = time.strip()
            time = _rstrip(time)
            addEntry(theLebels, name, time);
    f.close()
    
    theSizes = {}
    maxSize = 0
    minSize = 10000
    f = open('tempa_output1/up_MV_1_hmc_2.8_2link_0.05_size', 'r')
    for line in f:
            if 'NodeSize' in line:
                continue   
            name, sep, time = line.partition('=')    
            name = name.strip()
            time = time.strip()
            time = _rstrip(time)
            time = str2num(time)             
            addEntry(theSizes, name, time);
            if time > maxSize:
                maxSize = time 
            if time < minSize:
                minSize = time 
     
    f.close()
    
    theColors = {}
    for key, values in theSizes.items():
        color = htmlRgb (values, minSize, maxSize)
        addEntry(theColors, key, color);
    #print theEntries        
            
    graph = GvGen('Here is a title hold place')
    graph.styleDefaultAppend("color", "Black")
    graph.smart_mode = 1
    graph.styleAppend("clustLabal", "shape", "none")
    graph.styleAppend("TFInf", "shape", "diamond")
    graph.styleAppend("fLink", "color", "#6bfd6b")
    graph.styleAppend("bLink", "color", "#fb7780")
    #graph.styleAppend("bLink", "color", "#fb7780")
    graph.styleAppend("BiLink", "color", "black")
    
    nodes = {}
    i = 2
    sortedEntries = sorted(theEntries.items())
    '''
    for key, values in theEntries.items():
            cl1 = graph.newItem('')
            graph.propertyAppend(cl1, "style",'filled')        
            graph.propertyAppend(cl1, "color",'#eff7ff')        
            j=-1
            labelNode=graph.newItem(`key`+ ' hours',cl1)
            pos=`i`+','+`j`;
            graph.propertyAppend(labelNode, "pos",pos)
            graph.styleApply("clustLabal", labelNode)        
            j-=1
       '''
    for entry in sortedEntries:
            cl1 = graph.newItem('')
            graph.propertyAppend(cl1, "style", 'filled')        
            graph.propertyAppend(cl1, "color", '#eff7ff')        
            j = -1
            labelNode = graph.newItem(`entry[0]` + ' hours', cl1)
            pos = `i` + ',' + `j`;
            graph.propertyAppend(labelNode, "pos", pos)
            graph.styleApply("clustLabal", labelNode)        
            j -= 1
            
            for val in entry[1]:
                    nodes[val] = graph.newItem(val, cl1)
                    pos = `i` + ',' + `j`;
                    graph.propertyAppend(nodes[val], "pos", pos)
                    graph.propertyAppend(nodes[val], "URL", "javascript:top.onClick=showEdgeLabels(" + `val` + ")")                               
                    graph.styleAppend("node", "color", "none")
                    graph.styleAppend("node", "fillcolor", '#ccccff')                
                    graph.styleAppend("node", "style", "filled")               
                    graph.styleApply("node", nodes[val])
                                         
                    j -= 1
            i += 2
                                
    graph.dot()
    

if __name__ == '__main__':
    main()
