import struct

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
    0x700F: "GetProperty(target, property)",
    0x7010: "BuildAction(actor, ability, target, target_type)",
    0x700B: "ExecuteAction(action_id, flag)",
    0x7001: "checkTargetStatus(target, status_id)",
    0x7002: "checkTargetElement(target, element_id)",
    0x7005: "targetDistToParty(target)",
    0x7015: "clearActionQueue()",
    0x7020: "setNextTurnActor(actor)",
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
        indent = 2
        
        while cursor < len(self.disasm.bytecode):
            w_idx = get_worker_for_offset(cursor)
            worker = self.disasm.workers[w_idx] if w_idx < len(self.disasm.workers) else None
            
            # Print labels / function headers
            if cursor in labels:
                for w_num, lbl_type, lbl_idx in labels[cursor]:
                    if lbl_type == "Func":
                        indent = 2
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
                stack.append("rX")
            elif opcode == 0x29:  # PUSHY
                stack.append("rY")
            
            # Stack pop operations / assignments
            elif opcode == 0x25:  # POPA
                val = stack.pop() if stack else "?"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}rA = {val}")
                else:
                    output.append(f"{' ' * indent}Set return register rA to {val}")
            elif opcode == 0x2A:  # POPX
                val = stack.pop() if stack else "?"
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
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}rX_check: goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}Check rX and jump to Label {argv:02d}")
            elif opcode == 0xD6:  # POPXCJMP
                cond = "rX"
                if mode == "pseudocode":
                    output.append(f"{' ' * indent}if {cond}: goto label_{argv:02d}")
                else:
                    output.append(f"{' ' * indent}If {cond} is true: Jump to Label {argv:02d}")
            elif opcode == 0xD7:  # POPXNCJMP
                cond = "rX"
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
            elif opcode in [0xB5, 0xD8]:  # CALL, CALLPOPA
                call_name = CALL_TARGET_MAP.get(argv, f"call_{argv:04X}")
                
                # Map of call ID to (num_args, returns_val)
                BATTLE_CALL_SIGNATURES = {
                    0x700F: (2, True),   # GetProperty(target, property)
                    0x7010: (4, True),   # BuildAction(actor, ability, target, target_type)
                    0x700B: (2, False),  # ExecuteAction(action_id, flag)
                    0x00A9: (0, True),   # GetRandomValue()
                    0x005F: (0, False),  # halt()
                }
                
                sig = BATTLE_CALL_SIGNATURES.get(argv)
                if sig:
                    num_args, returns_val = sig
                else:
                    num_args = len(stack)
                    returns_val = (opcode == 0xD8 or "get" in call_name.lower())
                    
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
                        output.append(f"{' ' * indent}Set rA to result of {stmt}")
                elif returns_val:
                    stack.append(stmt)
                else:
                    if mode == "pseudocode":
                        output.append(f"{' ' * indent}{stmt}")
                    else:
                        if "wait" in call_name and args:
                            output.append(f"{' ' * indent}Wait for {args[0]} frames")
                        elif "halt" in call_name:
                            output.append(f"{' ' * indent}Halt script execution")
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


