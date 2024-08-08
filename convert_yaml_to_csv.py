import yaml
import csv

def yaml_to_csv(yaml_file_path, csv_file_path):
    # Load YAML data
    with open(yaml_file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    
    # Write CSV
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write header
        header = data[0].keys() if data else []
        writer.writerow(header)
        
        # Write rows
        for row in data:
            writer.writerow(row.values())

# Usage
yaml_to_csv('schema.yaml', 'schema.csv')
