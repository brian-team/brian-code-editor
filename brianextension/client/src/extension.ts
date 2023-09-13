"use strict";

const vscode = require('vscode');

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

// const formatter ={
//     provideDocumentFormattingEdits(document): vscode.TextEdit[] {
//       const firstLine = document.lineAt(0);
//       if (firstLine.text !== '42') {
//         return [vscode.TextEdit.insert(firstLine.range.start, '42\n')];
//       }
//     }
//   }
//     new vscode.languages.registerDocumentFormattingEditProvider('python',provider,formatter );

// Below is mostly copied from
// https://github.com/openlawlibrary/pygls/blob/main/examples/json-vscode-extension/client/src/extension.ts

/* -------------------------------------------------------------------------
 * Original work Copyright (c) Microsoft Corporation. All rights reserved.
 * Original work licensed under the MIT License.
 * See ThirdPartyNotices.txt in the project root for license information.
 * All modifications Copyright (c) Open Law Library. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http: // www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ----------------------------------------------------------------------- */

import * as net from "net";
import * as path from "path";
import { ExtensionContext, ExtensionMode, workspace } from "vscode";
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
} from "vscode-languageclient/node";

function isVirtualWorkspace(): boolean {
    const isVirtual = workspace.workspaceFolders && workspace.workspaceFolders.every((f) => f.uri.scheme !== 'file');
    return !!isVirtual;
}

let client: LanguageClient;

function getClientOptions(): LanguageClientOptions {
    return {
        // Register the server for python documents
        documentSelector: isVirtualWorkspace()
        ? [{ language: 'python' }]
        : [
            { scheme: 'file', language: 'python' },
            { scheme: 'untitled', language: 'python' },
            { scheme: 'vscode-notebook', language: 'python' },
            { scheme: 'vscode-notebook-cell', language: 'python' },
        ],
        outputChannelName: "[pygls] BrianLanguageServer",
        synchronize: {
            // Notify the server about file changes to '.clientrc files contain in the workspace
            fileEvents: workspace.createFileSystemWatcher("**/.clientrc"),
        },
    };
}

function startLangServerTCP(addr: number): LanguageClient {
    const serverOptions: ServerOptions = () => {
        return new Promise((resolve /*, reject */) => {
            const clientSocket = new net.Socket();
            clientSocket.connect(addr, "127.0.0.1", () => {
                resolve({
                    reader: clientSocket,
                    writer: clientSocket,
                });
            });
        });
    };

    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        getClientOptions()
    );
}

function startLangServer(
    command: string,
    args: string[],
    cwd: string
): LanguageClient {
    const serverOptions: ServerOptions = {
        args,
        command,
        options: { cwd },
    };

    return new LanguageClient(command, serverOptions, getClientOptions());
}

export function activate(context: ExtensionContext): void {
    if (context.extensionMode === ExtensionMode.Development) {
        // Development - Run the server manually
        client = startLangServerTCP(2087);
    } else {
        // Production - Client is going to run the server (for use within `.vsix` package)
        const cwd = path.join(__dirname, "..", "..");
        const pythonPath = workspace
            .getConfiguration("python")
            .get<string>("pythonPath");

        if (!pythonPath) {
            throw new Error("`python.pythonPath` is not set");
        }

        client = startLangServer(pythonPath, ["-m", "server"], cwd);
    }

    context.subscriptions.push(client.start());
}

export function deactivate(): Thenable<void> {
    return client ? client.stop() : Promise.resolve();
}
