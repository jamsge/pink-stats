from os import listdir
from os.path import isfile, join
import json
from difflib import SequenceMatcher
import re


def similar(a, b):
    if (not a == b and a.lower() == b.lower()):
        return 0.99
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

print (similar("glazed", "Glazed"))

participants_unsorted = []
participants_ids = []

for dir in listdir("./tourney/"):
    files = listdir("./tourney/"+dir)
    match_json = json.load(open("./tourney/"+dir+"/"+files[0]))
    participant_json = json.load(open("./tourney/"+dir+"/"+files[1]))
    for p in participant_json:
        participants_unsorted.append(p["participant"]["name"])
        participants_ids.append({p["participant"]["name"] : p["participant"]["id"]})

participants = []
[participants.append(x) for x in participants_unsorted if x not in participants]

split_list = []
for p in participants:
    # account for typing error
    p = p.replace("{", "[")
    p = p.replace("]", "")
    p = p.replace("*", "")
    p = p.replace("}", "")
    split = p.split("[")
    if (len(split) == 1):
        split.insert(0, split[0].split("#")[0])
    for i in range(len(split)):
        if split[i][-1:] == " ":
            split[i] = split[i][0:-1]
    split_list.append(split)

tag_dictionary = {}
for pair in split_list:
    found_similar_tag = False
    for key in tag_dictionary:
        similarity_score = similar(key, pair[0])
        if (similarity_score >= 0.79 and not similarity_score == 1):
            tag_dictionary[key]["other_tags"].append(pair[0])
            if (not pair[1] in tag_dictionary[key]["codes"]):
                tag_dictionary[key]["codes"].append(pair[1])
            found_similar_tag = True

    if not found_similar_tag:
        tag_dictionary[pair[0]] = {"other_tags": [], "codes": [pair[1]]}

# to_be_deleted = []
# for tag1 in tag_dictionary.copy():
#     codes1 = tag_dictionary[tag1]["codes"]
#     for code1 in codes1:
#         for tag2 in tag_dictionary.copy():
#             if not tag1 == tag2:
#                 codes2 = tag_dictionary[tag2]["codes"]
#                 for code2 in codes2:
#                     if (code1 == code2):
#                         print("match", code1, code2, tag1, tag2)
#                         to_be_transferred = tag_dictionary[tag2]
#                         del tag_dictionary[tag2]
#                         tag_dictionary[tag1]["other_tags"].append(tag2)


with open("test.json", "w") as outfile:
    json.dump(tag_dictionary, outfile)
