const vscode = require('vscode');
const fs = require('fs');

const tokenTypes = ['variable', 'type', 'number', 'comment', 'operator'];
const tokenModifiers = ['declaration', 'definition', 'readonly', 'deprecated', 'modification', 'documentation', 'defaultLibrary'];
let variables = new Set();
const legend = new vscode.SemanticTokensLegend(tokenTypes, tokenModifiers);
const provider = {
    provideDocumentSemanticTokens: (document) => {
        const builder = new vscode.SemanticTokensBuilder(legend);
        const text = document.getText();
        const differential_variable_pattern = /d(\w+)\/dt/g;
        const variable_pattern = /(?<=\n|\s)(\w+)(?=\s*=|:)/g;
        const word_pattern = /\w+/g;

        let match;
        while ((match = differential_variable_pattern.exec(text))) {
            variables.add(match[0].substring(1, match[0].length -3));
        }
        while(match = variable_pattern.exec(text)){
            variables.add(match[0]);
        }
        console.log(variables + 'variables')
        while ((match = word_pattern.exec(text))) {
            if (variables.has(match[0])) {
                const startPos = document.positionAt(match.index);
                const endPos = document.positionAt(match.index + match[0].length);
                builder.push(startPos.line, startPos.character, endPos.character - startPos.character, 0, 0);
            }
        }
        return builder.build();
    }
};
let newArray = Array.from(variables);
const selector = { language: 'brian', scheme: 'file' };
vscode.languages.registerDocumentSemanticTokensProvider(selector, provider, legend);

vscode.languages.registerHoverProvider('brian', {
    provideHover(document, position, token) {
        const docText = document.getText();
        const workspaceFolder = vscode.workspace.getWorkspaceFolder(document.uri);
        return new vscode.Hover('Hello Brian I am Abhishek');
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