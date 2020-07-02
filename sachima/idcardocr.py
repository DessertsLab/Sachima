import os
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import time

X = 1280.00 / 3840.00
PIXEL_X = int(X * 3840)
print(X, PIXEL_X)

MASKS_DIR = os.path.join(os.path.dirname(__file__), "masks")

CARD_MASK = os.path.join(MASKS_DIR, "idcard_mask.jpg")
NAME_MASK = os.path.join(MASKS_DIR, "name_mask_%s.jpg" % PIXEL_X)
SEX_MASK = os.path.join(MASKS_DIR, "sex_mask_%s.jpg" % PIXEL_X)
NATION_MASK = os.path.join(MASKS_DIR, "nation_mask_%s.jpg" % PIXEL_X)
ADDRESS_MASK = os.path.join(MASKS_DIR, "address_mask_%s.jpg" % PIXEL_X)
IDNUM_MASK = os.path.join(MASKS_DIR, "idnum_mask_%s.jpg" % PIXEL_X)


def img_resize_w(imggray, dwidth):
    crop = imggray
    size = crop.get().shape
    height = size[0]
    width = size[1]
    height = height * dwidth / width
    crop = cv2.resize(
        src=crop, dsize=(dwidth, int(height)), interpolation=cv2.INTER_CUBIC
    )
    return crop


# 图像捕获
def find(img_name):
    print(u"进入身份证模版匹配流程...")
    mask_name = CARD_MASK
    print(mask_name)
    MIN_MATCH_COUNT = 10
    img1 = cv2.UMat(cv2.imread(mask_name, 0))  # queryImage in Gray mask
    img1 = img_resize_w(img1, 640)
    img2 = cv2.UMat(cv2.imread(img_name, 0))  # trainImage in Gray img
    img2 = img_resize_w(img2, 1920)
    img_org = cv2.UMat(cv2.imread(img_name))  # color img
    img_org = img_resize_w(img_org, 1920)
    #  Initiate SIFT detector
    t1 = round(time.time() * 1000)

    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=10)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    # 两个最佳匹配之间距离需要大于ratio 0.7,距离过于相似可能是噪声点
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    # reshape为(x,y)数组
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # 用HomoGraphy计算图像与图像之间映射关系, M为转换矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        # matchesMask = mask.ravel().tolist()
        # 使用转换矩阵M计算出img1在img2的对应形状
        h, w = cv2.UMat.get(img1).shape
        M_r = np.linalg.inv(M)
        im_r = cv2.warpPerspective(img_org, M_r, (w, h))
        # self.showimg(im_r)
    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
    t2 = round(time.time() * 1000)
    print(u"查找身份证耗时:%s" % (t2 - t1))
    return im_r


# # 展示图像
# def showimg(img):
#     cv2.namedWindow("contours", 0)
#     # cv2.resizeWindow("contours", 1600, 1200);
#     cv2.imshow("contours", img)
#     cv2.waitKey()


def ocr(imgname):
    # generate_mask(x)
    img_data_gray, img_org = img_resize_gray(imgname)
    result_dict = dict()
    # name_pic = find_name(img_data_gray, img_org)
    name_pic = find_object(img_data_gray, img_org, NAME_MASK, 700, 300)
    result_dict["name"] = get_name(name_pic)

    sex_pic = find_object(img_data_gray, img_org, SEX_MASK, 300, 300)
    result_dict["sex"] = get_sex(sex_pic)

    nation_pic = find_object(img_data_gray, img_org, NATION_MASK, 500, 320)
    result_dict["nation"] = get_nation(nation_pic)

    address_pic = find_object(img_data_gray, img_org, ADDRESS_MASK, 1700, 560)
    result_dict["address"] = get_address(address_pic)

    idnum_pic = find_object(img_data_gray, img_org, IDNUM_MASK, 2300, 300)
    result_dict["idnum"], result_dict["birth"] = get_idnum_and_birth(idnum_pic)
    return result_dict


