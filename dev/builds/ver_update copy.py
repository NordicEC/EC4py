import toml
import json
from pathlib import Path

def version_updated():
    
    
    # Opening JSON file
    pa = Path(".").parent /"package.json"
    f = open(pa)

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list

    project_version =data["version"]
    print("Project Version",project_version)
    # Closing file
    f.close()
    
    pyproject = Path(".").parent /"pyproject.toml"
    with open(pyproject, "r") as f:
        data = toml.load(f)
    print(data)
    data["project"]["version"]=project_version
    with open(pyproject, 'w') as f:
        toml.dump(data, f)
