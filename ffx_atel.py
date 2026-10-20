import struct
try:
    from ffx_ability_db import FFX_MASTER_ABILITIES
except ImportError:
    FFX_MASTER_ABILITIES = {}

GENERIC_ACTION_FLAGS = {16384, 16538, 16400}

# FFX Atel Opcodes Mapping
OPCODE_MAP = {
    0x00: "NOP",
    0x01: "OPLOR",     # Logical OR
    0x02: "OPLAND",    # Logical AND
    0x03: "OPOR",      # Bitwise OR
    0x04: "OPEOR",     # Bitwise XOR
    0x05: "OPAND",     # Bitwise AND
    0x06: "OPEQ",      # Equal
    0x07: "OPNE",      # Not Equal
    0x08: "OPGTU",     # Greater than (unsigned)
    0x09: "OPLSU",     # Less than (unsigned)
    0x0A: "OPGT",      # Greater than
    0x0B: "OPLS",      # Less than
    0x0C: "OPGTEU",    # Greater or equal (unsigned)
    0x0D: "OPLSEU",    # Less or equal (unsigned)
    0x0E: "OPGTE",     # Greater or equal
    0x0F: "OPLSE",     # Less or equal
    0x10: "OPBON",     # Turn bit ON
    0x11: "OPBOFF",    # Turn bit OFF
    0x12: "OPSLL",     # Shift left logical
    0x13: "OPSRL",     # Shift right logical
    0x14: "OPADD",     # Add
    0x15: "OPSUB",     # Subtract
    0x16: "OPMUL",     # Multiply
    0x17: "OPDIV",     # Divide
    0x18: "OPMOD",     # Modulo
    0x19: "OPNOT",     # Logical NOT
    0x1B: "OPFIXADRS",
    0x1C: "OPBNOT",    # Bitwise NOT
    0x1D: "LABEL",
    0x1E: "TAG",
    0x25: "POPA",      # Set LastCallResult (rA)
    0x26: "PUSHA",     # Get LastCallResult (rA)
    0x28: "PUSHX",     # Get test (rX)
    0x29: "PUSHY",     # case (Get rY)
    0x2A: "POPX",      # Set test (rX)
    0x2B: "REPUSH",    # Clone / duplicate stack top
    0x2C: "POPY",      # switch (Set rY)
    0x34: "RTS",       # Return from subroutine
    0x36: "REQ",       # Run worker asynchronously
    0x37: "REQSW",     # Run worker and await start
    0x38: "REQEW",     # Run worker and await end
    0x39: "PREQ",      # Run party member asynchronously
    0x3A: "PREQSW",    # Run party member and await start
    0x3B: "PREQEW",    # Run party member and await end
    0x3C: "RET",       # Return
    0x3D: "RETN",      # Return with cleanup
    0x3E: "RETT",      # Return to main
    0x3F: "RETTN",     # Return with cleanup to main
    0x40: "HALT",      # Halt
    0x41: "PUSHN",
    0x42: "PUSHT",
    0x43: "PUSHVP",
    0x44: "PUSHFIX",
    0x45: "FREQ",
    0x46: "TREQ",
    0x47: "BREQ",
    0x48: "BFREQ",
    0x49: "BTREQ",
    0x4A: "FREQSW",
    0x4B: "TREQSW",
    0x4C: "BREQSW",
    0x4D: "BFREQSW",
    0x4E: "BTREQSW",
    0x4F: "FREQEW",
    0x50: "TREQEW",
    0x51: "BREQEW",
    0x52: "BFREQEW",
    0x53: "BTREQEW",
    0x54: "DRET",      # Direct return
    0x59: "POPI0",     # Set I0
    0x5A: "POPI1",     # Set I1
    0x5B: "POPI2",     # Set I2
    0x5C: "POPI3",     # Set I3
    0x5D: "POPF0",     # Set F0
    0x5E: "POPF1",     # Set F1
    0x5F: "POPF2",     # Set F2
    0x60: "POPF3",     # Set F3
    0x61: "POPF4",     # Set F4
    0x62: "POPF5",     # Set F5
    0x63: "POPF6",     # Set F6
    0x64: "POPF7",     # Set F7
    0x65: "POPF8",     # Set F8
    0x66: "POPF9",     # Set F9
    0x67: "PUSHI0",    # Get I0
    0x68: "PUSHI1",    # Get I1
    0x69: "PUSHI2",    # Get I2
    0x6A: "PUSHI3",    # Get I3
    0x6B: "PUSHF0",    # Get F0
    0x6C: "PUSHF1",    # Get F1
    0x6D: "PUSHF2",    # Get F2
    0x6E: "PUSHF3",    # Get F3
    0x6F: "PUSHF4",    # Get F4
    0x70: "PUSHF5",    # Get F5
    0x71: "PUSHF6",    # Get F6
    0x72: "PUSHF7",    # Get F7
    0x73: "PUSHF8",    # Get F8
    0x74: "PUSHF9",    # Get F9
    0x75: "PUSHAINTER",
    0x77: "REQWAIT",   # await script
    0x78: "PREQWAIT",  # await party member script
    0x79: "REQCHG",    # Change interaction script
    0x7A: "ACTREQ",
    0x9F: "PUSHV",     # Get variable
    0xA0: "POPV",      # Set variable
    0xA1: "POPVL",     # Set variable (limited)
    0xA2: "PUSHAR",    # Get array item
    0xA3: "POPAR",     # Set array item
    0xA4: "POPARL",    # Set array item (limited)
    0xA7: "PUSHARP",   # Get array pointer
    0xAD: "PUSHI",     # Direct value (int32)
    0xAE: "PUSHII",    # Direct value (int16)
    0xAF: "PUSHF",     # Direct value (float)
    0xB0: "JMP",       # Jump always
    0xB1: "CJMP",      # Jump if last test true
    0xB2: "NCJMP",     # Jump if last test false
    0xB3: "JSR",       # Jump to subroutine (worker)
    0xB5: "CALL",      # Call function
    0xD5: "POPXJMP",   # Check and always jump
    0xD6: "POPXCJMP",  # Check and jump if true
    0xD7: "POPXNCJMP", # Check and jump if false
    0xD8: "CALLPOPA",  # Call function and pop result to rA
    0xF6: "SYSTEM",    # System call marker
}

# Common FFX Library Functions Mapping
CALL_TARGET_MAP = {
    0x0000: "wait(frames)",
    0x0001: "loadModel(model)",
    0x0002: "attachToCamera(ID, int, unused)",
    0x0004: "attachToMapGroup(groupIndex)",
    0x0005: "unloadActor()",
    0x0010: "getEntranceIndex()",
    0x0011: "transitionToRoom(room, spawnpoint)",
    0x0013: "setPosition(x, y, z)",
    0x0015: "setDestination(x, y, z)",
    0x0016: "setMovementSpeed(speed)",
    0x0018: "startMotion(activeBits, flags, targetWorker)",
    0x0019: "startRotation(activeBits, flags, targetWorker)",
    0x001A: "waitForMotion()",
    0x001B: "waitForRotation()",
    0x0033: "getWorkerIndex(workerOrSelf)",
    0x0034: "enableFieldInteraction(type)",
    0x0035: "disableFieldInteraction(type)",
    0x0036: "stopMotion(worker)",
    0x0038: "getWorkerX(worker)",
    0x0039: "getWorkerY(worker)",
    0x003A: "getWorkerZ(worker)",
    0x0042: "linkWorkerToChr(btlChr)",
    0x0043: "setWorkerAsPlayer()",
    0x0046: "HeldButtonsBitfield()",
    0x005D: "enablePlayerControl()",
    0x005E: "disablePlayerControl()",
    0x005F: "halt()",
    0x0064: "displayFieldString(msgWindow, string)",
    0x0065: "positionMessage(msgWindow, x, y, align)",
    0x006B: "closeMessage(msgWindow)",
    0x006C: "setMovementSpeed2(speed)",
    0x0076: "getWorkerType()",
    0x007C: "waitForText(msgWindow)",
    0x0084: "waitForTextEx(msgWindow, param2)",
    0x0085: "setTouchRadius(radius)",
    0x0086: "CurrentMap()",
    0x0087: "CurrentRoom()",
    0x0090: "getYaw()",
    0x0092: "getWorkerYaw(worker)",
    0x0094: "setGravity(g)",
    0x0095: "setRotationYaw(angle)",
    0x0096: "setRotationPitch(angle)",
    0x00A3: "getWorkerPosition(worker, xDest, yDest, zDest)",
    0x00A4: "workerDist(workerA, workerB)",
    0x00A6: "GetRandomInRange(maxExclusive)",
    0x00A7: "deactivate(worker)",
    0x00A8: "activate(worker)",
    0x00A9: "GetRandomValue()",
    0x00AA: "SetRandomEncountersActive(active)",
    0x00CB: "removePartyMember(playerChar)",
    0x00CF: "saveMotion(motion)",
    0x00D0: "SavedMotion()",
    0x00D5: "playFieldVoiceLine(voiceFile)",
    0x00DF: "playSfx(sfx)",
    0x00E7: "putPartyMemberInSlot(slot, playerChar)",
    0x00EC: "findPartyMemberFormationIndex(playerChar)",
    0x00ED: "getWorkerLinkedChr()",
    0x00F6: "waitForWorker(level, worker)",
    0x0102: "setBgmToLoad(bgm)",
    0x0104: "playBgm(bgm)",
    0x010D: "SetPrimerCollected(primerIndex)",
    0x010E: "CollectedPrimersBitfield()",
    0x0128: "workerWithinRadius(worker, radius)",
    0x0132: "setActorCollisionActive(worker, active)",
    0x0135: "PlayerTotalGil()",
    0x0136: "obtainGil(amount)",
    0x0137: "tryPayGil(amount)",
    0x013B: "displayFieldChoice(msgWindow, string, p3, p4, x, y, align)",
    0x015B: "obtainTreasure(msgWindow, treasure)",
    0x015F: "addKeyItem(keyItem)",
    0x0160: "hasKeyItem(keyItem)",
    0x0161: "removeKeyItem(keyItem)",
    0x0171: "fillPartyMemberHp(playerChar)",
    0x0172: "fillPartyMemberMp(playerChar)",
    0x0188: "fadeoutBgm(frames)",
    0x01A7: "obtainTreasureSilently(treasure)",
    0x01AB: "TotalBattlesFought()",
    0x1001: "sin(float)",
    0x1002: "cos(float)",
    0x1005: "atan2(y, x)",
    0x1006: "sqrt(float)",
    0x100A: "toInteger(float)",
    0x1013: "normalizeAngle(angle)",
    0x1019: "abs(float)",
    0x101A: "distance(x1, y1, x2, y2)",
    0x4003: "fadeinFromColor(frames, r, g, b)",
    0x4004: "fadeinFromBlack(frames)",
    0x4005: "fadeoutToBlack(frames)",
    0x4008: "setScreenOverlayColor(r, g, b, alpha)",
    0x400D: "waitForFade()",
    0x5000: "playCharMotion(motion)",
    0x5001: "loadMapMotionBundle(bundleIdx)",
    0x5003: "awaitMotion()",
    0x5006: "scaleActor(scaleXYZ)",
    0x5008: "setHidden(hidden)",
    # Battle library functions
    0x7000: "BattleInitSync",
    0x7001: "CheckTargetStatus",
    0x7002: "CheckTargetElement",
    0x7003: "WaitBattleAnim",
    0x7005: "TargetDistToParty",
    0x7006: "SetActorFacing",
    0x7007: "PlayActorMotion",
    0x7008: "WaitActorMotion",
    0x7009: "SetShadowEnabled",
    0x700A: "SetTargetableState",
    0x700B: "ExecuteAction",
    0x700C: "SpawnBattleEffect",
    0x700D: "SetMotionSpeed",
    0x700F: "GetProperty",
    0x7010: "FilterTargets",
    0x7012: "ResetActorPosition",
    0x7015: "ClearActionQueue",
    0x7016: "SetBattleCamera",
    0x7017: "LoadBattleEffect",
    0x7018: "SetProperty",
    0x7019: "GetLastActionId",
    0x701A: "GetAbilityProperty",
    0x701C: "SetActorVisibility",
    0x701D: "GetTargetCount",
    0x701E: "CheckTargetMatch",
    0x7020: "SetNextTurnActor",
    0x7021: "GetBattleRangeState",
    0x7024: "GetEncounterId",
    0x7026: "SetDamageDisplay",
    0x7028: "DisplayBattleText",
    0x7029: "SetSensorActive",
    0x702A: "GetActivePartyMask",
    0x702B: "IsActorReady",
    0x702D: "SetCameraBounds",
    0x702E: "SetModelPartState",
    0x7030: "GetBattleStateFlag",
    0x7031: "SyncActorState",
    0x7032: "RotateActor",
    0x7033: "MoveActorToTarget",
    0x7034: "ReturnActorToBase",
    0x7037: "SetStatModifier",
    0x7038: "TriggerSpecialEvent",
    0x703B: "PlayBattleVoice",
    0x703C: "ShowBattleDialog",
    0x704A: "CheckActorProximity",
    0x7051: "WaitEffectLoad",
    0x7052: "LinkActorProperty",
    0x7055: "SetEncounterFlag",
    0x7058: "CheckMotionFinished",
    0x705A: "ExecuteCounterAction",
    0x705D: "InitBattleResource",
    0x706B: "SetElementalAffinity",
    0x7078: "GetActorSlotIndex",
    0x707B: "AttachActorEffect",
    0x7086: "UpdateBattleHud",
    0x708E: "CheckPhaseReady",
    0x708F: "SetAnimBlend",
    0x7093: "GetPhaseTimer",
    0x7097: "TriggerStageEvent",
    0x70A1: "CountMatchingTargets",
    0x70A5: "SetBossStateVar",
    0x70A8: "SetTargetWeight",
    0x70AA: "GetInitProperty",
    0x70AB: "SetInitProperty",
    0x70B2: "SetInitFloat",
    0x70B5: "ApplyInitConfig",
    0x70CC: "QueueSubAction",
    0x70CD: "TriggerHitReaction",
    0x70CE: "FinishTurnAction",
    0x70D5: "SetCTBDelay",
    0x70E0: "CanExecuteCounter",
    0x70E2: "PlayMonsterAnim",
    0x7104: "SetAttachmentVisible",
    0x7107: "PlaySoundEffect",
    0x7108: "StopSoundEffect",
    0x7117: "SetArenaParameter",
    0x8000: "MathHelperCall",
}

