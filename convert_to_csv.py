from pathlib import Path
import csv
import os

# Input txt directory
input_dir = "output"

# Output csv directory
csv_output_dir = "csv_output"

os.makedirs(csv_output_dir, exist_ok=True)

txt_files = list(Path(input_dir).glob("*.txt"))

print(f"Found {len(txt_files)} files")

for index, file_path in enumerate(txt_files, start=1):

    try:
        print(f"[{index}/{len(txt_files)}] Processing: {file_path.name}")

        csv_file = os.path.join(
            csv_output_dir,
            f"{file_path.stem}.csv"
        )

        with open(file_path, "r", encoding="utf-8") as txt_f, \
             open(csv_file, "w", encoding="utf-8", newline="") as csv_f:

            writer = csv.writer(csv_f)

            # Header
            writer.writerow(["Line Number", "Sentence"])

            for line_num, line in enumerate(txt_f, start=1):
                writer.writerow([line_num, line.strip()])

        print(f"Saved: {csv_file}")

    except Exception as e:
        print(f"Error: {file_path.name} -> {e}")

print("Completed.")