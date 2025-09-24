# Vyper LSP For VSCode

Vyper language server extension for Visual Studio Code.

## About

This project is an **alpha release** of a Visual Studio Code extension that provides a language server for [Vyper](https://vyper.readthedocs.io/), a smart contract programming language.

Please note that this is a work in progress, and some features may be incomplete or subject to change as development continues.

This extension is a client that relies on [Couleuvre](https://github.com/trocher/couleuvre), a Vyper language server implementation. By default, the extension uses the `couleuvre` package bundled with the extension, but you can also use one available in your environment.

## Features

- **Jump to definition**: Navigate to the definition of variables, functions, and contracts within your Vyper code.
- **Find symbols**: Quickly locate symbols in your Vyper files.
- **Go to modules**: Easily navigate to imported modules in your Vyper projects.

## Setting Up

By default, the extension is compatible with any Vyper version without any additional setup required.

Resolving external dependencies is what is trickier.

- By default, the extension will try to use the python interpreter inherited from VSCode (`Python: Select Interpreter`) and its corresponding `sys.path` to look for external dependencies (e.g. `snekmate`)
- If Vyper is not installed in that environment, or the contract uses another version of Vyper, the server will work with a managed environement, but external dependencies will not be resolved.

- More advanced users can specify a specific Python interpreter to use via the `vyper.interpreter` setting. This is useful if you want to specify a different environment than the one used by VSCode, in which case:
  - Couleuvre should be installed in that environment.
  - Any Vyper external imports (e.g. snekmate) are resolved relative to the interpreter's environment.

## Disclaimer

This extension is in early development, use at your own risk. Couleuvre is not affiliated with the Vyper project.
