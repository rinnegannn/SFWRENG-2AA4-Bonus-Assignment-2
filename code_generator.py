#!/usr/bin/env python3
"""
This is a soccer model to Java code generator.
This generator implements the translation algorithm,
reads from the draw.io XML files and generates Java source code.
"""

import xml.etree.ElementTree as ET
import re
import os
from typing import Dict, List, Tuple, Optional


class Entity:
    """represents a class/entity in the model"""
    def __init__(self, entity_id: str, name: str):
        self.id = entity_id
        self.name = name
        self.parent: Optional[str] = None
        self.fields: List[Dict] = []
        self.children: List[str] = []


class Relationship:
    """represents relationship between entities"""
    def __init__(self, source_id: str, target_id: str, label: str, is_inheritance: bool = False):
        self.source_id = source_id
        self.target_id = target_id
        self.label = label
        self.is_inheritance = is_inheritance
        self.relationship_name = ""
        self.cardinality = ""
        self._parse_label()

    
    def _parse_label(self):
        """extracts the relationship name and cardinality from the label"""
        if self.label and '\n' in self.label:
            parts = self.label.split('\n')
            self.relationship_name = parts[0].strip() if len(parts) > 0 else ""
            self.cardinality = parts[1].strip() if len(parts) > 1 else "1 : 1"


        else:
            self.relationship_name = self.label.strip() if self.label else "related"
            self.cardinality = "1 : 1"


