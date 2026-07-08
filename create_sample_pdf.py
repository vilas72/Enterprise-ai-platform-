from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

path = Path('sample.pdf')
c = canvas.Canvas(str(path), pagesize=letter)
c.setFont('Helvetica', 12)
y = 750
for line in [
    'Redis is an in-memory cache database.',
    'FastAPI is a Python web framework.',
    'Magento is Adobe Commerce.',
]:
    c.drawString(72, y, line)
    y -= 16
c.save()
print(path.resolve())
