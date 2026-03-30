import os
import re
import unicodedata
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'static/webp_optimizados'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def limpiar_nombre(texto):
    texto = texto.strip().lower()
    # Eliminar acentos
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    # Reemplazar espacios y guiones bajos por guiones
    texto = texto.replace(' ', '-').replace('_', '-')
    # Eliminar cualquier carácter que no sea letra, número o guión
    texto = re.sub(r'[^a-z0-9\-]', '', texto)
    # Eliminar guiones múltiples
    texto = re.sub(r'-+', '-', texto)
    # Eliminar guiones al inicio o final
    texto = texto.strip('-')
    return texto

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No se enviaron archivos'}), 400
    
    files = request.files.getlist('files[]')
    resultados = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(file.stream)
                
                nombre_original = file.filename
                nombre_sin_ext = os.path.splitext(nombre_original)[0]
                nuevo_nombre = limpiar_nombre(nombre_sin_ext)
                if not nuevo_nombre:
                    nuevo_nombre = "imagen"
                
                # Convertir a modo compatible con WebP si es necesario
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGBA')
                    
                ruta_salida_base = os.path.join(UPLOAD_FOLDER, f"{nuevo_nombre}.webp")
                ruta_salida = ruta_salida_base
                
                # Evitar sobreescribir
                contador = 1
                while os.path.exists(ruta_salida):
                    ruta_salida = os.path.join(UPLOAD_FOLDER, f"{nuevo_nombre}-{contador}.webp")
                    contador += 1
                    
                # Guardar como WebP optimizado
                img.save(ruta_salida, 'webp', quality=80, method=6)
                
                nombre_archivo_final = os.path.basename(ruta_salida)
                resultados.append({
                    'original': nombre_original,
                    'nuevo': nombre_archivo_final,
                    'url': f'/download/{nombre_archivo_final}'
                })
            except Exception as e:
                print(f"Error procesando {file.filename}: {e}")
                
    return jsonify({'success': True, 'archivos': resultados})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" Dashboard iniciado: Abre http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
