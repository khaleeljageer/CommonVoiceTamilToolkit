import re
import os
from pathlib import Path

def is_invalid_sentence(m_text: str) -> bool:
    l_text = m_text.strip()

    if not l_text:
        return True

    # Single token (word, number, punctuation, etc.)
    if len(l_text.split()) == 1:
        return True

    # Only special characters/punctuation
    if re.fullmatch(r"[^\w\s]+", l_text, flags=re.UNICODE):
        return True

    return False


# Input directory containing .txt files
input_dir = "/run/media/asuran/Khaleel_SSD/CommonVoice/thamizh_mann/data"

output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

txt_files = list(Path(input_dir).glob("*.txt"))

print(f"Found {len(txt_files)} txt files")

for input_file in txt_files:

    file_name = input_file.stem
    output_file = os.path.join(
        output_dir,
        f"{file_name}_parsed.txt"
    )

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        text = re.sub(r'\s+', ' ', text).strip()

        sentences = re.split(r'(?<=[.!?])\s+', text)

        filtered_sentences = []

        for sentence in sentences:

            # Keep only:
            # Tamil Unicode chars + space + .,!? punctuation : Refer CommonVoice Mozilla Tamil dataset for allowed chars
            sentence = re.sub(
                r'[^ \u0B80-\u0BFF\.\,\!\?]',
                '',
                sentence
            )

            # Remove extra spaces
            sentence = re.sub(r'\s+', ' ', sentence).strip()

            # Skip empty
            if not sentence:
                continue

            # Remove sentences containing English letters : Refer CommonVoice Mozilla Tamil dataset for allowed chars
            if re.search(r'[A-Za-z]', sentence):
                continue

            # Word count filter
            word_count = len(sentence.split())

            if word_count >= 15:
                continue

            filtered_sentences.append(sentence)

        # Write output
        with open(output_file, "w", encoding="utf-8") as f:
            for line in filtered_sentences:
                sentence = line.strip()
                if is_invalid_sentence(sentence):
                    print(
                        f"Skipping : '{sentence}'"
                    )
                    continue
                f.write(sentence + "\n")

        print(f"Processed: {input_file.name}")
        print(f"Saved: {output_file}")
        print(f"Valid sentences: {len(filtered_sentences)}")
        print("-" * 50)

    except Exception as e:
        print(f"Error processing {input_file.name}: {e}")

print("Processing completed.")