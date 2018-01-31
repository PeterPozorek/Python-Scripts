# this creates random branching lines with recursion
# input type: line - Line (Item Access), div - int (Item Access)
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import random
import math

def recursiveLine(line, depth, axis, resultList):
    pt1 = line.PointAt(0)
    pt2 = line.PointAt(1)
    dir0 = pt2 - pt1
    dir1 = rg.Vector3d(dir0) # copy
    dir2 = rg.Vector3d(dir0) # copy
    dir1.Rotate(math.pi/2, axis)
    dir1.Rotate(math.pi/2, dir0)
    dir2.Rotate(-math.pi/2, axis)
    dir2.Rotate(math.pi/2, dir0)
    dir1 *= random.random()*0.2 + 0.7; # random scale
    dir2 *= random.random()*0.2 + 0.7;
    line1 = rg.Line(pt2, pt2+dir1)
    line2 = rg.Line(pt2, pt2+dir2)
    resultList.append(line1)
    resultList.append(line2)
    axis = rg.Vector3d.CrossProduct(dir0,dir1)
    axis.Unitize()
    box = rg.Box(rg.Plane.WorldXY, [pt1, pt2, pt2+dir1, pt2+dir2, pt2+axis*dir1.Length/2])
    resultList.append(box)
    if(depth>0):
        if(random.random()<0.9): # random omission
            
            recursiveLine(line1, depth-1, axis, resultList)
        if(random.random()<0.8): # random omission
            #axis = rg.Vector3d.CrossProduct(dir0,dir2)
            recursiveLine(line2, depth-1, axis, resultList)

a = []
recursiveLine(line, div, rg.Vector3d.ZAxis, a)