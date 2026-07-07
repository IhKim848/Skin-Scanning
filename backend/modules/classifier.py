import torch
import torchvision.models as models
import torchvision.transforms as transforms
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import numpy as np
import os
from PIL import Image

class SkinDiseaseClassifier:
    def __init__(self):
        self.model = models.mobilenet_v2(pretrained=False)
        
        num_classes = 20
        self.model.classifier[1] = torch.nn.Linear(self.model.last_channel, num_classes)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'trained_skin_model.pth')

        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()

    def predict_and_explain(self, image_pil):
        input_tensor = self.preprocess(image_pil).unsqueeze(0)
        
        with torch.no_grad():
            output = self.model(input_tensor)
            pred_idx = torch.argmax(output, dim=1).item()
        
        targets = [ClassifierOutputTarget(pred_idx)]
        grayscale_cam = self.cam(input_tensor=input_tensor, targets=targets)[0, :]
        
        rgb_img = np.array(image_pil.resize((224, 224))) / 255.0
        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        
        return pred_idx, cam_image


if __name__ == "__main__":
    classifier = SkinDiseaseClassifier()
    print("AI 파이프라인 로드 완료!")