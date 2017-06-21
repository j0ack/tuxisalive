# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Rémi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import xml.dom.minidom
from xml.dom.minidom import Node

"""Example of a structure
exampleStruct = {
    'scene': {
        'header': {
            'name': 'Noname',
            'author': 'Kysoh',
            'version': '0.0.0',
            'description': 'Nodescription',
            'keywords': ['Nokeywords',],
            'length': 0.0,
            'category': 'common',
            'sub_category': 'common'
        },
        'wavs': {
            'count': 0
        },
        'body': {
            'script': {
                'language': 'python',
                'path': 'none'
            }
        }
    }
}
"""

def __insertLeaf(parentNode, textID, textValue, noTypes = False):
    """
    Insert a leaf in a xml structure
    """
    if textID.find("|") != -1:
        textID = textID[:textID.find("|")]
    xmlObj = xml.dom.minidom.Document()
    leafNode = xmlObj.createElement(textID)
    typeStr = str(type(textValue)).replace("<type '", '')
    typeStr = typeStr.replace("'>", '')
    if typeStr == 'str':
        if textValue == "":
            textValue = " "
    if not noTypes:
        leafNode.setAttribute('type', typeStr)
    text = xmlObj.createTextNode(str(textValue))
    leafNode.appendChild(text)
    parentNode.appendChild(leafNode)

def __insertNode(parentNode, nodeID):
    """
    Insert a node in a xml structure
    """
    if nodeID.find("|") != -1:
        nodeID = nodeID[:nodeID.find("|")]
    xmlObj = xml.dom.minidom.Document()
    newNode = xmlObj.createElement(nodeID)
    parentNode.appendChild(newNode)
    return newNode

def structToXML(struct, noTypes = False, xslPath = None):
    """
    Write a xml file from a dict structure
    """
    xmlObj = xml.dom.minidom.Document()
    
    if xslPath != None:
        strD = "type=\"text/xsl\" href=\"%s\"" % xslPath
        xslObj = xmlObj.createProcessingInstruction("xml-stylesheet", strD)
        xmlObj.appendChild(xslObj)

    def nodeStructToNXML(parentNode, nodeStruct):
        keys = nodeStruct.keys()
        keys.sort()
        for key in keys:
            if str(type(nodeStruct[key])) <> "<type 'dict'>":
                __insertLeaf(parentNode,  key, nodeStruct[key], noTypes)
            else:
                newNode = __insertNode(parentNode, key)
                nodeStructToNXML(newNode, nodeStruct[key])

    nodeStructToNXML(xmlObj, struct)
    
    result = xmlObj.toxml()
    xmlObj.unlink()
    del(xmlObj)
        
    return result

def xmlToStruct(xml_path):
    """
    Get a dict structure from a xml file
    """
    struct = {}
    def nodeXMLToStruct(parentNode, nodeStruct):
        for childNode in parentNode.childNodes:
            global lvTmp123
            if childNode.nodeValue == None:
                it = parentNode.getElementsByTagName(childNode.localName)
                if len(it[0].childNodes) > 0:
                    value = it[0].childNodes[0].nodeValue
                else:
                    value = ''
                typeVal = it[0].getAttribute('type')
                name = childNode.localName
                if it[0].getAttribute('type') != '':
                    leafName = name.encode('utf-8','replace')
                    if typeVal == 'str':
                        lvTmp123 = value.encode('utf-8','replace')
                    else:
                        lvTmp123 = ''
                        rTypeStr = 'global lvTmp123\nlvTmp123 = %s' % value
                        exec str(rTypeStr) in globals()
                    nodeStruct[leafName] = lvTmp123
                else:
                    name = name.encode('utf-8','replace')
                    nDict = {}
                    nodeStruct[name] = nDict
                    nodeXMLToStruct(it[0], nodeStruct[name])

    try:
        fXML = open(xml_path, 'rb')
    except IOError:
        return False, struct
    xmlStr = fXML.read()
    fXML.close()
    xmlObj = xml.dom.minidom.parseString(xmlStr)
    nodeXMLToStruct(xmlObj, struct)
    xmlObj.unlink()
    del(xmlObj)
    return True, struct