def generate_mask(x):
    name_mask_pic = cv2.UMat(cv2.imread("name_mask.jpg"))
    sex_mask_pic = cv2.UMat(cv2.imread("sex_mask.jpg"))
    nation_mask_pic = cv2.UMat(cv2.imread("nation_mask.jpg"))
    birth_mask_pic = cv2.UMat(cv2.imread("birth_mask.jpg"))
    year_mask_pic = cv2.UMat(cv2.imread("year_mask.jpg"))
    month_mask_pic = cv2.UMat(cv2.imread("month_mask.jpg"))
    day_mask_pic = cv2.UMat(cv2.imread("day_mask.jpg"))
    address_mask_pic = cv2.UMat(cv2.imread("address_mask.jpg"))
    idnum_mask_pic = cv2.UMat(cv2.imread("idnum_mask.jpg"))
    name_mask_pic = img_resize_x(name_mask_pic)
    sex_mask_pic = img_resize_x(sex_mask_pic)
    nation_mask_pic = img_resize_x(nation_mask_pic)
    birth_mask_pic = img_resize_x(birth_mask_pic)
    year_mask_pic = img_resize_x(year_mask_pic)
    month_mask_pic = img_resize_x(month_mask_pic)
    day_mask_pic = img_resize_x(day_mask_pic)
    address_mask_pic = img_resize_x(address_mask_pic)
    idnum_mask_pic = img_resize_x(idnum_mask_pic)
    cv2.imwrite("name_mask_%s.jpg" % PIXEL_X, name_mask_pic)
    cv2.imwrite("sex_mask_%s.jpg" % PIXEL_X, sex_mask_pic)
    cv2.imwrite("nation_mask_%s.jpg" % PIXEL_X, nation_mask_pic)
    cv2.imwrite("birth_mask_%s.jpg" % PIXEL_X, birth_mask_pic)
    cv2.imwrite("year_mask_%s.jpg" % PIXEL_X, year_mask_pic)
    cv2.imwrite("month_mask_%s.jpg" % PIXEL_X, month_mask_pic)
    cv2.imwrite("day_mask_%s.jpg" % PIXEL_X, day_mask_pic)
    cv2.imwrite("address_mask_%s.jpg" % PIXEL_X, address_mask_pic)
    cv2.imwrite("idnum_mask_%s.jpg" % PIXEL_X, idnum_mask_pic)


# 用于生成模板
def img_resize_x(imggray):
    # print 'dheight:%s' % dheight
    crop = imggray
    size = crop.get().shape
    dheight = int(size[0] * X)
    dwidth = int(size[1] * X)
    crop = cv2.resize(src=crop, dsize=(dwidth, dheight), interpolation=cv2.INTER_CUBIC)
    return crop


# idcardocr里面resize以高度为依据, 用于get部分
def img_resize(imggray, dheight):
    # print 'dheight:%s' % dheight
    crop = imggray
    size = crop.get().shape
    height = size[0]
    width = size[1]
    width = width * dheight / height
    crop = cv2.resize(
        src=crop, dsize=(int(width), dheight), interpolation=cv2.INTER_CUBIC
    )
    return crop


def img_resize_gray(imgorg):

    # imgorg = cv2.imread(imgname)
    crop = imgorg
    size = cv2.UMat.get(crop).shape
    # print size
    height = size[0]
    width = size[1]
    # 参数是根据3840调的
    height = int(height * 3840 * X / width)
    # print height
    crop = cv2.resize(
        src=crop, dsize=(int(3840 * X), height), interpolation=cv2.INTER_CUBIC
    )
    return hist_equal(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)), crop


# -------------------------


def find_object(crop_gray, crop_org, maskname, p1, p2):
    template = cv2.UMat(cv2.imread(maskname, 0))
    w, h = cv2.UMat.get(template).shape[::-1]
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = (max_loc[0] + w, max_loc[1] - int(20 * X))
    bottom_right = (top_left[0] + int(p1 * X), top_left[1] + int(p2 * X))
    result = cv2.UMat.get(crop_org)[
        top_left[1] - 10 : bottom_right[1], top_left[0] - 10 : bottom_right[0]
    ]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    return cv2.UMat(result)


def showimg(img):
    cv2.namedWindow("contours", 0)
    cv2.resizeWindow("contours", 1280, 720)
    cv2.imshow("contours", img)
    cv2.waitKey()


# psm model:
#  0    Orientation and script detection (OSD) only.
#  1    Automatic page segmentation with OSD.
#  2    Automatic page segmentation, but no OSD, or OCR.
#  3    Fully automatic page segmentation, but no OSD. (Default)
#  4    Assume a single column of text of variable sizes.
#  5    Assume a single uniform block of vertically aligned text.
#  6    Assume a single uniform block of text.
#  7    Treat the image as a single text line.
#  8    Treat the image as a single word.
#  9    Treat the image as a single word in a circle.
#  10    Treat the image as a single character.
#  11    Sparse text. Find as much text as possible in no particular order.
#  12    Sparse text with OSD.
#  13    Raw line. Treat the image as a single text line,
# 			bypassing hacks that are Tesseract-specific


def get_name(img):
    _, _, red = cv2.split(img)  # split 会自动将UMat转换回Mat
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(
        red, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 50
    )
    red = img_resize(red, 150)
    img = img_resize(img, 150)
    return get_result_vary_length(red, "chi_sim", img, "--psm 7")


