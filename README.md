Copilot JSON Extractor!!!


A Python-based automation tool that interacts with Microsoft Copilot to generate structured JSON data from prompt sequences using dynamic object inputs. The project supports incremental 

progress tracking, response parsing, and prompt continuation in case of API limits or interruptions.

🚀 Features

Submit a sequence of structured prompts to Microsoft Copilot.

Use variable substitution for dynamic prompt generation.

Extract and store structured JSON data from Copilot's responses.

Track progress with resume functionality.

Reset conversation between prompt cycles.

Supports large input sets with daily usage limits in mind.

Requirements
Python 3.8+

One of the following libraries for Copilot interaction:

sydney.py

talkingheads

Install dependencies via pip:

bash
Copy
Edit
pip install talkingheads  # or follow the sydney.py instructions


🧪 Usage
Prepare prompts.txt with placeholders like {object_id}.

Fill objects.txt with a list of objects (e.g., distilleries).

Run the script:

bash
Copy
Edit
python main.py
The script will:

Loop over each object.

Inject it into each prompt.

Send the prompt to Copilot.

gives the output.

Track progress for potential restarts.



