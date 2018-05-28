run with: python metamaker_b09.py

The program uses non-standard Python2 packages:
Tkinter
reportlab
when running the program from source, it might be required to install them
In linux:
sudo apt-get install python-tk
pip install reportlab

It is possible to make stand-alone executable by typing:
pyinstaller metamaker_b09.py -F
the executable can be found from pwd/dist
it might be necessary to install pyinstaller
Linux:
pip install pyinstaller
