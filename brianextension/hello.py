import vscode

def extract_brian_file_content(file_path):
    return vscode.commands.executeCommand('extension.extractBrianFileContent', file_path)