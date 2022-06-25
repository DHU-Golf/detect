import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

import project_config as cf
from data.golfdb.eval import ToTensor, Normalize
from data.golfdb.model import EventDetector
import project_config as cf

# from memory_profiler import profile

event_names = {
    0: 'Address',
    1: 'Toe-up',
    2: 'Mid-backswing (arm parallel)',
    3: 'Top',
    4: 'Mid-downswing (arm parallel)',
    5: 'Impact',
    6: 'Mid-follow-through (shaft parallel)',
    7: 'Finish'
}


class SampleVideo(Dataset):
    def __init__(self, path, input_size=160, transform=None):
        self.path = path
        self.input_size = input_size
        self.transform = transform

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        cap = cv2.VideoCapture(self.path)
        frame_size = [cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)]
        ratio = self.input_size / max(frame_size)
        new_size = tuple([int(x * ratio) for x in frame_size])
        delta_w = self.input_size - new_size[1]
        delta_h = self.input_size - new_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        # preprocess and return frames
        images = []
        for pos in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            _, img = cap.read()
            try:
                resized = cv2.resize(img, (new_size[1], new_size[0]))
            except:
                continue  # skip the error frame and continue
            b_img = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                       value=[0.406 * 255, 0.456 * 255, 0.485 * 255])  # ImageNet means (BGR)

            b_img_rgb = cv2.cvtColor(b_img, cv2.COLOR_BGR2RGB)
            images.append(b_img_rgb)
        cap.release()
        labels = np.zeros(len(images))  # only for compatibility with transforms
        sample = {'images': np.asarray(images), 'labels': np.asarray(labels)}
        if self.transform:
            sample = self.transform(sample)
        return sample


# @profile
def events(path, seq_length=64):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-p', '--path', help='Path to video that you want to test', default='test_video.mp4')
    # parser.add_argument('-s', '--seq-length', type=int, help='Number of frames to use per forward pass', default=64)
    # args = parser.parse_args()
    seq_length = seq_length

    # print('Preparing video: {}'.format(path))

    ds = SampleVideo(path, transform=transforms.Compose([ToTensor(),
                                                         Normalize([0.485, 0.456, 0.406],
                                                                   [0.229, 0.224, 0.225])]))

    dl = DataLoader(ds, batch_size=1, shuffle=False, drop_last=False)

    model = EventDetector(pretrain=True,
                          width_mult=1.,
                          lstm_layers=1,
                          lstm_hidden=256,
                          bidirectional=True,
                          dropout=False)

    # use cpu, my GPU memory is not enough

    try:
        if cf.golfdb_ver == "CBAM":
            path_m = cf.PROJECT_ROOT + "data/golfdb/models/split_4_flip+affine_7700.pth.tar"
        else:
            # do not forget to reset dataloader 和 model
            path_m = cf.PROJECT_ROOT + "data/golfdb/models/swingnet_1800.pth.tar"
        save_dict = torch.load(path_m)
    except:
        print(
            "Model weights not found. Download model weights and place in 'models' folder. See README for instructions")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # print('Using device:', device)
    model.load_state_dict(save_dict['model_state_dict'])
    # model.to(device)
    # model.to(torch.device('cpu'))   # use cpu, my GPU memory is not enough
    model.eval()
    # print("Loaded model weights")

    # print('Testing...')
    for sample in dl:
        images = sample['images']
        # full samples do not fit into GPU memory so evaluate sample in 'seq_length' batches
        batch = 0
        while batch * seq_length < images.shape[1]:
            if (batch + 1) * seq_length > images.shape[1]:
                image_batch = images[:, batch * seq_length:, :, :, :]
            else:
                image_batch = images[:, batch * seq_length:(batch + 1) * seq_length, :, :, :]
            logits = model(image_batch.cpu())
            # logits = model(image_batch.cuda())
            if batch == 0:
                probs = F.softmax(logits.data, dim=1).cpu().numpy()
            else:
                probs = np.append(probs, F.softmax(logits.data, dim=1).cpu().numpy(), 0)
            batch += 1

    # print(probs.shape)
    events = np.argmax(probs, axis=0)[:-1]
    # print('Predicted event frames: {}'.format(events))
    # cap = cv2.VideoCapture(path)
    # # cap = cv2.VideoCapture(args.path)
    #
    # confidence = []
    # for i, e in enumerate(events):
    #     confidence.append(probs[e, i])
    # # print('Condifence: {}'.format([np.round(c, 3) for c in confidence]))
    #
    # for i, e in enumerate(events):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, e)
    #     _, img = cap.read()
    #     cv2.putText(img, '{:.3f}'.format(confidence[i]), (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255))
    #     cv2.imshow(event_names[i], img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    # print(min(events),max(events))
    return events


if __name__ == "__main__":
    teacher = f"{cf.PROJECT_ROOT}data/video_raw/5.mp4"
    fin = events(teacher)
    print(fin)
