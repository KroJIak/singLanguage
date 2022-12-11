from cv2 import VideoCapture, imdecode, resize, imshow, line, waitKey, destroyAllWindows, cvtColor, COLOR_BGR2RGB, circle, FILLED, IMREAD_COLOR
from time import time
from math import hypot, acos, degrees, sqrt
import mediapipe as mp
import numpy as np
import sys
import matplotlib.pyplot as plt

class handDetector():
    def __init__(self, mode=False, maxHands=1, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.model_complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def getImg(self, img):
        self.img = img
        self.width, self.height = self.img.shape[1], self.img.shape[0]

    def getResults(self):
        self.imgRGB = cvtColor(self.img, COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)

    def drawPoints(self, drawAllHand=True, points=[], color=(255,255,255)):
        self.getResults()
        if self.results.multi_hand_landmarks:
            if drawAllHand:
                self.pos = self.getPositions()
                if len(self.pos) == 21:
                    for point in range(1, 21):
                        self.prePoint = self.parentPoint[point]
                        pos1 = [self.pos[self.prePoint][0], self.pos[self.prePoint][1]]
                        pos2 = [self.pos[point][0], self.pos[point][1]]
                        line(self.img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), color, 3)
            if len(points) != 0:
                for handLms in self.results.multi_hand_landmarks:
                    for num, pos in enumerate(handLms.landmark):
                        self.x, self.y = int(pos.x*self.width), int(pos.y*self.height)
                        if num in points:
                            circle(self.img, (self.x, self.y), 4, (224, 224, 224), FILLED)
                            circle(self.img, (self.x, self.y), 3, (237, 70, 47), FILLED)


    def getPositions(self, numHand=0):
        self.posDict = {}
        self.getResults()
        if self.results.multi_hand_landmarks:
            self.hand = self.results.multi_hand_landmarks[numHand]
            for num, pos in enumerate(self.hand.landmark):
                self.x, self.y = int(pos.x*self.width), int(pos.y*self.height)
                if 0 <= self.x < self.width and 0 <= self.y < self.height:
                    self.posDict[num] = [self.x, self.y]
        return self.posDict

detector = handDetector(maxHands=1, detectionCon=0.1)
detectorWord = handDetector(maxHands=1, detectionCon=0.1)

#pyuic5 -x uis\welcome.ui -o welcome.py

