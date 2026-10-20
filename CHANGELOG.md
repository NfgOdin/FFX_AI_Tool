# Final Fantasy X Monster AI & Stats Editor — Changelog

## [v1.2.0] — 2026-10-19

### 🌟 Major Highlights & New Features

#### 👾 1. Overhauled Visual AI Rule Builder (Multi-Hook & Boss State Machine Architecture)
* **Dynamic Chunk 1 Event Hook Resolution**: Automatically parses `Chunk 1` (`role == 2` Combat AI Worker and its 21 `uint16` event hook table) to resolve and edit all 9 battle event hooks (`⚡ Active Turn`, `🛡 Counter / React`, `💥 On Damage`, `💀 On Death`, `⏳ Pre-Turn`, `🎬 Battle Start`, `🎯 On Targeted`, `📐 Post-Turn`, `⏱ Status Tick`) across all 361 monsters and bosses.
* **Unmapped Hook Enabling**: Added one-click & automatic `Chunk 1` hook slot enabling (`enable_chunk1_hook_slot`) so Counter-Attack, On-Damage, and On-Death scripts can be added to any enemy even if originally unmapped (`0xFFFF`).
* **Phase & State Variable Gates**: Added support for local worker variable gates (`var_00..var_1F` with `==, !=, <, <=, >, >=` operators) and post-action variable mutations (`Set`, `Add`, `Reset`) to build multi-phase bosses, attack rotation loops, and damage-hit counters.
* **Composite Conditions (`AND` / `OR`) & Authentic Battle Engine Checks**: Added composite condition chaining, dynamic HP/MP ratio math (`GetProperty(-13, 0) * 100 < GetProperty(-13, 2) * pct`), Party Status mask checks (`0x701E`), Self Status checks (`0x700F`), Counter triggers (`Damage Taken > 0`, `Last Hit Was Physical / Magical`, `Last Hit Was Normal Attack`), and Alive Party/Monster counts.
* **Complete Target Selection System**: Added 31 targeting presets including `Random Alive Party`, `All Active Party`, `Self`, `All Allied Monsters`, `Random Allied Monster`, `Last Attacker`, `Provoker`, `Lowest/Highest HP/MP Party`, `Party With/Without Status`, specific characters (`Tidus` through `Rikku`), and specific monster formation slots (`Monster Slot 0..3`).
* **Multi-Action Turn Flow & Counter Opcode Support**: Added support for `Return (End Turn)` vs. `Continue (Multi-Action / Combo)` per rule and `ExecuteAction (0x700B)` vs. `ExecuteCounterAction (0x705A)`.
* **Searchable Action Filter, Live Pseudocode Preview & Upgraded Flowchart**: Added real-time ability filtering, live hook pseudocode preview, rule duplication, 7 comprehensive AI templates, and an upgraded Visual AI Flowchart rendering phase gates, composite conditions, variable mutations, and `Return`/`Continue` paths.

---

### 🔧 Bug Fixes & Improvements
* **Safe In-Place Atel Chunk 0 Binary Rebuilder**: Replaced the legacy append-only `inject_rules` with `rebuild_chunk0_binary`, which relocates all worker headers, function tables, jump tables, constant tables, and `shared_data`/`shared_header` pointers with 16-byte/64-byte alignment and automatically un-shares shared `RET` stub functions without corrupting adjacent workers or growing the file on repeated compilations.
* **Fixed Atel Decompiler Stack & Jump Target Bugs**:
  * Cleared evaluation stack at function entry points to prevent cross-function stack leakage.
  * Fixed `0xB5` (`CALL`) vs `0xD8` (`CALLPOPA`) return value handling and mapped all `0x70XX` battle engine calls with exact argument counts.
  * Fixed `0x2A` (`POPX`) condition tracking and `0xD6`/`0xD7` (`POPXCJMP`/`POPXNCJMP`) conditional jump popping, plus `POPI0..3`/`PUSHI0..3` scratch register preservation for target filter pipelines (`0x7010`).
* **Fixed Stat Diff, Randomizer & Modpack Offsets/Paths**:
  * Fixed `open_stat_diff_dialog` and `open_randomizer_dialog` to read/write monster stats at authentic `0x14` (HP), `0x18` (MP), `0x1C` (Overkill), `0x20..0x27` (Core Stats), `0x2B..0x2E` (Elemental Affinities), and `0x2F..0x47` (Status Resistances).
  * Fixed `open_randomizer_dialog` and `import_modpack` to traverse `_mXXX/mXXX.bin` subdirectories properly.

---

## [v1.1.0] — 2026-08-27

### 🌟 Major Highlights & New Features

