# FFX Monster AI & Stats Editor (FFX-AI-Tool)

A comprehensive Python-based desktop application designed to modify and compile the monster files from **Final Fantasy X**. It features a modern, dark-themed GUI for editing stats, disassembling and decompiling the battle AI scripts (Atel), and repacking the files back into their original game chunk structure.

---

## Key Features

- 🛠️ **Monster Stats Editing**: Read and modify core attributes (HP, MP, Strength, Defense, Agility, etc.), elemental properties (Weak, Resist, Immune, Absorb), status immunities, and item drops.
- 📜 **Battle Script AI Editor**: Disassemble and decompile the compiled battle script bytecode (Atel) into a readable rules syntax, modify it, and compile/inject it back into the monster file.
- 📦 **Chunk Repacking & Packing**: Work directly with the multi-chunk FFX monster file format. Automatically separates, edits, and repacks the chunks together.
- 🔠 **FFX Character Encoding Support**: Decode and encode FFX's custom text table mapping with SJIS-like string offsets.
- 🎨 **Modern Dark Mode Interface**: Built using Custom-styled `tkinter` and `ttk` styles for high accessibility and high visual appeal.

---

## File Format & Chunk Architecture

FFX monster files are organized into a multi-chunk structure header, usually consisting of 7 distinct segments:

| Chunk | Description |
|---|---|
| **Chunk 0** | Monster Core Stats (HP, MP, attributes, resistances, item rewards) |
| **Chunk 1** | Battle AI Script bytecode (Atel Engine) |
| **Chunk 2** | Localized text/strings (custom encoding) |
| **Chunks 3-6**| Animation, visual layout, and extra game assets |

The packer utility parses this file layout, manages section offsets, handles padding requirements, and compiles files seamlessly.

---

## Prerequisites

- **Python 3.8+**
- **tkinter** (usually included in standard Python installations on Windows/macOS; Linux users may need to run `sudo apt-get install python3-tk`).

---

## Installation & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/FFX-AI-Tool.git
   cd FFX-AI-Tool
   ```

2. **Run the editor from source:**
   ```bash
   python FFX_AI_Tool.py
   ```

---

## Building a Standalone Executable

You can compile the editor into a single standalone `.exe` using PyInstaller.

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   pyinstaller FFX_AI_Tool.spec
   ```
   
The built executable will be located in the `dist/` directory.

---

## Repository Structure

- [FFX_AI_Tool.py](file:///c:/Users/jonat/Desktop/Modding/Final%20Fantasy%20X&X2%20Modding/Custom%20FFX%20Tools/FFX-AI-Tool/FFX_AI_Tool.py): Main graphical user interface and application driver.
- [ffx_atel.py](file:///c:/Users/jonat/Desktop/Modding/Final%20Fantasy%20X&X2%20Modding/Custom%20FFX%20Tools/FFX-AI-Tool/ffx_atel.py): Atel engine disassembler, decompiler, compiler, and injection mechanics.
- [ffx_codec.py](file:///c:/Users/jonat/Desktop/Modding/Final%20Fantasy%20X&X2%20Modding/Custom%20FFX%20Tools/FFX-AI-Tool/ffx_codec.py): Custom FFX sjis/byte text encoding and translation map decoder.
- [ffx_monster_packer.py](file:///c:/Users/jonat/Desktop/Modding/Final%20Fantasy%20X&X2%20Modding/Custom%20FFX%20Tools/FFX-AI-Tool/ffx_monster_packer.py): Unpacker/repacker utility handling FFX's 7-chunk file format.
- [FFX_AI_Tool.spec](file:///c:/Users/jonat/Desktop/Modding/Final%20Fantasy%20X&X2%20Modding/Custom%20FFX%20Tools/FFX-AI-Tool/FFX_AI_Tool.spec): PyInstaller build specification.

---

## License

Licensed under the MIT License. See `LICENSE` for more information.
