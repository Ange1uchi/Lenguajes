import csv
from pathlib import Path

# Rutas de entrada y salida
input_path = Path("vcounters.csv")
output_path = Path("lcov.info")

if not input_path.exists():
    print(f" No se encontró {input_path}")
    exit(1)

with open(input_path, newline='') as f, open(output_path, "w") as out:
    reader = csv.reader(f)
    header = next(reader, None)  # saltar cabecera
    current_file = None

    for row in reader:
        if len(row) < 3:
            continue
        file_path, line, count = row[0].strip(), row[1].strip(), row[2].strip()

        # Si no es un número, saltar (evita errores tipo 'line,count')
        if not line.isdigit() or not count.isdigit():
            continue

        # Cambiar de archivo cuando sea necesario
        if file_path != current_file:
            if current_file:
                out.write("end_of_record\n")
            out.write(f"SF:{file_path}\n")
            current_file = file_path

        out.write(f"DA:{line},{count}\n")

    if current_file:
        out.write("end_of_record\n")

print(f"✅ Archivo LCOV generado correctamente en {output_path}")
