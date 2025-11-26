import os
import pickle
import sys
import django
from functools import lru_cache # Caching for faster loading 
import numpy as np

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropDetect.settings')
django.setup()

from django.conf import settings

@lru_cache(maxsize=1)
def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'Recommender', 'migrations', 'ML', 'bundle.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    assert model is not None and isinstance(model, dict) and 'model_name' in model and 'features_cols' in model and 'classes' in model    
    return model

# Mapping from training notebook
class_mapping = {
    'rice': 0, 'maize': 1, 'jute': 2, 'cotton': 3, 'coconut': 4, 
    'paddy': 5, 'ground nut': 6, 'kidney beans': 7, 'moth beans': 8, 
    'coco nut': 9, 'black gram': 10, 'banana': 11, 'grapes': 12, 
    'watermelon': 13, 'muskmelon': 14, 'apple': 15, 'orange': 16, 
    'papaya': 17, 'berry': 18, 'litchi': 19, 'mango': 20
}
# Reverse mapping: integer -> crop name
inv_class_mapping = {v: k for k, v in class_mapping.items()}

def predict_crop(features):
    model = load_model()
    features = list(map(float, features))
    X = np.array(features).reshape(1, -1)
    prediction_index = model['model_name'].predict(X)[0]
    
    # Return the crop name if index exists, else return the index
    return inv_class_mapping.get(prediction_index, prediction_index)    


if __name__ == "__main__":

    features = [100, 200, 300, 25, 50, 6.5, 100] 
    prediction = predict_crop(features)
    print(f"Prediction: {prediction}")