from text_to_latex import create_document, append_text
import os

from text_to_latex import append_display

# find path of test_documents directory
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_documents', 'test1')

# create test document
doc = create_document("A Test Document", path)

# append string to test document
append_text(doc, "This is an equation: $1+2 = 3 \in \mathbb{R}$")

# append display math to test document
append_display(doc, "This is an equation: $$1+2 = 3 \in \mathbb{R}$$")
