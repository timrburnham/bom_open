#import sys
from bom_open import bom_open

#with bom_open('test.txt', 'w', encoding='windows-1252') as f:
#    # f.write('Hello world')
#    f.write('Hello world \xab')
#
#with bom_open('test.txt', encoding='windows-1252') as f:
#    print(f.encoding)
#    print(f.read())

with bom_open(None, 'r+') as f:
    print(f.encoding)
    print(f.read())

# with bom_open(None, 'w', encoding='windows-1252') as f:
# #    print(f.buffer.peek())
#     print("Hello world \xab", file=f)
#     # print(f.read())

#print(sys.stdin.read())
#
#print(sys.stdin.buffer.peek())
