from main import main

def test():
    strings = ["0123456789", "AaBbCc", "79266203962", "Hello, World!"]
    shifts = [2, 3, 5, 1]
    for i in range(4):
        print(f"Test case {i+1}:")
        print(f"--- Encrypt '{strings[i]}' with shift {shifts[i]}")
        encrypted_string = main(['','e', strings[i], shifts[i]])
        print(f"--- Result: {encrypted_string}")
        print(f"--- Decrypt '{encrypted_string}' with shift {shifts[i]}")
        decrypted_string = main(['','d', encrypted_string, shifts[i]])
        print(f"--- Result: {decrypted_string}")
        print(f"--- Assert: {strings[i]==decrypted_string}")
        print()



if __name__ == "__main__":
    test()