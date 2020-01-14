"""
Generates ground truth frames
"""
import xml.etree.ElementTree as ET

def genFrames():
    with open("GT/Westlife_gt.xml") as file:
        parseXML(file)

def parseXML(xml):

    tree = ET.parse(xml)
    print(tree)