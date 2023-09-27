
from gpt4all import GPT4All, Embed4All
from termcolor import colored
from multiprocessing import Process, Manager, Queue
from typing import List, Dict, Any

def initialize_models():
    """Initialize GPT4All and Embed4All models. Raise an exception if failed."""
    try:
        model = GPT4All("wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin")
        embedder = Embed4All()
    except Exception as e:
        raise Exception(f"Error initializing models: {e}")

def generate_embedding(text: str) -> List[float]:
    """Generate embeddings for the given text using Embed4All.

    Args:
        text (str): The text for which to generate an embedding.

    Returns:
        List[float]: The generated embedding.

    Raises:
        Exception: If embedding generation fails.
    """
    try:
        return embedder.embed(text) if text else []
    except Exception as e:
        raise Exception(f"Error generating embedding: {e}")

def safe_generate(prompt: str, max_tokens: int = 50) -> str:
    """Safely generate text using GPT4All.

    Args:
        prompt (str): The prompt to send to the model.
        max_tokens (int, optional): The maximum number of tokens for the generated text. Defaults to 50.

    Returns:
        str: The generated text.

    Raises:
        Exception: If text generation fails.
    """
    try:
        text = model.generate(prompt, max_tokens=max_tokens)
        return text if text else "No output from model"
    except Exception as e:
        raise Exception(f"Error generating text: {e}")

class CEO:
    """The CEO class responsible for generating tasks for the Software Engineer."""
    def run(self, message_queue: Queue):
        try:
            ceo_request = safe_generate("Assign a task for the Software Engineer: ", 60)
            print(colored(f"=== CEO: {ceo_request} ===", 'yellow'))
            message_queue.put({"from": "CEO", "task": ceo_request, "embedding": generate_embedding(ceo_request)})
        except Exception as e:
            raise Exception(f"Error in CEO run: {e}")

class SoftwareEngineer:
    """The Software Engineer class responsible for breaking down tasks into sub-tasks."""
    def run(self, message_queue: Queue):
        try:
            ceo_message = message_queue.get()
            ceo_request = ceo_message["task"]
            sub_tasks = safe_generate(f"Break down the task '{ceo_request}' into sub-tasks: ", 120)
            print(colored(f"=== Software Engineer: {sub_tasks} ===", 'green'))
            message_queue.put({"from": "Software Engineer", "sub_tasks": sub_tasks, "embedding": generate_embedding(sub_tasks)})
        except Exception as e:
            raise Exception(f"Error in Software Engineer run: {e}")

class CodeGenerator:
    """The Code Generator class responsible for generating code snippets for sub-tasks."""
    def run(self, message_queue: Queue):
        try:
            software_engineer_message = message_queue.get()
            sub_tasks = software_engineer_message["sub_tasks"]
            code_snippets = safe_generate(f"Generate code snippets for the sub-tasks: {sub_tasks}", 240)
            print(colored(f"=== Code Generator: {code_snippets} ===", 'blue'))
            message_queue.put({"from": "Code Generator", "code_snippets": code_snippets, "embedding": generate_embedding(code_snippets)})
        except Exception as e:
            raise Exception(f"Error in Code Generator run: {e}")

class DataAnalyst:
    """The Data Analyst class responsible for analyzing data and providing insights."""
    def run(self, message_queue: Queue):
        try:
            insights = safe_generate("Analyze the data and provide insights: ", 120)
            print(colored(f"=== Data Analyst: {insights} ===", 'yellow'))
            message_queue.put({"from": "Data Analyst", "insights": insights, "embedding": generate_embedding(insights)})
        except Exception as e:
            raise Exception(f"Error in Data Analyst run: {e}")

class QAEngineer:
    """The QA Engineer class responsible for performing tests and providing results."""
    def run(self, message_queue: Queue):
        try:
            test_results = safe_generate("Perform tests and provide results: ", 120)
            print(colored(f"=== QA Engineer: {test_results} ===", 'red'))
            message_queue.put({"from": "QA Engineer", "test_results": test_results, "embedding": generate_embedding(test_results)})
        except Exception as e:
            raise Exception(f"Error in QA Engineer run: {e}")

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
        raise Exception(f"Error in main execution: {e}")
