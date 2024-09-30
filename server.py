import json
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import zmq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommandProcessor:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def process_command(self, command_type, **kwargs):
        try:
            if command_type == "os":
                return self.execute_os_command(**kwargs)
            elif command_type == "compute":
                return self.evaluate_math_expression(kwargs["expression"])
            else:
                return {"error": "Unsupported command type"}
        except Exception as e:
            logging.error(f"Command processing failed: {str(e)}")
            return {"error": str(e)}

    # def execute_os_command(self, command_name, *parameters):
    #     cmd = [command_name] + list(parameters)
    #     try:
    #         result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    #         return {"output": result.stdout.strip()}
    #     except subprocess.CalledProcessError as e:
    #         logging.error(f"OS command failed: {e}")
    #         return {"error": str(e)}

    def execute_os_command(self, command_name, *parameters, **kwargs):
        cmd = [command_name] + list(parameters)
        cmd.extend(kwargs.get('arguments', []))
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"output": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            logging.error(f"OS command failed: {e}")
            return {"error": str(e)}

    def evaluate_math_expression(self, expression):
        try:
            result = eval(expression)
            return {"result": result}
        except Exception as e:
            logging.error(f"Math evaluation failed: {str(e)}")
            return {"error": str(e)}

    def serve_forever(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                message = self.socket.recv_json()
                future = executor.submit(self.process_command, **message)
                result = future.result()
                self.socket.send_json(result)

if __name__ == "__main__":
    processor = CommandProcessor()
    processor.serve_forever()