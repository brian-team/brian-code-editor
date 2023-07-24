import * as vscode from 'vscode';
const tokenTypes = ['variable', 'type', 'number', 'comment', 'operator'];
const tokenModifiers = ['declaration', 'definition', 'readonly', 'deprecated', 'modification', 'documentation', 'defaultLibrary'];
console.log('semanticToken.js')
const legend = new vscode.SemanticTokensLegend(tokenTypes, tokenModifiers);

const provider = {
    provideDocumentSemanticTokens: (document) => {
        const builder = new vscode.SemanticTokensBuilder(legend);
        const text = document.getText();
        const variable_pattern = /d(\w+)\/dt/g;
        const word_pattern = /\w+/g;
        let variables = [];
        let match;
        while ((match = variable_pattern.exec(text))) {
            variables.push(match[0].substring(1, match[0].length - 3));
        }
        console.log(variables + 'variables')
        while ((match = word_pattern.exec(text))) {
            if (variables.indexOf(match[0]) != -1) {
                const startPos = document.positionAt(match.index);
                const endPos = document.positionAt(match.index + match[0].length);
                builder.push(startPos.line, startPos.character, endPos.character - startPos.character, 0, 0);
            }
        }
        return builder.build();
    }
};

const selector = { language: 'brian', scheme: 'file' };