class ModelToJavaGenerator:
    """main class for code generator"""
    
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.inheritance_relations: List[Relationship] = []
    
    def parse_model(self):
        """parse the draw.io XML file and extract entities and relationships"""
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        
        cells = root.findall(".//mxCell") #finds all mxCell elements in the XML file
        
        # extract the rectangles with values as entities
        for cell in cells:
            cell_id = cell.get('id')
            value = cell.get('value')
            style = cell.get('style', '')
            
            #check for entity ( if it has a value and is a rectangle)
            if value and 'whiteSpace=wrap' in style and cell_id:

                #remove any HTML tags if present
                clean_value = re.sub(r'<[^>]+>', '', value).strip()
                if clean_value and clean_value not in ['0', '1']:  #skip over root cells
                    entity = Entity(cell_id, clean_value)
                    self.entities[cell_id] = entity
                    print(f"Found entity: {clean_value} (ID: {cell_id})")
        
        #make a map of edge labels
        edge_labels = {}
        for cell in cells:
            parent_id = cell.get('parent')
            value = cell.get('value', '')
            style = cell.get('style', '')
            
            #check for edge label (if it has parent and is an edgeLabel)
            if parent_id and 'edgeLabel' in style and value:
                clean_label = re.sub(r'<[^>]+>', '', value).strip()
                #clean up HTML entities
                clean_label = clean_label.replace('&#xa;', '\n')
                edge_labels[parent_id] = clean_label
        
        # extract arrows/edges as relationships
        for cell in cells:
            source_id = cell.get('source')
            target_id = cell.get('target')
            cell_id = cell.get('id')
            style = cell.get('style', '')
            value = cell.get('value', '')
            
            if source_id and target_id:
                #check for inheritance relationship (empty triangle arrow)
                is_inheritance = 'endArrow=block' in style and 'endFill=0' in style
                
                #get edge label from the map
                edge_label = edge_labels.get(cell_id, "")
                
                #check the edge label for value
                if not edge_label and value:
                    edge_label = re.sub(r'<[^>]+>', '', value).strip()
                
                #create relationship object
                relationship = Relationship(source_id, target_id, edge_label, is_inheritance)
                
                #store relationships
                if is_inheritance:
                    self.inheritance_relations.append(relationship)
                    print(f"Found inheritance: {source_id} -> {target_id}")
                else:
                    self.relationships.append(relationship)
                    print(f"Found relationship: {source_id} -> {target_id} ({edge_label})")
    
    def process_inheritance(self):

        """process inheritance relationships"""
        for rel in self.inheritance_relations:
            if rel.source_id in self.entities and rel.target_id in self.entities:
                child = self.entities[rel.source_id]
                parent = self.entities[rel.target_id]
                child.parent = parent.name
                parent.children.append(child.name)
                print(f"Inheritance: {child.name} extends {parent.name}")
    
    def process_associations(self):

        """process association relationships and create fields"""
        for rel in self.relationships:
            if rel.source_id in self.entities and rel.target_id in self.entities:
                source_entity = self.entities[rel.source_id]
                target_entity = self.entities[rel.target_id]
                
                field_name = self.to_camel_case(rel.relationship_name) if rel.relationship_name else "related"
                field_type = self.determine_type(target_entity.name, rel.cardinality)
                
                field = {
                    'name': field_name,
                    'type': field_type,
                    'target_class': target_entity.name,
                    'cardinality': rel.cardinality
                }
                
                source_entity.fields.append(field)
                print(f"Field: {source_entity.name}.{field_name} : {field_type}")
    
    def turn_into_camelCase(self, text: str) -> str:
        """turns text into camelCase"""
        text = text.replace('_', ' ').replace('-', ' ') #turn underscores and hyphens into spaces
        words = text.split() #split into words
        if not words:
            return "field"
        #keep first word lowercase and the rest capitalized
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    def determine_type(self, target_class: str, cardinality: str) -> str:
        """determine type based on cardinality"""
        parts = cardinality.split(':') #split into source and target parts
        if len(parts) != 2:
            return target_class
        
        source_card = parts[0].strip()
        target_card = parts[1].strip()
        
        #check the cardinality/what we're storing
        if target_card == '*':
            return f"List<{target_class}>"
        elif target_card == '1':
            return target_class
        elif target_card.isdigit():
            #use array for fixed number
            return f"{target_class}[]"
        else:
            return target_class
    
    def generate_java_class(self, entity: Entity) -> str:
        """generate Java source code for entity"""
        code = []
        
        #check if we need to import List
        needs_list = any('List<' in field['type'] for field in entity.fields)
        
        if needs_list:
            code.append("import java.util.List;")
            code.append("import java.util.ArrayList;")
            code.append("")
        
        #declare class
        class_decl = f"public class {entity.name}"
        if entity.parent:
            class_decl += f" extends {entity.parent}"
        class_decl += " {"
        code.append(class_decl)
        code.append("")
        
        #fields
        if entity.fields:
            for field in entity.fields:
                code.append(f"    private {field['type']} {field['name']};")
            code.append("")
        
        #constructor
        code.append(f"    public {entity.name}() {{")
        #init collections
        for field in entity.fields:
            if 'List<' in field['type']:
                code.append(f"        this.{field['name']} = new ArrayList<>();")
        code.append("    }")
        code.append("")
        
        #getters and setters
        for field in entity.fields:
            #getter
            getter_name = f"get{field['name'][0].upper()}{field['name'][1:]}"
            code.append(f"    public {field['type']} {getter_name}() {{")
            code.append(f"        return this.{field['name']};")
            code.append("    }")
            code.append("")
            
            #setter
            setter_name = f"set{field['name'][0].upper()}{field['name'][1:]}"
            code.append(f"    public void {setter_name}({field['type']} {field['name']}) {{")
            code.append(f"        this.{field['name']} = {field['name']};")
            code.append("    }")
            code.append("")
        
        code.append("}")
        
        return '\n'.join(code)
    
    def generate_all_classes(self, output_dir: str):
        """generate the Java files for every entity"""
        os.makedirs(output_dir, exist_ok=True)
        
        for entity_id, entity in self.entities.items(): #iterate over all entities
            java_code = self.generate_java_class(entity)
            filename = os.path.join(output_dir, f"{entity.name}.java")
            
            with open(filename, 'w') as f:
                f.write(java_code)
            
            print(f"Generated: {filename}")
    
    def run(self, output_dir: str):
        """Main method for execution"""
        print("=" * 60)
        print("//Demo: Soccer Model to Java Code Generator//")
        print("=" * 60)
        print()
        
        print("- Parsing model")
        self.parse_model()
        print(f"Found {len(self.entities)} entities")
        print()
        
        print("- Processing inheritance")
        self.process_inheritance()
        print()
        
        print("- Processing relationships")
        self.process_associations()
        print()
        
        print("- Generating Java classes")
        self.generate_all_classes(output_dir)
        print()
        
        print("=" * 60)
        print(f"Finished generating. Output: {output_dir}")
        print("=" * 60)


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) >= 3: #checks for command line arguments
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        #default soccer example
        input_file = "model_soccer.drawio"
        output_dir = "examples/default/src-gen"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return
    
    generator = ModelToJavaGenerator(input_file)
    generator.run(output_dir)


if __name__ == "__main__":
    main()
