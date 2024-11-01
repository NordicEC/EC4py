import json
from pathlib import Path

def get_project_version():
    
    # Opening JSON file
    pp = Path(".").cwd()
    pa = pp /"package.json"
    if not pa.exists():
        # print(pa)
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
    # print("Project Version",project_version)
    # Closing file
    f.close()
    return project_version


if __name__ == '__main__':
    project_version = get_project_version()
    print("v"+project_version)
