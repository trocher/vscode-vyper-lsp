# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Implementation of tool support over LSP."""

from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Any, Optional


# **********************************************************
# Update sys.path before importing any bundled libraries.
# **********************************************************
def update_sys_path(path_to_add: str, strategy: str) -> None:
    """Add given path to `sys.path`."""
    if path_to_add not in sys.path and os.path.isdir(path_to_add):
        if strategy == "useBundled":
            sys.path.insert(0, path_to_add)
        elif strategy == "fromEnvironment":
            sys.path.append(path_to_add)


# Ensure that we can import LSP libraries, and other bundled libraries.
update_sys_path(
    os.fspath(pathlib.Path(__file__).parent.parent / "libs"),
    os.getenv("LS_IMPORT_STRATEGY", "useBundled"),
)

# **********************************************************
# Imports needed for the language server goes below this.
# **********************************************************
# pylint: disable=wrong-import-position,import-error
import lsp_jsonrpc as jsonrpc
import lsprotocol.types as lsp
from pygls import uris
import couleuvre

WORKSPACE_SETTINGS = {}
GLOBAL_SETTINGS = {}
RUNNER = pathlib.Path(__file__).parent / "lsp_runner.py"

MAX_WORKERS = 5

LSP_SERVER = couleuvre.server

# **********************************************************
# Tool specific code
# **********************************************************

# Reference:
#  LS Protocol:
#  https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/
#
#  Sample implementations:
#  Pylint: https://github.com/microsoft/vscode-pylint/blob/main/bundled/tool
#  Black: https://github.com/microsoft/vscode-black-formatter/blob/main/bundled/tool
#  isort: https://github.com/microsoft/vscode-isort/blob/main/bundled/tool

TOOL_MODULE = "couleuvre"

TOOL_DISPLAY = "Vyper LSP"

TOOL_ARGS = []  # default arguments always passed to couleuvre.


# **********************************************************
# Required Language Server Initialization and Exit handlers.
# **********************************************************
@LSP_SERVER.feature(lsp.INITIALIZE)
def initialize(params: lsp.InitializeParams) -> None:
    """LSP handler for initialize request."""
    log_to_output(f"CWD Server: {os.getcwd()}")

    paths = "\r\n   ".join(sys.path)
    log_to_output(f"sys.path used to run Server:\r\n   {paths}")

    GLOBAL_SETTINGS.update(**params.initialization_options.get("globalSettings", {}))

    settings = params.initialization_options["settings"]
    _update_workspace_settings(settings)
    log_to_output(
        f"Settings used to run Server:\r\n{json.dumps(settings, indent=4, ensure_ascii=False)}\r\n"
    )
    log_to_output(
        f"Global settings:\r\n{json.dumps(GLOBAL_SETTINGS, indent=4, ensure_ascii=False)}\r\n"
    )


@LSP_SERVER.feature(lsp.EXIT)
def on_exit(_params: Optional[Any] = None) -> None:
    """Handle clean up on exit."""
    jsonrpc.shutdown_json_rpc()


@LSP_SERVER.feature(lsp.SHUTDOWN)
def on_shutdown(_params: Optional[Any] = None) -> None:
    """Handle clean up on shutdown."""
    jsonrpc.shutdown_json_rpc()


def _get_global_defaults():
    return {
        "path": GLOBAL_SETTINGS.get("path", []),
        "interpreter": GLOBAL_SETTINGS.get("interpreter", [sys.executable]),
        "args": GLOBAL_SETTINGS.get("args", []),
        "importStrategy": GLOBAL_SETTINGS.get("importStrategy", "useBundled"),
        "showNotifications": GLOBAL_SETTINGS.get("showNotifications", "off"),
    }


def _update_workspace_settings(settings):
    if not settings:
        key = os.getcwd()
        WORKSPACE_SETTINGS[key] = {
            "cwd": key,
            "workspaceFS": key,
            "workspace": uris.from_fs_path(key),
            **_get_global_defaults(),
        }
        return

    for setting in settings:
        key = uris.to_fs_path(setting["workspace"])
        WORKSPACE_SETTINGS[key] = {
            "cwd": key,
            **setting,
            "workspaceFS": key,
        }


# *****************************************************
# Logging and notification.
# *****************************************************
def log_to_output(
    message: str, msg_type: lsp.MessageType = lsp.MessageType.Log
) -> None:
    LSP_SERVER.window_log_message(lsp.LogMessageParams(message=message, type=msg_type))


def log_error(message: str) -> None:
    LSP_SERVER.window_log_message(lsp.LogMessageParams(message=message, type=lsp.MessageType.Error))
    if os.getenv("LS_SHOW_NOTIFICATION", "off") in ["onError", "onWarning", "always"]:
        LSP_SERVER.window_show_message(lsp.ShowMessageParams(message=message, type=lsp.MessageType.Error))


def log_warning(message: str) -> None:
    LSP_SERVER.window_log_message(lsp.LogMessageParams(message=message, type=lsp.MessageType.Warning))
    if os.getenv("LS_SHOW_NOTIFICATION", "off") in ["onWarning", "always"]:
        LSP_SERVER.window_show_message(lsp.ShowMessageParams(message=message, type=lsp.MessageType.Warning))


def log_always(message: str) -> None:
    LSP_SERVER.window_log_message(lsp.LogMessageParams(message=message, type=lsp.MessageType.Info))
    if os.getenv("LS_SHOW_NOTIFICATION", "off") in ["always"]:
        LSP_SERVER.window_show_message(lsp.ShowMessageParams(message=message, type=lsp.MessageType.Info))


# *****************************************************
# Start the server.
# *****************************************************
if __name__ == "__main__":
    LSP_SERVER.start_io()
