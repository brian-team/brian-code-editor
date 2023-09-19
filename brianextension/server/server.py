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
    TEXT_DOCUMENT_COMPLETION
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
        self.visit(node)

    def visit_Call(self, node):
        if getattr(node.func, 'id', None) == 'Equations':
            self.eq_lines.append((node.args[0].lineno, node.args[0].end_lineno))
        self.generic_visit(node)

def is_in_Equations(params: Optional[CompletionParams] = None) -> bool:
    """Returns True if the user is currently in the `Equations()` block and False otherwise."""

    text_document = params.text_document.uri
    text = brian_server.workspace.get_document(text_document).source
    parsed = ast.parse(text)
    finder = EquationFinder(parsed)
    for start, end in finder.eq_lines:
        if start <= params.position.line + 1 <= end:
            return True
    return False


@brian_server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions()
)
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    if is_in_Equations(params):
        #  for each line we have to check if the cursor is before = between = and : or after :
        #  if before = we need no completion
        #  if between = and : we need to complete the variable name
        #  if after : we need to complete the flag name

        from brian2.core.base import __all__ as ALL_BASE
        base = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in ALL_BASE]

        from brian2.core.clocks import __all__ as ALL_CLOCK
        clock = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_CLOCK]

        from brian2.core.core_preferences import __all__ as ALL_CORE_PREFERENCES
        core_preferences = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_CORE_PREFERENCES]

        from brian2.core.functions import DEFAULT_CONSTANTS, DEFAULT_FUNCTIONS
        constants = [CompletionItem(label=c, kind=CompletionItemKind.Constant)
                        for c in DEFAULT_CONSTANTS]

        functions = [CompletionItem(label=f, kind=CompletionItemKind.Function)
                        for f in DEFAULT_FUNCTIONS]

        from brian2.core.magic import __all__ as ALL_MAGIC
        magic = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_MAGIC]

        from brian2.core.names import __all__ as ALL_NAMES
        names = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_NAMES]

        from brian2.core.namespace import __all__ as ALL_NAMESPACE
        namespace = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_NAMESPACE]

        from brian2.core.network import __all__ as ALL_NETWORK
        network = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_NETWORK]

        from brian2.core.variables import __all__ as ALL_VARIABLES
        variables = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_VARIABLES]

        from brian2.core.operations import __all__ as ALL_OPERATIONS
        operations = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_OPERATIONS]

        from brian2.core.preferences import __all__ as ALL_PREFERENCES
        preferences = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_PREFERENCES]

        from brian2.core.spikesource import __all__ as ALL_SPIKESOURCE
        spikesource = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_SPIKESOURCE]

        from brian2.core.tracking import __all__ as ALL_TRACKING
        tracking = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_TRACKING]

        from brian2.core.variables import __all__ as ALL_VARIABLES
        variables = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_VARIABLES]



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
        from brian2.units.unitsafefunctions import __all__ as ALL_UNITSAFEFUNCTIONS
        units_unitsafefunctions = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_UNITSAFEFUNCTIONS]


        # Utils module - https://github.com/brian-team/brian2/tree/master/brian2/utils
        from brian2.utils.logger import __all__ as ALL_LOGGER
        loggers = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_LOGGER]

        # Synapse module - https://brian2.readthedocs.io/en/stable/reference/brian2.synapses.html
        from brian2.synapses.synapses import __all__ as ALL_SYNAPSES
        synapses = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_SYNAPSES]

        # StateUpdaters module - https://brian2.readthedocs.io/en/stable/reference/brian2.stateupdaters.html
        from brian2.stateupdaters import __all__ as ALL_STATEUPDATERS
        stateupdaters = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_STATEUPDATERS]

        # spatialneuron - https://github.com/brian-team/brian2/blob/master/brian2/spatialneuron/__init__.py
        from brian2.spatialneuron import __all__ as ALL_SPATIALNEURON
        spatialneuron = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_SPATIALNEURON]

        # parsing
        # monitors - https://github.com/brian-team/brian2/blob/master/brian2/monitors/__init__.py
        from brian2.monitors import __all__ as ALL_MONITORS
        monitors = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_MONITORS]

        #input
        from brian2.input import __all__ as ALL_INPUT
        input = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_INPUT]

        # ImportExport - https://github.com/brian-team/brian2/blob/master/brian2/importexport/__init__.py
        from brian2.importexport import __all__ as ALL_IMPORTEXPORT
        importexport = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_IMPORTEXPORT]

        # Groups - https://github.com/brian-team/brian2/blob/master/brian2/groups/__init__.py
        from brian2.groups import __all__ as ALL_GROUPS
        groups = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_GROUPS]

        # Equations - https://github.com/brian-team/brian2/blob/master/brian2/equations/__init__.py
        from brian2.equations import __all__ as ALL_EQUATIONS
        equations = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                        for u in ALL_EQUATIONS]


        cursor_pos = params.position.character
        text = brian_server.workspace.get_document(params.text_document.uri).source
        line_content = text.splitlines()[params.position.line][:cursor_pos]
        if '=' in line_content:
            # between = and :
            if ':' not in line_content:
                # complete all
                return CompletionList(
            is_incomplete=False,
            items=constants + functions+units_all_units +units_fundamentalunits +units_stdunits +units_unitsafefunctions +loggers+synapses+stateupdaters+spatialneuron+monitors+input+importexport+groups+equations+names+namespace+network+variables+operations+preferences+spikesource+tracking+base+clock+core_preferences+magic,
    )

            else:
                # complete special symbols and flags and base units
                flag = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in Flag_List]

                special_symbols = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in list_of_special_symbols]

                base_unit = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in Base_units]

                return CompletionList(
                    is_incomplete=False,
                    items =special_symbols+base_unit+flag,
                )



