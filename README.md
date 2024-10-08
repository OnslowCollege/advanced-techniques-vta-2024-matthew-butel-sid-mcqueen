## Python Template

Use this template to develop a text-based program in Python 3.12.

This template includes:

- Default code file (`main.py`)
- Extensions to support Python development
- Ruff linter/formatter enabled to ensure code follows conventions
- mypy integration to ensure code follows PEP-484 (type hint annotations)
- Pip Manager, to easily download external Python packages
- Integration for diagrams.net (for files ending in `.drawio`)

## How to run your code

Once your Codespace has loaded:

1. to debug your code, click on the drop-down arrow next to the ▶️ play icon at the top-right of the screen and select "Debug Python file" (or press F5)
2. to run without debugging, click on the ▶️ play icon (or press Ctrl-F5)
3. to run your code in a REPL environment, click on the red cat icon next to the ▶️ play icon

## How to install PostgreSQL

Run these commands in the Terminal:

```bash
sudo apt update
sudo apt install postgresql
sudo service postgresql start
```

## How to connect to PostgreSQL

```bash
sudo su postgres -c psql template1
```

## How to check server status and start it 

service postgresql status

sudo service postgresql start
Then run...

```sql
ALTER USER postgres WITH PASSWORD '123456';
\q
```