# Verified argument counts for Atel VM & Battle Library calls
BATTLE_CALL_ARG_COUNTS = {
    0x005F: 0,
    0x00A9: 0,
    0x7000: 0,
    0x7001: 2,
    0x7002: 2,
    0x7003: 1,
    0x7005: 1,
    0x7006: 1,
    0x7007: 1,
    0x7008: 0,
    0x7009: 1,
    0x700A: 2,
    0x700B: 2,
    0x700C: 8,
    0x700D: 2,
    0x700F: 2,
    0x7010: 4,
    0x7012: 0,
    0x7015: 0,
    0x7016: 1,
    0x7017: 2,
    0x7018: 3,
    0x7019: 0,
    0x701A: 2,
    0x701C: 1,
    0x701D: 1,
    0x701E: 2,
    0x7020: 1,
    0x7021: 0,
    0x7024: 0,
    0x7026: 1,
    0x7028: 1,
    0x7029: 1,
    0x702A: 0,
    0x702B: 0,
    0x702D: 4,
    0x702E: 1,
    0x7030: 0,
    0x7031: 0,
    0x7032: 2,
    0x7033: 1,
    0x7034: 1,
    0x7037: 2,
    0x7038: 1,
    0x703B: 1,
    0x703C: 2,
    0x704A: 2,
    0x7051: 0,
    0x7052: 2,
    0x7055: 1,
    0x7058: 2,
    0x705A: 2,
    0x705D: 2,
    0x706B: 2,
    0x7078: 1,
    0x707B: 2,
    0x7086: 0,
    0x708E: 0,
    0x708F: 1,
    0x7093: 0,
    0x7097: 1,
    0x70A1: 1,
    0x70A5: 2,
    0x70A8: 2,
    0x70AA: 1,
    0x70AB: 2,
    0x70B2: 2,
    0x70B5: 0,
    0x70CC: 1,
    0x70CD: 1,
    0x70CE: 1,
    0x70D5: 1,
    0x70E0: 0,
    0x70E2: 2,
    0x7104: 2,
    0x7107: 1,
    0x7108: 1,
    0x7117: 2,
    0x8000: 1,
}

def show_dark_confirm(parent, title, prompt):
    import tkinter as tk
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("380x180")
    dialog.resizable(False, False)
    dialog.configure(bg="#121212")
    dialog.transient(parent)
    dialog.grab_set()
    
    dialog.update_idletasks()
    w, h = dialog.winfo_width(), dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (w // 2)
    y = (dialog.winfo_screenheight() // 2) - (h // 2)
    dialog.geometry(f"+{x}+{y}")
    
    lbl = tk.Label(dialog, text=prompt, bg="#121212", fg="#e5e7eb", font=("Segoe UI", 10), justify="center", wraplength=320)
    lbl.pack(fill="both", expand=True, pady=15, padx=20)
    
    res = {"value": None}
    def set_res(val):
        res["value"] = val
        dialog.destroy()
        
    btn_frame = tk.Frame(dialog, bg="#121212")
    btn_frame.pack(fill="x", side="bottom", pady=15)
    
    btn_yes = tk.Button(btn_frame, text="Yes", command=lambda: set_res(True), bg="#3b82f6", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", width=10)
    btn_yes.pack(side="left", expand=True, padx=10)
    
    btn_no = tk.Button(btn_frame, text="No", command=lambda: set_res(False), bg="#4b5563", fg="white", font=("Segoe UI", 9), relief="flat", width=10)
    btn_no.pack(side="left", expand=True, padx=10)
    
    btn_cancel = tk.Button(btn_frame, text="Cancel", command=lambda: set_res(None), bg="#1e1e1e", fg="#9ca3af", font=("Segoe UI", 9), relief="flat", width=10)
    btn_cancel.pack(side="left", expand=True, padx=10)
    
    parent.wait_window(dialog)
    return res["value"]

class AtelDisassembler:
    def __init__(self, chunk0_bytes):
        self.bytes = chunk0_bytes
        self.bytecode = b""
        self.bytecode_start = 0
        self.bytecode_len = 0
        self.workers = []
        self.creator_tag = ""
        self.script_id = ""
        self.ref_ints = []
        self.ref_floats = []
        
        self.parse_header()
        self.parse_workers()

    def read_u16(self, offset):
        if offset + 2 > len(self.bytes):
            return 0
        return struct.unpack("<H", self.bytes[offset:offset+2])[0]

    def read_u32(self, offset):
        if offset + 4 > len(self.bytes):
            return 0
        return struct.unpack("<I", self.bytes[offset:offset+4])[0]

    def parse_header(self):
        if len(self.bytes) < 0x38:
            return
        
        self.bytecode_len = self.read_u32(0x00)
        self.creator_tag_addr = self.read_u32(0x08)
        self.script_id_addr = self.read_u32(0x0C)
        self.bytecode_start = self.read_u32(0x30)
        self.namespace_count = self.read_u16(0x34)
        
        # Read bytecode
        if self.bytecode_start > 0 and self.bytecode_len > 0:
            self.bytecode = self.bytes[self.bytecode_start:self.bytecode_start+self.bytecode_len]
            
        # Read creator tag & script id strings
        self.creator_tag = self.read_string(self.creator_tag_addr)
        self.script_id = self.read_string(self.script_id_addr)

    def read_string(self, offset):
        if offset <= 0 or offset >= len(self.bytes):
            return ""
        end = offset
        while end < len(self.bytes) and self.bytes[end] != 0:
            end += 1
        try:
            return self.bytes[offset:end].decode("utf-8", errors="replace")
        except Exception:
            return ""

    def parse_workers(self):
        for i in range(self.namespace_count):
            worker_offset = self.read_u32(0x38 + i * 4)
            if worker_offset <= 0 or worker_offset + 0x34 > len(self.bytes):
                continue
            
            w_bytes = self.bytes[worker_offset:worker_offset+0x34]
            worker = {
                "index": i,
                "type": struct.unpack("<H", w_bytes[0x00:0x02])[0],
                "var_count": struct.unpack("<H", w_bytes[0x02:0x04])[0],
                "ref_int_count": struct.unpack("<H", w_bytes[0x04:0x06])[0],
                "ref_float_count": struct.unpack("<H", w_bytes[0x06:0x08])[0],
                "func_count": struct.unpack("<H", w_bytes[0x08:0x0A])[0],
                "jump_count": struct.unpack("<H", w_bytes[0x0A:0x0C])[0],
                "private_data_len": struct.unpack("<I", w_bytes[0x10:0x14])[0],
                "vars_offset": struct.unpack("<I", w_bytes[0x14:0x18])[0],
                "ref_ints_offset": struct.unpack("<I", w_bytes[0x18:0x1C])[0],
                "ref_floats_offset": struct.unpack("<I", w_bytes[0x1C:0x20])[0],
                "funcs_offset": struct.unpack("<I", w_bytes[0x20:0x24])[0],
                "jumps_offset": struct.unpack("<I", w_bytes[0x24:0x28])[0],
                "private_data_offset": struct.unpack("<I", w_bytes[0x2C:0x30])[0],
                "shared_data_offset": struct.unpack("<I", w_bytes[0x30:0x34])[0],
            }
            
            # Read refInts
            ref_ints = []
            if worker["ref_ints_offset"] > 0 and worker["ref_int_count"] > 0:
                for k in range(worker["ref_int_count"]):
                    val_addr = worker["ref_ints_offset"] + k * 4
                    if val_addr + 4 <= len(self.bytes):
                        ref_ints.append(struct.unpack("<i", self.bytes[val_addr:val_addr+4])[0])
            worker["ref_ints"] = ref_ints
            
            # Read refFloats
            ref_floats = []
            if worker["ref_floats_offset"] > 0 and worker["ref_float_count"] > 0:
                for k in range(worker["ref_float_count"]):
                    val_addr = worker["ref_floats_offset"] + k * 4
                    if val_addr + 4 <= len(self.bytes):
                        ref_floats.append(struct.unpack("<f", self.bytes[val_addr:val_addr+4])[0])
            worker["ref_floats"] = ref_floats

            # Read functions
            funcs = []
            if worker["funcs_offset"] > 0 and worker["func_count"] > 0:
                for k in range(worker["func_count"]):
                    func_addr = worker["funcs_offset"] + k * 4
                    if func_addr + 4 <= len(self.bytes):
                        funcs.append(self.read_u32(func_addr))
            worker["funcs"] = funcs

            # Read jumps
            jumps = []
            if worker["jumps_offset"] > 0 and worker["jump_count"] > 0:
                for k in range(worker["jump_count"]):
                    jump_addr = worker["jumps_offset"] + k * 4
                    if jump_addr + 4 <= len(self.bytes):
                        jumps.append(self.read_u32(jump_addr))
            worker["jumps"] = jumps

            self.workers.append(worker)

    def disassemble(self):
        if not self.bytecode:
            return "No Atel bytecode found."
        
        output = []
        output.append(f"// ==========================================================")
        output.append(f"// FFX Atel Script Disassembly")
        output.append(f"// Creator Tag: {self.creator_tag}")
        output.append(f"// Script ID:   {self.script_id}")
        output.append(f"// Workers:     {len(self.workers)}")
        output.append(f"// ==========================================================\n")
        
        # Build mappings of targets in bytecode
        # key: absolute_offset, value: list of (worker_idx, type_string, index)
        labels = {}
        for w in self.workers:
            for idx, addr in enumerate(w["funcs"]):
                labels.setdefault(addr, []).append((w["index"], "Func", idx))
            for idx, addr in enumerate(w["jumps"]):
                labels.setdefault(addr, []).append((w["index"], "Label", idx))
                
        # Group bytecode offsets by active worker (based on function entries)
        # We find which worker belongs to which bytecode ranges
        worker_ranges = []
        all_entry_points = []
        for w in self.workers:
            for addr in w["funcs"]:
                all_entry_points.append((addr, w["index"]))
        all_entry_points.sort()
        
        # Helper to get worker index for a given bytecode offset
        def get_worker_for_offset(offset):
            current_worker = 0
            for addr, w_idx in all_entry_points:
                if offset >= addr:
                    current_worker = w_idx
                else:
                    break
            return current_worker

        cursor = 0
        while cursor < len(self.bytecode):
            w_idx = get_worker_for_offset(cursor)
            worker = self.workers[w_idx] if w_idx < len(self.workers) else None
            
            # Print labels first if any exist at this address
            if cursor in labels:
                for w_num, lbl_type, lbl_idx in labels[cursor]:
                    if lbl_type == "Func":
                        output.append(f"\n// --- Worker {w_num} :: Function {lbl_idx} ---")
                        output.append(f"w{w_num:02d}_f{lbl_idx:02d}:")
                    else:
                        output.append(f"w{w_num:02d}_Label_{lbl_idx:02d}:")
            
            offset = cursor
            opcode = self.bytecode[cursor]
            cursor += 1
            
            has_args = (opcode >= 0x80)
            if has_args:
                if cursor + 2 > len(self.bytecode):
                    # Malformed end of bytecode
                    output.append(f" {offset:04X}: [MALFORMED OP {opcode:02X}]")
                    break
                arg1 = self.bytecode[cursor]
                arg2 = self.bytecode[cursor+1]
                cursor += 2
                argv = arg1 + arg2 * 0x100
                argv_signed = argv if argv < 0x8000 else (argv - 0x10000)
            else:
                argv = 0
                argv_signed = 0
                
            mnemonic = OPCODE_MAP.get(opcode, f"UNK_{opcode:02X}")
            
            # Format arguments beautifully
            arg_str = ""
            if has_args:
                # Branches / Jumps
                if opcode in [0xB0, 0xB1, 0xB2, 0xD5, 0xD6, 0xD7]:
                    # Target is a jump index in the current worker
                    if worker and argv < len(worker["jumps"]):
                        target_addr = worker["jumps"][argv]
                        arg_str = f"w{w_idx:02d}_Label_{argv:02d}  // target offset {target_addr:04X}"
                    else:
                        arg_str = f"Label_{argv:02d}"
                # Jump Subroutine (JSR)
                elif opcode == 0xB3:
                    arg_str = f"w{argv:02d}"
                # Call targets
                elif opcode in [0xB5, 0xD8]:
                    call_name = CALL_TARGET_MAP.get(argv, f"call_{argv:04X}")
                    arg_str = f"{call_name} ({argv:04X})"
                # Direct int constant (refInts)
                elif opcode == 0xAD:
                    if worker and argv < len(worker["ref_ints"]):
                        val = worker["ref_ints"][argv]
                        arg_str = f"refInts[{argv}] ({val})"
                    else:
                        arg_str = f"refInts[{argv}]"
                # Direct float constant (refFloats)
                elif opcode == 0xAF:
                    if worker and argv < len(worker["ref_floats"]):
                        val = worker["ref_floats"][argv]
                        arg_str = f"refFloats[{argv}] ({val:.4f})"
                    else:
                        arg_str = f"refFloats[{argv}]"
                # Variables (PUSHV, POPV, etc.)
                elif opcode in [0x9F, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA7]:
                    arg_str = f"var_{argv:02X}"
                # Immediate values (PUSHII)
                elif opcode == 0xAE:
                    arg_str = f"{argv_signed} (0x{argv:04X})"
                else:
                    arg_str = f"0x{argv:04X}"
                    
            hex_part = f"{opcode:02X}"
            if has_args:
                hex_part += f" {arg1:02X} {arg2:02X}"
            
            line_str = f"  {offset:04X}:   {hex_part:<10} {mnemonic:<10} {arg_str}"
            output.append(line_str)
            
        return "\n".join(output)

# Operators mapping for pseudocode
OP_SYMBOLS = {
    0x01: "or",     # Logical OPLOR
    0x02: "and",    # Logical OPLAND
    0x03: "|",      # Bitwise OPOR
    0x04: "^",      # Bitwise OPEOR
    0x05: "&",      # Bitwise OPAND
    0x06: "==",     # OPEQ
    0x07: "!=",     # OPNE
    0x08: ">",      # OPGTU
    0x09: "<",      # OPLSU
    0x0A: ">",      # OPGT
    0x0B: "<",      # OPLS
    0x0C: ">=",     # OPGTEU
    0x0D: "<=",     # OPLSEU
    0x0E: ">=",     # OPGTE
    0x0F: "<=",     # OPLSE
    0x12: "<<",     # OPSLL
    0x13: ">>",     # OPSRL
    0x14: "+",      # OPADD
    0x15: "-",      # OPSUB
    0x16: "*",      # OPMUL
    0x17: "/",      # OPDIV
    0x18: "%",      # OPMOD
}

# Operators mapping for Plain English
OP_ENGLISH = {
    0x01: "or",
    0x02: "and",
    0x03: "bitwise OR",
    0x04: "bitwise XOR",
    0x05: "bitwise AND",
    0x06: "is equal to",
    0x07: "is not equal to",
    0x08: "is greater than",
    0x09: "is less than",
    0x0A: "is greater than",
    0x0B: "is less than",
    0x0C: "is greater than or equal to",
    0x0D: "is less than or equal to",
    0x0E: "is greater than or equal to",
    0x0F: "is less than or equal to",
    0x14: "plus",
    0x15: "minus",
    0x16: "times",
    0x17: "divided by",
    0x18: "modulo",
}

class AtelDecompiler:
    def __init__(self, chunk0_bytes):
        self.disasm = AtelDisassembler(chunk0_bytes)
        
    def to_assembly(self):
        return self.disasm.disassemble()
        
    def to_pseudocode(self):
        return self.decompile(mode="pseudocode")
        
    def to_plain_english(self):
        return self.decompile(mode="english")
        
    def decompile(self, mode="pseudocode"):
        if not self.disasm.bytecode:
            return "No Atel bytecode found."
            
        output = []
        output.append(f"// ==========================================================")
        output.append(f"// FFX Atel Script Decompiled ({mode.upper()} View)")
        output.append(f"// Creator Tag: {self.disasm.creator_tag}")
        output.append(f"// Script ID:   {self.disasm.script_id}")
        output.append(f"// Workers:     {len(self.disasm.workers)}")
        output.append(f"// ==========================================================\n")
        
        # Build mappings of targets in bytecode
        labels = {}
        for w in self.disasm.workers:
            for idx, addr in enumerate(w["funcs"]):
                labels.setdefault(addr, []).append((w["index"], "Func", idx))
            for idx, addr in enumerate(w["jumps"]):
                labels.setdefault(addr, []).append((w["index"], "Label", idx))
                
        # Group entry points
        all_entry_points = []
        for w in self.disasm.workers:
            for addr in w["funcs"]:
                all_entry_points.append((addr, w["index"]))
        all_entry_points.sort()
        
        def get_worker_for_offset(offset):
            current_worker = 0
            for addr, w_idx in all_entry_points:
                if offset >= addr:
                    current_worker = w_idx
                else:
                    break
            return current_worker

        cursor = 0
        stack = []
        last_rx = "rX"
        indent = 2
        
        while cursor < len(self.disasm.bytecode):
            w_idx = get_worker_for_offset(cursor)
            worker = self.disasm.workers[w_idx] if w_idx < len(self.disasm.workers) else None
            
            # Print labels / function headers
            if cursor in labels:
                for w_num, lbl_type, lbl_idx in labels[cursor]:
                    if lbl_type == "Func":
                        indent = 2
                        stack.clear()
                        last_rx = "rX"
                        if mode == "pseudocode":
                            output.append(f"\ndef worker_{w_num:02d}_function_{lbl_idx:02d}():")
                        else:
                            output.append(f"\n[Worker {w_num:02d} :: Function {lbl_idx:02d}]")
                    else:
                        if mode == "pseudocode":
                            output.append(f"{' ' * (indent - 2)}label_{lbl_idx:02d}:")
                        else:
                            output.append(f"{' ' * (indent - 2)}[Label {lbl_idx:02d}]")
            
            offset = cursor
            opcode = self.disasm.bytecode[cursor]
            cursor += 1
            
            has_args = (opcode >= 0x80)
            argv = 0
            argv_signed = 0
            if has_args:
                if cursor + 2 > len(self.disasm.bytecode):
                    break
                arg1 = self.disasm.bytecode[cursor]
                arg2 = self.disasm.bytecode[cursor+1]
                cursor += 2
                argv = arg1 + arg2 * 0x100
                argv_signed = argv if argv < 0x8000 else (argv - 0x10000)
                
            mnemonic = OPCODE_MAP.get(opcode, f"UNK_{opcode:02X}")
            
            # Stack push operations
            if opcode == 0xAD:  # PUSHI
                if worker and argv < len(worker["ref_ints"]):
                    val = worker["ref_ints"][argv]
                    stack.append(f"refInts[{argv}]({val})")
                else:
                    stack.append(f"refInts[{argv}]")
            elif opcode == 0xAF:  # PUSHF
                if worker and argv < len(worker["ref_floats"]):
                    val = worker["ref_floats"][argv]
                    stack.append(f"{val:.4f}")
                else:
                    stack.append(f"refFloats[{argv}]")
            elif opcode == 0xAE:  # PUSHII
                stack.append(str(argv_signed))
            elif opcode == 0x9F:  # PUSHV
                stack.append(f"var_{argv:02X}")
            elif opcode == 0x26:  # PUSHA
                stack.append("rA")
            elif opcode == 0x28:  # PUSHX
                stack.append(last_rx)
            elif opcode == 0x29:  # PUSHY
                stack.append("rY")
            elif opcode in [0x67, 0x68, 0x69, 0x6A]:  # PUSHI0..PUSHI3
                stack.append(f"rI{opcode - 0x67}")
            
            # Stack pop operations / assignments
            elif opcode == 0x25:  # POPA
                val = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}rA = {val}")
                else:
                    output.append(f"{' ' * indent}Set return register rA to {val}")
            elif opcode == 0x2A:  # POPX
                val = stack.pop() if stack else "?"
                last_rx = val
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}rX = {val}")
                else:
                    output.append(f"{' ' * indent}Set test register rX to {val}")
            elif opcode == 0x2C:  # POPY
                val = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}rY = {val}")
                else:
                    output.append(f"{' ' * indent}Set case register rY to {val}")
            elif opcode in [0x59, 0x5A, 0x5B, 0x5C]:  # POPI0..POPI3
                val = stack.pop() if stack else "?"
                reg_name = f"rI{opcode - 0x59}"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}{reg_name} = {val}")
                else:
                    output.append(f"{' ' * indent}Set temp register {reg_name} to {val}")
            elif opcode in [0xA0, 0xA1]:  # POPV, POPVL
                val = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}var_{argv:02X} = {val}")
                else:
                    output.append(f"{' ' * indent}Set variable var_{argv:02X} to {val}")
            elif opcode in [0xA3, 0xA4]:  # POPAR, POPARL
                val = stack.pop() if stack else "?"
                idx = stack.pop() if stack else "?"
                arr = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}{arr}[{idx}] = {val}")
                else:
                    output.append(f"{' ' * indent}Set element at index {idx} in {arr} to {val}")
            
            # Binary operations
            elif opcode in OP_SYMBOLS:
                b = stack.pop() if stack else "?"
                a = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    sym = OP_SYMBOLS[opcode]
                    stack.append(f"({a} {sym} {b})")
                else:
                    sym_eng = OP_ENGLISH.get(opcode, OPCODE_MAP[opcode])
                    stack.append(f"({a} {sym_eng} {b})")
            
            # Unary operations
            elif opcode == 0x19:  # OPNOT
                a = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    stack.append(f"(!{a})")
                else:
                    stack.append(f"(not {a})")
            elif opcode == 0x1C:  # OPBNOT
                a = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    stack.append(f"(~{a})")
                else:
                    stack.append(f"(bitwise NOT of {a})")
                    
            # Branching / Jumps
            elif opcode == 0xB0:  # JMP
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}Jump to Label {argv:02d}")
            elif opcode == 0xB1:  # CJMP
                cond = stack.pop() if stack else "rA"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}if {cond}: goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}If {cond} is true: Jump to Label {argv:02d}")
            elif opcode == 0xB2:  # NCJMP
                cond = stack.pop() if stack else "rA"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}if not {cond}: goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}If {cond} is false: Jump to Label {argv:02d}")
            elif opcode == 0xD5:  # POPXJMP
                cond = stack.pop() if stack else last_rx
                last_rx = cond
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}rX_check ({cond}): goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}Check {cond} and jump to Label {argv:02d}")
            elif opcode == 0xD6:  # POPXCJMP
                cond = stack.pop() if stack else last_rx
                last_rx = cond
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}if {cond}: goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}If {cond} is true: Jump to Label {argv:02d}")
            elif opcode == 0xD7:  # POPXNCJMP
                cond = stack.pop() if stack else last_rx
                last_rx = cond
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}if not {cond}: goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}If {cond} is false: Jump to Label {argv:02d}")
            
            # Return instructions
            elif opcode in [0x34, 0x3C, 0x3D, 0x3E, 0x3F, 0x54, 0x73]:  # RTS, RET, etc.
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}return")
                else:
                    output.append(f"{' ' * indent}Exit / Return")
            
            # Library Calls
            elif opcode in [0xB5, 0xD8]:  # CALL (pushes return value), CALLPOPA (pops return into rA)
                raw_name = CALL_TARGET_MAP.get(argv, f"call_{argv:04X}")
                call_name = raw_name.split("(")[0]
                
                if argv in BATTLE_CALL_ARG_COUNTS:
                    num_args = BATTLE_CALL_ARG_COUNTS[argv]
                elif "(" in raw_name and ")" in raw_name:
                    inner = raw_name.split("(", 1)[1].rsplit(")", 1)[0].strip()
                    num_args = 0 if not inner else len(inner.split(","))
                else:
                    num_args = len(stack)
                
                returns_val = (opcode == 0xB5)
                    
                args = []
                for _ in range(num_args):
                    if stack:
                        args.insert(0, stack.pop())
                    else:
                        args.insert(0, "?")
                        
                stmt = f"{call_name}({', '.join(args)})"
                
                if opcode == 0xD8:
                    if mode == "pseudocode":
                        output.append(f"{' ' * indent}rA = {stmt}")
                    else:
                        output.append(f"{' ' * indent}Execute {stmt}")
                elif returns_val:
                    stack.append(stmt)
                else:
                    if mode == "pseudocode":
                        output.append(f"{' ' * indent}{stmt}")
                    else:
                        output.append(f"{' ' * indent}Call function: {stmt}")
                        
            elif opcode == 0x40:  # HALT
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}halt()")
                else:
                    output.append(f"{' ' * indent}Halt execution")
            
            elif opcode == 0x00:  # NOP
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}pass")
                else:
                    output.append(f"{' ' * indent}No operation")
            
        return "\n".join(output)


