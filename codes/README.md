
# pdf_txt.py setup

1. Install  Python 3.5

https://www.python.org/

### 2. Install OCR Algorithm (LSTM Neural Network Recognition) - https://github.com/tesseract-ocr/tesseract

sudo apt-get install tesseract-ocr

### 3. Install packages

pip install pillow
pip install pytesseract

### 4. change in policy.xml file at etc/ImageMagick-6

  <policy domain="coder" rights="none" pattern="PDF" />
			to 
  <policy domain="coder" rights="read" pattern="PDF" />

### 5. Comment out the limit tags for policymap.xml

  <!-- <policy domain="resource" name="temporary-path" value="/tmp"/> -->
  <!-- <policy domain="resource" name="memory" value="2GiB"/> -->
  <!-- <policy domain="resource" name="map" value="4GiB"/> -->
  <!-- <policy domain="resource" name="area" value="1GB"/> -->
  <!-- <policy domain="resource" name="disk" value="16EB"/> -->
  <!-- <policy domain="resource" name="file" value="768"/> -->
  <!-- <policy domain="resource" name="thread" value="4"/> -->
  <!-- <policy domain="resource" name="throttle" value="0"/> -->
  <!-- <policy domain="resource" name="time" value="3600"/> -->
  <!-- <policy domain="system" name="precision" value="6"/> -->
