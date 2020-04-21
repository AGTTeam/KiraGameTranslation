import os
import click
import game
from hacktools import common, nds, nitro

version = "0.8.0"
romfile = "data/dn1.nds"
rompatch = "data/dn1_patched.nds"
infolder = "data/extract/"
replacefolder = "data/replace/"
outfolder = "data/repack/"
bannerfile = "data/repack/banner.bin"
patchfile = "data/patch.xdelta"


@common.cli.command()
@click.option("--rom", is_flag=True, default=False)
@click.option("--bin", is_flag=True, default=False)
@click.option("--sce", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--nsbmd", is_flag=True, default=False)
def extract(rom, bin, sce, img, nsbmd):
    all = not rom and not bin and not sce and not img and not nsbmd
    if all or rom:
        nds.extractRom(romfile, infolder, outfolder)
        import extract_xap
        extract_xap.run()
    if all or bin:
        nds.extractBIN(game.binrange)
    if all or sce:
        import extract_sce
        extract_sce.run()
    if all or img:
        nitro.extractIMG("data/extract_XAP/", "data/out_IMG/")
    if all or nsbmd:
        nitro.extractNSBMD("data/extract/data/data/model/", "data/out_NSBMD/")


@common.cli.command()
@click.option("--no-rom", is_flag=True, default=False)
@click.option("--bin", is_flag=True, default=False)
@click.option("--sce", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--nsbmd", is_flag=True, default=False)
def repack(no_rom, bin, sce, img, nsbmd):
    all = not bin and not sce and not img and not nsbmd
    if all or bin:
        nds.repackBIN(game.binrange)
    if all or sce:
        import repack_sce
        repack_sce.run()
    if all or img:
        nitro.repackIMG("data/work_IMG/", "data/extract_XAP/", "data/repack_XAP/", ".NCGR", None, None, True)
    if all or nsbmd:
        common.copyFolder("data/extract/data/data/model/", "data/repack/data/data/model/")
        nitro.repackNSBMD("data/work_NSBMD/", "data/extract/data/data/model/", "data/repack/data/data/model/")
    if not no_rom:
        import repack_xap
        repack_xap.run()
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