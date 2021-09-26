from wand.image import Image as wi
from pytesseract import Output, pytesseract
import cv2

# get the path of pdf and set its resolution
pdf = wi(filename="./New folder/sample.pdf", resolution=300)
# convert pdf to img
pdfImg = pdf.convert('jpg')
# count for number of pages inside the pdf
pageCount = 1

# loop to get all pages
for img in pdfImg.sequence:
    # get image one by one
    page = wi(image=img)
    # save image as img with its sequence
    page.save(filename="img"+str(pageCount)+".jpg")
    # read img with cv2 for creating bounding boxes for text inside the images
    img1 = cv2.imread("img"+str(pageCount)+".jpg")
    # create an empty array
    textArray = []
    # use pytesseract to text from image
    text = pytesseract.image_to_string(img1, lang="eng")
    # add text to the array
    textArray.append(text)
    print(text)

    # TextFile
    # create a textFile name text with it's sequence like text1,text2
    with open('text'+str(pageCount)+'.txt', 'w') as filehandle:
        # read text from array line by line
        for listitem in textArray:
            # write the text to the file
            filehandle.write('%s' % listitem)

    # Bounding Boxes to each text or Text Detection
    # use pytesseract to get text with its coordinates
    d = pytesseract.image_to_data(img1, output_type=Output.DICT)

    # get array of Level
    n_boxes = len(d['level'])
    print(n_boxes)
    # loop to detect text word by word
    for i in range(n_boxes):
        # get the coordinates of each word , like left,top,width,height
        (x, y, w, h) = (d['left'][i], d['top']
                        [i], d['width'][i], d['height'][i])
        print((x, y, w, h))
        # create the bounding box to the text
        cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show image with text detection
    cv2.imshow('res', img1)

    # save image
    cv2.imwrite("img"+str(pageCount)+".jpg", img1)
    # cv2 wait key
    cv2.waitKey(5000)
    # page count
    pageCount += 1
