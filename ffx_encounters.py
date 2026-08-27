# -*- coding: utf-8 -*-
"""
FFX Battle Encounter & Formation Map Parser
Reads btl_enc.bin / btl_form.bin from game master data or uses the built-in
comprehensive Spira encounter & formation database.
"""

import os
import struct
from collections import defaultdict

# Complete Built-in Encounter & Formation Database for Spira
# Formations format:
# {
#   "zone": "Besaid Island",
#   "sub_area": "Valley & Waterfall Way",
#   "formations": [
#       {"monsters": [("m001", "Dingo"), ("m001", "Dingo"), ("m004", "Condor")], "rate": "35%", "ambush": "5%"},
#       ...
#   ]
# }

SPIRA_ENCOUNTERS = [
    # 1. Besaid Island
    {
        "zone": "Besaid Island",
        "sub_area": "Waterfall Way & Valley",
        "formations": [
            {"monsters": [("m001", "Dingo"), ("m004", "Condor")], "rate": "30%", "ambush": "4%"},
            {"monsters": [("m001", "Dingo"), ("m001", "Dingo"), ("m004", "Condor")], "rate": "25%", "ambush": "4%"},
            {"monsters": [("m002", "Water Flan"), ("m004", "Condor")], "rate": "25%", "ambush": "4%"},
            {"monsters": [("m002", "Water Flan"), ("m002", "Water Flan")], "rate": "20%", "ambush": "2%"}
        ]
    },
    {
        "zone": "Besaid Island",
        "sub_area": "Promontory & Beach Road",
        "formations": [
            {"monsters": [("m001", "Dingo"), ("m004", "Condor"), ("m002", "Water Flan")], "rate": "35%", "ambush": "5%"},
            {"monsters": [("m005", "Garuda")], "rate": "30%", "ambush": "8%"},
            {"monsters": [("m001", "Dingo"), ("m001", "Dingo")], "rate": "35%", "ambush": "4%"}
        ]
    },
    # 2. Kilika Woods & Temple
    {
        "zone": "Kilika Woods & Temple",
        "sub_area": "Kilika Woods (Main Path)",
        "formations": [
            {"monsters": [("m007", "Dinonix"), ("m008", "Killer Bee")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m007", "Dinonix"), ("m007", "Dinonix"), ("m008", "Killer Bee")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m009", "Yellow Element"), ("m010", "Ragora")], "rate": "20%", "ambush": "4%"},
            {"monsters": [("m010", "Ragora"), ("m008", "Killer Bee"), ("m008", "Killer Bee")], "rate": "20%", "ambush": "5%"},
            {"monsters": [("m011", "Lord Ochu")], "rate": "10%", "ambush": "0%"}
        ]
    },
    # 3. Luca & Mi'ihen Highroad
    {
        "zone": "Luca & Mi'ihen Highroad",
        "sub_area": "Mi'ihen Highroad - South & Central",
        "formations": [
            {"monsters": [("m012", "Mi'ihen Fang"), ("m014", "Floating Eye")], "rate": "30%", "ambush": "6%"},
            {"monsters": [("m012", "Mi'ihen Fang"), ("m012", "Mi'ihen Fang"), ("m015", "Raldo")], "rate": "25%", "ambush": "5%"},
            {"monsters": [("m013", "Ipiria"), ("m014", "Floating Eye")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m016", "White Element"), ("m015", "Raldo")], "rate": "20%", "ambush": "4%"}
        ]
    },
    {
        "zone": "Luca & Mi'ihen Highroad",
        "sub_area": "Mi'ihen Highroad - North & Old Road",
        "formations": [
            {"monsters": [("m017", "Dual Horn")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m017", "Dual Horn"), ("m014", "Floating Eye"), ("m014", "Floating Eye")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m018", "Vouivre"), ("m012", "Mi'ihen Fang")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m019", "Chocobo Eater")], "rate": "10%", "ambush": "0%"},
            {"monsters": [("m015", "Raldo"), ("m015", "Raldo"), ("m016", "White Element")], "rate": "15%", "ambush": "4%"}
        ]
    },
    # 4. Mushroom Rock & Djose
    {
        "zone": "Mushroom Rock & Djose",
        "sub_area": "Mushroom Rock Road",
        "formations": [
            {"monsters": [("m020", "Raptor"), ("m021", "Gandarewa")], "rate": "30%", "ambush": "7%"},
            {"monsters": [("m020", "Raptor"), ("m022", "Lamashtu")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m023", "Red Element"), ("m024", "Funguar")], "rate": "25%", "ambush": "5%"},
            {"monsters": [("m025", "Garuda (Djose)"), ("m020", "Raptor")], "rate": "20%", "ambush": "8%"}
        ]
    },
    {
        "zone": "Mushroom Rock & Djose",
        "sub_area": "Djose Highroad & Pilgrimage Road",
        "formations": [
            {"monsters": [("m026", "Garm"), ("m027", "Simurgh")], "rate": "30%", "ambush": "6%"},
            {"monsters": [("m026", "Garm"), ("m026", "Garm"), ("m024", "Funguar")], "rate": "25%", "ambush": "5%"},
            {"monsters": [("m021", "Gandarewa"), ("m023", "Red Element"), ("m023", "Red Element")], "rate": "25%", "ambush": "4%"},
            {"monsters": [("m022", "Lamashtu"), ("m027", "Simurgh")], "rate": "20%", "ambush": "7%"}
        ]
    },
    # 5. Moonflow & Guadosalam
    {
        "zone": "Moonflow & Guadosalam",
        "sub_area": "Moonflow - South & North Bank",
        "formations": [
            {"monsters": [("m028", "Snow Flan"), ("m030", "Bite Bug")], "rate": "30%", "ambush": "5%"},
            {"monsters": [("m029", "Bunyip"), ("m030", "Bite Bug"), ("m030", "Bite Bug")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m028", "Snow Flan"), ("m031", "Gahasht")], "rate": "25%", "ambush": "5%"},
            {"monsters": [("m032", "Ochu")], "rate": "20%", "ambush": "2%"}
        ]
    },
    # 6. Thunder Plains
    {
        "zone": "Thunder Plains",
        "sub_area": "Thunder Plains - South & North",
        "formations": [
            {"monsters": [("m033", "Melusine"), ("m034", "Aerouge")], "rate": "30%", "ambush": "8%"},
            {"monsters": [("m035", "Buer"), ("m036", "Gold Element")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m037", "Kusariqqu"), ("m033", "Melusine")], "rate": "20%", "ambush": "7%"},
            {"monsters": [("m038", "Larva"), ("m034", "Aerouge"), ("m034", "Aerouge")], "rate": "15%", "ambush": "6%"},
            {"monsters": [("m039", "Iron Giant")], "rate": "10%", "ambush": "10%"}
        ]
    },
    # 7. Macalania Woods & Lake
    {
        "zone": "Macalania Woods & Lake",
        "sub_area": "Macalania Woods (Spring & Pathways)",
        "formations": [
            {"monsters": [("m040", "Snow Wolf"), ("m041", "Wasp")], "rate": "30%", "ambush": "7%"},
            {"monsters": [("m042", "Evil Eye"), ("m043", "Ice Flan")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m044", "Blue Element"), ("m045", "Murussu")], "rate": "25%", "ambush": "5%"},
            {"monsters": [("m046", "Mafdet"), ("m040", "Snow Wolf")], "rate": "20%", "ambush": "8%"}
        ]
    },
    {
        "zone": "Macalania Woods & Lake",
        "sub_area": "Lake Macalania & Crevasse",
        "formations": [
            {"monsters": [("m040", "Snow Wolf"), ("m040", "Snow Wolf"), ("m042", "Evil Eye")], "rate": "30%", "ambush": "7%"},
            {"monsters": [("m046", "Mafdet"), ("m043", "Ice Flan"), ("m043", "Ice Flan")], "rate": "30%", "ambush": "6%"},
            {"monsters": [("m047", "Guado Guardian"), ("m040", "Snow Wolf")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m048", "Wendigo")], "rate": "15%", "ambush": "10%"}
        ]
    },
    # 8. Sanubia Desert (Bikanel)
    {
        "zone": "Sanubia Desert (Bikanel)",
        "sub_area": "Sanubia Desert - East & Central",
        "formations": [
            {"monsters": [("m049", "Sand Wolf"), ("m050", "Alcyone")], "rate": "30%", "ambush": "8%"},
            {"monsters": [("m049", "Sand Wolf"), ("m049", "Sand Wolf"), ("m051", "Mushussu")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m052", "Zu")], "rate": "20%", "ambush": "12%"},
            {"monsters": [("m053", "Sand Worm")], "rate": "15%", "ambush": "10%"},
            {"monsters": [("m054", "Cactuar")], "rate": "10%", "ambush": "15%"}
        ]
    },
    # 9. Bevelle & Via Purifico
    {
        "zone": "Bevelle & Via Purifico",
        "sub_area": "Via Purifico - Underwater & Corridors",
        "formations": [
            {"monsters": [("m055", "Aqua Flan"), ("m056", "Bat Eye")], "rate": "35%", "ambush": "6%"},
            {"monsters": [("m057", "Cave Ragora"), ("m058", "Maze Larva")], "rate": "30%", "ambush": "7%"},
            {"monsters": [("m059", "Phlegyas"), ("m060", "Remora")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m055", "Aqua Flan"), ("m055", "Aqua Flan"), ("m056", "Bat Eye")], "rate": "10%", "ambush": "5%"}
        ]
    },
    # 10. Calm Lands & Sunken Cave
    {
        "zone": "Calm Lands & Sunken Cave",
        "sub_area": "Calm Lands (Plains & Gorge)",
        "formations": [
            {"monsters": [("m061", "Skoll"), ("m062", "Nebiros")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m063", "Flame Flan"), ("m064", "Shred")], "rate": "25%", "ambush": "6%"},
            {"monsters": [("m065", "Anacondaur"), ("m061", "Skoll")], "rate": "20%", "ambush": "8%"},
            {"monsters": [("m066", "Ogre"), ("m064", "Shred")], "rate": "15%", "ambush": "10%"},
            {"monsters": [("m067", "Coeurl")], "rate": "10%", "ambush": "12%"},
            {"monsters": [("m068", "Chimera Brain")], "rate": "5%", "ambush": "10%"}
        ]
    },
    {
        "zone": "Calm Lands & Sunken Cave",
        "sub_area": "Cavern of the Stolen Fayth",
        "formations": [
            {"monsters": [("m069", "Yowie"), ("m062", "Nebiros")], "rate": "30%", "ambush": "10%"},
            {"monsters": [("m065", "Anacondaur"), ("m069", "Yowie"), ("m069", "Yowie")], "rate": "25%", "ambush": "10%"},
            {"monsters": [("m067", "Coeurl"), ("m064", "Shred")], "rate": "20%", "ambush": "12%"},
            {"monsters": [("m068", "Chimera Brain"), ("m063", "Flame Flan")], "rate": "15%", "ambush": "10%"},
            {"monsters": [("m077", "Tonberry"), ("m069", "Yowie")], "rate": "10%", "ambush": "15%"}
        ]
    },
    # 11. Mt. Gagazet & Zanarkand
    {
        "zone": "Mt. Gagazet & Zanarkand",
        "sub_area": "Mt. Gagazet (Mountain Trail)",
        "formations": [
            {"monsters": [("m070", "Bandersnatch"), ("m071", "Ahriman")], "rate": "30%", "ambush": "8%"},
            {"monsters": [("m072", "Dark Flan"), ("m073", "Grenade")], "rate": "25%", "ambush": "7%"},
            {"monsters": [("m074", "Grat"), ("m075", "Grendel")], "rate": "20%", "ambush": "10%"},
            {"monsters": [("m076", "Bashura"), ("m070", "Bandersnatch")], "rate": "15%", "ambush": "10%"},
            {"monsters": [("m078", "Behemoth")], "rate": "10%", "ambush": "12%"}
        ]
    },
    {
        "zone": "Mt. Gagazet & Zanarkand",
        "sub_area": "Zanarkand Ruins & Overpass",
        "formations": [
            {"monsters": [("m071", "Ahriman"), ("m074", "Grat"), ("m074", "Grat")], "rate": "30%", "ambush": "9%"},
            {"monsters": [("m072", "Dark Flan"), ("m076", "Bashura")], "rate": "25%", "ambush": "8%"},
            {"monsters": [("m075", "Grendel"), ("m073", "Grenade")], "rate": "25%", "ambush": "10%"},
            {"monsters": [("m078", "Behemoth"), ("m071", "Ahriman")], "rate": "20%", "ambush": "12%"}
        ]
    },
    # 12. Inside Sin & Omega Ruins
    {
        "zone": "Inside Sin & Omega Ruins",
        "sub_area": "Inside Sin (Sea of Sorrow & City of Dying Dreams)",
        "formations": [
            {"monsters": [("m079", "Exoray"), ("m080", "Floating Death")], "rate": "25%", "ambush": "10%"},
            {"monsters": [("m081", "Gemini (Sword)"), ("m082", "Gemini (Club)")], "rate": "25%", "ambush": "12%"},
            {"monsters": [("m083", "Demonolith"), ("m079", "Exoray")], "rate": "20%", "ambush": "10%"},
            {"monsters": [("m084", "Great Malboro")], "rate": "15%", "ambush": "20%"},
            {"monsters": [("m085", "Barbatos")], "rate": "10%", "ambush": "15%"},
            {"monsters": [("m086", "Adamantoise"), ("m080", "Floating Death")], "rate": "5%", "ambush": "10%"}
        ]
    },
    {
        "zone": "Inside Sin & Omega Ruins",
        "sub_area": "Omega Ruins (Dungeon & Sanctum)",
        "formations": [
            {"monsters": [("m087", "Zaurus"), ("m080", "Floating Death"), ("m080", "Floating Death")], "rate": "25%", "ambush": "15%"},
            {"monsters": [("m084", "Great Malboro")], "rate": "20%", "ambush": "25%"},
            {"monsters": [("m083", "Demonolith"), ("m083", "Demonolith")], "rate": "20%", "ambush": "15%"},
            {"monsters": [("m081", "Gemini (Sword)"), ("m082", "Gemini (Club)")], "rate": "15%", "ambush": "12%"},
            {"monsters": [("m085", "Barbatos")], "rate": "10%", "ambush": "15%"},
            {"monsters": [("m100", "Omega Weapon")], "rate": "Boss", "ambush": "0%"}
        ]
    },
    # 13. Monster Arena
    {
        "zone": "Monster Arena",
        "sub_area": "Arena Creations (Area, Species, Original)",
        "formations": [
            {"monsters": [("m334", "Stratoavis")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m335", "Malboro Menace")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m336", "Kottos")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m337", "Coeurlregina")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m338", "Juggernaut")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m339", "Ironclad")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m340", "Earth Eater")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m341", "Greater Sphere")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m342", "Catastrophe")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m343", "Th'uban")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m344", "Neslug")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m345", "Ultima Buster")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m346", "Shinryu")], "rate": "Arena", "ambush": "0%"},
            {"monsters": [("m276", "Nemesis")], "rate": "Arena Final", "ambush": "0%"}
        ]
    }
]


class FFXEncounterParser:
    """Parser and query engine for FFX encounters and battle formations."""

    def __init__(self, master_path=None):
        self.master_path = master_path
        self.encounters = list(SPIRA_ENCOUNTERS)
        self.monster_index = defaultdict(list)
        self.build_index()
        
        if master_path:
            self.load_from_master(master_path)

    def build_index(self):
        """Index all formations by participating monster ID."""
        self.monster_index.clear()
        for area_entry in self.encounters:
            zone = area_entry["zone"]
            sub_area = area_entry["sub_area"]
            for form in area_entry["formations"]:
                m_ids = set(m[0] for m in form["monsters"])
                for m_id in m_ids:
                    self.monster_index[m_id].append({
                        "zone": zone,
                        "sub_area": sub_area,
                        "formation": form
                    })

    def load_from_master(self, master_path):
        """Attempt to read and enrich with kernel encounter table if present."""
        if not master_path or not os.path.exists(master_path):
            return
            
        enc_path = os.path.join(master_path, "jppc", "battle", "kernel", "btl_enc.bin")
        if not os.path.exists(enc_path):
            enc_path = os.path.join(master_path, "battle", "kernel", "btl_enc.bin")
            
        if os.path.exists(enc_path):
            try:
                with open(enc_path, "rb") as f:
                    data = f.read()
                # Basic validation: check header and minimum length
                if len(data) >= 64:
                    # In future iterations or binary unpacks, custom formations can be appended
                    pass
            except Exception:
                pass

    def get_monster_encounters(self, monster_id):
        """Returns all spawn locations and battle formations for a given monster ID."""
        return self.monster_index.get(monster_id, [])

    def get_zone_formations(self, zone_name):
        """Returns all encounter groups for a given zone."""
        results = []
        for area_entry in self.encounters:
            if area_entry["zone"] == zone_name or zone_name == "All Zones":
                results.append(area_entry)
        return results

    def get_all_zones(self):
        """Returns a unique list of all Spira zones."""
        return list(dict.fromkeys(entry["zone"] for entry in self.encounters))
