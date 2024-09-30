# Client Server Model With ZMQ

## A simple client server model with python and ZeroMq that runs os commands and simple arithmatic math commands

<br><br>

To use it and test it fallow instructions below:


### 1. Download project

Download the project into your devise or simply clone the project into your virtual environment or any directory
you want by running the
command :

```commandline
git clone https://github.com/HB2102/simple_client_server_with_ZMQ
```



### 2. Install requirements

First you should install the requirements of the project, for that, go to the project directory and run the command :

```commandline
pip install -r requirements/requirements.txt
```

and wait for pip to install packages.


### 3. Run the project
For running the project firs run the "server.py" file with any code runner or run this command in the terminal of the project directory:

```commandline
python server.py
```

or in some cases (some linux users):
```commandline
python3 server.py
```

you can use python3 instead of python in all the following commands.


after running the server we can run the 'client.py' by the order. The client supports two types of commands, OS and OS commands and Math
commands. 


### 3. Run OS Commands
For running the os command use the patern below:

```commandline
python client.py os [command name] [command arguments]
```

for example the below command shows directories in the root of OS:
```commandline
python client.py os ls /
```

or this command makes a directory with the name AZMA:
```commandline
python client.py os mkdir AZMA
```


### 4. Run Math Commands
You can use math commands to evaluate simple arithmatic expressions with this pattern:

```commandline
python client.py compute "[expression]"
```

for example:
```commandline
python client.py compute "(2 + 2) * 10" 
```

output:
```json
{
  "result": 40
}
```


Thank you for your time.