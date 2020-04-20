import os
import game
from hacktools import common


def run():
    infolder = "data/extract/data/data/window/"
    outfolder = "data/repack/data/data/window/"
    repackfolder = "data/repack_XAP/"

    common.logMessage("Repacking XAP from", repackfolder, "...")
    files = common.getFiles(infolder, ".xap")
    for file in common.showProgress(files):
        common.logDebug("Processing", file, "...")
        with common.Stream(infolder + file, "rb") as f:
            with common.Stream(outfolder + file, "wb") as fout:
                fout.write(f.read(4))
                numfiles = f.readUShort()
                fout.writeUShort(numfiles)
                fout.write(f.read(6))
                currentoff = f.readUInt()
                fout.writeUInt(currentoff)
                for i in range(numfiles):
                    f.seek(16 + 16 * i)
                    fout.seek(f.tell())
                    type = f.readString(4)
                    fout.writeString(type)
                    size = f.readUInt()
                    f.seek(4, 1)
                    offset = f.readUInt()
                    xapfile = game.convertXAPName(file, type)
                    if os.path.isfile(repackfolder + xapfile):
                        # Read the new file
                        size = os.path.getsize(repackfolder + xapfile)
                        fout.writeUInt(size)
                        fout.writeUInt(size)
                        fout.writeUInt(currentoff)
                        fout.seek(currentoff)
                        with common.Stream(repackfolder + xapfile, "rb") as fxap:
                            fout.write(fxap.read())
                        currentoff += size
                    else:
                        # Copy the file
                        fout.writeUInt(size)
                        fout.writeUInt(size)
                        fout.writeUInt(currentoff)
                        fout.seek(currentoff)
                        f.seek(offset)
                        fout.write(f.read(size))
                        currentoff += size
    common.logMessage("Done! Extracted", len(files), "files")
