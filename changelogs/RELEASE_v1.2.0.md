# Release Notes — FFX Monster AI & Stats Editor v1.2.0

### 🌟 New Features & Highlights
* **Overhauled Visual AI Rule Builder (Multi-Hook & Boss State Machine Architecture)**:
  * **Dynamic Chunk 1 Event Hook Resolution**: Automatically parses `Chunk 1` (`role == 2` Combat AI Worker and its 21 `uint16` event hook table) to resolve and edit all 9 battle event hooks (`⚡ Active Turn`, `🛡 Counter / React`, `💥 On Damage`, `💀 On Death`, `⏳ Pre-Turn`, `🎬 Battle Start`, `🎯 On Targeted`, `📐 Post-Turn`, `⏱ Status Tick`) across all 361 monsters and bosses.
  * **Unmapped Hook Enabling**: Added one-click & automatic `Chunk 1` hook slot enabling (`enable_chunk1_hook_slot`) so Counter-Attack, On-Damage, and On-Death scripts can be added to any enemy even if originally unmapped (`0xFFFF`).
  * **Phase & State Variable Gates**: Added support for local worker variable gates (`var_00..var_1F` with `==, !=, <, <=, >, >=` operators) and post-action variable mutations (`Set`, `Add`, `Reset`) to build multi-phase bosses, attack rotation loops, and damage-hit counters.
  * **Composite Conditions (`AND` / `OR`) & Authentic Battle Engine Checks**: Added composite condition chaining, dynamic HP/MP ratio math (`GetProperty(-13, 0) * 100 < GetProperty(-13, 2) * pct`), Party Status mask checks (`0x701E`), Self Status checks (`0x700F`), Counter triggers (`Damage Taken > 0`, `Last Hit Was Physical / Magical`, `Last Hit Was Normal Attack`), and Alive Party/Monster counts.
  * **Complete Target Selection System**: Added 31 targeting presets including `Random Alive Party`, `All Active Party`, `Self`, `All Allied Monsters`, `Random Allied Monster`, `Last Attacker`, `Provoker`, `Lowest/Highest HP/MP Party`, `Party With/Without Status`, specific characters (`Tidus` through `Rikku`), and specific monster formation slots (`Monster Slot 0..3`).
  * **Multi-Action Turn Flow & Counter Opcode Support**: Added support for `Return (End Turn)` vs. `Continue (Multi-Action / Combo)` per rule and `ExecuteAction (0x700B)` vs. `ExecuteCounterAction (0x705A)`.
  * **Searchable Action Filter, Live Pseudocode Preview & Upgraded Flowchart**: Added real-time ability filtering, live hook pseudocode preview, rule duplication, 7 comprehensive AI templates, and an upgraded Visual AI Flowchart rendering phase gates, composite conditions, variable mutations, and `Return`/`Continue` paths.

### 🔧 Bug Fixes & Improvements
* **Safe In-Place Atel Chunk 0 Binary Rebuilder**: Replaced the legacy append-only `inject_rules` with `rebuild_chunk0_binary`, which relocates all worker headers, function tables, jump tables, constant tables, and `shared_data`/`shared_header` pointers with 16-byte/64-byte alignment and automatically un-shares shared `RET` stub functions without corrupting adjacent workers or growing the file on repeated compilations.
* **Fixed Atel Decompiler Stack & Jump Target Bugs**:
  * Cleared evaluation stack at function entry points to prevent cross-function stack leakage.
  * Fixed `0xB5` (`CALL`) vs `0xD8` (`CALLPOPA`) return value handling and mapped all `0x70XX` battle engine calls with exact argument counts.
  * Fixed `0x2A` (`POPX`) condition tracking and `0xD6`/`0xD7` (`POPXCJMP`/`POPXNCJMP`) conditional jump popping, plus `POPI0..3`/`PUSHI0..3` scratch register preservation for target filter pipelines (`0x7010`).
* **Fixed Stat Diff, Randomizer & Modpack Offsets/Paths**:
  * Fixed `open_stat_diff_dialog` and `open_randomizer_dialog` to read/write monster stats at authentic `0x14` (HP), `0x18` (MP), `0x1C` (Overkill), `0x20..0x27` (Core Stats), `0x2B..0x2E` (Elemental Affinities), and `0x2F..0x47` (Status Resistances).
  * Fixed `open_randomizer_dialog` and `import_modpack` to traverse `_mXXX/mXXX.bin` subdirectories properly.
