'''
Transform PDF to Text

@claudioalvesmonteiro
May/2020
'''

# import packages
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi


name = 'meeting_31'

def pdfToTxt(filename):
	print('Extracting ')
	print('WARNING: Corrupted text on file may retrive errors during extraction')
	# open image 
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

	file = open('data/text/{}.txt'.format(filename), 'w')
	file.write(extract)
	file.close()


pdfToTxt('meeting_27')