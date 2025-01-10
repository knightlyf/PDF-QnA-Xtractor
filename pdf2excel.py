import fitz
import pandas as pd
import re
import os

folder_path = "pdfs/"
output_path = "excel/"
question_pattern = re.compile(r"^\d+[\.\)]\s+.*")

os.makedirs(output_path, exist_ok=True)


def extract_questions_answers(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    questions = []
    answers = []

    for page in doc:
        text = page.get_text("text")
        lines = text.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if question_pattern.match(line):
                questions.append(line)
                if i + 1 < len(lines):
                    answer = lines[i + 1].strip()
                    answers.append(answer)
                    i += 1
                else:
                    answers.append("")
            i += 1

    df = pd.DataFrame({"Question": questions, "Answer": answers})
    df.to_excel(output_path, index=False)


for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        excel_filename = filename.replace(".pdf", ".xlsx")
        excel_path = os.path.join(output_path, excel_filename)

        extract_questions_answers(pdf_path, excel_path)
        print(f"Extracted Q&A saved to {excel_path}")
