from direct.interval.IntervalGlobal import Func
from direct.gui.DirectGui import *
from panda3d.core import TextNode
from direct.showbase.DirectObject import DirectObject
from Toon import Toon
import random
from direct.directnotify.DirectNotify import DirectNotify


class MakeAToon(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.notify = DirectNotify().newCategory("MakeAToon")
        self.music = loader.loadMusic("phase_3/audio/bgm/create_a_toon.ogg")
        self.music.setLoop(True)
        self.music.play()
        self.hprDelta = -1
        self.accept('l', self.devTool)
        base.transitions.fadeIn(finishIval=Func(self.enter))
        self.background = loader.loadModel('phase_3/models/makeatoon/tt_m_ara_mat_room')
        camera.setPosHpr(-5.7, -12.3501, 2.15, -24.8499, 2.73, 0)
        self.genderWalls = self.background.find('**/genderWalls')
        self.genderProps = self.background.find('**/genderProps')
        self.genderWalls.reparentTo(render)
        self.genderProps.reparentTo(render)
        self.floor = self.background.find('**/floor')
        self.floor.reparentTo(render)
        self.spotlightActor = loader.loadModel("phase_3/models/makeatoon/roomAnim_model")
        self.spotlightActor.reparentTo(render)
        self.spotlightJoint = self.spotlightActor.find('**/spotlightJoint')
        self.spotlight = self.background.find('**/spotlight')
        self.spotlight.reparentTo(self.spotlightJoint)
        self.spotlight.setColor(1, 1, 1, 0.3)
        self.spotlight.setPos(1.18, -1.27, 0.41)
        self.spotlight.setScale(2.6)
        self.spotlight.setHpr(0, 0, 0)
        self.mainFrame = DirectFrame(frameSize=(.5, -.5, -1, 1), pos=(-1.25, 1, 0), frameColor=(0, 0, 0, 0),
                                       image=(loader.loadModel('phase_3/models/gui/dialog_box_gui')),
                                       image_scale=(1, 1, 1.5))
        button = loader.loadModel("phase_3/models/gui/quit_button")
        self.colorBtn = DirectButton(text="Color", text_scale=0.15, text_pos=(0.01, -0.04), text_align=TextNode.ACenter,
                                     parent=self.mainFrame, relief=None, pos=(0, 0, 0),
                                     image=(button.find('**/QuitBtn_UP'), button.find('**/QuitBtn_DN'),
                                           button.find('**/QuitBtn_RLVR')), image_scale=2, command=self.enterColor)
        self.clothesBtn = DirectButton(text="Clothing", text_scale=0.15, text_pos=(0.01, -0.04), relief=None,
                                       text_align=TextNode.ACenter, parent=self.mainFrame, pos=(0, 0, -0.3),
                                       image=(button.find('**/QuitBtn_UP'), button.find('**/QuitBtn_DN'),
                                            button.find('**/QuitBtn_RLVR')), image_scale=2, command=self.enterClothing)
        self.genderBtn = DirectButton(text="Gender", text_scale=0.15, text_pos=(0.01, -0.04), parent=self.mainFrame,
                                      text_align=TextNode.ACenter, relief=None, pos=(0, 0, 0.6),
                                       image=(button.find('**/QuitBtn_UP'), button.find('**/QuitBtn_DN'),
                                              button.find('**/QuitBtn_RLVR')), image_scale=2, command=self.enterGender)
        self.bodyBtn = DirectButton(text="Body", text_scale=0.15, text_pos=(0.01, -0.04), parent=self.mainFrame,
                                      text_align=TextNode.ACenter, relief=None, pos=(0, 0, 0.3),
                                      image=(button.find('**/QuitBtn_UP'), button.find('**/QuitBtn_DN'),
                                             button.find('**/QuitBtn_RLVR')), image_scale=2, command=self.enterBody)
        self.nameBtn = DirectButton(text="Name", text_scale=0.15, text_pos=(0.01, -0.04), parent=self.mainFrame,
                                      text_align=TextNode.ACenter, relief=None, pos=(0, 0, -0.6),
                                      image=(button.find('**/QuitBtn_UP'), button.find('**/QuitBtn_DN'),
                                             button.find('**/QuitBtn_RLVR')), image_scale=2, command=self.enterName)
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        rotateUp = gui.find('**/tt_t_gui_mat_arrowRotateUp')
        rotateDown = gui.find('**/tt_t_gui_mat_arrowRotateDown')
        self.rotateLeftBtn = DirectButton(relief=None, image=(rotateUp, rotateDown, rotateUp, rotateDown),
                                          image_scale=(-0.5, 0.5, 0.5), image1_scale=(-0.6, 0.6, 0.6),
                                          image2_scale=(-0.6, 0.6, 0.6), pos=(-0.2, 0, -0.9))
        self.rotateLeftBtn.bind(DGG.B1PRESS, self.rotateToonLeft)
        self.rotateLeftBtn.bind(DGG.B1RELEASE, self.stopToonRotateLeftTask)
        self.rotateRightBtn = DirectButton(relief=None, image=(rotateUp, rotateDown, rotateUp, rotateDown),
                                          image_scale=(0.5, 0.5, 0.5), image1_scale=(0.6, 0.6, 0.6),
                                           image2_scale=(0.6, 0.6, 0.6), pos=(0.5, 0, -0.9))
        self.rotateRightBtn.bind(DGG.B1PRESS, self.rotateToonRight)
        self.rotateRightBtn.bind(DGG.B1RELEASE, self.stopToonRotateRightTask)
        self.toon = Toon().generateRandomToon()
        self.toon.reparentTo(render)
        self.toon.setHpr(160, 0, 0)
        self.toon.setPos(.7, .4, 0)
        self.toon.setScale(0.81)
        self.text = OnscreenText(text="Make a Toon", font=loader.loadFont("phase_3/models/fonts/MickeyFont"),
                                 align=TextNode.ACenter, pos=(0, 0.8, 0), scale=0.2, mayChange=True,
                                 fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1))

    def enter(self):
        pass

    def resetButtons(self):
        self.genderBtn['state'] = DGG.NORMAL
        self.bodyBtn['state'] = DGG.NORMAL
        self.colorBtn['state'] = DGG.NORMAL
        self.clothesBtn['state'] = DGG.NORMAL
        self.nameBtn['state'] = DGG.NORMAL

    def exitCurrentShop(self):
        if self.text.getText() == "Gender Shop":
            self.notify.info("Leaving gender shop")
            self.boyBtn.destroy()
            del self.boyBtn
            self.girlBtn.destroy()
            del self.girlBtn
        elif self.text.getText() == "Body Shop":
            self.notify.info("Leaving body shop")
            self.species.destroy()
            del self.species
            self.head.destroy()
            del self.head
            self.body.destroy()
            del self.body
            self.legs.destroy()
            del self.legs
        elif self.text.getText() == "Color Shop":
            self.notify.info("Leaving color shop")
        elif self.text.getText() == "Clothing Shop":
            self.notify.info("Leaving clothing shop")
        elif self.text.getText() == "Name Shop":
            self.notify.info("Leaving name shop")
        else:
            self.notify.warning("Can't exit a shop if you haven't entered")

    def enterGender(self):
        self.exitCurrentShop()
        self.text.setText("Gender Shop")
        self.resetButtons()
        self.genderBtn['state'] = DGG.DISABLED
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        guiBoyUp = gui.find('**/tt_t_gui_mat_boyUp')
        guiBoyDown = gui.find('**/tt_t_gui_mat_boyDown')
        guiGirlUp = gui.find('**/tt_t_gui_mat_girlUp')
        guiGirlDown = gui.find('**/tt_t_gui_mat_girlDown')
        self.boyBtn = DirectButton(relief=None, image=(guiBoyUp, guiBoyDown, guiBoyUp, guiBoyDown),
                                   image_scale=(1, 1, 1), image1_scale=(0.95, 0.95, 0.95),
                                   image2_scale=(0.95, 0.95, 0.95), pos=(1.2, 0, 0.5), text=('', "Boy", "Boy", ""),
                                   text_scale=0.2, text_pos=(0, 0.3), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                   command=self.generateRandomToon, extraArgs='m')
        self.girlBtn = DirectButton(relief=None, image=(guiGirlUp, guiGirlDown, guiGirlUp, guiGirlDown),
                                    image_scale=(1, 1, 1), image1_scale=(0.95, 0.95, 0.95),
                                    image2_scale=(0.95, 0.95, 0.95), pos=(1.2, 0, -0.5), text=("", "Girl", "Girl", ""),
                                    text_scale=0.2, text_pos=(0, -0.4), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                    command=self.generateRandomToon, extraArgs="f")
        guiBoyUp.removeNode()
        guiBoyDown.removeNode()
        guiGirlUp.removeNode()
        guiGirlDown.removeNode()
        gui.removeNode()

    def generateRandomToon(self, gender):
        self.toon.gender = gender
        self.toon.swapToonLegs(random.choice(["dgs", "dgm", "dgl"]), True)
        if gender == 'm':
            self.toon.swapToonTorso(random.choice(["ss", "ms", "ls"]), True)
        else:
            self.toon.swapToonTorso(random.choice(["sd", "md", "ld"]), True)
        self.toon.swapToonHead(mat=True)
        self.toon.generateToonColor(True)
        self.toon.loop("neutral")

    def enterBody(self):
        self.exitCurrentShop()
        self.text.setText("Body Shop")
        self.resetButtons()
        self.bodyBtn['state'] = DGG.DISABLED
        gui = loader.loadModel("phase_3/models/gui/tt_m_gui_mat_mainGui")
        guiRArrowUp = gui.find('**/tt_t_gui_mat_arrowUp')
        guiRArrowDown = gui.find('**/tt_t_gui_mat_arrowDown')
        guiRArrowRollover = gui.find('**/tt_t_gui_mat_arrowUp')
        guiRArrowDisabled = gui.find('**/tt_t_gui_mat_arrowDisabled')
        shuffleFrame = gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleArrowUp = gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDown = gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        shuffleArrowRollover = gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDisabled = gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
        upsellModel = loader.loadModel('phase_3/models/gui/tt_m_gui_ups_mainGui')
        self.species = DirectFrame(image=shuffleFrame, image_scale=0.5, relief=None, pos=(1.25, 0, 0.6), text="Species",
                                   text_scale=0.0625, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1), scale=2)
        self.speciesL = DirectButton(parent=self.species, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                     shuffleArrowRollover, shuffleArrowDisabled), image_scale=0.5, image1_scale=0.6,
                                     image2_scale=0.6, pos=(-0.166, 0, 0.003), extraArgs=[-1], command=self.swapSpecies)
        self.speciesR = DirectButton(parent=self.species, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                     shuffleArrowRollover, shuffleArrowDisabled), image_scale=-0.6, image1_scale=-0.7,
                                     image2_scale=-0.7, pos=(0.168, 0, 0), extraArgs=[1], command=self.swapSpecies)
        self.head = DirectFrame(image=shuffleFrame, image_scale=-0.5, relief=None, pos=(1.25, 0, 0.2), text="Head",
                                text_scale=0.0625, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1), scale=2)
        self.headL = DirectButton(parent=self.head, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                  shuffleArrowRollover, shuffleArrowDisabled), image_scale=0.6, image1_scale=0.7,
                                  image2_scale=0.7, pos=(-0.168, 0, 0), extraArgs=[-1], command=self.swapHead)
        self.headR = DirectButton(parent=self.head, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                  shuffleArrowRollover, shuffleArrowDisabled), image_scale=-0.5, image1_scale=-0.6,
                                  image2_scale=-0.6, pos=(0.167, 0, 0), extraArgs=[1], command=self.swapHead)
        self.body = DirectFrame(image=shuffleFrame, image_scale=0.5, relief=None, pos=(1.25, 0, -0.2), text="Body",
                                text_scale=0.0625, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1), scale=2)
        self.bodyL = DirectButton(parent=self.body, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                  shuffleArrowRollover, shuffleArrowDisabled), image_scale=0.5, image1_scale=0.6,
                                  image2_scale=0.6, pos=(-0.166, 0, 0.003), extraArgs=[-1], command=self.swapTorso)
        self.bodyR = DirectButton(parent=self.body, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                  shuffleArrowRollover, shuffleArrowDisabled), image_scale=-0.6, image1_scale=-0.7,
                                  image2_scale=-0.7, pos=(0.168, 0, 0), extraArgs=[1], command=self.swapTorso)
        self.legs = DirectFrame(image=shuffleFrame, image_scale=-0.5, relief=None, pos=(1.25, 0, -0.6), text="Legs",
                                text_scale=0.0625, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1), scale=2)
        self.legsL = DirectButton(parent=self.legs, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                  shuffleArrowRollover, shuffleArrowDisabled), image_scale=0.6, image1_scale=0.7,
                                  image2_scale=0.7, pos=(-0.168, 0, 0), extraArgs=[-1], command=self.swapLeg)
        self.legsR = DirectButton(parent=self.legs, relief=None, image=(shuffleArrowUp, shuffleArrowDown,
                                  shuffleArrowRollover, shuffleArrowDisabled), image_scale=-0.5, image1_scale=-0.6,
                                  image2_scale=-0.6, pos=(0.167, 0, 0), extraArgs=[1], command=self.swapLeg)
        gui.removeNode()
        guiRArrowUp.removeNode()
        guiRArrowDown.removeNode()
        guiRArrowRollover.removeNode()
        guiRArrowDisabled.removeNode()
        shuffleFrame.removeNode()
        shuffleArrowUp.removeNode()
        shuffleArrowDown.removeNode()
        shuffleArrowRollover.removeNode()
        shuffleArrowDisabled.removeNode()
        upsellModel.removeNode()
        self.speciesList = self.toon.getSpeciesList()
        if self.speciesList.index(self.toon.animalType) == 0:
            self.speciesL.hide()
            self.speciesR.show()
        elif self.speciesList.index(self.toon.animalType) == len(self.speciesList) - 1:
            self.speciesR.hide()
            self.speciesL.show()
        else:
            self.speciesL.show()
            self.speciesR.show()
        self.mouseHeadList = ["ss", "ls"]
        self.headList = ["ss", "sl", "ls", "ll"]
        if self.toon.animalType == "mouse":
            if self.mouseHeadList.index(self.toon.headStyle) == 0:
                self.headL.hide()
                self.headR.show()
            elif self.mouseHeadList.index(self.toon.headStyle) == 1:
                self.headR.hide()
                self.headL.show()
        else:
            if self.headList.index(self.toon.headStyle) == 0:
                self.headL.hide()
                self.headR.show()
            elif self.headList.index(self.toon.headStyle) == len(self.headList) - 1:
                self.headR.hide()
                self.headL.show()
            else:
                self.headL.show()
                self.headR.show()
        if self.toon.gender == "m":
            self.genderTorso = ["ss", "ms", "ls"]
        elif self.toon.gender == "f":
            self.genderTorso = ["sd", "md", "ld"]
        if self.toon.torsoStyle == "dgl":
            self.bodyR.hide()
            self.bodyL.show()
        elif self.toon.torsoStyle == "dgs":
            self.bodyL.hide()
            self.bodyR.show()
        self.legDict = ["dgs", "dgm", "dgl"]
        if self.toon.legStyle == "dgl":
            self.legsR.hide()
            self.legsL.show()
        elif self.toon.legStyle == "dgs":
            self.legsL.hide()
            self.legsR.show()

    def swapSpecies(self, step):
        curHead = self.speciesList.index(self.toon.animalType)
        new = curHead + step
        newStyle = []
        newStyle.append(self.speciesList[new])
        if self.speciesList[new] == 'mouse':
            newStyle.append(random.choice(["ss", "ls"]))
        else:
            newStyle.append(random.choice(["ss", "sl", "ls", "ll"]))
        self.toon.swapToonHead(newStyle)
        if new == 0:
            self.speciesL.hide()
            self.speciesR.show()
        elif new == len(self.speciesList) - 1:
            self.speciesR.hide()
            self.speciesL.show()
        else:
            self.speciesL.show()
            self.speciesR.show()
        if self.toon.animalType == "mouse":
            if self.mouseHeadList.index(self.toon.headStyle) == 0:
                self.headL.hide()
                self.headR.show()
            elif self.mouseHeadList.index(self.toon.headStyle) == 1:
                self.headR.hide()
                self.headL.show()
        else:
            if self.headList.index(self.toon.headStyle) == 0:
                self.headL.hide()
                self.headR.show()
            elif self.headList.index(self.toon.headStyle) == len(self.headList) - 1:
                self.headR.hide()
                self.headL.show()
            else:
                self.headL.show()
                self.headR.show()

    def swapHead(self, step):
        newStyle = []
        newStyle.append(self.toon.animalType)
        if self.toon.animalType == "mouse":
            curHead = self.mouseHeadList.index(self.toon.headStyle)
            newStyle.append(self.mouseHeadList[curHead + step])
            if (curHead + step) == 0:
                self.headL.hide()
                self.headR.show()
            elif (curHead + step) == 1:
                self.headR.hide()
                self.headL.show()
            else:
                print "This shouldn't occur"
        else:
            curHead = self.headList.index(self.toon.headStyle)
            newStyle.append(self.headList[curHead + step])
            if (curHead + step) == 0:
                self.headL.hide()
                self.headR.show()
            elif (curHead + step) == len(self.headList) - 1:
                self.headR.hide()
                self.headL.show()
            else:
                self.headL.show()
                self.headR.show()
        self.toon.swapToonHead(newStyle)


    def swapTorso(self, step):
        curTorso = self.genderTorso.index(self.toon.genderTorso)
        new = curTorso + step
        self.toon.swapToonTorso(self.genderTorso[new])
        self.toon.loop("neutral")
        if self.toon.torsoStyle == "dgl":
            self.bodyR.hide()
            self.bodyL.show()
        elif self.toon.torsoStyle == "dgs":
            self.bodyL.hide()
            self.bodyR.show()
        else:
            self.bodyL.show()
            self.bodyR.show()

    def swapLeg(self, step):
        curLeg = self.legDict.index(self.toon.legStyle)
        new = curLeg + step
        self.toon.swapToonLegs(self.legDict[new])
        self.toon.loop("neutral")
        if self.toon.legStyle == "dgl":
            self.legsR.hide()
            self.legsL.show()
        elif self.toon.legStyle == "dgs":
            self.legsL.hide()
            self.legsR.show()
        else:
            self.legsL.show()
            self.legsR.show()

    def enterColor(self):
        self.exitCurrentShop()
        self.text.setText("Color Shop")
        self.resetButtons()
        self.colorBtn['state'] = DGG.DISABLED

    def enterClothing(self):
        self.exitCurrentShop()
        self.text.setText("Clothing Shop")
        self.resetButtons()
        self.clothesBtn['state'] = DGG.DISABLED

    def enterName(self):
        self.exitCurrentShop()
        self.text.setText("Name Shop")
        self.resetButtons()
        self.nameBtn['state'] = DGG.DISABLED

    def devTool(self):
        print self.species.getPos(), self.head.getPos()

    def rotateToonLeft(self, event):
        taskMgr.add(self.rotateToonLeftTask, 'rotateToonLeftTask')

    def rotateToonLeftTask(self, task):
        self.toon.setH(self.toon.getH() + self.hprDelta)
        return task.cont

    def stopToonRotateLeftTask(self, event):
        taskMgr.remove('rotateToonLeftTask')

    def rotateToonRight(self, event):
        taskMgr.add(self.rotateToonRightTask, 'rotateToonRightTask')

    def rotateToonRightTask(self, task):
        self.toon.setH(self.toon.getH() - self.hprDelta)
        return task.cont

    def stopToonRotateRightTask(self, event):
        taskMgr.remove('rotateToonRightTask')