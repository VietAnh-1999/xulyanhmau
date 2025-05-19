import cv2
import numpy as np

img = cv2.VideoCapture(0)

def xacdinhkhoi(image):
    
    #CHUYEN VE DEN TRANG
    image_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    # LAM MO DE GIAM NHIEU
    image_blurred = cv2.GaussianBlur(image_gray,(3,3),0)
    cv2.imshow("blur",image_blurred)
    # phat hien canh trong anh
    image_edges = cv2.Canny(image_blurred,30,100)
    cv2. imshow("edges",image_edges)
    #tim  cac diem duong vien
    contours,_ = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Duyet cac duong vien da tim duoc
    for contour in contours:
        #lay da giac ben  ngoai
        lenth = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour,lenth,True)

        # lay so dinh cua da giac
        point = len(approx)


        #xac dinh hinh dua tren so dinh
        shape = "khong xac dinh"

        if point == 3:
            shape = "Tam giac"

        elif point == 4:
            (x,y,w,h) = cv2.boundingRect(contour)
            ratio = float(w) / h
            shape = "Hinh Vuong" if 0.95 <= ratio <= 1.05 else "Hinh chu nhat"
        elif point >= 8:
            shape = "Hinh Tron"

        #ve hinh doi tuong va hinh dang len anh goc
        cv2.drawContours(image, [contour],-1,(255,0,0),1)
        cv2.putText(image,shape,(approx[0][0][0],approx[0][0][1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,0,0),1)

i = 0     
print("nhan 'q' de thoat")
while True:
    path = "D:/Xulyanhmau/codechup/picture/"
    _,image = img.read()
    #xacdinhkhoi(image)
    cv2.imshow("",image)
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('c'):
        name_file = path + "picture" + str(i) + ".jpg"
        cv2.imwrite(name_file, image)
        # picture = cv2.imread(name_file)
        # xacdinhkhoi(picture)
        # cv2.imshow("nhandang", picture)
        i += 1