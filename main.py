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

# should be enough?
def convert_to_decimal(byte):
    return int(byte, 2)

def read_image_and_prepare_data(path="",):

    if path == "":
        raise ValueError("Path cannot be empty.")

    img = cv2.imread(path)

    # flatten
    img_byte_stream = img.flatten()

    # convert into a bit stream
    img_bit_stream = np.array(list(map(convert_to_binary, img_byte_stream)))

    return img_bit_stream, img_byte_stream, img.shape

def encode_message_in_img(msg_chunk, img_byte):

    # so take the chunk and replace the talk end of the img byte with it
    print(f'Chunk from Message: {msg_chunk}')
    print(f'Byte from Image: {img_byte}')

    new_img_byte = np.concatenate((img_byte[:6], msg_chunk))

    # should return a binary string
    return "".join(new_img_byte)

def stitch_new_image(modified_stream, old_stream):

    length_of_modified_bytes = len(modified_stream)

    new_image_byte_stream = np.concatenate((modified_stream, old_stream[length_of_modified_bytes:]))
    return new_image_byte_stream

def encode(path, msg, output_path = "encode_output.png"):

    # # read the image, prepare by flattening and then getting the bit stream
    image_bit_stream, img_bytes_stream, image_dimensions = read_image_and_prepare_data(path)

    # take the message to be encoded and turn it into a stream of bits.
    message_bit_stream = np.array(list(map(convert_to_binary_string, list(msg)))).flatten()

    # divide the message bit stream into chunks of 2
    message_bit_stream = np.array(chunks(message_bit_stream, 2))

    # encode the the message stream into the image
    modified_bits_stream = list(map(encode_message_in_img, message_bit_stream, image_bit_stream))

    # convert back to a stream of bytes
    modified_byte_stream = np.array(list(map(convert_to_decimal, modified_bits_stream)))

    # stitch the new stream of bytes to the old one
    new_image_bytes = stitch_new_image(modified_byte_stream, img_bytes_stream)

    # reshape and then export
    new_image_matrix = new_image_bytes.reshape(image_dimensions)

    cv2.imwrite(output_path, new_image_matrix)
    print("Done!")

def bin2char(binary_string):
    return chr(int(binary_string, 2))

def decode(path, length_of_message=6):
    # this should be a byte stream
    img_bits_stream, _ , dims = read_image_and_prepare_data(path)

    encoded_message_bits = []
    for x in range(length_of_message * 4):
        encoded_message_bits.append(img_bits_stream[x][6:])

    # create np array and reshape so that the length of the message works
    encoded_message_bits = np.array(encoded_message_bits).reshape((length_of_message, 8))

    # get the byte strings
    encoded_message_byte_strings = list(map("".join, encoded_message_bits))

    # turn the byte strings into characters and join them
    encoded_message = "".join(list(map(bin2char, encoded_message_byte_strings)))

    return encoded_message

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    encode_or_decode = int(input("Enter 1 for encode, Enter 2 for decode"))

    if encode_or_decode == 1:
        input_image_path = input("Specify Input Path with extension: ")
        encoding_msg = input("What message would you like to encode?: ")

        encode(path=input_image_path, msg=encoding_msg)

    if encode_or_decode == 2:
        input_image_path = input("Specify Output Path with extension: ")
        msg_length = int(input("Enter the length of the message:"))

        out = decode(input_image_path, msg_length)
        print(f'Here is the encoded message: {out}')
    # input_image_path = "test.png"
    #
    # encoding_msg = "Hello!"
    # encode(path=input_image_path, msg=encoding_msg)

    # all you need to know is the length of the message
    decode_img_path = "encode_output.png"

    decode(decode_img_path, length_of_message=6)

    exit(0)




