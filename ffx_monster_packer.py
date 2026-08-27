import os
import struct
import tempfile
import shutil

def unpack_chunks(data: bytes) -> list:
    if len(data) < 0x30:
        return []
    indicator = struct.unpack("<I", data[0:4])[0]
    chunk_count = indicator - 1
    offsets = []
    for i in range(chunk_count + 1):
        offset = struct.unpack("<I", data[i*4+4 : i*4+8])[0]
        offsets.append(offset)
        
    chunks = []
    for i in range(chunk_count):
        offset = offsets[i]
        if offset == 0:
            chunks.append(b"")
        else:
            to = -1
            for j in range(i + 1, chunk_count + 1):
                if offsets[j] >= offset:
                    to = offsets[j]
                    break
            if to == -1:
                to = len(data)
            chunks.append(data[offset:to])
    return chunks

def repack_chunks(chunks: list) -> bytes:
    header = bytearray(0x30)
    struct.pack_into("<I", header, 0, 8)
    
    end_offset = 0x30
    paddings = []
    
    for i in range(7):
        chunk = chunks[i]
        addr_target = 0x04 + 0x04 * i
        if not chunk or len(chunk) == 0:
            struct.pack_into("<I", header, addr_target, 0)
            paddings.append(0)
        else:
            struct.pack_into("<I", header, addr_target, end_offset)
            end_offset += len(chunk)
            padding = 0
            paddings.append(padding)
            
    struct.pack_into("<I", header, 0x20, end_offset)
    
    out = bytearray(header)
    for i in range(7):
        chunk = chunks[i]
        if chunk:
            out.extend(chunk)
        if paddings[i] > 0:
            out.extend(b"\x00" * paddings[i])
            
    return bytes(out)

def safe_atomic_write(filepath: str, data: bytes):
    dir_name = os.path.dirname(os.path.abspath(filepath))
    fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as tmp_file:
            tmp_file.write(data)
        shutil.move(temp_path, filepath)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

def parse_stat_block_names(stat_bytes: bytes, codec, charset: str):
    if len(stat_bytes) < 128:
        return "", "", ""
    def read_str(chunk_bytes, offset_idx):
        off = struct.unpack("<H", chunk_bytes[offset_idx : offset_idx+2])[0]
        return codec.decode_ffx_bytes(chunk_bytes[128:], off, charset)
    
    name = read_str(stat_bytes, 0x00)
    sensor = read_str(stat_bytes, 0x04)
    scan = read_str(stat_bytes, 0x0C)
    return name, sensor, scan

def serialize_stat_block(original_bytes: bytes, stats_dict: dict, name: str, sensor: str, scan: str, codec, charset: str) -> bytes:
    block = bytearray(original_bytes[:128])
    
    struct.pack_into("<I", block, 0x14, int(stats_dict["hp"]))
    struct.pack_into("<I", block, 0x18, int(stats_dict["mp"]))
    struct.pack_into("<I", block, 0x1C, int(stats_dict["overkill"]))
    
    block[0x20] = int(stats_dict["str"])
    block[0x21] = int(stats_dict["def"])
    block[0x22] = int(stats_dict["mag"])
    block[0x23] = int(stats_dict["mdf"])
    block[0x24] = int(stats_dict["agi"])
    block[0x25] = int(stats_dict["lck"])
    block[0x26] = int(stats_dict["eva"])
    block[0x27] = int(stats_dict["acc"])
    
    block[0x28] = (block[0x28] & 0xFE) | (1 if stats_dict["armored"] else 0)
    block[0x77] = int(stats_dict["doom"])
    struct.pack_into("<H", block, 0x78, int(stats_dict["arena_idx"]))
    struct.pack_into("<H", block, 0x7A, int(stats_dict["sound_ref"]))
    
    # Elements
    block[0x2B] = stats_dict["elem_absorb"]
    block[0x2C] = stats_dict["elem_immune"]
    block[0x2D] = stats_dict["elem_resist"]
    block[0x2E] = stats_dict["elem_weak"]
    
    # Status Resists
    block[0x2F] = int(stats_dict["res_death"])
    block[0x30] = int(stats_dict["res_zombie"])
    block[0x31] = int(stats_dict["res_petrify"])
    block[0x32] = int(stats_dict["res_poison"])
    block[0x33] = int(stats_dict["res_powerbreak"])
    block[0x34] = int(stats_dict["res_magicbreak"])
    block[0x35] = int(stats_dict["res_armorbreak"])
    block[0x36] = int(stats_dict["res_mentalbreak"])
    block[0x37] = int(stats_dict["res_confuse"])
    block[0x38] = int(stats_dict["res_berserk"])
    block[0x39] = int(stats_dict["res_provoke"])
    block[0x3A] = int(stats_dict["res_threaten"])
    block[0x3B] = int(stats_dict["res_sleep"])
    block[0x3C] = int(stats_dict["res_silence"])
    block[0x3D] = int(stats_dict["res_darkness"])
    block[0x47] = int(stats_dict["res_slow"])
    block[0x46] = int(stats_dict["res_haste"])
    
    # Auto-statuses
    struct.pack_into("<H", block, 0x48, stats_dict["perm_status"])
    struct.pack_into("<H", block, 0x4A, stats_dict["temp_status"])
    struct.pack_into("<H", block, 0x4C, stats_dict["extra_status"])
    
    # Rebuild strings
    string_buf = bytearray()
    unique = {}
    offsets = []
    keys = []
    
    for s in [name, sensor, sensor, scan, scan]:
        if s in unique:
            off, key = unique[s]
        else:
            off = len(string_buf)
            key = len(unique)
            unique[s] = (off, key)
            encoded = codec.encode_ffx_string(s, charset) + [0x00]
            string_buf.extend(encoded)
        offsets.append(off)
        keys.append(key)
        
    struct.pack_into("<HH", block, 0x00, offsets[0], keys[0])
    struct.pack_into("<HH", block, 0x04, offsets[1], keys[1])
    struct.pack_into("<HH", block, 0x08, offsets[2], keys[2])
    struct.pack_into("<HH", block, 0x0C, offsets[3], keys[3])
    struct.pack_into("<HH", block, 0x10, offsets[4], keys[4])
    
    return bytes(block) + bytes(string_buf)
