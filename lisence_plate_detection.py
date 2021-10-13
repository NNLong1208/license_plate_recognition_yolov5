import torch.backends.cudnn as cudnn
from models.experimental import attempt_load
from utils.general import non_max_suppression
from modules.pre_process import pre_process_yolo
from utils.torch_utils import select_device
from modules.modules import *

class lisence_plate_detection():
    def __init__(self, path_model = './models/lisence_plate_detection.pt'):
        try:
            self.__device = select_device('0')
            self.__model  = attempt_load(path_model, map_location=self.__device)
            self.__model.half()
            cudnn.benchmark = True
        except:
            print('Load model fail')

    def detect(self, img, crop = True, thred = 0.75):
        img_ = cv2.resize(img, (640, 480))
        img_ = pre_process_yolo(img_, self.__device, True)
        pred = self.__model(img_, augment=False)[0]
        pred = non_max_suppression(pred, thred, 0.45, classes=None, agnostic=True)[0]
        if crop:
            return pred, crop_image(pred, img)
        else:
            return pred