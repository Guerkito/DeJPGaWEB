import os
import sys
import re
import unicodedata
from PIL import Image

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

def convertir_a_webp(ruta_imagen, directorio_salida):
    try:
        nombre_original = os.path.basename(ruta_imagen)
        nombre_sin_ext = os.path.splitext(nombre_original)[0]
        nuevo_nombre = limpiar_nombre(nombre_sin_ext)
        
        if not nuevo_nombre:
            nuevo_nombre = "imagen"

        img = Image.open(ruta_imagen)
        # Convertir a modo compatible con WebP si es necesario
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA')
            
        ruta_salida = os.path.join(directorio_salida, f"{nuevo_nombre}.webp")
        
        # Evitar sobreescribir archivos existentes
        contador = 1
        while os.path.exists(ruta_salida):
            ruta_salida = os.path.join(directorio_salida, f"{nuevo_nombre}-{contador}.webp")
            contador += 1
            
        # Guardar como WebP optimizado
        img.save(ruta_salida, 'webp', quality=80, method=6)
        print(f"  [Éxito] {nombre_original} -> {os.path.basename(ruta_salida)}")
        return ruta_salida
    except Exception as e:
        print(f"  [Error] al convertir {ruta_imagen}: {e}")
        return None

def main():
    directorio_entrada = sys.argv[1] if len(sys.argv) > 1 else '.'
    directorio_salida = os.path.join(directorio_entrada, 'webp_optimizados')
    
    formatos_soportados = ('.jpg', '.jpeg', '.png')
    
    try:
        imagenes = [f for f in os.listdir(directorio_entrada) if f.lower().endswith(formatos_soportados) and os.path.isfile(os.path.join(directorio_entrada, f))]
    except Exception as e:
        print(f"[!] Error al leer el directorio {directorio_entrada}: {e}")
        sys.exit(1)
    
    if not imagenes:
        print(f"No se encontraron imágenes JPG o PNG en el directorio: {os.path.abspath(directorio_entrada)}")
        sys.exit(0)
        
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    print(f"Se encontraron {len(imagenes)} imágenes. Iniciando procesamiento...\n")
    
    for archivo in imagenes:
        ruta_completa = os.path.join(directorio_entrada, archivo)
        convertir_a_webp(ruta_completa, directorio_salida)
        
    print(f"\n¡Proceso terminado! Tus imágenes están en la carpeta: {os.path.abspath(directorio_salida)}")

if __name__ == '__main__':
    main()
