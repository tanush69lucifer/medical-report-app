from .xray_model import XRayModel
from .ct_mri_model import CTMRIModel
from .ultrasound_model import UltrasoundModel
from .spect_pet_model import SpectPETModel

class ModelManager:
    def __init__(self):
        # Initialize available models
        self.models = {
            "xray": XRayModel(),
            "ct_mri": CTMRIModel(),
            "ultrasound": UltrasoundModel(),
            "spect_pet": SpectPETModel()
        }
        self.active_model = None

    def load_model(self, model_name):
        if model_name in self.models:
            self.active_model = self.models[model_name]
            return f"{model_name} model loaded."
        else:
            raise ValueError(f"Model '{model_name}' not found!")

    def predict(self, data):
        if not self.active_model:
            raise RuntimeError("No model loaded. Call load_model() first.")
        return self.active_model.predict(data)
