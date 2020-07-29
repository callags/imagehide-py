import PIL as pillow
from PIL import Image
import binascii
import optparse
import sys

    # rgb2hex takes the current value of the red, green, blue
    # pixels of the image and converts them to hex values

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    # In hex2rgb we are taking the hexcode and converting back to
    # rgb values. First we remove the "#" sign from the hex value 
    # to filter out each rgb color through the tuple () to ensure
    # each pixel gets their correct value to before inserting the 
    # binary message.

def hex2rgb(hexcode):
    hex_values = hexcode.lstrip('#')
    rgb_values = tuple(int(hex_values[i:i+2], 16) for i in (0, 2, 4))
    return rgb_values[0], rgb_values[1], rgb_values[2]

    # When str2bin receieves the message from hide() it
    # first converts the message into hexadecimal in base
    # 16. Afterwards we transform it into an integer
    # followed by changing the integer into a binary string

    # At the very end we want to return the binary string
    # without the '0b' appended at the beggining back to
    # the hide().

def str2bin(message):

    binary_array = [bin(ord(x))[2:].zfill(8) for x in message]
    binary_message = ""
    element = 0
    while element < len(binary_array):
        binary_message += binary_array[int(element)]
        element += 1
    return binary_message

    # bin2str takes the binary message and converts it to ascii
    # by first converting binary to an integer followed by
    # converting the integer to its equivalent ascii. Finally
    # we return the message to the main function

def bin2str(binary):
    message = binascii.unhexlify('%x' % (int('0b'+binary, 2)))
    display_message = (str(message).lstrip('b').replace("'", "").strip('"'))
    return display_message

    # Encode takes the hexidecimal value of each pixel and
    # see if it's with the range of 0 through 5. If it does
    # then it adds the current digit of the binary message to
    # the hexcode variable and returns the current pixel that has
    # the desired hexadecimal value of 0 through 5

    # If the hexcode variable value is not between 0 and 5 it
    # will return nothing back to the calling function

def encode(hexcode, digit, pixel_choice):
    blue = 3
    green = 2
    red = 1

    if pixel_choice == blue:
        if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
            hexcode = hexcode[:-1] + digit
            return hexcode
        else:
            return None

    elif pixel_choice == green:
        if hexcode[-3] in ('0', '1', '2', '3', '4', '5'):
            saved_pixels = hexcode[5:]
            tampered_pixel = hexcode[:-3] + digit
            hexcode = tampered_pixel + saved_pixels
            return hexcode
        else:
            return None

    elif pixel_choice == red:
        if hexcode[-5] in ('0', '1', '2', '3', '4', '5'):
            saved_pixels = hexcode[3:]
            tampered_pixel = hexcode[:-5] + digit
            hexcode = tampered_pixel + saved_pixels
            return hexcode
        else:
            return None

    # Decode takes each hexadecimal value it has and returns
    # the current value of either 0 or 1 to the retr function
    # to be store in the digit variable. Otherwise it returns
    # None back to the retr function

def decode(hexcode, pixel_choice):
    blue = 3
    green = 2
    red = 1

    # Here we are determining which hexadecimal pixel ends
    # in 1 or 0 based on the user's choice

    if pixel_choice == blue:
        if hexcode[-1] in ('0', '1'):
            return hexcode[-1]
        else:
            return None

    elif pixel_choice == green:
        if hexcode[-3] in ('0', '1'):
                return hexcode[-3]
        else:
                return None

    elif pixel_choice == red:
        if hexcode[-5] in ('0', '1'):
            return hexcode[-5]
        else:
            return None

