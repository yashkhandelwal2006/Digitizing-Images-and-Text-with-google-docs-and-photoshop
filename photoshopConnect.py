
from photoshop import PhotoshopConnection
from os.path import dirname, basename
with PhotoshopConnection(password='grignard') as conn:
    filename="ObjectToBeSegemented/stag.png"
    x=10
    y=20
    name="second"
    script = open('script.js', 'r').read()
    script += f'pasteImage("{filename}", "{name}", {x}, {y})'
    result = conn.execute(script)
    print(result)
    jpeg_binary = conn.get_document_thumbnail()
    print(conn.execute('activeDocument.close()'))
