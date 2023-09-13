To prepare everything to run the language server/client, do the following:
- Create a virtual environment for Python, e.g. using the built-in venv module in the current directory:
    - python3 -m venv env
    - source env/bin/activate
- Install the dependencies (pygls and brian2)
    - python -m pip install -r requirements.txt
- Install the node modules (assumes you have npm installed)
    - npm install
    - cd client
    - npm install
- Start Visual Studio Code and open the current directory (*not* the parent directory)
- Open debug view (`ctrl + shift + D`)
- Select `Server + Client` and press `F5`

This will open a new window with the extension loaded and start the server. In the original Visual Studio Code window, you can add breakpoints for debugging. If you make changes, restart the server/client.