def hide(filename, message, pixel_choice):

    # First we open the image into the img variable and
    # send the message, being text from main to str2bin
    # function and the results to the binary variable

    img = Image.open(filename)

    # After converting the string to binary we will add a
    # delimiter of 15 '1's and one zero

    binary = str2bin(message) + '1111111111111110'

    # At this point we define the type and depth of a pixel
    # in the image as RGBA in the img variable as well as
    # assign datas with the sequence of pixels of the original
    # image

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        digit = 0
        temp = ''
        for item in datas:
            if (digit < len(binary)):

                # Here we go through the entire length of the binary message
                # using the digit variable stated earlier. Each digit of the
                # binary message is stored in the chosen pixel from the user
                # that has a hexadecimal value between 0 and 5 through the
                # rgb2hex function and sent to the encode function to store 
                # the hidden message within the image

                newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit], pixel_choice)

                # If the encode functions returns None it means the current
                # hexidecimal value is greater than 5 we simply append the
                # pixel to the newData array

                if newpix == None:
                    newData.append(item)

                # Here we take the values of newpix from the encode function
                # and sent it to hex2rgb function to restore their rgb values
                # and appends these values to RGBA format and increments the
                # digits value

                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1

            # When the digits variable exceeds the length of the binary message
            # we will simply append the remaining pixels to the item variable
            # until we reach the end of the datas variable for the entire image.

            else:
                newData.append(item)

        # After that loop is complete with storing data for each available
        # blue pixel we store the altered pixels in the newData variable
        # and saves the image in PNG format and display 'Completed!' to
        # the user

        img.putdata(newData)
        img.save(filename, "PNG")
        return "Completed!\n"

    # If the image is not in the correct mode it will display this error message
    # to inform the user why the encode function didn't work for them

    return "Incorrect Image Mode, Couldn't Hide"

def retr(filename, pixel_choice):

    # Assuming the user had used the encode function successfully
    # in the retrieve function we are openning the altered image
    # and storing it to the img variable

    img = Image.open(filename)
    binary = ''

    # Similar to the hide function we check to see if the image is
    # set in RGBA format

    if img.mode in ('RGBA'):

        # Here we convert the image to RGBA and store it in the img
        # variable and store the pixel values of the image in the
        # datas variable in a specific sequence to not alter the
        # appearance of the image.

        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:

            # In this part of the program we convert the pixels
            # to hexadecimal value and take the last value of
            # each pixel if it's either 0 or 1 and assign it to
            # the digit variable. If digit is assigned None we
            # move on to the next pixel. Given digit is assigned
            # 0 or 1 we add it to the binary variable for each
            # pixel throughout the image

            digit = decode(rgb2hex(item[0], item[1], item[2]), pixel_choice)
            if digit == None:
                pass
            else:

                # As we appended binary to each digit found
                # we will see if the last 16 elements of
                # binary is equal to 1111111111111110. If it
                # test is proven true we will print "Success"
                # to the user and send everything up until the
                # last 16 elements of binary to the bin2str
                # function

                binary = binary + digit
                if (binary[-16:] == '1111111111111110'):
                    print("Success!\n")
                    return bin2str(binary[:-16])

        return bin2str(binary)
    return "Incorrect Image Mode, couldn't retrieve message!\n"

def Main():

    # Here we setting up the options to encode/decode
    # messages using -e/-d respectively into an image

    parser = optparse.OptionParser('usage %prog ' +
                                   '<options> <target file>')
    parser.add_option('-e', dest='hide', type='string',
                      help='target picture path to hide text')
    parser.add_option('-d', dest='retr', type='string',
                      help='target picture path to retrieve text')

    # At this point we are setting up using the -e and -d
    # options for the hide.py as arguments for an image

    (options, args) = parser.parse_args()

    # Given a user enters the -e option the message and picture
    # will be sent to the hide function

    if (options.hide != None):
        print("Choose which type of pixel you want to hide your message in \n")
        print("1. Red\n2. Green\n3. Blue\n")
        pixel_choice = input("Please select the number of the pixel you wish to use: ")

        if pixel_choice.isdigit():
            pixel_choice = int(pixel_choice)

            if 1 <= pixel_choice <= 3:
                print("You choose option %d\n" % pixel_choice)

            else:
                print("You have entered an incorrect number. Please restart the program")
                sys.exit(0)

            text = input("Enter a message to hide: ")
            print(hide(options.hide, text, pixel_choice))

        else:
            print("You have entered an incorrect number. Please restart the program")
            sys.exit(0)

    # If the user enters the -d option the program will go the
    # retrieve function. Given the retr function was successful,
    # we will display the hidden message within the image

    elif (options.retr != None):
        print("Choose which type of pixel you choose previously to hide your message in \n")
        print("1. Red\n2. Green\n3. Blue\n")
        pixel_choice = input("Please select the number of the pixel you used : ")

        if pixel_choice.isdigit():
            pixel_choice = int(pixel_choice)

            if 1 <= pixel_choice <= 3:
                print("You choose option %d\n" % pixel_choice)

            else:
                print("You have entered an incorrect number. Please restart the program.")
                sys.exit(0)

            print(retr(options.retr, pixel_choice))

        else:
            print("You have entered an incorrect number. Please restart the program.")
            sys.exit(0)

    else:
        print(parser.usage)
        exit(0)

if __name__ == '__main__':
    Main()