def compile_rules_to_atel(rules, script_id="001"):
    import struct
    # 1. Compile bytecode
    func0_bytes = b"\x3C" # RET
    func1_bytes = b"\xD8\x5F\x00\x3C" # CALLPOPA halt(), RET
    
    # Build Function 2 bytecode
    bytecode2 = bytearray()
    jumps = []
    
    for rule in rules:
        cond_type = rule.get("condition", "Always")
        chance = int(rule.get("chance", 100))
        
        chance_failed_jump_idx = None
        if chance < 100:
            bytecode2.extend(b"\xB5\xA9\x00")  # CALL GetRandomValue()
            bytecode2.extend(b"\xAE\x64\x00")  # PUSHII 100
            bytecode2.extend(b"\x18")          # OPMOD
            bytecode2.extend(struct.pack("<B H", 0xAE, chance)) # PUSHII chance
            bytecode2.extend(b"\x0B")          # OPLS
            bytecode2.extend(b"\x2A")          # POPX
            
            chance_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode2.extend(struct.pack("<B H", 0xD7, chance_failed_jump_idx))
            
        cond_failed_jump_idx = None
        if cond_type == "HP < 50%":
            bytecode2.extend(b"\xAE\xF2\xFF")  # PUSHII -14 (Self)
            bytecode2.extend(b"\xAE\x15\x00")  # PUSHII 21 (HP%)
            bytecode2.extend(b"\xB5\x0F\x70")  # CALL call_700F
            bytecode2.extend(b"\xAE\x32\x00")  # PUSHII 50
            bytecode2.extend(b"\x0B")          # OPLS
            bytecode2.extend(b"\x2A")          # POPX
            
            cond_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode2.extend(struct.pack("<B H", 0xD7, cond_failed_jump_idx))
            
        elif cond_type == "MP < 50%":
            bytecode2.extend(b"\xAE\xF2\xFF")  # PUSHII -14 (Self)
            bytecode2.extend(b"\xAE\x16\x00")  # PUSHII 22 (MP%)
            bytecode2.extend(b"\xB5\x0F\x70")  # CALL call_700F
            bytecode2.extend(b"\xAE\x32\x00")  # PUSHII 50
            bytecode2.extend(b"\x0B")          # OPLS
            bytecode2.extend(b"\x2A")          # POPX
            
            cond_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode2.extend(struct.pack("<B H", 0xD7, cond_failed_jump_idx))
            
        # Execute Action
        action_id = int(rule.get("action_id", 4))
        target_str = rule.get("target", "Target")
        target_val = -16 if target_str == "Target" else -14
        
        bytecode2.extend(b"\xAE\xF2\xFF")  # PUSHII -14
        bytecode2.extend(struct.pack("<B H", 0xAE, action_id)) # PUSHII action_id
        bytecode2.extend(struct.pack("<B h", 0xAE, target_val)) # PUSHII target
        bytecode2.extend(b"\xAE\x00\x00")  # PUSHII 0
        bytecode2.extend(b"\xB5\x10\x70")  # CALL call_7010
        
        bytecode2.extend(b"\xA0\x02\x00")  # POPV var_02
        bytecode2.extend(b"\x9F\x02\x00")  # PUSHV var_02
        bytecode2.extend(b"\xAE\x00\x40")  # PUSHII 16384 (0x4000)
        bytecode2.extend(b"\xD8\x0B\x70")  # CALLPOPA call_700B
        bytecode2.extend(b"\x3C")          # RET
        
        # Resolve target offset for condition jump (relative to func2 start, plus func0 + func1 size which is 5)
        next_rule_offset = len(bytecode2) + 5
        if chance_failed_jump_idx is not None:
            jumps[chance_failed_jump_idx] = next_rule_offset
        if cond_failed_jump_idx is not None:
            jumps[cond_failed_jump_idx] = next_rule_offset
            
    bytecode2.extend(b"\x3C") # RET
    
    # Full bytecode segment
    full_bytecode = func0_bytes + func1_bytes + bytes(bytecode2)
    bytecode_len = len(full_bytecode)
    
    # 2. Determine offsets and align
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
    
    # 3. Build binary data
    data = bytearray(bytecode_start + bytecode_len)
    
    # File Header
    struct.pack_into("<I", data, 0x00, bytecode_len)
    struct.pack_into("<I", data, 0x08, creator_tag_addr)
    struct.pack_into("<I", data, 0x0C, script_id_addr)
    struct.pack_into("<I", data, 0x30, bytecode_start)
    struct.pack_into("<H", data, 0x34, 1) # namespace count
    
    # Worker offsets table
    worker_0_offset = header_size + worker_offsets_size
    struct.pack_into("<I", data, 0x38, worker_0_offset)
    
    # Worker 0 Header
    struct.pack_into("<H", data, worker_0_offset + 0x00, 1) # type
    struct.pack_into("<H", data, worker_0_offset + 0x02, 5) # var count
    struct.pack_into("<H", data, worker_0_offset + 0x04, 0) # ref int count
    struct.pack_into("<H", data, worker_0_offset + 0x06, 0) # ref float count
    struct.pack_into("<H", data, worker_0_offset + 0x08, 3) # func count
    struct.pack_into("<H", data, worker_0_offset + 0x0A, len(jumps)) # jump count
    struct.pack_into("<I", data, worker_0_offset + 0x14, funcs_offset) # vars_offset placeholder
    struct.pack_into("<I", data, worker_0_offset + 0x20, funcs_offset)
    struct.pack_into("<I", data, worker_0_offset + 0x24, jumps_offset)
    
    # Function Table
    struct.pack_into("<I", data, funcs_offset + 0, 0) # func 0 offset
    struct.pack_into("<I", data, funcs_offset + 4, 1) # func 1 offset
    struct.pack_into("<I", data, funcs_offset + 8, 5) # func 2 offset
    
    # Jump Table
    for i, jump_addr in enumerate(jumps):
        struct.pack_into("<I", data, jumps_offset + i * 4, jump_addr)
        
    # Strings
    data[creator_tag_addr : creator_tag_addr + len(creator_tag_str)] = creator_tag_str
    data[script_id_addr : script_id_addr + len(script_id_str)] = script_id_str
    
    # Bytecode
    data[bytecode_start : bytecode_start + bytecode_len] = full_bytecode
    
    return bytes(data)