parentPoint = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
posList = { 'А': {0: [402, 315], 1: [389, 233], 2: [339, 160], 3: [287, 116], 4: [239, 116], 5: [264, 174], 6: [208, 145], 7: [265, 172], 8: [288, 186], 9: [248, 223], 10: [212, 198], 11: [282, 228], 12: [288, 236], 13: [240, 274], 14: [208, 247], 15: [274, 270], 16: [282, 279], 17: [232, 329], 18: [204, 301], 19: [251, 308], 20: [265, 319]},
            'Б': {0: [409, 411], 1: [335, 393], 2: [292, 343], 3: [261, 305], 4: [235, 269], 5: [319, 246], 6: [301, 164], 7: [286, 113], 8: [273, 71], 9: [316, 234], 10: [289, 182], 11: [290, 204], 12: [298, 223], 13: [315, 231], 14: [283, 187], 15: [287, 227], 16: [297, 256], 17: [317, 234], 18: [296, 182], 19: [293, 185], 20: [303, 191]},
            'В': {0: [329, 462], 1: [386, 412], 2: [412, 338], 3: [425, 279], 4: [452, 242], 5: [359, 257], 6: [360, 177], 7: [358, 128], 8: [354, 87], 9: [322, 259], 10: [321, 170], 11: [319, 116], 12: [316, 70], 13: [286, 274], 14: [283, 192], 15: [282, 141], 16: [281, 98], 17: [250, 304], 18: [245, 241], 19: [244, 203], 20: [245, 168]},
            'Г': {0: [443, 215], 1: [385, 221], 2: [320, 263], 3: [266, 316], 4: [231, 351], 5: [379, 244], 6: [364, 262], 7: [354, 279], 8: [351, 291], 9: [417, 242], 10: [392, 270], 11: [382, 293], 12: [379, 312], 13: [448, 226], 14: [411, 252], 15: [397, 278], 16: [389, 301], 17: [473, 206], 18: [434, 202], 19: [401, 194], 20: [368, 190]},
            'Д': {0: [440, 257], 1: [410, 259], 2: [359, 252], 3: [304, 212], 4: [260, 175], 5: [392, 290], 6: [358, 304], 7: [327, 304], 8: [300, 301], 9: [386, 272], 10: [349, 278], 11: [316, 280], 12: [288, 280], 13: [378, 251], 14: [337, 246], 15: [310, 244], 16: [290, 241], 17: [371, 229], 18: [334, 215], 19: [310, 210], 20: [289, 205]},
            'Ж': {0: [418, 327], 1: [370, 309], 2: [320, 267], 3: [265, 241], 4: [222, 225], 5: [375, 173], 6: [285, 169], 7: [224, 179], 8: [182, 188], 9: [370, 170], 10: [283, 172], 11: [225, 184], 12: [180, 193], 13: [363, 174], 14: [281, 178], 15: [232, 187], 16: [192, 191], 17: [355, 186], 18: [290, 183], 19: [250, 187], 20: [217, 189]},
            'З': {0: [380, 346], 1: [346, 337], 2: [307, 293], 3: [268, 255], 4: [234, 227], 5: [352, 205], 6: [333, 149], 7: [303, 112], 8: [276, 83], 9: [332, 209], 10: [285, 187], 11: [282, 213], 12: [299, 223], 13: [312, 220], 14: [260, 209], 15: [264, 248], 16: [288, 263], 17: [300, 238], 18: [252, 233], 19: [254, 262], 20: [277, 280]},
            'И': {0: [326, 415], 1: [377, 390], 2: [404, 318], 3: [399, 263], 4: [369, 235], 5: [357, 257], 6: [358, 195], 7: [365, 189], 8: [372, 198], 9: [323, 254], 10: [314, 185], 11: [323, 184], 12: [332, 195], 13: [288, 261], 14: [277, 183], 15: [271, 129], 16: [266, 85], 17: [255, 279], 18: [249, 220], 19: [247, 179], 20: [246, 142]},
            'Й': {0: [331, 431], 1: [380, 390], 2: [401, 316], 3: [394, 260], 4: [358, 239], 5: [356, 258], 6: [354, 195], 7: [359, 189], 8: [366, 205], 9: [322, 255], 10: [308, 186], 11: [315, 179], 12: [324, 188], 13: [289, 263], 14: [275, 185], 15: [271, 131], 16: [271, 90], 17: [257, 284], 18: [250, 227], 19: [247, 185], 20: [247, 148]},
            'К': {0: [383, 437], 1: [417, 380], 2: [408, 313], 3: [368, 278], 4: [328, 262], 5: [389, 257], 6: [377, 181], 7: [368, 133], 8: [356, 94], 9: [353, 264], 10: [339, 181], 11: [329, 127], 12: [318, 85], 13: [319, 284], 14: [303, 235], 15: [327, 271], 16: [343, 305], 17: [288, 314], 18: [276, 269], 19: [302, 289], 20: [321, 318]},
            'Н': {0: [328, 493], 1: [371, 435], 2: [381, 353], 3: [338, 297], 4: [288, 275], 5: [369, 280], 6: [387, 190], 7: [399, 139], 8: [406, 95], 9: [319, 275], 10: [308, 178], 11: [306, 117], 12: [301, 70], 13: [276, 290], 14: [258, 213], 15: [276, 234], 16: [288, 263], 17: [238, 320], 18: [200, 262], 19: [180, 224], 20: [161, 191]},
            'О': {0: [353, 480], 1: [292, 411], 2: [255, 338], 3: [220, 285], 4: [196, 236], 5: [359, 274], 6: [307, 188], 7: [257, 198], 8: [227, 222], 9: [376, 267], 10: [345, 171], 11: [314, 120], 12: [290, 74], 13: [379, 272], 14: [364, 181], 15: [349, 130], 16: [338, 87], 17: [367, 279], 18: [358, 207], 19: [347, 165], 20: [335, 130]},
            'Р': {0: [416, 328], 1: [408, 286], 2: [364, 247], 3: [299, 251], 4: [257, 258], 5: [365, 202], 6: [306, 160], 7: [266, 133], 8: [235, 113], 9: [344, 227], 10: [294, 207], 11: [272, 214], 12: [266, 226], 13: [331, 249], 14: [282, 229], 15: [270, 237], 16: [273, 251], 17: [327, 271], 18: [286, 260], 19: [266, 262], 20: [260, 271]},
            'С': {0: [396, 372], 1: [342, 363], 2: [291, 323], 3: [246, 288], 4: [210, 257], 5: [369, 236], 6: [318, 169], 7: [263, 153], 8: [218, 160], 9: [377, 224], 10: [324, 153], 11: [261, 140], 12: [212, 148], 13: [376, 221], 14: [319, 158], 15: [259, 146], 16: [214, 153], 17: [367, 225], 18: [315, 176], 19: [268, 160], 20: [231, 162]},
            'У': {0: [359, 355], 1: [407, 314], 2: [440, 250], 3: [471, 201], 4: [506, 175], 5: [386, 189], 6: [372, 151], 7: [376, 195], 8: [386, 235], 9: [344, 196], 10: [334, 165], 11: [346, 217], 12: [357, 254], 13: [306, 210], 14: [290, 161], 15: [305, 204], 16: [322, 242], 17: [274, 230], 18: [236, 183], 19: [207, 154], 20: [185, 126]},
            'Ф': {0: [353, 373], 1: [317, 321], 2: [300, 253], 3: [277, 195], 4: [255, 150], 5: [408, 197], 6: [331, 147], 7: [274, 137], 8: [236, 137], 9: [391, 193], 10: [316, 152], 11: [259, 145], 12: [214, 147], 13: [370, 194], 14: [299, 156], 15: [251, 152], 16: [213, 151], 17: [351, 199], 18: [295, 165], 19: [261, 163], 20: [233, 163]},
            'Х': {0: [386, 364], 1: [385, 314], 2: [358, 258], 3: [304, 237], 4: [267, 237], 5: [394, 203], 6: [380, 125], 7: [339, 101], 8: [307, 100], 9: [366, 215], 10: [333, 151], 11: [318, 147], 12: [322, 140], 13: [340, 235], 14: [284, 216], 15: [297, 247], 16: [330, 255], 17: [316, 259], 18: [269, 241], 19: [276, 268], 20: [299, 286]},
            'Ц': {0: [321, 441], 1: [367, 415], 2: [379, 357], 3: [351, 314], 4: [313, 290], 5: [380, 275], 6: [384, 193], 7: [381, 144], 8: [378, 102], 9: [338, 273], 10: [338, 184], 11: [336, 128], 12: [335, 82], 13: [297, 289], 14: [292, 254], 15: [302, 300], 16: [309, 337], 17: [260, 318], 18: [261, 289], 19: [279, 325], 20: [291, 359]},
            'Ч': {0: [391, 395], 1: [332, 329], 2: [285, 253], 3: [234, 201], 4: [188, 173], 5: [389, 179], 6: [300, 132], 7: [236, 129], 8: [187, 134], 9: [379, 180], 10: [289, 141], 11: [230, 148], 12: [183, 162], 13: [365, 188], 14: [280, 160], 15: [231, 163], 16: [190, 171], 17: [350, 205], 18: [281, 185], 19: [240, 188], 20: [204, 193]},
            'Ш': {0: [314, 468], 1: [361, 431], 2: [365, 358], 3: [322, 302], 4: [275, 279], 5: [373, 282], 6: [367, 187], 7: [361, 132], 8: [354, 88], 9: [333, 276], 10: [326, 180], 11: [317, 121], 12: [313, 73], 13: [296, 286], 14: [287, 199], 15: [284, 144], 16: [283, 97], 17: [263, 311], 18: [253, 265], 19: [262, 272], 20: [270, 290]},
            'Щ': {0: [326, 473], 1: [368, 418], 2: [368, 339], 3: [320, 287], 4: [270, 270], 5: [372, 277], 6: [371, 192], 7: [366, 140], 8: [359, 95], 9: [333, 273], 10: [328, 183], 11: [324, 127], 12: [321, 76], 13: [297, 284], 14: [288, 200], 15: [289, 147], 16: [289, 100], 17: [265, 305], 18: [255, 259], 19: [267, 271], 20: [277, 291]},
            'Ъ': {0: [356, 463], 1: [404, 413], 2: [429, 334], 3: [448, 267], 4: [481, 221], 5: [378, 266], 6: [347, 186], 7: [320, 142], 8: [298, 102], 9: [339, 282], 10: [294, 263], 11: [308, 325], 12: [333, 335], 13: [303, 301], 14: [261, 288], 15: [282, 342], 16: [310, 346], 17: [268, 321], 18: [232, 299], 19: [249, 337], 20: [272, 351]},
            'Ы': {0: [343, 487], 1: [384, 431], 2: [385, 359], 3: [345, 308], 4: [299, 285], 5: [382, 290], 6: [386, 205], 7: [387, 150], 8: [385, 103], 9: [338, 292], 10: [322, 221], 11: [328, 260], 12: [336, 299], 13: [298, 305], 14: [281, 245], 15: [295, 280], 16: [308, 315], 17: [261, 326], 18: [237, 266], 19: [227, 231], 20: [219, 198]},
            'Ь': {0: [356, 462], 1: [402, 411], 2: [428, 333], 3: [450, 268], 4: [480, 224], 5: [378, 272], 6: [349, 190], 7: [322, 143], 8: [302, 103], 9: [339, 287], 10: [297, 264], 11: [307, 317], 12: [331, 337], 13: [303, 306], 14: [265, 288], 15: [278, 333], 16: [303, 346], 17: [270, 327], 18: [236, 302], 19: [245, 332], 20: [263, 348]},
            'Э': {0: [440, 398], 1: [396, 372], 2: [333, 340], 3: [266, 336], 4: [216, 339], 5: [365, 225], 6: [307, 152], 7: [254, 147], 8: [218, 152], 9: [355, 233], 10: [272, 236], 11: [280, 282], 12: [314, 295], 13: [341, 251], 14: [269, 260], 15: [288, 296], 16: [319, 300], 17: [329, 271], 18: [275, 277], 19: [279, 305], 20: [295, 320]},
            'Ю': {0: [384, 422], 1: [321, 393], 2: [268, 334], 3: [214, 286], 4: [166, 259], 5: [351, 244], 6: [250, 208], 7: [194, 223], 8: [163, 239], 9: [359, 230], 10: [258, 194], 11: [202, 215], 12: [173, 242], 13: [355, 229], 14: [264, 195], 15: [217, 211], 16: [192, 228], 17: [344, 234], 18: [291, 182], 19: [271, 156], 20: [261, 135]},
            'Я': {0: [447, 395], 1: [398, 399], 2: [339, 362], 3: [281, 324], 4: [243, 286], 5: [360, 251], 6: [287, 183], 7: [236, 139], 8: [194, 109], 9: [353, 233], 10: [289, 157], 11: [234, 120], 12: [188, 91], 13: [343, 233], 14: [273, 214], 15: [283, 259], 16: [304, 288], 17: [333, 245], 18: [281, 225], 19: [286, 254], 20: [301, 276]}}

