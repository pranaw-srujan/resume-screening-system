from modules.extract_text import extract_text

# Replace this with the actual filename you uploaded earlier
filepath = "static/uploads/sample_resume_3_sneha.docx"

text = extract_text(filepath)

print("----- EXTRACTED TEXT START -----")
print(text)
print("----- EXTRACTED TEXT END -----")
print(f"\nTotal characters extracted: {len(text)}")