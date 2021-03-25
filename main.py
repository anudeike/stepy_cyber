import cv2
from itertools import chain
import numpy as np
# import sys
# np.set_printoptions(threshold=sys.maxsize)


def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

def convert_to_binary(byte):

    raw = list(bin(byte))[2:]

    # pad the length
    num_zeros_to_pad = 8 - len(raw)
    padding_zeros = ['0' for _ in range(num_zeros_to_pad)]

    padded = np.concatenate((padding_zeros, raw))
    return padded

def convert_to_binary_string(ch):

    raw = list(bin(ord(ch)))[2:]

    # pad the length
    num_zeros_to_pad = 8 - len(raw)
    padding_zeros = ['0' for _ in range(num_zeros_to_pad)]

    padded = np.concatenate((padding_zeros, raw))
    return padded

def read_image_and_prepare_data(path="",):

    if path == "":
        raise ValueError("Path cannot be empty.")

    img = cv2.imread(path)
    img_dimensions = img.shape[:2]

    # flatten
    img = img.flatten()

    # convert into a bit stream
    img_bit_stream = np.array(list(map(convert_to_binary, img)))

    return img_bit_stream, img_dimensions

def encode_message_in_img(msg_chunk, img_byte):

    # so take the chunk and replace the talk end of the img byte with it
    print(f'Chunk from Message: {msg_chunk}')
    print(f'Byte from Image: {img_byte}')

    new_img_byte = np.concatenate((img_byte[:6], msg_chunk))

    # should return a binary string
    return "".join(new_img_byte)

def encode(path, msg, output_path = "encode_output.png"):

    # # read the image, prepare by flattening and then getting the bit stream
    image_bit_stream, image_dimensions = read_image_and_prepare_data(input_image_path)

    # take the message to be encoded and turn it into a stream of bits.
    message_bit_stream = np.array(list(map(convert_to_binary_string, list(encoding_msg)))).flatten()

    # divide the message bit stream into chunks of 2
    message_bit_stream = np.array(chunks(message_bit_stream, 2))

    # encode the the message stream into the image
    v = list(map(encode_message_in_img, message_bit_stream, image_bit_stream))
    #print(message_bit_stream)
    print(v)
    pass

def decode(path):
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    """
    How the algorithm works
    
    
    """
    input_image_path = "test.png"
    encoding_msg = "Hello!"
    encode(path=input_image_path, msg=encoding_msg)

    exit(0)




