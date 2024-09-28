from openai import OpenAI
import os
import json
import polars as pl


if __name__ == "__main__":
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    with open('all_raw_data.json', 'r') as f:
        all_text = json.load(f)
    
    all_text = json.loads(all_text)

    score = {'intro': [], 'score': []}

    for k, _ in all_text.items():   
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': 'Give this introduction a grade based on the IELTS rubric with 0.25 increment.'
                },
                {
                    "role": "user",
                    'content': all_text[k]
                }
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        score['intro'].append(k) 
        score['score'].append(chat_completion.choices[0].message.content) 

    pl.DataFrame(score).write_csv('score_3nd_prompt.csv')