def compile_rules_to_bytecode(rules, jump_index_offset=0, function_start_offset=0):
    import struct
    bytecode = bytearray()
    jumps = []
    
    for rule in rules:
        cond_type = rule.get("condition", "Always")
        chance = int(rule.get("chance", 100))
        
        chance_failed_jump_idx = None
        if chance < 100:
            bytecode.extend(b"\xB5\xA9\x00")  # CALL GetRandomValue()
            bytecode.extend(b"\xAE\x64\x00")  # PUSHII 100
            bytecode.extend(b"\x18")          # OPMOD
            bytecode.extend(struct.pack("<B H", 0xAE, chance)) # PUSHII chance
            bytecode.extend(b"\x0B")          # OPLS
            bytecode.extend(b"\x2A")          # POPX
            
            chance_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode.extend(struct.pack("<B H", 0xD7, jump_index_offset + chance_failed_jump_idx))
            
        cond_failed_jump_idx = None
        if cond_type == "HP < 50%":
            bytecode.extend(b"\xAE\xF2\xFF")  # PUSHII -14 (Self)
            bytecode.extend(b"\xAE\x15\x00")  # PUSHII 21 (HP%)
            bytecode.extend(b"\xB5\x0F\x70")  # CALL call_700F
            bytecode.extend(b"\xAE\x32\x00")  # PUSHII 50
            bytecode.extend(b"\x0B")          # OPLS
            bytecode.extend(b"\x2A")          # POPX
            
            cond_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode.extend(struct.pack("<B H", 0xD7, jump_index_offset + cond_failed_jump_idx))
            
        elif cond_type == "MP < 50%":
            bytecode.extend(b"\xAE\xF2\xFF")  # PUSHII -14 (Self)
            bytecode.extend(b"\xAE\x16\x00")  # PUSHII 22 (MP%)
            bytecode.extend(b"\xB5\x0F\x70")  # CALL call_700F
            bytecode.extend(b"\xAE\x32\x00")  # PUSHII 50
            bytecode.extend(b"\x0B")          # OPLS
            bytecode.extend(b"\x2A")          # POPX
            
            cond_failed_jump_idx = len(jumps)
            jumps.append(0)
            bytecode.extend(struct.pack("<B H", 0xD7, jump_index_offset + cond_failed_jump_idx))
            
        # Execute Action
        action_id = int(rule.get("action_id", 4))
        target_str = rule.get("target", "Target")
        target_val = -16 if target_str == "Target" else -14
        
        bytecode.extend(b"\xAE\xF2\xFF")  # PUSHII -14
        bytecode.extend(struct.pack("<B H", 0xAE, action_id)) # PUSHII action_id
        bytecode.extend(struct.pack("<B h", 0xAE, target_val)) # PUSHII target
        bytecode.extend(b"\xAE\x00\x00")  # PUSHII 0
        bytecode.extend(b"\xB5\x10\x70")  # CALL call_7010
        
        bytecode.extend(b"\xA0\x02\x00")  # POPV var_02
        bytecode.extend(b"\x9F\x02\x00")  # PUSHV var_02
        bytecode.extend(b"\xAE\x00\x40")  # PUSHII 16384 (0x4000)
        bytecode.extend(b"\xD8\x0B\x70")  # CALLPOPA call_700B
        bytecode.extend(b"\x3C")          # RET
        
        # Resolve next rule target offset
        next_rule_offset = function_start_offset + len(bytecode)
        if chance_failed_jump_idx is not None:
            jumps[chance_failed_jump_idx] = next_rule_offset
        if cond_failed_jump_idx is not None:
            jumps[cond_failed_jump_idx] = next_rule_offset
            
    bytecode.extend(b"\x3C") # RET
    return bytes(bytecode), jumps


