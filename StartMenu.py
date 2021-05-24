from direct.gui.DirectGui import *
import random
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func
from panda3d.core import ModelPool, TexturePool


class StartMenu(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        base.transitions.irisIn(finishIval=Func(self.enter))
        self.bg = loader.loadModel("phase_3/models/gui/entering-background")
        self.bg.reparentTo(base.aspect2d)
        self.bg.setScale(2)
        button = loader.loadModel("phase_3/models/gui/quit_button")
        self.enterGameBtn = DirectButton(image=(button.find('**/QuitBtn_UP'), button.find('**/QuitBtn_DN'),
                                           button.find('**/QuitBtn_RLVR')), relief=None, command=self.exit,
                                    image_scale=2, text="Enter Game", text_scale=0.1, text_pos=(0.01, -0.025),
                                         state=DGG.DISABLED)
        button.removeNode()
        del button
        self.version = DirectLabel(text=base.config.GetString('game-version'), scale=0.05, relief=None, parent=self.bg,
                                   pos=(0.794444, 0, -0.490278))
        self.music = random.choice([loader.loadMusic("phase_3/audio/bgm/ttr_theme.ogg"),
                                    loader.loadMusic("phase_3/audio/bgm/ttr_d_theme_phase1.ogg"),
                                    loader.loadMusic("phase_3/audio/bgm/ttr_d_theme_phase2.ogg"),
                                    loader.loadMusic("phase_3/audio/bgm/ttr_d_theme_phase2_loop.ogg")])
        self.music.setLoop(True)
        self.music.play()

    def enter(self):
        self.enterGameBtn['state'] = DGG.NORMAL

    def enterMakeAToon(self):
        from MakeAToon import MakeAToon
        self.makeAToon = MakeAToon()

    def exit(self):
        base.transitions.fadeOut(finishIval=Sequence(Func(self.destroy), Func(self.enterMakeAToon)))
        '''self.destroy()
        self.enterMakeAToon()'''

    def destroy(self):
        self.bg.removeNode()
        del self.bg
        self.enterGameBtn.destroy()
        del self.enterGameBtn
        self.version.destroy()
        del self.version
        self.music.stop()
        del self.music
        base.garbageCollect()
