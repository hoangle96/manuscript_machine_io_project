import json
# import spacy 
# import numpy as np fac
import re

with open('all_raw_data.json', 'r') as f:
    all_text = json.load(f)
    
all_text = json.loads(all_text)

stats = {}

# count number of paragraphs
# count number sentence, count avg length of sentences 
reference_pattern = r'\[\d+(?:,\s*\d+)*\]'
for intro_title, intro in all_text.items():
    params = [i for i in intro.split('\r\n\r\n') if len(i)>1]

    sentence_length = []

    for param in params:
        param.replace('\r\n', '')
        sentences = [re.sub(r'[,.]', '', re.sub(reference_pattern, '', i.strip()))  for i in param.split('.') if len(i.strip()) > 1]
        for sen in sentences:
            words =  [w for w in sen.split(' ') if len(w)] 
            # all_sen_len = [len(w) for w in words]
            sentence_length.append(len(words))

    
    stats[intro_title] = {'n_params': len(params),
                            'avg_sen_len': sum(sentence_length)/len(sentence_length), 
                            'min_sen_len': min(sentence_length), 
                            'max_sen_len': max(sentence_length),
                            'avg_n_sen': len(sentence_length)/len(params)}

with open('descriptive_stat.json', 'w') as f:
    json.dump(stats, f)
          