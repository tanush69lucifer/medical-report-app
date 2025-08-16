import tensorflow as tf
from . import utils_preprocess

class UltrasoundModel:
    def __init__(self, model_path="models/ultrasound_model.h5"):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, image_path: str):
        img = utils_preprocess.load_and_preprocess(image_path, target_size=(128, 128))
        preds = self.model.predict(img)
        return preds
