import xml.etree.ElementTree as ET

# From disk
# Import XML data
tree = ET.parse('FalV.xml')
# Parse the XML data
root = tree.getroot()

## From strings
## root = ET.fromstring(country_data_as_string)


# Function to find and remove nodes with a specific child value
def remove_nodes_with_child_value(root, tag, child_tag, child_value):
    for parent in root.findall(tag):
        child = parent.find(child_tag)
        if child is not None and child.text == child_value:
            root.remove(parent)

# Remove nodes where <廢止註記> contains "廢"
remove_nodes_with_child_value(root, '法規', '廢止註記', '廢')

# Convert the modified XML back to a string
modified_xml = tree = ET.ElementTree(root)
tree.write('FalV_trimmed.xml', encoding='utf-8', xml_declaration=True)

