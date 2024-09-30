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
        """
        Initializes the CommandProcessor. This includes:
        - Creating a ZeroMQ context
        - Creating a REP ZeroMQ socket
        - Binding the socket to TCP port 5555
        """

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")




    def process_command(self, command_type, **kwargs):
        """
        Process a command.
        
        Parameters
        ----------
        command_type: str
            The type of command to process. Can be "os" or "compute".
        **kwargs:
            Additional keyword arguments. For "os" commands, these are passed as arguments to the subprocess. For "compute" commands, a required argument is "expression", which is the expression to evaluate.
        
        Returns
        -------
        dict
            A dictionary with a single key. If the command is successful, the key is "output". If the command fails, the key is "error".
        """

        
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
        




    def execute_os_command(self, command_name, *parameters, **kwargs):
        """
        Execute an OS command and return the output as a string.
        
        Parameters
        ----------
        command_name: str
            The name of the command to execute.
        *parameters: 
            Additional parameters to pass to the command.
        **kwargs:
            Additional keyword arguments. An optional argument is "arguments", which is a list of additional arguments to pass to the command.
        
        Returns
        -------
        dict
            A dictionary with a single key. If the command is successful, the key is "output" and the value is the output of the command as a string. If the command fails, the key is "error" and the value is a string describing the error.
        """


        cmd = [command_name] + list(parameters)
        cmd.extend(kwargs.get('arguments', []))
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"output": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            logging.error(f"OS command failed: {e}")
            return {"error": str(e)}




    def evaluate_math_expression(self, expression):
        """
        Evaluate a math expression and return the result as a dict.
        
        Parameters
        ----------
        expression: str
            The math expression to evaluate.
        
        Returns
        -------
        dict
            A dictionary with a single key. If the expression is valid, the key is "result" and the value is the result of the expression. If the expression is invalid, the key is "error" and the value is a string describing the error.
        """



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