import csv
import PyPDF2
import re
import argparse

def extract_paragraphs_with_word(input_file, output_file, word='shall'):
    pdf_text = ""
    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()

    section_pattern = r'(\d+(?:\.\d+)+)\s+([^\n]+)'  # Pattern to capture section info and description

    sections = re.split(section_pattern, pdf_text)[1:]  # Skip the first element (empty)

    rows = []
    for i in range(0, len(sections), 3):
        section_info = sections[i]
        section_desc = sections[i + 1] if i + 1 < len(sections) else ""

        sentences = [line for line in sections[i + 2].split('\n') if word in line.lower()]
        for sentence in sentences:
            rows.append([section_info, section_desc, sentence.strip()])

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Section Info', 'Nearest Subheading', 'Sentence with "{}"'.format(word)])
        for row in rows:
            csvwriter.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract sentences containing a specific word from a PDF file and save them in a CSV file.')
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('output_csv', nargs='?', help='Path to the output CSV file. If not specified, the name of the PDF file with .csv extension will be used.')

    args = parser.parse_args()
    input_pdf_path = args.input_pdf
    output_csv_path = args.output_csv or (input_pdf_path[:-4] + '.csv')

    extract_paragraphs_with_word(input_pdf_path, output_csv_path)

