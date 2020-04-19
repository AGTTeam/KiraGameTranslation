import os
import click
from hacktools import common, nds, nitro

version = "0.5.0"
romfile = "data/dn1.nds"
rompatch = "data/dn1_patched.nds"
infolder = "data/extract/"
replacefolder = "data/replace/"
outfolder = "data/repack/"
bannerfile = "data/repack/banner.bin"
patchfile = "data/patch.xdelta"


@common.cli.command()
@click.option("--rom", is_flag=True, default=False)
@click.option("--sce", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--nsbmd", is_flag=True, default=False)
def extract(rom, sce, img, nsbmd):
    all = not rom and not sce and not img and not nsbmd
    if all or rom:
        nds.extractRom(romfile, infolder, outfolder)
        import extract_xap
        extract_xap.run()
    if all or sce:
        import extract_sce
        extract_sce.run()
    if all or img:
        nitro.extractIMG("data/out_XAP/", "data/out_IMG/")
    if all or nsbmd:
        nitro.extractNSBMD("data/extract/data/data/model/", "data/out_NSBMD/")


@common.cli.command()
@click.option("--no-rom", is_flag=True, default=False)
@click.option("--sce", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--nsbmd", is_flag=True, default=False)
def repack(no_rom, sce, img, nsbmd):
    all = not sce and not img and not nsbmd
    if all or sce:
        import repack_sce
        repack_sce.run()
    if all or img:
        # TODO
        pass
    if all or nsbmd:
        # TODO
        pass
    if not no_rom:
        if os.path.isdir(replacefolder):
            common.mergeFolder(replacefolder, outfolder)
        nds.editBannerTitle(bannerfile, "DEATH NOTE\n-Kira Game-\nKonami Digital Entertainment")
        nds.repackRom(romfile, rompatch, outfolder, patchfile)


if __name__ == "__main__":
    click.echo("KiraGameTranslation version " + version)
    if not os.path.isdir("data"):
        common.logError("data folder not found.")
        quit()
    common.cli()
