from transformers import AutoTokenizer, AutoModelForCausalLM

# Directory to save the model
model_path = "../models/mistral-7b"



# Load and save the model
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print(f"Mistral model saved to {model_path}")
