import json

def export_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file)
        file.close()

def read_json(path):
    var = None
    with open(path, "r") as file:
        var = json.load(file)
        file.close()
    return var