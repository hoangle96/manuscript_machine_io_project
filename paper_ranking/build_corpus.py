from pathlib import Path
import json
import unicodedata

all_cvpr_intro = Path.home() / "Downloads\intro\intro\cvpr"

all_text = {}
idx = 0
for f_p in all_cvpr_intro.glob('*.txt'):
    with open(f_p, 'rb') as f:
        text = f.read()
    
    all_text[str(f_p.name)] = unicodedata.normalize('NFC', text.decode())
all_text = json.dumps(all_text)
with open('all_raw_data.json', 'w') as f:
    json.dump(all_text, f)

