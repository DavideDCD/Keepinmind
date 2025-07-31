import re
import pandas as pd

"""Patrick.py: Python script for relationship map building.
This script will produce an excel file with all the occurences 
of characters interations in a scene."""

__author__      = "Davide Di Censo PhD, Federica Santacroce PhD candidate"

# Initialize the relationship map
relationship_map = {}

def build_relationship_map(scene, speakers, mentioned):
    for speaker, speaker_weight in speakers.items():
        # if speaker in scene:
        for mention, mention_weight in mentioned.items():
            matches = re.findall(mention, scene, flags=re.IGNORECASE)
            count = len(matches)
            # if count > 0:
                # Calculate the weighted count
            weighted_count = count * (speaker_weight + mention_weight)
            # Increment the score for each occurrence
            if speaker in relationship_map:
                if mention in relationship_map[speaker]:
                    relationship_map[speaker][mention].append(weighted_count)
                else:
                    relationship_map[speaker][mention] = [weighted_count]
            else:
                relationship_map[speaker] = {mention: [weighted_count]}
    return relationship_map

def get_speakers_and_mentioned(w1, w2):
    speakers = {
        "PATRICK1": w1, "NICHOLAS1": w1, "ANNETTE1": w1, "JULIA1": w1, "DAVID1": w1, "JOHNNY1": w1, "ANNE1": w1, "WILLY1": w1, "ELEANOR1": w1, "MARIANNE1": w1, "BRIDGET1": w1, "SONNY1": w1, "VIRGINIA1": w1, "MARY1": w1, "ROBERT1": w1, "SEAMUS1": w1, "NANCY1": w1,
        "PATRICK2": w2, "NICHOLAS2": w2, "ANNETTE2": w2, "JULIA2": w2, "DAVID2": w2, "JOHNNY2": w2, "ANNE2": w2, "WILLY2": w2, "ELEANOR2": w2, "MARIANNE2": w2, "BRIDGET2": w2, "SONNY2": w2, "VIRGINIA2": w2, "MARY2": w2, "ROBERT2": w2, "SEAMUS2": w2, "NANCY2": w2
    }
    mentioned = speakers.copy()
    return speakers, mentioned

# List of text files to process
text_files = [
    "Patrick_Melrose_101.txt",
    "Patrick_Melrose_102.txt",
    "Patrick_Melrose_103.txt",
    "Patrick_Melrose_104.txt",
    "Patrick_Melrose_105.txt",
]

# Try different w1, w2 pairs (e.g., w1 from 0.0 to 1.0 in steps of 0.1)
for i in range(0, 11):
    w1 = i / 10
    w2 = 1 - w1
    speakers, mentioned = get_speakers_and_mentioned(w1, w2)
    excel_filename = f"relationship_map_w1_{w1:.1f}_w2_{w2:.1f}.xlsx"
    with pd.ExcelWriter(excel_filename) as writer:
        for text_file in text_files:
            with open(text_file, "r") as text:
                plot = text.read()
            scenes = re.split('INT.|EXT.', plot)
            new_list = [x for x in scenes if x != '']
            scenes = [x for x in new_list if x != '/']
            relationship_map = {}
            for scene in scenes:
                relationship_map = build_relationship_map(scene, speakers, mentioned)
            # Aggregate scores for unordered pairs
            pair_scores = {}
            for speaker, mentions in relationship_map.items():
                for mention, scores in mentions.items():
                    if speaker == mention:
                        continue  # skip self-pairs if not needed
                    pair = tuple(sorted([speaker, mention]))
                    pair_scores[pair] = pair_scores.get(pair, 0) + sum(scores)
            data = []
            for (speaker, mention), total_score in pair_scores.items():
                co_occurrence = total_score if (speaker.endswith('2') and mention.endswith('2')) else 0
                mention_idx = total_score if (speaker.endswith('1') or mention.endswith('1')) else 0
                data.append([speaker, mention, total_score, co_occurrence, mention_idx])
            df = pd.DataFrame(
                data,
                columns=["Speaker", "Mention", "Total Score", "Co-occurrence Index", "Mention Index"]
            )
            sheet_name = text_file.replace('.txt', '')[:31]  # Excel sheet name max length is 31
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added sheet: {sheet_name} to {excel_filename}")
