import os
import game
from hacktools import common


def run():
    infolder = "data/extract/data/data/window/"
    outfolder = "data/extract_XAP/"
    common.makeFolder(outfolder)

    common.logMessage("Extracting XAP to", outfolder, "...")
    files = common.getFiles(infolder, ".xap")
    for file in common.showProgress(files):
        common.logDebug("Processing", file, "...")
        with common.Stream(infolder + file, "rb") as f:
            f.seek(4)
            numfiles = f.readUShort()
            for i in range(numfiles):
                f.seek(16 + 16 * i)
                type = f.readString(4)
                size1 = f.readUInt()
                size2 = f.readUInt()
                if size1 != size2:
                    common.logError("Compressed file? Skipping")
                    continue
                offset = f.readUInt()
                xapfile = game.convertXAPName(file, type)
                common.makeFolders(outfolder + os.path.dirname(file))
                f.seek(offset)
                with common.Stream(outfolder + xapfile, "wb") as fout:
                    fout.write(f.read(size1))
    common.logMessage("Done! Extracted", len(files), "files")
