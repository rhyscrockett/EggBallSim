import csv
import json

def read_csv(filepath):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(filepath, fieldnames, rows):
    with open(filepath, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def read_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

def write_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)