#### 👾 1. Universal Monster AI Rule Extractor & Interactive Builder
* **Automatic Rule Extraction**: Opening any monster (vanilla or modded) now automatically decompiles and extracts all of its active battle actions, spells, targets, probability percentages, and trigger conditions into the Visual Rule Builder.
* **Expanded Condition Triggers**: Full support for 20 condition types (e.g. *HP < 25% Desperation*, *MP < 25%*, *Turn 1/2/3*, *Every 2/3 Turns*, *Target Status Checks: Reflect/Protect/Shell/Haste/Poison/Silence/Blind*, *Solo Fiend*, *Party Alive <= 1/2*).
* **Interactive Editing**: Add new abilities, modify existing triggers, reorder action execution priorities, delete moves, and inject back into bytecode with 1 click.
* **Built-in Ability Name Resolver**: Automatically resolves and displays friendly ability names (e.g., `Attack (Physical) (0x10)`, `Water (0x17)`, `Cure (0x27)`, `Haste (0x2e)`).

#### 🗺️ 2. Encounter & Formation Map Explorer
* **Dedicated "Encounters & Spawns" Tab**:
  * **Active Monster View**: Displays all Spira maps, sub-areas, and formation party compositions where the active monster spawns.
  * **1-Click Monster Switching**: Click any companion enemy tag inside a formation card to instantly load and edit it.
  * **Spira World Map Explorer**: Comprehensive bestiary database covering 14 Spira regions (*Besaid*, *Kilika*, *Mi'ihen*, *Mushroom Rock / Djose*, *Moonflow*, *Thunder Plains*, *Macalania*, *Sanubia*, *Bevelle*, *Calm Lands*, *Mt. Gagazet*, *Sin / Omega*, *Monster Arena*, *Dark Aeons & Superbosses*).
  * Includes spawn rates %, ambush %, and full encounter groups for Dark Aeons, Penance (Body/Arms), Ultima & Omega Weapon, and Nemesis.

#### 🎲 3. Monster Randomizer Suite
* **Configurable Game Randomizer**:
  * Randomize Base Attributes (HP, MP, Str, Def, Mag, MDef, Agi, Luck, Eva, Acc) within configurable multiplier ranges.
  * Randomize Elemental Affinities (Weak, Resist, Immune, Absorb).
  * Randomize Status Weaknesses & Immunities.
  * Randomize Item Drops & Steal loot tables.
  * Shuffle Battle AI Action assignments with seed input support.

#### ⚖️ 4. Difficulty Presets & Custom Balance Profiles
* **One-Click Difficulty Presets in Batch Scaler**:
  * *Standard Hard Mode (1.5x)*
  * *Nightmare Mode (2.5x)*
  * *Casual Speedrun (0.6x)*
  * *Boss Rush Challenge (2.0x)*
  * *Gold & AP Farm (3.0x)*
* **JSON Profile Manager**: Save and load custom rebalance configurations (`.json`).

#### ⚔️ 5. Equipment Drop & Auto-Ability Slot Editor
* Added controls in the **Loot Tables** tab for Weapon Drop Bias (`0x2D`), Max Equipment Slots (`0x2E`), Slot Variance (`0x2F`), and Auto-Ability Bonus Weight (`0x30`).

#### 📊 6. Side-by-Side Stat Diff Inspector
* Live variance comparison tool (<kbd>Ctrl</kbd> + <kbd>D</kbd>) comparing active stats against original `.bak` backups with color-coded buff/nerf indicators.

#### 📦 7. Portable Modpack System (`.ffxmod`)
* Export and import lightweight JSON patch files to easily share and install monster balance mods.

#### 📄 8. Dark-Themed Bestiary Card Exporter
* Export monster stats, resistances, loot, and elemental affinities as styled standalone HTML reports or Markdown wiki cards.

#### 🎨 9. Atel Syntax Highlighting & Global Keyboard Shortcuts
* Color-coded Atel disassembly (keywords, functions, registers, labels, numbers).
* Shortcuts: <kbd>Ctrl</kbd>+<kbd>S</kbd> (Save), <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> (Save All), <kbd>Ctrl</kbd>+<kbd>F</kbd> (Search), <kbd>F5</kbd> (Rescan), <kbd>Ctrl</kbd>+<kbd>D</kbd> (Diff).

---

### 🔧 Bug Fixes & Improvements
* Fixed Atel decompiler fallback when parsing single-worker monster bytecode.
* Fixed monster explorer filter to support simultaneous text search and regional zone filtering.
* Cleaned up atomic file writing with automated `.bak` backups on all operations.

---

## [v1.0.0] — Initial Release
* Initial release of FFX Monster AI & Stats Editor.
* Monster stat editing, SJIS text decoding, Atel script disassembling, chunk packing/unpacking, and player stat editing.
