import * as vscode from 'vscode';
vscode.languages.registerHoverProvider('brian', {
    provideHover(document, position, token) {
        const docText = document.getText();
        const workspaceFolder = vscode.workspace.getWorkspaceFolder(document.uri);
        console.log("hello abhishek yaha me hu")
        return new vscode.Hover('I am a hover!');

    }
});