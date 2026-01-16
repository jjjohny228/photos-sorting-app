import os

def count_files(file_path):
    print(len(os.listdir(file_path)))


if __name__ == '__main__':
    count_files('full_dataset')
