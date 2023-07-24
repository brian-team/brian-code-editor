const vscode = require('vscode');
const fs = require('fs');

vscode.languages.registerHoverProvider('brian', {
    provideHover(document, position, token) {
        const docText = document.getText();
        const workspaceFolder = vscode.workspace.getWorkspaceFolder(document.uri);
        console.log("hello abhishek yaha me hu")
        return new vscode.Hover('I am a hover!');
    }
});

function extractBrianFileContent(filePath) {
    return new Promise((resolve, reject) => {
        const fileExtension = filePath.split('.').pop();

        if (fileExtension === 'brian') {
            fs.readFile(filePath, 'utf-8', (error, content) => {
                if (error) {
                    reject(error.message);
                } else {
                    resolve(content);
                }
            });
        } else {
            reject('Please provide a .brian file to extract its content.');
        }
    });
}

function activate(context) {
    context.subscriptions.push(vscode.commands.registerCommand('extension.extractBrianFileContent', extractBrianFileContent));
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};