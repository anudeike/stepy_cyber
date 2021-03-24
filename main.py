import cv2
from itertools import chain

def char_to_binary(c):
    # helper function to get the correct representation of the binary number we need
    raw_bin = list(bin(ord(c))[2:])

    # if the length is less than 9 pad it with zeros at the front
    num_zeros_to_pad = 9 - len(raw_bin)
    padding_zeros = ['0' for _ in range(num_zeros_to_pad)]

    return padding_zeros + raw_bin


def convert_message_to_binary(msg):
    char_list = list(msg)

    binary_rep_array = []

    for char in char_list:
        binary_rep_array.append(char_to_binary(char))

    return binary_rep_array

def encode_image(bin_rep, imageMatrix):

    x = 0
    while x < (len(imageMatrix)):
        # flatten the region
        encoding_region = list(chain.from_iterable(imageMatrix[x:x+3]))

        for i in range(bin_rep):
            if int(bin_rep[i]) == 1:
                # make sure that it is odd
                print("odd")
            else:
                print("even")

        x += 3

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # # read the image
    # image = cv2.imread("test.png")
    # color = image
    # print(color.shape) # (64, 64, 3)

    # use a test
    fakeImage = [(27, 64, 164), (248, 244, 194), (174, 246, 250), (149, 95, 232),
     (188, 156, 169), (71, 167, 127), (132, 173, 97), (113, 69, 206),
     (255, 29, 213), (53, 153, 220), (246, 225, 229), (142, 82, 175)]

    msgToBeEncoded = "Hii"

    # convert to binary
    binary_rep = convert_message_to_binary(msgToBeEncoded)

    # flatten
    flatten_binary_rep = list(chain.from_iterable(binary_rep))

    # encode
    encode_image(flatten_binary_rep, fakeImage)



