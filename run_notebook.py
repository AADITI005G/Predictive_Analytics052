from pathlib import Path
import nbformat
from nbclient import NotebookClient
root=Path(__file__).resolve().parent
path=root/'Food_Delivery_Three_Datasets_KDD.ipynb'
nb=nbformat.read(path,as_version=4)
NotebookClient(nb,timeout=1800,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbformat.write(nb,path)
print('Executed and saved all notebook cells.')
