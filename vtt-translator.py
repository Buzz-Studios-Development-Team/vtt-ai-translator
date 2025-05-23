# # VTT AI Translator
# ## About
# This is a notebook to translate VTT subtitle / caption files fluently using the OpenAI API and webvtt. It can be switched to Deepseek easily in the future for more cost-efficient processing. Made by Connor Wright for Georgia Tech's Buzz Studios Filmmaking Club. 
# 
# ## How to Use 
# * Clone the repo
# * Change the folder / file paths to the respective vtt
# * Set a language using the ISO language code
# * Put in an OpenAI API key (or ask for mine)
# * Run all the cells

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

for index, caption in enumerate(webvtt.read(vtt_path)):
    caption.text = caption.text.replace("\n", f" ~ ")
    caption_text = caption.text + f" #{index}# "
    captions_2.append(caption_text)


## Chunking functionality (removed)
'''
if captions:
    captions_list.append(copy.deepcopy(captions))

captions_list = [
    "\n".join(c) if isinstance(c, list) else str(c)
    for c in captions_list
]
'''


captions_2 = " | ".join(captions_2) if isinstance(captions_2, list) else str(captions_2)
print(webvtt.read(vtt_path)[0])

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
            2. Translate each line into {language} with language code {trans_lang}. Do not change or remove any '~' or '|' or '#\d#' characters. If there is a '~' or a '|' or a '#' mid-sentence, keep it mid-sentence. \
            3. Alter the translated subtitles into more fluent sentences \
            4. Use the setResult method to output the translated subtitles as a string[].
"""

'''
### Response chunking -- removed 
responses = []
for captions in captions_list:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": captions}
        ]
    )
    responses.append(response)
'''
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": captions}
    ]
)
    
print(response)

### Save translated captions as new vtt file 
import re

def extract_index(text):
    match = re.search(r"#(\d+)#", text)
    if match:
        return int(match.group(1))
    else:
        return None

## Get GPT response as string, split into list
trans_str = str(response.choices[0].message.content)
trans_list = trans_str.split(" | ")

trans_vtt = webvtt.read(vtt_path)


## Create a dictionary for accessing translated captions in case GPT missed lines
index_to_translation = {}
for line in trans_list:
    idx = extract_index(line)
    if idx is not None:
        cleaned_line = re.sub(r'#\d+#\s*$', '', line).strip()
        index_to_translation[idx] = cleaned_line
        #print(idx, cleaned_line)

## Replace original captions with translated lines
line_index = 0
for i, caption in enumerate(trans_vtt):
    num_lines = len(caption.text.split(" ~ "))
    if i in index_to_translation:
        trans_lines = []
        for j in range(line_index, line_index+num_lines):
            trans_lines.append(index_to_translation[j])
        caption.text = "\n".join(trans_lines).replace(" ~ ", "\n")
    else:
        caption.text = "[MISSING TRANSLATION] \n" ##could also just set it as the untranslated text

    line_index += num_lines


## Save as new file w/ specified language name 
trans_filename = str(os.path.splitext(vtt_name)[0]) + '-' + str(language) + '-'  + str(trans_lang) + '.vtt'
trans_path = os.path.join(folder_path, trans_filename)
trans_vtt.save(trans_path)
print(trans_vtt[0])


