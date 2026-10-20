# Final Fantasy X Monster AI & Stats Editor (FFX-AI-Tool) — User Guide & Walkthrough Manual

Welcome to the **FFX Monster AI & Stats Editor** (v1.2.0)! This application is a complete modding suite designed to customize monster stats, edit and compile battle AI scripts across all event hooks, inspect battle formations, create balance overhauls, and repack game files for **Final Fantasy X** (PC HD Remaster & PS2).

📥 **Direct Download (Latest Standalone Release v1.2.0)**: [FFX_AI_Tool.zip](https://github.com/NfgOdin/FFX_AI_Tool/releases/download/v1.2.0/FFX_AI_Tool.zip)

---

## 🌟 Core Features
- **Overhauled Visual AI Rule Builder (Multi-Hook & Boss State Machine Architecture)**: Edit all 9 `Chunk 1` Combat AI event hooks (`Active Turn`, `Counter / React`, `On Damage`, `On Death`, `Pre-Turn`, `Battle Start`, `On Targeted`, `Post-Turn`, `Status Tick`), enable unmapped hooks with 1 click, configure `var_00..var_1F` phase gates and state mutations (`Set`/`Add`/`Reset`), chain composite conditions (`AND`/`OR`), select from 31 target presets, and compile losslessly in-place into Atel `Chunk 0` bytecode.
- **Atel Battle AI Disassembler, Decompiler & Live Pseudocode Preview**: Inspect Raw Assembly, C-Style Pseudocode, and Plain English translations with real-time syntax highlighting and constant editing.
- **Visual AI Flowchart Graph**: Interactive node-and-edge flowchart visualizing phase gates, composite conditions, target selection, variable mutations, and `Return` / `Continue` control flow.
- **Complete Monster Stats, Elementals, Status Resistances & Loot Editor**: Edit HP, MP, Overkill, Core Stats, Elemental Affinities, Status Resistances, Item Drops, Steal/Bribe tables, Ronso Rage, and Equipment Drop slot/ability biases.
- **Spira Encounter & Formation Map Explorer**: Browse enemy party formations across 14 Spira regions (including Dark Aeons & Superbosses) with 1-click monster switching.
- **Monster Randomizer, Difficulty Presets, Stat Diff Inspector, Modpacks (`.ffxmod`) & Bestiary Exporter**: Built-in tools for full-game randomization, batch difficulty scaling, side-by-side `.bak` stat comparison, portable JSON modpacks, and HTML/Markdown bestiary cards.

---

## 📖 Table of Contents
1. [Getting Started & Folder Setup](#1-getting-started--folder-setup)
2. [Monster Explorer & Regional Zone Filters](#2-monster-explorer--regional-zone-filters)
3. [Battle AI Script Editor (Atel Engine)](#3-battle-ai-script-editor-atel-engine)
4. [Visual AI Rule Builder](#4-visual-ai-rule-builder)
5. [Visual AI Flowchart Graph](#5-visual-ai-flowchart-graph)
6. [Monster Core Stats, Elements & Resistances](#6-monster-core-stats-elements--resistances)
7. [Loot Tables & Equipment Drop Editor](#7-loot-tables--equipment-drop-editor)
8. [Player Battle Stats Editor](#8-player-battle-stats-editor)
9. [Encounter & Formation Map Explorer](#9-encounter--formation-map-explorer)
10. [Monster Randomizer Suite](#10-monster-randomizer-suite)
11. [Difficulty Presets & Batch Scaler](#11-difficulty-presets--batch-scaler)
12. [Side-by-Side Stat Diff Inspector](#12-side-by-side-stat-diff-inspector)
13. [Modpack Manager (.ffxmod)](#13-modpack-manager-ffxmod)
14. [Bestiary Card Exporter (HTML & Markdown)](#14-bestiary-card-exporter-html--markdown)
15. [Keyboard Shortcuts & Hotkeys](#15-keyboard-shortcuts--hotkeys)

---

## 1. Getting Started & Folder Setup

### Setting Your Master Directory
When you launch the editor, point the **Master Directory** bar at the top to your extracted FFX game data:
- Click **"📂 Browse..."** and select your extracted `ffx/master` directory or the `jppc/battle/mon` folder.
- If you have extracted FFX files using *VBF Browser*, select the top-level `master` folder. The tool will automatically locate monster files (`m001.bin` through `m346.bin`), the command dictionary (`command.bin`), and item tables (`item.bin`).
- Click **"🔄 Scan Monsters"** (or press <kbd>F5</kbd>) to populate the monster list on the left.

### Automatic Backups & Safety
- Whenever you modify and save a monster file, the tool automatically creates a backup copy (`.bak`) in the same folder.
- To restore any monster back to its original state, right-click its name in the left monster list and choose **"Restore from Backup (.bak)"**.

---

## 2. Monster Explorer & Regional Zone Filters

The left panel gives you full access to all monsters found in your game directory:

- **🔍 Search / Filter Bar**: Type any part of a monster's name or ID (e.g. `Dingo`, `m001`, `Malboro`, `Penance`).
- **🗺️ Zone Filter Dropdown**: Filter monsters by their native region in Spira:
  - *Besaid Island*, *Kilika Woods*, *Luca / Mi'ihen*, *Mushroom Rock / Djose*, *Moonflow*, *Thunder Plains*, *Macalania*, *Sanubia Desert (Bikanel)*, *Bevelle / Via Purifico*, *Calm Lands / Sunken Cave*, *Mt. Gagazet / Zanarkand*, *Inside Sin / Omega Ruins*, *Monster Arena*, *Story Bosses*, and *Dark Aeons & Superbosses*.
- **Right-Click Context Menu**:
  - **Restore from Backup (.bak)**: Reverts the monster to its original unedited state.
  - **📊 Compare with Backup (Stat Diff)...**: Opens a live side-by-side stat diff window comparing your edits against the backup.
  - **📄 Export Bestiary Card...**: Generates a dark HTML report or Markdown wiki card for this monster.
  - **Batch Scale Selected Stats...**: Multiplies HP, Str, Mag, etc. for all selected monsters at once.
  - **Make Selected Status Immune...**: Sets 100% resistance across selected monsters.
  - **Set Selected Element Affinities...**: Batch assigns Weak/Resist/Immune/Absorb properties.

---

## 3. Battle AI Script Editor (Atel Engine)

Located in the **"👾 AI Atel Script"** tab, this editor lets you inspect, understand, and fine-tune monster battle behaviors:

### 3 View Modes
1. **Raw Assembly**: Displays native Atel virtual machine opcodes (`PUSHI`, `CALL`, `POPXNCJMP`, `RET`, registers `rA`, `rX`, `rY`).
2. **Decompiled Pseudocode**: Formats the script into readable C-style functions and conditionals (`if (GetProperty(-14, 21) < 50) { BuildAction(-14, 0x0027, -14, 0); }`).
3. **Plain English**: Translates battle routines into clear, descriptive sentences (*"If HP is below 50%, cast Cure on Self with 100% chance"*).

### Real-Time Syntax Highlighting
- **Purple**: Flow control keywords (`if`, `goto`, `return`, `halt`, `def`).
- **Blue**: Engine syscalls and functions (`BuildAction`, `ExecuteAction`, `GetProperty`, `checkTargetStatus`).
- **Cyan**: Labels and subroutines (`label_0`, `w1_Label_4`).
- **Orange**: Virtual registers & variables (`rA`, `rX`, `rY`, `var_01`, `refInts`).
- **Emerald**: Numeric constants and hexadecimal values (`0x7010`, `100`, `16384`).
- **Grey Italic**: Comments and annotations.

### Script Constant Value Editor
The right pane of the AI script tab lists all integer and float constants used by the script. Select any constant (such as an HP percentage threshold or turn timer), enter a new value, and click **"Apply Value"** to update the script without touching raw bytecode!

---

## 4. Visual AI Rule Builder

Located inside the AI Script tab under the **"Visual AI Rule Builder"** section:

### Multi-Hook Event Architecture (`Chunk 1` Combat AI Resolver)
When you load any monster or boss, the tool parses its `Chunk 1` worker descriptor table (`role == 2`) to automatically identify its true Combat AI Worker and all 9 battle event hooks:
- `⚡ Active Turn (Slot 0)` — Regular CTB turn behavior
- `🛡 Counter / React (Slot 3)` — Counter-attacks and reaction scripts after being acted upon
- `💥 On Damage (Slot 2)` — Immediate reactions when damage is taken
- `💀 On Death (Slot 4)` — Final attacks or death phase transitions
- `⏳ Pre-Turn (Slot 1)`, `🎬 Battle Start (Slot 5)`, `🎯 On Targeted (Slot 6)`, `📐 Post-Turn (Slot 7)`, `⏱ Status Tick (Slot 8)`
- If a hook slot is currently unmapped (`0xFFFF`), click **"✨ Enable Unmapped Hook"** (or simply compile rules into it) to automatically allocate a dedicated function and bind it in `Chunk 1`!

### Creating & Customizing Rules
1. **➕ Add Rule / 📋 Duplicate / ✨ Templates**: Add rules from scratch, duplicate an existing rule, or load one of **7 Preset AI Templates** (*Standard Fiend*, *3-Turn Elemental Rotation*, *2-Phase Boss State Machine*, *Physical Counter (Behemoth)*, *Bomb Swell Counter*, *Healer / Support Fiend*, *Smart Debuffer & Dispel*).
2. **Configure Phase / State Gate**:
   - Filter rules by `Any Phase` or any local AI worker variable (`var_00` through `var_1F`) using `==, !=, <, <=, >, >=` (e.g., `var_00 == 1` for Boss Phase 2 or rotation steps).
3. **Build Primary & Secondary Conditions (`AND` / `OR`)**:
   - *HP / MP Thresholds*: `Always`, `Self HP < 75%`, `Self HP < 50%`, `Self HP < 33%`, `Self HP < 25% (Desperation)`, `Self HP < 15%`, `Self MP < 25%`, `Self MP >= 20`.
   - *Counter & Damage Triggers*: `Damage Taken > 0`, `Last Hit Was Physical`, `Last Hit Was Magical`, `Last Hit Was Normal Attack`.
   - *Party & Self Status Checks*: `Party Has/No Reflect`, `Protect`, `Shell`, `Haste`, `Poison`, `Silence`, `Darkness`, `Sleep`, `Petrify`, `Self Has/No Haste/Protect/Shell/Reflect/Regen`.
   - *Encounter & Turn Checks*: `Turn == 1/2/3`, `Every 2/3 Turns`, `Solo Fiend (Alive Monsters == 1)`, `Alive Party == 1`, `Alive Party <= 2`.
4. **Select an Action / Spell (with Real-Time Search Filter)**:
   - Type into the **🔍 Filter Actions** box to quickly find any monster skill, magic spell, or boss overdrive, and choose between `Standard Action (0x700B)` or `Counter Action (0x705A)`.
5. **Choose from 31 Target Presets**:
   - `Random Alive Party`, `All Active Party`, `Self`, `All Allied Monsters`, `Random Allied Monster`, `Last Attacker / Triggering Actor`, `Provoker`, `Lowest/Highest HP/MP Party`, `Party With/Without Status`, specific party members (`Tidus` through `Rikku`), or specific monster formation slots (`Monster Slot 0..3`).
6. **Configure Variable / State Mutation & Turn Flow**:
   - Mutate any `var_XX` after the action (`Set =`, `Add +`, `Reset = 0`) to advance turn rotations or switch boss phases.
   - Choose **`Return (End Turn)`** to finish the hook after executing, or **`Continue (Multi-Action)`** to chain multiple actions/buffs in a single turn!
7. **🔍 Live Hook Preview & ⚡ Compile**:
   - Click **"🔍 Preview Hook Code"** to inspect the exact Atel assembly and decompiled C-style pseudocode, then click **"⚡ Compile Rules into Active Hook"** to losslessly rebuild `Chunk 0` in-place!

---

## 5. Visual AI Flowchart Graph

Click the **"📈 Visual AI Flowchart"** tab to view an interactive visual graph of the active hook's AI logic:
- Displays the active `Chunk 1` Event Hook, Worker index, and Function index.
- Renders Phase/State gates, composite `AND`/`OR` conditions, probability percentages, target selectors, variable mutations, and `RETURN (End Turn)` vs. `CONTINUE (Combo)` flow paths.

---

## 6. Monster Core Stats, Elements & Resistances

Located in the **"📊 Monster Stats"** tab:

### Core Attributes
- **HP & MP**: Maximum health and mana pools.
- **Overkill HP**: Damage threshold required to trigger an Overkill.
- **Base Stats (0–255)**: Strength, Defense, Magic, Magic Defense, Agility, Luck, Evasion, Accuracy.
- **Localization**: Japanese Name, English Name, Sensor descriptions, and Scan text lore.

### Elemental Affinities
Set affinities for **Fire**, **Ice**, **Thunder**, **Water**, and **Holy**:
- `Normal`: Standard 1.0x damage.
- `Weak`: 1.5x damage taken.
- `Resist`: 0.5x damage taken.
- `Immune`: 0 damage taken.
- `Absorb`: Absorbs damage as HP healing.

### Status Resistances
Configure resistance values (0% = Vulnerable, 100% = Immune, 255% = Permanent Immunity) for 16 status effects:
*Death, Zombie, Petrify, Poison, Power Break, Magic Break, Armor Break, Mental Break, Confusion, Berserk, Provoke, Threaten, Sleep, Silence, Darkness, Slow.*

---

## 7. Loot Tables & Equipment Drop Editor

Located in the **"🎁 Loot Tables"** tab:

### Battle Rewards
- **Gil Reward**: Currency awarded upon defeat.
- **AP (Normal)** & **AP (Overkill)**: Ability Points earned.
- **Item Drops**: Normal Drop (Common & Rare) and Overkill Drop (Common & Rare) with quantities.
- **Steal Table**: Common Steal and Rare Steal items with quantities.
- **Bribe Table**: Item received and quantity when using the Bribe command.
- **Ronso Rage**: Blue Magic ability Kimahri learns when using Lancet on this monster.

### Equipment Drop & Auto-Ability Attributes
- **Weapon Drop Bias (0–255)**: Balances whether dropped gear favors weapons or armor.
- **Max Equipment Slots (1–4)**: Maximum number of ability slots on dropped gear.
- **Slot Count Variance (0–4)**: Random slot roll variance.
- **Auto-Ability Bonus Weight (0–255)**: Higher weights roll stronger passive abilities on dropped equipment.

---

## 8. Player Battle Stats Editor

Located in the **"👤 Player Stats"** tab:
- Reads and modifies starting character statistics for all 7 party members (*Tidus, Yuna, Auron, Wakka, Lulu, Kimahri, Rikku*) from `battle/kernel/ply_save.bin`.
- Modify base HP, MP, Strength, Defense, Magic, Magic Defense, Agility, Luck, Evasion, and Accuracy.
- Click **"💾 Save Player Stats to ply_save.bin"** to write changes to your game.

---

## 9. Encounter & Formation Map Explorer

Located in the **"🗺️ Encounters & Spawns"** tab:

### Active Monster Formations (Left Panel)
- Displays every region, sub-area, and battle group where the currently loaded monster spawns.
- Shows spawn frequency % and ambush chances.
- **1-Click Monster Switching**: Click any companion monster badge in a formation card (e.g. `[m004] Condor`) to load and edit that enemy instantly!

### Spira World Map Explorer (Right Panel)
- Select any of Spira's 14 regions from the dropdown or use the search bar to inspect all enemy formations.
- Includes complete mappings for all Dark Aeons, Penance (Body/Arms), Ultima & Omega Weapon, and Nemesis.
- Click **"🔍 Load First Monster in Formation"** to jump directly to any enemy group.

---

## 10. Monster Randomizer Suite

Click the **"🎲 Randomizer..."** button in the top toolbar to launch the game randomizer:

1. **Select What to Randomize**:
   - [x] Base Stats (HP, MP, Str, Def, Mag, Agi) within custom min/max multiplier bounds (e.g., `0.7x` to `1.6x`).
   - [x] Elemental Affinities (Weak, Resist, Immune, Absorb).
   - [x] Status Weaknesses & Immunities.
   - [x] Item Drops & Steal tables.
   - [x] Shuffle Battle AI actions and behaviors.
2. **Seed (Optional)**: Enter any numeric or text seed for reproducible randomizer seeds to share with friends.
3. Click **"🎲 Run Randomizer"** to patch all monsters across your game directory!

---

## 11. Difficulty Presets & Batch Scaler

Click the **"⚖️ Batch Scale..."** button in the top toolbar (or right-click multiple monsters):

### 1-Click Difficulty Presets
- **Standard Hard Mode (1.5x)**: 1.5x HP, 1.25x Str/Mag, 1.2x Def/MDF, 1.15x Agility, +25% Status Res.
- **Nightmare Mode (2.5x)**: 2.5x HP, 1.5x Str/Mag, 1.4x Def/MDF, 1.3x Agility, +50% Status Res, 40% Floor.
- **Casual Speedrun (0.6x)**: 0.6x HP, 0.75x Stats, 2.0x AP/Gil/Items.
- **Boss Rush Challenge (2.0x)**: 2.0x HP, 1.4x Str/Mag, 1.3x Def/MDF, 1.25x Agi.
- **Gold & AP Farm (3.0x)**: 3.0x Gil, 3.0x AP, 2.0x Items.

### Custom JSON Profiles
- Click **"💾 Save Preset (.json)"** to export your custom multipliers.
- Click **"📂 Load Preset (.json)"** to load community balancing configs.

---

## 12. Side-by-Side Stat Diff Inspector

Press <kbd>Ctrl</kbd> + <kbd>D</kbd> (or click **"📊 Stat Diff..."** in the toolbar):
- Compares your current monster's modified stats against its original `.bak` backup file.
- Displays exact variance numbers and percentage differences:
  - 🟢 **Green (Buffs)**: Stats increased above vanilla values.
  - 🔴 **Red (Nerfs)**: Stats decreased below vanilla values.
  - ⚪ **White**: Unchanged stats.

---

## 13. Modpack Manager (.ffxmod)

Click the **"📦 Modpack..."** button in the top toolbar:
- **📤 Export Modpack (.ffxmod)**: Generates a lightweight, portable JSON patch file containing all of your monster balance changes, stat tweaks, loot adjustments, and AI bytecode.
- **📥 Import & Apply Modpack**: Installs an `.ffxmod` patch into your game directory with automatic `.bak` backups created for all modified files.

---

## 14. Bestiary Card Exporter (HTML & Markdown)

Click the **"📄 Bestiary..."** button in the top toolbar:
- **Dark HTML Report (`.html`)**: Creates a modern, self-contained HTML bestiary infobox report with gradients, styled stat grids, resistance tables, and loot charts.
- **Markdown Wiki Page (`.md`)**: Creates a clean GitHub-flavored markdown file ready to paste into wikis or mod documentation.

---

## 15. Keyboard Shortcuts & Hotkeys

| Shortcut | Action |
|---|---|
| <kbd>Ctrl</kbd> + <kbd>S</kbd> | Save current monster changes to disk |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>S</kbd> | Save all modified monsters in cache to disk |
| <kbd>Ctrl</kbd> + <kbd>F</kbd> | Jump to and focus the Monster Search filter box |
| <kbd>F5</kbd> | Rescan monster directory |
| <kbd>Ctrl</kbd> + <kbd>D</kbd> | Open Side-by-Side Stat Diff Inspector |

---

## License & Credits

Developed with ❤️ for the Final Fantasy X modding community.  
Licensed under the **MIT License**.
