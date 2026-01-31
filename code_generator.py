#!/usr/bin/env python3
"""
Soccer Model to Java Code Generator

This script implements a translation algorithm that reads Entity-Relationship models 
from draw.io XML files and generates corresponding Java source code. It handles:
- Entity extraction
- Inheritance relationships
- Associations/Relationships (1:1, 1:*, etc.)
- Java class generation with getters, setters, and constructors
"""

import xml.etree.ElementTree as ET
import re
import os
from typing import Dict, List, Tuple, Optional


class Entity:
    """
    Represents a class/entity in the model.
    
    Attributes:
        id (str): The unique identifier from the XML.
        name (str): The name of the entity (class name).
        parent (Optional[str]): The name of the parent class if this entity inherits from another.
        fields (List[Dict]): A list of fields/attributes representing relationships.
        children (List[str]): Names of child classes that inherit from this entity.
    """
    def __init__(self, entity_id: str, name: str):
        """
        Initialize an Entity.

        Args:
            entity_id: Unique descriptor for the entity.
            name: Human-readable name of the entity.
        """
        self.id = entity_id
        self.name = name
        self.parent: Optional[str] = None
        self.fields: List[Dict] = []
        self.children: List[str] = []


class Relationship:
    """
    Represents a relationship between two entities.
    
    Attributes:
        source_id (str): ID of the source entity.
        target_id (str): ID of the target entity.
        label (str): Raw label text from the edge.
        is_inheritance (bool): True if this represents an inheritance (is-a) relationship.
        relationship_name (str): Parsed name of the relationship.
        cardinality (str): Parsed cardinality (e.g., "1 : *").
    """
    def __init__(self, source_id: str, target_id: str, label: str, is_inheritance: bool = False):
        """
        Initialize a Relationship.

        Args:
            source_id: ID of the source entity.
            target_id: ID of the target entity.
            label: Text label on the connector.
            is_inheritance: Whether this is an inheritance arrow.
        """
        self.source_id = source_id
        self.target_id = target_id
        self.label = label
        self.is_inheritance = is_inheritance
        self.relationship_name = ""
        self.cardinality = ""
        self._parse_label()

    
    def _parse_label(self):
        """
        Extracts the relationship name and cardinality from the raw label.
        
        Expected format: "Name \n Cardinality" (e.g., "has \n 1 : *")
        """
        if self.label and '\n' in self.label:
            parts = self.label.split('\n')
            self.relationship_name = parts[0].strip() if len(parts) > 0 else ""
            self.cardinality = parts[1].strip() if len(parts) > 1 else "1 : 1"


        else:
            self.relationship_name = self.label.strip() if self.label else "related"
            self.cardinality = "1 : 1"


class ModelToJavaGenerator:
    """
    Main class for the code generator logic.
    
    Attributes:
        xml_file (str): Path to the input XML file.
        entities (Dict[str, Entity]): Map of ID to Entity objects.
        relationships (List[Relationship]): List of association relationships.
        inheritance_relations (List[Relationship]): List of inheritance relationships.
    """
    
    def __init__(self, xml_file: str):
        """
        Initialize the generator.

        Args:
            xml_file: Path to the draw.io XML file.
        """
        self.xml_file = xml_file
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.inheritance_relations: List[Relationship] = []
    
    def parse_model(self):
        """
        Parses the draw.io XML file to extract entities and relationships.
        
        This method scans the XML for 'mxCell' elements, differentiating between
        entity nodes (rectangles) and relationship edges (arrows).
        """
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
        """
        Links entities based on inheritance relationships.
        
        Updates the 'parent' attribute of child entities and the 'children' list
        of parent entities.
        """
        for rel in self.inheritance_relations:
            if rel.source_id in self.entities and rel.target_id in self.entities:
                child = self.entities[rel.source_id]
                parent = self.entities[rel.target_id]
                child.parent = parent.name
                parent.children.append(child.name)
                print(f"Inheritance: {child.name} extends {parent.name}")
    
    def process_associations(self):
        """
        Converts association relationships into fields within the entities.
        
        For each relationship, a field is added to the source entity using the
        target entity's type, based on the specified cardinality.
        """
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
    
    def to_camel_case(self, text: str) -> str:
        """
        Converts a string to camelCase.

        Args:
            text: The input string (e.g., "hello_world" or "Hello World").

        Returns:
            The string in camelCase (e.g., "helloWorld").
        """
        text = text.replace('_', ' ').replace('-', ' ') #turn underscores and hyphens into spaces
        words = text.split() #split into words
        if not words:
            return "field"
        #keep first word lowercase and the rest capitalized
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    def determine_type(self, target_class: str, cardinality: str) -> str:
        """
        Determines the Java type for a relationship field based on cardinality.

        Args:
            target_class: The class name of the target entity.
            cardinality: The cardinality string (e.g., "1 : *").

        Returns:
            The Java type string (e.g., "List<Target>" or "Target").
        """
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
        """
        Generates the Java source code for a single entity.

        Args:
            entity: The Entity object to generate code for.

        Returns:
            A string containing the complete Java class definition.
        """
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
        """
        Generates and saves Java files for all parsed entities.

        Args:
            output_dir: The directory where Java files should be saved.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for entity_id, entity in self.entities.items(): #iterate over all entities
            java_code = self.generate_java_class(entity)
            filename = os.path.join(output_dir, f"{entity.name}.java")
            
            with open(filename, 'w') as f:
                f.write(java_code)
            
            print(f"Generated: {filename}")
    
    def run(self, output_dir: str):
        """
        Executes the full generation pipeline.

        Args:
            output_dir: The target directory for the generated code.
        """
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
    """
    Main entry point for the CLI.
    Parses command line arguments and initiates the generation process.
    """
    import sys
    
    if len(sys.argv) >= 3: #checks for command line arguments
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        #default soccer example
        input_file = "examples/default/model_soccer.drawio"
        output_dir = "examples/default/src-gen"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return
    
    generator = ModelToJavaGenerator(input_file)
    generator.run(output_dir)


if __name__ == "__main__":
    main()
