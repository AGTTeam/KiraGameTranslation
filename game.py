from hacktools import common


class ScenarioPart:
    num = 0
    unk1 = 0
    unk2 = 0
    strings = []


class ScenarioString:
    unk1 = 0
    index = 0
    pointer = 0
    offset = 0
    sjis = ""


def readScenario(file):
    parts = []
    with common.Stream(file, "rb") as f:
        partnum = f.readUInt()
        for i in range(partnum):
            section = ScenarioPart()
            section.num = f.readUInt()
            section.unk1 = f.readUInt()
            section.unk2 = f.readUInt()
            section.strings = []
            parts.append(section)
        for section in parts:
            for j in range(section.num):
                string = ScenarioString()
                string.unk1 = f.readUInt()
                string.index = f.readUInt()
                f.seek(4, 1)  # Always 0xffffffff
                string.pointer = f.readUInt()
                section.strings.append(string)
        for section in parts:
            for string in section.strings:
                f.seek(string.pointer)
                string.offset = f.readUInt()
                f.seek(string.offset)
                string.sjis = readShiftJIS(f)
    return parts


def readShiftJIS(f, encoding="shift_jis"):
    sjis = ""
    while True:
        b1 = f.readByte()
        if b1 == 0x02:
            sjis += f.read(2).decode(encoding).replace("〜", "～")
        elif b1 == 0x0A:
            sjis += "|"
        elif b1 == 0x00:
            break
        elif b1 >= 0x20 and b1 <= 0x7e:
            sjis += chr(b1)
        else:
            if b1 == 0x03:
                color = f.readByte()
                sjis += "<col" + chr(color) + ">"
            else:
                if b1 != 0x1F:
                    common.logWarning("Unknown control code", common.toHex(b1))
                sjis += "<" + common.toHex(b1) + ">"
    return sjis


def writeShiftJIS(f, s, encoding="shift_jis"):
    x = 0
    while x < len(s):
        c = s[x]
        if c == "|":
            f.writeByte(0x0A)
        elif c == "<" and s[x:x+4] == "<col":
            f.writeByte(0x03)
            f.writeByte(ord(s[x+4]))
            x += 5
        elif c == "<" and x < len(s) - 3 and s[x+3] == ">":
            code = s[x+1] + s[x+2]
            f.write(bytes.fromhex(code))
            x += 3
        elif ord(c) < 128:
            f.writeByte(ord(c))
        else:
            f.writeByte(0x02)
            f.write(c.encode(encoding))
        x += 1
    f.writeByte(0x00)
