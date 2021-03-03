import codecs
import os
import game
from hacktools import common, nitro


def run():
    infolder = "data/extract/data/data/scenario/"
    outfolder = "data/repack/data/data/scenario/"
    infile = "data/scenario_input.txt"
    fontfile = "data/replace/data/data/font/font.nftr"
    chartot = transtot = 0

    if not os.path.isfile(infile):
        common.logError("Input file", infile, "not found")
        return

    common.copyFolder(infolder, outfolder)
    common.logMessage("Repacking SCE from", infile, "...")
    # Read the glyph size from the font
    if not os.path.isfile(fontfile):
        fontfile = fontfile.replace("replace/", "extract/")
    glyphs = nitro.readNFTR(fontfile).glyphs
    with codecs.open(infile, "r", "utf-8") as script:
        files = common.getFiles(infolder, ".bin")
        for file in common.showProgress(files):
            section = common.getSection(script, file)
            if len(section) == 0:
                continue
            chartot, transtot = common.getSectionPercentage(section, chartot, transtot)
            # Repack the file
            common.logDebug("Processing", file, "...")
            parts = game.readScenario(infolder + file)
            with common.Stream(outfolder + file, "wb") as f:
                # Write the parts and string data
                f.writeUInt(len(parts))
                for part in parts:
                    f.writeUInt(part.num)
                    f.writeUInt(part.unk1)
                    f.writeUInt(part.unk2)
                for part in parts:
                    for string in part.strings:
                        f.writeInt(string.unk1)
                        f.writeUInt(string.index)
                        f.writeUInt(0xffffffff)
                        string.pointeroff = f.tell()
                        f.writeUInt(0)
                addedstrings = {}
                for part in parts:
                    # Order the strings by offset and write the new strings
                    for string in part.strings:
                        sjis = string.sjis
                        add1f = False
                        if sjis.endswith("<1F>"):
                            sjis = sjis[:-4]
                            add1f = True
                        newsjis = ""
                        if sjis in section:
                            newsjis = section[sjis].pop(0)
                            if len(section[sjis]) == 0:
                                del section[sjis]
                        if newsjis != "":
                            if newsjis == "!":
                                newsjis = ""
                            if newsjis.startswith("<<"):
                                newsjis = common.wordwrap(newsjis[2:], glyphs, game.wordwrap2, game.detectTextCode)
                                newsjis = common.centerLines("<<" + newsjis.replace("|", "|<<"), glyphs, game.wordwrap2, game.detectTextCode)
                            else:
                                newsjis = common.wordwrap(newsjis, glyphs, game.wordwrap, game.detectTextCode)
                        else:
                            newsjis = sjis
                        if add1f:
                            newsjis += "<1F>"
                        if newsjis in addedstrings:
                            string.sjisoff = addedstrings[newsjis]
                        else:
                            string.sjisoff = f.tell()
                            game.writeShiftJIS(f, newsjis)
                            addedstrings[newsjis] = string.sjisoff
                    # Align bytes
                    f.writeZero(f.tell() % 16)
                    # Write the new pointers
                    for string in part.strings:
                        ptroff = f.tell()
                        f.writeUInt(string.sjisoff)
                        f.seek(string.pointeroff)
                        f.writeUInt(ptroff)
                        f.seek(ptroff + 4)
    common.logMessage("Done! Translation is at {0:.2f}%".format((100 * transtot) / chartot))
