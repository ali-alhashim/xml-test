
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


from xml.dom.minidom import parse
import re



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



def Canonicalizing(XMLString:str):
    #1- The document is encoded in UTF-8
    TheXML = XMLString.encode('utf-8')

    #2-Line breaks normalized to #xA on input, before parsing
    TheXML = str(TheXML).replace("\\n", "#xA")

    #3- Attribute values are normalized, as if by a validating processor

    #4- Character and parsed entity references are replaced

    #5- CDATA sections are replaced with their character content

    #6- The XML declaration and document type declaration are removed

    TheXML = re.sub("<!--.*-->","",TheXML)
    TheXML = re.sub("<\?xml .*?>","",TheXML)
      
    #8- Whitespace outside of the document element and within start and end tags is normalized
    TheXML = re.sub("\s>",">",TheXML)
    #9- All whitespace in character content is retained (excluding characters removed during line feed normalization)
    TheXML = re.sub("\s\s"," ",TheXML)
    #10- Attribute value delimiters are set to quotation marks (double quotes)
    TheXML = str(TheXML).replace("'", "\"")


    #11- Special characters in attribute values and character content are replaced by character references

    #12 Superfluous namespace declarations are removed from each element

    #13 Default attributes are added to each element

    #14 Fixup of xml:base attributes [C14N-Issues] is performed

    #15 Lexicographic order is imposed on the namespace declarations and attributes of each element
    return TheXML

##############################

print(Canonicalizing(document.toxml()))

#with open("result.xml","w") as fs:
#    fs.write(document.toxml())
# toprettyxml()
#    fs.close()



### pip install signxml
#from lxml import etree
#from signxml import XMLSigner, XMLVerifier

#data_to_sign = "<Test/>"
#cert = open("cert.pem").read()
#key = open("privkey.pem").read()
#root = etree.fromstring(data_to_sign)
#signed_root = XMLSigner().sign(root, key=key, cert=cert)
#verified_data = XMLVerifier().verify(signed_root).signed_xml