def adjust_file_pointers(data, threshold, shift):
    def adj_32(offset):
        val = struct.unpack("<I", data[offset:offset+4])[0]
        if val >= threshold:
            struct.pack_into("<I", data, offset, val + shift)
            
    adj_32(0x08) # creator_tag_addr
    adj_32(0x0C) # script_id_addr
    adj_32(0x30) # bytecode_start
    
    namespace_count = struct.unpack("<H", data[0x34:0x36])[0]
    for i in range(namespace_count):
        w_off_addr = 0x38 + i * 4
        adj_32(w_off_addr)
        
        w_off = struct.unpack("<I", data[w_off_addr:w_off_addr+4])[0]
        adj_32(w_off + 0x14) # vars_offset
        adj_32(w_off + 0x18) # ref_ints_offset
        adj_32(w_off + 0x1C) # ref_floats_offset
        adj_32(w_off + 0x20) # funcs_offset
        adj_32(w_off + 0x24) # jumps_offset
        adj_32(w_off + 0x2C) # private_data_offset
        adj_32(w_off + 0x30) # shared_data_offset


def inject_rules(original_bytes, rules, worker_idx=1, func_idx=2):
    disasm = AtelDisassembler(original_bytes)
    if worker_idx >= len(disasm.workers):
        raise ValueError(f"Worker index {worker_idx} out of range (max {len(disasm.workers)-1})")
    worker = disasm.workers[worker_idx]
    if func_idx >= len(worker["funcs"]):
        raise ValueError(f"Function index {func_idx} out of range (max {len(worker['funcs'])-1})")
        
    S = worker["funcs"][func_idx]
    
    entry_points = sorted(list(set(addr for w in disasm.workers for addr in w["funcs"])))
    idx = entry_points.index(S)
    E = entry_points[idx+1] if idx + 1 < len(entry_points) else len(disasm.bytecode)
    
    num_existing_jumps = len(worker["jumps"])
    
    new_func_bytecode, new_jumps = compile_rules_to_bytecode(
        rules, 
        jump_index_offset=num_existing_jumps, 
        function_start_offset=S
    )
    
    data = bytearray(original_bytes)
    
    # Operation 1: Insert new jumps
    jumps_offset = worker["jumps_offset"]
    jumps_end = jumps_offset + num_existing_jumps * 4
    jump_shift = len(new_jumps) * 4
    
    data[jumps_end:jumps_end] = bytes(jump_shift)
    for i, jump_val in enumerate(new_jumps):
        struct.pack_into("<I", data, jumps_end + i * 4, jump_val)
        
    worker_offset = struct.unpack("<I", data[0x38 + worker_idx * 4 : 0x38 + worker_idx * 4 + 4])[0]
    struct.pack_into("<H", data, worker_offset + 0x0A, num_existing_jumps + len(new_jumps))
    
    # Adjust pointers after jump table insertion
    adjust_file_pointers(data, threshold=jumps_end, shift=jump_shift)
    
    # Re-read disasm to get updated bytecode_start address
    bytecode_start_updated = struct.unpack("<I", data[0x30:0x34])[0]
    func_file_start = bytecode_start_updated + S
    func_file_end = bytecode_start_updated + E
    
    delta = len(new_func_bytecode) - (E - S)
    
    # Operation 2: Replace function bytecode
    data[func_file_start:func_file_end] = new_func_bytecode
    
    bytecode_len = struct.unpack("<I", data[0x00:0x04])[0]
    struct.pack_into("<I", data, 0x00, bytecode_len + delta)
    
    # Adjust pointers after bytecode change
    adjust_file_pointers(data, threshold=func_file_end, shift=delta)
    
    # Update function and jump tables
    namespace_count = struct.unpack("<H", data[0x34:0x36])[0]
    for i in range(namespace_count):
        w_off = struct.unpack("<I", data[0x38 + i * 4 : 0x38 + i * 4 + 4])[0]
        f_count = struct.unpack("<H", data[w_off + 0x08:w_off + 0x0A])[0]
        f_offset = struct.unpack("<I", data[w_off + 0x20:w_off + 0x24])[0]
        
        for k in range(f_count):
            addr_offset = f_offset + k * 4
            val = struct.unpack("<I", data[addr_offset:addr_offset+4])[0]
            if val > S:
                struct.pack_into("<I", data, addr_offset, val + delta)
                
        j_count = struct.unpack("<H", data[w_off + 0x0A:w_off + 0x0C])[0]
        j_offset = struct.unpack("<I", data[w_off + 0x24:w_off + 0x28])[0]
        
        orig_j_count = j_count - len(new_jumps) if i == worker_idx else j_count
        for k in range(j_count):
            addr_offset = j_offset + k * 4
            val = struct.unpack("<I", data[addr_offset:addr_offset+4])[0]
            if k < orig_j_count and val > S:
                struct.pack_into("<I", data, addr_offset, val + delta)
                
    return bytes(data)


