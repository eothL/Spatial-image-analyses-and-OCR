import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import json
import os

# Importation de l'image 
image_path = r"Extrait_IQOA_data.png"
image = Image.open(image_path)

# Augmentation de la résolution de l'image
base_width = 3000
w_percent = (base_width / float(image.size[0]))
h_size = int((float(image.size[1]) * float(w_percent)))
image = image.resize((base_width, h_size), Image.LANCZOS)

# Prétraitement de l'image
# Convertir en niveaux de gris
image = image.convert('L')

# Augmentation du contraste
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2)

# Appliquer un filtre de netteté
image = image.filter(ImageFilter.SHARPEN)

# Appliquer un filtre de seuil
image = image.point(lambda x: 0 if x < 150 else 255)

# Sauvegarder l'image prétraitée pour vérifier visuellement
preprocessed_image_path = "preprocessed_image.png"
image.save(preprocessed_image_path)

# Utilisation de easyocr pour récupérer le texte
reader = easyocr.Reader(["fr"], gpu=False)
results = reader.readtext(preprocessed_image_path)

# Affichage des résultats pour débogage
for result in results:
    bbox, text, confidence = result
    print(f"Text found: {text} with confidence {confidence}")

# On extrait les informations importantes et on les prépare pour JSON
donnee_extrait = []

# On impose un seuil de confiance minimal
confidence_threshold = 0.5

# Analyser et structurer les données extraites
for result in results:
    bbox, text, confidence = result
    if confidence > confidence_threshold:
        data = {
            'text': text,
            'left': int(bbox[0][0]),
            'top': int(bbox[0][1]),
            'width': int(bbox[1][0] - bbox[0][0]),
            'height': int(bbox[2][1] - bbox[0][1]),
            'conf': float(confidence)
        }
        donnee_extrait.append(data)

# Convertir les données extraites en un format structuré de tableau
table_data = {
    "EQUIPEMENTS": [],
    "SUR OUVRAGE": [],
    "SUBDI": [],
    "CDOA": []
}

# Logique pour organiser les données dans les colonnes appropriées
# Cette partie peut être ajustée selon les résultats spécifiques obtenus de l'OCR

for item in donnee_extrait:
    if "EQUIPEMENTS" in item['text'] or "SUR OUVRAGE" in item['text']:
        table_data["EQUIPEMENTS"].append(item)
    elif "SUBDI" in item['text'] or "CDOA" in item['text']:
        table_data["SUR OUVRAGE"].append(item)
    else:
        # Vous pouvez ajouter plus de logique ici pour structurer les données du tableau
        table_data["EQUIPEMENTS"].append(item)

# Conversion en JSON
output_dir = 'output'
output_path = os.path.join(output_dir, 'table_results.json')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(output_path, "w") as json_file:
    json.dump(table_data, json_file, indent=4)

print(f"Résultat OCR sauvegardé dans {output_path}")
