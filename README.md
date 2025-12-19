# Vyper LSP For VSCode

[![VSCode Version](https://vsmarketplacebadges.dev/version/trocher.vyper.png)](https://marketplace.visualstudio.com/items?itemName=trocher.vyper)
[![VSCode Downloads](https://vsmarketplacebadges.dev/downloads-short/trocher.vyper.png)](https://marketplace.visualstudio.com/items?itemName=trocher.vyper)

[![Open VSX Version](https://img.shields.io/open-vsx/v/trocher/vyper)](https://open-vsx.org/extension/trocher/vyper)
[![Open VSX Downloads](https://img.shields.io/open-vsx/dt/trocher/vyper)](https://open-vsx.org/extension/trocher/vyper)



Vyper language server extension for Visual Studio Code.

- VSCode Marketplace: https://marketplace.visualstudio.com/items?itemName=trocher.vyper
- Open VSX: https://open-vsx.org/extension/trocher/vyper

## About

This project is an **alpha release** of a Visual Studio Code extension that provides a language server for [Vyper](https://vyper.readthedocs.io/), a smart contract programming language.

Please note that this is a work in progress, and some features may be incomplete or subject to change as development continues.

This extension is a client that relies on [Couleuvre](https://github.com/trocher/couleuvre), a Vyper language server implementation. By default, the extension uses the `couleuvre` package bundled with the extension, but you can also use one available in your environment.

## Features

- **Jump to definition**: Navigate to the definition of variables, functions, and contracts within your Vyper code.
- **Go to modules**: Easily navigate to imported modules in your Vyper projects.
- **Jump to references**: Find all references to a symbol in your Vyper files.
- **Find symbols**: Quickly locate symbols in your Vyper files.
- **Diagnostics**: Get real-time feedback on syntax and semantic errors in your Vyper code.
- **Auto-completion**: Benefit from intelligent code completion suggestions as you type.

## Setting Up

By default, the extension is compatible with any Vyper version without any additional setup required.

Resolving external dependencies is what is trickier.

- By default, the extension will try to use the python interpreter inherited from VSCode (`Python: Select Interpreter`) and its corresponding `sys.path` to look for external dependencies (e.g. `snekmate`)
- If Vyper is not installed in that environment, or the contract uses another version of Vyper, the server will work with a managed environement, but external dependencies will not be resolved.

### Advanced Configuration

More advanced users can specify a specific Python interpreter to use via the `vyper.interpreter` setting. This is useful if you want to specify a different environment than the one used by VSCode, in which case:
  - [Couleuvre](https://github.com/trocher/couleuvre) should be installed in that environment.
  - Any Vyper external imports (e.g. snekmate) are resolved relative to the interpreter's environment.

## Disclaimer

This extension is in early development, use at your own risk. This extension is not affiliated with the Vyper project.
