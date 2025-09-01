import os
from PIL import Image
import pdfplumber
from docx import Document

def load_text_from_file(path_or_file):
    if hasattr(path_or_file, 'read'):
        data = path_or_file.read()
        if isinstance(data, bytes):
            import tempfile
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(data)
            tmp.close()
            path = tmp.name
        else:
            return str(data)
    else:
        path = path_or_file
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif ext == '.pdf':
        text = ''
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''
        return text
    elif ext == '.docx':
        doc = Document(path)
        return '\n'.join([p.text for p in doc.paragraphs])
    else:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f'[unavailable: {e}]'
