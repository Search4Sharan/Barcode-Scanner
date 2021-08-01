from imutils.video import VideoStream
from pyzbar import pyzbar
from pylibdmtx import pylibdmtx
#import zxing
import argparse
import datetime
import imutils
import time
import cv2
import hashlib

f= open("data.txt","w+")
ap = argparse.ArgumentParser()
#reader = .BarCodeReader("/home/creator/.local/bin/zxing")
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

l=[]
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)


csv = open(args["output"], "w")
found = set()



while True: 
    if  cv2.waitKey(20)&0xff==ord("q"):
        break
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    
    barcodes = pylibdmtx.decode(frame)

        
    for barcode in barcodes:
    
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


        barcodeData = barcode.data.decode("utf-8")
        barcodeType = "DMC"
        dat="Data :"+barcodeData
        typ="Type :"+barcodeType
        fr = open("data.txt", "r")
        f.writelines(dat)
        f.writelines("\n")
        print("Data :",barcodeData,'\n')
        print("Type :",barcodeType)

        
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


       
        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.datetime.now(),
                barcodeData))
            csv.flush()
            found.add(barcodeData)

   
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    
    if key == ord("q"):
        break
print("[INFO] cleaning up...")
csv.close()
f= open("out.txt","w+")
output_file_path = "out.txt"
input_file_path = "data.txt"

#2
completed_lines_hash = set()

#3
output_file = open(output_file_path, "w")

#4
for line in open(input_file_path, "r"):
  #5
  hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
  #6
  if hashValue not in completed_lines_hash:
    output_file.write(line)
    completed_lines_hash.add(hashValue)
#7
output_file.close()