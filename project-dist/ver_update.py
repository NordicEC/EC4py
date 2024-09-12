import toml
import json
from pathlib import Path

def version_updated():
    
    
    # Opening JSON file
    pa = Path().cwd()
    file ="package.json"
    for i in range(2):
        if not (pa / file).exists():
            pa= pa.parent
    print(pa / file)
    f = open(pa / file)

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list

    project_version =data["version"]
    print("Project Version",project_version)
    # Closing file
    f.close()
    
    pyproject = pa /"pyproject.toml"
    with open(pyproject, "r") as f:
        data = toml.load(f)
    print(data)
    data["project"]["version"]=project_version
    with open(pyproject, 'w') as f:
        toml.dump(data, f)
