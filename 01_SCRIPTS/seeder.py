import argparse
import csv
import random
from datetime import datetime, timedelta
from tqdm import tqdm

PRODUCTO_BASE = ["camiseta", "pantalon", "zapato", "chaqueta", "bota", "gorro", "remera", "short"]
PRODUCTO_EXTRA = ["algodon", "deportivo", "premium", "basico", "invierno", "verano", "urbano", "clasico"]

CATEGORIA_BASE = ["ropa", "calzado", "accesorio", "deporte", "outdoor", "casual"]
CATEGORIA_EXTRA = ["hombre", "mujer", "infantil", "unisex", "premium", "basico"]

REGIONES = ["Sur", "Este", "Oeste", "Norte"]

INICIO = datetime(2025, 1, 1)
FIN = datetime(2026, 12, 31, 23, 59, 59)

N = 10000000

def nombre_aleatorio(base, extra):
    return f"{random.choice(base)}-{random.choice(extra)}"

def fecha_uniforme():
    delta = FIN - INICIO
    segundos = random.uniform(0, delta.total_seconds())
    return (INICIO + timedelta(seconds=segundos)).strftime("%Y-%m-%d")

def generar_ventas_stream(n):
    header = ["fecha", "producto", "categoria", "cantidad", "precio_unitario", "región"]
    yield header
    batch_size = 10000
    batch = []
    for _ in range(n):
        fila = [
            fecha_uniforme(),
            nombre_aleatorio(PRODUCTO_BASE, PRODUCTO_EXTRA),
            nombre_aleatorio(CATEGORIA_BASE, CATEGORIA_EXTRA),
            random.randint(1, 20),
            random.randint(10, 100),
            random.choice(REGIONES),
        ]
        batch.append(fila)
        if len(batch) == batch_size:
            for f in sorted(batch, key=lambda f: f[0]):
                yield f
            batch = []
    if batch:
        for f in sorted(batch, key=lambda f: f[0]):
            yield f

def main():
    parser = argparse.ArgumentParser(description="Genera ventas.csv con N registros aleatorios.")
    parser.add_argument("-n", "--num", type=int, default=N, help=f"Cantidad de ventas a generar (por defecto: {N})")
    args = parser.parse_args()

    if args.num < 1:
        parser.error("n debe ser al menos 1")

    import os

    # Crear el directorio si no existe
    output_dir = "../00_DATA"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "ventas.csv"), mode="w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)
        ventas_gen = generar_ventas_stream(args.num)
        writer.writerow(next(ventas_gen))  # header
        for fila in tqdm(ventas_gen, total=args.num, desc="Generando ventas"):
            writer.writerow(fila)

     
    print(f"ventas.csv creado con {args.num} registros.")

if __name__ == "__main__":
    main()
