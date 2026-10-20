import os
import sys
import struct
import json
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import OrderedDict

from ffx_codec import FFXCodec
from ffx_atel import (
    AtelDisassembler, AtelDecompiler, compile_rules_to_atel, compile_rules_to_bytecode,
    decompile_atel_to_rules, inject_rules, show_dark_confirm,
    parse_chunk1_ai_map, enable_chunk1_hook_slot,
    AI_EVENT_HOOK_DEFS, CONDITION_PRESETS, TARGET_PRESETS, AI_RULE_TEMPLATES
)
import ffx_monster_packer as packer
from ffx_encounters import FFXEncounterParser

script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(script_dir, "ffx_ai_tool_recent_files.json")
ELEMENT_STATES = ["Normal", "Weak", "Resist", "Immune", "Absorb"]
from ffx_ability_db import FFX_MASTER_ABILITIES

ZONE_CATEGORIES = [
    "All Zones",
    "Besaid Island",
    "Kilika Woods & Temple",
    "Luca & Mi'ihen Highroad",
    "Mushroom Rock & Djose",
    "Moonflow & Guadosalam",
    "Thunder Plains",
    "Macalania Woods & Lake",
    "Sanubia Desert (Bikanel)",
    "Bevelle & Via Purifico",
    "Calm Lands & Sunken Cave",
    "Mt. Gagazet & Zanarkand",
    "Inside Sin & Omega Ruins",
    "Monster Arena",
    "Story Bosses",
    "Dark Aeons & Superbosses",
]

MONSTER_ZONE_MAP = {
    # Besaid
    "m001": "Besaid Island", "m002": "Besaid Island", "m003": "Besaid Island", "m004": "Besaid Island",
    "m005": "Besaid Island", "m006": "Besaid Island",
    # Kilika
    "m007": "Kilika Woods & Temple", "m008": "Kilika Woods & Temple", "m009": "Kilika Woods & Temple",
    "m010": "Kilika Woods & Temple", "m011": "Kilika Woods & Temple",
    # Mi'ihen & Luca
    "m012": "Luca & Mi'ihen Highroad", "m013": "Luca & Mi'ihen Highroad", "m014": "Luca & Mi'ihen Highroad",
    "m015": "Luca & Mi'ihen Highroad", "m016": "Luca & Mi'ihen Highroad", "m017": "Luca & Mi'ihen Highroad",
    "m018": "Luca & Mi'ihen Highroad", "m019": "Luca & Mi'ihen Highroad",
    # Mushroom Rock & Djose
    "m020": "Mushroom Rock & Djose", "m021": "Mushroom Rock & Djose", "m022": "Mushroom Rock & Djose",
    "m023": "Mushroom Rock & Djose", "m024": "Mushroom Rock & Djose", "m025": "Mushroom Rock & Djose",
    "m026": "Mushroom Rock & Djose", "m027": "Mushroom Rock & Djose",
    # Moonflow & Guadosalam
    "m028": "Moonflow & Guadosalam", "m029": "Moonflow & Guadosalam", "m030": "Moonflow & Guadosalam",
    "m031": "Moonflow & Guadosalam", "m032": "Moonflow & Guadosalam",
    # Thunder Plains
    "m033": "Thunder Plains", "m034": "Thunder Plains", "m035": "Thunder Plains", "m036": "Thunder Plains",
    "m037": "Thunder Plains", "m038": "Thunder Plains", "m039": "Thunder Plains",
    # Macalania
    "m040": "Macalania Woods & Lake", "m041": "Macalania Woods & Lake", "m042": "Macalania Woods & Lake",
    "m043": "Macalania Woods & Lake", "m044": "Macalania Woods & Lake", "m045": "Macalania Woods & Lake",
    "m046": "Macalania Woods & Lake", "m047": "Macalania Woods & Lake", "m048": "Macalania Woods & Lake",
    # Bikanel
    "m049": "Sanubia Desert (Bikanel)", "m050": "Sanubia Desert (Bikanel)", "m051": "Sanubia Desert (Bikanel)",
    "m052": "Sanubia Desert (Bikanel)", "m053": "Sanubia Desert (Bikanel)", "m054": "Sanubia Desert (Bikanel)",
    # Bevelle / Via Purifico
    "m055": "Bevelle & Via Purifico", "m056": "Bevelle & Via Purifico", "m057": "Bevelle & Via Purifico",
    "m058": "Bevelle & Via Purifico", "m059": "Bevelle & Via Purifico", "m060": "Bevelle & Via Purifico",
    # Calm Lands & Sunken Cave
    "m061": "Calm Lands & Sunken Cave", "m062": "Calm Lands & Sunken Cave", "m063": "Calm Lands & Sunken Cave",
    "m064": "Calm Lands & Sunken Cave", "m065": "Calm Lands & Sunken Cave", "m066": "Calm Lands & Sunken Cave",
    "m067": "Calm Lands & Sunken Cave", "m068": "Calm Lands & Sunken Cave", "m069": "Calm Lands & Sunken Cave",
    # Gagazet & Zanarkand
    "m070": "Mt. Gagazet & Zanarkand", "m071": "Mt. Gagazet & Zanarkand", "m072": "Mt. Gagazet & Zanarkand",
    "m073": "Mt. Gagazet & Zanarkand", "m074": "Mt. Gagazet & Zanarkand", "m075": "Mt. Gagazet & Zanarkand",
    "m076": "Mt. Gagazet & Zanarkand", "m077": "Mt. Gagazet & Zanarkand", "m078": "Mt. Gagazet & Zanarkand",
    # Sin & Omega
    "m079": "Inside Sin & Omega Ruins", "m080": "Inside Sin & Omega Ruins", "m081": "Inside Sin & Omega Ruins",
    "m082": "Inside Sin & Omega Ruins", "m083": "Inside Sin & Omega Ruins", "m084": "Inside Sin & Omega Ruins",
    "m085": "Inside Sin & Omega Ruins", "m086": "Inside Sin & Omega Ruins", "m087": "Inside Sin & Omega Ruins",
    "m099": "Inside Sin & Omega Ruins", "m100": "Inside Sin & Omega Ruins",
    # Monster Arena Creations & Originals
    "m276": "Monster Arena", "m277": "Monster Arena", "m279": "Monster Arena",
    "m280": "Monster Arena", "m281": "Monster Arena", "m282": "Monster Arena", "m283": "Monster Arena",
    "m292": "Monster Arena", "m293": "Monster Arena", "m294": "Monster Arena", "m295": "Monster Arena",
    "m296": "Monster Arena", "m297": "Monster Arena", "m298": "Monster Arena", "m299": "Monster Arena",
    "m300": "Monster Arena", "m301": "Monster Arena", "m302": "Monster Arena", "m303": "Monster Arena",
    "m304": "Monster Arena", "m305": "Monster Arena", "m306": "Monster Arena", "m307": "Monster Arena",
    "m308": "Monster Arena", "m309": "Monster Arena", "m310": "Monster Arena", "m311": "Monster Arena",
    "m312": "Monster Arena", "m313": "Monster Arena", "m314": "Monster Arena", "m315": "Monster Arena",
    "m316": "Monster Arena", "m317": "Monster Arena", "m318": "Monster Arena",
    # Belgemine Aeons & Magus Sisters (Remiem Temple)
    "m284": "Story Bosses", "m285": "Story Bosses", "m286": "Story Bosses",
    "m287": "Story Bosses", "m288": "Story Bosses", "m289": "Story Bosses",
    "m290": "Story Bosses", "m291": "Story Bosses",
    # Dark Aeons & Penance Superbosses
    "m334": "Dark Aeons & Superbosses", "m335": "Dark Aeons & Superbosses",
    "m336": "Dark Aeons & Superbosses", "m337": "Dark Aeons & Superbosses",
    "m338": "Dark Aeons & Superbosses", "m339": "Dark Aeons & Superbosses",
    "m340": "Dark Aeons & Superbosses", "m341": "Dark Aeons & Superbosses",
    "m342": "Dark Aeons & Superbosses", "m343": "Dark Aeons & Superbosses",
    "m344": "Dark Aeons & Superbosses", "m345": "Dark Aeons & Superbosses",
    "m346": "Dark Aeons & Superbosses",
    # Story Bosses
    "m153": "Story Bosses", "m102": "Story Bosses", "m103": "Story Bosses", "m110": "Story Bosses",
    "m156": "Story Bosses", "m104": "Story Bosses", "m117": "Story Bosses", "m160": "Story Bosses",
    "m161": "Story Bosses", "m111": "Story Bosses", "m121": "Story Bosses", "m122": "Story Bosses",
    "m123": "Story Bosses", "m124": "Story Bosses", "m125": "Story Bosses", "m141": "Story Bosses",
    "m222": "Story Bosses", "m212": "Story Bosses", "m119": "Story Bosses", "m120": "Story Bosses",
    "m126": "Story Bosses", "m127": "Story Bosses", "m229": "Story Bosses", "m134": "Story Bosses",
    "m135": "Story Bosses", "m142": "Story Bosses", "m143": "Story Bosses", "m128": "Story Bosses",
    "m129": "Story Bosses", "m130": "Story Bosses", "m136": "Story Bosses", "m137": "Story Bosses",
    "m139": "Story Bosses", "m138": "Story Bosses", "m140": "Story Bosses", "m113": "Story Bosses",
    "m131": "Story Bosses", "m132": "Story Bosses", "m173": "Story Bosses", "m174": "Story Bosses",
    "m176": "Story Bosses"
}

APP_VERSION = "1.2.0"
VERSION = "1.2.0"

