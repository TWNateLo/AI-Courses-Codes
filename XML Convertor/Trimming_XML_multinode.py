import xml.etree.ElementTree as ET

def parse_law_node(law_node):
    """
    Parse the given law node and extract relevant information into a dictionary.
    """
    law_info = {}
    
    law_info['法規性質'] = law_node.findtext('法規性質')
    law_info['法規名稱'] = law_node.findtext('法規名稱')
    law_info['法規網址'] = law_node.findtext('法規網址')
    law_info['法規類別'] = law_node.findtext('法規類別')
    law_info['最新異動日期'] = law_node.findtext('最新異動日期')
    law_info['生效日期'] = law_node.findtext('生效日期')
    law_info['生效內容'] = law_node.findtext('生效內容')
    law_info['廢止註記'] = law_node.findtext('廢止註記')
    law_info['是否英譯註記'] = law_node.findtext('是否英譯註記')
    law_info['英文法規名稱'] = law_node.findtext('英文法規名稱')
    law_info['附件'] = law_node.findtext('附件')
    law_info['沿革內容'] = law_node.findtext('沿革內容')
    law_info['前言'] = law_node.findtext('前言')
    
    return law_info

def create_law_element(law_info):
    """
    Create an XML element for a law from the given dictionary of law information.
    """
    law_element = ET.Element('法規')
    
    for key, value in law_info.items():
        sub_element = ET.SubElement(law_element, key)
        sub_element.text = value
    
    return law_element

def parse_xml_to_dict(xml_file_path):
    """
    Parse the XML file and convert it into a list of dictionaries.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    laws = []
    
    for law_node in root.findall('法規'):
        law_info = parse_law_node(law_node)
        laws.append(law_info)
    
    return laws

def dict_to_xml(laws, output_xml_file_path):
    """
    Convert a list of dictionaries to an XML file.
    """
    root = ET.Element('法規集')
    
    for law_info in laws:
        law_element = create_law_element(law_info)
        root.append(law_element)
    
    tree = ET.ElementTree(root)
    tree.write(output_xml_file_path, encoding='utf-8', xml_declaration=True)

# Path to the input XML file
input_xml_file_path = 'path_to_your_input_file.xml'

# Path to the output XML file
output_xml_file_path = 'path_to_your_output_file.xml'

# Parse the input XML file to a list of dictionaries
laws = parse_xml_to_dict(input_xml_file_path)

# Convert the list of dictionaries to an XML file
dict_to_xml(laws, output_xml_file_path)

print(f"Output XML file saved to {output_xml_file_path}")