import json
import os
from sydney import SydneyClient  # Import SydneyClient from sydney-py

# Define daily prompt limit
DAILY_PROMPT_LIMIT = 100
current_prompt_count = 0

# Define a sequence of prompts with placeholders and corresponding keys
PROMPT_SEQUENCE = [
    ("Provide a brief history of {}.", "History"),
    ("List the popular products of {}.", "PopularProducts"),
    ("Describe the tasting notes for {} products.", "TastingNotes"),
    ("Explain the distilling process at {}.", "DistillingProcess"),
    ("Mention any notable awards for {}.", "Awards"),
]

# Set up the environment variable for the Sydney Client session cookie
SESSION_COOKIE = "your_session_cookie_here"  # Replace with your actual session cookie value
os.environ["BING_COOKIES"] = SESSION_COOKIE  # Set session cookie in environment variable

# Initialize Sydney client
chathead = SydneyClient()  # No need to pass the cookie parameter here

# Load Object IDs from an external file (each line is an Object ID)
with open("object_ids.txt", "r") as f:
    object_ids = [line.strip() for line in f if line.strip()]

# Count total Object IDs and total prompts
total_object_ids = len(object_ids)
total_prompts = len(PROMPT_SEQUENCE)
print(f"Total Object IDs: {total_object_ids}")
print(f"Total number of prompts per Object ID: {total_prompts}")

# Initialize data storage for all objects
all_data = []

# Load or initialize progress marker
progress_marker_file = "progress_marker.txt"
if os.path.exists(progress_marker_file):
    with open(progress_marker_file, "r") as marker_file:
        lines = marker_file.readlines()
        if "Complete" in lines[-1]:
            print("All Object IDs have already been processed.")
            exit()
        else:
            # Extract last processed Object ID, prompt indexes, and daily prompt count
            last_processed = lines[-1].strip().split(',')
            obj_index_start = int(last_processed[0].split()[-1]) - 1
            prompt_index_start = int(last_processed[1].split()[-1]) - 1
            current_prompt_count = int(last_processed[2].split()[-1])
else:
    obj_index_start, prompt_index_start = 0, 0
    current_prompt_count = 0

# Function to submit prompt and retrieve specific targeted answer
def sydney_prompt(prompt_text: str, key: str) -> dict:
    global current_prompt_count
    if current_prompt_count >= DAILY_PROMPT_LIMIT:
        print("Daily prompt limit reached. Exiting.")
        exit()
    
    print(f"Submitting prompt to Sydney: {prompt_text}")
    response = chathead.ask(prompt_text)  # Use Sydney's `ask` method
    current_prompt_count += 1

    # Isolate and return only the targeted answer for the specific key
    return {key: response.get("target_answer")} if response and "target_answer" in response else {key: "Not available"}

# Function to update progress marker with Object ID, prompt index, and daily prompt count
def update_progress_marker(object_index: int, prompt_index: int):
    with open(progress_marker_file, "w") as marker_file:
        marker_file.write(f"Current Object ID: {object_index + 1} of {total_object_ids}, "
                          f"Current Prompt: {prompt_index + 1} of {total_prompts}, "
                          f"Daily Prompt Count: {current_prompt_count}\n")
    print(f"Updated progress marker to Object ID {object_index + 1}, Prompt {prompt_index + 1}, "
          f"Daily Prompt Count: {current_prompt_count}")

# Iterate through each Object ID and process all prompts
for obj_index in range(obj_index_start, total_object_ids):
    object_id = object_ids[obj_index]
    object_data = {
        "distillery": object_id,
        "details": {}
    }

    # Execute prompts for each Object ID, resuming from last prompt if interrupted
    for i in range(prompt_index_start if obj_index == obj_index_start else 0, total_prompts):
        prompt_text, key = PROMPT_SEQUENCE[i]
        formatted_prompt = prompt_text.format(object_id)

        update_progress_marker(obj_index, i)  # Update marker file before each prompt

        # Get response from Sydney for the specific key
        response = sydney_prompt(formatted_prompt, key)
        if response:
            object_data["details"].update(response)

        # Save JSON data after each prompt in case of interruption
        with open("distillery_data.json", "w") as f:
            json.dump(all_data + [object_data], f, indent=4)

        print(f"Prompt {i + 1} of {total_prompts} for Object ID {obj_index + 1} of {total_object_ids} complete")

    # Add completed Object ID data to all_data array
    all_data.append(object_data)

    # Update progress count and save to file
    with open(progress_marker_file, "a") as marker_file:
        if obj_index + 1 == total_object_ids:
            marker_file.write("Complete\n")
            print("All Object IDs completed.")
        else:
            marker_file.write(f"Object list {obj_index + 1} of {total_object_ids} complete\n")

    # Reset prompt index after each Object ID
    prompt_index_start = 0

# Reset Sydney conversation (if needed)
def reset_sydney_conversation():
    print("Resetting Sydney conversation.")
    chathead.reset_conversation()  # Reset the conversation if supported

reset_sydney_conversation()
