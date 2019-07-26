import sys
from bom_open import bom_open

with bom_open('-') as f:
    print(f.encoding, file=sys.stderr)
    print(f.read())
