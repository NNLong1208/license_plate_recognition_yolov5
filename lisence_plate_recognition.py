from lisence_plate_detection import *
from character_recognition import *
import numpy as np
class lisence_plate_recognition():
    def __init__(self):
        self.lpd = lisence_plate_detection()
        self.cd = character_recognition()

    def predict(self, img):
        point, img_crop = self.lpd.detect(img)
        if len(img_crop) != 0:
            pred = self.cd.detect(img_crop[0])
            char = self.get_char(pred)
            return char
        return None

    def get_char(self, pred):
        char = []
        names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-']
        for ele in pred:
            char.append(names[int(ele[5])])
        char.insert(2, '-')
        char.insert(5, ' ')
        char = ''.join(char)
        return char