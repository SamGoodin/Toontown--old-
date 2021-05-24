from panda3d.core import *
loadPrcFile("config/config.prc")

vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

from GameBase import GameBase

game = GameBase()
from direct.gui import DirectGuiGlobals
DirectGuiGlobals.setDefaultFont(loader.loadFont('phase_3/models/fonts/ImpressBT.ttf'))
DirectGuiGlobals.setDefaultRolloverSound(loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))

from StartMenu import StartMenu
StartMenu()

game.run()