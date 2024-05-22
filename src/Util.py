import json

def parseFileName(path: str) -> str:
    dirs = path.split("/")
    file = dirs[len(dirs) - 1].split(".")
    file = file[:-1]
    name = ".".join(file)
    return name


def getTotalFrames(path) -> int:
    # Opening JSON file
    file = open(path)

    # returns JSON object as
    # a dictionary
    data = json.load(file)

    return len(data)
