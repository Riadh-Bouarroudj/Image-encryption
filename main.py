import numpy as np
import imageio.v2 as imageio
import secrets
import cv2
import os
from Encryption import *
from Scrambling import *

def main():
    current_directory = os.path.dirname(__file__)
    img_path = os.path.join(current_directory, 'Images/Airplane.tiff')
    original_image = imageio.imread(img_path)

    """Encryption techniques"""
    #Logistic map
    encrypted_image=Logistic_map(original_image,r=3.99, x0=0.5)
    decrypted_image=Logistic_map(encrypted_image,r=3.99, x0=0.5)
    Display_images(original_image, encrypted_image, decrypted_image, 'Logistic map encryption')


    #Henon map
    encrypted_image=Henon_map(original_image,a=1.5, b=2.3)
    decrypted_image=Henon_map(encrypted_image,a=1.5, b=2.3)
    Display_images(original_image, encrypted_image, decrypted_image, 'Henon map encryption')


    #AES encryption
    key = secrets.token_bytes(16)         #Example key = b'1234567890128456'
    iv = secrets.token_bytes(16)
    #CBC mode provides better security compared to ECB mode
    encrypted_image=Encrypt_AES(original_image,key,'CBC',iv)
    decrypted_image=Decrypt_AES(encrypted_image,key,'CBC',iv)
    Display_images(original_image, encrypted_image, decrypted_image, 'AES encryption with CBC mode')

    encrypted_image=Encrypt_AES(original_image,key,'ECB')
    decrypted_image=Decrypt_AES(encrypted_image,key,'ECB')
    Display_images(original_image, encrypted_image, decrypted_image, 'AES encryption with ECB mode')


    """Scrambling techniques"""
    #Hyper chaotic chen system
    encrypted_image, permutation=Encrypt_chen_system(original_image, a=35, b=3, c=28, initial_state=[1.0, 1.0, 1.0], t=np.linspace(0, 100, original_image.shape[0]*original_image.shape[1]))
    decrypted_image=Decrypt_chen_system(encrypted_image, permutation)
    Display_images(original_image, encrypted_image, decrypted_image, 'Hyper chaotic chen system scrambling')


    #Arnold Transformation
    if original_image.shape[0]!=original_image.shape[0]:       #Arnold transformation works only with square images
        size=max(original_image.shape[0],original_image.shape[1])
        original_image=cv2.resize(original_image,(size,size))       
    encrypted_image=Encrypt_Arnold_transform(original_image, iterations=10)
    decrypted_image=Decrypt_Arnold_transform(encrypted_image, iterations=10)
    Display_images(original_image, encrypted_image, decrypted_image, 'Arnold transformation scrambling')

if __name__ == "__main__":
    main()