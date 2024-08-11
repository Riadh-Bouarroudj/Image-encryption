import numpy as np
from Crypto.Cipher import AES


def Logistic_map(imagex, r, x0):
    image=np.copy(imagex)
    if len((np.asarray(image)).shape)==3: 
        long=3
    else: 
        long=1

    for channel in range (long):
        if long==3:
            img=image[:,:,channel]
        else:
            img=image
        x = x0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                x = r * x * (1 - x)
                img[i, j] = int(255 * x) ^ img[i, j]
        if long==3:
            image[:,:,channel]=img
        else:
            image=img
    return image


def Henon_map(imagex, a, b):
    image=np.copy(imagex)
    if len((np.asarray(image)).shape)==3: 
        long=3
    else: 
        long=1

    for channel in range (long):
        if long==3:
            img=image[:,:,channel]
        else:
            img=image
        height, width = img.shape
        x=a; y=b
        for i in range(height):
            for j in range(width):
                x = 1 - a * x**2 +  y
                y = b *x
                img[i, j] = img[i, j] ^ int(x * 255)
        if long==3:
            image[:,:,channel]=img
        else:
            image=img
    return image


def Encrypt_AES(imagex, key, mode, iv=None):  #CBC mode provides better security compared to ECB mode
    image=np.copy(imagex)
    if len((np.asarray(image)).shape)==3: long=3
    else: long=1

    for channel in range (long):
        if long==3:
            img=image[:,:,channel]
        else:
            img=image
        if mode=="CBC":
            cipher = AES.new(key, AES.MODE_CBC, iv)
        elif mode=="ECB":
            cipher = AES.new(key, AES.MODE_ECB)
        else:
            raise ValueError("Choose either 'CBC' or 'ECB' mode")
        img_data = img.flatten()
        img_bytes=img_data.tobytes()
        ciphertext = cipher.encrypt(img_bytes)
        encrypted_data = np.frombuffer(ciphertext, dtype=np.uint8)
        encrypted_img = encrypted_data.reshape(img.shape)
        if long==3:
            image[:,:,channel]=encrypted_img
        else:
            image=encrypted_img
    return(image)

def Decrypt_AES(imagex, key, mode, iv=None):
    image=np.copy(imagex)
    if len((np.asarray(image)).shape)==3:
        long=3
    else:
        long=1

    for channel in range (long):
        if long==3:
            img=image[:,:,channel]
        else:
            img=image   
        if mode=="CBC":
            cipher = AES.new(key, AES.MODE_CBC, iv)
        elif mode=="ECB":
            cipher = AES.new(key, AES.MODE_ECB)
        else:
            raise ValueError("Choose either CBC or ECB mode")
        decrypted_img_bytes = img.flatten()
        decrypted_img_bytes=decrypted_img_bytes.tobytes()
        decrypted_data = cipher.decrypt(decrypted_img_bytes)
        decrypted_data = np.frombuffer(decrypted_data, dtype=np.uint8)
        decrypted_img = decrypted_data.reshape(img.shape)
        if long==3:
            image[:,:,channel]=decrypted_img
        else:
            image=decrypted_img
    return(image)

