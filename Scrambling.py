import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def chen_system(state, t, a, b, c):
    x, y, z = state
    return [a*(y - x), (c - a)*x - x*z + c*y, x*y - b*z]

def Encrypt_chen_system(imagex, a, b, c, initial_state, t):
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
        flat_image = img.flatten()
        solution = odeint(chen_system, initial_state, t, args=(a, b, c))
        permutation = np.argsort(solution[:, 0] % len(flat_image))
        scrambled_image = flat_image[permutation]
        scrambled_image=scrambled_image.reshape(img.shape)
        if long==3:
            image[:,:,channel]=np.copy(scrambled_image)
        else:
            image=scrambled_image
    return image, permutation

def Decrypt_chen_system(imagex, permutation):
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
        flat_image = img.flatten()
        inverse_permutation = np.argsort(permutation)
        descrambled_image = flat_image[inverse_permutation]
        descrambled_image=descrambled_image.reshape(img.shape)
        if long==3:
            image[:,:,channel]=np.copy(descrambled_image)
        else:
            image=descrambled_image
    return image


#Arnold transformation is designed to work only with square image
def Encrypt_Arnold_transform(imagex, iterations):
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
        n, m = img.shape
        transformed_image = np.array(img, copy=True)
        
        for _ in range(iterations):
            new_image = np.zeros((n, m), dtype="uint8")
            for x in range(n):
                for y in range(m):
                    new_image[(2*x + y) % n][(x + y) % m] = transformed_image[x][y]
            transformed_image = new_image
        if long==3:
            image[:,:,channel]=transformed_image
        else:
            image=transformed_image
    return(image)

def Decrypt_Arnold_transform(imagex, iterations):
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
        n, m = img.shape
        transformed_image = np.array(img, copy=True)
        
        for _ in range(iterations):
            new_image = np.zeros((n, m), dtype="uint8")
            for x in range(n):
                for y in range(m):
                    new_image[x][y] = transformed_image[(2*x + y) % n][(x + y) % m]
            transformed_image = new_image
        if long==3:
            image[:,:,channel]=transformed_image
        else:
            image=transformed_image
    return(image)


def Display_images(original_image, encrypted_image, decrypted_image,Title):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ax1.imshow(original_image, cmap='gray')
    ax1.set_title('Original image')
    ax2.imshow(encrypted_image, cmap='gray')
    ax2.set_title('Encrypted image')
    ax3.imshow(decrypted_image, cmap='gray')
    ax3.set_title('Decrypted image')
    fig.suptitle(Title, fontsize=16, y=0.88)
    print("Are the original and decrypted images similar ?",np.array_equal(original_image, decrypted_image))
    plt.show()