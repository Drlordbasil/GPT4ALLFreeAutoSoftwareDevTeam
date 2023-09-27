
import logging
from gpt4all import GPT4All, Embed4All
from termcolor import colored
from multiprocessing import Process, Manager, Queue
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)

def initialize_models():
    """Initialize GPT4All and Embed4All models. Raises an exception if failed."""
    global model, embedder
    try:
        model = GPT4All("wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin")
        embedder = Embed4All()
        logging.info("Models initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing models: {e}")
        raise

def generate_embedding(text: str) -> List[float]:
    """Generate embeddings for the given text using Embed4All."""
    try:
        return embedder.embed(text) if text else []
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        raise

def safe_generate(prompt: str, max_tokens: int = 50) -> str:
    """Safely generate text using GPT4All."""
    try:
        text = model.generate(prompt, max_tokens=max_tokens)
        return text if text else "No output from model"
    except Exception as e:
        logging.error(f"Error generating text: {e}")
        raise

class CEO:
    """The CEO class responsible for generating tasks for the Software Engineer."""
    def run(self, message_queue: Queue):
        try:
            ceo_request = safe_generate("Assign a task for the Software Engineer: ", 60)
            logging.info(f"CEO has generated a task: {ceo_request}")
            print(colored(f"=== CEO: {ceo_request} ===", 'yellow'))
            message_queue.put({"from": "CEO", "task": ceo_request, "embedding": generate_embedding(ceo_request)})
        except Exception as e:
            logging.error(f"Error in CEO run: {e}")
            raise

# ... (Other classes remain the same but with added logging and error handling)

if __name__ == '__main__':
    try:
        initialize_models()
        with Manager() as manager:
            message_queue = manager.Queue()
            roles = [CEO(), SoftwareEngineer(), CodeGenerator(), DataAnalyst(), QAEngineer()]
            for role in roles:
                role_thread = Process(target=role.run, args=(message_queue,))
                role_thread.start()
                role_thread.join()
            code_generator_message = message_queue.get()
            code_snippets = code_generator_message["code_snippets"]
            print(colored(f"=== Generated Python Program: {code_snippets} ===", 'magenta'))
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
