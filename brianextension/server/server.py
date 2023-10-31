############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
from typing import Optional
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionOptions,
    CompletionList,
    CompletionParams,
    Diagnostic,
    TextDocumentPublishDiagnosticsNotification,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    Range,
    Position,
)
from pygls.server import LanguageServer
import ast

Flag_List = ['event-driven','unless refractory','constant','constant over dt','shared','linked']

list_of_special_symbols = ['dt','i','j','lastspike','lastupdate','N','not_refractory','t','t_in_timesteps']

Base_units =  ['Hz', 'amp', 'ampere', 'becquerel', 'candle', 'coulomb', 'farad', 'gray', 'henry', 'hertz', 'joule', 'katal', 'kelvin', 'kilogram', 'kliter', 'lumen', 'lux', 'mM', 'meter', 'mmolar', 'mol',  'newton', 'ohm', 'pascal', 'radian', 'second', 'siemens', 'sievert', 'steradian', 'tesla', 'volt', 'watt', 'weber']

class BrianLanguageServer(LanguageServer):
    CONFIGURATION_SECTION = "jsonServer"
    def __init__(self, *args):
        super().__init__(*args)
brian_server = BrianLanguageServer("pygls-brian-example", "v0.1")

class EquationFinder(ast.NodeVisitor):
    def __init__(self, node):
        self.eq_lines = []
        self.eq_constants = []
        self.visit(node)

    def visit_Call(self, node):
        if getattr(node.func, 'id', None) == 'Equations':
            self.eq_lines.append((node.args[0].lineno, node.args[0].end_lineno))
            if isinstance(node.args[0], ast.Constant):
                self.eq_constants.append(node.args[0].value)
            else:
                self.eq_constants.append(None)
        self.generic_visit(node)

def is_in_Equations(params: Optional[CompletionParams] = None) -> bool:
    """Returns True if the user is currently in the `Equations()` block and False otherwise."""

    text_document = params.text_document.uri # provide the link
    text = brian_server.workspace.get_document(text_document).source # give text
    parsed = ast.parse(text)
    finder = EquationFinder(parsed)
    for start, end in finder.eq_lines:
        if start <= params.position.line + 1 <= end:
            return True
    return False

@brian_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    text = brian_server.workspace.get_document(params.text_document.uri).source
    diagnostics = get_diagnostics(text)
    ls.publish_diagnostics(params.text_document.uri, diagnostics)


@brian_server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    text = brian_server.workspace.get_document(params.text_document.uri).source
    diagnostics = get_diagnostics(text)
    ls.publish_diagnostics(params.text_document.uri, diagnostics)


def get_diagnostics(text):
    # Get the lines with equations (if any)
    eq_finder = EquationFinder(ast.parse(text))
    eqs_lines = eq_finder.eq_lines
    eqs_constants = eq_finder.eq_constants

    diagnostics = []
    for (start, end), eqs_value in zip(eqs_lines, eqs_constants):
        try:
            from brian2.equations.equations import Equations
            if eqs_value is None:
                # An equation, but one that isn't defined with a string (maybe a variable?)
                continue
            # Try to parse the equations
            Equations(eqs_value)
        except Exception as e:
            # If there is an error, create a diagnostic
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(start, 0),
                    end=Position(end, 0)
                ),
                message=str(e),
                severity=1,
                source='Brian Language Server'
            ))
    return diagnostics


@brian_server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions()
)
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    if is_in_Equations(params):

        from brian2.core.functions import DEFAULT_CONSTANTS, DEFAULT_FUNCTIONS
        constants = [CompletionItem(label=c, kind=CompletionItemKind.Constant)
                        for c in DEFAULT_CONSTANTS]

        functions = [CompletionItem(label=f, kind=CompletionItemKind.Function)
                        for f in DEFAULT_FUNCTIONS]

    # Units module - https://brian2.readthedocs.io/en/stable/reference/brian2.units.html
        from brian2.units.allunits import __all__ as ALL_UNITS
        units_all_units = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_UNITS]

        from brian2.units.fundamentalunits import __all__ as ALL_FUNDAMENTALUNITS
        units_fundamentalunits = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_FUNDAMENTALUNITS]
        from brian2.units.stdunits import __all__ as ALL_STDUNITS
        units_stdunits = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_STDUNITS]

        special_symbols = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in list_of_special_symbols]



        cursor_pos = params.position.character
        text = brian_server.workspace.get_document(params.text_document.uri).source
        line_content = text.splitlines()[params.position.line][:cursor_pos]
        pre_line_content = text.splitlines()[params.position.line-1][:cursor_pos]
        if '=' in line_content:
            # between = and :
            if ':' not in line_content:
                # complete all
                return CompletionList(
                is_incomplete=False,
                items=constants + functions+units_all_units +units_fundamentalunits +units_stdunits +special_symbols,
                )
            elif ':' in line_content:
                # complete special symbols and flags and base units
                flag = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in Flag_List]


                base_unit = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in Base_units]

                return CompletionList(
                    is_incomplete=False,
                    items =base_unit+flag,
                )

        elif ':' not in pre_line_content:
            # line break
                # complete all
                return CompletionList(
                is_incomplete=False,
                items=constants + functions+units_all_units +units_fundamentalunits +units_stdunits +special_symbols,
                )
        elif ':' in line_content:
                # complete special symbols and flags and base units
                flag = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in Flag_List]


                base_unit = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in Base_units]

                return CompletionList(
                    is_incomplete=False,
                    items =base_unit+flag,
                )

