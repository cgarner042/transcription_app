from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import os
import logging
from datetime import datetime

# Configure logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    filename=f"../logs/summarization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.DEBUG,
    format=LOG_FORMAT
)

INPUT_DIR = "../data/output/"
PROMPT_PATH = "../global_prompt.txt"
DEFAULT_PROMPT = ("Summarize this transcript into a concise, engaging YouTube description "
                  "that highlights key points while being casual and optimized for SEO. "
                  "Limit the main description to 500 characters. Add relevant hashtags based on the content.")

MODELS = {
    "mistral": "mistralai/Mistral-7B-v0.1",
    "flan-t5": "google/flan-t5-large",
    "bart": "facebook/bart-large-cnn"
}


def load_prompt(prompt_path):
    """Load the global prompt from a file, or use the default if unavailable."""
    try:
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                prompt = f.read().strip()
                logging.info("Custom prompt loaded.")
                return prompt
        else:
            logging.warning("Prompt file not found. Using default prompt.")
            return DEFAULT_PROMPT
    except Exception as e:
        logging.error(f"Error loading prompt: {e}")
        return DEFAULT_PROMPT


def summarize_text(text, model_name, prompt):
    """Summarize text using a specific model."""
    try:
        logging.info(f"Loading model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        logging.info("Starting summarization.")
        input_text = f"{prompt}\n\n{text}"
        summary = summarizer(input_text, max_length=500, min_length=100, do_sample=False)
        logging.info("Summarization completed.")
        return summary[0]["summary_text"]
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        raise


if __name__ == "__main__":
    try:
        # Load prompt
        prompt = load_prompt(PROMPT_PATH)

        # List available files
        files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
        if not files:
            raise FileNotFoundError("No text files found in input directory.")

        print("Available text files:")
        for idx, file_name in enumerate(files, 1):
            print(f"{idx}: {file_name}")

        # Select file
        file_index = int(input("Enter the number of the file to summarize: ").strip()) - 1
        if file_index < 0 or file_index >= len(files):
            raise IndexError("Invalid file number selected.")

        selected_file = files[file_index]
        file_path = os.path.join(INPUT_DIR, selected_file)
        with open(file_path, "r") as f:
            transcript_text = f.read()

        # Select model
        print("Available models:")
        for idx, model_name in enumerate(MODELS.keys(), 1):
            print(f"{idx}: {model_name}")

        model_index = int(input("Enter the number of the model to use: ").strip()) - 1
        model_name = list(MODELS.values())[model_index]

        # Generate summary
        summary = summarize_text(transcript_text, model_name, prompt)

        # Save summary
        output_path = os.path.join(INPUT_DIR, f"{os.path.splitext(selected_file)[0]}_summary.txt")
        with open(output_path, "w") as f:
            f.write(summary)
        print(f"Summary saved to {output_path}.")
    except Exception as e:
        logging.critical(f"Script terminated due to error: {e}")
        print(f"Error: {e}")