def get_sex(img):
    _, _, red = cv2.split(img)
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(
        red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50
    )
    red = img_resize(red, 150)
    return get_result_fix_length(red, 1, "chi_sim", "--psm 10")


def get_nation(img):
    _, _, red = cv2.split(img)
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(
        red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50
    )
    red = img_resize(red, 150)
    return get_result_fix_length(red, 1, "chi_sim", "--psm 10")


def get_address(img):
    _, _, red = cv2.split(img)
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(
        red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50
    )
    red = img_resize(red, 300)
    # img = img_resize(img, 300)
    # cv2.imwrite('address_red.png', red)
    img = Image.fromarray(cv2.UMat.get(red).astype("uint8"))
    # return punc_filter(get_result_vary_length(red,'chi_sim', img, '-psm 6'))
    return punc_filter(get_result_vary_length(red, "chi_sim", img, "--psm 6"))
    # return punc_filter(pytesseract.image_to_string(img, lang='chi_sim', config='-psm 3').replace(" ",""))


def get_idnum_and_birth(img):
    _, _, red = cv2.split(img)
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(
        red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50
    )
    red = img_resize(red, 150)
    # cv2.imwrite('idnum_red.png', red)
    # idnum_str = get_result_fix_length(red, 18, 'idnum', '-psm 8')
    # idnum_str = get_result_fix_length(red, 18, 'eng', '--psm 8 ')
    img = Image.fromarray(cv2.UMat.get(red).astype("uint8"))
    idnum_str = get_result_vary_length(red, "eng", img, "--psm 8 ")
    return idnum_str, idnum_str[6:14]


def get_result_fix_length(red, fix_length, langset, custom_config=""):
    red_org = red
    cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(
        red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(red, contours, -1, (0, 255, 0), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)

    h_threshold = 54
    numset_contours = []
    calcu_cnt = 1
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > h_threshold:
            numset_contours.append((x, y, w, h))
    while len(numset_contours) != fix_length:
        if calcu_cnt > 50:
            print(u"计算次数过多！目前阈值为：", h_threshold)
            break
        numset_contours = []
        calcu_cnt += 1
        if len(numset_contours) > fix_length:
            h_threshold += 1
            contours_cnt = 0
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h > h_threshold:
                    contours_cnt += 1
                    numset_contours.append((x, y, w, h))
        if len(numset_contours) < fix_length:
            h_threshold -= 1
            contours_cnt = 0
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h > h_threshold:
                    contours_cnt += 1
                    numset_contours.append((x, y, w, h))
    result_string = ""
    numset_contours.sort(key=lambda num: num[0])
    for x, y, w, h in numset_contours:
        result_string += pytesseract.image_to_string(
            cv2.UMat.get(red_org)[y - 10 : y + h + 10, x - 10 : x + w + 10],
            lang=langset,
            config=custom_config,
        )
    return result_string


def get_result_vary_length(red, langset, org_img, custom_config=""):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(
        red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(red, contours, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    result_string = ""
    result_string += pytesseract.image_to_string(
        cv2.UMat.get(red_org)[y - 10 : y + h + 10, x - 10 : x + w + 10],
        lang=langset,
        config=custom_config,
    )
    return punc_filter(result_string)


def punc_filter(str):
    temp = str
    xx = u"([\u4e00-\u9fff0-9A-Z]+)"
    pattern = re.compile(xx)
    results = pattern.findall(temp)
    string = ""
    for result in results:
        string += result
    return string


# 这里使用直方图拉伸，不是直方图均衡
def hist_equal(img):
    image = img.get()  # UMat to Mat
    lut = np.zeros(256, dtype=image.dtype)  # 创建空的查找表
    hist = cv2.calcHist(
        [image],  # 计算图像的直方图
        [0],  # 使用的通道
        None,  # 没有使用mask
        [256],  # it is a 1D histogram
        [0, 256],
    )
    minBinNo, maxBinNo = 0, 255
    # 计算从左起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(hist):
        if binValue != 0:
            minBinNo = binNo
            break
    # 计算从右起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(reversed(hist)):
        if binValue != 0:
            maxBinNo = 255 - binNo
            break
    # print minBinNo, maxBinNo
    # 生成查找表
    for i, v in enumerate(lut):
        if i < minBinNo:
            lut[i] = 0
        elif i > maxBinNo:
            lut[i] = 255
        else:
            lut[i] = int(255.0 * (i - minBinNo) / (maxBinNo - minBinNo) + 0.5)
    # 计算,调用OpenCV cv2.LUT函数,参数 image --  输入图像，lut -- 查找表
    result = cv2.LUT(image, lut)
    return cv2.UMat(result)
