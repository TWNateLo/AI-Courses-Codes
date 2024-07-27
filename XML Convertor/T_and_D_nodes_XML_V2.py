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




def modify_tiaowen_content(root, parent_tag):
    """
    Modify the content of <條文> to merge <編章節>, <條號>, and <條文內容> with custom wording,
    using the <法規名稱> node's value as part of the custom text. Overwrite original <條文> content.
    """
    for parent in root.findall(parent_tag):
        law_name = parent.find('法規名稱').text if parent.find('法規名稱') is not None else ''
        bianzhangjie = parent.find('法規內容/編章節').text if parent.find('法規內容/編章節') is not None else ''

        # Remove all spaces from <編章節> contents
        bianzhangjie_cleaned = bianzhangjie.replace(" ", "")

        for tiaowen in parent.findall('.//條文'):
            tiaohou = tiaowen.find('條號').text if tiaowen.find('條號') is not None else ''
            # Remove all spaces from <編章節> contents
            tiaohou_cleaned = tiaohou.replace(" ", "")
            tiaowen_neirong = tiaowen.find('條文內容').text if tiaowen.find('條文內容') is not None else ''
            
            custom_text = f'依照"{law_name}"{bianzhangjie_cleaned}{tiaohou_cleaned}之規定，{tiaowen_neirong}'
            
            # Overwrite the content of <條文> with custom text
            tiaowen.text = custom_text
            
            # Remove child nodes <條號> and <條文內容>
            for child in list(tiaowen):
                if child.tag in ['條號', '條文內容']:
                    tiaowen.remove(child)

        # Remove the <編章節> node
        for bianzhangjie_node in parent.findall('法規內容/編章節'):
            parent.find('法規內容').remove(bianzhangjie_node)



# Edit the 前言 part into tagged form
def modify_preface_content(root, parent_tag):
    """
    Modify the content of <前言> to remove newline characters and add custom text using the <法規名稱> node.
    """
    for parent in root.findall(parent_tag):
        law_name = parent.find('法規名稱').text if parent.find('法規名稱') is not None else ''
        
        qianyan = parent.find('前言')
        if qianyan is not None and qianyan.text:
            qianyan_text = qianyan.text.replace('\n', '')
            custom_qianyan_text = f'"{law_name}"前言:{qianyan_text}'
            qianyan.text = custom_qianyan_text


# Edit the 沿革 part into tagged form
def modify_Changelog_content(root, parent_tag):
    """
    Modify the content of <前言> to remove newline characters and add custom text using the <法規名稱> node.
    """
    for parent in root.findall(parent_tag):
        law_name = parent.find('法規名稱').text if parent.find('法規名稱') is not None else ''
        
        Changelog = parent.find('沿革內容')
        if Changelog is not None and Changelog.text:
            # If the .txet.replace()
            Changelog_text = Changelog.text.replace(' ', '').replace('\n', '，')
            custom_Changelog_text = f'"{law_name}"沿革內容:{Changelog_text}'
            Changelog.text = custom_Changelog_text



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

    # Modify <條文> content
    modify_tiaowen_content(root, parent_tag)

    # Modify <前言> content
    modify_preface_content(root, parent_tag)

    # Modify <沿革> content
    modify_Changelog_content(root, parent_tag)

    # Write the result to a new XML file
    tree.write(output_xml_file_path, encoding='utf-8', xml_declaration=True)

# Path to the input XML file
input_xml_file_path = 'FalV.xml'

# Path to the output XML file
output_xml_file_path = 'FalV_modded_V2.xml'

# Tags and value to use for removal
parent_tag = '法規'
child_tag = '廢止註記'
value = '廢'
excluded_tags = {"廢止註記", "最新異動日期", "是否英譯註記", "生效日期", "法規類別", "法規性質", "生效內容", "附件"}

# Parse and process the XML file
parse_and_process_xml(input_xml_file_path, output_xml_file_path, parent_tag, child_tag, value, excluded_tags)

print(f"Output XML file saved to {output_xml_file_path}")