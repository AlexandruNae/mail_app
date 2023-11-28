import os
import PyPDF2
from src.utils import title_to_alias

import fitz  # PyMuPDF

# Pentru Enigma otiliei
diacritic_mapping_enigma_otiliei = {
    '=': 'ș',
    '`': 'â',
    '[': 'ă',
    '\\': 'ț',
    ']': 'î',
    '}': 'Î',
    '+': 'Ș',
    '|': 'Ț',
}

# Pentru Enigma otiliei
diacritic_mapping_iona = {
    'ᗰ': 'ș',
    '`': 'â',
    'ူ': 'ă',
    'ᘰ': 'ț',
    ']': 'î',
    '}': 'Î',
    'ᗠ': 'Ș',
}

diacritic_mapping_patul_proust = {
    'Ń': 'ț',
    'ł': 'Ț',
}

diacritic_mapping_patul_ion = {
    's,': 'ș',
    't,': 'ț',
}

def replace_diacritics(input_text, mapping):
    for wrong_char, correct_char in mapping.items():
        input_text = input_text.replace(wrong_char, correct_char)
    return input_text

def title_to_alias(input_text):
    title_underscores = input_text.lower().replace("-", "_").replace(" ", "_")
    parts = title_underscores.split('_', 5)
    # If we have less than 6 parts, it means there weren't 5 underscores, return the original string
    if len(parts) < 6:
        return title_underscores
    # Join the parts back together with underscores
    return '_'.join(parts[:5])

def normalize_page_content(page_content, max_words_per_line=15):
    # page_content = replace_diacritics(page_content, diacritic_mapping_patul_ion)
    words = page_content.split()
    normalized_lines = []
    current_line_words = []

    for word in words:
        # Check if the word is a dialogue dash, and if so, start a new line
        if word.startswith("—"):
            if current_line_words:  # Add the current line if it has words
                normalized_lines.append(' '.join(current_line_words))
                current_line_words = [word]
            else:  # If the current line is empty, just add the dialogue dash
                current_line_words.append(word)
        elif len(current_line_words) < max_words_per_line:
            current_line_words.append(word)
        else:
            normalized_lines.append(' '.join(current_line_words))
            current_line_words = [word]

    if current_line_words:  # Add the last line if it has words
        normalized_lines.append(' '.join(current_line_words))

    return '\n'.join(normalized_lines)



def split_pdf_into_txt(pdf_path, book_alias, char_limit=8000):
    # Create the main folder 'lectures' if not exist
    if not os.path.exists('../lectures'):
        os.makedirs('../lectures')

    # Create the book folder
    book_folder = f'../lectures/{book_alias}'
    if not os.path.exists(book_folder):
        os.makedirs(book_folder)

    # Open PDF
    with fitz.open(pdf_path) as pdf:
        char_buffer = ""
        file_count = 1

        for page in pdf:
            # Get content of each page
            page_content = page.get_text()

            # Normalize the content of the page
            page_content = normalize_page_content(page_content)

            char_buffer += page_content

            # Check if the buffer exceeds the character limit and split accordingly
            while len(char_buffer) >= char_limit:
                split_index = char_buffer.rfind('\n', 0, char_limit)
                if split_index == -1:
                    split_index = char_limit

                # Write the content to a txt file
                with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(char_buffer[:split_index])

                # Update char_buffer and file_count
                char_buffer = char_buffer[split_index:]
                file_count += 1

        # Handle any remaining text
        if char_buffer.strip():
            with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                txt_file.write(char_buffer)


def split_txt_file(file_path, dest_folder, lines_per_file):
    # Check if the source file exists
    if not os.path.exists(file_path):
        print("The source file does not exist.")
        return

    # Check if the destination folder exists, if not, create it
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Open the source file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Splitting the file
    for i in range(0, len(lines), lines_per_file):
        part_no = i // lines_per_file + 1
        part_name = os.path.join(dest_folder, f'part_{part_no}.txt')

        with open(part_name, 'w') as part_file:
            part_file.writelines(lines[i:i + lines_per_file])

    print(f"File '{file_path}' has been split into {part_no} parts in '{dest_folder}'.")


# Example usage

if __name__ == "__main__":
    # Assume the current working directory is 'mail_app_scripts'
    # Construct the relative path to the PDF within the project directory
    pdf_relative_path = os.path.join('book_pdf', 'Ultima noapte de dragoste, întâia noapte de război.pdf')

    # Get the absolute path of the current script (which is in 'mail_app_scripts')
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the project directory with the relative path to get the full path to the PDF
    pdf_path = os.path.join(project_directory, pdf_relative_path)


    book_title = 'Ultima noapte de dragoste, întâia noapte de război'  # Replace with your book title
    book_alias = title_to_alias(book_title)

    split_pdf_into_txt(pdf_path, book_alias)