# ==============================================================================
# FFX AI EVENT HOOKS, TARGETS, CONDITIONS, & RULE BUILDER ENGINE
# ==============================================================================

AI_EVENT_HOOK_DEFS = [
    (0, "turn",      "⚡ Active Turn",      "Regular CTB turn execution script"),
    (3, "react",     "🛡 Counter / React",  "Post-attack reaction / counterattack script"),
    (2, "damage",    "💥 On Damage",        "Immediate response when hit damage is taken"),
    (4, "death",     "💀 On Death",         "Final attack / phase shift / death script"),
    (1, "pre_turn",  "⏳ Pre-Turn",         "Runs immediately before turn / stance ready"),
    (5, "start",     "🎬 Battle Start",     "Runs on encounter start or monster spawn"),
    (6, "targeted",  "🎯 On Targeted",      "Runs when targeted or action is queued"),
    (7, "post_turn", "📐 Post-Turn",        "Runs after turn resolution (field/cliff checks)"),
    (8, "tick",      "⏱ Status Tick",      "Runs on status / phase state ticks"),
]

STATUS_PROP_MAP = {
    "KO / Dead": 4,
    "Petrify": 5,
    "Sleep": 6,
    "Silence": 7,
    "Darkness": 8,
    "Poison": 9,
    "Confusion": 10,
    "Berserk": 11,
    "Provoke": 18,
    "Doom": 22,
    "Defend": 28,
    "Haste": 33,
    "Slow": 34,
    "Shell": 35,
    "Protect": 36,
    "Reflect": 37,
    "Regen": 39,
    "Magic Lock": 43,
}

PROP_TO_STATUS_NAME = {v: k for k, v in STATUS_PROP_MAP.items()}

CONDITION_PRESETS = [
    "Always",
    # Self HP / MP Thresholds
    "Self HP < 75%",
    "Self HP < 50%",
    "Self HP < 33%",
    "Self HP < 25%",
    "Self HP >= 50%",
    "Self MP < 50%",
    "Self MP < 25%",
    # Legacy aliases (mapped automatically to Self HP/MP)
    "HP < 50%",
    "HP < 25%",
    "MP < 50%",
    "MP < 25%",
    # Party Status Checks (0x701E CheckTargetMatch on Active Party -14)
    "Party: Anyone Has Reflect",
    "Party: Anyone Has Haste",
    "Party: Anyone Has Protect",
    "Party: Anyone Has Shell",
    "Party: Anyone Has Regen",
    "Party: Anyone Is Poisoned",
    "Party: Anyone Is Silenced",
    "Party: Anyone Is Blind",
    "Party: Anyone Is Sleeping",
    "Party: Anyone Is Petrified",
    "Party: Has Valid Frontline Target",
    # Self Status Checks (0x700F GetProperty on Self -13)
    "Self: Is Provoked",
    "Self: Is Silenced",
    "Self: Not Hasted",
    "Self: Not Protected",
    "Self: Not Shelled",
    "Self: Not Reflecting",
    "Self: Not Regenerating",
    # Counter / Reaction Triggers (for Slot 3 Counter & Slot 2 On Damage)
    "Counter: Took Damage (Hit > 0)",
    "Counter: Hit by Physical Attack",
    "Counter: Hit by Magical Attack",
    # Turn / State Variable Checks
    "Phase / State: var_00 == 0",
    "Phase / State: var_00 == 1",
    "Phase / State: var_00 == 2",
    "Phase / State: var_00 == 3",
    "Turn Step: var_01 == 0",
    "Turn Step: var_01 == 1",
    "Turn Step: var_01 == 2",
    "Turn Step: var_01 == 3",
    "Turn Step: var_01 == 4",
    "Turn Step: var_02 == 0",
    "Turn Step: var_02 == 1",
    "Turn Step: var_02 == 2",
    "Turn Step: var_02 == 3",
    # Formation / Ally Checks
    "Allies: Monster Slot 0 Dead",
    "Allies: Monster Slot 1 Dead",
    "Allies: Monster Slot 2 Dead",
    "Allies: Monster Slot 1 Alive",
    "Solo Fiend (Last Standing)",
    "Party Alive <= 1",
    "Party Alive <= 2",
]

