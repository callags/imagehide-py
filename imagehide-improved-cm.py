import PIL as pillow
from PIL import Image
import binascii
import optparse
import sys
from os import path

DELIMITTER = '1111111111111110'
SUB_DELIMITTER = '1110111011101110'

def pixel():

    print("1. Red\n2. Green\n3. Blue\n")
    pixel_choice = input("Pixel: ")

    red = 1
    green = 2
    blue = 3

    if pixel_choice.isdigit():
        pixel_choice = int(pixel_choice)

        if 1 <= pixel_choice <= 3:
            print()
            if pixel_choice == blue:
                print("You choose the blue pixels!")
                return pixel_choice
            elif pixel_choice == green:
                print("You choose the green pixels!")
                return pixel_choice
            elif pixel_choice == red:
                print("You choose the red pixels!")
                return pixel_choice

        else:
            print("\nYou have entered an incorrect number. Please restart the program\n")
            sys.exit(0)

    else:
        print("\nYou have entered an incorrect character. Please restart the program\n")
        sys.exit(0)

def rgb2hex(r, g, b):

    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):

    hex_values = hexcode.lstrip('#')
    rgb_values = tuple(int(hex_values[i:i+2], 16) for i in (0, 2, 4))
    return rgb_values[0], rgb_values[1], rgb_values[2]

def str2bin(message):

    message = str(message)
    binary_array = [bin(ord(x))[2:].zfill(8) for x in message]
    binary_message = ""
    element = 0
    while element < len(binary_array):
        binary_message += binary_array[int(element)]
        element += 1
    return binary_message

def bin2str(binary):
    message = binascii.unhexlify('%x' % (int('0b'+binary, 2)))
    message = (str(message).lstrip('b').replace("'", "").strip('"'))
    return message
        
        

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

def decode(hexcode, pixel_choice):

    blue = 3
    green = 2
    red = 1

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

def hide(filename, user_input, pixel_choice, filename_binary):
    
    if filename_binary == None:
        binary = str2bin(user_input) + DELIMITTER
    else:
        binary = user_input + DELIMITTER + filename_binary + SUB_DELIMITTER
        
    img = Image.open(filename)
        
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        digit = 0
        temp = ''
        for item in datas:
            if (digit < len(binary)):

                newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit], pixel_choice)

                if newpix == None:
                    newData.append(item)

                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1

            else:
                newData.append(item)

        img.putdata(newData)
        img.save(filename, "PNG")
        return "\nCompleted!\n"

    return "Error, couldn't embed your input into the image!\n"

def retr(filename, pixel_choice, retrieve):

    img = Image.open(filename)
    binary = ''
    
    text = 1
    file = 2

    if img.mode in ('RGBA'):

        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:

            digit = decode(rgb2hex(item[0], item[1], item[2]), pixel_choice)
            if digit == None:
                pass
            else:
                binary = binary + digit

                if retrieve == text:
                    if (binary[-16:] == DELIMITTER):
                        print("\nSuccess!\n")
                        return bin2str(binary[:-16])
                
                elif retrieve == file:
                    if (binary[-16:] == SUB_DELIMITTER):
                        start = binary.find(DELIMITTER) + len(DELIMITTER)
                        end = binary.find(SUB_DELIMITTER)
                        filename_binary = binary[start:end]
                        filename = bin2str(filename_binary)
                        file_index = len(DELIMITTER) + len(SUB_DELIMITTER) + len(filename_binary)
                        file_content = (bin2str(binary[:-(file_index)])).split('\\n')
                        with open(filename, "w") as out:
                            for line in file_content:
                                print(line, file=out)
                        #sys.exit(0)
                        return "\nSuccess!\n"
                       
                        
    return "Error, couldn't retrieve your hidden input!\n"

def Main():

    # Here we setting up the options to encode/decode
    # messages using -e/-d respectively into an image

    parser = optparse.OptionParser('usage %prog ' +
                                   '<options> <target file>')
    parser.add_option('-e', dest='hide', type='string',
                      help='target picture path to hide text')
    parser.add_option('-d', dest='retr', type='string',
                      help='target picture path to retrieve text')
    parser.add_option('-f', dest='embed', 
                      help='target file path to hide in image')
    parser.add_option('-g', dest='file_retr',
                      help='target image to retrieve file from')

    # At this point we are setting up using the -e and -d
    # options for the hide.py as arguments for an image

    (options, args) = parser.parse_args()

    if (options.hide != None):
        print("\nPlease enter a message that you would like to hide in your image!\n")
        text = input("Message: ")
        
        print("\nChoose which type of pixel you want to hide your message in \n")
        pixel_choice = pixel()
        
        if pixel_choice:
            print(hide(options.hide, text, pixel_choice, None))

    elif (options.retr != None):
        print("Choose which type of pixel you choose previously to hide your message in \n")
        pixel_choice = pixel()
        retrieve = 1
        
        if pixel_choice:
            print(retr(options.retr, pixel_choice, retrieve))

    elif (options.embed):

       print("\nPlease enter the fullname of the file that you wish to embed into your image with.")
       print("If your file is in another directory that you're running this program from, please " \
             "include the full path.")
       print("\nBe careful to not enter empty space down below.\n")

       infile = input("Enter file name: ")

       if path.exists(infile):
           
           with open(infile, 'r') as out:
                    message = out.read()
           
           binary_message = str2bin(message)
           filename_binary = str2bin(infile)

           print("\nChoose which type of pixel you want to hide your file in.\n")
           pixel_choice = pixel()
           
           if pixel_choice:
               print(hide(options.embed, binary_message, pixel_choice, filename_binary))

       else:
           print("\nThis is not a valid file. Please check the filename or directory path and restart the program.\n")
          
    elif(options.file_retr):

       print("\nPlease select the pixel you hide your file within your image\n")
       pixel_choice = pixel()
       retrieve = 2
       
       if pixel_choice:
           print(retr(options.file_retr, pixel_choice, retrieve))

    else:
        print(parser.usage)
        exit(0)

if __name__ == '__main__':
    Main()
