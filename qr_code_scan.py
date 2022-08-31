import sys
import cv2
import math
from pyzbar.pyzbar import decode

# p_img = r'.\img\CO2.jpeg'
p_img = sys.argv[1].split(";;")
result = []


def rotate(image, angleInDegrees):

    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)

    rot = cv2.getRotationMatrix2D(img_c, angleInDegrees, 1)

    rad = math.radians(angleInDegrees)
    sin = math.sin(rad)
    cos = math.cos(rad)
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))

    rot[0, 2] += ((b_w / 2) - img_c[0])
    rot[1, 2] += ((b_h / 2) - img_c[1])

    outImg = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)
    return outImg


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


for pth in p_img:

    img = cv2.imread(pth)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray_img_eqhist = cv2.equalizeHist(gray_img)
    img = gray_img

    code = decode(img)
    for qrcode in code:
        # print(qrcode.data.decode("utf-8"))
        if(qrcode.type == "QRCODE"):
            val = qrcode.data.decode("utf-8")
            if val not in result:
                result.append(val)
            # cv2.imshow("Inteira", img)
            # cv2.waitKey(0)

    # cv2.imshow("Cortada", gray_img)
    # cv2.waitKey(0)

    img = image_resize(img, height=4000)
    img = image_resize(img, width=3000)

    div_h = 4 * 4
    div_w = 3 * 4

    (h, w) = img.shape[:2]

    nh = h//div_h
    nw = w//div_w

    recorte = 3

    for j in range(0, (div_h-recorte+1)):
        for i in range(0, (div_w-recorte+1)):
            # crop = img[nh*i:nh*(i+1), nw*i:nw*(i+1)]
            crop = img[nh*j:nh*(j+recorte), nw*i:nw*(i+recorte)]

            code = decode(crop)
            for qrcode in code:
                if(qrcode.type == "QRCODE"):
                    # print(qrcode.data.decode("utf-8"))
                    val = qrcode.data.decode("utf-8")
                    if val not in result:
                        result.append(val)
                        # print(val)
                    # cv2.imshow("Cortada", crop)
                    # cv2.waitKey(0)

            # for a in range(0, 360, 90):
            #     rotated = rotate(crop, a)
            #     code = decode(rotated)
            #     if(qrcode.type=="QRCODE"):
            #         for qrcode in code:
            #             val = qrcode.data.decode("utf-8")
            #             if val not in result:
            #                 result.append(val)

            # cv2.imshow("Rotacionada", rotated)
            # cv2.waitKey(0)


print(result)
