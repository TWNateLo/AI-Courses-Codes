import xml.etree.ElementTree as ET

def remove_nodes_with_child_value(root, parent_tag, child_tag, value):
    """
    Remove parent nodes that have a child node with a specific value. (remove parents with specific value "廢止")
    """
    parents_to_remove = []
    
    for parent in root.findall(parent_tag):
        for child in parent.findall(child_tag):
            if child.text == value:
                parents_to_remove.append(parent)
                break
    
    for parent in parents_to_remove:
        root.remove(parent)

def remove_specific_child_nodes(root, parent_tag, excluded_tags):
    """
    Remove specific child nodes from parent nodes.
    """
    for parent in root.findall(parent_tag):
        for child in list(parent):
            if child.tag in excluded_tags:
                parent.remove(child)

def parse_and_process_xml(input_xml_file_path, output_xml_file_path, parent_tag, child_tag, value, excluded_tags):
    """
    Parse the XML file, process it to remove specific nodes and child nodes, and write to a new XML file.
    """
    tree = ET.parse(input_xml_file_path)
    root = tree.getroot()
    
    # Remove nodes with specific child value
    remove_nodes_with_child_value(root, parent_tag, child_tag, value)
    
    # Remove specific child nodes
    remove_specific_child_nodes(root, parent_tag, excluded_tags)
    
    # Write the result to a new XML file
    tree.write(output_xml_file_path, encoding='utf-8', xml_declaration=True)

# Path to the input XML file
input_xml_file_path = 'FalV.xml'

# Path to the output XML file
output_xml_file_path = 'FalV_modded.xml'

# Tags and value to use for removal
parent_tag = '法規'
child_tag = '廢止註記'
value = '廢'
excluded_tags = {"廢止註記", "最新異動日期", "是否英譯註記", "生效日期", "法規類別", "法規性質"}

# Parse and process the XML file
parse_and_process_xml(input_xml_file_path, output_xml_file_path, parent_tag, child_tag, value, excluded_tags)

print(f"Output XML file saved to {output_xml_file_path}")