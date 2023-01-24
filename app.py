
####
    #    1. Remove the 
    #    <Invoice><ext:UBLExtensions/>
    #     block 
    #    2. Remove the 
    #    <invoice><cac:Additional
    #    DocumentReference/> 
    #    block where <cbc:ID/> = 
    #    QR 
    #    3. Remove the 
    #    <invoice><cac:Signature/> 
    #    block  
    #    4. Canonicalize the Invoice 
    #    using the C14N11 
    #    standard 
    #   5. Hash the resulting string 
    #   using SHA256 to a binary 
    #   object 
    #   6. Base64 encode the binary 
    #   object to generate the 
    #   digest value 
    #
    #
    ####

from io import StringIO
from xml.dom.minidom import parse
import lxml.etree as ET
##############################################################
def xmlRemoveElement(elementName:str):
    nodes = document.getElementsByTagName(elementName)
    for node in nodes:
        parent = node.parentNode
        parent.removeChild(node) 
###############################################################
document = parse('invoice.xml')


xmlRemoveElement("ext:UBLExtensions")

##  Next Step find the Element cac:AdditionalDocumentReference and has Child cbc:ID with text QR
##  <cac:AdditionalDocumentReference>
##       <cbc:ID>QR</cbc:ID>
##
##

nodes = document.getElementsByTagName("cac:AdditionalDocumentReference")

for node in nodes:
     nodeX = node.getElementsByTagName("cbc:ID")
     if nodeX[0].firstChild.nodeValue =="QR":
        parent = node.parentNode
        parent.removeChild(node) 
        break


## next step remove cac:Signature
xmlRemoveElement("cac:Signature")


#print(document.toxml())

## XML Canonicalization C14N11

et = ET.parse(document.toxml())
output = StringIO.StringIO()
et.write_c14n(output)
print(output.getvalue())





#with open("result.xml","w") as fs:
#    fs.write(document.toxml())
#    fs.close()
