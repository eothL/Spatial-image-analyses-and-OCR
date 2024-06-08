# Importation des librairies 
import easyocr
import os
import json

# Importation de l'image 
image_path = "Genova.png"

reader = easyocr.Reader(["fr"], gpu= False) # on choisit les langues qu'il doit reconnaître 
results = reader.readtext(image_path)

#print(results) #debug

# On extrait les informations importantes et on les prépare pour JSON
donnee_extrait = []

# on impose un seuil de confiance minimal
confidence_threshold = 0.5

for result in results :
    bbox, text, confidence = result
    if confidence > confidence_threshold :
        data = {
            'text': text,
            'left': int(bbox[0][0]), #int pour mettre au bon format JSON
            'top': int(bbox[0][1]),
            'width':  int(bbox[1][0] - bbox[0][0]),
            'height': int(bbox[2][1] - bbox[0][1]),
            'conf': float(confidence)
        }
        #print(f"Text found: {data['text']} with a confidence {data['conf']}") #debug
        donnee_extrait.append(data)

#print(donnee_extrait) #debug

# Conversion en JSON
output_dir ='output'
output_path = os.path.join(output_dir,'ocr_results.json')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(output_path,"w") as json_file:
    json.dump(donnee_extrait, json_file, indent = 4)

print(f"Résultat OCR sauvegardé dans {output_path}")
