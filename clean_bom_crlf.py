#!/usr/bin/env python3
"""Always run this after editing QCMD to strip BOM and CRLF."""
import sys

path = r'c:\Users\User\OneDrive\Documents\os400\os400_utilities\QCMD'
with open(path, 'rb') as f:
    data = f.read()
if data.startswith(b'\xef\xbb\xbf'):
    data = data[3:]
if b'\r\n' in data:
    data = data.replace(b'\r\n', b'\n')
with open(path, 'wb') as f:
    f.write(data)
print(f"Clean: BOM={data[:3]==b'\\xef\\xbb\\xbf'}, CRLF={b'\\r\\n' in data}")
