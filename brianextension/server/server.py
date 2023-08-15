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
    TEXT_DOCUMENT_COMPLETION,
)
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionOptions,
    CompletionParams,
)
from pygls.server import LanguageServer

class BrianLanguageServer(LanguageServer):

    CONFIGURATION_SECTION = "jsonServer"

    def __init__(self, *args):
        super().__init__(*args)


brian_server = BrianLanguageServer("pygls-brian-example", "v0.1")


@brian_server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions()
)
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""
    from brian2.core.functions import DEFAULT_CONSTANTS, DEFAULT_FUNCTIONS
    constants = [CompletionItem(label=c, kind=CompletionItemKind.Constant)
                    for c in DEFAULT_CONSTANTS]
    functions = [CompletionItem(label=f, kind=CompletionItemKind.Function)
                    for f in DEFAULT_FUNCTIONS]

    from brian2.units.allunits import __all__ as ALL_UNITS
    units = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in ALL_UNITS]



    return CompletionList(
        is_incomplete=False,
        items=constants + functions+units,
    )

def definition(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""
    from brian2.core.functions import DEFAULT_CONSTANTS, DEFAULT_FUNCTIONS
    constants = [CompletionItem(label=c, kind=CompletionItemKind.Constant)
                    for c in DEFAULT_CONSTANTS]
    functions = [CompletionItem(label=f, kind=CompletionItemKind.Function)
                    for f in DEFAULT_FUNCTIONS]

    from brian2.units.allunits import __all__ as ALL_UNITS
    units = [CompletionItem(label=u, kind=CompletionItemKind.Unit)
                    for u in ALL_UNITS]



    return CompletionList(
        is_incomplete=False,
        items=constants + functions+units,
    )