def showWord(word):
    f = open('alphabet/'+word+'.png', 'rb')
    chunk = f.read()
    chunkArr = np.frombuffer(chunk, dtype=np.uint8)
    imgWord = imdecode(chunkArr, IMREAD_COLOR)
    detectorWord.getImg(imgWord)
    detectorWord.drawPoints()
    imgWord = resize(imgWord, (int(imgWord.shape[1] * scalePWord / 100), int(imgWord.shape[0] * scalePWord / 100)))
    imshow('Word', imgWord)

def setCamera(mode=0):
    global img
    success, img = camera.read()
    detector.getImg(img)
    if mode == 1: detector.drawPoints(color=(0,255,0))

def showCamera():
    global img
    img = resize(img, (int(img.shape[1] * scalePCam / 100), int(img.shape[0] * scalePCam / 100)))
    imshow('Camera', img)

def getPerc(word, prePoint, point):
    global arrPerc
    pos1 = [posList[word][prePoint][0], posList[word][prePoint][1]]
    pos2 = [posList[word][point][0], posList[word][point][1]]
    dwx, dwy = pos2[0] - pos1[0], pos1[1] - pos2[1]
    pos1 = [pos[prePoint][0], pos[prePoint][1]]
    pos2 = [pos[point][0], pos[point][1]]
    dx, dy = pos2[0] - pos1[0], pos1[1] - pos2[1]
    whyp, hyp = hypot(dwx, dwy), hypot(dx, dy)
    try:
        deg = degrees(acos((dx * dwx + dy * dwy) / (whyp * hyp)))
        hp = min(whyp, hyp) / max(whyp, hyp)
        dp = 1 - deg / 180
        return int((sqrt(hp * dp)) * 100) - (100 - arrPerc[prePoint])
    except:
        return 0