def decompile_atel_to_rules(chunk0_bytes, worker_idx=1, func_idx=2):
    disasm = AtelDisassembler(chunk0_bytes)
    if worker_idx >= len(disasm.workers):
        return None
    worker = disasm.workers[worker_idx]
    if func_idx >= len(worker["funcs"]):
        return None
    S = worker["funcs"][func_idx]
    
    entry_points = sorted(list(set(addr for w in disasm.workers for addr in w["funcs"])))
    idx = entry_points.index(S)
    E = entry_points[idx+1] if idx + 1 < len(entry_points) else len(disasm.bytecode)
    
    func_bytecode = disasm.bytecode[S:E]
    
    # Parse instructions
    instructions = []
    cursor = 0
    while cursor < len(func_bytecode):
        offset = cursor
        opcode = func_bytecode[cursor]
        cursor += 1
        
        has_args = (opcode >= 0x80)
        if has_args:
            if cursor + 2 > len(func_bytecode):
                break
            arg1 = func_bytecode[cursor]
            arg2 = func_bytecode[cursor+1]
            cursor += 2
            argv = arg1 + arg2 * 0x100
            argv_signed = argv if argv < 0x8000 else (argv - 0x10000)
        else:
            argv_signed = 0
            
        instructions.append((opcode, argv_signed, offset))
        
    rules = []
    i = 0
    n = len(instructions)
    
    while i < n:
        if instructions[i][0] == 0x3C: # RET
            i += 1
            continue
            
        chance = 100
        condition = "Always"
        
        # 1. Chance check pattern (7 instructions)
        if (i + 6 < n and
            instructions[i][0] == 0xB5 and instructions[i][1] == 0x00A9 and
            instructions[i+1][0] == 0xAE and instructions[i+1][1] == 100 and
            instructions[i+2][0] == 0x18 and
            instructions[i+3][0] == 0xAE and
            instructions[i+4][0] == 0x0B and
            instructions[i+5][0] == 0x2A and
            instructions[i+6][0] == 0xD7):
            
            chance = instructions[i+3][1]
            i += 7
            
        # 2. Condition check pattern (7 instructions)
        if (i + 6 < n and
            instructions[i][0] == 0xAE and instructions[i][1] == -14 and
            instructions[i+1][0] == 0xAE and
            instructions[i+2][0] == 0xB5 and instructions[i+2][1] == 0x700F and
            instructions[i+3][0] == 0xAE and instructions[i+3][1] == 50 and
            instructions[i+4][0] == 0x0B and
            instructions[i+5][0] == 0x2A and
            instructions[i+6][0] == 0xD7):
            
            param = instructions[i+1][1]
            if param == 21:
                condition = "HP < 50%"
            elif param == 22:
                condition = "MP < 50%"
            else:
                condition = f"Param_{param} < 50%"
            i += 7
            
        # 3. Action execution pattern (10 instructions)
        if (i + 9 < n and
            instructions[i][0] == 0xAE and instructions[i][1] == -14 and
            instructions[i+1][0] == 0xAE and
            instructions[i+2][0] == 0xAE and
            instructions[i+3][0] == 0xAE and instructions[i+3][1] == 0 and
            instructions[i+4][0] == 0xB5 and instructions[i+4][1] == 0x7010 and
            instructions[i+5][0] == 0xA0 and instructions[i+5][1] == 2 and
            instructions[i+6][0] == 0x9F and instructions[i+6][1] == 2 and
            instructions[i+7][0] == 0xAE and instructions[i+7][1] == 16384 and
            instructions[i+8][0] == 0xD8 and instructions[i+8][1] == 0x700B and
            instructions[i+9][0] == 0x3C):
            
            action_id = instructions[i+1][1]
            target_val = instructions[i+2][1]
            target = "Target" if target_val == -16 else "Self"
            
            rules.append({
                "condition": condition,
                "action_id": action_id,
                "target": target,
                "chance": chance
            })
            i += 10
        else:
            return None
            
    return rules