class FFXAIToolGUI:
    def __init__(self, parent, is_embedded=False):
        self.parent = parent
        self.is_embedded = is_embedded
        self.root = parent.winfo_toplevel() if is_embedded else parent
        
        # Theme colors
        self.bg_color = "#121212"
        self.card_color = "#1e1e1e"
        self.accent_color = "#3b82f6"
        self.accent_hover = "#2563eb"
        self.text_color = "#e5e7eb"
        self.text_dim = "#9ca3af"
        self.border_color = "#374151"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.btn_color_secondary = "#4b5563"
        self.active_color = "#2563eb"
        
        if not is_embedded:
            self.root.title(f"FFX Monster AI & Stats Editor — v{APP_VERSION}")
            self.root.geometry("1100x700")
            self.root.minsize(950, 600)
            self.root.configure(bg=self.bg_color)
            
            # Setup ttk style
            self.style = ttk.Style()
            self.style.theme_use("clam")
            
            self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
            self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.accent_color)
            self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10, "italic"), foreground=self.text_dim)
            self.style.configure("TEntry", fieldbackground=self.card_color, foreground=self.text_color, 
                                 bordercolor=self.border_color, lightcolor=self.border_color, darkcolor=self.border_color)
            self.style.configure("TCombobox", fieldbackground=self.card_color, background=self.card_color, 
                                 foreground=self.text_color, arrowcolor=self.accent_color, bordercolor=self.border_color)
            self.style.map("TCombobox",
                           fieldbackground=[("readonly", self.card_color), ("disabled", self.card_color)],
                           foreground=[("readonly", self.text_color), ("disabled", self.text_dim)],
                           background=[("readonly", self.card_color), ("disabled", self.card_color), ("active", self.border_color)],
                           arrowcolor=[("disabled", self.text_dim), ("!disabled", self.accent_color)],
                           bordercolor=[("focus", self.accent_color), ("!focus", self.border_color)])
            
            # Notebook tabs
            self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
            self.style.configure("TNotebook.Tab", background=self.card_color, foreground=self.text_dim, 
                                 padding=[15, 6], font=("Segoe UI", 9, "bold"), borderwidth=1, bordercolor=self.border_color)
            self.style.map("TNotebook.Tab", 
                           background=[("selected", self.accent_color), ("active", self.border_color), ("", self.card_color)],
                           foreground=[("selected", "#ffffff"), ("active", self.text_color), ("", self.text_dim)])
            
            # Scrollbar Styling
            self.style.configure("Vertical.TScrollbar", background=self.card_color, troughcolor=self.bg_color, 
                                 bordercolor=self.border_color, arrowcolor=self.accent_color,
                                 lightcolor=self.border_color, darkcolor=self.border_color)
            self.style.map("Vertical.TScrollbar",
                           background=[("active", self.accent_color), ("pressed", self.accent_color), ("", self.card_color)],
                           arrowcolor=[("active", "#ffffff"), ("", self.accent_color)])
            self.style.configure("Horizontal.TScrollbar", background=self.card_color, troughcolor=self.bg_color, 
                                 bordercolor=self.border_color, arrowcolor=self.accent_color,
                                 lightcolor=self.border_color, darkcolor=self.border_color)
            self.style.map("Horizontal.TScrollbar",
                           background=[("active", self.accent_color), ("pressed", self.accent_color), ("", self.card_color)],
                           arrowcolor=[("active", "#ffffff"), ("", self.accent_color)])

            # Treeview Styling
            self.style.configure("Treeview", background=self.card_color, fieldbackground=self.card_color, 
                                 foreground=self.text_color, borderwidth=1, bordercolor=self.border_color,
                                 font=("Segoe UI", 9), rowheight=24)
            self.style.configure("Treeview.Heading", background=self.bg_color, foreground=self.accent_color,
                                 font=("Segoe UI", 9, "bold"), borderwidth=1, bordercolor=self.border_color)
            self.style.map("Treeview", 
                           background=[("selected", self.accent_color), ("!selected", self.card_color)],
                           foreground=[("selected", "#ffffff"), ("!selected", self.text_color)])

        # State Variables
        self.codec = FFXCodec()
        
        # Style the dropdown Listbox popup globally (white background, black text for high visibility on Windows)
        self.root.option_add("*TCombobox*Listbox.background", "#ffffff")
        self.root.option_add("*TCombobox*Listbox.foreground", "#000000")
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.accent_color)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.root.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))

        # Safeguard bind to force dropdown Listbox colors (white background, black text) on Windows
        def on_combobox_click(event):
            def configure_listbox(retries=0):
                try:
                    popdown = str(event.widget) + ".popdown"
                    listbox = popdown + ".f.l"
                    if event.widget.tk.call("winfo", "exists", listbox):
                        event.widget.tk.call(
                            listbox, "configure",
                            "-background", "#ffffff",
                            "-foreground", "#000000",
                            "-selectbackground", self.accent_color,
                            "-selectforeground", "#ffffff",
                            "-font", "{Segoe UI} 10"
                        )
                    elif retries < 10:
                        event.widget.after(20, lambda: configure_listbox(retries + 1))
                except Exception:
                    if retries < 10:
                        event.widget.after(20, lambda: configure_listbox(retries + 1))
            event.widget.after(5, configure_listbox)

        self.root.bind_class("TCombobox", "<ButtonPress-1>", on_combobox_click, add="+")
        self.root.bind_class("TCombobox", "<Down>", on_combobox_click, add="+")
        
        self.master_path = ""
        self.loc_name = "jppc"
        self.monsters_list = []      # list of dicts: {'id': 'm001', 'name': 'Dingo', 'path': '...', 'number': 1}
        self.current_monster = None  # selected dict
        self.chunks = []             # 7 bytearrays
        self.stat_bytes_jp = bytearray()
        self.stat_bytes_us = bytearray()
        self.loot_bytes = bytearray()
        self.jp_name = ""
        self.us_name = ""
        self.jp_sensor = ""
        self.us_sensor = ""
        self.jp_scan = ""
        self.us_scan = ""
        self.player_data_bytes = bytearray()
        
        # Mappings of items/commands
        self.item_name_map = {}
        self.items_list = []
        self.commands_list = []
        self.command_map = {}
        self.monmagic1_map = {}
        self.monmagic2_map = {}
        
        # Load Configuration
        self.config = self.load_config()
        
        # Caching & Dirty state tracking
        self.monster_cache = {}
        self.loaded_state = None
        self._handling_select = False
        self.encounter_parser = FFXEncounterParser()
        
        self.create_widgets()
        self.load_item_and_command_mappings()
        self.setup_syntax_highlighting()
        self.setup_shortcuts()
        
        self.auto_detect_directory()
        
    def load_config(self):
        config = {"master_path": ""}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config.update(json.load(f))
            except Exception:
                pass
        return config

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def log(self, text, tag=None):
        if self.is_embedded and hasattr(self.parent, "log"):
            self.parent.log(text, tag)
        else:
            if hasattr(self, "txt_log") and self.txt_log:
                self.txt_log.insert(tk.END, str(text) + "\n", tag or "default")
                self.txt_log.see(tk.END)
            else:
                print(text)

    def auto_detect_directory(self):
        # 1. Check saved config first
        config_path = self.config.get("master_path", "")
        if config_path and os.path.exists(config_path):
            self.ent_master_path.delete(0, tk.END)
            self.ent_master_path.insert(0, config_path)
            self.master_path = config_path
            self.codec.ffx_master_path = config_path
            self.log(f"Loaded master directory from config: {config_path}")
            self.scan_monsters()
            return

        # 2. Fallback to auto-detect relative to script
        detected_path = os.path.abspath(os.path.join(script_dir, "..", "VBF Browser", "extracted", "ffx_ps2", "ffx", "master"))
        if os.path.exists(detected_path):
            self.ent_master_path.delete(0, tk.END)
            self.ent_master_path.insert(0, detected_path)
            self.master_path = detected_path
            self.codec.ffx_master_path = detected_path
            self.log(f"Auto-detected FFX master directory: {detected_path}")
            self.scan_monsters()

    def scan_monsters(self):
        path = self.ent_master_path.get().strip()
        if not path or not os.path.exists(path):
            self.log("Invalid master directory path.", "error")
            return
            
        dirty_ids = [m_id for m_id, entry in self.monster_cache.items() if entry.get("is_dirty")]
        if dirty_ids:
            ans = show_dark_confirm(
                self.root,
                "Unsaved Changes",
                "You have unsaved monster modifications in memory.\n\n"
                "Do you want to save all modified monsters to disk before scanning?\n"
                "(Selecting 'No' will discard all your unsaved modifications)."
            )
            if ans is True:
                if not self.save_all_to_disk():
                    return
            elif ans is None:
                return
                
        self.monster_cache.clear()
        self.current_monster = None
        self.loaded_state = None
        
        self.master_path = path
        self.codec.ffx_master_path = path
        
        # Look for the localization folders that have battle/mon/
        # Gameplay data is technically read from jppc/battle/mon/
        mon_dir = os.path.join(path, "jppc", "battle", "mon")
        if not os.path.exists(mon_dir):
            # Try raw parent path if it's already battle/mon
            if path.endswith(os.path.join("battle", "mon")):
                mon_dir = path
            else:
                self.log(f"Could not find battle/mon directory under: {path}/jppc/", "error")
                return
 
        self.log(f"Scanning monsters in {mon_dir}...")
        
        # Load Item/Command mappings first to resolve dropdown lists
        self.load_item_and_command_mappings()
        
        # Clear list
        self.tree_monsters.delete(*self.tree_monsters.get_children())
        self.monsters_list.clear()
        
        folders = []
        for name in os.listdir(mon_dir):
            if name.startswith("_m") and os.path.isdir(os.path.join(mon_dir, name)):
                folders.append(name)
        folders.sort()
        
        for name in folders:
            folder_path = os.path.join(mon_dir, name)
            m_id = name[1:]  # "m001"
            bin_name = f"{m_id}.bin"
            bin_path = os.path.join(folder_path, bin_name)
            
            if os.path.exists(bin_path):
                # Try to decode name
                english_name = self.extract_monster_english_name(bin_path)
                m_num = int(m_id[1:])
                monster_info = {
                    "id": m_id,
                    "name": english_name or f"Monster {m_num}",
                    "path": bin_path,
                    "number": m_num
                }
                self.monsters_list.append(monster_info)
                self.tree_monsters.insert("", tk.END, iid=m_id, values=(m_id, monster_info["name"]))
                
        self.log(f"Scan complete. Found {len(self.monsters_list)} monsters.", "success")
        self.load_player_stats()

    def load_item_and_command_mappings(self):
        # We load items from uspc or new_uspc or jppc to resolve names
        loc = "new_uspc" if os.path.exists(os.path.join(self.master_path, "new_uspc")) else "jppc"
        
        self.item_name_map.clear()
        self.items_list.clear()
        self.commands_list.clear()
        
        # 1. Load items
        item_bin_path = os.path.join(self.master_path, loc, "battle", "kernel", "item.bin")
        if os.path.exists(item_bin_path):
            try:
                records, _, _, _ = self.codec.read_ffx_text_bin(item_bin_path, 92, "us")
                for r in records:
                    item_id = 0x2000 + r["id"]
                    self.item_name_map[item_id] = r["name"]
                    self.items_list.append((item_id, r["name"]))
            except Exception as e:
                self.log(f"Failed to load items: {e}", "error")
                
        # Helper to find kernel file in subdirectories
        def find_kernel_bin(filename):
            for sub in [loc, "new_uspc", "uspc", "new_jppc", "jppc"]:
                p = os.path.join(self.master_path, sub, "battle", "kernel", filename)
                if os.path.exists(p):
                    return p
            return None

        # 2. Load commands (command.bin) -> 0x0000 base & 0x3000 base
        cmd_path = find_kernel_bin("command.bin")
        if cmd_path:
            try:
                records, _, _, _ = self.codec.read_ffx_text_bin(cmd_path, 92, "us")
                for r in records:
                    if r["name"].strip():
                        cmd_id = r["id"]
                        self.command_map[cmd_id] = r["name"].strip()
                        self.item_name_map[cmd_id] = r["name"].strip()
                        self.commands_list.append((cmd_id, r["name"].strip()))
                        
                        m_id = 0x3000 + cmd_id
                        self.item_name_map[m_id] = r["name"].strip()
                        self.commands_list.append((m_id, r["name"].strip()))
            except Exception as e:
                self.log(f"Failed to load commands: {e}", "error")

        # 3. Load monster magic 1 (monmagic1.bin)
        mm1_path = find_kernel_bin("monmagic1.bin")
        if mm1_path:
            try:
                records, _, _, _ = self.codec.read_ffx_text_bin(mm1_path, 92, "us")
                for r in records:
                    if r["name"].strip():
                        self.monmagic1_map[r["id"]] = r["name"].strip()
            except Exception:
                pass

        # 4. Load monster magic 2 (monmagic2.bin) -> 0x4000 base
        mm2_path = find_kernel_bin("monmagic2.bin")
        if mm2_path:
            try:
                records, _, _, _ = self.codec.read_ffx_text_bin(mm2_path, 92, "us")
                for r in records:
                    if r["name"].strip():
                        self.monmagic2_map[r["id"]] = r["name"].strip()
                        m_id = 0x4000 + r["id"]
                        self.item_name_map[m_id] = r["name"].strip()
                        self.commands_list.append((m_id, r["name"].strip()))
            except Exception:
                pass
                
        # Fallbacks for items
        if not self.items_list:
            fallbacks = [
                (0x2000, "Potion"), (0x2001, "Hi-Potion"), (0x2002, "X-Potion"), (0x2003, "Mega-Potion"),
                (0x2004, "Ether"), (0x2005, "Turbo Ether"), (0x2006, "Phoenix Down"), (0x2007, "Mega Phoenix"),
                (0x2008, "Elixir"), (0x2009, "Megalixir"), (0x200A, "Antidote"), (0x200B, "Soft"),
                (0x200F, "Remedy")
            ]
            for item_id, name in fallbacks:
                self.item_name_map[item_id] = name
                self.items_list.append((item_id, name))
                
        # Merge comprehensive Master Abilities
        for cmd_id, name in FFX_MASTER_ABILITIES.items():
            if cmd_id not in self.item_name_map:
                self.item_name_map[cmd_id] = name
            if not any(c[0] == cmd_id for c in self.commands_list):
                self.commands_list.append((cmd_id, name))
                
        # Sort commands list logically by ID
        self.commands_list.sort(key=lambda x: x[0])
                
        # Update combo dropdowns
        item_combos = [
            self.cmb_drop_n_p_c, self.cmb_drop_n_p_r, self.cmb_drop_n_s_c, self.cmb_drop_n_s_r,
            self.cmb_drop_o_p_c, self.cmb_drop_o_p_r, self.cmb_drop_o_s_c, self.cmb_drop_o_s_r,
            self.cmb_steal_c, self.cmb_steal_r, self.cmb_bribe_item
        ]
        items_choices = [f"{name} ({hex(item_id)})" for item_id, name in self.items_list]
        for combo in item_combos:
            combo["values"] = ["None (0x0000)"] + items_choices
            
        self.cmb_ronso["values"] = ["None (0x0000)"] + [f"{name} ({hex(cmd_id)})" for cmd_id, name in self.commands_list]
        self.update_rule_builder_actions()

    def resolve_command_name(self, cmd_id):
        if cmd_id in [0, 4]:
            return "Attack (0x0)"
        if cmd_id in [0x6004, 0x6005, 0x6006, 0x6007]:
            flags = {0x6004: "Magic Counter", 0x6005: "Standby / Wait", 0x6006: "Defend", 0x6007: "Charge Energy"}
            return f"{flags[cmd_id]} ({hex(cmd_id)})"

        m_id = self.current_monster["id"] if self.current_monster else "m001"
        m_name = self.current_monster["name"].lower() if self.current_monster else ""
        m_num_str = m_id.replace("_m", "").replace("m", "")
        m_num = int(m_num_str) if m_num_str.isdigit() else 1
        
        is_boss_or_aeon = any(k in m_name for k in ["boss", "dark", "seymour", "jecht", "penance", "sin", "nemesis", "anima", "yojimbo", "weapon", "sister", "cindy", "sandy", "mindy", "valefor", "ifrit", "ixion", "shiva", "bahamut"]) or m_num >= 270 or (101 <= m_num <= 176)

        # 1. 0x3000 base
        if 0x3000 <= cmd_id <= 0x3FFF:
            sub = cmd_id - 0x3000
            if sub in self.command_map and 0x30 <= sub <= 0x60:
                return f"{self.command_map[sub]} ({hex(cmd_id)})"
            if not is_boss_or_aeon and sub in self.monmagic1_map and not self.monmagic1_map[sub].startswith("Command "):
                return f"{self.monmagic1_map[sub]} ({hex(cmd_id)})"
            if sub in self.command_map:
                return f"{self.command_map[sub]} ({hex(cmd_id)})"
            if sub in self.monmagic1_map:
                return f"{self.monmagic1_map[sub]} ({hex(cmd_id)})"

        # 2. 0x4000 base
        if 0x4000 <= cmd_id <= 0x4FFF:
            sub = cmd_id - 0x4000
            if is_boss_or_aeon:
                if sub in self.monmagic2_map and not self.monmagic2_map[sub].startswith("Command "):
                    return f"{self.monmagic2_map[sub]} ({hex(cmd_id)})"
                if sub in self.monmagic1_map and not self.monmagic1_map[sub].startswith("Command "):
                    return f"{self.monmagic1_map[sub]} ({hex(cmd_id)})"
            else:
                if sub in self.monmagic1_map and not self.monmagic1_map[sub].startswith("Command "):
                    return f"{self.monmagic1_map[sub]} ({hex(cmd_id)})"
                if sub in self.monmagic2_map and not self.monmagic2_map[sub].startswith("Command "):
                    return f"{self.monmagic2_map[sub]} ({hex(cmd_id)})"
            if sub in self.command_map:
                return f"{self.command_map[sub]} ({hex(cmd_id)})"

        # 3. Direct match in loaded maps
        if cmd_id in self.item_name_map:
            return f"{self.item_name_map[cmd_id]} ({hex(cmd_id)})"
            
        for cid, name in self.commands_list:
            if cid == cmd_id:
                return f"{name} ({hex(cmd_id)})"
                
        # 4. Match in Master Abilities Dictionary
        if cmd_id in FFX_MASTER_ABILITIES:
            return f"{FFX_MASTER_ABILITIES[cmd_id]} ({hex(cmd_id)})"
            
        return f"Action {cmd_id} ({hex(cmd_id)})"

    def extract_monster_english_name(self, filepath):
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            chunks = packer.unpack_chunks(data)
            if len(chunks) > 6:
                chunk6 = chunks[6]
                if len(chunk6) >= 128:
                    offset = struct.unpack("<H", chunk6[0:2])[0]
                    name = self.codec.decode_ffx_bytes(chunk6[128:], offset, "us")
                    return name
        except Exception:
            pass
        return ""

    def get_current_gui_state(self):
        state = {}
        # Entry fields
        state["jp_name"] = self.ent_jp_name.get()
        state["us_name"] = self.ent_us_name.get()
        state["jp_sensor"] = self.txt_jp_sensor.get("1.0", tk.END).strip()
        state["us_sensor"] = self.txt_us_sensor.get("1.0", tk.END).strip()
        state["jp_scan"] = self.txt_jp_scan.get("1.0", tk.END).strip()
        state["us_scan"] = self.txt_us_scan.get("1.0", tk.END).strip()
        
        # StringVars / IntVars
        vars_to_track = [
            "var_hp", "var_mp", "var_overkill",
            "var_str", "var_def", "var_mag", "var_mdf", "var_agi", "var_lck", "var_eva", "var_acc",
            "var_armored", "var_doom", "var_arena_idx", "var_sound_ref",
            "var_res_death", "var_res_zombie", "var_res_petrify", "var_res_poison",
            "var_res_powerbreak", "var_res_magicbreak", "var_res_armorbreak", "var_res_mentalbreak",
            "var_res_confuse", "var_res_berserk", "var_res_provoke", "var_res_threaten",
            "var_res_sleep", "var_res_silence", "var_res_darkness", "var_res_slow", "var_res_haste",
            "var_auto_zombie", "var_auto_poison", "var_auto_haste", "var_auto_regen",
            "var_auto_protect", "var_auto_shell", "var_auto_reflect", "var_auto_autolife", "var_auto_doom",
            "var_gil", "var_ap_n", "var_ap_o",
            "var_pct_drop_p", "var_pct_drop_s", "var_pct_steal", "var_pct_gear",
            "var_qty_drop_n_p_c", "var_qty_drop_n_p_r", "var_qty_drop_n_s_c", "var_qty_drop_n_s_r",
            "var_qty_drop_o_p_c", "var_qty_drop_o_p_r", "var_qty_drop_o_s_c", "var_qty_drop_o_s_r",
            "var_qty_steal_c", "var_qty_steal_r", "var_qty_bribe", "var_zanmato",
            "var_gil_steal", "var_arena_price",
            "var_weapon_bias", "var_max_slots", "var_slot_variance", "var_ability_weight"
        ]
        for v in vars_to_track:
            if hasattr(self, v):
                state[v] = getattr(self, v).get()
                
        # Comboboxes
        combos_to_track = [
            "cmb_elem_fire", "cmb_elem_ice", "cmb_elem_thunder", "cmb_elem_water", "cmb_elem_holy",
            "cmb_ronso", "cmb_drop_n_p_c", "cmb_drop_n_p_r", "cmb_drop_n_s_c", "cmb_drop_n_s_r",
            "cmb_drop_o_p_c", "cmb_drop_o_p_r", "cmb_drop_o_s_c", "cmb_drop_o_s_r",
            "cmb_steal_c", "cmb_steal_r", "cmb_bribe_item"
        ]
        for c in combos_to_track:
            if hasattr(self, c):
                state[c] = getattr(self, c).get()
                
        return state

    def check_is_dirty(self):
        if not self.current_monster or not hasattr(self, "loaded_state") or self.loaded_state is None:
            return False
        current = self.get_current_gui_state()
        for k, v in self.loaded_state.items():
            if current.get(k) != v:
                return True
        return False

    def update_monster_tree_name(self, m_id, name, is_modified):
        m = next((m for m in self.monsters_list if m["id"] == m_id), None)
        base_name = name or (m["name"] if m else "")
        display_name = f"* {base_name}" if is_modified else base_name
        self.tree_monsters.item(m_id, values=(m_id, display_name))

    def apply_monster_edits_silent(self):
        if not self.current_monster:
            return
            
        m_id = self.current_monster["id"]
        
        # Serialize GUI variables to bytes in memory
        jp_name = self.ent_jp_name.get().strip()
        us_name = self.ent_us_name.get().strip()
        
        jp_sensor = self.txt_jp_sensor.get("1.0", tk.END).strip()
        us_sensor = self.txt_us_sensor.get("1.0", tk.END).strip()
        
        jp_scan = self.txt_jp_scan.get("1.0", tk.END).strip()
        us_scan = self.txt_us_scan.get("1.0", tk.END).strip()
        
        new_stat_jp = self.serialize_stat_block(self.stat_bytes_jp, jp_name, jp_sensor, jp_scan, "jp")
        new_stat_us = self.serialize_stat_block(self.stat_bytes_us, us_name, us_sensor, us_scan, "us")
        new_loot = self.serialize_loot_block()
        
        new_chunks = list(self.chunks)
        new_chunks[2] = new_stat_jp
        new_chunks[4] = new_loot
        new_chunks[6] = new_stat_us
        
        self.monster_cache[m_id] = {
            "chunks": new_chunks,
            "stat_bytes_jp": new_stat_jp,
            "stat_bytes_us": new_stat_us,
            "loot_bytes": new_loot,
            "us_name": us_name,
            "is_dirty": True
        }
        
        self.loaded_state = self.get_current_gui_state()
        self.update_monster_tree_name(m_id, us_name, is_modified=True)

    def apply_monster_edits(self):
        if not self.current_monster:
            messagebox.showwarning("Warning", "No active monster loaded.")
            return
        
        try:
            self.apply_monster_edits_silent()
            us_name = self.ent_us_name.get().strip()
            self.log(f"Applied edits for {self.current_monster['id']} to memory cache.")
            messagebox.showinfo("Applied", f"Applied edits for {us_name or self.current_monster['id']} to memory cache successfully. Use 'Save All to Disk' or 'Save Monster .bin' to write changes to disk.")
        except Exception as e:
            self.log(f"Failed to apply edits: {e}", "error")
            messagebox.showerror("Error", f"Failed to serialize changes:\n{str(e)}")

    def save_all_to_disk(self):
        if self.current_monster and self.check_is_dirty():
            try:
                self.apply_monster_edits_silent()
            except Exception as e:
                self.log(f"Failed to apply active edits before saving: {e}", "error")
                messagebox.showerror("Error", f"Failed to serialize changes for active monster:\n{str(e)}")
                return False

        dirty_ids = [m_id for m_id, entry in self.monster_cache.items() if entry.get("is_dirty")]
        if not dirty_ids:
            messagebox.showinfo("Save All", "No modified monsters in memory to save.")
            return True
            
        success_count = 0
        self.log(f"Saving {len(dirty_ids)} modified monsters to disk...")
        
        for m_id in dirty_ids:
            cache_entry = self.monster_cache[m_id]
            m = next((x for x in self.monsters_list if x["id"] == m_id), None)
            if not m:
                continue
            filepath = m["path"]
            
            try:
                repacked_data = packer.repack_chunks(cache_entry["chunks"])
                
                # Backup and write
                bak_path = filepath + ".bak"
                if not os.path.exists(bak_path):
                    shutil.copy2(filepath, bak_path)
                    
                packer.safe_atomic_write(filepath, repacked_data)
                    
                cache_entry["is_dirty"] = False
                
                us_name = cache_entry["us_name"]
                self.update_monster_tree_name(m_id, us_name, is_modified=False)
                
                m["name"] = us_name
                success_count += 1
                self.log(f"Saved {m_id}.bin successfully to disk.", "success")
            except Exception as e:
                self.log(f"Failed to save {m_id}.bin: {e}", "error")
                messagebox.showerror("Error", f"Failed to save {m_id}.bin:\n{str(e)}")
                
        messagebox.showinfo("Success", f"Successfully saved {success_count} monsters to disk!")
        return success_count == len(dirty_ids)

    def open_batch_scale_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("⚖️ Batch Scale Monster Stats")
        dialog.geometry("450x780")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        lbl_header = tk.Label(dialog, text="⚖️ Batch Scale Monster Stats", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 14, "bold"))
        lbl_header.pack(pady=(15, 5))
        lbl_sub = tk.Label(dialog, text="Enter multipliers to scale monster stats.\n(Calculated from original game files to prevent compounding).", bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 9, "italic"), justify="center")
        lbl_sub.pack(pady=(0, 15))
        
        # Checkboxes Container
        chk_frame = tk.LabelFrame(dialog, text=" Select Monster Categories to Scale ", bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        chk_frame.pack(fill="x", padx=40, pady=(0, 10))
        
        self.var_chk_all = tk.BooleanVar(value=True)
        self.var_chk_tutorial = tk.BooleanVar(value=False)
        self.var_chk_story = tk.BooleanVar(value=False)
        self.var_chk_optional = tk.BooleanVar(value=False)
        self.var_chk_fiends = tk.BooleanVar(value=False)
        
        def on_all_toggled():
            if self.var_chk_all.get():
                self.var_chk_tutorial.set(False)
                self.var_chk_story.set(False)
                self.var_chk_optional.set(False)
                self.var_chk_fiends.set(False)
                
        def on_other_toggled():
            if (self.var_chk_tutorial.get() or self.var_chk_story.get() or 
                self.var_chk_optional.get() or self.var_chk_fiends.get()):
                self.var_chk_all.set(False)
            else:
                self.var_chk_all.set(True)
                
        chk_all = tk.Checkbutton(chk_frame, text="All Monsters", variable=self.var_chk_all, command=on_all_toggled, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color, font=("Segoe UI", 9))
        chk_all.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        chk_tut = tk.Checkbutton(chk_frame, text="Tutorial & Prologue", variable=self.var_chk_tutorial, command=on_other_toggled, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color, font=("Segoe UI", 9))
        chk_tut.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        chk_story = tk.Checkbutton(chk_frame, text="Main Story Bosses", variable=self.var_chk_story, command=on_other_toggled, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color, font=("Segoe UI", 9))
        chk_story.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        chk_opt = tk.Checkbutton(chk_frame, text="Optional & Endgame", variable=self.var_chk_optional, command=on_other_toggled, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color, font=("Segoe UI", 9))
        chk_opt.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        chk_fiends = tk.Checkbutton(chk_frame, text="Normal Fiends / Others", variable=self.var_chk_fiends, command=on_other_toggled, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color, font=("Segoe UI", 9))
        chk_fiends.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Form Container
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="x", padx=40)
        
        # Helper to add entry row
        def add_row(parent, row, label_text, default_val):
            lbl = tk.Label(parent, text=label_text, bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 10))
            lbl.grid(row=row, column=0, sticky="w", pady=5)
            var = tk.StringVar(value=default_val)
            ent = ttk.Entry(parent, textvariable=var, width=12)
            ent.grid(row=row, column=1, sticky="e", pady=5)
            return var
            
        var_hp = add_row(form_frame, 0, "HP / Overkill Multiplier:", "1.0")
        var_mp = add_row(form_frame, 1, "MP Multiplier:", "1.0")
        var_str_mag = add_row(form_frame, 2, "Strength & Magic Multiplier:", "1.0")
        var_def_mdf = add_row(form_frame, 3, "Defense & MDF Multiplier:", "1.0")
        var_agi = add_row(form_frame, 4, "Agility / Speed Multiplier:", "1.0")
        var_res = add_row(form_frame, 5, "Status Resistance Mult:", "1.0")
        var_res_floor = add_row(form_frame, 6, "Min Status Res Floor (if 0):", "0")
        var_misc = add_row(form_frame, 7, "Luck / Eva / Acc Multiplier:", "1.0")
        
        var_gil = add_row(form_frame, 8, "Gil Reward Multiplier:", "1.0")
        var_ap = add_row(form_frame, 9, "AP Reward Multiplier:", "1.0")
        var_items = add_row(form_frame, 10, "Item Quantity Multiplier:", "1.0")
        
        form_frame.columnconfigure(0, weight=1)
        
        # Presets Bar
        preset_frame = tk.Frame(dialog, bg=self.bg_color)
        preset_frame.pack(fill="x", padx=40, pady=(10, 0))
        tk.Label(preset_frame, text="Preset:", bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        
        cmb_preset = ttk.Combobox(preset_frame, values=[
            "Custom",
            "Standard Hard Mode (1.5x)",
            "Nightmare Mode (2.5x)",
            "Casual Speedrun (0.6x)",
            "Boss Rush Challenge (2.0x)",
            "Gold & AP Farm (3.0x)"
        ], state="readonly", width=20)
        cmb_preset.set("Custom")
        cmb_preset.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        def on_preset_selected(e=None):
            p = cmb_preset.get()
            if p == "Standard Hard Mode (1.5x)":
                var_hp.set("1.5"); var_mp.set("1.2"); var_str_mag.set("1.25"); var_def_mdf.set("1.2")
                var_agi.set("1.15"); var_res.set("1.25"); var_res_floor.set("20"); var_misc.set("1.1")
                var_gil.set("1.2"); var_ap.set("1.2"); var_items.set("1.0")
            elif p == "Nightmare Mode (2.5x)":
                var_hp.set("2.5"); var_mp.set("2.0"); var_str_mag.set("1.5"); var_def_mdf.set("1.4")
                var_agi.set("1.3"); var_res.set("1.5"); var_res_floor.set("40"); var_misc.set("1.2")
                var_gil.set("1.5"); var_ap.set("1.5"); var_items.set("1.0")
            elif p == "Casual Speedrun (0.6x)":
                var_hp.set("0.6"); var_mp.set("0.8"); var_str_mag.set("0.75"); var_def_mdf.set("0.7")
                var_agi.set("0.9"); var_res.set("0.8"); var_res_floor.set("0"); var_misc.set("1.0")
                var_gil.set("2.0"); var_ap.set("2.0"); var_items.set("2.0")
            elif p == "Boss Rush Challenge (2.0x)":
                var_hp.set("2.0"); var_mp.set("1.5"); var_str_mag.set("1.4"); var_def_mdf.set("1.3")
                var_agi.set("1.25"); var_res.set("1.3"); var_res_floor.set("30"); var_misc.set("1.15")
                var_gil.set("2.0"); var_ap.set("2.0"); var_items.set("1.0")
            elif p == "Gold & AP Farm (3.0x)":
                var_hp.set("1.0"); var_mp.set("1.0"); var_str_mag.set("1.0"); var_def_mdf.set("1.0")
                var_agi.set("1.0"); var_res.set("1.0"); var_res_floor.set("0"); var_misc.set("1.0")
                var_gil.set("3.0"); var_ap.set("3.0"); var_items.set("2.0")
                
        cmb_preset.bind("<<ComboboxSelected>>", on_preset_selected)
        
        def save_preset_json():
            f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Save Scaling Preset")
            if f:
                data = {
                    "hp": var_hp.get(), "mp": var_mp.get(), "str_mag": var_str_mag.get(), "def_mdf": var_def_mdf.get(),
                    "agi": var_agi.get(), "res": var_res.get(), "res_floor": var_res_floor.get(), "misc": var_misc.get(),
                    "gil": var_gil.get(), "ap": var_ap.get(), "items": var_items.get()
                }
                with open(f, "w") as fp:
                    json.dump(data, fp, indent=2)
                messagebox.showinfo("Saved", "Scaling preset saved successfully!")
                
        def load_preset_json():
            f = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")], title="Load Scaling Preset")
            if f and os.path.exists(f):
                try:
                    with open(f, "r") as fp:
                        data = json.load(fp)
                    if "hp" in data: var_hp.set(data["hp"])
                    if "mp" in data: var_mp.set(data["mp"])
                    if "str_mag" in data: var_str_mag.set(data["str_mag"])
                    if "def_mdf" in data: var_def_mdf.set(data["def_mdf"])
                    if "agi" in data: var_agi.set(data["agi"])
                    if "res" in data: var_res.set(data["res"])
                    if "res_floor" in data: var_res_floor.set(data["res_floor"])
                    if "misc" in data: var_misc.set(data["misc"])
                    if "gil" in data: var_gil.set(data["gil"])
                    if "ap" in data: var_ap.set(data["ap"])
                    if "items" in data: var_items.set(data["items"])
                    cmb_preset.set("Custom")
                    messagebox.showinfo("Loaded", "Scaling preset loaded successfully!")
                except Exception as ex:
                    messagebox.showerror("Error", f"Failed to load preset:\n{ex}")
                    
        btn_save_p = tk.Button(preset_frame, text="💾", command=save_preset_json, bg=self.card_color, fg=self.text_color, relief="flat", padx=5)
        btn_save_p.pack(side="left", padx=2)
        btn_load_p = tk.Button(preset_frame, text="📂", command=load_preset_json, bg=self.card_color, fg=self.text_color, relief="flat", padx=5)
        btn_load_p.pack(side="left", padx=2)
        
        # Button container
        btn_frame = tk.Frame(dialog, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=40, pady=(20, 0))
        
        btn_scale = tk.Button(btn_frame, text="⚡ Apply Multipliers", 
                              command=lambda: self.run_batch_scale(var_hp, var_mp, var_str_mag, var_def_mdf, var_agi, var_res, var_res_floor, var_misc, var_gil, var_ap, var_items, dialog),
                              bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground=self.accent_hover)
        btn_scale.pack(fill="x", pady=(0, 10))
        self.bind_hover(btn_scale, is_primary=True)
        
        btn_revert = tk.Button(btn_frame, text="⏪ Revert All to Original Stats", 
                               command=lambda: self.run_revert_all(dialog),
                               bg=self.card_color, fg=self.text_color, font=("Segoe UI", 10), relief="flat", activebackground=self.border_color)
        btn_revert.pack(fill="x")
        self.bind_hover(btn_revert, is_primary=False)

    def run_batch_scale(self, hp_mult, mp_mult, str_mag_mult, def_mdf_mult, agi_mult, res_mult, res_floor, misc_mult, gil_mult, ap_mult, item_mult, dialog):
        path = self.ent_master_path.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Invalid master directory path.")
            return
            
        mon_dir = os.path.join(path, "jppc", "battle", "mon")
        if not os.path.exists(mon_dir):
            if path.endswith(os.path.join("battle", "mon")):
                mon_dir = path
            else:
                messagebox.showerror("Error", f"Could not find battle/mon directory under: {path}/jppc/")
                return
                
        all_folders = [name for name in os.listdir(mon_dir) if name.startswith("_m") and os.path.isdir(os.path.join(mon_dir, name))]
        if not all_folders:
            messagebox.showinfo("Info", "No monster folders found to scale.")
            return
            
        # Category lists
        tutorial_ids = {"m159", "m170", "m107", "m108", "m158", "m101", "m232", "m230", "m144", "m114", "m115", "m116", "m145", "m147", "m148"}
        story_ids = {"m153", "m102", "m103", "m110", "m156", "m104", "m117", "m160", "m161", "m111", "m121", "m122", "m123", "m124", "m125", "m141", "m222", "m212", "m119", "m120", "m126", "m127", "m229", "m134", "m135", "m142", "m143", "m128", "m129", "m130", "m136", "m137", "m139", "m138", "m140", "m113", "m131", "m132", "m173", "m174", "m176"}
        optional_ids = {"m109", "m099", "m100", "m334", "m335", "m336", "m337", "m338", "m339", "m340", "m341", "m342", "m343", "m344", "m345", "m346", "m276"}
        
        folders = []
        for name in all_folders:
            m_id = name[1:]
            is_tutorial = m_id in tutorial_ids
            is_story = m_id in story_ids
            is_optional = m_id in optional_ids
            is_fiend = not (is_tutorial or is_story or is_optional)
            
            should_scale = False
            if self.var_chk_all.get():
                should_scale = True
            else:
                if self.var_chk_tutorial.get() and is_tutorial:
                    should_scale = True
                if self.var_chk_story.get() and is_story:
                    should_scale = True
                if self.var_chk_optional.get() and is_optional:
                    should_scale = True
                if self.var_chk_fiends.get() and is_fiend:
                    should_scale = True
            
            if should_scale:
                folders.append(name)
                
        if not folders:
            messagebox.showinfo("Info", "No monsters matching the selected categories were found.")
            return
            
        try:
            hp_m = float(hp_mult.get())
            mp_m = float(mp_mult.get())
            sm_m = float(str_mag_mult.get())
            dm_m = float(def_mdf_mult.get())
            ag_m = float(agi_mult.get())
            res_m = float(res_mult.get())
            res_f = int(res_floor.get())
            ms_m = float(misc_mult.get())
            gil_m = float(gil_mult.get())
            ap_m = float(ap_mult.get())
            item_m = float(item_mult.get())
        except ValueError:
            messagebox.showerror("Error", "All multipliers must be numeric, and floor must be an integer.")
            return
            
        self.log(f"Starting batch scaling for {len(folders)} monsters: HP={hp_m}x, MP={mp_m}x, Str/Mag={sm_m}x, Def/MDF={dm_m}x, Agi={ag_m}x, StatusRes={res_m}x, StatusResFloor={res_f}, Luck/Eva/Acc={ms_m}x, Gil={gil_m}x, AP={ap_m}x, Items={item_m}x")
        
        success_count = 0
        for name in folders:
            folder_path = os.path.join(mon_dir, name)
            m_id = name[1:]
            bin_name = f"{m_id}.bin"
            bin_path = os.path.join(folder_path, bin_name)
            bak_path = bin_path + ".bak"
            
            if not os.path.exists(bin_path):
                continue
                
            try:
                if not os.path.exists(bak_path):
                    shutil.copy2(bin_path, bak_path)
                    self.log(f"Created backup of original file at {bak_path}")
                
                with open(bak_path, "rb") as f:
                    data = f.read()
                    
                chunks = packer.unpack_chunks(data)
                if len(chunks) < 7:
                    continue
                    
                # 1. Scale Stats and Status Resistances in Chunk 2 and Chunk 6
                for chunk_idx in [2, 6]:
                    c_bytes = bytearray(chunks[chunk_idx])
                    if len(c_bytes) < 128:
                        continue
                        
                    old_hp = struct.unpack("<I", c_bytes[0x14:0x18])[0]
                    old_mp = struct.unpack("<I", c_bytes[0x18:0x1C])[0]
                    old_overkill = struct.unpack("<I", c_bytes[0x1C:0x20])[0]
                    
                    new_hp = int(old_hp * hp_m)
                    new_mp = int(old_mp * mp_m)
                    new_overkill = int(old_overkill * hp_m)
                    
                    struct.pack_into("<I", c_bytes, 0x14, new_hp)
                    struct.pack_into("<I", c_bytes, 0x18, new_mp)
                    struct.pack_into("<I", c_bytes, 0x1C, new_overkill)
                    
                    old_str = c_bytes[0x20]
                    old_def = c_bytes[0x21]
                    old_mag = c_bytes[0x22]
                    old_mdf = c_bytes[0x23]
                    old_agi = c_bytes[0x24]
                    old_lck = c_bytes[0x25]
                    old_eva = c_bytes[0x26]
                    old_acc = c_bytes[0x27]
                    
                    new_str = min(255, max(1, int(old_str * sm_m)))
                    new_def = min(255, max(1, int(old_def * dm_m)))
                    new_mag = min(255, max(1, int(old_mag * sm_m)))
                    new_mdf = min(255, max(1, int(old_mdf * dm_m)))
                    new_agi = min(255, max(1, int(old_agi * ag_m)))
                    new_lck = min(255, max(1, int(old_lck * ms_m)))
                    new_eva = min(255, max(0, int(old_eva * ms_m)))
                    new_acc = min(255, max(0, int(old_acc * ms_m)))
                    
                    c_bytes[0x20] = new_str
                    c_bytes[0x21] = new_def
                    c_bytes[0x22] = new_mag
                    c_bytes[0x23] = new_mdf
                    c_bytes[0x24] = new_agi
                    c_bytes[0x25] = new_lck
                    c_bytes[0x26] = new_eva
                    c_bytes[0x27] = new_acc
                    
                    # Status Resists (offsets: 0x2F to 0x3D, 0x46, 0x47)
                    res_offsets = [0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x46, 0x47]
                    for off in res_offsets:
                        old_res = c_bytes[off]
                        if old_res != 255:  # skip immunity
                            if old_res == 0 and res_f > 0:
                                new_res = min(254, max(0, res_f))
                            else:
                                new_res = min(254, max(0, int(old_res * res_m)))
                            c_bytes[off] = new_res
                            
                    chunks[chunk_idx] = bytes(c_bytes)
                    
                # 2. Scale Gil, AP, and Item Quantities in Chunk 4 (Loot)
                loot_bytes = bytearray(chunks[4])
                if len(loot_bytes) >= 0x30:
                    old_gil = struct.unpack("<H", loot_bytes[0x00:0x02])[0]
                    old_ap_n = struct.unpack("<H", loot_bytes[0x02:0x04])[0]
                    old_ap_o = struct.unpack("<H", loot_bytes[0x04:0x06])[0]
                    
                    new_gil = min(65535, max(0, int(old_gil * gil_m)))
                    new_ap_n = min(65535, max(0, int(old_ap_n * ap_m)))
                    new_ap_o = min(65535, max(0, int(old_ap_o * ap_m)))
                    
                    struct.pack_into("<H", loot_bytes, 0x00, new_gil)
                    struct.pack_into("<H", loot_bytes, 0x02, new_ap_n)
                    struct.pack_into("<H", loot_bytes, 0x04, new_ap_o)
                    
                    qty_offsets = [0x14, 0x15, 0x16, 0x17, 0x20, 0x21, 0x22, 0x23, 0x28, 0x29, 0x2C]
                    for off in qty_offsets:
                        old_qty = loot_bytes[off]
                        if old_qty > 0:
                            new_qty = min(99, max(1, int(old_qty * item_m)))
                            loot_bytes[off] = new_qty
                            
                    chunks[4] = bytes(loot_bytes)
                    
                repacked_data = packer.repack_chunks(chunks)
                packer.safe_atomic_write(bin_path, repacked_data)
                    
                if m_id in self.monster_cache:
                    del self.monster_cache[m_id]
                    
                success_count += 1
            except Exception as e:
                self.log(f"Failed to scale {bin_name}: {e}", "error")
                
        self.log(f"Batch scaling complete. Successfully scaled {success_count} monsters.", "success")
        messagebox.showinfo("Success", f"Successfully scaled {success_count} monsters!")
        
        if self.current_monster:
            self.load_monster_file(self.current_monster["id"])
            
        dialog.destroy()

    def run_revert_all(self, dialog):
        path = self.ent_master_path.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Invalid master directory path.")
            return
            
        mon_dir = os.path.join(path, "jppc", "battle", "mon")
        if not os.path.exists(mon_dir):
            if path.endswith(os.path.join("battle", "mon")):
                mon_dir = path
            else:
                messagebox.showerror("Error", f"Could not find battle/mon directory under: {path}/jppc/")
                return
                
        folders = [name for name in os.listdir(mon_dir) if name.startswith("_m") and os.path.isdir(os.path.join(mon_dir, name))]
        if not folders:
            return
            
        if not messagebox.askyesno("Confirm Revert", "Are you sure you want to revert all monster files back to their original (.bak) stats?"):
            return
            
        success_count = 0
        for name in folders:
            folder_path = os.path.join(mon_dir, name)
            m_id = name[1:]
            bin_name = f"{m_id}.bin"
            bin_path = os.path.join(folder_path, bin_name)
            bak_path = bin_path + ".bak"
            
            if os.path.exists(bak_path):
                try:
                    shutil.copy2(bak_path, bin_path)
                    if m_id in self.monster_cache:
                        del self.monster_cache[m_id]
                    success_count += 1
                except Exception as e:
                    self.log(f"Failed to revert {bin_name}: {e}", "error")
                    
        self.log(f"Revert complete. Successfully restored {success_count} original files.", "success")
        messagebox.showinfo("Success", f"Successfully restored {success_count} original files!")
        
        if self.current_monster:
            self.load_monster_file(self.current_monster["id"])
            
        dialog.destroy()

    def on_batch_scale_selected(self):
        sel = self.tree_monsters.selection()
        if not sel:
            return
        
        # Build custom styled dark scale dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("⚖️ Scale Selected Monster Stats")
        dialog.geometry("380x300")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        lbl_header = tk.Label(dialog, text="⚖️ Scale Selected Monsters", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 12, "bold"))
        lbl_header.pack(pady=(15, 5))
        
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="x", padx=40, pady=10)
        
        lbl_hp = tk.Label(form_frame, text="HP Multiplier:", bg=self.bg_color, fg=self.text_color)
        lbl_hp.grid(row=0, column=0, sticky="w", pady=5)
        var_hp = tk.StringVar(value="1.5")
        ent_hp = ttk.Entry(form_frame, textvariable=var_hp, width=10)
        ent_hp.grid(row=0, column=1, sticky="e", pady=5)
        
        lbl_str = tk.Label(form_frame, text="Stats Multiplier:", bg=self.bg_color, fg=self.text_color)
        lbl_str.grid(row=1, column=0, sticky="w", pady=5)
        var_str = tk.StringVar(value="1.2")
        ent_str = ttk.Entry(form_frame, textvariable=var_str, width=10)
        ent_str.grid(row=1, column=1, sticky="e", pady=5)
        
        form_frame.columnconfigure(0, weight=1)
        
        def run_scale():
            try:
                hp_mult = float(var_hp.get())
                stat_mult = float(var_str.get())
            except ValueError:
                messagebox.showerror("Error", "Multipliers must be numeric values.")
                return
                
            success = 0
            for item in sel:
                m = next((x for x in self.monsters_list if x["id"] == item), None)
                if not m:
                    continue
                bin_path = m["path"]
                bak_path = bin_path + ".bak"
                try:
                    if not os.path.exists(bak_path):
                        shutil.copy2(bin_path, bak_path)
                    with open(bak_path, "rb") as f:
                        data = f.read()
                    chunks = packer.unpack_chunks(data)
                    if len(chunks) < 7:
                        continue
                        
                    for chunk_idx in [2, 6]:
                        c_bytes = bytearray(chunks[chunk_idx])
                        if len(c_bytes) < 128:
                            continue
                            
                        # HP
                        old_hp = struct.unpack("<I", c_bytes[0x14:0x18])[0]
                        old_overkill = struct.unpack("<I", c_bytes[0x1C:0x20])[0]
                        struct.pack_into("<I", c_bytes, 0x14, int(old_hp * hp_mult))
                        struct.pack_into("<I", c_bytes, 0x1C, int(old_overkill * hp_mult))
                        
                        # Attributes
                        for off in [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]:
                            c_bytes[off] = min(255, max(0, int(c_bytes[off] * stat_mult)))
                            
                        chunks[chunk_idx] = bytes(c_bytes)
                        
                    repacked_data = packer.repack_chunks(chunks)
                    packer.safe_atomic_write(bin_path, repacked_data)
                    if item in self.monster_cache:
                        del self.monster_cache[item]
                    success += 1
                except Exception as e:
                    self.log(f"Failed scaling {item}: {e}", "error")
                    
            self.log(f"Scaled stats for {success} selected monsters.", "success")
            messagebox.showinfo("Success", f"Successfully scaled {success} monsters!")
            if self.current_monster:
                self.load_monster_file(self.current_monster["id"])
            dialog.destroy()
            
        btn_apply = tk.Button(dialog, text="Scale Selected", command=run_scale, bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief="flat", activebackground=self.accent_hover)
        btn_apply.pack(fill="x", padx=40, pady=15)
        self.bind_hover(btn_apply, is_primary=True)

    def on_batch_immune_selected(self):
        sel = self.tree_monsters.selection()
        if not sel:
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("🛡️ Immunize Selected Monsters")
        dialog.geometry("380x280")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        lbl_header = tk.Label(dialog, text="🛡️ Make Selected Monsters Immune", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 12, "bold"))
        lbl_header.pack(pady=(15, 5))
        
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="x", padx=40, pady=10)
        
        lbl_status = tk.Label(form_frame, text="Select Status Effect:", bg=self.bg_color, fg=self.text_color)
        lbl_status.grid(row=0, column=0, sticky="w", pady=5)
        
        status_opts = ["Death", "Zombie", "Petrify", "Poison", "Confuse", "Berserk", "Sleep", "Silence", "Darkness", "Slow"]
        cmb_status = ttk.Combobox(form_frame, values=status_opts, state="readonly", width=18)
        cmb_status.set("Death")
        cmb_status.grid(row=0, column=1, sticky="e", pady=5)
        
        form_frame.columnconfigure(0, weight=1)
        
        status_offset_map = {
            "Death": 0x2F, "Zombie": 0x30, "Petrify": 0x31, "Poison": 0x32,
            "Confuse": 0x37, "Berserk": 0x38, "Sleep": 0x3B, "Silence": 0x3C,
            "Darkness": 0x3D, "Slow": 0x47
        }
        
        def run_immune():
            status_name = cmb_status.get()
            target_off = status_offset_map.get(status_name)
            if target_off is None:
                return
                
            success = 0
            for item in sel:
                m = next((x for x in self.monsters_list if x["id"] == item), None)
                if not m:
                    continue
                bin_path = m["path"]
                bak_path = bin_path + ".bak"
                try:
                    if not os.path.exists(bak_path):
                        shutil.copy2(bin_path, bak_path)
                    with open(bak_path, "rb") as f:
                        data = f.read()
                    chunks = packer.unpack_chunks(data)
                    if len(chunks) < 7:
                        continue
                        
                    for chunk_idx in [2, 6]:
                        c_bytes = bytearray(chunks[chunk_idx])
                        if len(c_bytes) < 128:
                            continue
                        c_bytes[target_off] = 255 # Immune
                        chunks[chunk_idx] = bytes(c_bytes)
                        
                    repacked_data = packer.repack_chunks(chunks)
                    packer.safe_atomic_write(bin_path, repacked_data)
                    if item in self.monster_cache:
                        del self.monster_cache[item]
                    success += 1
                except Exception as e:
                    self.log(f"Failed setting immunity on {item}: {e}", "error")
                    
            self.log(f"Set immunity to {status_name} for {success} selected monsters.", "success")
            messagebox.showinfo("Success", f"Successfully immunised {success} monsters against {status_name}!")
            if self.current_monster:
                self.load_monster_file(self.current_monster["id"])
            dialog.destroy()
            
        btn_apply = tk.Button(dialog, text="Set Immunity", command=run_immune, bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief="flat", activebackground=self.accent_hover)
        btn_apply.pack(fill="x", padx=40, pady=15)
        self.bind_hover(btn_apply, is_primary=True)

    def on_batch_element_selected(self):
        sel = self.tree_monsters.selection()
        if not sel:
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("🔥 Set Element Affinities")
        dialog.geometry("380x300")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        lbl_header = tk.Label(dialog, text="🔥 Set Elemental Affinities", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 12, "bold"))
        lbl_header.pack(pady=(15, 5))
        
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="x", padx=40, pady=10)
        
        lbl_element = tk.Label(form_frame, text="Select Element:", bg=self.bg_color, fg=self.text_color)
        lbl_element.grid(row=0, column=0, sticky="w", pady=5)
        
        cmb_element = ttk.Combobox(form_frame, values=["Fire", "Ice", "Thunder", "Water", "Holy"], state="readonly", width=18)
        cmb_element.set("Fire")
        cmb_element.grid(row=0, column=1, sticky="e", pady=5)
        
        lbl_affinity = tk.Label(form_frame, text="Select Affinity:", bg=self.bg_color, fg=self.text_color)
        lbl_affinity.grid(row=1, column=0, sticky="w", pady=5)
        
        cmb_affinity = ttk.Combobox(form_frame, values=ELEMENT_STATES, state="readonly", width=18)
        cmb_affinity.set("Normal")
        cmb_affinity.grid(row=1, column=1, sticky="e", pady=5)
        
        form_frame.columnconfigure(0, weight=1)
        
        elem_bit_map = {
            "Fire": 0x01, "Ice": 0x02, "Thunder": 0x04, "Water": 0x08, "Holy": 0x10
        }
        
        def run_elements():
            elem_name = cmb_element.get()
            affinity_state = cmb_affinity.get()
            bit = elem_bit_map[elem_name]
            
            success = 0
            for item in sel:
                m = next((x for x in self.monsters_list if x["id"] == item), None)
                if not m:
                    continue
                bin_path = m["path"]
                bak_path = bin_path + ".bak"
                try:
                    if not os.path.exists(bak_path):
                        shutil.copy2(bin_path, bak_path)
                    with open(bak_path, "rb") as f:
                        data = f.read()
                    chunks = packer.unpack_chunks(data)
                    if len(chunks) < 7:
                        continue
                        
                    for chunk_idx in [2, 6]:
                        c_bytes = bytearray(chunks[chunk_idx])
                        if len(c_bytes) < 128:
                            continue
                        
                        # Clear existing bit from element maps (absorb 0x2B, immune 0x2C, resist 0x2D, weak 0x2E)
                        c_bytes[0x2B] &= ~bit
                        c_bytes[0x2C] &= ~bit
                        c_bytes[0x2D] &= ~bit
                        c_bytes[0x2E] &= ~bit
                        
                        # Apply new affinity state
                        if affinity_state == "Absorb":
                            c_bytes[0x2B] |= bit
                        elif affinity_state == "Immune":
                            c_bytes[0x2C] |= bit
                        elif affinity_state == "Resist":
                            c_bytes[0x2D] |= bit
                        elif affinity_state == "Weak":
                            c_bytes[0x2E] |= bit
                            
                        chunks[chunk_idx] = bytes(c_bytes)
                        
                    repacked_data = packer.repack_chunks(chunks)
                    packer.safe_atomic_write(bin_path, repacked_data)
                    if item in self.monster_cache:
                        del self.monster_cache[item]
                    success += 1
                except Exception as e:
                    self.log(f"Failed setting element on {item}: {e}", "error")
                    
            self.log(f"Set {elem_name} affinity to {affinity_state} for {success} selected monsters.", "success")
            messagebox.showinfo("Success", f"Successfully set {elem_name} element affinity to {affinity_state} for {success} monsters!")
            if self.current_monster:
                self.load_monster_file(self.current_monster["id"])
            dialog.destroy()
            
        btn_apply = tk.Button(dialog, text="Set Element", command=run_elements, bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief="flat", activebackground=self.accent_hover)
        btn_apply.pack(fill="x", padx=40, pady=15)
        self.bind_hover(btn_apply, is_primary=True)

    def on_restore_monster_backup(self):
        sel = self.tree_monsters.selection()
        if not sel:
            return
        m_id = sel[0]
        m = next((x for x in self.monsters_list if x["id"] == m_id), None)
        if not m:
            return
        filepath = m["path"]
        bak_path = filepath + ".bak"
        if not os.path.exists(bak_path):
            messagebox.showerror("Error", "No backup file (.bak) found for this monster.")
            return
            
        if not messagebox.askyesno("Confirm Restore", f"Are you sure you want to restore {m['name']} from its backup file?"):
            return
            
        try:
            shutil.copy2(bak_path, filepath)
            if m_id in self.monster_cache:
                del self.monster_cache[m_id]
            self.log(f"Restored {m_id}.bin from backup.", "success")
            messagebox.showinfo("Success", f"Successfully restored {m['name']} from backup!")
            self.load_monster_file(m_id)
        except Exception as e:
            self.log(f"Failed to restore backup: {e}", "error")
            messagebox.showerror("Error", f"Failed to restore backup:\n{str(e)}")

    def load_monster_file(self, m_id):
        self.current_monster = next((m for m in self.monsters_list if m["id"] == m_id), None)
        if not self.current_monster:
            return
        
        filepath = self.current_monster["path"]
        self.log(f"Loading monster {m_id}: {self.current_monster['name']}...")
        
        try:
            # Check if this monster is already in cache
            if m_id in self.monster_cache:
                self.log(f"Loading {m_id} from in-memory cache...")
                cache_entry = self.monster_cache[m_id]
                self.chunks = list(cache_entry["chunks"])
                self.stat_bytes_jp = bytearray(cache_entry["stat_bytes_jp"])
                self.stat_bytes_us = bytearray(cache_entry["stat_bytes_us"])
                self.loot_bytes = bytearray(cache_entry["loot_bytes"])
            else:
                with open(filepath, "rb") as f:
                    data = f.read()
                self.chunks = packer.unpack_chunks(data)
                if len(self.chunks) < 7:
                    raise ValueError("Bin file has fewer than 7 chunks. Is it a valid monster bin?")
                    
                self.stat_bytes_jp = bytearray(self.chunks[2])
                self.loot_bytes = bytearray(self.chunks[4])
                self.stat_bytes_us = bytearray(self.chunks[6])
                
                us_name = self.extract_monster_english_name(filepath)
                self.monster_cache[m_id] = {
                    "chunks": list(self.chunks),
                    "stat_bytes_jp": bytes(self.stat_bytes_jp),
                    "stat_bytes_us": bytes(self.stat_bytes_us),
                    "loot_bytes": bytes(self.loot_bytes),
                    "us_name": us_name,
                    "is_dirty": False
                }
                
            # Parse stats
            self.parse_monster_stats()
            # Parse loot
            self.parse_monster_loot()
            # Disassemble AI script
            self.disassemble_ai_script()
            self.update_rule_builder_actions()
            
            # Decompile multi-hook rules from Chunk 0 + Chunk 1
            self.load_ai_rules_from_chunks()
            
            # Snapshot GUI state
            self.loaded_state = self.get_current_gui_state()
            
            # Populate Encounter & Formation view
            self.populate_encounters_view()
            
            self.log(f"Loaded {m_id} successfully.", "success")
        except Exception as e:
            self.log(f"Failed to load monster: {e}", "error")
            messagebox.showerror("Error", f"Failed to load monster file:\n{str(e)}")

    def disassemble_ai_script(self):
        if not self.chunks or len(self.chunks) < 1:
            self.txt_atel.delete("1.0", tk.END)
            self.txt_atel.insert(tk.END, "No monster loaded.")
            return
            
        chunk0 = self.chunks[0]
        mode = self.cmb_atel_mode.get()
        
        try:
            decompiler = AtelDecompiler(chunk0)
            if mode == "Raw Assembly":
                text = decompiler.to_assembly()
            elif mode == "Plain English":
                text = decompiler.to_plain_english()
            else:  # Decompiled Pseudocode
                text = decompiler.to_pseudocode()
                
            self.txt_atel.delete("1.0", tk.END)
            self.txt_atel.insert(tk.END, text)
            self.apply_atel_syntax_highlighting()
            
            # Populate constants tree
            self.populate_constants_tree()
        except Exception as e:
            self.txt_atel.delete("1.0", tk.END)
            self.txt_atel.insert(tk.END, f"Error decompiling AI script:\n{str(e)}")

    def populate_constants_tree(self):
        self.tree_constants.delete(*self.tree_constants.get_children())
        if not self.chunks or len(self.chunks) < 1:
            return
            
        chunk0 = self.chunks[0]
        try:
            disasm = AtelDisassembler(chunk0)
            for w in disasm.workers:
                w_idx = w["index"]
                # refInts
                for idx, val in enumerate(w["ref_ints"]):
                    self.tree_constants.insert(
                        "", tk.END,
                        iid=f"w{w_idx}_int_{idx}",
                        values=(f"Worker {w_idx}", "int", idx, str(val))
                    )
                # refFloats
                for idx, val in enumerate(w["ref_floats"]):
                    self.tree_constants.insert(
                        "", tk.END,
                        iid=f"w{w_idx}_float_{idx}",
                        values=(f"Worker {w_idx}", "float", idx, f"{val:.4f}")
                    )
        except Exception as e:
            self.log(f"Error populating constants tree: {e}", "error")

    def on_constant_selected(self):
        sel = self.tree_constants.selection()
        if not sel:
            return
        item_id = sel[0]
        values = self.tree_constants.item(item_id, "values")
        if values:
            val = values[3]
            self.ent_const_val.delete(0, tk.END)
            self.ent_const_val.insert(0, val)

    def on_apply_const_value(self):
        sel = self.tree_constants.selection()
        if not sel:
            messagebox.showwarning("Warning", "No constant selected.")
            return
        item_id = sel[0]
        new_val = self.ent_const_val.get().strip()
        if not new_val:
            return
            
        values = list(self.tree_constants.item(item_id, "values"))
        # Validate based on type
        const_type = values[1]
        try:
            if const_type == "int":
                int(new_val)
            else:
                float(new_val)
        except ValueError:
            messagebox.showerror("Error", f"Invalid format for {const_type} value.")
            return
            
        values[3] = new_val
        self.tree_constants.item(item_id, values=values)

    def on_apply_constants_to_script(self):
        if not self.chunks or len(self.chunks) < 1:
            return
            
        chunk0 = bytearray(self.chunks[0])
        try:
            disasm = AtelDisassembler(chunk0)
            
            # Read all items from tree view
            for item_id in self.tree_constants.get_children():
                values = self.tree_constants.item(item_id, "values")
                worker_str, const_type, idx_str, val_str = values
                worker_idx = int(worker_str.split()[1])
                const_idx = int(idx_str)
                
                worker = next((w for w in disasm.workers if w["index"] == worker_idx), None)
                if not worker:
                    continue
                    
                if const_type == "int":
                    val = int(val_str)
                    offset = worker["ref_ints_offset"] + const_idx * 4
                    struct.pack_into("<i", chunk0, offset, val)
                else:
                    val = float(val_str)
                    offset = worker["ref_floats_offset"] + const_idx * 4
                    struct.pack_into("<f", chunk0, offset, val)
                    
            # Update the chunk in memory
            self.chunks[0] = bytes(chunk0)
            if self.current_monster:
                m_id = self.current_monster["id"]
                self.monster_cache[m_id]["chunks"][0] = bytes(chunk0)
                self.monster_cache[m_id]["is_dirty"] = True
                self.update_monster_tree_name(m_id, self.current_monster["name"], True)
                
            self.disassemble_ai_script()
            self.log("Applied constants to script successfully.", "success")
        except Exception as e:
            self.log(f"Failed to apply constants to script: {e}", "error")
            messagebox.showerror("Error", f"Failed to apply constants:\n{str(e)}")

    def build_rule_builder_tab(self, parent):
        self.ai_map_info = None
        self.current_hook_key = "turn"
        self.rules_by_hook = {k: [] for _, k, _, _ in AI_EVENT_HOOK_DEFS}
        self.modified_hooks = set()
        self.rule_data_map = {}
        self.extra_conditions_list = []

        # Row 1: AI Worker Info Badge & Preset Template Toolbar
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 6))

        self.lbl_ai_worker_info = tk.Label(
            top_frame,
            text="🤖 AI Worker: Not Loaded",
            bg=self.card_color,
            fg=self.accent_color,
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=3
        )
        self.lbl_ai_worker_info.pack(side="left", padx=(0, 8))

        ttk.Label(top_frame, text="Preset:").pack(side="left", padx=(4, 4))
        preset_names = list(AI_RULE_TEMPLATES.keys()) + [
            "Standard Attacker (Dingo)",
            "Flying Attacker (Condor)",
            "Spellcaster (Water Flan)",
            "Healer/Support (White Element)"
        ]
        self.cmb_ai_preset = ttk.Combobox(top_frame, values=preset_names, state="readonly", width=36)
        self.cmb_ai_preset.set(preset_names[0])
        self.cmb_ai_preset.pack(side="left", padx=4)

        btn_load_preset = tk.Button(
            top_frame, text="📥 Load Preset", command=self.on_apply_ai_template,
            bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=2
        )
        btn_load_preset.pack(side="left", padx=3)
        self.bind_hover(btn_load_preset, is_primary=True)

        btn_reload_ai = tk.Button(
            top_frame, text="🔄 Reload From Script", command=self.load_ai_rules_from_chunks,
            bg=self.card_color, fg=self.text_color, font=("Segoe UI", 9), relief="flat", padx=8, pady=2
        )
        btn_reload_ai.pack(side="left", padx=3)
        self.bind_hover(btn_reload_ai)

        self.btn_enable_hook = tk.Button(
            top_frame, text="➕ Enable Unmapped Hook", command=self.on_enable_current_hook_slot,
            bg=self.btn_color_secondary, fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=2
        )
        self.btn_enable_hook.pack(side="right", padx=3)
        self.bind_hover(self.btn_enable_hook)

        # Row 2: Event Hook Selector Bar
        hook_bar = tk.Frame(parent, bg=self.bg_color)
        hook_bar.pack(fill="x", pady=(0, 8))

        self.hook_buttons = {}
        short_labels = {
            "turn": "⚡ Active Turn",
            "react": "🛡 Counter / React",
            "damage": "💥 On Damage",
            "death": "💀 On Death",
            "pre_turn": "⏳ Pre-Turn",
            "start": "🎬 Battle Start",
            "targeted": "🎯 On Targeted",
            "post_turn": "📐 Post-Turn",
            "tick": "⏱ Status Tick",
        }
        for slot_idx, hook_key, full_label, desc in AI_EVENT_HOOK_DEFS:
            lbl_txt = short_labels.get(hook_key, full_label)
            b = tk.Button(
                hook_bar,
                text=lbl_txt,
                command=lambda hk=hook_key: self.on_select_ai_hook(hk),
                bg=self.card_color,
                fg=self.text_color,
                font=("Segoe UI", 8, "bold"),
                relief="flat",
                padx=7,
                pady=3
            )
            b.pack(side="left", padx=(0, 4))
            self.hook_buttons[hook_key] = b

        # Horizontal Split Panel
        paned = ttk.Panedwindow(parent, orient="horizontal")
        paned.pack(fill="both", expand=True)

        # Left Panel: Rules List + Live Pseudocode Preview + Compile Buttons
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=3)

        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill="both", expand=True)

        cols = ("phase", "condition", "action", "target", "chance", "state_flow")
        self.tree_rules = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        self.tree_rules.heading("phase", text="Phase Gate")
        self.tree_rules.heading("condition", text="Trigger Condition(s)")
        self.tree_rules.heading("action", text="Action / Ability")
        self.tree_rules.heading("target", text="Target")
        self.tree_rules.heading("chance", text="Chance")
        self.tree_rules.heading("state_flow", text="State & Flow")

        self.tree_rules.column("phase", width=85, anchor="center")
        self.tree_rules.column("condition", width=165, anchor="w")
        self.tree_rules.column("action", width=140, anchor="w")
        self.tree_rules.column("target", width=110, anchor="center")
        self.tree_rules.column("chance", width=55, anchor="center")
        self.tree_rules.column("state_flow", width=125, anchor="w")
        self.tree_rules.pack(fill="both", expand=True, side="left")

        scroll_rules_y = ttk.Scrollbar(tree_frame, command=self.tree_rules.yview)
        scroll_rules_y.pack(fill="y", side="right")
        self.tree_rules.config(yscrollcommand=scroll_rules_y.set)

        # Live Hook Pseudocode Preview
        preview_frame = ttk.LabelFrame(left_frame, text=" 📜 Live Hook Pseudocode Preview ", padding=4)
        preview_frame.pack(fill="x", pady=(6, 4))
        self.txt_rule_preview = tk.Text(
            preview_frame, bg="#0d0d0d", fg="#a7f3d0", font=("Consolas", 9),
            height=5, wrap="none", relief="flat"
        )
        self.txt_rule_preview.pack(fill="x", expand=True, side="left")
        prev_scroll = ttk.Scrollbar(preview_frame, command=self.txt_rule_preview.yview)
        prev_scroll.pack(fill="y", side="right")
        self.txt_rule_preview.config(yscrollcommand=prev_scroll.set)

        # Bottom Compile Buttons
        compile_bar = ttk.Frame(left_frame)
        compile_bar.pack(fill="x", pady=(4, 0))

        btn_compile = tk.Button(
            compile_bar,
            text="⚙ Compile Active Hook to AI Script",
            command=lambda: self.on_compile_rule_based_ai(compile_all_modified=False),
            bg=self.success_color, fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", pady=5
        )
        btn_compile.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.bind_hover_color(btn_compile, "#059669", self.success_color)

        btn_compile_all = tk.Button(
            compile_bar,
            text="⚡ Compile All Modified Hooks",
            command=lambda: self.on_compile_rule_based_ai(compile_all_modified=True),
            bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", pady=5
        )
        btn_compile_all.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self.bind_hover(btn_compile_all, is_primary=True)

        # Right Panel: Rule Editor Form
        right_frame = ttk.LabelFrame(paned, text=" 🔧 Rule Inspector & Logic Builder ", padding=8)
        paned.add(right_frame, weight=2)

        var_choices = ["Any"] + [f"var_{i:02X}" for i in range(32)]
        var_only_choices = [f"var_{i:02X}" for i in range(32)]

        # 1. Phase / State Gate
        ttk.Label(right_frame, text="Phase Gate:").grid(row=0, column=0, sticky="w", pady=3)
        phase_f = ttk.Frame(right_frame)
        phase_f.grid(row=0, column=1, sticky="ew", pady=3, padx=4)

        self.cmb_phase_var = ttk.Combobox(phase_f, values=var_choices, state="readonly", width=9)
        self.cmb_phase_var.set("Any")
        self.cmb_phase_var.pack(side="left")

        self.cmb_phase_op = ttk.Combobox(phase_f, values=["==", "!=", "<", "<=", ">", ">="], state="readonly", width=4)
        self.cmb_phase_op.set("==")
        self.cmb_phase_op.pack(side="left", padx=3)

        self.var_phase_val = tk.StringVar(value="0")
        tk.Spinbox(
            phase_f, from_=-999, to=9999, textvariable=self.var_phase_val, width=6,
            bg=self.card_color, fg=self.text_color, insertbackground=self.text_color
        ).pack(side="left")

        # 2. Primary Condition
        ttk.Label(right_frame, text="Condition:").grid(row=1, column=0, sticky="w", pady=3)
        self.cmb_rule_cond = ttk.Combobox(right_frame, values=CONDITION_PRESETS, width=26)
        self.cmb_rule_cond.set("Always")
        self.cmb_rule_cond.grid(row=1, column=1, sticky="ew", pady=3, padx=4)

        # 3. Extra Composite Conditions (AND / OR)
        ttk.Label(right_frame, text="Composite:").grid(row=2, column=0, sticky="w", pady=3)
        comp_f = ttk.Frame(right_frame)
        comp_f.grid(row=2, column=1, sticky="ew", pady=3, padx=4)

        self.cmb_logic_op = ttk.Combobox(comp_f, values=["AND", "OR"], state="readonly", width=5)
        self.cmb_logic_op.set("AND")
        self.cmb_logic_op.pack(side="left")

        self.var_extra_conds = tk.StringVar(value="")
        self.ent_extra_conds = ttk.Entry(comp_f, textvariable=self.var_extra_conds, width=14)
        self.ent_extra_conds.pack(side="left", fill="x", expand=True, padx=3)

        btn_add_extra = tk.Button(
            comp_f, text="+Cond", command=self.on_append_extra_condition,
            bg=self.card_color, fg=self.text_color, font=("Segoe UI", 8), relief="flat", padx=4
        )
        btn_add_extra.pack(side="left", padx=1)
        self.bind_hover(btn_add_extra)

        btn_clr_extra = tk.Button(
            comp_f, text="Clr", command=lambda: self.var_extra_conds.set(""),
            bg=self.card_color, fg=self.text_dim, font=("Segoe UI", 8), relief="flat", padx=4
        )
        btn_clr_extra.pack(side="left", padx=1)
        self.bind_hover(btn_clr_extra)

        # 4. Action Search & Selection
        ttk.Label(right_frame, text="Find Action:").grid(row=3, column=0, sticky="w", pady=3)
        act_search_f = ttk.Frame(right_frame)
        act_search_f.grid(row=3, column=1, sticky="ew", pady=3, padx=4)

        self.var_action_filter = tk.StringVar(value="")
        ent_act_filter = ttk.Entry(act_search_f, textvariable=self.var_action_filter, width=16)
        ent_act_filter.pack(side="left", fill="x", expand=True)
        ent_act_filter.bind("<KeyRelease>", self.on_filter_rule_actions)

        self.var_is_counter_op = tk.BooleanVar(value=False)
        tk.Checkbutton(
            act_search_f, text="Counter (0x705A)", variable=self.var_is_counter_op,
            bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color,
            activebackground=self.bg_color, activeforeground=self.text_color, font=("Segoe UI", 8)
        ).pack(side="right", padx=(4, 0))

        ttk.Label(right_frame, text="Action:").grid(row=4, column=0, sticky="w", pady=3)
        self.cmb_rule_action = ttk.Combobox(right_frame, width=26)
        self.cmb_rule_action.grid(row=4, column=1, sticky="ew", pady=3, padx=4)

        # 5. Target Selection
        ttk.Label(right_frame, text="Target:").grid(row=5, column=0, sticky="w", pady=3)
        self.cmb_rule_target = ttk.Combobox(right_frame, values=TARGET_PRESETS, state="readonly", width=26)
        self.cmb_rule_target.set("Target")
        self.cmb_rule_target.grid(row=5, column=1, sticky="ew", pady=3, padx=4)

        # 6. Chance (%)
        ttk.Label(right_frame, text="Chance (%):").grid(row=6, column=0, sticky="w", pady=3)
        self.var_rule_chance = tk.StringVar(value="100")
        tk.Spinbox(
            right_frame, from_=1, to=100, textvariable=self.var_rule_chance, width=24,
            bg=self.card_color, fg=self.text_color, insertbackground=self.text_color
        ).grid(row=6, column=1, sticky="ew", pady=3, padx=4)

        # 7. State / Variable Update
        ttk.Label(right_frame, text="State Update:").grid(row=7, column=0, sticky="w", pady=3)
        var_f = ttk.Frame(right_frame)
        var_f.grid(row=7, column=1, sticky="ew", pady=3, padx=4)

        self.cmb_var_op = ttk.Combobox(var_f, values=["None", "Set", "Add", "Reset"], state="readonly", width=6)
        self.cmb_var_op.set("None")
        self.cmb_var_op.pack(side="left")

        self.cmb_var_idx = ttk.Combobox(var_f, values=var_only_choices, state="readonly", width=8)
        self.cmb_var_idx.set("var_00")
        self.cmb_var_idx.pack(side="left", padx=3)

        self.var_mut_val = tk.StringVar(value="1")
        tk.Spinbox(
            var_f, from_=-999, to=9999, textvariable=self.var_mut_val, width=6,
            bg=self.card_color, fg=self.text_color, insertbackground=self.text_color
        ).pack(side="left")

        # 8. Turn Control Flow
        ttk.Label(right_frame, text="Turn Flow:").grid(row=8, column=0, sticky="w", pady=3)
        self.cmb_rule_flow = ttk.Combobox(
            right_frame,
            values=["Return (End Turn)", "Continue (Multi-Action / Combo)"],
            state="readonly", width=26
        )
        self.cmb_rule_flow.set("Return (End Turn)")
        self.cmb_rule_flow.grid(row=8, column=1, sticky="ew", pady=3, padx=4)

        right_frame.columnconfigure(1, weight=1)

        # Command Buttons inside Right Frame
        btn_cmd_frame = ttk.Frame(right_frame)
        btn_cmd_frame.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(10, 2))

        row_crud1 = ttk.Frame(btn_cmd_frame)
        row_crud1.pack(fill="x", pady=2)

        btn_update = tk.Button(
            row_crud1, text="💾 Update Rule", command=self.on_update_rule_item,
            bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", pady=3
        )
        btn_update.pack(side="left", fill="x", expand=True, padx=(0, 2))
        self.bind_hover(btn_update, is_primary=True)

        btn_add = tk.Button(
            row_crud1, text="➕ Add Rule", command=self.on_add_rule_item,
            bg=self.btn_color_secondary, fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", pady=3
        )
        btn_add.pack(side="left", fill="x", expand=True, padx=(2, 0))
        self.bind_hover(btn_add)

        row_crud2 = ttk.Frame(btn_cmd_frame)
        row_crud2.pack(fill="x", pady=2)

        btn_dup = tk.Button(
            row_crud2, text="📋 Duplicate", command=self.on_duplicate_rule_item,
            bg=self.card_color, fg=self.text_color, font=("Segoe UI", 9), relief="flat", pady=3
        )
        btn_dup.pack(side="left", fill="x", expand=True, padx=(0, 2))
        self.bind_hover(btn_dup)

        btn_delete = tk.Button(
            row_crud2, text="🗑 Delete Rule", command=self.on_delete_rule_item,
            bg=self.error_color, fg="#ffffff", font=("Segoe UI", 9), relief="flat", pady=3
        )
        btn_delete.pack(side="left", fill="x", expand=True, padx=(2, 0))
        self.bind_hover_color(btn_delete, "#dc2626", self.error_color)

        # Reorder Buttons
        reorder_frame = ttk.Frame(btn_cmd_frame)
        reorder_frame.pack(fill="x", pady=(6, 0))

        btn_up = tk.Button(
            reorder_frame, text="▲ Move Up", command=self.on_move_rule_up,
            bg=self.card_color, fg=self.text_color, relief="flat", width=11, pady=2
        )
        btn_up.pack(side="left", expand=True, fill="x", padx=(0, 2))
        self.bind_hover(btn_up)

        btn_down = tk.Button(
            reorder_frame, text="▼ Move Down", command=self.on_move_rule_down,
            bg=self.card_color, fg=self.text_color, relief="flat", width=11, pady=2
        )
        btn_down.pack(side="left", expand=True, fill="x", padx=(2, 0))
        self.bind_hover(btn_down)

        self.tree_rules.bind("<<TreeviewSelect>>", lambda e: self.on_rule_item_selected())

    def update_rule_builder_actions(self):
        if not hasattr(self, "cmb_rule_action"):
            return
        vals = [f"{name} ({hex(cmd_id)})" for cmd_id, name in self.commands_list]
        self._all_action_choices = vals
        self.cmb_rule_action["values"] = vals
        if vals and not self.cmb_rule_action.get():
            self.cmb_rule_action.set(vals[0])

    def on_filter_rule_actions(self, event=None):
        if not hasattr(self, "_all_action_choices"):
            self.update_rule_builder_actions()
        query = self.var_action_filter.get().strip().lower()
        if not query:
            filtered = self._all_action_choices
        else:
            filtered = [v for v in self._all_action_choices if query in v.lower()]
        self.cmb_rule_action["values"] = filtered if filtered else self._all_action_choices
        if filtered:
            self.cmb_rule_action.set(filtered[0])

    def on_append_extra_condition(self):
        cond = self.cmb_rule_cond.get().strip()
        if not cond or cond == "Always":
            return
        curr = self.var_extra_conds.get().strip()
        parts = [p.strip() for p in curr.split(";") if p.strip()] if curr else []
        if cond not in parts:
            parts.append(cond)
        self.var_extra_conds.set("; ".join(parts))

    def _get_hook_func_map(self, ai_map=None):
        m = ai_map if ai_map is not None else self.ai_map_info
        if not m:
            return {}
        hooks = m.get("hooks", {})
        if isinstance(hooks, dict):
            return {k: (v if v is not None else 0xFFFF) for k, v in hooks.items()}
        out = {}
        for h in hooks:
            fk = h.get("func_idx")
            out[h["key"]] = fk if fk is not None else 0xFFFF
        return out

    def load_ai_rules_from_chunks(self):
        if not self.chunks or len(self.chunks) < 2:
            return
        try:
            self.ai_map_info = parse_chunk1_ai_map(self.chunks[1], self.chunks[0])
            self.rules_by_hook = decompile_atel_to_rules(self.chunks[0], self.chunks[1], return_all_hooks=True)
            self.modified_hooks = set()

            # Keep current_hook_key if valid, or default to turn
            if self.current_hook_key not in self.rules_by_hook:
                self.current_hook_key = "turn"

            self.refresh_hook_selector_bar()
            self.populate_rules_tree_for_current_hook()

            total_rules = sum(len(v) for v in self.rules_by_hook.values())
            active_hooks = [k for k, v in self.rules_by_hook.items() if v]
            self.log(
                f"Decompiled {total_rules} AI rules across {len(active_hooks)} event hooks "
                f"(AI Worker w{self.ai_map_info['ai_worker_idx']}, {self.ai_map_info['var_count']} local vars).",
                "info"
            )
        except Exception as e:
            self.log(f"Error decompiling multi-hook AI rules: {e}", "error")

    def refresh_hook_selector_bar(self):
        if not hasattr(self, "hook_buttons"):
            return
        short_labels = {
            "turn": "⚡ Turn",
            "react": "🛡 Counter",
            "damage": "💥 Damage",
            "death": "💀 Death",
            "pre_turn": "⏳ Pre-Turn",
            "start": "🎬 Init",
            "targeted": "🎯 Targeted",
            "post_turn": "📐 Post-Turn",
            "tick": "⏱ Tick",
        }
        hooks_map = self._get_hook_func_map()
        ai_w = self.ai_map_info.get("ai_worker_idx", 0) if self.ai_map_info else 0
        var_cnt = self.ai_map_info.get("var_count", 0) if self.ai_map_info else 0

        for hook_key, btn in self.hook_buttons.items():
            cnt = len(self.rules_by_hook.get(hook_key, []))
            func_idx = hooks_map.get(hook_key, 0xFFFF)
            base_lbl = short_labels.get(hook_key, hook_key)
            badge = f" ({cnt})" if cnt > 0 else ""
            if hook_key in getattr(self, "modified_hooks", set()):
                badge += "*"
            btn.config(text=f"{base_lbl}{badge}")

            if hook_key == self.current_hook_key:
                btn.config(bg=self.accent_color, fg="#ffffff")
            elif func_idx != 0xFFFF and cnt > 0:
                btn.config(bg=self.card_color, fg=self.success_color)
            elif func_idx != 0xFFFF:
                btn.config(bg=self.card_color, fg=self.text_color)
            else:
                btn.config(bg=self.bg_color, fg=self.text_dim)

        cur_func = hooks_map.get(self.current_hook_key, 0xFFFF)
        func_str = f"w{ai_w}_f{cur_func}" if cur_func != 0xFFFF else "Unmapped (0xFFFF)"
        self.lbl_ai_worker_info.config(
            text=f"🤖 Worker w{ai_w} (Role 2) | {var_cnt} Vars | Hook: {self.current_hook_key} -> {func_str}"
        )
        if hasattr(self, "btn_enable_hook"):
            if cur_func == 0xFFFF:
                self.btn_enable_hook.config(state="normal", bg=self.accent_color, text="➕ Enable Unmapped Hook")
            else:
                self.btn_enable_hook.config(state="normal", bg=self.btn_color_secondary, text=f"✔ Hook Mapped ({func_str})")

    def on_select_ai_hook(self, hook_key):
        # Save current tree order into rules_by_hook before switching
        self._sync_tree_to_current_hook_rules()
        self.current_hook_key = hook_key
        if hasattr(self, "var_is_counter_op"):
            self.var_is_counter_op.set(hook_key == "react")
        self.refresh_hook_selector_bar()
        self.populate_rules_tree_for_current_hook()
        if hasattr(self, "cvs_flowchart"):
            try:
                self.draw_flowchart()
            except Exception:
                pass

    def on_enable_current_hook_slot(self):
        if not self.chunks or len(self.chunks) < 2:
            return
        slot_idx = 0
        for s_idx, hk, _, _ in AI_EVENT_HOOK_DEFS:
            if hk == self.current_hook_key:
                slot_idx = s_idx
                break
        try:
            new_c0, new_c1, ai_w, f_idx = enable_chunk1_hook_slot(self.chunks[0], self.chunks[1], slot_idx)
            self.chunks[0] = new_c0
            self.chunks[1] = new_c1
            if self.current_monster:
                m_id = self.current_monster["id"]
                self.monster_cache[m_id]["chunks"][0] = new_c0
                self.monster_cache[m_id]["chunks"][1] = new_c1
                self.monster_cache[m_id]["is_dirty"] = True
                self.update_monster_tree_name(m_id, self.current_monster["name"], True)
            self.ai_map_info = parse_chunk1_ai_map(self.chunks[1], self.chunks[0])
            self.refresh_hook_selector_bar()
            self.disassemble_ai_script()
            self.log(f"Enabled Hook '{self.current_hook_key}' (Slot {slot_idx}) -> w{ai_w}_f{f_idx}.", "success")
        except Exception as e:
            self.log(f"Failed to enable hook slot: {e}", "error")
            messagebox.showerror("Error", f"Failed to enable hook slot:\n{e}")

    def _format_rule_row_values(self, rule):
        # 1. Phase gate display
        p_var = rule.get("phase_var", "Any")
        if p_var and p_var != "Any":
            phase_str = f"{p_var} {rule.get('phase_op', '==')} {rule.get('phase_val', 0)}"
        else:
            phase_str = "Any"

        # 2. Condition display
        cond = rule.get("condition", "Always")
        extra = [c for c in rule.get("extra_conditions", []) if c and c != "Always"]
        logic_op = rule.get("logic_op", "AND")
        if extra:
            cond_str = f"{cond} {logic_op} " + f" {logic_op} ".join(extra)
        else:
            cond_str = cond

        # 3. Action display
        action_id = rule.get("action_id", 4)
        resolved_act = self.resolve_command_name(action_id)
        if rule.get("is_counter_op", False):
            resolved_act = f"[Counter] {resolved_act}"

        # 4. Target & Chance
        target_str = rule.get("target", "Target")
        chance_str = f"{rule.get('chance', 100)}%"

        # 5. State & Flow
        v_op = rule.get("var_op", "None")
        v_idx = rule.get("var_idx", "var_00")
        v_val = rule.get("var_val", 1)
        flow = rule.get("flow", "Return")
        state_parts = []
        if v_op == "Set":
            state_parts.append(f"{v_idx}={v_val}")
        elif v_op == "Add":
            state_parts.append(f"{v_idx}+={v_val}")
        elif v_op == "Reset":
            state_parts.append(f"{v_idx}=0")
        state_parts.append("Continue ⏩" if str(flow).startswith("Continue") else "Return")
        state_flow_str = " | ".join(state_parts)

        return (phase_str, cond_str, resolved_act, target_str, chance_str, state_flow_str)

    def populate_rules_tree_for_current_hook(self):
        self.tree_rules.delete(*self.tree_rules.get_children())
        self.rule_data_map.clear()
        rules = self.rules_by_hook.get(self.current_hook_key, [])
        for idx, rule in enumerate(rules):
            r_copy = dict(rule)
            r_copy.setdefault("hook", self.current_hook_key)
            r_copy.setdefault("phase_var", "Any")
            r_copy.setdefault("phase_op", "==")
            r_copy.setdefault("phase_val", 0)
            r_copy.setdefault("condition", "Always")
            r_copy.setdefault("extra_conditions", [])
            r_copy.setdefault("logic_op", "AND")
            r_copy.setdefault("action_id", 4)
            r_copy.setdefault("target", "Target")
            r_copy.setdefault("chance", 100)
            r_copy.setdefault("var_op", "None")
            r_copy.setdefault("var_idx", "var_00")
            r_copy.setdefault("var_val", 1)
            r_copy.setdefault("flow", "Return")
            r_copy.setdefault("is_counter_op", self.current_hook_key == "counter")

            iid = f"rule_{idx}"
            self.rule_data_map[iid] = r_copy
            self.tree_rules.insert("", tk.END, iid=iid, values=self._format_rule_row_values(r_copy))

        self.update_live_rule_preview()

    def _sync_tree_to_current_hook_rules(self):
        if not hasattr(self, "tree_rules"):
            return
        ordered = []
        for iid in self.tree_rules.get_children():
            if iid in self.rule_data_map:
                ordered.append(dict(self.rule_data_map[iid]))
        self.rules_by_hook[self.current_hook_key] = ordered

    def _build_rule_dict_from_form(self):
        p_var = self.cmb_phase_var.get().strip() or "Any"
        p_op = self.cmb_phase_op.get().strip() or "=="
        try:
            p_val = int(self.var_phase_val.get().strip())
        except ValueError:
            p_val = 0

        cond = self.cmb_rule_cond.get().strip() or "Always"
        extra_raw = self.var_extra_conds.get().strip()
        extra_list = [p.strip() for p in extra_raw.split(";") if p.strip()] if extra_raw else []
        logic_op = self.cmb_logic_op.get().strip() or "AND"

        act_name = self.cmb_rule_action.get().strip()
        clean_act = act_name.replace("[Counter] ", "").strip()
        action_id = 4
        start_hex = clean_act.rfind("(0x")
        if start_hex != -1:
            end_hex = clean_act.find(")", start_hex)
            if end_hex != -1:
                try:
                    action_id = int(clean_act[start_hex + 3:end_hex], 16)
                except ValueError:
                    action_id = 4
        elif clean_act.lower().startswith("0x"):
            try:
                action_id = int(clean_act, 16)
            except ValueError:
                action_id = 4
        else:
            for cmd_id, name in self.commands_list:
                if name.lower() == clean_act.lower() or clean_act.lower().startswith(name.lower()):
                    action_id = cmd_id
                    break

        target = self.cmb_rule_target.get().strip() or "Target"
        try:
            chance = max(1, min(100, int(self.var_rule_chance.get().replace("%", "").strip())))
        except ValueError:
            chance = 100

        var_op = self.cmb_var_op.get().strip() or "None"
        var_idx = self.cmb_var_idx.get().strip() or "var_00"
        try:
            var_val = int(self.var_mut_val.get().strip())
        except ValueError:
            var_val = 1

        flow_raw = self.cmb_rule_flow.get().strip()
        flow = "Continue" if flow_raw.startswith("Continue") else "Return"
        is_counter_op = bool(self.var_is_counter_op.get())

        hooks_map = self._get_hook_func_map()
        func_idx = hooks_map.get(self.current_hook_key, 2)

        return {
            "hook": self.current_hook_key,
            "func_idx": func_idx,
            "phase_var": p_var,
            "phase_op": p_op,
            "phase_val": p_val,
            "condition": cond,
            "extra_conditions": extra_list,
            "logic_op": logic_op,
            "action_id": action_id,
            "target": target,
            "chance": chance,
            "var_op": var_op,
            "var_idx": var_idx,
            "var_name": var_idx,
            "var_val": var_val,
            "flow": flow,
            "is_counter_op": is_counter_op,
            "is_counter_exec": is_counter_op,
        }

    def update_live_rule_preview(self):
        if not hasattr(self, "txt_rule_preview"):
            return
        self._sync_tree_to_current_hook_rules()
        rules = self.rules_by_hook.get(self.current_hook_key, [])
        self.txt_rule_preview.delete("1.0", tk.END)
        if not rules:
            self.txt_rule_preview.insert(tk.END, f"// No rules in hook '{self.current_hook_key}' (returns immediately).\nreturn")
            return

        lines = [f"// Hook: {self.current_hook_key} ({len(rules)} rules)"]
        for idx, r in enumerate(rules):
            conds = []
            if r.get("phase_var", "Any") not in ("Any", "", None):
                conds.append(f"{r['phase_var']} {r.get('phase_op', '==')} {r.get('phase_val', 0)}")
            c_main = r.get("condition", "Always")
            if c_main != "Always":
                extras = [x for x in r.get("extra_conditions", []) if x and x != "Always"]
                if extras:
                    lop = r.get("logic_op", "AND").lower()
                    conds.append("(" + f" {lop} ".join([c_main] + extras) + ")")
                else:
                    conds.append(c_main)
            if r.get("chance", 100) < 100:
                conds.append(f"Random(100) < {r['chance']}%")

            act_str = self.resolve_command_name(r.get("action_id", 4))
            fn_name = "ExecuteCounterAction" if r.get("is_counter_op") or r.get("is_counter_exec") else "ExecuteAction"
            tgt_str = r.get("target", "Target")

            body_Parts = [f"{fn_name}({tgt_str}, {act_str})"]
            v_op = r.get("var_op", "None")
            v_idx = r.get("var_idx") or r.get("var_name") or "var_00"
            v_val = r.get("var_val", 1)
            if v_op == "Set":
                body_Parts.append(f"{v_idx} = {v_val}")
            elif v_op == "Add":
                body_Parts.append(f"{v_idx} += {v_val}")
            elif v_op == "Reset":
                body_Parts.append(f"{v_idx} = 0")

            if str(r.get("flow", "Return")).startswith("Return"):
                body_Parts.append("return")

            if conds:
                lines.append(f"if {' and '.join(conds)}:")
                for bp in body_Parts:
                    lines.append(f"    {bp}")
            else:
                for bp in body_Parts:
                    lines.append(bp)
        self.txt_rule_preview.insert(tk.END, "\n".join(lines))

    def on_apply_ai_template(self):
        preset = self.cmb_ai_preset.get()
        if preset in AI_RULE_TEMPLATES:
            tmpl = AI_RULE_TEMPLATES[preset]
            if isinstance(tmpl, dict):
                for hk, h_rules in tmpl.items():
                    self.rules_by_hook[hk] = [dict(r) for r in h_rules]
                    if h_rules:
                        self.modified_hooks.add(hk)
            elif isinstance(tmpl, list):
                target_hk = "react" if "Counter" in preset else self.current_hook_key
                self.rules_by_hook[target_hk] = [dict(r) for r in tmpl]
                self.modified_hooks.add(target_hk)
                self.current_hook_key = target_hk
        else:
            # Classic presets
            classic_rules = []
            if preset in ("Standard Attacker (Dingo)", "Flying Attacker (Condor)"):
                classic_rules = [{"condition": "Always", "action_id": 16384, "target": "Random Alive Party Member", "chance": 100}]
            elif preset == "Spellcaster (Water Flan)":
                classic_rules = [{"condition": "Always", "action_id": 0x3057, "target": "Random Alive Party Member", "chance": 100}]
            elif preset == "Healer/Support (White Element)":
                classic_rules = [
                    {"condition": "Self HP < 50%", "action_id": 0x304E, "target": "Self", "chance": 100},
                    {"condition": "Always", "action_id": 0x3054, "target": "Random Alive Party Member", "chance": 100},
                ]
            self.rules_by_hook[self.current_hook_key] = classic_rules
            self.modified_hooks.add(self.current_hook_key)

        self.refresh_hook_selector_bar()
        self.populate_rules_tree_for_current_hook()
        self.log(f"Loaded AI template '{preset}' into Visual Rule Builder.", "info")

    def on_rule_item_selected(self):
        sel = self.tree_rules.selection()
        if not sel:
            return
        item_id = sel[0]
        rule = self.rule_data_map.get(item_id)
        if not rule:
            return

        p_var = rule.get("phase_var") or "Any"
        self.cmb_phase_var.set(p_var)
        self.cmb_phase_op.set(rule.get("phase_op", "=="))
        self.var_phase_val.set(str(rule.get("phase_val", 0)))

        self.cmb_rule_cond.set(rule.get("condition", "Always"))
        self.cmb_logic_op.set(rule.get("logic_op", "AND"))
        self.var_extra_conds.set("; ".join(rule.get("extra_conditions", [])))

        resolved_act = self.resolve_command_name(rule.get("action_id", 4))
        self.cmb_rule_action.set(resolved_act)
        self.var_is_counter_op.set(bool(rule.get("is_counter_op", rule.get("is_counter_exec", False))))

        self.cmb_rule_target.set(rule.get("target", "Random Alive Party Member"))
        self.var_rule_chance.set(str(rule.get("chance", 100)))

        self.cmb_var_op.set(rule.get("var_op", "None"))
        self.cmb_var_idx.set(rule.get("var_idx") or rule.get("var_name") or "var_00")
        self.var_mut_val.set(str(rule.get("var_val", 1)))

        flow = rule.get("flow", "Return")
        self.cmb_rule_flow.set(
            "Continue (Multi-Action / Combo)" if str(flow).startswith("Continue") else "Return (End Turn)"
        )

    def on_update_rule_item(self):
        sel = self.tree_rules.selection()
        if not sel:
            messagebox.showwarning("Warning", "No rule selected to update.")
            return
        item_id = sel[0]
        new_rule = self._build_rule_dict_from_form()
        self.rule_data_map[item_id] = new_rule
        self.tree_rules.item(item_id, values=self._format_rule_row_values(new_rule))
        self.modified_hooks.add(self.current_hook_key)
        self.refresh_hook_selector_bar()
        self.update_live_rule_preview()

    def on_add_rule_item(self):
        import uuid
        new_rule = self._build_rule_dict_from_form()
        item_id = f"rule_{uuid.uuid4().hex[:8]}"
        self.rule_data_map[item_id] = new_rule
        self.tree_rules.insert("", tk.END, iid=item_id, values=self._format_rule_row_values(new_rule))
        self.tree_rules.selection_set(item_id)
        self.modified_hooks.add(self.current_hook_key)
        self.refresh_hook_selector_bar()
        self.update_live_rule_preview()

    def on_duplicate_rule_item(self):
        sel = self.tree_rules.selection()
        if not sel:
            messagebox.showwarning("Warning", "No rule selected to duplicate.")
            return
        import uuid
        src_id = sel[0]
        src_rule = dict(self.rule_data_map.get(src_id, self._build_rule_dict_from_form()))
        src_rule["extra_conditions"] = list(src_rule.get("extra_conditions", []))
        item_id = f"rule_{uuid.uuid4().hex[:8]}"
        self.rule_data_map[item_id] = src_rule
        idx = self.tree_rules.index(src_id)
        self.tree_rules.insert("", idx + 1, iid=item_id, values=self._format_rule_row_values(src_rule))
        self.tree_rules.selection_set(item_id)
        self.modified_hooks.add(self.current_hook_key)
        self.refresh_hook_selector_bar()
        self.update_live_rule_preview()

    def on_delete_rule_item(self):
        sel = self.tree_rules.selection()
        if not sel:
            messagebox.showwarning("Warning", "No rule selected to delete.")
            return
        item_id = sel[0]
        self.tree_rules.delete(item_id)
        self.rule_data_map.pop(item_id, None)
        self.modified_hooks.add(self.current_hook_key)
        self.refresh_hook_selector_bar()
        self.update_live_rule_preview()

    def on_move_rule_up(self):
        sel = self.tree_rules.selection()
        if not sel:
            return
        node = sel[0]
        idx = self.tree_rules.index(node)
        if idx > 0:
            self.tree_rules.move(node, "", idx - 1)
            self.modified_hooks.add(self.current_hook_key)
            self.update_live_rule_preview()

    def on_move_rule_down(self):
        sel = self.tree_rules.selection()
        if not sel:
            return
        node = sel[0]
        idx = self.tree_rules.index(node)
        self.tree_rules.move(node, "", idx + 1)
        self.modified_hooks.add(self.current_hook_key)
        self.update_live_rule_preview()

    def on_compile_rule_based_ai(self, compile_all_modified=False):
        if not self.current_monster:
            messagebox.showwarning("Warning", "No monster selected.")
            return

        self._sync_tree_to_current_hook_rules()

        if compile_all_modified:
            target_hooks = list(self.modified_hooks | {self.current_hook_key})
        else:
            target_hooks = [self.current_hook_key]

        # Filter to hooks that actually have rules (or the active hook)
        hooks_to_compile = [hk for hk in target_hooks if self.rules_by_hook.get(hk)]
        if not hooks_to_compile:
            messagebox.showwarning("Warning", f"No rules to compile in '{self.current_hook_key}'.")
            return

        try:
            m_id = self.current_monster["id"]
            cur_chunk0 = bytes(self.chunks[0])
            cur_chunk1 = bytes(self.chunks[1]) if len(self.chunks) > 1 else b""

            compiled_summary = []
            for hk in hooks_to_compile:
                rules = self.rules_by_hook.get(hk, [])
                if not rules:
                    continue

                ai_map = parse_chunk1_ai_map(cur_chunk1, cur_chunk0)
                ai_w = ai_map["ai_worker_idx"]
                hooks_map = self._get_hook_func_map(ai_map)
                func_idx = hooks_map.get(hk, 0xFFFF)

                # Auto-enable unmapped hook in Chunk 1 if needed
                if func_idx == 0xFFFF:
                    slot_idx = 0
                    for s_idx, d_hk, _, _ in AI_EVENT_HOOK_DEFS:
                        if d_hk == hk:
                            slot_idx = s_idx
                            break
                    cur_chunk0, cur_chunk1, ai_w, func_idx = enable_chunk1_hook_slot(cur_chunk0, cur_chunk1, slot_idx)
                    self.log(f"Auto-enabled Chunk 1 Hook '{hk}' (Slot {slot_idx}) -> w{ai_w}_f{func_idx}.", "info")

                cur_chunk0 = inject_rules(
                    cur_chunk0,
                    rules,
                    worker_idx=ai_w,
                    func_idx=func_idx,
                    chunk1_bytes=cur_chunk1,
                    hook_key=hk
                )
                compiled_summary.append(f"{hk} (w{ai_w}_f{func_idx}: {len(rules)} rules)")
                self.modified_hooks.discard(hk)

            self.chunks[0] = cur_chunk0
            self.chunks[1] = cur_chunk1
            self.monster_cache[m_id]["chunks"][0] = cur_chunk0
            self.monster_cache[m_id]["chunks"][1] = cur_chunk1
            self.monster_cache[m_id]["is_dirty"] = True

            self.ai_map_info = parse_chunk1_ai_map(self.chunks[1], self.chunks[0])
            self.refresh_hook_selector_bar()
            self.update_monster_tree_name(m_id, self.current_monster["name"], True)
            self.disassemble_ai_script()

            summary_str = ", ".join(compiled_summary)
            self.log(f"Compiled AI hooks for {self.current_monster['name']}: {summary_str}", "success")
            messagebox.showinfo(
                "Success",
                f"Compiled and injected AI bytecode successfully!\n\nUpdated Hooks:\n• " + "\n• ".join(compiled_summary)
            )
        except Exception as e:
            self.log(f"Failed to compile AI script: {e}", "error")
            messagebox.showerror("Error", f"Compilation failed:\n{str(e)}")

    def parse_monster_stats(self):
        b = self.stat_bytes_jp
        # Decode localized strings
        def read_str(chunk_bytes, offset_idx, key_idx, charset):
            if len(chunk_bytes) < 128:
                return ""
            off = struct.unpack("<H", chunk_bytes[offset_idx : offset_idx+2])[0]
            return self.codec.decode_ffx_bytes(chunk_bytes[128:], off, charset)
            
        self.jp_name = read_str(self.stat_bytes_jp, 0x00, 0x02, "jp")
        self.jp_sensor = read_str(self.stat_bytes_jp, 0x04, 0x06, "jp")
        self.jp_scan = read_str(self.stat_bytes_jp, 0x0C, 0x0E, "jp")
        
        self.us_name = read_str(self.stat_bytes_us, 0x00, 0x02, "us")
        self.us_sensor = read_str(self.stat_bytes_us, 0x04, 0x06, "us")
        self.us_scan = read_str(self.stat_bytes_us, 0x0C, 0x0E, "us")
        
        # Populate Name fields
        self.ent_jp_name.delete(0, tk.END)
        self.ent_jp_name.insert(0, self.jp_name)
        self.ent_us_name.delete(0, tk.END)
        self.ent_us_name.insert(0, self.us_name)
        
        # Populate Sensor/Scan
        self.txt_jp_sensor.delete("1.0", tk.END)
        self.txt_jp_sensor.insert(tk.END, self.jp_sensor)
        self.txt_us_sensor.delete("1.0", tk.END)
        self.txt_us_sensor.insert(tk.END, self.us_sensor)
        
        self.txt_jp_scan.delete("1.0", tk.END)
        self.txt_jp_scan.insert(tk.END, self.jp_scan)
        self.txt_us_scan.delete("1.0", tk.END)
        self.txt_us_scan.insert(tk.END, self.us_scan)
        
        # Main attributes
        self.var_hp.set(struct.unpack("<I", b[0x14:0x18])[0])
        self.var_mp.set(struct.unpack("<I", b[0x18:0x1C])[0])
        self.var_overkill.set(struct.unpack("<I", b[0x1C:0x20])[0])
        
        self.var_str.set(b[0x20])
        self.var_def.set(b[0x21])
        self.var_mag.set(b[0x22])
        self.var_mdf.set(b[0x23])
        self.var_agi.set(b[0x24])
        self.var_lck.set(b[0x25])
        self.var_eva.set(b[0x26])
        self.var_acc.set(b[0x27])
        
        # Armored Properties
        armored = (b[0x28] & 0x01) > 0
        self.var_armored.set(1 if armored else 0)
        
        # Misc Properties
        self.var_doom.set(b[0x77])
        self.var_arena_idx.set(struct.unpack("<H", b[0x78:0x7A])[0])
        self.var_sound_ref.set(struct.unpack("<H", b[0x7A:0x7C])[0])
        
        # Elemental properties
        def get_elem_state(bit):
            if b[0x2B] & bit: return "Absorb"
            if b[0x2C] & bit: return "Immune"
            if b[0x2D] & bit: return "Resist"
            if b[0x2E] & bit: return "Weak"
            return "Normal"
            
        self.cmb_elem_fire.set(get_elem_state(0x01))
        self.cmb_elem_ice.set(get_elem_state(0x02))
        self.cmb_elem_thunder.set(get_elem_state(0x04))
        self.cmb_elem_water.set(get_elem_state(0x08))
        self.cmb_elem_holy.set(get_elem_state(0x10))
        
        # Status Resists
        self.var_res_death.set(b[0x2F])
        self.var_res_zombie.set(b[0x30])
        self.var_res_petrify.set(b[0x31])
        self.var_res_poison.set(b[0x32])
        self.var_res_powerbreak.set(b[0x33])
        self.var_res_magicbreak.set(b[0x34])
        self.var_res_armorbreak.set(b[0x35])
        self.var_res_mentalbreak.set(b[0x36])
        self.var_res_confuse.set(b[0x37])
        self.var_res_berserk.set(b[0x38])
        self.var_res_provoke.set(b[0x39])
        self.var_res_threaten.set(b[0x3A])
        self.var_res_sleep.set(b[0x3B])
        self.var_res_silence.set(b[0x3C])
        self.var_res_darkness.set(b[0x3D])
        self.var_res_slow.set(b[0x47])
        self.var_res_haste.set(b[0x46])
        
        # Auto-statuses
        perm = struct.unpack("<H", b[0x48:0x4A])[0]
        temp = struct.unpack("<H", b[0x4A:0x4C])[0]
        extra = struct.unpack("<H", b[0x4C:0x4E])[0]
        
        self.var_auto_zombie.set(1 if perm & 0x0002 else 0)
        self.var_auto_poison.set(1 if perm & 0x0008 else 0)
        
        self.var_auto_haste.set(1 if temp & 0x0800 else 0)
        self.var_auto_regen.set(1 if temp & 0x0400 else 0)
        self.var_auto_protect.set(1 if temp & 0x0010 else 0)
        self.var_auto_shell.set(1 if temp & 0x0008 else 0)
        self.var_auto_reflect.set(1 if temp & 0x0020 else 0)
        
        self.var_auto_autolife.set(1 if extra & 0x0200 else 0)
        self.var_auto_doom.set(1 if extra & 0x4000 else 0)

    def parse_monster_loot(self):
        b = self.loot_bytes
        
        self.var_gil.set(struct.unpack("<H", b[0x00:0x02])[0])
        self.var_ap_n.set(struct.unpack("<H", b[0x02:0x04])[0])
        self.var_ap_o.set(struct.unpack("<H", b[0x04:0x06])[0])
        
        # Ronso rage command id
        rage_id = struct.unpack("<H", b[0x06:0x08])[0]
        self.set_combo_to_id(self.cmb_ronso, rage_id)
        
        # Chances
        self.var_pct_drop_p.set(b[0x08])
        self.var_pct_drop_s.set(b[0x09])
        self.var_pct_steal.set(b[0x0A])
        self.var_pct_gear.set(b[0x0B])
        
        # Item drop normal/overkill types
        def set_item_combo(combo, offset):
            item_id = struct.unpack("<H", b[offset:offset+2])[0]
            self.set_combo_to_id(combo, item_id)
            
        set_item_combo(self.cmb_drop_n_p_c, 0x0C)
        set_item_combo(self.cmb_drop_n_p_r, 0x0E)
        set_item_combo(self.cmb_drop_n_s_c, 0x10)
        set_item_combo(self.cmb_drop_n_s_r, 0x12)
        
        self.var_qty_drop_n_p_c.set(b[0x14])
        self.var_qty_drop_n_p_r.set(b[0x15])
        self.var_qty_drop_n_s_c.set(b[0x16])
        self.var_qty_drop_n_s_r.set(b[0x17])
        
        set_item_combo(self.cmb_drop_o_p_c, 0x18)
        set_item_combo(self.cmb_drop_o_p_r, 0x1A)
        set_item_combo(self.cmb_drop_o_s_c, 0x1C)
        set_item_combo(self.cmb_drop_o_s_r, 0x1E)
        
        self.var_qty_drop_o_p_c.set(b[0x20])
        self.var_qty_drop_o_p_r.set(b[0x21])
        self.var_qty_drop_o_s_c.set(b[0x22])
        self.var_qty_drop_o_s_r.set(b[0x23])
        
        # Steal and bribe
        set_item_combo(self.cmb_steal_c, 0x24)
        set_item_combo(self.cmb_steal_r, 0x26)
        self.var_qty_steal_c.set(b[0x28])
        self.var_qty_steal_r.set(b[0x29])
        
        set_item_combo(self.cmb_bribe_item, 0x2A)
        self.var_qty_bribe.set(b[0x2C])
        
        # Zanmato
        self.var_zanmato.set(b[0x112] + 1)
        self.var_gil_steal.set(b[0x113])
        self.var_arena_price.set(struct.unpack("<I", b[0x114:0x118])[0])
        
        # Equipment Properties
        if len(b) > 0x30:
            self.var_weapon_bias.set(b[0x2D] if len(b) > 0x2D else 128)
            self.var_max_slots.set(b[0x2E] if len(b) > 0x2E else 4)
            self.var_slot_variance.set(b[0x2F] if len(b) > 0x2F else 0)
            self.var_ability_weight.set(b[0x30] if len(b) > 0x30 else 0)

    def set_combo_to_id(self, combo, target_id):
        if target_id == 0:
            combo.set("None (0x0000)")
            return
        # Find matches in list
        for item in combo["values"]:
            if f"({hex(target_id)})" in item:
                combo.set(item)
                return
        # Fallback raw hex
        combo.set(f"Unknown (0x{target_id:04X})")

    def get_id_from_combo(self, combo):
        val = combo.get()
        if "None" in val or not val:
            return 0
        try:
            # Parse hex inside parentheses, e.g. "Potion (0x2000)"
            start = val.rfind("(0x")
            if start != -1:
                end = val.find(")", start)
                return int(val[start+3:end], 16)
        except Exception:
            pass
        return 0

    def apply_save(self):
        if not self.current_monster:
            messagebox.showwarning("Warning", "No active monster loaded.")
            return False
            
        m_id = self.current_monster["id"]
        filepath = self.current_monster["path"]
        
        # If GUI has dirty changes, silently apply to cache first
        if self.check_is_dirty():
            try:
                self.apply_monster_edits_silent()
            except Exception as e:
                self.log(f"Failed to apply active edits: {e}", "error")
                messagebox.showerror("Error", f"Failed to serialize changes:\n{str(e)}")
                return False
                
        if m_id not in self.monster_cache:
            return False
            
        cache_entry = self.monster_cache[m_id]
        self.log(f"Writing stats and loot for monster {m_id} to disk...")
        
        try:
            repacked_data = packer.repack_chunks(cache_entry["chunks"])
            
            # Backup and write
            bak_path = filepath + ".bak"
            if not os.path.exists(bak_path):
                shutil.copy2(filepath, bak_path)
                self.log(f"Created backup of original file at {bak_path}")
                
            packer.safe_atomic_write(filepath, repacked_data)
                
            cache_entry["is_dirty"] = False
            
            self.log(f"Saved {len(repacked_data)} bytes successfully to {filepath}.", "success")
            messagebox.showinfo("Success", f"Monster file {m_id}.bin saved successfully!")
            
            # Remove * indicator
            us_name = cache_entry["us_name"]
            self.update_monster_tree_name(m_id, us_name, is_modified=False)
            
            if self.current_monster:
                self.current_monster["name"] = us_name
                
            return True
        except Exception as e:
            self.log(f"Save failed: {e}", "error")
            messagebox.showerror("Error", f"Failed to repack and save file:\n{str(e)}")
            return False

    def serialize_stat_block(self, original_bytes, name, sensor, scan, charset):
        # Build elemental bitfields
        absorb = 0
        immune = 0
        resist = 0
        weak = 0
        elem_combos = [
            (self.cmb_elem_fire.get(), 0x01),
            (self.cmb_elem_ice.get(), 0x02),
            (self.cmb_elem_thunder.get(), 0x04),
            (self.cmb_elem_water.get(), 0x08),
            (self.cmb_elem_holy.get(), 0x10)
        ]
        for state, bit in elem_combos:
            if state == "Absorb": absorb |= bit
            elif state == "Immune": immune |= bit
            elif state == "Resist": resist |= bit
            elif state == "Weak": weak |= bit

        # Auto-statuses
        orig_block = original_bytes[:128]
        perm = struct.unpack("<H", orig_block[0x48:0x4A])[0]
        temp = struct.unpack("<H", orig_block[0x4A:0x4C])[0]
        extra = struct.unpack("<H", orig_block[0x4C:0x4E])[0]
        
        perm = (perm & ~0x0002) | (0x0002 if self.var_auto_zombie.get() else 0)
        perm = (perm & ~0x0008) | (0x0008 if self.var_auto_poison.get() else 0)
        
        temp = (temp & ~0x0800) | (0x0800 if self.var_auto_haste.get() else 0)
        temp = (temp & ~0x0400) | (0x0400 if self.var_auto_regen.get() else 0)
        temp = (temp & ~0x0010) | (0x0010 if self.var_auto_protect.get() else 0)
        temp = (temp & ~0x0008) | (0x0008 if self.var_auto_shell.get() else 0)
        temp = (temp & ~0x0020) | (0x0020 if self.var_auto_reflect.get() else 0)
        
        extra = (extra & ~0x0200) | (0x0200 if self.var_auto_autolife.get() else 0)
        extra = (extra & ~0x4000) | (0x4000 if self.var_auto_doom.get() else 0)

        stats_dict = {
            "hp": self.var_hp.get(),
            "mp": self.var_mp.get(),
            "overkill": self.var_overkill.get(),
            "str": self.var_str.get(),
            "def": self.var_def.get(),
            "mag": self.var_mag.get(),
            "mdf": self.var_mdf.get(),
            "agi": self.var_agi.get(),
            "lck": self.var_lck.get(),
            "eva": self.var_eva.get(),
            "acc": self.var_acc.get(),
            "armored": self.var_armored.get(),
            "doom": self.var_doom.get(),
            "arena_idx": self.var_arena_idx.get(),
            "sound_ref": self.var_sound_ref.get(),
            "elem_absorb": absorb,
            "elem_immune": immune,
            "elem_resist": resist,
            "elem_weak": weak,
            "res_death": self.var_res_death.get(),
            "res_zombie": self.var_res_zombie.get(),
            "res_petrify": self.var_res_petrify.get(),
            "res_poison": self.var_res_poison.get(),
            "res_powerbreak": self.var_res_powerbreak.get(),
            "res_magicbreak": self.var_res_magicbreak.get(),
            "res_armorbreak": self.var_res_armorbreak.get(),
            "res_mentalbreak": self.var_res_mentalbreak.get(),
            "res_confuse": self.var_res_confuse.get(),
            "res_berserk": self.var_res_berserk.get(),
            "res_provoke": self.var_res_provoke.get(),
            "res_threaten": self.var_res_threaten.get(),
            "res_sleep": self.var_res_sleep.get(),
            "res_silence": self.var_res_silence.get(),
            "res_darkness": self.var_res_darkness.get(),
            "res_slow": self.var_res_slow.get(),
            "res_haste": self.var_res_haste.get(),
            "perm_status": perm,
            "temp_status": temp,
            "extra_status": extra
        }

        return packer.serialize_stat_block(original_bytes, stats_dict, name, sensor, scan, self.codec, charset)

    def serialize_loot_block(self):
        block = bytearray(self.loot_bytes)
        
        struct.pack_into("<H", block, 0x00, int(self.var_gil.get()))
        struct.pack_into("<H", block, 0x02, int(self.var_ap_n.get()))
        struct.pack_into("<H", block, 0x04, int(self.var_ap_o.get()))
        
        struct.pack_into("<H", block, 0x06, self.get_id_from_combo(self.cmb_ronso))
        
        block[0x08] = int(self.var_pct_drop_p.get())
        block[0x09] = int(self.var_pct_drop_s.get())
        block[0x0A] = int(self.var_pct_steal.get())
        block[0x0B] = int(self.var_pct_gear.get())
        
        struct.pack_into("<H", block, 0x0C, self.get_id_from_combo(self.cmb_drop_n_p_c))
        struct.pack_into("<H", block, 0x0E, self.get_id_from_combo(self.cmb_drop_n_p_r))
        struct.pack_into("<H", block, 0x10, self.get_id_from_combo(self.cmb_drop_n_s_c))
        struct.pack_into("<H", block, 0x12, self.get_id_from_combo(self.cmb_drop_n_s_r))
        
        block[0x14] = int(self.var_qty_drop_n_p_c.get())
        block[0x15] = int(self.var_qty_drop_n_p_r.get())
        block[0x16] = int(self.var_qty_drop_n_s_c.get())
        block[0x17] = int(self.var_qty_drop_n_s_r.get())
        
        struct.pack_into("<H", block, 0x18, self.get_id_from_combo(self.cmb_drop_o_p_c))
        struct.pack_into("<H", block, 0x1A, self.get_id_from_combo(self.cmb_drop_o_p_r))
        struct.pack_into("<H", block, 0x1C, self.get_id_from_combo(self.cmb_drop_o_s_c))
        struct.pack_into("<H", block, 0x1E, self.get_id_from_combo(self.cmb_drop_o_s_r))
        
        block[0x20] = int(self.var_qty_drop_o_p_c.get())
        block[0x21] = int(self.var_qty_drop_o_p_r.get())
        block[0x22] = int(self.var_qty_drop_o_s_c.get())
        block[0x23] = int(self.var_qty_drop_o_s_r.get())
        
        struct.pack_into("<H", block, 0x24, self.get_id_from_combo(self.cmb_steal_c))
        struct.pack_into("<H", block, 0x26, self.get_id_from_combo(self.cmb_steal_r))
        
        block[0x28] = int(self.var_qty_steal_c.get())
        block[0x29] = int(self.var_qty_steal_r.get())
        
        struct.pack_into("<H", block, 0x2A, self.get_id_from_combo(self.cmb_bribe_item))
        block[0x2C] = int(self.var_qty_bribe.get())
        
        # Equipment Properties
        if len(block) > 0x30:
            block[0x2D] = min(255, max(0, int(self.var_weapon_bias.get())))
            block[0x2E] = min(4, max(1, int(self.var_max_slots.get())))
            block[0x2F] = min(4, max(0, int(self.var_slot_variance.get())))
            block[0x30] = min(255, max(0, int(self.var_ability_weight.get())))
        
        block[0x112] = max(1, min(100, int(self.var_zanmato.get()))) - 1
        block[0x113] = int(self.var_gil_steal.get())
        struct.pack_into("<I", block, 0x114, int(self.var_arena_price.get()))
        
        return bytes(block)

    def filter_monsters(self, event=None):
        q = self.ent_search_mon.get().strip().lower()
        selected_zone = "All Zones"
        if hasattr(self, "cmb_zone_filter"):
            selected_zone = self.cmb_zone_filter.get()
            
        self.tree_monsters.delete(*self.tree_monsters.get_children())
        for m in self.monsters_list:
            m_id = m["id"]
            m_zone = MONSTER_ZONE_MAP.get(m_id, "Other / Field")
            
            # Check zone match
            if selected_zone != "All Zones" and m_zone != selected_zone:
                continue
                
            # Check query match
            if not q or q in m_id or q in m["name"].lower() or q in m_zone.lower():
                disp_name = m["name"]
                if m_id in self.monster_cache and self.monster_cache[m_id].get("is_dirty"):
                    disp_name = f"* {disp_name}"
                self.tree_monsters.insert("", tk.END, iid=m_id, values=(m_id, disp_name))

    def revert_tree_selection(self, prev_id):
        self._handling_select = True
        try:
            self.tree_monsters.selection_set(prev_id)
        finally:
            self._handling_select = False

    def on_monster_selected(self, event=None):
        if hasattr(self, "_handling_select") and self._handling_select:
            return
            
        sel = self.tree_monsters.selection()
        if not sel:
            return
            
        new_m_id = sel[0]
        
        if self.current_monster and self.current_monster["id"] != new_m_id:
            if self.check_is_dirty():
                ans = show_dark_confirm(
                    self.root,
                    "Unapplied Edits",
                    f"You have unapplied edits for {self.current_monster['name']}.\n\n"
                    "Do you want to apply them to memory before switching?"
                )
                if ans is True:
                    try:
                        self.apply_monster_edits_silent()
                    except Exception as e:
                        self.log(f"Failed to apply edits: {e}", "error")
                        messagebox.showerror("Error", f"Failed to serialize changes:\n{str(e)}")
                        self.revert_tree_selection(self.current_monster["id"])
                        return
                elif ans is False:
                    pass
                else:
                    self.revert_tree_selection(self.current_monster["id"])
                    return
                    
        self.load_monster_file(new_m_id)

    def browse_master_folder(self):
        folder = filedialog.askdirectory(title="Select Extracted FFX Master Folder")
        if folder:
            path = os.path.abspath(folder)
            self.config["master_path"] = path
            self.save_config()
            if hasattr(self, "parent") and self.parent and hasattr(self.parent, "update_global_master_path"):
                self.parent.update_global_master_path(path)
            else:
                self.ent_master_path.delete(0, tk.END)
                self.ent_master_path.insert(0, path)
                self.scan_monsters()

    def bind_hover(self, btn, is_primary=False):
        if is_primary:
            btn.bind("<Enter>", lambda e: btn.config(bg=self.accent_hover))
            btn.bind("<Leave>", lambda e: btn.config(bg=self.accent_color))
        else:
            btn.bind("<Enter>", lambda e: btn.config(bg=self.border_color))
            btn.bind("<Leave>", lambda e: btn.config(bg=self.card_color))

    def bind_hover_color(self, btn, hover, normal):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal))

    def create_widgets(self):
        self.main_container = ttk.Frame(self.parent, padding=10)
        self.main_container.pack(fill="both", expand=True)
        
        # Grid layout: Top Bar, Middle Body, Bottom Console (only standalone)
        self.top_panel = ttk.LabelFrame(self.main_container, text=" Configuration ", padding=10)
        self.top_panel.pack(fill="x", side="top", pady=(0, 10))
        
        lbl = ttk.Label(self.top_panel, text="Master Folder:")
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.ent_master_path = ttk.Entry(self.top_panel, width=65)
        self.ent_master_path.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.top_panel.columnconfigure(1, weight=1)
        
        btn_browse = tk.Button(self.top_panel, text="Browse...", command=self.browse_master_folder, bg=self.card_color, 
                               fg=self.text_color, relief="flat", activebackground=self.border_color)
        btn_browse.grid(row=0, column=2, padx=(0, 10))
        self.bind_hover(btn_browse)
        
        btn_scan = tk.Button(self.top_panel, text="Scan Monsters", command=self.scan_monsters, bg=self.accent_color, 
                              fg="white", font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.accent_hover)
        btn_scan.grid(row=0, column=3, padx=(0, 10))
        self.bind_hover(btn_scan, is_primary=True)
        
        btn_scale_all = tk.Button(self.top_panel, text="⚖️ Scale...", command=self.open_batch_scale_dialog, bg=self.card_color, 
                                  fg=self.text_color, font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.border_color)
        btn_scale_all.grid(row=0, column=4, padx=(0, 6))
        self.bind_hover(btn_scale_all, is_primary=False)
        
        btn_random = tk.Button(self.top_panel, text="🎲 Randomizer...", command=self.open_randomizer_dialog, bg=self.card_color, 
                               fg=self.text_color, font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.border_color)
        btn_random.grid(row=0, column=5, padx=(0, 6))
        self.bind_hover(btn_random, is_primary=False)
        
        btn_diff = tk.Button(self.top_panel, text="📊 Stat Diff...", command=self.open_stat_diff_dialog, bg=self.card_color, 
                             fg=self.text_color, font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.border_color)
        btn_diff.grid(row=0, column=6, padx=(0, 6))
        self.bind_hover(btn_diff, is_primary=False)
        
        btn_modpack = tk.Button(self.top_panel, text="📦 Modpack...", command=self.open_modpack_dialog, bg=self.card_color, 
                                fg=self.text_color, font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.border_color)
        btn_modpack.grid(row=0, column=7, padx=(0, 6))
        self.bind_hover(btn_modpack, is_primary=False)
        
        btn_wiki = tk.Button(self.top_panel, text="📄 Bestiary...", command=self.export_bestiary_card, bg=self.card_color, 
                             fg=self.text_color, font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.border_color)
        btn_wiki.grid(row=0, column=8)
        self.bind_hover(btn_wiki, is_primary=False)
        
        # Middle Body split into Left Panel and Right Notebook
        self.body_paned = ttk.PanedWindow(self.main_container, orient="horizontal")
        self.body_paned.pack(fill="both", expand=True, side="top")
        
        self.left_panel = ttk.Frame(self.body_paned, width=280, padding=(0, 0, 10, 0))
        self.body_paned.add(self.left_panel, weight=1)
        
        # Search monster
        sf = ttk.Frame(self.left_panel)
        sf.pack(fill="x", side="top", pady=(0, 4))
        ttk.Label(sf, text="🔍 Filter:").pack(side="left", padx=(0, 5))
        self.ent_search_mon = ttk.Entry(sf)
        self.ent_search_mon.pack(fill="x", expand=True, side="left")
        self.ent_search_mon.bind("<KeyRelease>", self.filter_monsters)
        
        # Zone filter
        zf = ttk.Frame(self.left_panel)
        zf.pack(fill="x", side="top", pady=(0, 8))
        ttk.Label(zf, text="🗺️ Zone:").pack(side="left", padx=(0, 5))
        self.cmb_zone_filter = ttk.Combobox(zf, values=ZONE_CATEGORIES, state="readonly", width=18)
        self.cmb_zone_filter.set("All Zones")
        self.cmb_zone_filter.pack(fill="x", expand=True, side="left")
        self.cmb_zone_filter.bind("<<ComboboxSelected>>", self.filter_monsters)
        
        # Monster List
        tree_frame = ttk.Frame(self.left_panel)
        tree_frame.pack(fill="both", expand=True)
        self.tree_monsters = ttk.Treeview(tree_frame, columns=("ID", "Name"), show="headings", selectmode="extended")
        self.tree_monsters.heading("ID", text="ID")
        self.tree_monsters.heading("Name", text="Name")
        self.tree_monsters.column("ID", width=60, anchor="center")
        self.tree_monsters.column("Name", width=160, anchor="w")
        self.tree_monsters.pack(fill="both", expand=True, side="left")
        self.tree_monsters.bind("<<TreeviewSelect>>", self.on_monster_selected)
        
        # Right click context menu setup
        self.menu_monster = tk.Menu(self.root, tearoff=0, bg=self.card_color, fg=self.text_color, activebackground=self.accent_color, activeforeground="#ffffff")
        self.menu_monster.add_command(label="Restore from Backup (.bak)", command=self.on_restore_monster_backup)
        self.menu_monster.add_command(label="📊 Compare with Backup (Stat Diff)...", command=self.open_stat_diff_dialog)
        self.menu_monster.add_command(label="📄 Export Bestiary Card...", command=self.export_bestiary_card)
        self.menu_monster.add_separator()
        self.menu_monster.add_command(label="Batch Scale Selected Stats...", command=self.on_batch_scale_selected)
        self.menu_monster.add_command(label="Make Selected Status Immune...", command=self.on_batch_immune_selected)
        self.menu_monster.add_command(label="Set Selected Element Affinities...", command=self.on_batch_element_selected)
        
        def show_monster_menu(event):
            item = self.tree_monsters.identify_row(event.y)
            if item:
                # If right-clicked item is not already selected, select it
                if item not in self.tree_monsters.selection():
                    self.tree_monsters.selection_set(item)
                
                # Check if backup exists
                m = next((x for x in self.monsters_list if x["id"] == item), None)
                if m and os.path.exists(m["path"] + ".bak"):
                    self.menu_monster.entryconfig(0, state="normal")
                else:
                    self.menu_monster.entryconfig(0, state="disabled")
                
                # Disable multi-run features if multiple are selected or customize labels
                sel_count = len(self.tree_monsters.selection())
                if sel_count > 1:
                    self.menu_monster.entryconfig(0, state="disabled") # disable backup restore for multi selection
                    
                self.menu_monster.post(event.x_root, event.y_root)
                
        self.tree_monsters.bind("<Button-3>", show_monster_menu)
        
        scroll = ttk.Scrollbar(tree_frame, command=self.tree_monsters.yview)
        scroll.pack(fill="y", side="right")
        self.tree_monsters.config(yscrollcommand=scroll.set)
        
        # Action Buttons frame
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        btn_keep = tk.Button(btn_frame, text="Apply Monster Edits", command=self.apply_monster_edits, bg=self.card_color,
                             fg=self.text_color, font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.border_color, height=2)
        btn_keep.pack(fill="x", pady=(0, 5))
        self.bind_hover(btn_keep, is_primary=False)
        
        btn_save = tk.Button(btn_frame, text="💾 Save Current to Disk", command=self.apply_save, bg=self.accent_color,
                             fg="white", font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.accent_hover, height=2)
        btn_save.pack(fill="x", pady=(0, 5))
        self.bind_hover(btn_save, is_primary=True)
        
        btn_save_all = tk.Button(btn_frame, text="💾 Save All to Disk", command=self.save_all_to_disk, bg=self.success_color,
                                 fg="white", font=("Segoe UI", 9, "bold"), relief="flat", activebackground="#059669", height=2)
        btn_save_all.pack(fill="x")
        self.bind_hover_color(btn_save_all, "#059669", self.success_color)
        
        # Right Panel: Editor Notebook
        self.right_panel = ttk.Frame(self.body_paned, padding=(10, 0, 0, 0))
        self.body_paned.add(self.right_panel, weight=3)
        
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill="both", expand=True)
        
        # 1. AI Script Tab
        self.tab_atel = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_atel, text=" 👾 AI Atel Script ")
        
        # Paned window inside tab_atel
        paned_atel = ttk.Panedwindow(self.tab_atel, orient="horizontal")
        paned_atel.pack(fill="both", expand=True)
        
        # Left pane: Script viewer
        frame_viewer = ttk.Frame(paned_atel)
        paned_atel.add(frame_viewer, weight=2)
        
        # Left pane toolbar
        frame_toolbar = ttk.Frame(frame_viewer)
        frame_toolbar.pack(fill="x", pady=(0, 5))
        ttk.Label(frame_toolbar, text="View Mode:").pack(side="left", padx=(0, 5))
        self.cmb_atel_mode = ttk.Combobox(frame_toolbar, values=["Raw Assembly", "Decompiled Pseudocode", "Plain English"], state="readonly", width=22)
        self.cmb_atel_mode.set("Decompiled Pseudocode")
        self.cmb_atel_mode.pack(side="left")
        self.cmb_atel_mode.bind("<<ComboboxSelected>>", lambda e: self.disassemble_ai_script())
        
        # Scrollbars and text
        scroll_frame = ttk.Frame(frame_viewer)
        scroll_frame.pack(fill="both", expand=True)
        self.txt_atel = tk.Text(scroll_frame, bg="#0d0d0d", fg="#a7f3d0", font=("Consolas", 10), wrap="none", relief="flat")
        self.txt_atel.pack(fill="both", expand=True, side="left")
        
        scroll_atel_y = ttk.Scrollbar(scroll_frame, command=self.txt_atel.yview)
        scroll_atel_y.pack(fill="y", side="right")
        scroll_atel_x = ttk.Scrollbar(frame_viewer, orient="horizontal", command=self.txt_atel.xview)
        scroll_atel_x.pack(fill="x", side="bottom")
        self.txt_atel.config(yscrollcommand=scroll_atel_y.set, xscrollcommand=scroll_atel_x.set)
        
        # Right pane: Constants Editor
        frame_constants = ttk.LabelFrame(paned_atel, text=" Constants Editor ", padding=5)
        paned_atel.add(frame_constants, weight=1)
        
        # Treeview for constants
        tree_frame = ttk.Frame(frame_constants)
        tree_frame.pack(fill="both", expand=True)
        
        self.tree_constants = ttk.Treeview(tree_frame, columns=("worker", "type", "index", "value"), show="headings", selectmode="browse")
        self.tree_constants.heading("worker", text="Worker")
        self.tree_constants.heading("type", text="Type")
        self.tree_constants.heading("index", text="Idx")
        self.tree_constants.heading("value", text="Value")
        self.tree_constants.column("worker", width=60, anchor="center")
        self.tree_constants.column("type", width=70, anchor="center")
        self.tree_constants.column("index", width=40, anchor="center")
        self.tree_constants.column("value", width=90, anchor="e")
        self.tree_constants.pack(fill="both", expand=True, side="left")
        
        scroll_const_y = ttk.Scrollbar(tree_frame, command=self.tree_constants.yview)
        scroll_const_y.pack(fill="y", side="right")
        self.tree_constants.config(yscrollcommand=scroll_const_y.set)
        
        # Controls
        control_frame = ttk.Frame(frame_constants, padding=5)
        control_frame.pack(fill="x", pady=5)
        
        ttk.Label(control_frame, text="Value:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_const_val = ttk.Entry(control_frame, width=15)
        self.ent_const_val.grid(row=0, column=1, padx=5, pady=5)
        
        btn_update_const = tk.Button(control_frame, text="Apply Value", command=self.on_apply_const_value, bg=self.accent_color, fg="#ffffff", activebackground=self.active_color, relief="flat", padx=10)
        btn_update_const.grid(row=0, column=2, padx=5, pady=5)
        self.bind_hover(btn_update_const)
        
        btn_save_consts = tk.Button(frame_constants, text="Apply Constants to Script", command=self.on_apply_constants_to_script, bg=self.btn_color_secondary, fg="#ffffff", activebackground=self.active_color, relief="flat", pady=5)
        btn_save_consts.pack(fill="x", side="bottom", pady=5)
        self.bind_hover(btn_save_consts)
        
        self.tree_constants.bind("<<TreeviewSelect>>", lambda e: self.on_constant_selected())
        
        # 2. Stats Tab
        self.tab_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stats, text=" 📊 Attributes & Elements ")
        self.build_stats_tab(self.tab_stats)
        
        # 3. Status Tab
        self.tab_status = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_status, text=" 🛡️ Status Resistances ")
        self.build_status_tab(self.tab_status)
        
        # 4. Loot Tab
        self.tab_loot = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_loot, text=" 💎 Loot Tables ")
        self.build_loot_tab(self.tab_loot)
        
        # 5. Rule Builder Tab
        self.tab_rule_builder = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_rule_builder, text=" 🔧 Visual AI Rule Builder ")
        self.build_rule_builder_tab(self.tab_rule_builder)
        
        # 6. Player Stats Tab
        self.tab_player_stats = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_player_stats, text=" 👤 Player Stats ")
        self.build_player_stats_tab(self.tab_player_stats)
        
        # 7. Visual AI Flowchart Tab
        self.tab_flowchart = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_flowchart, text=" 📈 Visual AI Flowchart ")
        self.build_flowchart_tab(self.tab_flowchart)
        
        # 8. Encounter & Formation Map Tab
        self.tab_encounters = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_encounters, text=" 🗺️ Encounters & Spawns ")
        self.build_encounters_tab(self.tab_encounters)
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_atel_notebook_tab_changed)
        
        if not self.is_embedded:
            self.console_panel = ttk.LabelFrame(self.main_container, text=" Process Logs ", padding=5)
            self.console_panel.pack(fill="x", side="bottom", pady=(10, 0))
            self.txt_log = tk.Text(self.console_panel, bg="#0d0d0d", fg="#e5e7eb", font=("Consolas", 9), height=5, wrap="word", relief="flat")
            self.txt_log.pack(fill="both", expand=True, side="left")
            log_scroll = ttk.Scrollbar(self.console_panel, command=self.txt_log.yview)
            log_scroll.pack(fill="y", side="right")
            self.txt_log.config(yscrollcommand=log_scroll.set)

    def build_stats_tab(self, parent):
        # Create scrollable frame
        canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        scroll_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        scroll_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Setup sub-panels in scroll_frame
        # Localized strings
        grp_names = ttk.LabelFrame(scroll_frame, text=" Monster Localization (Names & Description) ", padding=10)
        grp_names.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(grp_names, text="Japanese Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_jp_name = ttk.Entry(grp_names, width=25)
        self.ent_jp_name.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_names, text="English Name:").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.ent_us_name = ttk.Entry(grp_names, width=25)
        self.ent_us_name.grid(row=0, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_names, text="Japanese Sensor:").grid(row=1, column=0, sticky="nw", pady=5)
        self.txt_jp_sensor = tk.Text(grp_names, width=30, height=3, bg=self.card_color, fg=self.text_color, insertbackground="white", highlightthickness=1, highlightbackground=self.border_color, relief="flat", font=("Segoe UI", 9))
        self.txt_jp_sensor.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        
        ttk.Label(grp_names, text="English Sensor:").grid(row=1, column=2, sticky="nw", pady=5, padx=(20, 0))
        self.txt_us_sensor = tk.Text(grp_names, width=30, height=3, bg=self.card_color, fg=self.text_color, insertbackground="white", highlightthickness=1, highlightbackground=self.border_color, relief="flat", font=("Segoe UI", 9))
        self.txt_us_sensor.grid(row=1, column=3, sticky="ew", pady=5, padx=5)

        ttk.Label(grp_names, text="Japanese Scan:").grid(row=2, column=0, sticky="nw", pady=5)
        self.txt_jp_scan = tk.Text(grp_names, width=30, height=3, bg=self.card_color, fg=self.text_color, insertbackground="white", highlightthickness=1, highlightbackground=self.border_color, relief="flat", font=("Segoe UI", 9))
        self.txt_jp_scan.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        
        ttk.Label(grp_names, text="English Scan:").grid(row=2, column=2, sticky="nw", pady=5, padx=(20, 0))
        self.txt_us_scan = tk.Text(grp_names, width=30, height=3, bg=self.card_color, fg=self.text_color, insertbackground="white", highlightthickness=1, highlightbackground=self.border_color, relief="flat", font=("Segoe UI", 9))
        self.txt_us_scan.grid(row=2, column=3, sticky="ew", pady=5, padx=5)

        grp_names.columnconfigure(1, weight=1)
        grp_names.columnconfigure(3, weight=1)

        # Attributes
        grp_attr = ttk.LabelFrame(scroll_frame, text=" Base Attributes ", padding=10)
        grp_attr.pack(fill="x", padx=10, pady=5)
        for c in range(6):
            grp_attr.columnconfigure(c, weight=1)
        
        # row 0
        ttk.Label(grp_attr, text="HP:").grid(row=0, column=0, sticky="w", pady=5)
        self.var_hp = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=9999999, textvariable=self.var_hp, width=12, bg=self.card_color, fg=self.text_color, buttonbackground=self.card_color).grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="MP:").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.var_mp = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=99999, textvariable=self.var_mp, width=12, bg=self.card_color, fg=self.text_color, buttonbackground=self.card_color).grid(row=0, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Overkill HP:").grid(row=0, column=4, sticky="w", pady=5, padx=(20, 0))
        self.var_overkill = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=999999, textvariable=self.var_overkill, width=12, bg=self.card_color, fg=self.text_color, buttonbackground=self.card_color).grid(row=0, column=5, sticky="w", pady=5, padx=5)
        
        # row 1
        ttk.Label(grp_attr, text="Strength:").grid(row=1, column=0, sticky="w", pady=5)
        self.var_str = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=255, textvariable=self.var_str, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Defense:").grid(row=1, column=2, sticky="w", pady=5, padx=(20, 0))
        self.var_def = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=255, textvariable=self.var_def, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Magic:").grid(row=1, column=4, sticky="w", pady=5, padx=(20, 0))
        self.var_mag = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=255, textvariable=self.var_mag, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=5, sticky="w", pady=5, padx=5)

        # row 2
        ttk.Label(grp_attr, text="Magic Def:").grid(row=2, column=0, sticky="w", pady=5)
        self.var_mdf = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=255, textvariable=self.var_mdf, width=8, bg=self.card_color, fg=self.text_color).grid(row=2, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Agility:").grid(row=2, column=2, sticky="w", pady=5, padx=(20, 0))
        self.var_agi = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=255, textvariable=self.var_agi, width=8, bg=self.card_color, fg=self.text_color).grid(row=2, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Luck:").grid(row=2, column=4, sticky="w", pady=5, padx=(20, 0))
        self.var_lck = tk.StringVar(value="1")
        tk.Spinbox(grp_attr, from_=1, to=255, textvariable=self.var_lck, width=8, bg=self.card_color, fg=self.text_color).grid(row=2, column=5, sticky="w", pady=5, padx=5)
        
        # row 3
        ttk.Label(grp_attr, text="Evasion:").grid(row=3, column=0, sticky="w", pady=5)
        self.var_eva = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=255, textvariable=self.var_eva, width=8, bg=self.card_color, fg=self.text_color).grid(row=3, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Accuracy:").grid(row=3, column=2, sticky="w", pady=5, padx=(20, 0))
        self.var_acc = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=255, textvariable=self.var_acc, width=8, bg=self.card_color, fg=self.text_color).grid(row=3, column=3, sticky="w", pady=5, padx=5)
        
        # Properties
        ttk.Label(grp_attr, text="Armored:").grid(row=3, column=4, sticky="w", pady=5, padx=(20, 0))
        self.var_armored = tk.IntVar()
        ttk.Checkbutton(grp_attr, text="Pierce protection", variable=self.var_armored).grid(row=3, column=5, sticky="w", pady=5, padx=5)

        # row 4 (CTB Icon, Doom Counter, Sound Bank Ref)
        ttk.Label(grp_attr, text="Doom Count:").grid(row=4, column=0, sticky="w", pady=5)
        self.var_doom = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=255, textvariable=self.var_doom, width=8, bg=self.card_color, fg=self.text_color).grid(row=4, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Arena ID:").grid(row=4, column=2, sticky="w", pady=5, padx=(20, 0))
        self.var_arena_idx = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=65535, textvariable=self.var_arena_idx, width=12, bg=self.card_color, fg=self.text_color).grid(row=4, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_attr, text="Sound Bank:").grid(row=4, column=4, sticky="w", pady=5, padx=(20, 0))
        self.var_sound_ref = tk.StringVar(value="0")
        tk.Spinbox(grp_attr, from_=0, to=65535, textvariable=self.var_sound_ref, width=12, bg=self.card_color, fg=self.text_color).grid(row=4, column=5, sticky="w", pady=5, padx=5)

        # Elements
        grp_elem = ttk.LabelFrame(scroll_frame, text=" Elemental Affinities ", padding=10)
        grp_elem.pack(fill="x", padx=10, pady=5)
        
        elements = [("Fire", "cmb_elem_fire"), ("Ice", "cmb_elem_ice"), ("Thunder", "cmb_elem_thunder"), ("Water", "cmb_elem_water"), ("Holy", "cmb_elem_holy")]
        for idx, (el_name, el_var) in enumerate(elements):
            c = idx * 2
            ttk.Label(grp_elem, text=f"{el_name}:").grid(row=0, column=c, sticky="w", pady=5, padx=(10 if c > 0 else 0, 0))
            
            combo = ttk.Combobox(grp_elem, state="readonly", width=8)
            combo["values"] = ELEMENT_STATES
            combo.set("Normal")
            combo.grid(row=0, column=c+1, sticky="w", pady=5, padx=5)
            setattr(self, el_var, combo)

    def build_status_tab(self, parent):
        canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        scroll_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        scroll_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Resistances Panel
        grp_res = ttk.LabelFrame(scroll_frame, text=" Status Resistance Chance (0% to 100%, 255 = Immune) ", padding=10)
        grp_res.pack(fill="x", padx=10, pady=10)
        for c in range(6):
            grp_res.columnconfigure(c, weight=1)
        
        status_fields = [
            ("Death", "var_res_death"), ("Zombie", "var_res_zombie"), ("Petrify", "var_res_petrify"),
            ("Poison", "var_res_poison"), ("Confuse", "var_res_confuse"), ("Berserk", "var_res_berserk"),
            ("Provoke", "var_res_provoke"), ("Threaten", "var_res_threaten"), ("Sleep", "var_res_sleep"),
            ("Silence", "var_res_silence"), ("Darkness", "var_res_darkness"), ("Slow", "var_res_slow"),
            ("Haste", "var_res_haste"), ("Power Break", "var_res_powerbreak"), ("Magic Break", "var_res_magicbreak"),
            ("Armor Break", "var_res_armorbreak"), ("Mental Break", "var_res_mentalbreak")
        ]
        
        for idx, (label_txt, var_name) in enumerate(status_fields):
            r = idx // 3
            c = (idx % 3) * 2
            
            ttk.Label(grp_res, text=f"{label_txt}:").grid(row=r, column=c, sticky="w", pady=5, padx=(10 if c > 0 else 0, 0))
            
            var = tk.StringVar(value="0")
            spin = tk.Spinbox(grp_res, from_=0, to=255, textvariable=var, width=5, bg=self.card_color, fg=self.text_color)
            spin.grid(row=r, column=c+1, sticky="w", pady=5, padx=5)
            setattr(self, var_name, var)
            
        # Auto-statuses
        grp_auto = ttk.LabelFrame(scroll_frame, text=" Permanent / Auto-Statuses ", padding=10)
        grp_auto.pack(fill="x", padx=10, pady=5)
        
        auto_statuses = [
            ("Auto-Zombie", "var_auto_zombie"),
            ("Auto-Poison", "var_auto_poison"),
            ("Auto-Haste", "var_auto_haste"),
            ("Auto-Regen", "var_auto_regen"),
            ("Auto-Protect", "var_auto_protect"),
            ("Auto-Shell", "var_auto_shell"),
            ("Auto-Reflect", "var_auto_reflect"),
            ("Auto-Life", "var_auto_autolife"),
            ("Auto-Doom", "var_auto_doom")
        ]
        
        for idx, (lbl_txt, var_name) in enumerate(auto_statuses):
            r = idx // 3
            c = idx % 3
            
            var = tk.IntVar()
            chk = ttk.Checkbutton(grp_auto, text=lbl_txt, variable=var)
            chk.grid(row=r, column=c, sticky="w", pady=5, padx=10)
            setattr(self, var_name, var)

    def build_loot_tab(self, parent):
        canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        scroll_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        scroll_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # AP & Gil
        grp_basics = ttk.LabelFrame(scroll_frame, text=" AP, Gil & Rage ", padding=10)
        grp_basics.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(grp_basics, text="Gil:").grid(row=0, column=0, sticky="w", pady=5)
        self.var_gil = tk.StringVar(value="0")
        tk.Spinbox(grp_basics, from_=0, to=999999, textvariable=self.var_gil, width=10, bg=self.card_color, fg=self.text_color).grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_basics, text="AP Normal:").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.var_ap_n = tk.StringVar(value="0")
        tk.Spinbox(grp_basics, from_=0, to=99999, textvariable=self.var_ap_n, width=10, bg=self.card_color, fg=self.text_color).grid(row=0, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_basics, text="AP Overkill:").grid(row=0, column=4, sticky="w", pady=5, padx=(20, 0))
        self.var_ap_o = tk.StringVar(value="0")
        tk.Spinbox(grp_basics, from_=0, to=99999, textvariable=self.var_ap_o, width=10, bg=self.card_color, fg=self.text_color).grid(row=0, column=5, sticky="w", pady=5, padx=5)

        ttk.Label(grp_basics, text="Ronso Rage:").grid(row=1, column=0, sticky="w", pady=5)
        self.cmb_ronso = ttk.Combobox(grp_basics, state="readonly", width=20)
        self.cmb_ronso.grid(row=1, column=1, columnspan=2, sticky="w", pady=5, padx=5)

        # Loot Drop chances
        grp_chances = ttk.LabelFrame(scroll_frame, text=" Drop / Steal Chances (0-255) ", padding=10)
        grp_chances.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(grp_chances, text="Primary Drop %:").grid(row=0, column=0, sticky="w", pady=5)
        self.var_pct_drop_p = tk.StringVar(value="0")
        tk.Spinbox(grp_chances, from_=0, to=255, textvariable=self.var_pct_drop_p, width=8, bg=self.card_color, fg=self.text_color).grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_chances, text="Secondary Drop %:").grid(row=0, column=2, sticky="w", pady=5, padx=(15, 0))
        self.var_pct_drop_s = tk.StringVar(value="0")
        tk.Spinbox(grp_chances, from_=0, to=255, textvariable=self.var_pct_drop_s, width=8, bg=self.card_color, fg=self.text_color).grid(row=0, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_chances, text="Steal Chance %:").grid(row=0, column=4, sticky="w", pady=5, padx=(15, 0))
        self.var_pct_steal = tk.StringVar(value="0")
        tk.Spinbox(grp_chances, from_=0, to=255, textvariable=self.var_pct_steal, width=8, bg=self.card_color, fg=self.text_color).grid(row=0, column=5, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_chances, text="Gear Drop %:").grid(row=0, column=6, sticky="w", pady=5, padx=(15, 0))
        self.var_pct_gear = tk.StringVar(value="0")
        tk.Spinbox(grp_chances, from_=0, to=255, textvariable=self.var_pct_gear, width=8, bg=self.card_color, fg=self.text_color).grid(row=0, column=7, sticky="w", pady=5, padx=5)

        # Detailed Drops table
        grp_details = ttk.LabelFrame(scroll_frame, text=" Detailed Drops & Steals Items ", padding=10)
        grp_details.pack(fill="x", padx=10, pady=5)
        
        # Primary Drop Normal
        ttk.Label(grp_details, text="Primary Drop (Normal):", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        
        ttk.Label(grp_details, text="Common:").grid(row=0, column=1, sticky="w", pady=5)
        self.cmb_drop_n_p_c = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_n_p_c.grid(row=0, column=2, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=0, column=3, sticky="w", pady=5)
        self.var_qty_drop_n_p_c = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_n_p_c, width=4, bg=self.card_color, fg=self.text_color).grid(row=0, column=4, sticky="w", pady=5, padx=5)

        ttk.Label(grp_details, text="Rare:").grid(row=0, column=5, sticky="w", pady=5, padx=(15, 0))
        self.cmb_drop_n_p_r = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_n_p_r.grid(row=0, column=6, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=0, column=7, sticky="w", pady=5)
        self.var_qty_drop_n_p_r = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_n_p_r, width=4, bg=self.card_color, fg=self.text_color).grid(row=0, column=8, sticky="w", pady=5, padx=5)

        # Primary Drop Overkill
        ttk.Label(grp_details, text="Primary Drop (Overkill):", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        
        ttk.Label(grp_details, text="Common:").grid(row=1, column=1, sticky="w", pady=5)
        self.cmb_drop_o_p_c = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_o_p_c.grid(row=1, column=2, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=1, column=3, sticky="w", pady=5)
        self.var_qty_drop_o_p_c = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_o_p_c, width=4, bg=self.card_color, fg=self.text_color).grid(row=1, column=4, sticky="w", pady=5, padx=5)

        ttk.Label(grp_details, text="Rare:").grid(row=1, column=5, sticky="w", pady=5, padx=(15, 0))
        self.cmb_drop_o_p_r = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_o_p_r.grid(row=1, column=6, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=1, column=7, sticky="w", pady=5)
        self.var_qty_drop_o_p_r = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_o_p_r, width=4, bg=self.card_color, fg=self.text_color).grid(row=1, column=8, sticky="w", pady=5, padx=5)

        # Secondary Drop Normal
        ttk.Label(grp_details, text="Secondary Drop (Normal):", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        
        ttk.Label(grp_details, text="Common:").grid(row=2, column=1, sticky="w", pady=5)
        self.cmb_drop_n_s_c = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_n_s_c.grid(row=2, column=2, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=2, column=3, sticky="w", pady=5)
        self.var_qty_drop_n_s_c = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_n_s_c, width=4, bg=self.card_color, fg=self.text_color).grid(row=2, column=4, sticky="w", pady=5, padx=5)

        ttk.Label(grp_details, text="Rare:").grid(row=2, column=5, sticky="w", pady=5, padx=(15, 0))
        self.cmb_drop_n_s_r = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_n_s_r.grid(row=2, column=6, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=2, column=7, sticky="w", pady=5)
        self.var_qty_drop_n_s_r = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_n_s_r, width=4, bg=self.card_color, fg=self.text_color).grid(row=2, column=8, sticky="w", pady=5, padx=5)

        # Secondary Drop Overkill
        ttk.Label(grp_details, text="Secondary Drop (Overkill):", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        
        ttk.Label(grp_details, text="Common:").grid(row=3, column=1, sticky="w", pady=5)
        self.cmb_drop_o_s_c = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_o_s_c.grid(row=3, column=2, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=3, column=3, sticky="w", pady=5)
        self.var_qty_drop_o_s_c = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_o_s_c, width=4, bg=self.card_color, fg=self.text_color).grid(row=3, column=4, sticky="w", pady=5, padx=5)

        ttk.Label(grp_details, text="Rare:").grid(row=3, column=5, sticky="w", pady=5, padx=(15, 0))
        self.cmb_drop_o_s_r = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_drop_o_s_r.grid(row=3, column=6, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=3, column=7, sticky="w", pady=5)
        self.var_qty_drop_o_s_r = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_drop_o_s_r, width=4, bg=self.card_color, fg=self.text_color).grid(row=3, column=8, sticky="w", pady=5, padx=5)

        # Steals
        ttk.Label(grp_details, text="Steal Drop Loot:", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        
        ttk.Label(grp_details, text="Common:").grid(row=4, column=1, sticky="w", pady=5)
        self.cmb_steal_c = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_steal_c.grid(row=4, column=2, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=4, column=3, sticky="w", pady=5)
        self.var_qty_steal_c = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_steal_c, width=4, bg=self.card_color, fg=self.text_color).grid(row=4, column=4, sticky="w", pady=5, padx=5)

        ttk.Label(grp_details, text="Rare:").grid(row=4, column=5, sticky="w", pady=5, padx=(15, 0))
        self.cmb_steal_r = ttk.Combobox(grp_details, state="readonly", width=18)
        self.cmb_steal_r.grid(row=4, column=6, sticky="w", pady=5, padx=5)
        ttk.Label(grp_details, text="Qty:").grid(row=4, column=7, sticky="w", pady=5)
        self.var_qty_steal_r = tk.StringVar(value="1")
        tk.Spinbox(grp_details, from_=1, to=99, textvariable=self.var_qty_steal_r, width=4, bg=self.card_color, fg=self.text_color).grid(row=4, column=8, sticky="w", pady=5, padx=5)

        # Bribe & Zanmato properties
        grp_bribe = ttk.LabelFrame(scroll_frame, text=" Bribe & Zanmato Level ", padding=10)
        grp_bribe.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(grp_bribe, text="Bribe Item:").grid(row=0, column=0, sticky="w", pady=5)
        self.cmb_bribe_item = ttk.Combobox(grp_bribe, state="readonly", width=20)
        self.cmb_bribe_item.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_bribe, text="Bribe Qty:").grid(row=0, column=2, sticky="w", pady=5, padx=(15, 0))
        self.var_qty_bribe = tk.StringVar(value="0")
        tk.Spinbox(grp_bribe, from_=0, to=99, textvariable=self.var_qty_bribe, width=6, bg=self.card_color, fg=self.text_color).grid(row=0, column=3, sticky="w", pady=5, padx=5)

        ttk.Label(grp_bribe, text="Zanmato Level (1-5):").grid(row=0, column=4, sticky="w", pady=5, padx=(15, 0))
        self.var_zanmato = tk.StringVar(value="1")
        tk.Spinbox(grp_bribe, from_=1, to=5, textvariable=self.var_zanmato, width=5, bg=self.card_color, fg=self.text_color).grid(row=0, column=5, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_bribe, text="Stealable Gil (x100):").grid(row=1, column=0, sticky="w", pady=5)
        self.var_gil_steal = tk.StringVar(value="0")
        tk.Spinbox(grp_bribe, from_=0, to=255, textvariable=self.var_gil_steal, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_bribe, text="Arena Price:").grid(row=1, column=2, sticky="w", pady=5, padx=(15, 0))
        self.var_arena_price = tk.StringVar(value="0")
        tk.Spinbox(grp_bribe, from_=0, to=9999999, textvariable=self.var_arena_price, width=12, bg=self.card_color, fg=self.text_color).grid(row=1, column=3, sticky="w", pady=5, padx=5)

        # Equipment Drop Properties
        grp_gear = ttk.LabelFrame(scroll_frame, text=" Equipment Drops & Slot Properties ", padding=10)
        grp_gear.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(grp_gear, text="Weapon Drop Bias (0-255):").grid(row=0, column=0, sticky="w", pady=5)
        self.var_weapon_bias = tk.StringVar(value="128")
        tk.Spinbox(grp_gear, from_=0, to=255, textvariable=self.var_weapon_bias, width=8, bg=self.card_color, fg=self.text_color).grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_gear, text="Max Slots (1-4):").grid(row=0, column=2, sticky="w", pady=5, padx=(15, 0))
        self.var_max_slots = tk.StringVar(value="4")
        tk.Spinbox(grp_gear, from_=1, to=4, textvariable=self.var_max_slots, width=6, bg=self.card_color, fg=self.text_color).grid(row=0, column=3, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_gear, text="Slot Variance (0-4):").grid(row=0, column=4, sticky="w", pady=5, padx=(15, 0))
        self.var_slot_variance = tk.StringVar(value="0")
        tk.Spinbox(grp_gear, from_=0, to=4, textvariable=self.var_slot_variance, width=6, bg=self.card_color, fg=self.text_color).grid(row=0, column=5, sticky="w", pady=5, padx=5)
        
        ttk.Label(grp_gear, text="Auto-Ability Bonus Weight:").grid(row=1, column=0, sticky="w", pady=5)
        self.var_ability_weight = tk.StringVar(value="0")
        tk.Spinbox(grp_gear, from_=0, to=255, textvariable=self.var_ability_weight, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=1, sticky="w", pady=5, padx=5)

    def build_player_stats_tab(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(top_frame, text="Select Playable Character:").pack(side="left", padx=5)
        self.cmb_player_char = ttk.Combobox(top_frame, values=[
            "Tidus (Rec 0)",
            "Yuna (Rec 1)",
            "Auron (Rec 2)",
            "Kimahri (Rec 3)",
            "Wakka (Rec 4)",
            "Lulu (Rec 5)",
            "Rikku (Rec 6)",
            "Seymour (Rec 7)"
        ], state="readonly", width=25)
        self.cmb_player_char.set("Tidus (Rec 0)")
        self.cmb_player_char.pack(side="left", padx=5)
        self.cmb_player_char.bind("<<ComboboxSelected>>", self.on_player_char_selected)
        
        self.grp_player_attr = ttk.LabelFrame(parent, text=" Character Base Attributes ", padding=15)
        self.grp_player_attr.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.var_ply_hp = tk.StringVar(value="0")
        self.var_ply_mp = tk.StringVar(value="0")
        self.var_ply_str = tk.StringVar(value="0")
        self.var_ply_def = tk.StringVar(value="0")
        self.var_ply_mag = tk.StringVar(value="0")
        self.var_ply_mdf = tk.StringVar(value="0")
        self.var_ply_agi = tk.StringVar(value="0")
        self.var_ply_lck = tk.StringVar(value="0")
        self.var_ply_eva = tk.StringVar(value="0")
        self.var_ply_acc = tk.StringVar(value="0")
        
        ttk.Label(self.grp_player_attr, text="HP:").grid(row=0, column=0, sticky="w", pady=6, padx=5)
        tk.Spinbox(self.grp_player_attr, from_=1, to=9999999, textvariable=self.var_ply_hp, width=12, bg=self.card_color, fg=self.text_color, buttonbackground=self.card_color).grid(row=0, column=1, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="MP:").grid(row=0, column=2, sticky="w", pady=6, padx=(20, 5))
        tk.Spinbox(self.grp_player_attr, from_=0, to=99999, textvariable=self.var_ply_mp, width=12, bg=self.card_color, fg=self.text_color, buttonbackground=self.card_color).grid(row=0, column=3, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Strength:").grid(row=1, column=0, sticky="w", pady=6, padx=5)
        tk.Spinbox(self.grp_player_attr, from_=1, to=255, textvariable=self.var_ply_str, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=1, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Defense:").grid(row=1, column=2, sticky="w", pady=6, padx=(20, 5))
        tk.Spinbox(self.grp_player_attr, from_=1, to=255, textvariable=self.var_ply_def, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=3, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Magic:").grid(row=1, column=4, sticky="w", pady=6, padx=(20, 5))
        tk.Spinbox(self.grp_player_attr, from_=1, to=255, textvariable=self.var_ply_mag, width=8, bg=self.card_color, fg=self.text_color).grid(row=1, column=5, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Magic Def:").grid(row=2, column=0, sticky="w", pady=6, padx=5)
        tk.Spinbox(self.grp_player_attr, from_=1, to=255, textvariable=self.var_ply_mdf, width=8, bg=self.card_color, fg=self.text_color).grid(row=2, column=1, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Agility:").grid(row=2, column=2, sticky="w", pady=6, padx=(20, 5))
        tk.Spinbox(self.grp_player_attr, from_=1, to=255, textvariable=self.var_ply_agi, width=8, bg=self.card_color, fg=self.text_color).grid(row=2, column=3, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Luck:").grid(row=2, column=4, sticky="w", pady=6, padx=(20, 5))
        tk.Spinbox(self.grp_player_attr, from_=1, to=255, textvariable=self.var_ply_lck, width=8, bg=self.card_color, fg=self.text_color).grid(row=2, column=5, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Evasion:").grid(row=3, column=0, sticky="w", pady=6, padx=5)
        tk.Spinbox(self.grp_player_attr, from_=0, to=255, textvariable=self.var_ply_eva, width=8, bg=self.card_color, fg=self.text_color).grid(row=3, column=1, sticky="w", pady=6, padx=5)
        
        ttk.Label(self.grp_player_attr, text="Accuracy:").grid(row=3, column=2, sticky="w", pady=6, padx=(20, 5))
        tk.Spinbox(self.grp_player_attr, from_=0, to=255, textvariable=self.var_ply_acc, width=8, bg=self.card_color, fg=self.text_color).grid(row=3, column=3, sticky="w", pady=6, padx=5)
        
        btn_ply_frame = ttk.Frame(parent)
        btn_ply_frame.pack(fill="x", pady=15)
        
        btn_ply_apply = tk.Button(btn_ply_frame, text="Apply Character Edits", command=self.on_apply_player_edits, bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief="flat", height=2)
        btn_ply_apply.pack(fill="x", pady=2)
        self.bind_hover(btn_ply_apply, is_primary=True)
        
        btn_ply_save = tk.Button(btn_ply_frame, text="💾 Save Player Stats to Disk", command=self.on_save_player_stats, bg=self.success_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief="flat", height=2)
        btn_ply_save.pack(fill="x", pady=2)
        self.bind_hover_color(btn_ply_save, "#059669", self.success_color)

    def load_player_stats(self):
        self.player_data_bytes = bytearray()
        if not self.master_path or not os.path.exists(self.master_path):
            return
        loc = "new_uspc" if os.path.exists(os.path.join(self.master_path, "new_uspc")) else "jppc"
        filepath = os.path.join(self.master_path, loc, "battle", "kernel", "ply_save.bin")
        if not os.path.exists(filepath):
            found = False
            for root, dirs, files in os.walk(self.master_path):
                if "ply_save.bin" in files:
                    filepath = os.path.join(root, "ply_save.bin")
                    found = True
                    break
            if not found:
                self.log("Could not find ply_save.bin", "error")
                return
        try:
            with open(filepath, "rb") as f:
                self.player_data_bytes = bytearray(f.read())
            self.log(f"Loaded player stats database (size={len(self.player_data_bytes)}).", "success")
            self.on_player_char_selected()
        except Exception as e:
            self.log(f"Failed to load player stats: {e}", "error")

    def on_player_char_selected(self, event=None):
        if not hasattr(self, "player_data_bytes") or not self.player_data_bytes:
            return
        val = self.cmb_player_char.get()
        try:
            char_idx = int(val.split("Rec ")[1].replace(")", ""))
        except Exception:
            return
            
        rec_len = 148
        offset = 20 + char_idx * rec_len
        if offset + 20 > len(self.player_data_bytes):
            return
            
        hp = struct.unpack("<I", self.player_data_bytes[offset + 4 : offset + 8])[0]
        mp = struct.unpack("<I", self.player_data_bytes[offset + 8 : offset + 12])[0]
        
        self.var_ply_hp.set(hp)
        self.var_ply_mp.set(mp)
        
        self.var_ply_str.set(self.player_data_bytes[offset + 12])
        self.var_ply_def.set(self.player_data_bytes[offset + 13])
        self.var_ply_mag.set(self.player_data_bytes[offset + 14])
        self.var_ply_mdf.set(self.player_data_bytes[offset + 15])
        self.var_ply_agi.set(self.player_data_bytes[offset + 16])
        self.var_ply_lck.set(self.player_data_bytes[offset + 17])
        self.var_ply_eva.set(self.player_data_bytes[offset + 18])
        self.var_ply_acc.set(self.player_data_bytes[offset + 19])

    def on_apply_player_edits(self):
        if not hasattr(self, "player_data_bytes") or not self.player_data_bytes:
            messagebox.showwarning("Warning", "No player stats loaded.")
            return
        val = self.cmb_player_char.get()
        try:
            char_idx = int(val.split("Rec ")[1].replace(")", ""))
        except Exception:
            return
            
        rec_len = 148
        offset = 20 + char_idx * rec_len
        if offset + 20 > len(self.player_data_bytes):
            return
            
        try:
            hp = int(self.var_ply_hp.get())
            mp = int(self.var_ply_mp.get())
            
            struct.pack_into("<I", self.player_data_bytes, offset + 4, hp)
            struct.pack_into("<I", self.player_data_bytes, offset + 28, hp)
            
            struct.pack_into("<I", self.player_data_bytes, offset + 8, mp)
            struct.pack_into("<I", self.player_data_bytes, offset + 32, mp)
            
            self.player_data_bytes[offset + 12] = int(self.var_ply_str.get())
            self.player_data_bytes[offset + 13] = int(self.var_ply_def.get())
            self.player_data_bytes[offset + 14] = int(self.var_ply_mag.get())
            self.player_data_bytes[offset + 15] = int(self.var_ply_mdf.get())
            self.player_data_bytes[offset + 16] = int(self.var_ply_agi.get())
            self.player_data_bytes[offset + 17] = int(self.var_ply_lck.get())
            self.player_data_bytes[offset + 18] = int(self.var_ply_eva.get())
            self.player_data_bytes[offset + 19] = int(self.var_ply_acc.get())
            
            messagebox.showinfo("Applied", f"Applied edits for {val.split(' (')[0]} to memory cache.")
            self.log(f"Applied player edits for {val.split(' (')[0]} to memory.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply edits: {e}")

    def on_save_player_stats(self):
        if not hasattr(self, "player_data_bytes") or not self.player_data_bytes:
            messagebox.showwarning("Warning", "No player stats to save.")
            return
            
        save_paths = []
        if self.master_path:
            for root, dirs, files in os.walk(self.master_path):
                if "ply_save.bin" in files:
                    save_paths.append(os.path.join(root, "ply_save.bin"))
                    
        if not save_paths:
            messagebox.showerror("Error", "Could not locate ply_save.bin to save.")
            return
            
        success_count = 0
        for path in save_paths:
            try:
                import shutil
                bak_path = path + ".bak"
                if not os.path.exists(bak_path):
                    shutil.copy2(path, bak_path)
                    
                with open(path, "wb") as f:
                    f.write(self.player_data_bytes)
                success_count += 1
                self.log(f"Saved player stats to {path}.", "success")
            except Exception as e:
                self.log(f"Failed to save player stats to {path}: {e}", "error")
                
        messagebox.showinfo("Saved", f"Player stats saved successfully to {success_count} localization files!")

    def build_flowchart_tab(self, parent):
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill="both", expand=True)
        
        self.cvs_flowchart = tk.Canvas(canvas_frame, bg=self.bg_color, borderwidth=0, highlightthickness=0)
        self.cvs_flowchart.pack(side="left", fill="both", expand=True)
        
        flowchart_scroll_y = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.cvs_flowchart.yview)
        flowchart_scroll_y.pack(side="right", fill="y")
        flowchart_scroll_x = ttk.Scrollbar(parent, orient="horizontal", command=self.cvs_flowchart.xview)
        flowchart_scroll_x.pack(side="bottom", fill="x")
        
        self.cvs_flowchart.configure(yscrollcommand=flowchart_scroll_y.set, xscrollcommand=flowchart_scroll_x.set)
        
        def _on_flowchart_mousewheel(event):
            self.cvs_flowchart.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.cvs_flowchart.bind("<Enter>", lambda e: self.cvs_flowchart.bind_all("<MouseWheel>", _on_flowchart_mousewheel))
        self.cvs_flowchart.bind("<Leave>", lambda e: self.cvs_flowchart.unbind_all("<MouseWheel>"))

    def draw_flowchart(self):
        self.cvs_flowchart.delete("all")

        hook_title = getattr(self, "current_hook_key", "active_turn").upper()
        # Start node
        self.cvs_flowchart.create_oval(160, 10, 280, 38, fill=self.accent_color, outline=self.border_color, width=2)
        self.cvs_flowchart.create_text(220, 24, text=f"START ({hook_title})", fill="#ffffff", font=("Segoe UI", 8, "bold"))

        current_y = 38
        rules_ids = self.tree_rules.get_children()

        if not rules_ids:
            self.cvs_flowchart.create_line(220, current_y, 220, current_y + 40, arrow=tk.LAST, fill=self.text_dim, width=2)
            current_y += 40
            self.cvs_flowchart.create_oval(185, current_y, 255, current_y + 26, fill=self.btn_color_secondary, outline=self.border_color, width=2)
            self.cvs_flowchart.create_text(220, current_y + 13, text="RETURN", fill="#ffffff", font=("Segoe UI", 8, "bold"))
            self.cvs_flowchart.configure(scrollregion=(0, 0, 620, current_y + 50))
            return

        for rule_id in rules_ids:
            values = self.tree_rules.item(rule_id, "values")
            if len(values) >= 6:
                phase_str, cond, act_name, target, chance_str, state_flow = values[:6]
            else:
                phase_str = "Any"
                cond, act_name, target, chance_str = values[:4]
                state_flow = "Return"

            self.cvs_flowchart.create_line(220, current_y, 220, current_y + 28, arrow=tk.LAST, fill=self.text_dim, width=2)
            current_y += 28

            has_phase = (phase_str != "Any")
            has_cond = (cond != "Always")
            has_chance = (chance_str != "100%")

            if has_phase or has_cond or has_chance:
                points = [220, current_y, 330, current_y + 34, 220, current_y + 68, 110, current_y + 34]
                self.cvs_flowchart.create_polygon(points, fill=self.card_color, outline=self.accent_color, width=2)

                cond_lines = []
                if has_phase:
                    cond_lines.append(f"[{phase_str}]")
                if has_cond:
                    cond_lines.append(cond)
                if has_chance:
                    cond_lines.append(f"({chance_str} Chance)")
                cond_text = "\n".join(cond_lines)
                self.cvs_flowchart.create_text(220, current_y + 34, text=cond_text, fill=self.text_color, font=("Segoe UI", 8), justify="center")

                self.cvs_flowchart.create_line(330, current_y + 34, 410, current_y + 34, 410, current_y + 62, arrow=tk.LAST, fill=self.success_color, width=2)
                self.cvs_flowchart.create_text(370, current_y + 22, text="True", fill=self.success_color, font=("Segoe UI", 8, "bold"))

                self.cvs_flowchart.create_rectangle(335, current_y + 62, 505, current_y + 122, fill=self.success_color, outline=self.border_color, width=1)
                act_box_txt = f"{act_name}\nTarget: {target}\n[{state_flow}]"
                self.cvs_flowchart.create_text(420, current_y + 92, text=act_box_txt, fill="#ffffff", font=("Segoe UI", 8, "bold"), justify="center")

                self.cvs_flowchart.create_line(220, current_y + 68, 220, current_y + 142, fill=self.error_color, width=2)
                self.cvs_flowchart.create_text(200, current_y + 98, text="False", fill=self.error_color, font=("Segoe UI", 8, "bold"))

                if "Continue" in state_flow:
                    self.cvs_flowchart.create_line(420, current_y + 122, 420, current_y + 142, 220, current_y + 142, arrow=tk.LAST, fill=self.accent_color, width=2)
                else:
                    self.cvs_flowchart.create_line(505, current_y + 92, 555, current_y + 92, arrow=tk.LAST, fill=self.success_color, width=2)
                    self.cvs_flowchart.create_text(578, current_y + 92, text="RET", fill=self.success_color, font=("Segoe UI", 8, "bold"))

                current_y += 142
            else:
                self.cvs_flowchart.create_rectangle(125, current_y, 315, current_y + 58, fill=self.card_color, outline=self.accent_color, width=2)
                act_box_txt = f"{act_name}\nTarget: {target}\n[{state_flow}]"
                self.cvs_flowchart.create_text(220, current_y + 29, text=act_box_txt, fill=self.text_color, font=("Segoe UI", 8, "bold"), justify="center")
                current_y += 58

        self.cvs_flowchart.create_line(220, current_y, 220, current_y + 35, arrow=tk.LAST, fill=self.text_dim, width=2)
        current_y += 35
        self.cvs_flowchart.create_oval(185, current_y, 255, current_y + 26, fill=self.accent_color, outline=self.border_color, width=2)
        self.cvs_flowchart.create_text(220, current_y + 13, text="RETURN", fill="#ffffff", font=("Segoe UI", 8, "bold"))

        self.cvs_flowchart.configure(scrollregion=(0, 0, 620, current_y + 50))

    def setup_shortcuts(self):
        self.root.bind("<Control-s>", lambda e: self.apply_save())
        self.root.bind("<Control-S>", lambda e: self.save_all_to_disk())
        self.root.bind("<Control-f>", lambda e: (self.ent_search_mon.focus_set(), self.ent_search_mon.select_range(0, tk.END)))
        self.root.bind("<F5>", lambda e: self.scan_monsters())
        self.root.bind("<Control-d>", lambda e: self.open_stat_diff_dialog())

    def setup_syntax_highlighting(self):
        if not hasattr(self, "txt_atel"):
            return
        self.txt_atel.tag_configure("kw", foreground="#c084fc", font=("Consolas", 10, "bold"))
        self.txt_atel.tag_configure("func", foreground="#60a5fa", font=("Consolas", 10, "bold"))
        self.txt_atel.tag_configure("lbl", foreground="#38bdf8", font=("Consolas", 10, "bold"))
        self.txt_atel.tag_configure("reg", foreground="#fb923c")
        self.txt_atel.tag_configure("num", foreground="#34d399")
        self.txt_atel.tag_configure("comment", foreground="#9ca3af", font=("Consolas", 10, "italic"))
        self.txt_atel.tag_configure("str", foreground="#fde047")

    def apply_atel_syntax_highlighting(self):
        if not hasattr(self, "txt_atel"):
            return
        content = self.txt_atel.get("1.0", tk.END)
        for tag in ["kw", "func", "lbl", "reg", "num", "comment", "str"]:
            self.txt_atel.tag_remove(tag, "1.0", tk.END)
        
        import re
        patterns = [
            ("comment", r"(//.*$|#.*$)"),
            ("lbl", r"\b(w\d+_Label_\d+|w\d+_f\d+|label_\d+|Label_\d+)\b:?"),
            ("kw", r"\b(if|goto|return|halt|pass|def|case|switch|and|or|not)\b"),
            ("func", r"\b(BuildAction|ExecuteAction|ExecuteCounterAction|GetProperty|SetProperty|GetRandomValue|GetTargetMask|GetEntityStatus|SetTargetFilter|GetLastAttacker|GetLastActionId|GetPartyWithStatusMask|GetAbilityProperty|CountSetBits|RandomTargetFromMask|GetHighestStatTarget|GetLowestStatTarget|GetFirstSetBitTarget|ShowBattleDialog|PlayEffect|checkTargetStatus|checkTargetElement|targetDistToParty|wait|halt|loadModel|setPosition|setMovementSpeed|call_[0-9A-Fa-f]+)\b"),
            ("reg", r"\b(rA|rX|rY|var_[0-9A-Fa-f]+|refInts|refFloats|I\d+|F\d+)\b"),
            ("num", r"\b(0x[0-9A-Fa-f]+|-?\d+)\b"),
            ("str", r'"[^"\n]*"'),
        ]
        for tag, pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.txt_atel.tag_add(tag, start, end)

    def open_stat_diff_dialog(self):
        if not self.current_monster:
            messagebox.showwarning("Warning", "Please select a monster first.")
            return
            
        m_id = self.current_monster["id"]
        filepath = self.current_monster["path"]
        bak_path = filepath + ".bak"
        
        orig_bytes_us = None
        orig_loot = None
        if os.path.exists(bak_path):
            try:
                with open(bak_path, "rb") as f:
                    bak_data = f.read()
                bak_chunks = packer.unpack_chunks(bak_data)
                if len(bak_chunks) > 6:
                    orig_bytes_us = bak_chunks[6]
                    orig_loot = bak_chunks[4]
            except Exception as e:
                self.log(f"Error loading .bak file: {e}", "error")
                
        # Dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"📊 Stat Diff Comparison — {m_id} ({self.current_monster['name']})")
        dialog.geometry("750x600")
        dialog.minsize(650, 450)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        
        # Header
        top_f = tk.Frame(dialog, bg=self.bg_color)
        top_f.pack(fill="x", padx=15, pady=(15, 10))
        tk.Label(top_f, text=f"📊 Stat Variance Comparison: {self.current_monster['name']} ({m_id})", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 13, "bold")).pack(side="left")
        
        status_txt = "Comparing Current vs Original Backup (.bak)" if orig_bytes_us else "No .bak file found (Comparing against current values)"
        tk.Label(dialog, text=status_txt, bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 9, "italic")).pack(padx=15, anchor="w", pady=(0, 10))
        
        # Table
        tree_f = ttk.Frame(dialog)
        tree_f.pack(fill="both", expand=True, padx=15, pady=5)
        
        tree = ttk.Treeview(tree_f, columns=("Category", "Stat", "Original", "Current", "Diff", "Change"), show="headings")
        tree.heading("Category", text="Category")
        tree.heading("Stat", text="Attribute")
        tree.heading("Original", text="Original (.bak)")
        tree.heading("Current", text="Current (Modified)")
        tree.heading("Diff", text="Variance")
        tree.heading("Change", text="% Change")
        
        tree.column("Category", width=110, anchor="w")
        tree.column("Stat", width=140, anchor="w")
        tree.column("Original", width=100, anchor="center")
        tree.column("Current", width=100, anchor="center")
        tree.column("Diff", width=90, anchor="center")
        tree.column("Change", width=90, anchor="center")
        
        tree.tag_configure("buff", background="#064e3b", foreground="#6ee7b7")
        tree.tag_configure("nerf", background="#450a0a", foreground="#fca5a5")
        tree.tag_configure("neutral", foreground=self.text_color)
        
        scroll = ttk.Scrollbar(tree_f, command=tree.yview)
        scroll.pack(fill="y", side="right")
        tree.config(yscrollcommand=scroll.set)
        tree.pack(fill="both", expand=True, side="left")
        
        def get_stat_u32(block, offset):
            return struct.unpack("<I", block[offset:offset+4])[0] if block and len(block) >= offset+4 else 0
        def get_stat_u16(block, offset):
            return struct.unpack("<H", block[offset:offset+2])[0] if block and len(block) >= offset+2 else 0
        def get_stat_u8(block, offset):
            return block[offset] if block and len(block) > offset else 0

        stats_list = [
            ("Core", "HP", get_stat_u32(orig_bytes_us, 0x14) if orig_bytes_us else int(self.var_hp.get()), int(self.var_hp.get())),
            ("Core", "MP", get_stat_u32(orig_bytes_us, 0x18) if orig_bytes_us else int(self.var_mp.get()), int(self.var_mp.get())),
            ("Core", "Overkill HP", get_stat_u32(orig_bytes_us, 0x1C) if orig_bytes_us else int(self.var_overkill.get()), int(self.var_overkill.get())),
            ("Core", "Strength", get_stat_u8(orig_bytes_us, 0x20) if orig_bytes_us else int(self.var_str.get()), int(self.var_str.get())),
            ("Core", "Defense", get_stat_u8(orig_bytes_us, 0x21) if orig_bytes_us else int(self.var_def.get()), int(self.var_def.get())),
            ("Core", "Magic", get_stat_u8(orig_bytes_us, 0x22) if orig_bytes_us else int(self.var_mag.get()), int(self.var_mag.get())),
            ("Core", "Magic Defense", get_stat_u8(orig_bytes_us, 0x23) if orig_bytes_us else int(self.var_mdf.get()), int(self.var_mdf.get())),
            ("Core", "Agility", get_stat_u8(orig_bytes_us, 0x24) if orig_bytes_us else int(self.var_agi.get()), int(self.var_agi.get())),
            ("Core", "Luck", get_stat_u8(orig_bytes_us, 0x25) if orig_bytes_us else int(self.var_lck.get()), int(self.var_lck.get())),
            ("Core", "Evasion", get_stat_u8(orig_bytes_us, 0x26) if orig_bytes_us else int(self.var_eva.get()), int(self.var_eva.get())),
            ("Core", "Accuracy", get_stat_u8(orig_bytes_us, 0x27) if orig_bytes_us else int(self.var_acc.get()), int(self.var_acc.get())),
            ("Loot", "Gil", get_stat_u16(orig_loot, 0x00) if orig_loot else int(self.var_gil.get()), int(self.var_gil.get())),
            ("Loot", "AP (Normal)", get_stat_u16(orig_loot, 0x02) if orig_loot else int(self.var_ap_n.get()), int(self.var_ap_n.get())),
            ("Loot", "AP (Overkill)", get_stat_u16(orig_loot, 0x04) if orig_loot else int(self.var_ap_o.get()), int(self.var_ap_o.get())),
            ("Resistances", "Death Res", get_stat_u8(orig_bytes_us, 0x2F) if orig_bytes_us else int(self.var_res_death.get()), int(self.var_res_death.get())),
            ("Resistances", "Petrify Res", get_stat_u8(orig_bytes_us, 0x31) if orig_bytes_us else int(self.var_res_petrify.get()), int(self.var_res_petrify.get())),
            ("Resistances", "Poison Res", get_stat_u8(orig_bytes_us, 0x32) if orig_bytes_us else int(self.var_res_poison.get()), int(self.var_res_poison.get())),
            ("Resistances", "Silence Res", get_stat_u8(orig_bytes_us, 0x3C) if orig_bytes_us else int(self.var_res_silence.get()), int(self.var_res_silence.get())),
            ("Resistances", "Darkness Res", get_stat_u8(orig_bytes_us, 0x3D) if orig_bytes_us else int(self.var_res_darkness.get()), int(self.var_res_darkness.get())),
            ("Resistances", "Slow Res", get_stat_u8(orig_bytes_us, 0x47) if orig_bytes_us else int(self.var_res_slow.get()), int(self.var_res_slow.get())),
        ]
        
        for cat, name, orig, curr in stats_list:
            diff = curr - orig
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            if orig > 0 and diff != 0:
                pct = ((curr - orig) / orig) * 100.0
                pct_str = f"+{pct:.1f}%" if pct > 0 else f"{pct:.1f}%"
            elif diff != 0:
                pct_str = "N/A"
            else:
                pct_str = "-"
                
            tag = "buff" if diff > 0 else ("nerf" if diff < 0 else "neutral")
            tree.insert("", tk.END, values=(cat, name, str(orig), str(curr), diff_str, pct_str), tags=(tag,))

    def open_randomizer_dialog(self):
        import random
        dialog = tk.Toplevel(self.root)
        dialog.title("🎲 Monster Randomizer Suite")
        dialog.geometry("480x720")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        
        # Header
        lbl_h = tk.Label(dialog, text="🎲 Monster Randomizer", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 14, "bold"))
        lbl_h.pack(pady=(15, 5))
        lbl_s = tk.Label(dialog, text="Randomize monster stats, affinities, loot tables, and AI routines.", bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 9, "italic"))
        lbl_s.pack(pady=(0, 15))
        
        # Options Frame
        opt_frame = tk.LabelFrame(dialog, text=" Randomizer Options ", bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 9, "bold"), padx=15, pady=10)
        opt_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        var_rnd_stats = tk.BooleanVar(value=True)
        var_rnd_elems = tk.BooleanVar(value=True)
        var_rnd_res = tk.BooleanVar(value=True)
        var_rnd_loot = tk.BooleanVar(value=True)
        var_rnd_ai = tk.BooleanVar(value=False)
        
        tk.Checkbutton(opt_frame, text="Randomize Base Stats (HP, Str, Def, Mag, Agi)", variable=var_rnd_stats, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color).pack(anchor="w", pady=2)
        tk.Checkbutton(opt_frame, text="Randomize Elemental Affinities (Weak/Resist/Absorb)", variable=var_rnd_elems, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color).pack(anchor="w", pady=2)
        tk.Checkbutton(opt_frame, text="Randomize Status Resistances", variable=var_rnd_res, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color).pack(anchor="w", pady=2)
        tk.Checkbutton(opt_frame, text="Randomize Item Drops & Steals", variable=var_rnd_loot, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color).pack(anchor="w", pady=2)
        tk.Checkbutton(opt_frame, text="Shuffle Battle AI Actions", variable=var_rnd_ai, bg=self.bg_color, fg=self.text_color, selectcolor=self.card_color, activebackground=self.bg_color, activeforeground=self.text_color).pack(anchor="w", pady=2)
        
        # Scaling Bounds Frame
        bnd_frame = tk.LabelFrame(dialog, text=" Stat Scaling Bounds & Seed ", bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 9, "bold"), padx=15, pady=10)
        bnd_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        f1 = tk.Frame(bnd_frame, bg=self.bg_color)
        f1.pack(fill="x", pady=4)
        tk.Label(f1, text="Min Stat Multiplier:", bg=self.bg_color, fg=self.text_color).pack(side="left")
        var_min_m = tk.StringVar(value="0.7")
        ttk.Entry(f1, textvariable=var_min_m, width=8).pack(side="right")
        
        f2 = tk.Frame(bnd_frame, bg=self.bg_color)
        f2.pack(fill="x", pady=4)
        tk.Label(f2, text="Max Stat Multiplier:", bg=self.bg_color, fg=self.text_color).pack(side="left")
        var_max_m = tk.StringVar(value="1.6")
        ttk.Entry(f2, textvariable=var_max_m, width=8).pack(side="right")
        
        f3 = tk.Frame(bnd_frame, bg=self.bg_color)
        f3.pack(fill="x", pady=4)
        tk.Label(f3, text="Random Seed (optional):", bg=self.bg_color, fg=self.text_color).pack(side="left")
        var_seed = tk.StringVar(value="")
        ttk.Entry(f3, textvariable=var_seed, width=14).pack(side="right")
        
        def run_randomize():
            seed_val = var_seed.get().strip()
            if seed_val:
                try:
                    random.seed(int(seed_val))
                except ValueError:
                    random.seed(seed_val)
                    
            try:
                min_m = float(var_min_m.get())
                max_m = float(var_max_m.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid min/max multipliers.")
                return
                
            path = self.ent_master_path.get().strip()
            if not path or not os.path.exists(path):
                messagebox.showerror("Error", "Invalid master directory.")
                return
                
            mon_dir = os.path.join(path, "jppc", "battle", "mon")
            if not os.path.exists(mon_dir):
                if path.endswith(os.path.join("battle", "mon")):
                    mon_dir = path
                else:
                    messagebox.showerror("Error", "Could not find battle/mon directory.")
                    return
                    
            count = 0
            for entry_name in sorted(os.listdir(mon_dir)):
                folder_p = os.path.join(mon_dir, entry_name)
                if entry_name.startswith("_m") and os.path.isdir(folder_p):
                    m_id = entry_name[1:]
                    fpath = os.path.join(folder_p, f"{m_id}.bin")
                elif entry_name.startswith("m") and entry_name.endswith(".bin"):
                    fpath = folder_p
                else:
                    continue
                if not os.path.exists(fpath):
                    continue
                bak_path = fpath + ".bak"
                if not os.path.exists(bak_path):
                    shutil.copy2(fpath, bak_path)
                    
                with open(bak_path, "rb") as f:
                    data = f.read()
                chunks = packer.unpack_chunks(data)
                if len(chunks) < 7:
                    continue
                    
                # 1. Randomize stats (chunks 2 and 6) using authentic FFX stat offsets
                for chunk_idx in [2, 6]:
                    c = bytearray(chunks[chunk_idx])
                    if len(c) < 128:
                        continue
                    if var_rnd_stats.get():
                        hp = struct.unpack("<I", c[0x14:0x18])[0]
                        mp = struct.unpack("<I", c[0x18:0x1C])[0]
                        ok = struct.unpack("<I", c[0x1C:0x20])[0]
                        hp_m = random.uniform(min_m, max_m)
                        struct.pack_into("<I", c, 0x14, min(99999999, max(1, int(hp * hp_m))))
                        struct.pack_into("<I", c, 0x18, min(9999, max(0, int(mp * random.uniform(min_m, max_m)))))
                        struct.pack_into("<I", c, 0x1C, min(99999999, max(1, int(ok * hp_m))))
                        
                        for off in [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]:
                            val = c[off]
                            new_val = min(255, max(1, int(val * random.uniform(min_m, max_m))))
                            c[off] = new_val
                            
                    if var_rnd_elems.get():
                        # Ensure mutually exclusive elemental states across 0x2B..0x2E
                        absorb, immune, resist, weak = 0, 0, 0, 0
                        for bit in [1, 2, 4, 8, 16]:
                            st = random.choice(["Normal", "Normal", "Weak", "Resist", "Immune", "Absorb"])
                            if st == "Absorb": absorb |= bit
                            elif st == "Immune": immune |= bit
                            elif st == "Resist": resist |= bit
                            elif st == "Weak": weak |= bit
                        c[0x2B] = absorb
                        c[0x2C] = immune
                        c[0x2D] = resist
                        c[0x2E] = weak
                        
                    if var_rnd_res.get():
                        for off in [0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x46, 0x47]:
                            if off < len(c) and c[off] != 255:
                                c[off] = random.choice([0, 25, 50, 100, 254])
                            
                    chunks[chunk_idx] = bytes(c)
                    
                # 2. Randomize loot (chunk 4)
                if var_rnd_loot.get() and self.items_list:
                    l = bytearray(chunks[4])
                    if len(l) >= 0x30:
                        for off in [0x0C, 0x0E, 0x10, 0x12, 0x18, 0x1A, 0x1C, 0x1E, 0x24, 0x26]:
                            rand_item = random.choice(self.items_list)[0]
                            struct.pack_into("<H", l, off, rand_item)
                        chunks[4] = bytes(l)
                        
                new_data = packer.repack_chunks(chunks)
                packer.safe_atomic_write(fpath, new_data)
                count += 1
                
            self.monster_cache.clear()
            self.scan_monsters()
            dialog.destroy()
            messagebox.showinfo("Success", f"Randomized {count} monsters successfully!")
            
        btn_run = tk.Button(dialog, text="🎲 Run Randomizer", command=run_randomize, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground=self.accent_hover, height=2)
        btn_run.pack(fill="x", padx=30, pady=(15, 5))
        self.bind_hover(btn_run, is_primary=True)

    def open_modpack_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("📦 FFX Modpack Manager")
        dialog.geometry("400x260")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        
        tk.Label(dialog, text="📦 Modpack Manager", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))
        tk.Label(dialog, text="Export or import lightweight modpack patches (.ffxmod).", bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 9, "italic")).pack(pady=(0, 20))
        
        btn_exp = tk.Button(dialog, text="📤 Export Modpack (.ffxmod)...", command=lambda: (dialog.destroy(), self.export_modpack()), bg=self.card_color, fg=self.text_color, font=("Segoe UI", 10, "bold"), relief="flat", height=2)
        btn_exp.pack(fill="x", padx=40, pady=5)
        self.bind_hover(btn_exp)
        
        btn_imp = tk.Button(dialog, text="📥 Import & Apply Modpack...", command=lambda: (dialog.destroy(), self.import_modpack()), bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", height=2)
        btn_imp.pack(fill="x", padx=40, pady=5)
        self.bind_hover(btn_imp, is_primary=True)

    def export_modpack(self):
        f = filedialog.asksaveasfilename(defaultextension=".ffxmod", filetypes=[("FFX Modpack", "*.ffxmod"), ("JSON Files", "*.json")], title="Export FFX Modpack")
        if not f:
            return
            
        mod_data = {
            "format": "FFX-MOD-v1",
            "name": "Custom FFX Balance Mod",
            "version": "1.0",
            "monsters": {}
        }
        
        for m_id, entry in self.monster_cache.items():
            if entry.get("chunks"):
                chunks_hex = [c.hex() for c in entry["chunks"]]
                mod_data["monsters"][m_id] = {
                    "name": entry.get("us_name", m_id),
                    "chunks": chunks_hex
                }
                
        try:
            with open(f, "w") as fp:
                json.dump(mod_data, fp, indent=2)
            self.log(f"Exported modpack with {len(mod_data['monsters'])} monsters to {f}.", "success")
            messagebox.showinfo("Success", f"Modpack exported successfully ({len(mod_data['monsters'])} monsters)!")
        except Exception as e:
            self.log(f"Failed to export modpack: {e}", "error")
            messagebox.showerror("Error", f"Failed to export modpack:\n{e}")

    def import_modpack(self):
        f = filedialog.askopenfilename(filetypes=[("FFX Modpack", "*.ffxmod"), ("JSON Files", "*.json")], title="Import FFX Modpack")
        if not f or not os.path.exists(f):
            return
            
        try:
            with open(f, "r") as fp:
                mod_data = json.load(fp)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read modpack file:\n{e}")
            return
            
        monsters = mod_data.get("monsters", {})
        if not monsters:
            messagebox.showwarning("Warning", "No monster data found in this modpack.")
            return
            
        path = self.ent_master_path.get().strip()
        mon_dir = os.path.join(path, "jppc", "battle", "mon") if path else ""
        if not mon_dir or not os.path.exists(mon_dir):
            if path and path.endswith(os.path.join("battle", "mon")):
                mon_dir = path
            else:
                messagebox.showerror("Error", "Please configure a valid master folder before importing.")
                return
                
        applied = 0
        for m_id, m_info in monsters.items():
            fpath = os.path.join(mon_dir, f"_{m_id}", f"{m_id}.bin")
            if not os.path.exists(fpath):
                fpath = os.path.join(mon_dir, f"{m_id}.bin")
            if not os.path.exists(fpath):
                continue
            bak_path = fpath + ".bak"
            if not os.path.exists(bak_path):
                shutil.copy2(fpath, bak_path)
                
            chunks_hex = m_info.get("chunks", [])
            if chunks_hex:
                chunks = [bytes.fromhex(ch) for ch in chunks_hex]
                repacked = packer.repack_chunks(chunks)
                packer.safe_atomic_write(fpath, repacked)
                applied += 1
                
        self.monster_cache.clear()
        self.scan_monsters()
        self.log(f"Imported modpack '{mod_data.get('name', 'Mod')}' with {applied} monsters.", "success")
        messagebox.showinfo("Success", f"Applied modpack to {applied} monsters successfully!")

    def export_bestiary_card(self):
        if not self.current_monster:
            messagebox.showwarning("Warning", "Please select a monster first.")
            return
            
        m_id = self.current_monster["id"]
        m_name = self.current_monster["name"]
        m_zone = MONSTER_ZONE_MAP.get(m_id, "Spira Field")
        
        f = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Report", "*.html"), ("Markdown Page", "*.md")],
            title=f"Export Bestiary Card for {m_name}",
            initialfile=f"{m_id}_{m_name.replace(' ', '_')}_bestiary.html"
        )
        if not f:
            return
            
        is_html = f.endswith(".html") or f.endswith(".htm")
        
        if is_html:
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{m_name} ({m_id}) — Bestiary Card</title>
<style>
  body {{ background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; padding: 30px; margin: 0; }}
  .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; max-width: 800px; margin: 0 auto; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
  .header {{ background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 20px; color: white; }}
  .header h1 {{ margin: 0; font-size: 26px; }}
  .header .meta {{ color: #bfdbfe; font-size: 14px; margin-top: 4px; }}
  .section {{ padding: 20px; border-bottom: 1px solid #334155; }}
  .section h2 {{ color: #60a5fa; font-size: 16px; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 0.5px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; }}
  .stat-box {{ background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 10px; text-align: center; }}
  .stat-label {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; }}
  .stat-value {{ font-size: 20px; font-weight: bold; color: #38bdf8; margin-top: 2px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #334155; }}
  th {{ background: #0f172a; color: #94a3b8; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h1>{m_name}</h1>
    <div class="meta">ID: {m_id} &bull; Zone: {m_zone} &bull; Arena ID: {self.var_arena_idx.get()}</div>
  </div>
  <div class="section">
    <h2>Core Attributes</h2>
    <div class="grid">
      <div class="stat-box"><div class="stat-label">HP</div><div class="stat-value">{int(self.var_hp.get()):,}</div></div>
      <div class="stat-box"><div class="stat-label">MP</div><div class="stat-value">{int(self.var_mp.get()):,}</div></div>
      <div class="stat-box"><div class="stat-label">Overkill</div><div class="stat-value">{int(self.var_overkill.get()):,}</div></div>
      <div class="stat-box"><div class="stat-label">Strength</div><div class="stat-value">{self.var_str.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Defense</div><div class="stat-value">{self.var_def.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Magic</div><div class="stat-value">{self.var_mag.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Magic Def</div><div class="stat-value">{self.var_mdf.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Agility</div><div class="stat-value">{self.var_agi.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Luck</div><div class="stat-value">{self.var_lck.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Evasion</div><div class="stat-value">{self.var_eva.get()}</div></div>
      <div class="stat-box"><div class="stat-label">Accuracy</div><div class="stat-value">{self.var_acc.get()}</div></div>
    </div>
  </div>
  <div class="section">
    <h2>Elemental Affinities</h2>
    <table>
      <tr><th>Fire</th><th>Ice</th><th>Thunder</th><th>Water</th><th>Holy</th></tr>
      <tr>
        <td>{self.cmb_elem_fire.get()}</td>
        <td>{self.cmb_elem_ice.get()}</td>
        <td>{self.cmb_elem_thunder.get()}</td>
        <td>{self.cmb_elem_water.get()}</td>
        <td>{self.cmb_elem_holy.get()}</td>
      </tr>
    </table>
  </div>
  <div class="section">
    <h2>Rewards & Loot</h2>
    <table>
      <tr><th>Gil</th><td>{int(self.var_gil.get()):,}</td><th>Steal (Common)</th><td>{self.cmb_steal_c.get()} (x{self.var_qty_steal_c.get()})</td></tr>
      <tr><th>AP (Normal)</th><td>{int(self.var_ap_n.get()):,}</td><th>Steal (Rare)</th><td>{self.cmb_steal_r.get()} (x{self.var_qty_steal_r.get()})</td></tr>
      <tr><th>AP (Overkill)</th><td>{int(self.var_ap_o.get()):,}</td><th>Drop (Common)</th><td>{self.cmb_drop_n_p_c.get()} (x{self.var_qty_drop_n_p_c.get()})</td></tr>
      <tr><th>Bribe</th><td>{self.cmb_bribe_item.get()} (x{self.var_qty_bribe.get()})</td><th>Drop (Rare)</th><td>{self.cmb_drop_n_p_r.get()} (x{self.var_qty_drop_n_p_r.get()})</td></tr>
    </table>
  </div>
</div>
</body>
</html>"""
            with open(f, "w", encoding="utf-8") as fp:
                fp.write(html_content)
        else:
            md_content = f"""# {m_name} ({m_id})

**Zone:** {m_zone}  
**Arena Index:** {self.var_arena_idx.get()}  

## Core Attributes
| HP | MP | Overkill | Str | Def | Mag | MDef | Agi | Lck | Eva | Acc |
|---|---|---|---|---|---|---|---|---|---|---|
| {int(self.var_hp.get()):,} | {int(self.var_mp.get()):,} | {int(self.var_overkill.get()):,} | {self.var_str.get()} | {self.var_def.get()} | {self.var_mag.get()} | {self.var_mdf.get()} | {self.var_agi.get()} | {self.var_lck.get()} | {self.var_eva.get()} | {self.var_acc.get()} |

## Elemental Affinities
- **Fire:** {self.cmb_elem_fire.get()}
- **Ice:** {self.cmb_elem_ice.get()}
- **Thunder:** {self.cmb_elem_thunder.get()}
- **Water:** {self.cmb_elem_water.get()}
- **Holy:** {self.cmb_elem_holy.get()}

## Loot & Rewards
- **Gil:** {int(self.var_gil.get()):,}
- **AP:** {int(self.var_ap_n.get()):,} (Normal) / {int(self.var_ap_o.get()):,} (Overkill)
- **Steal (Common):** {self.cmb_steal_c.get()} (x{self.var_qty_steal_c.get()})
- **Steal (Rare):** {self.cmb_steal_r.get()} (x{self.var_qty_steal_r.get()})
- **Drop (Common):** {self.cmb_drop_n_p_c.get()} (x{self.var_qty_drop_n_p_c.get()})
- **Drop (Rare):** {self.cmb_drop_n_p_r.get()} (x{self.var_qty_drop_n_p_r.get()})
- **Bribe:** {self.cmb_bribe_item.get()} (x{self.var_qty_bribe.get()})
"""
            with open(f, "w", encoding="utf-8") as fp:
                fp.write(md_content)
                
        self.log(f"Exported bestiary card for {m_name} to {f}", "success")
        messagebox.showinfo("Success", f"Bestiary card exported successfully to:\n{f}")

    def build_encounters_tab(self, parent):
        paned = ttk.Panedwindow(parent, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        # Left Panel: Active Monster Formations & Spawns
        left_frame = ttk.LabelFrame(paned, text=" 📍 Active Monster Spawns & Battle Formations ", padding=10)
        paned.add(left_frame, weight=3)
        
        self.lbl_enc_active_title = ttk.Label(left_frame, text="No Monster Selected", font=("Segoe UI", 11, "bold"), foreground=self.accent_color)
        self.lbl_enc_active_title.pack(anchor="w", pady=(0, 2))
        
        self.lbl_enc_active_zone = ttk.Label(left_frame, text="Zone: -", font=("Segoe UI", 9, "italic"), foreground=self.text_dim)
        self.lbl_enc_active_zone.pack(anchor="w", pady=(0, 10))
        
        # Scrollable container for active monster formations
        cvs_active = tk.Canvas(left_frame, borderwidth=0, highlightthickness=0, bg=self.bg_color)
        sb_active = ttk.Scrollbar(left_frame, orient="vertical", command=cvs_active.yview)
        self.frame_enc_active = ttk.Frame(cvs_active)
        
        self.frame_enc_active.bind("<Configure>", lambda e: cvs_active.configure(scrollregion=cvs_active.bbox("all")))
        cvs_active.create_window((0, 0), window=self.frame_enc_active, anchor="nw")
        cvs_active.configure(yscrollcommand=sb_active.set)
        
        cvs_active.pack(side="left", fill="both", expand=True)
        sb_active.pack(side="right", fill="y")
        
        def _on_enc_wheel(event):
            cvs_active.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.frame_enc_active.bind("<Enter>", lambda e: cvs_active.bind_all("<MouseWheel>", _on_enc_wheel))
        self.frame_enc_active.bind("<Leave>", lambda e: cvs_active.unbind_all("<MouseWheel>"))
        
        # Right Panel: Spira World Map Encounter Explorer
        right_frame = ttk.LabelFrame(paned, text=" 🌍 Spira World Encounter Explorer ", padding=10)
        paned.add(right_frame, weight=4)
        
        top_bar = ttk.Frame(right_frame)
        top_bar.pack(fill="x", pady=(0, 8))
        
        ttk.Label(top_bar, text="Region:").pack(side="left", padx=(0, 5))
        self.cmb_enc_world_zone = ttk.Combobox(top_bar, values=["All Zones"] + self.encounter_parser.get_all_zones(), state="readonly", width=20)
        self.cmb_enc_world_zone.set("All Zones")
        self.cmb_enc_world_zone.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.cmb_enc_world_zone.bind("<<ComboboxSelected>>", self.refresh_world_encounters)
        
        ttk.Label(top_bar, text="🔍 Search:").pack(side="left", padx=(0, 5))
        self.ent_enc_world_search = ttk.Entry(top_bar, width=14)
        self.ent_enc_world_search.pack(side="left")
        self.ent_enc_world_search.bind("<KeyRelease>", self.refresh_world_encounters)
        
        # Treeview for World Encounters
        tree_f = ttk.Frame(right_frame)
        tree_f.pack(fill="both", expand=True)
        
        self.tree_world_enc = ttk.Treeview(tree_f, columns=("SubArea", "Formation", "Rate", "Ambush"), show="headings", selectmode="browse")
        self.tree_world_enc.heading("SubArea", text="Sub-Area")
        self.tree_world_enc.heading("Formation", text="Formation Party")
        self.tree_world_enc.heading("Rate", text="Spawn Rate")
        self.tree_world_enc.heading("Ambush", text="Ambush")
        
        self.tree_world_enc.column("SubArea", width=130, anchor="w")
        self.tree_world_enc.column("Formation", width=220, anchor="w")
        self.tree_world_enc.column("Rate", width=75, anchor="center")
        self.tree_world_enc.column("Ambush", width=70, anchor="center")
        
        self.tree_world_enc.pack(fill="both", expand=True, side="left")
        sb_world = ttk.Scrollbar(tree_f, command=self.tree_world_enc.yview)
        sb_world.pack(fill="y", side="right")
        self.tree_world_enc.config(yscrollcommand=sb_world.set)
        
        # Bottom Action Bar
        btn_bar = ttk.Frame(right_frame)
        btn_bar.pack(fill="x", pady=(8, 0))
        
        btn_load_sel = tk.Button(btn_bar, text="🔍 Load First Monster in Formation", command=self.on_load_formation_monster, bg=self.accent_color, fg="white", font=("Segoe UI", 9, "bold"), relief="flat", activebackground=self.accent_hover)
        btn_load_sel.pack(side="right")
        self.bind_hover(btn_load_sel, is_primary=True)
        
        self.refresh_world_encounters()

    def populate_encounters_view(self):
        if not hasattr(self, "frame_enc_active"):
            return
            
        for widget in self.frame_enc_active.winfo_children():
            widget.destroy()
            
        if not self.current_monster:
            self.lbl_enc_active_title.config(text="No Monster Selected")
            self.lbl_enc_active_zone.config(text="Zone: -")
            return
            
        m_id = self.current_monster["id"]
        m_name = self.current_monster["name"]
        m_zone = MONSTER_ZONE_MAP.get(m_id, "Spira Field")
        
        self.lbl_enc_active_title.config(text=f"📍 {m_name} ({m_id})")
        self.lbl_enc_active_zone.config(text=f"Primary Zone: {m_zone}")
        
        encounters = self.encounter_parser.get_monster_encounters(m_id)
        if not encounters:
            lbl = tk.Label(self.frame_enc_active, text="No specific random encounter table mapped for this monster.\n(May be a story boss, event cutscene battle, or special trigger).", bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 9, "italic"), justify="left")
            lbl.pack(anchor="w", padx=5, pady=10)
            return
            
        for enc in encounters:
            card = tk.LabelFrame(self.frame_enc_active, text=f" {enc['zone']} — {enc['sub_area']} ", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 9, "bold"), padx=10, pady=8)
            card.pack(fill="x", expand=True, pady=(0, 10))
            
            form = enc["formation"]
            rate_txt = f"Spawn Rate: {form.get('rate', 'Normal')}  |  Ambush Rate: {form.get('ambush', '0%')}"
            tk.Label(card, text=rate_txt, bg=self.bg_color, fg=self.text_dim, font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(0, 6))
            
            p_frame = tk.Frame(card, bg=self.bg_color)
            p_frame.pack(fill="x")
            
            for m_entry in form["monsters"]:
                comp_id, comp_name = m_entry
                is_current = (comp_id == m_id)
                btn_bg = self.accent_color if is_current else self.card_color
                btn_fg = "#ffffff" if is_current else self.text_color
                
                b = tk.Button(
                    p_frame,
                    text=f"👾 {comp_name} ({comp_id})" + (" [Active]" if is_current else ""),
                    command=lambda mid=comp_id: self.select_and_load_monster(mid),
                    bg=btn_bg, fg=btn_fg, font=("Segoe UI", 8, "bold" if is_current else "normal"),
                    relief="flat", padx=6, pady=2
                )
                b.pack(side="left", padx=(0, 5), pady=2)
                if not is_current:
                    self.bind_hover(b)

    def refresh_world_encounters(self, event=None):
        if not hasattr(self, "tree_world_enc"):
            return
            
        self.tree_world_enc.delete(*self.tree_world_enc.get_children())
        zone = self.cmb_enc_world_zone.get()
        query = self.ent_enc_world_search.get().strip().lower()
        
        all_zones = self.encounter_parser.get_zone_formations(zone)
        
        for area_entry in all_zones:
            sub_area = area_entry["sub_area"]
            for form in area_entry["formations"]:
                m_names = [f"{m[1]} ({m[0]})" for m in form["monsters"]]
                form_str = " + ".join(m_names)
                rate = form.get("rate", "Normal")
                ambush = form.get("ambush", "0%")
                
                # Check filter
                if query and (query not in sub_area.lower() and query not in form_str.lower() and query not in area_entry["zone"].lower()):
                    continue
                    
                first_m_id = form["monsters"][0][0] if form["monsters"] else ""
                self.tree_world_enc.insert(
                    "", tk.END,
                    values=(sub_area, form_str, rate, ambush),
                    tags=(first_m_id,)
                )

    def on_load_formation_monster(self):
        sel = self.tree_world_enc.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a formation row first.")
            return
        tags = self.tree_world_enc.item(sel[0], "tags")
        if tags and tags[0]:
            self.select_and_load_monster(tags[0])

    def select_and_load_monster(self, monster_id):
        m = next((x for x in self.monsters_list if x["id"] == monster_id), None)
        if not m:
            messagebox.showinfo("Info", f"Monster {monster_id} is not currently present in the scanned directory.")
            return
        self.tree_monsters.selection_set(monster_id)
        self.tree_monsters.see(monster_id)
        self.load_monster_file(monster_id)

    def on_atel_notebook_tab_changed(self, event=None):
        try:
            tab_idx = self.notebook.index("current")
            tab_text = self.notebook.tab(tab_idx, "text")
            if "Flowchart" in tab_text:
                self.draw_flowchart()
            elif "Encounters" in tab_text:
                self.populate_encounters_view()
        except Exception:
            pass

def main():
    root = tk.Tk()
    # High DPI scaling support on Windows
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = FFXAIToolGUI(root, is_embedded=False)
    root.mainloop()

if __name__ == "__main__":
    main()