TARGET_PRESETS = [
    "Random Alive Party Member",
    "All Active Party",
    "Self",
    "All Allied Monsters",
    "Last Attacker (Counter)",
    "Provoker",
    "Lowest HP Party Member",
    "Highest HP Party Member",
    "Lowest MP Party Member",
    "Highest MP Party Member",
    "Party Member With Reflect",
    "Party Member Without Reflect",
    "Party Member With Haste",
    "Party Member Without Haste",
    "Party Member With Protect",
    "Party Member Without Protect",
    "Party Member With Shell",
    "Party Member Without Shell",
    "Party Member Without Poison",
    "Party Member Without Silence",
    "Party Member Without Darkness",
    "Character: Tidus",
    "Character: Yuna",
    "Character: Auron",
    "Character: Kimahri",
    "Character: Wakka",
    "Character: Lulu",
    "Character: Rikku",
    "Aeon / Summon",
    "Monster Slot 0 (Main Boss)",
    "Monster Slot 1",
    "Monster Slot 2",
    "Monster Slot 3",
]

CHAR_MASK_TO_NAME = {
    1: "Character: Tidus",
    2: "Character: Yuna",
    4: "Character: Auron",
    8: "Character: Kimahri",
    16: "Character: Wakka",
    32: "Character: Lulu",
    64: "Character: Rikku",
    -21: "Aeon / Summon",
    20: "Monster Slot 0 (Main Boss)",
    21: "Monster Slot 1",
    22: "Monster Slot 2",
    23: "Monster Slot 3",
}
NAME_TO_CHAR_MASK = {v: k for k, v in CHAR_MASK_TO_NAME.items()}


