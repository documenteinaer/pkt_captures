#!/usr/bin/env python3

import json
import os
import sys

print("This script is used for 03.06.2022 folder")

if len(sys.argv) < 2:
    print("Please provide an argument", file=sys.stderr)
    exit(-1)


json_dir=sys.argv[1]

collections = {}
i = 0

# Colț 0 - Început latură 1
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir0_pos0_colt0.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


# Latură 1
x_start=41.61
x_end=41.61
y_start=20.44
y_end=33.16

for it in range(1,13):
    json_name = os.path.join(json_dir, "linux_etaj0_dir0_pos"+str(it)+".json")
    json_file = open(json_name)
    collection = json.load(json_file)
    collection["collection0"]["x"] = x_start
    collection["collection0"]["y"] = y_start + it * (y_end - y_start) / 13

    # Add to collections 
    collections["collection"+str(i)] = collection["collection0"]
    i+=1


# Colț 1 - Final Latură 1
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir0_pos13_colt1.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


# Colț 1 - Început latură 2
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir1_pos14_colt1.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


# Latură 2
x_start=41.61
x_end=54.37
y_start=33.16
y_end=33.16

for it in range(15,28):
    json_name = os.path.join(json_dir, "linux_etaj0_dir1_pos"+str(it)+".json")
    json_file = open(json_name)
    collection = json.load(json_file)
    collection["collection0"]["y"] = y_start
    collection["collection0"]["x"] = x_start + (it-14) * (x_end - x_start) / 14

    # Add to collections 
    collections["collection"+str(i)] = collection["collection0"]
    i+=1


# Colț 2 - Final latură 2
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir1_pos28_colt2.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


# Colț 2 - Început latură 3
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir2_pos29_colt2.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


# Latură 3
x_start=54.37
x_end=54.37
y_start=33.16
y_end=20.44

for it in range(30,43):
    json_name = os.path.join(json_dir, "linux_etaj0_dir2_pos"+str(it)+".json")
    json_file = open(json_name)
    collection = json.load(json_file)
    collection["collection0"]["x"] = x_start
    collection["collection0"]["y"] = y_start + (it-29) * (y_end - y_start) / 14

    # Add to collections 
    collections["collection"+str(i)] = collection["collection0"]
    i+=1


# Colț 3 - Final latură 3
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir2_pos43_colt3.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1



# Colț 3 - Început latură 4
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir3_pos44_colt3.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


# Latură 4
x_start=54.37
x_end=41.61
y_start=20.44
y_end=20.44

for it in range(45,59):
    json_name = os.path.join(json_dir, "linux_etaj0_dir3_pos"+str(it)+".json")
    json_file = open(json_name)
    collection = json.load(json_file)
    collection["collection0"]["y"] = y_start
    collection["collection0"]["x"] = x_start + (it-44) * (x_end - x_start) / 15

    # Add to collections 
    collections["collection"+str(i)] = collection["collection0"]
    i+=1


# Colț 0 - Final latură 4
json_corner = open(os.path.join(json_dir, "linux_etaj0_dir3_pos59_colt0.json"))
collections["collection"+str(i)] = json.load(json_corner)["collection0"]
i+=1


out_filename = "0-linux-03-06-2022.json"
print("Result written to", out_filename)

# Scriere în fișier
with open(out_filename, 'w') as outfile:
    json.dump(collections, outfile, indent = 2)
