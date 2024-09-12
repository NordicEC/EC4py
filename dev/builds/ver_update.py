import toml
import json
from pathlib import Path

def version_updated():
    
    
    # Opening JSON file
    pp = Path(".").cwd()
    pa = pp /"package.json"
    if not pa.exists():
        print(pa)
        pp = pp.parent
        pa = pp /"package.json"
        if not pa.exists():
            pp = pp.parent
            pa = pp /"package.json"
             
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
    
    pyproject = pp /"pyproject.toml"
    with open(pyproject, "r") as f:
        data = toml.load(f)
    print(data)
    data["project"]["version"]=project_version
    with open(pyproject, 'w') as f:
        toml.dump(data, f)
