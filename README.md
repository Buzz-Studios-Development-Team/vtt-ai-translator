# VTT AI Translator
## About
This is a notebook to translate VTT subtitle / caption files more fluently than traditional translation tools using the OpenAI API and webvtt. It can be switched to Deepseek easily in the future for more cost-efficient processing. Made by Connor Wright for Georgia Tech's Buzz Studios Filmmaking Club. 

## Setting up for the first time
If you're unfamiliar with Git and/or Jupyter, please follow the instructions below to set up the tool on your computer.

### Setting up Git
First, if you have not yet set up Git, please navigate to [this link](https://git-scm.com/downloads) to download the Git CLI. CLI stands for command-line interface. Git is a version-control system, meaning it is used to keep a preserved history of major changes made to a software project. Projects that use Git live in what is called a repository. The typical workflow of Git involves making changes to a local copy of the files in the project and committing them, which creates a timeline of changes. 

GitHub is a service that holds what are called "remote" repositories, meaning that developers will synchronize their local repositories with a remote one. This allows several developers to work on the same project without interfering with each other. The main moral of the story here is that you'll just be using Git to download what is considered to be the most up-to-date version of the project to a local repository on your computer, where you can then use the tool. You won't have to actually commit or push any changes.

The Git CLI is what lets you use Git commands in your computer's command line. We'll just be using this to clone the project.

Once you've installed the CLI, open up your command line. This can be done by searching for "Command Prompt" or "cmd" in your start menu on Windows. On macOS, it'll be called Terminal.

Use the `cd` command to navigate to a directory where you want to put the files. That'll look something like `cd Documents`.

Once you're there, run this command: `git clone https://github.com/Buzz-Studios-Development-Team/vtt-ai-translator.git`

It should only take a few seconds for the file to be downloaded. You now have a local repository containing the latest form of the tool.

### Setting up Python and Jupyter

Jupyter is a tool that lets you run code in a local server accessed from your browser. In this case, the translator is written in Python. Jupyter notebooks are formatted in "cells," which are individual blocks of code that are intended to be run sequentially but can be run independently of one another. You don't have to write any code to be able to use this tool - you just need to be able to open a Jupyter notebook, make a couple of tiny changes, and then run what's already there.

First, check to see if you have python installed by running `python --version` in your command line. If it can't be found, go to [python.org](https://python.org) and download the latest version. You may need to restart your command line for the changes to take effect.

Now you're going to want to run the following command: `pip install jupyter`. Let us know if any issues arise there.

### Running the tool

Now that your environment is set up, you can go ahead and open up the Jupyter notebook. To do so, you're going to need to navigate your command line to the directory where you cloned the repository. If you put it in your Documents folder, you'll have to run the following: `cd Documents/vtt-ai-translator`. `cd` stands for change directory. It's the same thing as clicking through folders in your file explorer, except you have to actually type out the names of the folders to go into them. If you're not sure you're in the right place, run `dir` to see what's in the folder you're currently in, and run `cd ..` to go back up a level.

Once you're in the right directory (there should be a file called vtt-translator.ipynb), run `jupyter notebook`. Once it starts up, go to your browser and go to the URL `127.0.0.1:8888` (this is a local server running on your computer, accessed through port 8888). You should see a list of files, including the notebook named previously. Double-click it to open it.

Now your task will simply be to fill in the information that the tool needs to find your captioning file, as well as to tell it your language of choice. Scroll past all of the information from this write-up to find the cells containing Python code. In the second cell, you'll see the variables `folder_path`, `vtt_name`, and `trans_lang`.

`folder_path` is going to hold the full path to wherever you've saved a .vtt file you want to translate. For example, if it's in your Downloads folder, the path may look something like this: `C:\Users\abby\Downloads`. Note that you can find that full path in the top bar of the file explorer if you click on it. You can just copy and paste that into the quotation marks.

For `vtt_name`, just put the name of the file, such as `frisbee-fables-cc.vtt`.

Finally, for `trans_lang`, look up the ISO code of the language you want and put it in the quotation marks (for example, en for English, es for Spanish, jp for Japanese).

Lastly, paste the API key (provided by Connor) into the `api_key` field. Remember that key is private!

You're now ready to run the tool and create a translated captioning file. In the top bar, look for the double-triangle play button and click it. It won't look like very much is happening, but after a couple minutes or so, a new file should be created in the same place as the original .vtt file, such as `frisbee-fables-cc-fr.vtt`.

To restart with a new language, just change the ISO code and hit that double-arrow button again!