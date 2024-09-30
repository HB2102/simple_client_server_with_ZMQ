import json
import zmq
import sys


def send_command(command_type, **kwargs):
    """
    Send a command to the server and print the response.

    :param command_type: Either "os" or "compute", indicating the type of command to send.
    :param **kwargs: Additional arguments to be passed to the server, depending on the command type.

    The function sends a JSON message to the server, consisting of the command type and
    any additional arguments. The server's response is then printed to the console.

    :raises Exception: If there is an error sending or receiving the message.
    """

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    try:
        message = {"command_type": command_type, **kwargs}
        socket.send_json(message)
        response = socket.recv_json()
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error sending command: {str(e)}")
    finally:
        socket.close()




if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <command_type> [<arguments>...]")
        sys.exit(1)

    command_type = sys.argv[1]

    if command_type == 'compute':
        expression = sys.argv[2]
        kwargs = {"expression": expression}

    elif command_type == 'os':
        command_name = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        
        kwargs = {"command_name": command_name}
        if args:
            kwargs["arguments"] = args
        

    send_command(command_type, **kwargs)
