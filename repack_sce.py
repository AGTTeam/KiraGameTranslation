import codecs
import os
import game
from hacktools import common


def run():
    infolder = "data/extract/data/data/scenario/"
    outfolder = "data/repack/data/data/scenario/"
    infile = "data/scenario_input.txt"
    chartot = transtot = 0

    if not os.path.isfile(infile):
        common.logError("Input file", infile, "not found")
        return

    common.copyFolder(infolder, outfolder)
    common.logMessage("Repacking SCE from", infile, "...")
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
            with common.Stream(outfolder + file, "r+b") as f:
                for part in parts:
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
                            if add1f:
                                newsjis += "<1F>"
                            f.seek(string.offset)
                            game.writeShiftJIS(f, newsjis)
    common.logMessage("Done! Translation is at {0:.2f}%".format((100 * transtot) / chartot))
