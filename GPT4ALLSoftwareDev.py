from gpt4all import GPT4All, Embed4All
from termcolor import colored
from multiprocessing import Process, Manager, Queue
from typing import List, Dict, Any

# Initialize GPT4All and Embed4All models
try:
    model = GPT4All("wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin")
    
    embedder = Embed4All()
except Exception as e:
    print(f"Error initializing models: {e}")

# Function to generate embeddings
def generate_embedding(text: str) -> List[float]:
    try:
        if text:
            return embedder.embed(text)
        return []
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

# Function to safely generate text from the model
def safe_generate(prompt: str, max_tokens: int = 50) -> str:
    try:
        text = model.generate(prompt, max_tokens=max_tokens)
        return text if text else "No output from model"
    except Exception as e:
        print(f"Error generating text: {e}")
        return "Error generating text"

# CEO Class
class CEO:
    def run(self, message_queue: Queue):
        try:
            ceo_request = safe_generate("Assign a task for the Software Engineer: ", 60)
            print(colored(f"=== CEO: {ceo_request} ===", 'yellow'))
            message_queue.put({"from": "CEO", "task": ceo_request, "embedding": generate_embedding(ceo_request)})
        except Exception as e:
            print(f"Error in CEO run: {e}")

# Software Engineer Class
class SoftwareEngineer:
    def run(self, message_queue: Queue):
        try:
            ceo_message = message_queue.get()
            ceo_request = ceo_message["task"]
            sub_tasks = safe_generate(f"Break down the task '{ceo_request}' into sub-tasks: ", 120)
            print(colored(f"=== Software Engineer: {sub_tasks} ===", 'green'))
            message_queue.put({"from": "Software Engineer", "sub_tasks": sub_tasks, "embedding": generate_embedding(sub_tasks)})
        except Exception as e:
            print(f"Error in Software Engineer run: {e}")

# Code Generator Class
class CodeGenerator:
    def run(self, message_queue: Queue):
        try:
            software_engineer_message = message_queue.get()
            sub_tasks = software_engineer_message["sub_tasks"]
            code_snippets = safe_generate(f"Generate code snippets for the sub-tasks: {sub_tasks}", 240)
            print(colored(f"=== Code Generator: {code_snippets} ===", 'blue'))
            message_queue.put({"from": "Code Generator", "code_snippets": code_snippets, "embedding": generate_embedding(code_snippets)})
        except Exception as e:
            print(f"Error in Code Generator run: {e}")

# Data Analyst Class
class DataAnalyst:
    def run(self, message_queue: Queue):
        try:
            insights = safe_generate("Analyze the data and provide insights: ", 120)
            print(colored(f"=== Data Analyst: {insights} ===", 'yellow'))
            message_queue.put({"from": "Data Analyst", "insights": insights, "embedding": generate_embedding(insights)})
        except Exception as e:
            print(f"Error in Data Analyst run: {e}")

# QA Engineer Class
class QAEngineer:
    def run(self, message_queue: Queue):
        try:
            test_results = safe_generate("Perform tests and provide results: ", 120)
            print(colored(f"=== QA Engineer: {test_results} ===", 'red'))
            message_queue.put({"from": "QA Engineer", "test_results": test_results, "embedding": generate_embedding(test_results)})
        except Exception as e:
            print(f"Error in QA Engineer run: {e}")

# Main Execution
if __name__ == '__main__':
    try:
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
        print(f"Error in main execution: {e}")