def parse_chunk1_ai_map(chunk1_bytes, chunk0_bytes=None):
    """
    Parses Chunk 1's worker role descriptor table at 0x8C to locate the Combat AI Worker (role == 2)
    and its 21 uint16 event hook slots (Slots 0..20 at table_offset + 2).
    """
    disasm = AtelDisassembler(chunk0_bytes) if chunk0_bytes else None
    num_c0_workers = len(disasm.workers) if disasm else 0

    ai_worker_idx = None
    slots = [0xFFFF] * 21
    role_table_offset = None

    if chunk1_bytes and len(chunk1_bytes) >= 0x90:
        nw = chunk1_bytes[0]
        for i in range(nw):
            desc_off = 0x8C + i * 4
            if desc_off + 4 > len(chunk1_bytes):
                break
            w_idx, role, off = struct.unpack_from("<BBH", chunk1_bytes, desc_off)
            if role == 2 and off + 4 <= len(chunk1_bytes):
                cnt = struct.unpack_from("<H", chunk1_bytes, off)[0]
                max_cnt = min(cnt, (len(chunk1_bytes) - (off + 2)) // 2, 21)
                if max_cnt > 0:
                    ai_worker_idx = w_idx
                    role_table_offset = off
                    slots[:max_cnt] = list(struct.unpack_from(f"<{max_cnt}H", chunk1_bytes, off + 2))
                    break

    # Fallback if Chunk 1 wasn't provided or had no role=2 entry
    if ai_worker_idx is None:
        if num_c0_workers > 1:
            ai_worker_idx = 1
        else:
            ai_worker_idx = 0
        if disasm and ai_worker_idx < num_c0_workers:
            fc = len(disasm.workers[ai_worker_idx]["funcs"])
            if fc > 2:
                slots[0] = 2

    all_eps = []
    if disasm:
        all_eps = sorted(set(addr for w in disasm.workers for addr in w["funcs"]))

    def get_func_bytecode(w_idx, f_idx):
        if not disasm or w_idx >= len(disasm.workers):
            return b""
        w = disasm.workers[w_idx]
        if f_idx >= len(w["funcs"]):
            return b""
        s = w["funcs"][f_idx]
        idx = all_eps.index(s) if s in all_eps else -1
        e = all_eps[idx + 1] if (idx >= 0 and idx + 1 < len(all_eps)) else len(disasm.bytecode)
        return disasm.bytecode[s:e]

    hooks = []
    for slot_idx, key, label, desc in AI_EVENT_HOOK_DEFS:
        f_idx = slots[slot_idx] if slot_idx < len(slots) else 0xFFFF
        mapped_f = f_idx if f_idx != 0xFFFF else None
        bc = get_func_bytecode(ai_worker_idx, mapped_f) if mapped_f is not None else b""
        has_logic = len(bc) > 1 and bc != b"\x3C"
        hooks.append({
            "slot_idx": slot_idx,
            "key": key,
            "label": label,
            "description": desc,
            "func_idx": mapped_f,
            "has_logic": has_logic,
            "bytecode_len": len(bc),
        })

    var_count = 0
    func_count = 0
    if disasm and ai_worker_idx < len(disasm.workers):
        var_count = disasm.workers[ai_worker_idx]["var_count"]
        func_count = len(disasm.workers[ai_worker_idx]["funcs"])

    return {
        "ai_worker_idx": ai_worker_idx,
        "role_table_offset": role_table_offset,
        "slots": slots,
        "hooks": hooks,
        "var_count": var_count,
        "func_count": func_count,
    }


def _pack_pushii(val: int) -> bytes:
    return struct.pack("<Bh", 0xAE, int(val))


def _pack_pushv(var_idx: int) -> bytes:
    return struct.pack("<BH", 0x9F, int(var_idx) & 0xFFFF)


def _pack_popv(var_idx: int) -> bytes:
    return struct.pack("<BH", 0xA0, int(var_idx) & 0xFFFF)


def _pack_call(call_id: int, pop_a: bool = False) -> bytes:
    op = 0xD8 if pop_a else 0xB5
    return struct.pack("<BH", op, int(call_id) & 0xFFFF)


def _parse_var_index(var_str: str) -> int:
    s = str(var_str).strip()
    if s.lower().startswith("var_"):
        s = s[4:]
    try:
        return int(s, 16)
    except ValueError:
        try:
            return int(s)
        except ValueError:
            return 0


OP_STR_TO_BYTE = {
    "==": 0x06,
    "!=": 0x07,
    ">":  0x0A,
    "<":  0x0B,
    ">=": 0x0E,
    "<=": 0x0F,
}


def encode_single_condition_expr(cond_type: str) -> bytes:
    """
    Encodes a single condition into Atel stack bytecode that leaves a boolean (0 or 1)
    on top of the stack (ready for logical AND/OR or POPXNCJMP 0xD7).
    Returns b"" if the condition is 'Always' or unconditional.
    """
    import re
    cond = (cond_type or "Always").strip()
    if not cond or cond == "Always":
        return b""

    b = bytearray()

    # 1. Self HP / MP Percentage: e.g. "Self HP < 50%", "HP < 25%", "Self HP >= 50%"
    m_hp = re.match(r"^(?:Self\s+)?(HP|MP)\s*(<|<=|>|>=|==|!=)\s*(\d+)%$", cond, re.IGNORECASE)
    if m_hp:
        stat_kind = m_hp.group(1).upper()
        op_sym = m_hp.group(2)
        pct = max(1, min(100, int(m_hp.group(3))))
        cur_prop = 0 if stat_kind == "HP" else 1
        max_prop = 2 if stat_kind == "HP" else 3
        op_byte = OP_STR_TO_BYTE.get(op_sym, 0x0B)

        # GetProperty(-13, cur_prop)
        b.extend(_pack_pushii(-13))
        b.extend(_pack_pushii(cur_prop))
        b.extend(_pack_call(0x700F, pop_a=False))

        # GetProperty(-13, max_prop)
        b.extend(_pack_pushii(-13))
        b.extend(_pack_pushii(max_prop))
        b.extend(_pack_call(0x700F, pop_a=False))

        # Idiomatic vanilla fractions where exact (50% -> /2, 33% -> /3, 25% -> /4, 20% -> /5)
        if pct == 50:
            b.extend(_pack_pushii(2))
            b.extend(b"\x17")  # OPDIV
        elif pct in (33, 34):
            b.extend(_pack_pushii(3))
            b.extend(b"\x17")  # OPDIV
        elif pct == 25:
            b.extend(_pack_pushii(4))
            b.extend(b"\x17")  # OPDIV
        elif pct == 20:
            b.extend(_pack_pushii(5))
            b.extend(b"\x17")  # OPDIV
        else:
            b.extend(_pack_pushii(100))
            b.extend(b"\x17")  # max / 100
            b.extend(_pack_pushii(pct))
            b.extend(b"\x16")  # * pct

        b.append(op_byte)
        return bytes(b)

    # 2. Party Status Checks via 0x701E CheckTargetMatch(-14, status_prop)
    party_status_map = {
        "Party: Anyone Has Reflect": (37, False),
        "Target: Has Reflect":       (37, False),
        "Party: Anyone Has Haste":   (33, False),
        "Target: Has Haste":         (33, False),
        "Party: Anyone Has Protect": (36, False),
        "Target: Has Protect":       (36, False),
        "Party: Anyone Has Shell":   (35, False),
        "Target: Has Shell":         (35, False),
        "Party: Anyone Has Regen":   (39, False),
        "Party: Anyone Is Poisoned": (9,  False),
        "Target: Not Poisoned":      (9,  True),
        "Party: Anyone Is Silenced": (7,  False),
        "Target: Not Silenced":      (7,  True),
        "Party: Anyone Is Blind":    (8,  False),
        "Target: Not Blind":         (8,  True),
        "Party: Anyone Is Sleeping": (6,  False),
        "Party: Anyone Is Petrified":(5,  False),
        "Party: Has Valid Frontline Target": (-20, False),
    }
    if cond in party_status_map:
        st_prop, invert = party_status_map[cond]
        b.extend(_pack_pushii(-14))
        b.extend(_pack_pushii(st_prop))
        b.extend(_pack_call(0x701E, pop_a=False))
        if invert:
            b.extend(_pack_pushii(0))
            b.append(0x06)  # == 0
        return bytes(b)

    # 3. Self Status Checks via 0x700F GetProperty(-13, prop)
    self_status_map = {
        "Self: Is Provoked":      (43, "!=", 0),
        "Self: Is Silenced":      (7,  "!=", 0),
        "Self: Not Hasted":       (33, "==", 0),
        "Self: Not Protected":    (36, "==", 0),
        "Self: Not Shelled":      (35, "==", 0),
        "Self: Not Reflecting":   (37, "==", 0),
        "Self: Not Regenerating": (39, "==", 0),
    }
    if cond in self_status_map:
        prop_id, op_s, cmp_val = self_status_map[cond]
        b.extend(_pack_pushii(-13))
        b.extend(_pack_pushii(prop_id))
        b.extend(_pack_call(0x700F, pop_a=False))
        b.extend(_pack_pushii(cmp_val))
        b.append(OP_STR_TO_BYTE[op_s])
        return bytes(b)

    # 4. Counter / Reaction Triggers
    if cond == "Counter: Took Damage (Hit > 0)":
        b.extend(_pack_pushii(-13))
        b.extend(_pack_pushii(166))
        b.extend(_pack_call(0x700F, pop_a=False))
        b.extend(_pack_pushii(0))
        b.append(0x0A)  # > 0
        return bytes(b)
    if cond in ("Counter: Hit by Physical Attack", "Counter: Hit by Magical Attack"):
        atk_type = 1 if "Physical" in cond else 2
        b.extend(_pack_call(0x7019, pop_a=False))  # GetLastActionId()
        b.extend(_pack_pushii(10))                 # prop 10 = physical(1) / magical(2)
        b.extend(_pack_call(0x701A, pop_a=False))  # GetAbilityProperty(last_act, 10)
        b.extend(_pack_pushii(atk_type))
        b.append(0x06)  # == atk_type
        return bytes(b)
    m_last_act = re.match(r"^Counter:\s*Last Action\s*(==|!=)\s*(0x[0-9A-Fa-f]+|\d+)$", cond, re.IGNORECASE)
    if m_last_act:
        op_s = m_last_act.group(1)
        act_val = int(m_last_act.group(2), 0)
        b.extend(_pack_call(0x7019, pop_a=False))
        b.extend(_pack_pushii(act_val))
        b.append(OP_STR_TO_BYTE[op_s])
        return bytes(b)

    # 5. Formation / Ally Slot Checks
    ally_slot_map = {
        "Allies: Monster Slot 0 Dead":  (20, 4, "==", 1),
        "Allies: Monster Slot 1 Dead":  (21, 4, "==", 1),
        "Allies: Monster Slot 2 Dead":  (22, 4, "==", 1),
        "Allies: Monster Slot 1 Alive": (21, 4, "==", 0),
    }
    if cond in ally_slot_map:
        slot_id, prop_id, op_s, val = ally_slot_map[cond]
        b.extend(_pack_pushii(slot_id))
        b.extend(_pack_pushii(prop_id))
        b.extend(_pack_call(0x700F, pop_a=False))
        b.extend(_pack_pushii(val))
        b.append(OP_STR_TO_BYTE[op_s])
        return bytes(b)

    if cond == "Solo Fiend (Last Standing)":
        b.extend(_pack_pushii(-15))
        b.extend(_pack_call(0x701D, pop_a=False))  # GetTargetCount(-15)
        b.extend(_pack_pushii(1))
        b.append(0x0F)  # <= 1
        return bytes(b)

    m_party_alive = re.match(r"^Party Alive\s*(<=|==|<|>|>=)\s*(\d+)$", cond, re.IGNORECASE)
    if m_party_alive:
        op_s = m_party_alive.group(1)
        cnt_val = int(m_party_alive.group(2))
        b.extend(_pack_pushii(-14))
        b.extend(_pack_call(0x701D, pop_a=False))  # GetTargetCount(-14)
        b.extend(_pack_pushii(cnt_val))
        b.append(OP_STR_TO_BYTE.get(op_s, 0x0F))
        return bytes(b)

    # 6. Legacy Turn 1 / Turn 2 / Turn 3 / Every N Turns -> use var_01
    m_turn = re.match(r"^Turn\s+(\d+)$", cond, re.IGNORECASE)
    if m_turn:
        t_val = max(0, int(m_turn.group(1)) - 1)
        b.extend(_pack_pushv(1))
        b.extend(_pack_pushii(t_val))
        b.append(0x06)  # ==
        return bytes(b)

    m_every = re.match(r"^Every\s+(\d+)\s+Turns$", cond, re.IGNORECASE)
    if m_every:
        mod_val = max(2, int(m_every.group(1)))
        b.extend(_pack_pushv(1))
        b.extend(_pack_pushii(mod_val))
        b.append(0x18)  # OPMOD
        b.extend(_pack_pushii(0))
        b.append(0x06)  # == 0
        return bytes(b)

    # 7. CanExecuteCounter()
    if cond == "CanExecuteCounter()":
        b.extend(_pack_call(0x70E0, pop_a=False))
        return bytes(b)

    # 8. Compound top-level (A and B) / (A or B)
    # Strip outer parens if balanced
    s_strip = cond
    while s_strip.startswith("(") and s_strip.endswith(")"):
        depth = 0
        bal = True
        for ci, ch in enumerate(s_strip):
            if ch == "(": depth += 1
            elif ch == ")": depth -= 1
            if depth == 0 and ci < len(s_strip) - 1:
                bal = False
                break
        if bal:
            s_strip = s_strip[1:-1].strip()
        else:
            break

    depth = 0
    for ci in range(len(s_strip) - 5):
        ch = s_strip[ci]
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        elif depth == 0:
            if s_strip[ci:ci+5] == " and ":
                lhs_b = encode_single_condition_expr(s_strip[:ci])
                rhs_b = encode_single_condition_expr(s_strip[ci+5:])
                if lhs_b and rhs_b:
                    return lhs_b + rhs_b + b"\x02"
            elif s_strip[ci:ci+4] == " or ":
                lhs_b = encode_single_condition_expr(s_strip[:ci])
                rhs_b = encode_single_condition_expr(s_strip[ci+4:])
                if lhs_b and rhs_b:
                    return lhs_b + rhs_b + b"\x01"

    def _encode_scalar_operand(op_str: str) -> bytes:
        os_s = op_str.strip()
        while os_s.startswith("(") and os_s.endswith(")"):
            os_s = os_s[1:-1].strip()
        if re.match(r"^-?\d+$", os_s):
            return _pack_pushii(int(os_s))
        m_v = re.match(r"^var_([0-9A-Fa-f]+)$", os_s, re.IGNORECASE)
        if m_v:
            return _pack_pushv(int(m_v.group(1), 16))
        m_gp = re.match(r"^GetProperty\(\s*(var_[0-9A-Fa-f]+|-?\d+)\s*,\s*(-?\d+)\s*\)$", os_s)
        if m_gp:
            t_b = _encode_scalar_operand(m_gp.group(1))
            p_b = _pack_pushii(int(m_gp.group(2)))
            return t_b + p_b + _pack_call(0x700F, pop_a=False)
        m_rng = re.match(r"^GetRandomValue\(\)\s*%\s*(\d+)$", os_s)
        if m_rng:
            return _pack_call(0x00A9, pop_a=False) + _pack_pushii(int(m_rng.group(1))) + b"\x18"
        if os_s == "GetLastActionId()":
            return _pack_call(0x7019, pop_a=False)
        return b""

    # 9. General Variable / Property / Scalar Comparison: e.g. "Phase / State: var_00 == 1", "var_10 > var_12", "GetProperty(var_04, 47) == 0"
    clean_cond = re.sub(r"^(?:Phase / State:|Turn Step:)\s*", "", s_strip).strip()
    m_cmp = re.match(r"^(.+?)\s*(==|!=|<=|>=|<|>)\s*(.+)$", clean_cond)
    if m_cmp:
        lhs_b = _encode_scalar_operand(m_cmp.group(1))
        op_s = m_cmp.group(2)
        rhs_b = _encode_scalar_operand(m_cmp.group(3))
        if lhs_b and rhs_b:
            return lhs_b + rhs_b + bytes([OP_STR_TO_BYTE.get(op_s, 0x06)])

    # 10. Bare GetProperty(t, p) truthy check
    bare_b = _encode_scalar_operand(clean_cond)
    if bare_b:
        return bare_b

    return b""


AI_RULE_TEMPLATES = {
    "🔄 3-Turn Attack Rotation (Turn 1 -> 2 -> 3 -> Loop)": [
        {
            "condition": "Turn Step: var_01 == 0",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12354,  # Fire
            "target": "Random Alive Party Member",
            "chance": 100,
            "var_op": "Set",
            "var_name": "var_01",
            "var_val": 1,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Turn Step: var_01 == 1",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12356,  # Thunder
            "target": "Random Alive Party Member",
            "chance": 100,
            "var_op": "Set",
            "var_name": "var_01",
            "var_val": 2,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Always",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 16384,  # Attack
            "target": "All Active Party",
            "chance": 100,
            "var_op": "Reset",
            "var_name": "var_01",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
    ],
    "🔥 Boss Phase Shift at HP < 50% (Buff + Phase 1)": [
        {
            "condition": "Self HP < 50%",
            "extra_conditions": ["Phase / State: var_00 == 0"],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12339,  # Haste
            "target": "Self",
            "chance": 100,
            "var_op": "Set",
            "var_name": "var_00",
            "var_val": 1,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Phase / State: var_00 == 1",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12362,  # Firaga
            "target": "All Active Party",
            "chance": 50,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Always",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 16384,  # Attack
            "target": "Random Alive Party Member",
            "chance": 100,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
    ],
    "🛡 Counterattack: Physical & Magical Retaliation (For Counter / React Hook)": [
        {
            "condition": "Counter: Took Damage (Hit > 0)",
            "extra_conditions": ["Counter: Hit by Physical Attack"],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 16384,  # Physical Counter
            "target": "Last Attacker (Counter)",
            "chance": 100,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Counter: Took Damage (Hit > 0)",
            "extra_conditions": ["Counter: Hit by Magical Attack"],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12350,  # Dispel / Magic Counter
            "target": "Last Attacker (Counter)",
            "chance": 100,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
    ],
    "✨ Tactical Support (Dispel Party Buffs & Self-Heal)": [
        {
            "condition": "Self HP < 33%",
            "extra_conditions": ["Self: Not Regenerating"],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12332,  # Regen
            "target": "Self",
            "chance": 100,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Party: Anyone Has Reflect",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 12350,  # Dispel
            "target": "Party Member With Reflect",
            "chance": 100,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
        {
            "condition": "Always",
            "extra_conditions": [],
            "logic_op": "AND",
            "phase_var": "",
            "phase_op": "==",
            "phase_val": 0,
            "action_id": 16384,  # Attack
            "target": "Lowest HP Party Member",
            "chance": 100,
            "var_op": "None",
            "var_name": "",
            "var_val": 0,
            "flow": "Return",
            "is_counter_exec": False,
        },
    ],
}


def encode_rule_condition(cond_type: str, jump_target_idx: int, extra_conditions=None, logic_op="AND", phase_var="", phase_op="==", phase_val=0) -> bytes:
    """
    Encodes a complete rule condition (including optional phase gate and composite AND/OR conditions)
    followed by POPXNCJMP (0xD7) to jump_target_idx if false.
    """
    exprs = []
    if phase_var and str(phase_var).strip() and str(phase_var).strip() != "Any":
        v_idx = _parse_var_index(phase_var)
        exprs.append(encode_single_condition_expr(f"var_{v_idx:02X} {phase_op} {int(phase_val)}"))

    main_expr = encode_single_condition_expr(cond_type)
    if main_expr:
        exprs.append(main_expr)

    if extra_conditions:
        for ec in extra_conditions:
            e_bytes = encode_single_condition_expr(ec)
            if e_bytes:
                exprs.append(e_bytes)

    exprs = [e for e in exprs if e]
    if not exprs:
        return b""

    b = bytearray(exprs[0])
    comb_op = 0x01 if str(logic_op).upper() == "OR" else 0x02  # 0x01 = OPLOR, 0x02 = OPLAND
    for next_e in exprs[1:]:
        b.extend(next_e)
        b.append(comb_op)

    b.extend(struct.pack("<BH", 0xD7, int(jump_target_idx) & 0xFFFF))  # POPXNCJMP
    return bytes(b)


def encode_target_selection(target_str: str) -> bytes:
    """
    Encodes target selection onto the Atel stack so the resulting target bitmask
    is on top of the stack (ready for ExecuteAction 0x700B or 0x705A).
    Never overwrites monster local variables (var_XX)!
    """
    t = (target_str or "Random Alive Party Member").strip()
    b = bytearray()

    if t in ("Random Alive Party Member", "Target", "Random Party Member"):
        b.extend(_pack_pushii(-14))
        b.extend(_pack_pushii(4))
        b.extend(_pack_pushii(0))
        b.extend(_pack_pushii(0))
        b.extend(_pack_call(0x7010, pop_a=False))
        return bytes(b)

    if t in ("All Active Party", "Party", "All Party"):
        b.extend(_pack_pushii(-14))
        return bytes(b)

    if t == "Self":
        b.extend(_pack_pushii(-13))
        return bytes(b)

    if t in ("All Allied Monsters", "All Allies"):
        b.extend(_pack_pushii(-15))
        return bytes(b)

    if t in ("Last Attacker (Counter)", "Last Attacker"):
        b.extend(_pack_pushii(-17))
        return bytes(b)

    if t == "Provoker":
        b.extend(_pack_pushii(-13))
        b.extend(_pack_pushii(257))
        b.extend(_pack_call(0x700F, pop_a=False))
        return bytes(b)

    # Lowest / Highest HP or MP Party Member
    extremum_map = {
        "Lowest HP Party Member":  (0, 2),
        "Highest HP Party Member": (0, 1),
        "Lowest MP Party Member":  (1, 2),
        "Highest MP Party Member": (1, 1),
    }
    if t in extremum_map:
        prop_id, mode_id = extremum_map[t]
        # First filter alive party into -16 (CALLPOPA 0x7010(-14, 4, 0, 0))
        b.extend(_pack_pushii(-14))
        b.extend(_pack_pushii(4))
        b.extend(_pack_pushii(0))
        b.extend(_pack_pushii(0))
        b.extend(_pack_call(0x7010, pop_a=True))
        # Then select min/max of prop_id from -16 (CALL 0x7010(-16, prop_id, 0, mode_id))
        b.extend(_pack_pushii(-16))
        b.extend(_pack_pushii(prop_id))
        b.extend(_pack_pushii(0))
        b.extend(_pack_pushii(mode_id))
        b.extend(_pack_call(0x7010, pop_a=False))
        return bytes(b)

    # Status-filtered party member targeting
    status_target_map = {
        "Party Member With Reflect":     (37, 1),
        "Party Member Without Reflect":  (37, 0),
        "Party Member With Haste":       (33, 1),
        "Party Member Without Haste":    (33, 0),
        "Party Member With Protect":     (36, 1),
        "Party Member Without Protect":  (36, 0),
        "Party Member With Shell":       (35, 1),
        "Party Member Without Shell":    (35, 0),
        "Party Member Without Poison":   (9,  0),
        "Party Member Without Silence":  (7,  0),
        "Party Member Without Darkness": (8,  0),
    }
    if t in status_target_map:
        st_prop, st_val = status_target_map[t]
        b.extend(_pack_pushii(-14))
        b.extend(_pack_pushii(st_prop))
        b.extend(_pack_pushii(st_val))
        b.extend(_pack_pushii(0))
        b.extend(_pack_call(0x7010, pop_a=False))
        return bytes(b)

    # Specific Character or Monster Slot
    if t in NAME_TO_CHAR_MASK:
        b.extend(_pack_pushii(NAME_TO_CHAR_MASK[t]))
        return bytes(b)

    # Custom integer mask fallback
    try:
        mask_val = int(t, 0)
        b.extend(_pack_pushii(mask_val))
        return bytes(b)
    except ValueError:
        b.extend(_pack_pushii(-14))
        b.extend(_pack_pushii(4))
        b.extend(_pack_pushii(0))
        b.extend(_pack_pushii(0))
        b.extend(_pack_call(0x7010, pop_a=False))
        return bytes(b)


def compile_rules_to_bytecode(rules, jump_index_offset=0, function_start_offset=0):
    """
    Compiles a list of visual AI rules into valid FFX Atel bytecode and a jump table.
    Correctly passes (target_mask, ability_id) to ExecuteAction (0x700B / 0x705A),
    supports composite conditions, phase/state gates, variable mutations, and Return/Continue control flow.
    """
    bytecode = bytearray()
    jumps = []

    for rule in rules:
        cond_type = rule.get("condition", "Always")
        extra_conds = rule.get("extra_conditions", [])
        logic_op = rule.get("logic_op", "AND")
        phase_var = rule.get("phase_var", "")
        phase_op = rule.get("phase_op", "==")
        phase_val = rule.get("phase_val", 0)
        chance = int(rule.get("chance", 100))

        chance_failed_jump_idx = None
        if 0 < chance < 100:
            bytecode.extend(_pack_call(0x00A9, pop_a=False))  # CALL GetRandomValue()
            bytecode.extend(_pack_pushii(100))                # PUSHII 100
            bytecode.append(0x18)                             # OPMOD
            bytecode.extend(_pack_pushii(chance))             # PUSHII chance
            bytecode.append(0x0B)                             # OPLS (<)
            chance_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode.extend(struct.pack("<BH", 0xD7, (jump_index_offset + chance_failed_jump_idx) & 0xFFFF))

        cond_failed_jump_idx = None
        cond_bytes = encode_rule_condition(
            cond_type,
            jump_index_offset + len(jumps),
            extra_conditions=extra_conds,
            logic_op=logic_op,
            phase_var=phase_var,
            phase_op=phase_op,
            phase_val=phase_val,
        )
        if cond_bytes:
            cond_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode.extend(cond_bytes)

        # Optional pre/post state variable mutation
        var_op = rule.get("var_op", "None")
        var_name = rule.get("var_name") or rule.get("var_idx", "")
        var_val = int(rule.get("var_val", 0) or 0)

        # Target & Ability execution
        action_id = int(rule.get("action_id", 16384))
        if action_id == 4:
            # Map generic player Attack ID 4 to FFX's standard monster attack 0x4000 (16384) if selected
            action_id = 16384
        target_str = rule.get("target", "Random Alive Party Member")
        is_counter_exec = bool(rule.get("is_counter_exec", rule.get("is_counter_op", False)))

        if action_id > 0:
            bytecode.extend(encode_target_selection(target_str))
            bytecode.extend(_pack_pushii(action_id))
            exec_call_id = 0x705A if is_counter_exec else 0x700B
            bytecode.extend(_pack_call(exec_call_id, pop_a=True))

        # Apply Variable Update if configured
        if var_op and var_op != "None" and var_name:
            v_idx = _parse_var_index(var_name)
            if var_op == "Set":
                bytecode.extend(_pack_pushii(var_val))
                bytecode.extend(_pack_popv(v_idx))
            elif var_op == "Add":
                bytecode.extend(_pack_pushv(v_idx))
                bytecode.extend(_pack_pushii(var_val if var_val != 0 else 1))
                bytecode.append(0x14)  # OPADD
                bytecode.extend(_pack_popv(v_idx))
            elif var_op == "Reset":
                bytecode.extend(_pack_pushii(0))
                bytecode.extend(_pack_popv(v_idx))

        # Control flow: Return (stop after executing rule) vs Continue (fall through to next rule)
        flow_mode = rule.get("flow", "Return")
        if flow_mode != "Continue":
            bytecode.append(0x3C)  # RET

        next_rule_offset = function_start_offset + len(bytecode)
        if chance_failed_jump_idx is not None:
            jumps[chance_failed_jump_idx] = next_rule_offset
        if cond_failed_jump_idx is not None:
            jumps[cond_failed_jump_idx] = next_rule_offset

    bytecode.append(0x3C)  # Final RET
    return bytes(bytecode), jumps


def compile_rules_to_atel(rules, script_id="001"):
    """
    Compiles a standalone Atel Chunk 0 binary from visual rules.
    """
    func0_bytes = b"\x3C"             # RET
    func1_bytes = b"\xD8\x5F\x00\x3C" # CALLPOPA halt(), RET
    bytecode2, jumps = compile_rules_to_bytecode(rules, jump_index_offset=0, function_start_offset=5)

    full_bytecode = func0_bytes + func1_bytes + bytecode2
    bytecode_len = len(full_bytecode)

    header_size = 0x38
    worker_offsets_size = 0x04
    worker_header_size = 0x34

    funcs_offset = header_size + worker_offsets_size + worker_header_size
    funcs_size = 3 * 4

    jumps_offset = funcs_offset + funcs_size
    jumps_size = len(jumps) * 4

    creator_tag_addr = jumps_offset + jumps_size
    creator_tag_str = b"Antigravity\x00"

    script_id_addr = creator_tag_addr + len(creator_tag_str)
    script_id_str = script_id.encode("utf-8") + b"\x00"

    bytecode_start = script_id_addr + len(script_id_str)
    padding = (4 - (bytecode_start % 4)) % 4
    bytecode_start += padding

    data = bytearray(bytecode_start + bytecode_len)

    struct.pack_into("<I", data, 0x00, bytecode_len)
    struct.pack_into("<I", data, 0x08, creator_tag_addr)
    struct.pack_into("<I", data, 0x0C, script_id_addr)
    struct.pack_into("<I", data, 0x10, len(data))
    struct.pack_into("<I", data, 0x30, bytecode_start)
    struct.pack_into("<H", data, 0x34, 1)

    worker_0_offset = header_size + worker_offsets_size
    struct.pack_into("<I", data, 0x38, worker_0_offset)

    struct.pack_into("<H", data, worker_0_offset + 0x00, 1)
    struct.pack_into("<H", data, worker_0_offset + 0x02, 8)
    struct.pack_into("<H", data, worker_0_offset + 0x04, 0)
    struct.pack_into("<H", data, worker_0_offset + 0x06, 0)
    struct.pack_into("<H", data, worker_0_offset + 0x08, 3)
    struct.pack_into("<H", data, worker_0_offset + 0x0A, len(jumps))
    struct.pack_into("<I", data, worker_0_offset + 0x14, funcs_offset)
    struct.pack_into("<I", data, worker_0_offset + 0x20, funcs_offset)
    struct.pack_into("<I", data, worker_0_offset + 0x24, jumps_offset)

    struct.pack_into("<I", data, funcs_offset + 0, 0)
    struct.pack_into("<I", data, funcs_offset + 4, 1)
    struct.pack_into("<I", data, funcs_offset + 8, 5)

    for i, jump_addr in enumerate(jumps):
        struct.pack_into("<I", data, jumps_offset + i * 4, jump_addr)

    data[creator_tag_addr : creator_tag_addr + len(creator_tag_str)] = creator_tag_str
    data[script_id_addr : script_id_addr + len(script_id_str)] = script_id_str
    data[bytecode_start : bytecode_start + bytecode_len] = full_bytecode

    return bytes(data)


def adjust_file_pointers(data, threshold, shift):
    """Legacy helper retained for compatibility."""
    def adj_32(offset):
        val = struct.unpack("<I", data[offset:offset+4])[0]
        if val >= threshold:
            struct.pack_into("<I", data, offset, val + shift)
            
    adj_32(0x08)
    adj_32(0x0C)
    adj_32(0x30)
    
    namespace_count = struct.unpack("<H", data[0x34:0x36])[0]
    for i in range(namespace_count):
        w_off_addr = 0x38 + i * 4
        adj_32(w_off_addr)
        w_off = struct.unpack("<I", data[w_off_addr:w_off_addr+4])[0]
        adj_32(w_off + 0x14)
        adj_32(w_off + 0x18)
        adj_32(w_off + 0x1C)
        adj_32(w_off + 0x20)
        adj_32(w_off + 0x24)
        adj_32(w_off + 0x2C)
        adj_32(w_off + 0x30)


def rebuild_chunk0_binary(original_bytes: bytes, updated_bytecode: bytes, updated_workers: list) -> bytes:
    """
    Losslessly reconstructs a monster Chunk 0 Atel binary with updated bytecode and worker func/jump tables.
    Verified 361/361 bit-for-bit identical on all vanilla FFX monster files.
    """
    c0 = original_bytes
    ev_off = struct.unpack_from("<I", c0, 0x20)[0]
    fj_off = struct.unpack_from("<I", c0, 0x28)[0]
    sh_hdr = struct.unpack_from("<I", c0, 0x2C)[0]
    bc_start = struct.unpack_from("<I", c0, 0x30)[0]
    w0_off = struct.unpack_from("<I", c0, 0x38)[0]
    orig_sh_data = struct.unpack_from("<I", c0, w0_off + 0x30)[0]

    # Standalone / synthetic Chunk 0 fallback (when shared_data is not present)
    if orig_sh_data == 0 or fj_off == 0 or orig_sh_data >= len(c0):
        out = bytearray(c0[:bc_start])
        out.extend(updated_bytecode)
        struct.pack_into("<I", out, 0x00, len(updated_bytecode))
        struct.pack_into("<I", out, 0x10, len(out))
        return bytes(out)

    out = bytearray(c0[:bc_start])
    out.extend(updated_bytecode)
    new_sh_data = (len(out) + 0x3F) & ~0x3F
    out.extend(b"\x00" * (new_sh_data - len(out)))
    sh_delta = new_sh_data - orig_sh_data

    mid = bytearray(c0[orig_sh_data:fj_off])
    for rel in (0x68, 0x6C, 0xE4 + 0x0C, 0xE4 + 0x10, 0xE4 + 0x28, 0xE4 + 0x3C):
        if rel + 4 <= len(mid):
            val = struct.unpack_from("<I", mid, rel)[0]
            struct.pack_into("<I", mid, rel, val + sh_delta)
    out.extend(mid)

    new_fj_off = len(out)
    for i, w in enumerate(updated_workers):
        w_off = struct.unpack_from("<I", out, 0x38 + i * 4)[0]
        struct.pack_into("<H", out, w_off + 0x08, len(w["funcs"]))
        struct.pack_into("<H", out, w_off + 0x0A, len(w["jumps"]))
        struct.pack_into("<I", out, w_off + 0x20, len(out))
        for f_addr in w["funcs"]:
            out.extend(struct.pack("<I", f_addr))
        struct.pack_into("<I", out, w_off + 0x24, len(out))
        for j_addr in w["jumps"]:
            out.extend(struct.pack("<I", j_addr))
        struct.pack_into("<I", out, w_off + 0x30, new_sh_data)

    aligned_total = (len(out) + 0x0F) & ~0x0F
    out.extend(b"\x00" * (aligned_total - len(out)))

    struct.pack_into("<I", out, 0x00, len(updated_bytecode))
    struct.pack_into("<I", out, 0x10, len(out))
    struct.pack_into("<I", out, 0x20, ev_off + sh_delta)
    struct.pack_into("<I", out, 0x28, new_fj_off)
    struct.pack_into("<I", out, 0x2C, sh_hdr + sh_delta)
    return bytes(out)


def inject_rules(original_bytes, rules, worker_idx=None, func_idx=None, chunk1_bytes=None, slot_idx=0, hook_key=None):
    """
    Compiles visual AI rules and injects them into the specified (worker_idx, func_idx) or
    auto-resolved AI Worker & Event Hook Slot from Chunk 1, rebuilding Chunk 0 losslessly.
    """
    disasm = AtelDisassembler(original_bytes)
    if not disasm.workers:
        raise ValueError("No Atel workers found in Chunk 0.")

    if hook_key is not None:
        for s_idx, k, _, _ in AI_EVENT_HOOK_DEFS:
            if k == hook_key:
                slot_idx = s_idx
                break

    if worker_idx is None or func_idx is None:
        ai_map = parse_chunk1_ai_map(chunk1_bytes, original_bytes)
        if worker_idx is None:
            worker_idx = ai_map["ai_worker_idx"]
        if func_idx is None:
            mapped = ai_map["slots"][slot_idx] if 0 <= slot_idx < len(ai_map["slots"]) else 0xFFFF
            func_idx = mapped if mapped != 0xFFFF else 2

    if worker_idx >= len(disasm.workers):
        worker_idx = len(disasm.workers) - 1
    worker = disasm.workers[worker_idx]
    if func_idx >= len(worker["funcs"]):
        func_idx = len(worker["funcs"]) - 1

    S = worker["funcs"][func_idx]

    # Check if S is shared with another function stub in the same worker
    shared_func_indices = [fi for fi, faddr in enumerate(worker["funcs"]) if faddr == S and fi != func_idx]

    all_entry_points = sorted(set(addr for w in disasm.workers for addr in w["funcs"]))
    idx = all_entry_points.index(S)
    E = all_entry_points[idx + 1] if idx + 1 < len(all_entry_points) else len(disasm.bytecode)

    # Identify jump slots in worker["jumps"] that belonged exclusively to [S, E)
    old_j_indices = [ji for ji, jaddr in enumerate(worker["jumps"]) if S <= jaddr < E] if not shared_func_indices else []

    # Compile new function bytecode first with placeholder jump_index_offset=0
    raw_bc, raw_jumps = compile_rules_to_bytecode(rules, jump_index_offset=0, function_start_offset=S)

    # Build jump index mapping: reuse old_j_indices first, append any extra to the end of worker["jumps"]
    jump_remap = {}
    new_worker_jumps = list(worker["jumps"])
    for k in range(len(raw_jumps)):
        if k < len(old_j_indices):
            jump_remap[k] = old_j_indices[k]
        else:
            jump_remap[k] = len(new_worker_jumps)
            new_worker_jumps.append(0)

    # Patch jump indices inside raw_bc
    patched_bc = bytearray(raw_bc)
    cur = 0
    while cur < len(patched_bc):
        op = patched_bc[cur]
        cur += 1
        if op >= 0x80:
            if cur + 2 > len(patched_bc):
                break
            arg = patched_bc[cur] | (patched_bc[cur + 1] << 8)
            if op in (0xB0, 0xB1, 0xB2, 0xD5, 0xD6, 0xD7) and arg in jump_remap:
                struct.pack_into("<H", patched_bc, cur, jump_remap[arg])
            cur += 2

    # If S was shared with other empty stub functions, preserve a 1-byte RET (0x3C) at the end for them
    stub_ret_offset = None
    if shared_func_indices:
        stub_ret_offset = S + len(patched_bc) - 1  # Points to final 0x3C RET of patched_bc

    new_func_bc = bytes(patched_bc)
    delta = len(new_func_bc) - (E - S)

    # Update bytecode buffer
    updated_bytecode = disasm.bytecode[:S] + new_func_bc + disasm.bytecode[E:]

    # Update all workers' funcs and jumps
    updated_workers = []
    for w_i, w in enumerate(disasm.workers):
        w_copy = dict(w)
        new_funcs = []
        for f_i, f_addr in enumerate(w["funcs"]):
            if w_i == worker_idx and f_i == func_idx:
                new_funcs.append(S)
            elif w_i == worker_idx and f_i in shared_func_indices and stub_ret_offset is not None:
                new_funcs.append(stub_ret_offset)
            elif f_addr > S:
                new_funcs.append(f_addr + delta)
            else:
                new_funcs.append(f_addr)
        w_copy["funcs"] = new_funcs

        if w_i == worker_idx:
            # First shift existing jumps outside [S, E)
            shifted_jumps = []
            for j_i, j_addr in enumerate(new_worker_jumps):
                if j_i < len( w["jumps"]) and j_i not in old_j_indices:
                    shifted_jumps.append(j_addr + delta if j_addr > S else j_addr)
                else:
                    shifted_jumps.append(j_addr)
            # Write our new jump targets
            for k, target_addr in enumerate(raw_jumps):
                shifted_jumps[jump_remap[k]] = target_addr
            # Point any leftover unused old_j_indices to the final RET of new_func_bc
            for leftover_k in range(len(raw_jumps), len(old_j_indices)):
                shifted_jumps[old_j_indices[leftover_k]] = S + len(new_func_bc) - 1
            w_copy["jumps"] = shifted_jumps
        else:
            w_copy["jumps"] = [j_addr + delta if j_addr > S else j_addr for j_addr in w["jumps"]]

        updated_workers.append(w_copy)

    return rebuild_chunk0_binary(original_bytes, updated_bytecode, updated_workers)


def enable_chunk1_hook_slot(chunk0_bytes: bytes, chunk1_bytes: bytes, slot_idx: int):
    """
    If slot_idx (0..8) in Chunk 1 is currently unmapped (0xFFFF), appends a new 1-byte RET (0x3C)
    function to the AI worker in Chunk 0 and binds slot_idx in Chunk 1 to the new function index.
    Returns (new_chunk0_bytes, new_chunk1_bytes, ai_worker_idx, new_func_idx).
    """
    ai_map = parse_chunk1_ai_map(chunk1_bytes, chunk0_bytes)
    ai_w = ai_map["ai_worker_idx"]
    cur_f = ai_map["slots"][slot_idx] if 0 <= slot_idx < len(ai_map["slots"]) else 0xFFFF
    if cur_f != 0xFFFF:
        return chunk0_bytes, chunk1_bytes, ai_w, cur_f

    disasm = AtelDisassembler(chunk0_bytes)
    w = disasm.workers[ai_w]

    # Determine end of AI worker's last function
    all_eps = sorted(set(addr for ow in disasm.workers for addr in ow["funcs"]))
    last_s = max(w["funcs"]) if w["funcs"] else 0
    idx = all_eps.index(last_s) if last_s in all_eps else -1
    insert_pos = all_eps[idx + 1] if (idx >= 0 and idx + 1 < len(all_eps)) else len(disasm.bytecode)

    updated_bytecode = disasm.bytecode[:insert_pos] + b"\x3C" + disasm.bytecode[insert_pos:]
    new_func_idx = len(w["funcs"])

    updated_workers = []
    for w_i, ow in enumerate(disasm.workers):
        w_copy = dict(ow)
        w_copy["funcs"] = [addr + 1 if addr >= insert_pos else addr for addr in ow["funcs"]]
        if w_i == ai_w:
            w_copy["funcs"].append(insert_pos)
        w_copy["jumps"] = [addr + 1 if addr >= insert_pos else addr for addr in ow["jumps"]]
        updated_workers.append(w_copy)

    new_c0 = rebuild_chunk0_binary(chunk0_bytes, updated_bytecode, updated_workers)
    new_c1 = bytearray(chunk1_bytes)
    role_off = ai_map["role_table_offset"]
    if role_off is not None and role_off + 2 + (slot_idx + 1) * 2 <= len(new_c1):
        struct.pack_into("<H", new_c1, role_off + 2 + slot_idx * 2, new_func_idx)

    return new_c0, bytes(new_c1), ai_w, new_func_idx


# ==============================================================================
# AST / SYMBOLIC STACK DECOMPILER FOR VISUAL AI RULES
# ==============================================================================

def _translate_ast_condition(expr: str) -> tuple:
    """
    Translates a raw Atel symbolic boolean expression into (human_condition_str, chance_or_None, phase_tuple_or_None).
    """
    import re
    s = expr.strip()
    while s.startswith("(") and s.endswith(")"):
        # Check balanced parens
        depth = 0
        balanced = True
        for ch_i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0 and ch_i < len(s) - 1:
                balanced = False
                break
        if balanced:
            s = s[1:-1].strip()
        else:
            break

    # 1. Random chance: (GetRandomValue() % 100) < N or > N
    m_rng100 = re.match(r"^\(GetRandomValue\(\)\s*%\s*100\)\s*(<|<=|>|>=)\s*(\d+)$", s)
    if m_rng100:
        op, val = m_rng100.group(1), int(m_rng100.group(2))
        if op in ("<", "<="):
            return ("Always", max(1, min(99, val)), None)
        else:
            return ("Always", max(1, min(99, 100 - val)), None)

    m_rng_mod = re.match(r"^\(GetRandomValue\(\)\s*%\s*(\d+)\)\s*==\s*(\d+)$", s)
    if m_rng_mod:
        mod_n = max(2, int(m_rng_mod.group(1)))
        return ("Always", max(1, int(round(100.0 / mod_n))), None)

    # 2. Self HP / MP fraction: GetProperty(-13, 0) < (GetProperty(-13, 2) / N)
    m_hp_div = re.search(r"GetProperty\(-13,\s*(0|1)\)\s*(<|<=|>|>=)\s*\(GetProperty\(-13,\s*(?:2|3)\)\s*/\s*(\d+)\)", s)
    if m_hp_div:
        stat = "HP" if m_hp_div.group(1) == "0" else "MP"
        op = "<" if m_hp_div.group(2) in ("<", "<=") else ">="
        div_n = max(1, int(m_hp_div.group(3)))
        pct = 33 if div_n == 3 else int(round(100.0 / div_n))
        return (f"Self {stat} {op} {pct}%", None, None)

    m_hp_pct = re.search(r"GetProperty\(-13,\s*(0|1)\)\s*(<|<=|>|>=)\s*\(\(GetProperty\(-13,\s*(?:2|3)\)\s*/\s*100\)\s*\*\s*(\d+)\)", s)
    if m_hp_pct:
        stat = "HP" if m_hp_pct.group(1) == "0" else "MP"
        op = "<" if m_hp_pct.group(2) in ("<", "<=") else ">="
        pct = int(m_hp_pct.group(3))
        return (f"Self {stat} {op} {pct}%", None, None)

    # Legacy synthetic HP/MP check: GetProperty(-14, 21) < 50
    m_leg_hp = re.search(r"GetProperty\(-14,\s*(21|22)\)\s*(<|<=)\s*(\d+)", s)
    if m_leg_hp:
        stat = "HP" if m_leg_hp.group(1) == "21" else "MP"
        pct = int(m_leg_hp.group(3))
        return (f"Self {stat} < {pct}%", None, None)

    # 3. CheckTargetMatch (0x701E)
    m_701e = re.search(r"CheckTargetMatch\(-14,\s*(-?\d+)\)(?:\s*(==|!=)\s*(\d+))?", s)
    if m_701e:
        st_id = int(m_701e.group(1))
        op = m_701e.group(2) or "!="
        val = int(m_701e.group(3)) if m_701e.group(3) is not None else 1
        is_neg = (op == "==" and val == 0) or (op == "!=" and val == 1 and s.startswith("!"))
        if st_id == -20:
            return ("Party: Has Valid Frontline Target", None, None)
        st_map_pos = {
            37: "Party: Anyone Has Reflect",
            33: "Party: Anyone Has Haste",
            36: "Party: Anyone Has Protect",
            35: "Party: Anyone Has Shell",
            39: "Party: Anyone Has Regen",
            9:  "Target: Not Poisoned" if is_neg else "Party: Anyone Is Poisoned",
            7:  "Target: Not Silenced" if is_neg else "Party: Anyone Is Silenced",
            8:  "Target: Not Blind" if is_neg else "Party: Anyone Is Blind",
            6:  "Party: Anyone Is Sleeping",
            5:  "Party: Anyone Is Petrified",
        }
        if st_id in st_map_pos:
            return (st_map_pos[st_id], None, None)

    # 4. Counter / Last Action Checks
    if "GetProperty(-13, 166) > 0" in s or "GetProperty(-13, 166) != 0" in s:
        return ("Counter: Took Damage (Hit > 0)", None, None)

    m_abil_prop = re.search(r"GetAbilityProperty\(.*,\s*10\)\s*==\s*(\d+)", s)
    if m_abil_prop:
        atype = int(m_abil_prop.group(1))
        if atype == 1:
            return ("Counter: Hit by Physical Attack", None, None)
        elif atype == 2:
            return ("Counter: Hit by Magical Attack", None, None)

    m_last_act = re.search(r"GetLastActionId\(\)\s*(==|!=)\s*(\d+)", s)
    if m_last_act:
        return (f"Counter: Last Action {m_last_act.group(1)} {m_last_act.group(2)}", None, None)

    # 5. Self / Ally GetProperty checks
    m_self_prop = re.match(r"^GetProperty\((-?\d+),\s*(\d+)\)(?:\s*(==|!=|<|<=|>|>=)\s*(-?\d+))?$", s)
    if m_self_prop:
        t_id = int(m_self_prop.group(1))
        p_id = int(m_self_prop.group(2))
        op = m_self_prop.group(3) or "!="
        val = int(m_self_prop.group(4)) if m_self_prop.group(4) is not None else 1
        if t_id == -13:
            if p_id in (43, 18) and ((op == "!=" and val == 0) or (op == "==" and val == 1)):
                return ("Self: Is Provoked", None, None)
            if p_id == 7 and op != "==":
                return ("Self: Is Silenced", None, None)
            if p_id == 33 and op == "==" and val == 0:
                return ("Self: Not Hasted", None, None)
            if p_id == 36 and op == "==" and val == 0:
                return ("Self: Not Protected", None, None)
            if p_id == 35 and op == "==" and val == 0:
                return ("Self: Not Shelled", None, None)
            if p_id == 37 and op == "==" and val == 0:
                return ("Self: Not Reflecting", None, None)
            if p_id == 39 and op == "==" and val == 0:
                return ("Self: Not Regenerating", None, None)
        if t_id in (20, 21, 22) and p_id == 4:
            slot_num = t_id - 20
            state_w = "Dead" if val == 1 else "Alive"
            return (f"Allies: Monster Slot {slot_num} {state_w}", None, None)
        return (f"GetProperty({t_id}, {p_id}) {op} {val}", None, None)

    # 6. Variable comparison: var_XX op val or (val == rY)
    m_var = re.match(r"^var_([0-9A-Fa-f]+)\s*(==|!=|<=|>=|<|>)\s*(-?\d+)$", s)
    if m_var:
        v_hex = m_var.group(1).upper()
        op = m_var.group(2)
        val = int(m_var.group(3))
        v_idx = int(v_hex, 16)
        if v_idx == 0 and op == "==" and 0 <= val <= 3:
            return (f"Phase / State: var_00 == {val}", None, (f"var_{v_hex}", op, val))
        if v_idx in (1, 2) and op == "==" and 0 <= val <= 4:
            return (f"Turn Step: var_{v_hex} == {val}", None, (f"var_{v_hex}", op, val))
        return (f"var_{v_hex} {op} {val}", None, (f"var_{v_hex}", op, val))

    return (s, None, None)


def _translate_ast_target(target_expr: str, var_bindings: dict) -> str:
    """
    Translates a target expression (or variable bound to a target expression) into a human-readable TARGET_PRESETS string.
    """
    import re
    t = str(target_expr).strip()
    # Resolve variable binding if t is var_XX or rI0
    visited = set()
    while t in var_bindings and t not in visited:
        visited.add(t)
        t = str(var_bindings[t]).strip()

    if "FilterTargets(-16, 0, 0, 2)" in t:
        return "Lowest HP Party Member"
    if "FilterTargets(-16, 0, 0, 1)" in t:
        return "Highest HP Party Member"
    if "FilterTargets(-16, 1, 0, 2)" in t:
        return "Lowest MP Party Member"
    if "FilterTargets(-16, 1, 0, 1)" in t:
        return "Highest MP Party Member"

    m_ft = re.search(r"FilterTargets\(\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", t)
    if m_ft:
        pool, prop, val, mode = (int(m_ft.group(1)), int(m_ft.group(2)), int(m_ft.group(3)), int(m_ft.group(4)))
        if pool == -14 and prop == 4 and val == 0 and mode == 0:
            return "Random Alive Party Member"
        st_rev = {
            (37, 1): "Party Member With Reflect",
            (37, 0): "Party Member Without Reflect",
            (33, 1): "Party Member With Haste",
            (33, 0): "Party Member Without Haste",
            (36, 1): "Party Member With Protect",
            (36, 0): "Party Member Without Protect",
            (35, 1): "Party Member With Shell",
            (35, 0): "Party Member Without Shell",
            (9,  0): "Party Member Without Poison",
            (7,  0): "Party Member Without Silence",
            (8,  0): "Party Member Without Darkness",
        }
        if (prop, val) in st_rev:
            return st_rev[(prop, val)]
        if pool == -17:
            return "Last Attacker (Counter)"
        return "Random Alive Party Member"

    if "GetProperty(-13, 257)" in t:
        return "Provoker"

    try:
        ival = int(t, 0)
        if ival == -14:
            return "All Active Party"
        if ival == -13:
            return "Self"
        if ival == -15:
            return "All Allied Monsters"
        if ival == -17:
            return "Last Attacker (Counter)"
        if ival == -16:
            return "Random Alive Party Member"
        if ival in CHAR_MASK_TO_NAME:
            return CHAR_MASK_TO_NAME[ival]
    except ValueError:
        pass

    return "Random Alive Party Member"


def extract_rules_from_function_ast(disasm: AtelDisassembler, worker_idx: int, func_idx: int) -> list:
    """
    Symbolic Stack & Control-Flow AST Rule Extractor for any FFX Monster/Boss AI function.
    Accurately extracts:
      - Direct ExecuteAction (0x700B) and ExecuteCounterAction (0x705A) rules
      - Indirect boss state-machine rules where branches assign `var_ability = 0x3XXX..0x7XXX`
        before jumping to a shared epilogue `ExecuteAction(var_target, var_ability)`
      - Active branch conditions, RNG weights/chances, target filters, and state variable updates.
    """
    import re
    if worker_idx >= len(disasm.workers):
        return []
    worker = disasm.workers[worker_idx]
    if func_idx is None or func_idx >= len(worker["funcs"]):
        return []

    all_eps = sorted(set(addr for w in disasm.workers for addr in w["funcs"]))
    S = worker["funcs"][func_idx]
    idx = all_eps.index(S) if S in all_eps else -1
    E = all_eps[idx + 1] if (idx >= 0 and idx + 1 < len(all_eps)) else len(disasm.bytecode)
    if E <= S + 1:
        return []

    labels = {}
    for li, laddr in enumerate(worker["jumps"]):
        if S <= laddr < E:
            labels.setdefault(laddr, []).append(li)

    # First pass: check if this function uses an indirect epilogue `ExecuteAction(var_T, var_A)`
    # where `var_A` is a variable rather than an immediate integer
    bc = disasm.bytecode[S:E]
    indirect_ability_vars = set()
    indirect_target_vars = set()
    for pos in range(3, len(bc) - 3):
        if bc[pos] in (0xB5, 0xD8) and (bc[pos + 1] | (bc[pos + 2] << 8)) in (0x700B, 0x705A):
            if bc[pos - 3] == 0x9F:
                v_a = bc[pos - 2] | (bc[pos - 1] << 8)
                indirect_ability_vars.add(f"var_{v_a:02X}")
                if pos >= 6 and bc[pos - 6] == 0x9F:
                    v_t = bc[pos - 5] | (bc[pos - 4] << 8)
                    indirect_target_vars.add(f"var_{v_t:02X}")

    # Symbolic simulation over [S, E)
    cur = S
    stack = []
    last_rx = "rX"
    ry_expr = "rY"
    var_bindings = {}
    # active_guards: list of (guard_expr, expire_label_idx)
    active_guards = []
    switch_case_map = {}  # label_idx -> case_expr
    extracted_rules = []

    def current_condition_summary():
        conds = []
        chance = 100
        phase_info = None
        for g_expr, _ in active_guards:
            c_str, rng_c, p_info = _translate_ast_condition(g_expr)
            if rng_c is not None:
                chance = rng_c
            if p_info is not None and phase_info is None:
                phase_info = p_info
            if c_str and c_str != "Always" and c_str not in conds:
                conds.append(c_str)
        primary = conds[0] if conds else "Always"
        extras = conds[1:] if len(conds) > 1 else []
        return primary, extras, chance, phase_info

    while cur < E:
        if cur in labels:
            for li in labels[cur]:
                # Pop guards that jump to this label
                active_guards = [(ge, el) for (ge, el) in active_guards if el != li]
                if li in switch_case_map:
                    active_guards.append((switch_case_map[li], -1))

        op = disasm.bytecode[cur]
        cur += 1
        argv = 0
        argv_s = 0
        if op >= 0x80:
            if cur + 2 > E:
                break
            argv = disasm.bytecode[cur] | (disasm.bytecode[cur + 1] << 8)
            argv_s = argv if argv < 0x8000 else argv - 0x10000
            cur += 2

        if op == 0xAD:
            val = worker["ref_ints"][argv] if argv < len(worker["ref_ints"]) else 0
            stack.append(str(val))
        elif op == 0xAF:
            val = worker["ref_floats"][argv] if argv < len(worker["ref_floats"]) else 0.0
            stack.append(f"{val:.4f}")
        elif op == 0xAE:
            stack.append(str(argv_s))
        elif op == 0x9F:
            stack.append(f"var_{argv:02X}")
        elif op == 0x26:
            stack.append("rA")
        elif op == 0x28:
            stack.append(last_rx)
        elif op == 0x29:
            stack.append(ry_expr)
        elif op in (0x67, 0x68, 0x69, 0x6A):
            stack.append(f"rI{op - 0x67}")
        elif op == 0x25:
            if stack:
                stack.pop()
        elif op == 0x2A:
            last_rx = stack.pop() if stack else "rX"
        elif op == 0x2C:
            ry_expr = stack.pop() if stack else "rY"
        elif op in (0x59, 0x5A, 0x5B, 0x5C):
            val = stack.pop() if stack else "?"
            var_bindings[f"rI{op - 0x59}"] = val
        elif op in (0xA0, 0xA1):
            val = stack.pop() if stack else "?"
            v_name = f"var_{argv:02X}"
            var_bindings[v_name] = val

            # Check if this is an indirect boss ability assignment (e.g., var_06 = 24785)
            if v_name in indirect_ability_vars:
                try:
                    abil_id = int(val, 0)
                except ValueError:
                    abil_id = None
                if abil_id is not None and abil_id >= 4:
                    t_var = next(iter(indirect_target_vars), "-14")
                    target_str = _translate_ast_target(t_var, var_bindings)
                    prim_c, extra_c, chance_v, p_info = current_condition_summary()
                    rule_obj = {
                        "condition": prim_c,
                        "extra_conditions": extra_c,
                        "logic_op": "AND",
                        "phase_var": p_info[0] if p_info else "",
                        "phase_op": p_info[1] if p_info else "==",
                        "phase_val": p_info[2] if p_info else 0,
                        "action_id": abil_id,
                        "target": target_str,
                        "chance": chance_v,
                        "var_op": "None",
                        "var_name": "",
                        "var_val": 0,
                        "flow": "Return",
                        "is_counter_exec": False,
                    }
                    extracted_rules.append(rule_obj)
            else:
                # Check if this updates a state/step variable right after an extracted rule
                if extracted_rules and re.match(r"^\(var_[0-9A-Fa-f]+\s*\+\s*\d+\)$", str(val)):
                    last_r = extracted_rules[-1]
                    if last_r.get("var_op", "None") == "None":
                        last_r["var_op"] = "Add"
                        last_r["var_name"] = v_name
                        last_r["var_val"] = 1
                elif extracted_rules and str(val).lstrip("-").isdigit() and not str(val).startswith("FilterTargets"):
                    ival = int(val)
                    if 0 <= ival <= 10 and v_name not in indirect_target_vars:
                        last_r = extracted_rules[-1]
                        if last_r.get("var_op", "None") == "None":
                            last_r["var_op"] = "Set"
                            last_r["var_name"] = v_name
                            last_r["var_val"] = ival

        elif op in OP_SYMBOLS:
            b = stack.pop() if stack else "?"
            a = stack.pop() if stack else "?"
            # Resolve simple RNG variable alias: e.g. var_03 == 0 where var_03 = (GetRandomValue() % 3)
            if a in var_bindings and "GetRandomValue()" in str(var_bindings[a]):
                a = str(var_bindings[a])
            stack.append(f"({a} {OP_SYMBOLS[op]} {b})")
        elif op == 0x19:
            a = stack.pop() if stack else "?"
            stack.append(f"(!{a})")
        elif op == 0x1C:
            a = stack.pop() if stack else "?"
            stack.append(f"(~{a})")
        elif op == 0xB0:
            # Unconditional jump (often end of switch case or if-else branch)
            active_guards = [g for g in active_guards if g[1] != -1]
        elif op in (0xB1, 0xD6):
            c = stack.pop() if stack else last_rx
            last_rx = c
            # Switch-case dispatch pattern: if (K == rY): goto label_XX
            m_sw = re.match(r"^\((\d+)\s*==\s*(.+)\)$", c)
            if m_sw:
                switch_case_map[argv] = f"{m_sw.group(2)} == {m_sw.group(1)}"
        elif op in (0xB2, 0xD7):
            c = stack.pop() if stack else last_rx
            last_rx = c
            active_guards.append((c, argv))
        elif op in (0xB5, 0xD8):
            raw_name = CALL_TARGET_MAP.get(argv, f"call_{argv:04X}")
            cname = raw_name.split("(")[0]
            nargs = BATTLE_CALL_ARG_COUNTS.get(argv, len(stack))
            args = []
            for _ in range(nargs):
                args.insert(0, stack.pop() if stack else "?")
            call_s = f"{cname}({', '.join(args)})"
            if op == 0xB5:
                stack.append(call_s)
            else:
                if argv == 0x7010:
                    var_bindings["-16"] = call_s
                elif argv in (0x700B, 0x705A) and len(args) == 2:
                    t_arg, a_arg = args[0], args[1]
                    # Resolve ability ID (direct integer or bound variable)
                    abil_str = var_bindings.get(a_arg, a_arg)
                    try:
                        abil_id = int(str(abil_str), 0)
                    except ValueError:
                        abil_id = None

                    if abil_id is not None and abil_id >= 0:
                        target_str = _translate_ast_target(t_arg, var_bindings)
                        prim_c, extra_c, chance_v, p_info = current_condition_summary()
                        extracted_rules.append({
                            "condition": prim_c,
                            "extra_conditions": extra_c,
                            "logic_op": "AND",
                            "phase_var": p_info[0] if p_info else "",
                            "phase_op": p_info[1] if p_info else "==",
                            "phase_val": p_info[2] if p_info else 0,
                            "action_id": abil_id,
                            "target": target_str,
                            "chance": chance_v,
                            "var_op": "None",
                            "var_name": "",
                            "var_val": 0,
                            "flow": "Return",
                            "is_counter_exec": (argv == 0x705A),
                        })

    return extracted_rules


def decompile_atel_to_rules(chunk0_bytes, worker_idx=None, func_idx=None, chunk1_bytes=None, slot_idx=0, return_all_hooks=False):
    """
    Decompiles monster AI bytecode into high-level visual rule cards for the Visual AI Rule Builder.
    Automatically resolves the true AI Worker and Event Hook Slot via Chunk 1 when provided,
    and falls back to scanning active AI functions if worker_idx/func_idx are omitted.
    """
    # Allow calling decompile_atel_to_rules(chunk0_bytes, chunk1_bytes, return_all_hooks=True)
    if isinstance(worker_idx, (bytes, bytearray)):
        chunk1_bytes = worker_idx
        worker_idx = None

    disasm = AtelDisassembler(chunk0_bytes)
    if not disasm.workers:
        return {} if return_all_hooks else None

    if return_all_hooks:
        ai_map = parse_chunk1_ai_map(chunk1_bytes, chunk0_bytes)
        w_idx = ai_map["ai_worker_idx"]
        all_hooks_dict = {}
        seen_funcs = set()
        for h_entry in ai_map["hooks"]:
            hk = h_entry["key"]
            f_idx = h_entry["func_idx"]
            if f_idx is not None and f_idx != 0xFFFF and 0 <= w_idx < len(disasm.workers) and 0 <= f_idx < len(disasm.workers[w_idx]["funcs"]):
                # If multiple hooks point to the exact same shared 1-byte stub, don't duplicate
                rules = extract_rules_from_function_ast(disasm, w_idx, f_idx)
                for r in rules:
                    r["hook"] = hk
                    r["func_idx"] = f_idx
                    if r.get("var_name") and not r.get("var_idx"):
                        r["var_idx"] = r["var_name"]
                    if "is_counter_exec" in r and "is_counter_op" not in r:
                        r["is_counter_op"] = r["is_counter_exec"]
                all_hooks_dict[hk] = rules
                seen_funcs.add((w_idx, f_idx))
            else:
                all_hooks_dict[hk] = []

        # Fallback: if 'turn' had 0 rules (e.g. boss delegates to a helper function in the AI worker),
        # scan any helper functions in w_idx that weren't in seen_funcs
        if not all_hooks_dict.get("turn") and 0 <= w_idx < len(disasm.workers):
            for f_i in range(len(disasm.workers[w_idx]["funcs"])):
                if (w_idx, f_i) not in seen_funcs:
                    helper_rules = extract_rules_from_function_ast(disasm, w_idx, f_i)
                    if helper_rules:
                        for r in helper_rules:
                            r["hook"] = "turn"
                            r["func_idx"] = f_i
                            if r.get("var_name") and not r.get("var_idx"):
                                r["var_idx"] = r["var_name"]
                            if "is_counter_exec" in r and "is_counter_op" not in r:
                                r["is_counter_op"] = r["is_counter_exec"]
                        all_hooks_dict["turn"].extend(helper_rules)
        return all_hooks_dict

    # Resolve target worker_idx and func_idx via Chunk 1 if available
    if chunk1_bytes is not None or worker_idx is None or func_idx is None:
        ai_map = parse_chunk1_ai_map(chunk1_bytes, chunk0_bytes)
        if worker_idx is None:
            worker_idx = ai_map["ai_worker_idx"]
        if func_idx is None:
            mapped = ai_map["slots"][slot_idx] if 0 <= slot_idx < len(ai_map["slots"]) else 0xFFFF
            func_idx = mapped if mapped != 0xFFFF else None

    # If a specific (worker_idx, func_idx) was requested, extract directly from that function
    if worker_idx is not None and func_idx is not None:
        if 0 <= worker_idx < len(disasm.workers) and 0 <= func_idx < len(disasm.workers[worker_idx]["funcs"]):
            rules = extract_rules_from_function_ast(disasm, worker_idx, func_idx)
            if rules:
                return rules
            # If the user explicitly asked for a specific hook slot (via chunk1_bytes), return [] if that hook is empty
            if chunk1_bytes is not None:
                return []

    # Fallback: scan candidate AI functions across workers
    candidates = []
    if worker_idx is not None and 0 <= worker_idx < len(disasm.workers):
        for f_i in range(len(disasm.workers[worker_idx]["funcs"])):
            candidates.append((worker_idx, f_i))
    for w in disasm.workers:
        w_i = w["index"]
        for f_i in range(len(w["funcs"])):
            if (w_i, f_i) not in candidates:
                candidates.append((w_i, f_i))

    for w_i, f_i in candidates:
        rules = extract_rules_from_function_ast(disasm, w_i, f_i)
        if rules:
            return rules

    return None


