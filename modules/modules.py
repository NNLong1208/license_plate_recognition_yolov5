import cv2

def get_iou(bb1, bb2):
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[2], bb2[2])
    x_right = min(bb1[1], bb2[1])
    y_bottom = min(bb1[3], bb2[3])
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    bb1_area = (bb1[1] - bb1[0]) * (bb1[3] - bb1[2])
    bb2_area = (bb2[1] - bb2[0]) * (bb2[3] - bb2[2])

    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou

def get_ele_0(l):
    return l[0]

def get_ele_4(l):
    return l[4]

def get_ele_5(l):
    return l[5]

def get_area(ele):
    return (ele[2] - ele[0]) * (ele[3] - ele[1])

def sort_plate(pre):
    plate = [[],[]]
    for i in pre:
        if i[1] < 220:
            plate[0].append(i)
        else:
            plate[1].append(i)

    plate[0] = sorted(plate[0], key=get_ele_0)
    plate[1] = sorted(plate[1], key=get_ele_0)
    return plate

def convert(final, thred= 0.7):
    for id, ele in enumerate(final):
        if id != 2:
            if ele[5] in [18, 21, 29]:
                ele[5] = 1
            if ele[5] == 31:
                ele[5] = 2
            if ele[5] == 14:
                ele[5] = 3
            if ele[5] == 11:
                ele[5] = 8
            if ele[5] == 16:
                ele[5] = 6
            if ele[5] == 25:
                ele[5] == 9
    if len(final) > 9:
        final = [x for x in final if x[4] > thred]
    return final

def crop_image(points, img):
    img = cv2.resize(img, (640, 480))
    imgs_crop = []
    for point in points:
        image = img[int(point[1]):int(point[3]), int(point[0]):int(point[2])].copy()
        imgs_crop.append(image)
    return imgs_crop