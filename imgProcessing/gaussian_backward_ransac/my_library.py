import numpy as np
import matplotlib.pyplot as plt

def my_padding(src, filter):
    (h, w) = src.shape
    if isinstance(filter, tuple):
        (h_pad, w_pad) = filter
    else:
        (h_pad, w_pad) = filter.shape
    h_pad = h_pad // 2
    w_pad = w_pad // 2
    padding_img = np.zeros((h + h_pad * 2, w + w_pad * 2))
    padding_img[h_pad:h + h_pad, w_pad:w + w_pad] = src
    # repetition padding
    # up
    padding_img[:h_pad, w_pad:w_pad + w] = src[0, :]
    # down
    padding_img[h_pad + h:, w_pad:w_pad + w] = src[h - 1, :]
    # left
    padding_img[:, :w_pad] = padding_img[:, w_pad:w_pad + 1]
    # right
    padding_img[:, w_pad + w:] = padding_img[:, w_pad + w - 1:w_pad + w]

    return padding_img

def my_3D_padding(src, filter):
    (h, w, c) = src.shape
    if isinstance(filter, tuple):
        (h_pad, w_pad, c) = filter
    else:
        (h_pad, w_pad, c) = filter.shape
    h_pad = h_pad // 2
    w_pad = w_pad // 2

    padding_img = np.zeros((h + h_pad * 2, w + w_pad * 2, c), dtype=np.uint8)
    padding_img[h_pad:h + h_pad, w_pad:w + w_pad, :] = src

    # repetition padding
    # up
    padding_img[:h_pad, w_pad:w_pad + w, :] = src[0, :, :]
    # down
    padding_img[h_pad + h:, w_pad:w_pad + w, :] = src[h - 1, :, :]
    # left
    padding_img[:, :w_pad, :] = padding_img[:, w_pad:w_pad + 1, :]
    # right
    padding_img[:, w_pad + w:, :] = padding_img[:, w_pad + w - 1:w_pad + w, :]

    return padding_img


def my_filtering(src, filter):
    (h, w) = src.shape
    (f_h, f_w) = filter.shape
    pad_img = my_padding(src, filter)

    dst = np.zeros((h, w))
    for row in range(h):
        for col in range(w):
            dst[row, col] = np.sum(pad_img[row:row + f_h, col:col + f_w] * filter)

    return dst


def get_my_sobel():
    sobel_x = np.dot(np.array([[1], [2], [1]]), np.array([[-1, 0, 1]]))
    sobel_y = np.dot(np.array([[-1], [0], [1]]), np.array([[1, 2, 1]]))
    return sobel_x, sobel_y


def calc_derivatives(src):
    # calculate Ix, Iy
    sobel_x, sobel_y = get_my_sobel()
    Ix = my_filtering(src, sobel_x)
    Iy = my_filtering(src, sobel_y)
    return Ix, Iy

def show_patch_hist(patch_vector):
    index = np.arange(len(patch_vector))
    plt.bar(index, patch_vector)
    plt.title('orientation histogram')
    plt.show()

def my_get_Gaussian2D_mask(msize, sigma=1):
    #########################################
    # ToDo
    # 2D gaussian filter 만들기
    #########################################
    y, x = np.mgrid[-(msize // 2):(msize // 2) + 1, -(msize // 2):(msize // 2) + 1]
    # 해당 부분을 채워서 결과를 확인하기
    # 2차 gaussian mask 생성
    gaus2D = (1 / 2*np.pi*(sigma**2)) * np.exp(- ((x**2)+(y**2)) / 2*(sigma**2))
    # mask의 총 합 = 1
    gaus2D /= np.sum(gaus2D)
    return gaus2D

def my_get_Gaussian1D_mask(msize, sigma=1):
    #########################################
    # ToDo
    # 1D gaussian filter 만들기
    #########################################
    x = np.full((1, msize), [range(-(msize // 2), (msize // 2) + 1)])
    # 해당 부분을 채워서 결과를 확인하기
    gaus1D = (1 / np.sqrt(2*np.pi*sigma)) * np.exp(- (x**2) / 2*(sigma**2))
    # mask의 총 합 = 1
    gaus1D /= np.sum(gaus1D)
    return gaus1D