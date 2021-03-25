import cv2
from itertools import chain
import numpy as np
# import sys
# np.set_printoptions(threshold=sys.maxsize)

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

def map_binary_list_to_encoding_region(e, b_c):
    if int(b_c) == 1:
        # make sure that it is odd
        if e % 2 == 0:
            e += 1

        print("odd")
    else:
        # make sure it is even
        if e % 2 == 1:
            e -= 1
        print("even")

    return e

def encode_image(bin_rep, imageMatrix):

    print(f'Image Matrix: {imageMatrix}')
    print(f'Image Matrix Shape: {imageMatrix.shape}')

    x = 0
    outputImageMatrix = []
    for bin_char in bin_rep:
        # get the encoding region
        encoding_region = list(chain.from_iterable(imageMatrix[x:x + 3]))

        # map the encoding region to the bin Char array
        encoding_region_output = list(map(map_binary_list_to_encoding_region, encoding_region, bin_char))

        # append the output
        outputImageMatrix.append([encoding_region_output[j:j+3] for j in range(0, len(encoding_region_output), 3)])

        # make sure to only get every 3
        x += 3


    return list(chain.from_iterable(outputImageMatrix))

def read_image_and_prepare_data(path=""):
    if path == "":
        raise ValueError("Path cannot be empty.")

    img = cv2.imread(path)
    img_dimensions = img.shape[:2]

    # flatten
    img = img.reshape((img_dimensions[0] * img_dimensions[1], 3))

    return img, img_dimensions

def encode(path, msg, output_path = "encode_output.png"):

    # prepare data
    prepared_img_data, img_dimen = read_image_and_prepare_data(path)

    # msg
    msg_binary_representation = convert_message_to_binary(msg)

    # encode the image - get the data from the encoder
    encoded_image_data = np.array(encode_image(msg_binary_representation, prepared_img_data))

    # assert that the length of the of the encoded image_data is 3 * length of the msg
    assert encoded_image_data.shape[0] == len(msg) * 3, "The encoded image data should be 3 times the length of the message!"

    # concat the encoded image to the original image
    output_image_data_flat = np.concatenate((encoded_image_data, prepared_img_data[len(msg) * 3:]), axis=0)

    # reshape the output
    outputImage = output_image_data_flat.reshape((img_dimen[0], img_dimen[1], 3))

    # write the output
    cv2.imwrite(output_path, outputImage)

def decode(path):
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # # # read the image
    # image = cv2.imread("test.png")
    # dim = image.shape[:2]
    #  # (64, 64, 3)
    #
    # # flatten the image to make it usable
    # flattenImage = image.reshape((dim[0] * dim[1], 3))
    #
    # msgToBeEncoded = "Hii"
    #
    # # convert to binary
    # binary_rep = convert_message_to_binary(msgToBeEncoded)
    #
    # # encode
    # encoded_image_flat = np.array(encode_image(binary_rep, flattenImage))
    #
    # # encoded
    # print(f"Encoded Image Flat: {encoded_image_flat}")
    # print(f'Encoded Image Flat Shape: {encoded_image_flat.shape}')
    #
    # # concat
    #
    # outputImageFlat = np.concatenate((encoded_image_flat, flattenImage[len(msgToBeEncoded) * 3:]), axis=0)
    #
    #
    # print(f"outputImageFlat Image Flat 2: {outputImageFlat}")
    # print(f'outputImageFlat Flat Shape 2: {outputImageFlat.shape}')
    #
    # # output Image
    # outputImage = outputImageFlat.reshape((dim[0], dim[1], 3))
    #
    # print(f'Output: {outputImage.shape}')
    #
    # cv2.imwrite('asd.png', outputImage)

    # encode

    # DECODE
    #img_data, image_dimensions = read_image_and_prepare_data('asd.png')

    #print(img_data)





