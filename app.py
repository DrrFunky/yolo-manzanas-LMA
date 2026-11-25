from pathlib import Path

import gradio as gr
from PIL import Image
from ultralytics import YOLO

PESOS = Path("weights/best.pt")

if not PESOS.exists():
    raise FileNotFoundError(
        "Falta weights/best.pt. Copia aquí el modelo elegido "
        "(modelo_elegido.pt / best.pt desde resultados_manzanas.zip de Google Drive)."
    )

modelo = YOLO(str(PESOS))


def detectar(img):
    resultado = modelo(img)[0]
    imagen = resultado.plot()[:, :, ::-1]
    return Image.fromarray(imagen)


rutas = sorted(Path("demo").glob("*.png"))
ejemplos = [[str(ruta)] for ruta in rutas[:3]] or None

gr.Interface(
    fn=detectar,
    inputs=gr.Image(type="pil", label="Sube una imagen de manzanas"),
    outputs=gr.Image(type="pil", label="Detección"),
    title="Detector de calidad de manzanas",
    description="Clasifica manzanas como apple o damaged_apple con YOLO26.",
    examples=ejemplos,
).launch()
