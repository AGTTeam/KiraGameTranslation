import codecs
import game
from hacktools import common


def run():
    infolder = "data/extract/data/data/scenario/"
    outfile = "data/scenario_output.txt"

    common.logMessage("Extracting SCE to", outfile, "...")
    with codecs.open(outfile, "w", "utf-8") as out:
        files = common.getFiles(infolder, ".bin")
        for file in common.showProgress(files):
            common.logDebug("Processing", file, "...")
            parts = game.readScenario(infolder + file)
            out.write("!FILE:" + file + "\n")
            for part in parts:
                for string in part.strings:
                    sjis = string.sjis
                    if sjis.endswith("<1F>"):
                        sjis = sjis[:-4]
                    out.write(sjis + "=\n")
    common.logMessage("Done! Extracted", len(files), "files")
