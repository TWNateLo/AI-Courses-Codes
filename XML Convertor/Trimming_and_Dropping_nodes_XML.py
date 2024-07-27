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


def modify_law_dets_content(root, parent_tag):
    """
    Modify the content of <條文> to merge <編章節>, <條號>, and <條文內容> with custom wording,
    using the <法規名稱> node's value as part of the custom text.
    """
    for parent in root.findall(parent_tag):
        law_name = parent.find('法規名稱').text if parent.find('法規名稱') is not None else ''
        for law_dets in parent.findall('條文'):
            #chapter might not be good, not so sure
            law_chapter = parent.find('編章節').text if parent.find('編章節') is not None else ''
            law_no = law_dets.find('條號').text if law_dets.find('條號') is not None else ''
            law_dets_cont = law_dets.find('條文內容').text if law_dets.find('條文內容') is not None else ''
            
            custom_text = f'依照"{law_name}"{law_chapter}{law_no}之規定，{law_dets_cont}'
            
            # Modify the content of <條文>
            law_dets.text = custom_text



def modify_tiaowen_content(root, parent_tag):
    """
    Modify the content of <條文> to merge <編章節>, <條號>, and <條文內容> with custom wording,
    using the <法規名稱> node's value as part of the custom text. Overwrite original <條文> content.
    """
    for parent in root.findall(parent_tag):
        law_name = parent.find('法規名稱').text if parent.find('法規名稱') is not None else ''
        for tiaowen in parent.findall('條文'):
            bianzhangjie = parent.find('編章節').text if parent.find('編章節') is not None else ''
            tiaohou = tiaowen.find('條號').text if tiaowen.find('條號') is not None else ''
            tiaowen_neirong = tiaowen.find('條文內容').text if tiaowen.find('條文內容') is not None else ''
            
            custom_text = f'依照"{law_name}"{tiaohou}之規定，{tiaowen_neirong}'
            
            # Overwrite the content of <條文> with custom text
            tiaowen.text = custom_text
            
            # Remove child nodes <條號> and <條文內容>
            for child in list(tiaowen):
                if child.tag in ['條號', '條文內容']:
                    tiaowen.remove(child)


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
    modify_law_dets_content(root, parent_tag)

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
excluded_tags = {"廢止註記", "最新異動日期", "是否英譯註記", "生效日期", "法規類別", "法規性質", "生效內容"}

# Parse and process the XML file
parse_and_process_xml(input_xml_file_path, output_xml_file_path, parent_tag, child_tag, value, excluded_tags)

print(f"Output XML file saved to {output_xml_file_path}")