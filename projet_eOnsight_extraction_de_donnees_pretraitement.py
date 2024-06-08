import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import json
import os

# Importation de l'image 
image_path = "Genova.png"
image = Image.open(image_path)

# Augmenter la résolution de l'image
base_width = 3000
w_percent = (base_width / float(image.size[0]))
h_size = int((float(image.size[1]) * float(w_percent)))
image = image.resize((base_width, h_size), Image.LANCZOS)

# Prétraitement de l'image
# Convertir en niveaux de gris
image = image.convert('L')

# Augmenter le contraste
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2)

# Appliquer un filtre de netteté
image = image.filter(ImageFilter.SHARPEN)

# Sauvegarder l'image prétraitée pour vérifier visuellement
preprocessed_image_path = "preprocessed_image.png"
image.save(preprocessed_image_path)

# Utilisation de easyocr pour récupérer le texte
reader = easyocr.Reader(["fr"], gpu=False)
results = reader.readtext(preprocessed_image_path)

# On extrait les informations importantes et on les prépare pour JSON
donnee_extrait = []

# On impose un seuil de confiance minimal
confidence_threshold = 0.5

for result in results:
    bbox, text, confidence = result
    if confidence > confidence_threshold:
        data = {
            'text': text,
            'left': int(bbox[0][0]),  # int pour mettre au bon format JSON
            'top': int(bbox[0][1]),
            'width': int(bbox[1][0] - bbox[0][0]),
            'height': int(bbox[2][1] - bbox[0][1]),
            'conf': float(confidence)
        }
        print(f"Text found: {data['text']} with a confidence {data['conf']}")
        donnee_extrait.append(data)

# Conversion en JSON
output_dir = 'output'
output_path = os.path.join(output_dir, 'ocr_results.json')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(output_path, "w") as json_file:
    json.dump(donnee_extrait, json_file, indent=4)

print(f"Résultat OCR sauvegardé dans {output_path}")
