import pandas as pd
import os
os.environ["USE_TF"] = "0"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load dataset (CSV without questions, as you made earlier)
DATA_PATH = "standard_dataset.csv"

# Load the CSV
df = pd.read_csv(DATA_PATH)

# Load the T5 model for question generation
model_name = "valhalla/t5-small-qg-prepend"  # You can try other T5 variants too
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_questions(context):
    input_text = "generate questions: " + context
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=64, num_return_sequences=3, num_beams=5, early_stopping=True)

    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

def select_unit(standard, unit_title):
    # Filter the selected unit
    row = df[(df['standard'] == standard) & (df['unit_title'] == unit_title)]
    if row.empty:
        print("No matching unit found.")
        return None
    return row.iloc[0]

# Example: Select unit
standard_input = 1
unit_title_input = "The Clever Rabbit"  # You can change this to any unit title in your CSV

unit = select_unit(standard_input, unit_title_input)
if unit is not None:
    print(f"\nGenerating questions for: {unit_title_input}\n")
    lesson_content = {
        "The Clever Rabbit": "Once there was a clever rabbit who lived in a forest with many other animals. A fierce lion started eating the animals one by one..."
        # Add full lesson contents for other units here
    }
    context = lesson_content.get(unit_title_input)
    if context:
        questions = generate_questions(context)
        for i, q in enumerate(questions, 1):
            print(f"Q{i}: {q}")
    else:
        print("Lesson content not found for this unit.")
