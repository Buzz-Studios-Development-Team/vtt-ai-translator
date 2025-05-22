

### pip installations
#%pip install openai
#%pip install webvtt-py

### Package imports
import os
import copy
import subprocess
import sys

### pip installations
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ['openai', 'webvtt-py']
for p in packages:
        install(p)

from openai import OpenAI
import webvtt



### Setup variables
## Set file paths / language output 
folder_path = "/Users/connorwright/Downloads/GT.CS.CodeFiles/BuzzStudios/Assets/Subtitles/"
vtt_name = "antr-English.vtt"
trans_lang = "es"
language = "Spanish"

## Set API Key 
api_key = ""

vtt_path = os.path.join(folder_path, vtt_name)





### Turn original captions into single string for GPT input 
captions_list = []
captions = []
captions_2 = []

curr_chars = 0
max_tokens = 32000 # 4o-mini limit is 16000 tokens. 4 chars per token. Divide by 2 for safety

vtt = webvtt.read(vtt_path)

for caption in webvtt.read(vtt_path):
    caption.text = caption.text.replace("\n", " ~ ")
    caption_text = caption.text
    captions_2.append(caption_text)
    

## Chunking functionality (removed)
if captions:
    captions_list.append(copy.deepcopy(captions))

captions_list = [
    "\n".join(c) if isinstance(c, list) else str(c)
    for c in captions_list
]

captions_2 = " | ".join(captions_2) if isinstance(captions_2, list) else str(captions_2)

captions = captions_2



### Setup OpenAI client and context
#client = OpenAI(api_key="", base_url="https://api.deepseek.com")
client = OpenAI(api_key=api_key)

system_message = f"""You are a professional subtitle translator. \
            You will only receive a string transcription of a vtt file containing subtitles in English. \
            You will only output a {language} translation of the subtitles and bracketed actions. \
            Do not add anything else to your reply.\
            Do not merge sentences, translate each line individually. \
            Return the translated subtitles in the same order and length as the input. \
            Your steps are as follows: \
            1. Parse the input subtitles \
            2. Translate each line into {language} with language code {trans_lang}. Do not change or remove any '~' or '|' character. If there is a '~' or a '|' mid-sentence, keep it mid-sentence. \
            3. Alter the translated subtitles into more fluent sentences \
            4. Use the setResult method to output the translated subtitles as a string[].
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": captions}
    ]
)
    



### Save translated captions as new vtt file 

## Get GPT response as string, split into list
trans_str = str(response.choices[0].message.content)
trans_list = trans_str.split(" | ")
print(trans_list)

## Edit caption files to match translations, accounting for multi-line texts 
trans_vtt = webvtt.read(vtt_path)
line_index = 0
for i, caption in enumerate(trans_vtt):
    num_lines = len(caption.text.split(" ~ "))
    trans_lines = trans_list[line_index:line_index+num_lines]
    caption.text = "\n".join(trans_lines).replace(" ~ ", "\n")
    line_index += num_lines

## Save as new file w/ specified language name 
trans_filename = str(os.path.splitext(vtt_name)[0]) + '-' + str(trans_lang) + '.vtt'
trans_path = os.path.join(folder_path, trans_filename)
trans_vtt.save(trans_path)