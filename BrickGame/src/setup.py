from distutils.core import setup
import py2exe
import sys
import os

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcr71.dll",):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    #sys.argv.append("-q")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.1.0"
        self.company_name = "No Company"
        self.copyright = "no copyright"
        self.name = "py2exe sample file"

game = Target(
    version = "0.1.0",
    name = "Brick Game",
    description = "Brick Game",
    script = "BrickGame.py",
    icon_resources = [(1, "game.ico")],
    dest_base = "BrickGame"
)

game_c = Target(
    version = "2.1.0",
    name = "Brick Game",
    description = "Brick Game with console",
    script = "BrickGame.py",
    icon_resources = [(1, "game.ico")],
    dest_base = "BrickGame_console"
)

excludes = ["doctest", "pdb", "unittest", "difflib", "inspect"]
includes = ["pygame.locals", "pygame.event", "pygame.rect"]
packages = ["pygame"]

options = {
    "compressed": True,
    "optimize": 2,
    "ascii": 1,
    "bundle_files": 1,
    "excludes": excludes,
    #"includes": includes,
    "packages": packages,
    "dist_dir": "..\dist"
}

setup(
    options = {
        "py2exe": options
    },
    data_files=[
        ("Fonts", ('Fonts\\_font1_.png', 'Fonts\\_font2_.png')),
        ("Images", ('Images\\icon.bmp', 'Images\\_screen_.png')),
    ],
    zipfile = None,
    console = [game_c],
    windows = [game],
    )
