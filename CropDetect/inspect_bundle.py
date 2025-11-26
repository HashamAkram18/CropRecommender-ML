import os
import pickle
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropDetect.settings')
django.setup()

def inspect_bundle():
    model_path = os.path.join(settings.BASE_DIR, 'Recommender', 'migrations', 'ML', 'bundle.pkl')
    with open(model_path, 'rb') as f:
        bundle = pickle.load(f)
    
    print("Bundle Keys:", bundle.keys())
    if 'classes' in bundle:
        print("Classes:", bundle['classes'])
    
    if 'model_name' in bundle:
        print("Model Type:", type(bundle['model_name']))

if __name__ == "__main__":
    inspect_bundle()
