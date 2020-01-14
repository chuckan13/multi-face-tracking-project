"""
Parses the ground truth .xml files to get coordinates of bounding boxes.
"""
import csv 
import xml.etree.ElementTree as ET 
import track

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    trajectories = []

    for item in root:
        trajectory = []
        for children in item:
            frame = []
            frame.append(children.attrib['x'])
            frame.append(children.attrib['y'])
            frame.append(children.attrib['width'])
            frame.append(children.attrib['height'])
            trajectory.append(frame)
        trajectories.append(trajectory)
    return trajectories

def main(xml_file_path):
    parseXML(xml_file_path)

main()