def drawLines(prePoint, point):
    global arrPerc
    pos1 = [pos[prePoint][0], pos[prePoint][1]]
    pos2 = [pos[point][0], pos[point][1]]
    line(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (255 * arrPerc[point] // 100, 255 * arrPerc[point] // 100, 255), 3)

def main():
    global pos, arrPerc
    for word in posList:
        showWord(word)
        arrPerc = [0] * 21
        arrPerc[0] = 100
        flagSet = {-1}
        bTime = time() + 1
        while time() < bTime:
            setCamera()
            pos = detector.getPositions()
            if len(pos) == 21:
                for point in range(1, 21):
                    prePoint = parentPoint[point]
                    arrPerc[point] = getPerc(word, prePoint, point)
                    if arrPerc[point] < 0: arrPerc[point] = 0
                    if len(flagSet) != 0: drawLines(prePoint, point)
                flagSet = set(range(100-inaccuracy)).intersection(set(arrPerc))
                if len(flagSet) != 0: bTime = time() + 2
                else: setCamera(mode=1)
            else: bTime = time() + 2
            showCamera()
            key = waitKey(1)
            if key == 32: break
            elif key == 27: sys.exit()


scalePCam = 100
scalePWord = 100
inaccuracy = 75

if __name__ == '__main__':
    camera = VideoCapture(0)
    main()
    camera.release()
    destroyAllWindows()