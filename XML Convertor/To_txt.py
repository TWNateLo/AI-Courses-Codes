from lxml import etree

def xml_to_txt(xml_file, txt_file):
    # Parse the XML file
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Open the TXT file for writing
    with open(txt_file, 'w', encoding='utf-8') as f:
        # Recursively extract text content from XML
        extract_text(root, f)

def extract_text(element, file_handle):
    # Write the text content of the element if it exists
    if element.text:
        file_handle.write(element.text.strip() + '\n' + '\n')

    # Recurse through child elements
    for child in element:
        extract_text(child, file_handle)

# Example usage
if __name__ == "__main__":
    xml_file = 'FalV_modded_V2.xml'
    txt_file = 'output2.txt'
    xml_to_txt(xml_file, txt_file)