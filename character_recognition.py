import torch.backends.cudnn as cudnn
from models.experimental import attempt_load
from utils.general import non_max_suppression
from modules.pre_process import pre_process_yolo
from utils.torch_utils import select_device
from modules.modules import *

class character_recognition():
    def __init__(self, path_model = r'./models/recognition_best.pt'):
        try:
            self.__device = select_device('0')
            self.__model  = attempt_load(path_model, map_location=self.__device)
            self.__model.half()
            cudnn.benchmark = True
        except:
            print('Load model fail')

    def detect(self, img, thred = 0.5):
        img = cv2.resize(img, (640, 480))
        img_ = pre_process_yolo(img, self.__device, True)
        pred = self.__model(img_, augment=False)[0]
        pred = non_max_suppression(pred, thred, 0.45, classes=None, agnostic=True)[0]
        pred = self.process(pred)
        return pred

    def process(self, pre):
        pre = sort_plate(pre)
        final = []
        for l in pre:
            for id_1 in range(len(l)):
                temp = [l[id_1]]
                for id_2 in range(id_1, len(l)):
                    if get_iou(l[id_1], l[id_2]) > 0.6:
                        temp.append(l[id_2])

                if id_1 == 2:
                    chara = [get_ele_5(x) >= 10 for x in temp]
                    if sum(chara) > 1:
                        temp = [x for x in temp if get_ele_5(x) >= 10]
                        area = [get_area(x) for x in temp]
                        if sum([max(area) == x for x in area]) == 1:
                            temp = sorted(temp, key=get_area)
                        else:
                            temp = sorted(temp, key=get_ele_4)
                    else:
                        temp = sorted(temp, key=get_ele_4)
                else:
                    temp = sorted(temp, key=get_ele_4)
                final.append(temp[0])
        return convert(final)