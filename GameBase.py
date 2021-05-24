from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
#from direct.showbase.Transitions import Transitions
import os, shutil, atexit, tempfile
from direct.directnotify.DirectNotify import DirectNotify


class GameBase(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.notify = DirectNotify().newCategory("GameBase")
        self.winProps = WindowProperties()
        self.transitions.IrisModelName = 'phase_3/models/misc/iris'
        self.transitions.FadeModelName = 'phase_3/models/misc/fade'
        self.disableMouse()
        self.addCullBins()
        self.setCursorAndIcon()

    def addCullBins(self):
        cbm = CullBinManager.getGlobalPtr()
        cbm.addBin('ground', CullBinManager.BTUnsorted, 18)
        cbm.addBin('shadow', CullBinManager.BTBackToFront, 19)

    def setWinSize(self, x, y):
        self.winProps.setSize(x, y)
        self.setWinOrigin(-2, -2)
        self.win.requestProperties(self.winProps)
        self.notify.info("Window size changed")

    def setWinOrigin(self, x, y):
        self.winProps.setOrigin(x, y)
        self.win.requestProperties(self.winProps)

    def setFullscreen(self, flag):
        self.winProps.setFullscreen(flag)
        self.win.requestProperties(self.winProps)

    def garbageCollect(self):
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        self.notify.info("Garbage collected")

    def setCursorAndIcon(self):
        tempdir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, tempdir)
        vfs = VirtualFileSystem.getGlobalPtr()
        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('/phase_3/etc'))
        for filename in ['toonmono.cur', 'icon.ico']:
            p3filename = Filename(filename)
            found = vfs.resolveFilename(p3filename, searchPath)
            if not found:
                self.notify.warning("Failure to load cursor and icon")
                return
            with open(os.path.join(tempdir, filename), 'wb') as f:
                f.write(vfs.readFile(p3filename, False))
        wp = WindowProperties()
        wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'toonmono.cur')))
        wp.setIconFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'icon.ico')))
        self.win.requestProperties(wp)
        self.notify.info("Cursor and icon successfully loaded")

