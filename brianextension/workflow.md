# Project workflow

## BrianLang/Syntax
  - Brian.injection.json
     - This file is used to inject the BrianLang syntax into the Python File
  - Brian.tmLanguage.json
      - This file is used to define the syntax highlighting for the BrianLang syntax

## Client/src/extension.ts
  - This file is used to define the extension and the commands that are used in the extension
      - here's a brief explanation of each function:

      - isVirtualWorkspace(): This function checks if the current workspace is virtual or not. A virtual workspace is one that does not have any files on the local file system, but instead uses a remote or cloud-based file system.

      - getClientOptions(): This function returns an object that specifies the options for the language client. It registers the server for Python documents and sets up file synchronization.

      - startLangServerTCP(addr: number): This function starts a language server using TCP. It creates a new promise that resolves with a reader and writer for the client socket.

      - startLangServer(command: string, args: string[], cwd: string): This function starts a language server using a command and arguments. It creates a new server options object with the command, arguments, and current working directory.

## Server/server.py
  - The BrianLanguageServer class is the main class for the language server.
  - The EquationFinder class is used to find equations in the code.
  - The is_in_Equations function checks if the user is currently in the Equations() block.
  - The did_open and did_change functions are used to publish diagnostics when a text document is opened or changed.
  - The get_diagnostics function is used to get diagnostics for equations in the code.
  - The completions function provides completion items for the code, including constants, functions, units, and special symbols. It also checks if the user is currently in an equation block and provides completion items accordingly.
