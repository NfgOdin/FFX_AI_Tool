# FFX Monster AI & Stats Editor (FFX-AI-Tool)

An editor for managing, decompiling, disassembling, and editing monster stats and battle script AI (Atel) files in Final Fantasy X.

## Features

- **Monster Stats Editor**: Modify HP, MP, attributes, elemental resistances, and other monster stats.
- **Battle Script AI Editor**: Decompile, edit, compile, and inject custom Atel script rules for monster AI behavior.
- **Easy Packing**: Pack monster files back into the game data formats.
- **Dark Theme GUI**: Modern, user-friendly Dark Mode interface built using `tkinter` / `ttk`.

## Requirements

- Python 3.8 or higher
- `tkinter` (usually bundled with standard Python installations)

## Getting Started

### Running from Source
To run the editor directly from source:
```bash
python FFX_AI_Tool.py
```

### Building the Executable
You can build a standalone Windows executable (`FFX_AI_Tool.exe`) using PyInstaller:
```bash
pip install pyinstaller
pyinstaller FFX_AI_Tool.spec
```
The compiled executable will be located in the `dist` folder.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
