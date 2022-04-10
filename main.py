import os


def main():
    os.system('python config.py')
    print("Configuration Completed")
    os.system('python interpreter.py')
    print("Interpreter Running")


if __name__ == '__main__':
    main()
