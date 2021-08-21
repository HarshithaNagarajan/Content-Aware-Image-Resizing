import numpy as np
from scipy.ndimage.filters import convolve
import cv2

"""
public class SeamCarver {
   public SeamCarver(Picture picture)
   public Picture picture()                          // current picture
   public     int width()                            // width of current picture
   public     int height()                           // height of current picture
   public  double energy(int x, int y)               // energy of pixel at column x and row y
   public   int[] findHorizontalSeam()               // sequence of indices for horizontal seam
   public   int[] findVerticalSeam()                 // sequence of indices for vertical seam
   public    void removeHorizontalSeam(int[] seam)   // remove horizontal seam from picture
   public    void removeVerticalSeam(int[] seam)     // remove vertical seam from picture
}

"""


class CAIR():

    def __init__(self, image, scale):
        self.img = image
        self.scale = scale


    def energy_sobel(self):
        filter_dx = np.array([
            [1.0, 2.0, 1.0],
            [0.0, 0.0, 0.0],
            [-1.0, -2.0, -1.0],
        ])
        filter_dx = np.stack([filter_dx] * 3, axis=2)
        filter_dy = np.array([
            [1.0, 0.0, -1.0],
            [2.0, 0.0, -2.0],
            [1.0, 0.0, -1.0],
        ])
        filter_dy = np.stack([filter_dy] * 3, axis=2)

        img = self.img.astype('float32')
        convolved = np.absolute(convolve(img, filter_dx)) + np.absolute(convolve(img, filter_dy))
        energy_matrix = convolved.sum(axis=2)

        return energy_matrix

    def findCosts(self):

        r, c, _ = self.img.shape

        EM = self.energy_sobel()
        cost_matrix = EM

        for i in range(1, r):
            for j in range(c):
                if j == 0:
                    min_energy = min(cost_matrix[i - 1, j], cost_matrix[i - 1, j + 1])
                elif j == c - 1:
                    min_energy = min(cost_matrix[i - 1, j - 1], cost_matrix[i - 1, j])
                else:
                    min_energy = min(cost_matrix[i - 1, j - 1], cost_matrix[i - 1, j], cost_matrix[i - 1, j + 1])

                cost_matrix[i, j] = EM[i, j] + min_energy

        # print("\nM:\n", cost_matrix.shape)
        return cost_matrix

    def findVerticalSeam(self):

        r = self.img.shape[0]

        cost_matrix = self.findCosts()

        seam = np.zeros(r, dtype=int)

        # print(np.argmin(cost_matrix[r - 1]))
        # seam[matrix.shape[0] - 1] = list(np.where(cost_matrix == min(cost_matrix[matrix.shape[0] - 1, :])))[0][0]
        seam[r - 1] = np.argmin(cost_matrix[r - 1])
        # print(seam)
        for i in reversed(range(r - 1)):
            j = seam[i + 1]
            if j == 0:
                seam[i] = np.argmin(cost_matrix[i, j:j + 2])
            elif j == self.img.shape[1] - 1:
                seam[i] = np.argmin(cost_matrix[i][j - 1:j + 1]) + j - 1
            else:
                seam[i] = np.argmin(cost_matrix[i][j - 1:j + 2]) + j - 1
        # print("min seam:", seam)
        # print('done')
        return seam

    def removeVerticalSeam(self, seam):

        r, c = self.img.shape[:2]
        linear_inds = np.array(seam) + np.arange(r) * c
        new_image = np.zeros((r, c - 1, 3), dtype="uint8")

        for i in range(3):
            temp = np.delete(self.img[:, :, i], linear_inds.astype(int))
            temp = np.reshape(temp, (r, c - 1))
            new_image[:, :, i] = temp

        # self.img = np.delete(self.img[row], seam[row], axis=0) for row in range(r)

        self.img = new_image

    def reduceHeight(self):
        self.img = np.rot90(self.img, 1, (0, 1))
        self.img = self.reduceWidth()
        self.img = np.rot90(self.img, 3, (0, 1))
        return self.img

    def reduceWidth(self):
        r, c, _ = self.img.shape
        new_c = int(self.scale * c)

        for i in range(c - new_c):
            min_seam = self.findVerticalSeam()
            cv2.imshow("Iter", self.img)
            cv2.waitKey(1)
            self.removeVerticalSeam(min_seam)

        return self.img



    def addVerticalSeam(self, seam):
        r, c = self.img.shape[:2]
        new_image = np.zeros((r, c + 1, 3), dtype="uint8")
        for i in range(len(seam)):
            temp = np.insert(self.img[i], seam[i] + 1, self.img[i, seam[i]], axis=0)
            new_image[i, :] = temp

        self.img = new_image

    def increaseWidth(self):
        r, c, _ = self.img.shape
        new_c = int(self.scale * c)

        for i in range(c - new_c):
            min_seam = self.findVerticalSeam()
            cv2.imshow("Iter", self.img)
            cv2.waitKey(1)
            self.addVerticalSeam(min_seam)

        return self.img

    def increaseHeight(self):
        self.img = np.rot90(self.img, 1, (0, 1))
        self.img = self.increaseWidth()
        self.img = np.rot90(self.img, 3, (0, 1))
        return self.img
