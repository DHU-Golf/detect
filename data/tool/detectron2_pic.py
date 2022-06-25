import cv2
import torch
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer


def detect_pic(path_p):
    im = cv2.imread(path_p)
    cfg = get_cfg()
    # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml")
    has_gpu = torch.cuda.is_available()
    if not has_gpu:
        cfg.MODEL.DEVICE = 'cpu'
    predictor = DefaultPredictor(cfg)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]))
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite(path_p, out.get_image()[:, :, ::-1])


if __name__ == '__main__':
    import project_config as cf

    detect_pic(f'{cf.PROJECT_ROOT}/gui/a.png')
