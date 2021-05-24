from direct.actor.Actor import Actor
import ToonGlobals
import random
from panda3d.core import Multifile, Texture, NodePath
from direct.showbase.ShadowPlacer import ShadowPlacer
from pandac.PandaModules import BitMask32
from direct.directnotify.DirectNotify import DirectNotify

class Toon(Actor):

    def __init__(self):
        Actor.__init__(self)
        self.notify = DirectNotify().newCategory("Toon")
        self.__eyelashOpen = None
        self.__eyelashClosed = None
        self.shadowFileName = 'phase_3/models/props/drop_shadow'
        self.shadowPlacer = None
        self.dropShadow = None
        self.activeShadow = 0
        self.wantsActive = 1

    def deleteDropShadow(self):
        if self.shadowPlacer:
            self.shadowPlacer.delete()
            self.shadowPlacer = None
        if self.dropShadow:
            self.dropShadow.removeNode()
            self.dropShadow = None
        return

    def showShadow(self):
        if not ToonGlobals.globalDropShadowFlag:
            self.dropShadow.hide()
        else:
            self.dropShadow.show()

    def getShadowJoint(self):
        if hasattr(self, 'shadowJoint'):
            return self.shadowJoint
        shadowJoint = self.find('**/attachShadow')
        if shadowJoint.isEmpty():
            self.shadowJoint = NodePath(self)
        else:
            self.shadowJoint = shadowJoint
        return self.shadowJoint

    def setActiveShadow(self, isActive=1):
        isActive = isActive and self.wantsActive
        if not ToonGlobals.globalDropShadowFlag:
            self.storedActiveState = isActive
        if self.shadowPlacer != None:
            isActive = isActive and ToonGlobals.globalDropShadowFlag
            if self.activeShadow != isActive:
                self.activeShadow = isActive
                if isActive:
                    self.shadowPlacer.on()
                else:
                    self.shadowPlacer.off()
        return

    def initializeDropShadow(self, hasGeomNode=True):
        self.deleteDropShadow()
        if hasGeomNode:
            self.getGeomNode().setTag('cam', 'caster')
        dropShadow = loader.loadModel(self.shadowFileName)
        dropShadow.setScale(0.4)
        dropShadow.flattenMedium()
        dropShadow.setBillboardAxis(2)
        dropShadow.setColor(0.0, 0.0, 0.0, ToonGlobals.globalDropShadowGrayLevel, 1)
        self.shadowPlacer = ShadowPlacer(base.shadowTrav, dropShadow, BitMask32(1), BitMask32(2))
        self.dropShadow = dropShadow
        if not ToonGlobals.globalDropShadowFlag:
            self.dropShadow.hide()
        if self.getShadowJoint():
            dropShadow.reparentTo(self.getShadowJoint())
        else:
            self.dropShadow.hide()
        self.setActiveShadow(self.wantsActive)
        self.__globalDropShadowFlagChanged()
        self.__globalDropShadowGrayLevelChanged()

    def __globalDropShadowFlagChanged(self):
        if self.dropShadow != None:
            if ToonGlobals.globalDropShadowFlag == 0:
                if self.activeShadow == 1:
                    self.storedActiveState = 1
                    self.setActiveShadow(0)
            elif self.activeShadow == 0:
                self.setActiveShadow(1)
            self.showShadow()
        return

    def __globalDropShadowGrayLevelChanged(self):
        if self.dropShadow != None:
            self.dropShadow.setColor(0.0, 0.0, 0.0, ToonGlobals.globalDropShadowGrayLevel, 1)
        return

    def unparentToonParts(self):
        self.getPart('head').reparentTo(self.getGeomNode())
        self.getPart('torso').reparentTo(self.getGeomNode())
        self.getPart('legs').reparentTo(self.getGeomNode())

    def parentToonParts(self):
        self.attach("head", "torso", "def_head")
        self.attach("torso", "legs", "joint_hips")
        self.initializeDropShadow()

    def generateRandomToon(self):
        self.gender = random.choice(["m", "f"])
        self.legs = self.generateToonLegs(True)
        self.torso = self.generateToonTorso(True)
        self.generateToonHead(True)
        self.parentToonParts()
        self.generateToonColor(True)
        self.loop("neutral")
        return self

    def generateToonHead(self, mat=None):
        if mat:
            self.animalType = random.choice(ToonGlobals.allAnimalsList)
            if self.animalType == "mouse":
                self.headStyle = random.choice(['ss', 'ls'])
            else:
                self.headStyle = random.choice(['ss', 'sl', 'ls', 'll'])
        if self.animalType != "dog":
            pFile = Multifile()
            pFile.openRead("phase_3.mf")
            for file in pFile.getSubfileNames():
                if self.animalType in file and '1000' in file:
                    headFile = file
            pFile.close()
        else:
            headFile = random.choice(ToonGlobals.dogHeads)
        self.loadModel(headFile, "head")
        if self.animalType != "dog":
            if self.headStyle == 'ss':
                self.fixHeadShortShort()
            elif self.headStyle == 'sl':
                self.fixHeadShortLong()
            elif self.headStyle == 'ls':
                self.fixHeadLongShort()
            elif self.headStyle == 'll':
                self.fixHeadLongLong()
            else:
                print "ERROR"
        self.setupMuzzles()
        self.setupEyelashes()
        return self.getPart("head")

    def swapToonHead(self, headStyle=None, mat=None):
        self.unparentToonParts()
        self.removePart("head")
        if 'head' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['head']
        if mat:
            self.generateToonHead(mat)
        else:
            self.animalType = headStyle[0]
            self.headStyle = headStyle[1]
            self.generateToonHead()
        self.generateToonColor()
        self.parentToonParts()
        self.setupEyelashes()

    def fixHeadShortShort(self):
        for p in self.getPart("head").findAllMatches('**/*long*'):
            p.removeNode()

    def fixHeadLongLong(self):
        for p in self.getPart('head').findAllMatches('**/*short*'):
            p.removeNode()

    def fixHeadLongShort(self):
        if self.animalType != "duck" and self.animalType != "horse":
            if self.animalType == "rabbit":
                self.getPart("head").find('**/ears-long').removeNode()
            else:
                self.getPart("head").find('**/ears-short').removeNode()
        if self.animalType != "rabbit":
            self.getPart("head").find('**/eyes-short').removeNode()
        if self.animalType != "dog":
            self.getPart("head").find('**/joint_pupilL_short').removeNode()
            self.getPart("head").find('**/joint_pupilR_short').removeNode()
        self.getPart("head").find('**/head-short').removeNode()
        self.getPart("head").find('**/head-front-short').removeNode()
        if self.animalType != 'rabbit':
            muzzleParts = self.findAllMatches('**/muzzle-long*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                muzzleParts.getPath(partNum).removeNode()
        else:
            muzzleParts = self.findAllMatches('**/muzzle-short*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                muzzleParts.getPath(partNum).removeNode()

    def fixHeadShortLong(self):
        if self.animalType != "duck" and self.animalType != "horse":
            if self.animalType == "rabbit":
                self.getPart("head").find('**/ears-short').removeNode()
            else:
                self.getPart("head").find('**/ears-long').removeNode()
        if self.animalType != "rabbit":
            self.getPart("head").find('**/eyes-long').removeNode()
        if self.animalType != "dog":
            self.getPart("head").find('**/joint_pupilL_long').removeNode()
            self.getPart("head").find('**/joint_pupilR_long').removeNode()
        self.getPart("head").find('**/head-long').removeNode()
        self.getPart("head").find('**/head-front-long').removeNode()
        if self.animalType != "rabbit":
            muzzleParts = self.findAllMatches('**/muzzle-short*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                muzzleParts.getPath(partNum).removeNode()
        else:
            muzzleParts = self.findAllMatches('**/muzzle-long*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                muzzleParts.getPath(partNum).removeNode()

    def setupEyelashes(self):
        if self.gender == "m":
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
                self.__eyelashOpen = None
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
                self.__eyelashClosed = None
        else:
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
            model = loader.loadModel('phase_3' + ToonGlobals.EyelashDict[self.animalType])
            if "l" in self.headStyle:
                openString = 'open-long'
                closedString = 'closed-long'
            else:
                openString = 'open-short'
                closedString = 'closed-short'
            eyeOpen = model.find('**/' + openString)
            eyeClosed = model.find('**/' + closedString)
            if self.animalType == "dog":
                eyeOpen.setPos(0, -0.025, 0.025)
                eyeClosed.setPos(0, -0.025, 0.025)
            self.__eyelashOpen = eyeOpen.copyTo(self.getPart("head"))
            self.__eyelashClosed = eyeClosed.copyTo(self.getPart("head"))
            eyeOpen.removeNode()
            eyeClosed.removeNode()
            model.removeNode()
            self.__eyelashClosed.hide()
        return

    def setupMuzzles(self):
        self.__muzzles = []
        self.__surpriseMuzzles = []
        self.__angryMuzzles = []
        self.__sadMuzzles = []
        self.__smileMuzzles = []
        self.__laughMuzzles = []

        def hideAddNonEmptyItemToList(item, list):
            if not item.isEmpty():
                item.hide()
                list.append(item)

        def hideNonEmptyItem(item):
            if not item.isEmpty():
                item.hide()

        if self.animalType != "dog":
            muzzle = self.getPart("head").find("**/muzzle*neutral")
        else:
            muzzle = self.getPart("head").find("**/muzzle*")
            file = ToonGlobals.DogMuzzleDict[self.headStyle]
            muzzles = loader.loadModel("phase_3" + file + '1000')
            if not self.find('**/def_head').isEmpty():
                muzzles.reparentTo(self.getPart("head").find('**/def_head'))
            else:
                muzzles.reparentTo(self.find('**/joint_toHead'))
        surpriseMuzzle = self.find('**/muzzle*surprise')
        angryMuzzle = self.find('**/muzzle*angry')
        sadMuzzle = self.find('**/muzzle*sad')
        smileMuzzle = self.find('**/muzzle*smile')
        laughMuzzle = self.find('**/muzzle*laugh')
        self.__muzzles.append(muzzle)
        hideAddNonEmptyItemToList(surpriseMuzzle, self.__surpriseMuzzles)
        hideAddNonEmptyItemToList(angryMuzzle, self.__angryMuzzles)
        hideAddNonEmptyItemToList(sadMuzzle, self.__sadMuzzles)
        hideAddNonEmptyItemToList(smileMuzzle, self.__smileMuzzles)
        hideAddNonEmptyItemToList(laughMuzzle, self.__laughMuzzles)

    def generateToonLegs(self, mat=None):
        if mat:
            self.legStyle = random.choice(['dgs', 'dgm', 'dgl'])
        self.loadModel("phase_3" + ToonGlobals.LegDict.get(self.legStyle) + "1000", "legs")
        self.findAllMatches('**/boots_short').stash()
        self.findAllMatches('**/boots_long').stash()
        self.findAllMatches('**/shoes').stash()
        self.loadLegAnims()
        return self.getPart("legs")

    def generateToonTorso(self, mat=None):
        if mat:
            if self.gender == 'm':
                self.torsoStyle = random.choice(['ss', 'ms', 'ls'])
            elif self.gender == 'f':
                self.torsoStyle = random.choice(['sd', 'md', 'ld'])
        self.loadModel("phase_3" + ToonGlobals.TorsoDict.get(self.torsoStyle) + "1000", "torso")
        self.genderTorso = self.torsoStyle
        self.torsoStyle = ToonGlobals.TorsoStyleConverter.get(self.torsoStyle)
        self.loadTorsoAnims()
        self.generateToonClothes(mat)
        return self.getPart("torso")

    def generateToonClothes(self, ran=False):
        if ran:
            self.shirtColor = random.choice(ToonGlobals.ClothesColors)
            if self.gender == 'm':
                self.bottomPair = random.choice(ToonGlobals.BoyShorts)
            else:
                self.bottomPair = random.choice(ToonGlobals.GirlBottoms)
                self.bottomPair = self.bottomPair[0]
            self.bottomColor = random.choice(ToonGlobals.ClothesColors)
            self.darkBottomColor = self.bottomColor * 0.5
            self.darkBottomColor.setW(1.0)
            self.shirtChoice = random.choice(ToonGlobals.Shirts)
            self.sleevesChoice = ToonGlobals.Sleeves[ToonGlobals.Shirts.index(self.shirtChoice)]
        shirtTex = loader.loadTexture(self.shirtChoice, okMissing=True)
        shirtTex.setMinfilter(Texture.FTLinearMipmapLinear)
        shirtTex.setMagfilter(Texture.FTLinear)
        sleeveTex = loader.loadTexture(self.sleevesChoice, okMissing=True)
        sleeveTex.setMinfilter(Texture.FTLinearMipmapLinear)
        sleeveTex.setMagfilter(Texture.FTLinear)
        self.sleeveColor = self.shirtColor
        bottomTex = loader.loadTexture(self.bottomPair, okMissing=True)
        bottomTex.setMinfilter(Texture.FTLinearMipmapLinear)
        bottomTex.setMagfilter(Texture.FTLinear)
        self.top = self.getPart("torso").find('**/torso-top')
        self.top.setTexture(shirtTex, 1)
        self.top.setColor(self.shirtColor)
        self.sleeves = self.getPart("torso").find('**/sleeves')
        self.sleeves.setTexture(sleeveTex, 1)
        self.sleeves.setColor(self.sleeveColor)
        self.bottoms = self.getPart("torso").findAllMatches('**/torso-bot')
        for part in range(0, self.bottoms.getNumPaths()):
            bottom = self.bottoms.getPath(part)
            bottom.setTexture(bottomTex, 1)
            bottom.setColor(self.bottomColor)
        self.caps = self.getPart("torso").findAllMatches('**/torso-bot-cap')
        self.caps.setColor(self.darkBottomColor)

    def swapToonTorso(self, torsoStyle, ran=False):
        self.unparentToonParts()
        self.unloadAnims("neutral", "torso")
        self.removePart("torso")
        if 'torso' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['torso']
        self.torsoStyle = torsoStyle
        self.torso = self.generateToonTorso(ran)
        self.generateToonColor(ran)
        self.parentToonParts()

    def swapToonLegs(self, legStyle, ran=False):
        self.unparentToonParts()
        self.unloadAnims("neutral", "legs")
        self.removePart('legs')
        if 'legs' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['legs']
        self.legStyle = legStyle
        self.legs = self.generateToonLegs(ran)
        self.generateToonColor(ran)
        self.parentToonParts()

    def loadLegAnims(self):
        pFile = Multifile()
        for phaseFile in ToonGlobals.PhaseAnimsDict:
            pFile.openRead(phaseFile)
            for file in pFile.getSubfileNames():
                if self.legStyle in file and "shorts" in file and 'legs' in file:
                    if '1000' not in file and '500' not in file and '250' not in file:
                        for anim in ToonGlobals.PhaseAnimsDict.get(phaseFile):
                            if anim in file:
                                self.loadAnims({anim: file}, 'legs')
            pFile.close()

    def loadTorsoAnims(self):
        if self.gender == "m":
            gender = "shorts"
        else:
            gender = "skirt"
        pFile = Multifile()
        for phaseFile in ToonGlobals.PhaseAnimsDict:
            pFile.openRead(phaseFile)
            for file in pFile.getSubfileNames():
                if self.torsoStyle in file and gender in file and 'torso' in file:
                    if '1000' not in file and '500' not in file and '250' not in file:
                        for anim in ToonGlobals.PhaseAnimsDict.get(phaseFile):
                            if anim in file:
                                self.loadAnims({anim: file}, 'torso')
            pFile.close()

    def generateToonColor(self, ran=False):
        if ran:
            self.armColor = random.choice(ToonGlobals.allColorsList)
            self.legColor = self.armColor
            self.headColor = self.armColor
        self.torso.find('**/hands').setColor(ToonGlobals.allColorsList[0])
        for pieceName in ('arms', 'neck'):
            self.torso.find('**/' + pieceName).setColor(self.armColor)
        for pieceName in ('legs', 'feet'):
            self.legs.find('**/%s;+s' % pieceName).setColor(self.legColor)
        self.findAllMatches('**/head*').setColor(self.headColor)
        if self.animalType == 'cat' or self.animalType == 'rabbit' or self.animalType == 'bear' or \
                        self.animalType == 'mouse' or self.animalType == 'pig':
            self.getPart("head").findAllMatches('**/*ears*').setColor(self.headColor)

    def getSpeciesList(self):
        return ToonGlobals.allAnimalsList