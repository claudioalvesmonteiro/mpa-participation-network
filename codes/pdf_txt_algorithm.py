'''
Transform PDF to Text

@claudioalvesmonteiro
May/2020
'''

# import packages
import io
import os
from PIL import Image
import pytesseract
from wand.image import Image as wi


def pdfToTxt(filename):
	print('Extracting {}'.format(filename))
	print('WARNING: Corrupted text on file may retrive errors during extraction')

	# open image 
	filename = filename[0:-4]
	pdfFile = wi(filename = 'data/{}.pdf'.format(filename), resolution = 300)
	image = pdfFile.convert('jpeg')

	# transform image to imageBlob
	imageBlobs = []
	for img in image.sequence:
		imgPage = wi(image = img)
		imageBlobs.append(imgPage.make_blob('jpeg'))

	# extract text from imageBlob
	extract = ''
	for imgBlob in imageBlobs:
		image = Image.open(io.BytesIO(imgBlob))
		text = pytesseract.image_to_string(image, lang = 'eng')
		extract += text

	# save as text file
	file = open('data/text/{}.txt'.format(filename), 'w')
	file.write(extract)
	file.close()


# list files in directory
files = os.listdir('data/.')[0:3]

# if pdf, extract and save 
for file in files:
	if file[-4:] == '.pdf':
		pdfToTxt(file)
