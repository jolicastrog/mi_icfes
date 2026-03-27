from PIL import Image, ImageDraw, ImageFont
import os
 
def crear_icono(size: int, output_path: str):
    """Crea un icono simple azul con texto MI ICFES."""
    img = Image.new("RGBA", (size, size), color=(0, 48, 135, 255))  # Azul #003087
    draw = ImageDraw.Draw(img)
 
    # Circulo blanco de fondo
    margen = size // 8
    draw.ellipse([margen, margen, size-margen, size-margen],
                  fill=(255, 255, 255, 255))
 
    # Texto "MI" arriba
    font_size_mi = size // 4
    font_size_icfes = size // 6
    try:
        font_mi    = ImageFont.truetype("arial.ttf", font_size_mi)
        font_icfes = ImageFont.truetype("arial.ttf", font_size_icfes)
    except:
        font_mi    = ImageFont.load_default()
        font_icfes = ImageFont.load_default()
 
    # Centrar texto "MI"
    bbox_mi = draw.textbbox((0,0), "MI", font=font_mi)
    w_mi = bbox_mi[2] - bbox_mi[0]
    draw.text(((size-w_mi)//2, size//3 - font_size_mi//2), "MI",
               fill=(0, 48, 135, 255), font=font_mi)
 
    # Centrar texto "ICFES"
    bbox_ic = draw.textbbox((0,0), "ICFES", font=font_icfes)
    w_ic = bbox_ic[2] - bbox_ic[0]
    draw.text(((size-w_ic)//2, size*3//5), "ICFES",
               fill=(0, 48, 135, 255), font=font_icfes)
 
    img.save(output_path, "PNG")
    print(f"Icono creado: {output_path} ({size}x{size} px)")
 
os.makedirs("static", exist_ok=True)
crear_icono(192, "static/icon-192.png")
crear_icono(512, "static/icon-512.png")
print("Iconos listos en static/")
