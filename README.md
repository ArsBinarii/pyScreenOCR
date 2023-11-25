# pyScreenOCR
python script to periodically grab portion of screen and read it out loud

USAGE ex: python pyScreenOCR.py --coords 413 1459 1604 1632 --contrast 25 --original "capture.png" --processed "processed_capture.png" --verbose

```
usage: pyScreenOCR.py [-h] [--coords COORDS COORDS COORDS COORDS] [--contrast CONTRAST] [--original ORIGINAL] [--processed PROCESSED]
                      [--verbose]

Capture a portion of the screen, apply OCR, and read it aloud if it changes.

options:
  -h, --help            show this help message and exit
  --coords COORDS COORDS COORDS COORDS
                        Coordinates for the screen capture, in the format: top_x top_y bottom_x bottom_y
  --contrast CONTRAST   Contrast threshold (0-255) for image processing
  --original ORIGINAL   Filename for saving the original screenshot
  --processed PROCESSED
                        Filename for saving the processed screenshot
  --verbose             Print debug statements to the console
```


### install requirements via pip
### script is meant for Windows at this point
### install tesseract OCR for it to work https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe