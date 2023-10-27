# The Debuggers - Backend

## Setup

- Clone the respository
- Go the project directory
- Set up a virtual environment

```bash
virtualenv -p python3 env
source ./venv/bin/activate
```

- Install dependencies

```bash
pip install -r requirements.txt
```

- Create database `the_debuggers`
- copy .env.example to .env and set the variables in environment

```bash
cp .env.example .env
```

- Start the server

```bash
python main.py
```

Server will be started, when done working deactivate the virtual environment using

```bash
deactivate
```
