import torch

def pre_process_yolo(img, device, half):
    img_ = img[..., ::-1].copy()
    img_ = torch.from_numpy(img_).to(device)
    img_ = img_.half().to('cuda') if half else img_.float()
    img_ /= 255.0
    img_ = img_.permute(2, 0, 1)
    img_ = img_.unsqueeze(0)
    return img_
