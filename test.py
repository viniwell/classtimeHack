import os
from pathlib import Path


path = Path(os.path.join(__file__, f"../images/2.png")).absolute()
path.parent.mkdir(exist_ok=True, parents=True)


"""os.makedirs(path, exist_ok=True)
with open(path, 'w+'):
    pass"""

with open(path, 'wb') as file:
    file.write(b'Text in bytes')


with open(path, 'r') as file:
    print(file.readline())

print(str(path))