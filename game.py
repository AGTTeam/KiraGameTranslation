from hacktools import common, nitro

binranges = [(0x8753c, 0xa3c87)]
freeranges = [(0x869d0, 0x86b53), (0x87b6c, 0x8811a), (0x882dc, 0x8867f)]
wordwrap = 180
wordwrap2 = 240
tempglyphs = {}
scripttweaks = {
    "story03.bin": [
        (0x3c18, 0x55),  # 0x64
    ],
    "story05.bin": [
        (0x4368, 0x0),  # 0x6e
    ],
    "story06.bin": [
        (0x4238, 0x30),  # 0x4a
        (0x7888, 0x55),  # 0x6e
    ]
}


class ScenarioPart:
    num = 0
    unk1 = 0
    unk2 = 0
    strings = []


class ScenarioString:
    unk1 = 0
    index = 0
    unk2 = 0
    pointer = 0
    offset = 0
    sjis = ""


def readScenario(file):
    parts = []
    with common.Stream(file, "rb") as f:
        partnum = f.readUInt()
        for i in range(partnum):
            partpos = f.tell()
            part = ScenarioPart()
            part.num = f.readUInt()
            part.unk1 = f.readUInt()
            part.unk2 = f.readUInt()
            part.strings = []
            common.logDebug("part", i, common.toHex(partpos), common.varsHex(part))
            parts.append(part)
        for i in range(partnum):
            part = parts[i]
            for j in range(part.num):
                strpos = f.tell()
                string = ScenarioString()
                string.unk1 = f.readInt()
                string.index = f.readUInt()
                string.unk2 = f.readUInt()
                string.pointer = f.readUInt()
                string.part = i
                part.strings.append(string)
                common.logDebug("string", j, common.toHex(strpos), common.varsHex(string))
        for part in parts:
            for string in part.strings:
                f.seek(string.pointer)
                string.offset = f.readUInt()
                f.seek(string.offset)
                string.sjis = readShiftJIS(f)
                common.logDebug(common.toHex(string.offset), common.varsHex(string))
    return parts


def convertXAPName(file, type):
    # "GCN0" = ".NCGR", "ECN0" = ".NCER", etc
    type = "." + (type[:3])[::-1] + "R"
    file = file.replace("_a.", ".").replace("_g.", ".")
    return file.replace(".xap", type)


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
    s = s.replace("～", "〜")
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


def readBINString(f, encoding="shift_jis"):
    s = common.detectEncodedString(f, encoding, [0x20, 0x25, 0x4c], [(0x03, 0x34), (0x03, 0x35), (0x03, 0x36), (0x03, 0x37)])
    split = s.split("UNK(03", 1)
    while len(split) > 1:
        split2 = split[1].split(")", 1)
        s = split[0] + "<col" + split2[0] + ">" + split2[1]
        split = s.split("UNK(03", 1)
    return s


def writeBINString(f, s, maxlen=0, encoding="shift_jis"):
    split = s.split("<col", 1)
    while len(split) > 1:
        split2 = split[1].split(">", 1)
        s = split[0] + "UNK(03" + split2[0].zfill(2) + ")" + split2[1]
        split = s.split("<col", 1)
    if s.startswith("<<"):
        s = common.wordwrap(s[2:], tempglyphs, wordwrap2, detectTextCode)
        s = common.centerLines("<<" + s.replace("|", "|<<"), tempglyphs, wordwrap2, detectTextCode)
    return common.writeEncodedString(f, s, maxlen, encoding)


def detectTextCode(s, i=0):
    if s[i] == "<":
        return len(s[i:].split(">", 1)[0]) + 1
    return 0


ignorepalindex = [
    "kira_game/fukidasi.NCGR",
    "kira_game/l_kira.NCGR",
    "kira_game/touhyou.NCGR",
    "menu/playmemo.NCGR",
    "menu/single.NCGR",
    "menu/story_restart.NCGR",
    "menu/tuto_game.NCGR",
]


transpnsbmd = [
    "balloon/",
    "bg006a",
    "bg042a",
    "douchou",
    "giwaku2a",
    "hanron",
    "taikou1a",
    "taikou2a",
]


def readImage(infolder, file, extension):
    palettefile = file.replace(extension, ".NCLR")
    mapfile = file.replace(extension, ".NSCR")
    cellfile = file.replace(extension, ".NCER")
    ignorepal = file in ignorepalindex
    palettes, image, map, cell, width, height = nitro.readNitroGraphic(infolder + palettefile, infolder + file, infolder + mapfile, infolder + cellfile, ignorepal)
    return palettes, image, map, cell, width, height, mapfile, cellfile


def readNSBMD(file):
    for transpname in transpnsbmd:
        if transpname in file:
            return True
    return False


def writeNSBMD(file, nsbmd):
    for transpname in transpnsbmd:
        if transpname in file:
            return True, True, True
    return False, False, False
