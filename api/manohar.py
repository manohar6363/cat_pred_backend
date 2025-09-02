import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from typing import List, Dict

# Load ResNet50 model (pretrained on ImageNet)
model = ResNet50(weights="imagenet")

def preprocess_image(img_path: str) -> np.ndarray:
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def predict_breed(img_path: str) -> List[Dict[str, float]]:
    processed_img = preprocess_image(img_path)
    preds = model.predict(processed_img)
    decoded = decode_predictions(preds, top=3)[0]

    results: List[Dict[str, float]] = []
    for _, label, confidence in decoded:
        results.append({
            "breed": label,
            "confidence": round(float(confidence), 4)
        })
    return results