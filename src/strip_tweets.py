import json

file_in = "dat/corpora/australia/australia.jsonl"
file_out = "dat/corpora/australia/aus-tweets.txt"

with open(file_in, "r") as flein:
    with open(file_out, "w") as fleout:
        for line in flein:
            data = json.loads(line.strip('\n'))
            fleout.write(data['full_text'] + '\n')
