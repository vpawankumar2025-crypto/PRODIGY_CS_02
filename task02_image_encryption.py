"""
Task-02: Pixel Manipulation for Image Encryption
Encrypts and decrypts images by applying XOR operation on pixel values using a key.
Supports both swapping and XOR-based encryption.

Requirements:
    pip install Pillow numpy
"""

import numpy as np
from PIL import Image
import os


def xor_encrypt_decrypt(image_path, key, output_path):
    """
    Encrypt or decrypt an image using XOR pixel manipulation.
    XOR is its own inverse: applying it twice restores the original.
    
    Args:
        image_path (str): Path to the input image
        key (int): Integer key (0-255) for XOR operation
        output_path (str): Path to save the output image
    """
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img, dtype=np.uint8)

    # XOR every pixel channel with the key
    encrypted_array = img_array ^ key

    encrypted_img = Image.fromarray(encrypted_array.astype(np.uint8))
    encrypted_img.save(output_path)
    print(f"✅ Image saved to: {output_path}")


def swap_encrypt(image_path, output_path, seed=42):
    """
    Encrypt an image by randomly swapping pixel positions.
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the encrypted image
        seed (int): Random seed for reproducibility
    """
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img, dtype=np.uint8)
    flat = img_array.reshape(-1, 3).copy()

    rng = np.random.default_rng(seed)
    indices = np.arange(len(flat))
    rng.shuffle(indices)

    shuffled = flat[indices]
    encrypted_array = shuffled.reshape(img_array.shape)

    encrypted_img = Image.fromarray(encrypted_array.astype(np.uint8))
    encrypted_img.save(output_path)
    print(f"✅ Swap-encrypted image saved to: {output_path}")
    return indices  # Return indices needed for decryption


def swap_decrypt(image_path, output_path, indices):
    """
    Decrypt a swap-encrypted image by reversing the pixel shuffle.
    
    Args:
        image_path (str): Path to the encrypted image
        output_path (str): Path to save the decrypted image
        indices (np.array): The original shuffle indices used during encryption
    """
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img, dtype=np.uint8)
    flat = img_array.reshape(-1, 3).copy()

    # Reverse the shuffle
    reverse_indices = np.argsort(indices)
    original = flat[reverse_indices]
    decrypted_array = original.reshape(img_array.shape)

    decrypted_img = Image.fromarray(decrypted_array.astype(np.uint8))
    decrypted_img.save(output_path)
    print(f"✅ Swap-decrypted image saved to: {output_path}")


def main():
    print("=" * 50)
    print("   Pixel Manipulation Image Encryption Tool")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. XOR Encrypt/Decrypt an image")
        print("  2. Swap Encrypt an image")
        print("  3. Swap Decrypt an image")
        print("  4. Exit")

        choice = input("\nEnter your choice (1/2/3/4): ").strip()

        if choice == '1':
            path = input("Enter the image path: ").strip()
            if not os.path.exists(path):
                print("❌ File not found.")
                continue
            try:
                key = int(input("Enter XOR key (0-255): ").strip())
                if not (0 <= key <= 255):
                    print("Key must be between 0 and 255.")
                    continue
            except ValueError:
                print("Invalid key.")
                continue
            output = input("Enter output image path (e.g., output.png): ").strip()
            xor_encrypt_decrypt(path, key, output)

        elif choice == '2':
            path = input("Enter the image path: ").strip()
            if not os.path.exists(path):
                print("❌ File not found.")
                continue
            output = input("Enter output image path (e.g., encrypted.png): ").strip()
            try:
                seed = int(input("Enter a numeric seed (e.g., 42): ").strip())
            except ValueError:
                seed = 42
            global _swap_indices
            _swap_indices = swap_encrypt(path, output, seed=seed)
            print("⚠️  Remember your seed to decrypt later!")

        elif choice == '3':
            path = input("Enter the encrypted image path: ").strip()
            if not os.path.exists(path):
                print("❌ File not found.")
                continue
            output = input("Enter output image path (e.g., decrypted.png): ").strip()
            if '_swap_indices' not in globals():
                print("❌ No swap indices found in current session. Use XOR decrypt or restart with the same seed.")
                continue
            swap_decrypt(path, output, _swap_indices)

        elif choice == '4':
            print("\nGoodbye! 👋")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
