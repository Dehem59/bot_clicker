import json


with open("proxies.txt", "r") as f:
    lines = f.readlines()

result = {}
for line in lines:
    split_line = line.split(":")
    name = split_line[0].split(".")[-1]
    result[name] = {
        "host": split_line[0], "port": split_line[1], "user": split_line[2], "pass": split_line[3].rstrip("\n")
    }

with open("proxies.json", "w") as f:
    f.write(json.dumps(result))
