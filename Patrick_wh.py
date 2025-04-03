import re
import pandas as pd

"""Patrick_wh.py: Python script for weighted relationship map building.
This script will produce an excel file with all the occurences of characters interations
in a scene, weighted for the number of character phisycally present in the scene."""

__author__      = "Davide Di Censo PhD, Federica Santacroce PhD candidate"

# Initialize the relationship map
relationship_map = {}

def build_relationship_map(scene, speakers, mentioned, num_present_speakers):
    for speaker, speaker_weight in speakers.items():
        if speaker in scene:
            for mention, mention_weight in mentioned.items():
                matches = re.findall(mention, scene, flags=re.IGNORECASE)
                count = len(matches)
                # if count > 0:
                    # Calculate the weighted count
                weighted_count = (count * (speaker_weight + mention_weight)) / num_present_speakers
                # Increment the score for each occurrence
                if speaker in relationship_map:
                    if mention in relationship_map[speaker]:
                        relationship_map[speaker][mention].append(weighted_count)
                    else:
                        relationship_map[speaker][mention] = [weighted_count]
                else:
                    relationship_map[speaker] = {mention: [weighted_count]}
    return relationship_map

characters = {
    "PATRICK2",
    "NICHOLAS2",
    "ANNETTE2", 
    "JULIA2",
    "DAVID2",
    "JOHNNY2",
    "ANNE2",
    "WILLY2",
    "ELEANOR2",
    "MARIANNE2",
    "BRIDGET2",
    "SONNY2",
    "VIRGINIA2",
    "MARY2",
    "ROBERT2",
    "SEAMUS2",
    "NANCY2"
}

speakers = {
    "PATRICK1": 1,
    "NICHOLAS1": 1,
    "ANNETTE1": 1, 
    "JULIA1": 1,
    "DAVID1": 1,
    "JOHNNY1": 1,
    "ANNE1": 1,
    "WILLY1": 1,
    "ELEANOR1": 1,
    "MARIANNE1": 1,
    "BRIDGET1": 1,
    "SONNY1": 1,
    "VIRGINIA1": 1,
    "MARY1": 1,
    "ROBERT1": 1,
    "SEAMUS1": 1,
    "NANCY1": 1,
    "PATRICK2": 2,
    "NICHOLAS2": 2,
    "ANNETTE2": 2, 
    "JULIA2": 2,
    "DAVID2": 2,
    "JOHNNY2": 2,
    "ANNE2": 2,
    "WILLY2": 2,
    "ELEANOR2": 2,
    "MARIANNE2": 2,
    "BRIDGET2": 2,
    "SONNY2": 2,
    "NICHOLAS1": 1,
    "ANNETTE1": 1, 
    "JULIA1": 1,
    "DAVID1": 1,
    "JOHNNY1": 1,
    "ANNE1": 1,
    "WILLY1": 1,
    "ELEANOR1": 1,
    "MARIANNE1": 1,
    "BRIDGET1": 1,
    "SONNY1": 1,
    "VIRGINIA1": 1,
    "MARY1": 1,
    "ROBERT1": 1,
    "SEAMUS1": 1,
    "NANCY1": 1,
    "PATRICK2": 2,
    "NICHOLAS2": 2,
    "ANNETTE2": 2, 
    "JULIA2": 2,
    "DAVID2": 2,
    "JOHNNY2": 2,
    "ANNE2": 2,
    "WILLY2": 2,
    "ELEANOR2": 2,
    "MARIANNE2": 2,
    "BRIDGET2": 2,
    "SONNY2": 2,
    "VIRGINIA2": 2,
    "MARY2": 2,
    "ROBERT2": 2,
    "SEAMUS2": 2,
    "NANCY2": 2
}

mentioned = {
    "PATRICK1": 1,
    "NICHOLAS1": 1,
    "ANNETTE1": 1, 
    "JULIA1": 1,
    "DAVID1": 1,
    "JOHNNY1": 1,
    "ANNE1": 1,
    "WILLY1": 1,
    "ELEANOR1": 1,
    "MARIANNE1": 1,
    "BRIDGET1": 1,
    "SONNY1": 1,
    "VIRGINIA1": 1,
    "MARY1": 1,
    "ROBERT1": 1,
    "SEAMUS1": 1,
    "NANCY1": 1,
    "PATRICK2": 2,
    "NICHOLAS2": 2,
    "ANNETTE2": 2, 
    "JULIA2": 2,
    "DAVID2": 2,
    "JOHNNY2": 2,
    "ANNE2": 2,
    "WILLY2": 2,
    "ELEANOR2": 2,
    "MARIANNE2": 2,
    "BRIDGET2": 2,
    "SONNY2": 2,
    "NICHOLAS1": 1,
    "ANNETTE1": 1, 
    "JULIA1": 1,
    "DAVID1": 1,
    "JOHNNY1": 1,
    "ANNE1": 1,
    "WILLY1": 1,
    "ELEANOR1": 1,
    "MARIANNE1": 1,
    "BRIDGET1": 1,
    "SONNY1": 1,
    "VIRGINIA1": 1,
    "MARY1": 1,
    "ROBERT1": 1,
    "SEAMUS1": 1,
    "NANCY1": 1,
    "PATRICK2": 2,
    "NICHOLAS2": 2,
    "ANNETTE2": 2, 
    "JULIA2": 2,
    "DAVID2": 2,
    "JOHNNY2": 2,
    "ANNE2": 2,
    "WILLY2": 2,
    "ELEANOR2": 2,
    "MARIANNE2": 2,
    "BRIDGET2": 2,
    "SONNY2": 2,
    "VIRGINIA2": 2,
    "MARY2": 2,
    "ROBERT2": 2,
    "SEAMUS2": 2,
    "NANCY2": 2
}

# Open the file
text = open("Patrick_Melrose.txt", "r")
plot = text.read()
# split text in scenes
scenes = re.split('INT.|EXT.', plot)
# remove garbage
new_list = [x for x in scenes if x != '']
scenes = [x for x in new_list if x != '/']

# count occurrences for each scene
for scene in scenes:
    present_speakers = [character for character in characters if character in scene]
    num_present_speakers = len(present_speakers)
    if num_present_speakers >0:
        # print(f"{num_present_speakers}")
        relationship_map = build_relationship_map(scene, speakers, mentioned, num_present_speakers)

for speaker, mentions in relationship_map.items():
    for mention, scores in mentions.items():
        total_score = sum(scores)
        print(f"{speaker} - {mention}: {scores} = {total_score}")

data = []
for speaker, mentions in relationship_map.items():
    for mention, scores in mentions.items():
        total_score = sum(scores)
        data.append([speaker, mention, total_score])

df = pd.DataFrame(data, columns=["Speaker", "Mention", "Total Score"])

# Save the DataFrame to an Excel file
df.to_excel("weighted_relationship_map.xlsx", index=False)