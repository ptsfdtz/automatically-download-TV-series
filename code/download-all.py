import os
import requests
from tqdm import tqdm
import zipfile

def download_file(url, path, filename):
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        full_path = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path)
        
        print(f"Downloading {full_path}")
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 
        with open(full_path, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                bar.update(len(data))
                file.write(data)
                
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def replace_last_digit(url, replacement):
    last_digit_index = url.rfind('1')
    if last_digit_index != -1:
        modified_url = url[:last_digit_index] + str(replacement) + url[last_digit_index + 1:]
        return modified_url
    else:
        return url

def zip_folder(folder_path, zip_path):
    print("Zipping...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def main():
    user_input = input("视频集数,链接,存储路径,压缩（用逗号分隔）: ")
    values = user_input.split(',')

    total = int(values[0]) + 1
    original_url = values[1]
    base_path = values[2]
    selection = values[3]

    download_folder = os.path.join(base_path, 'downloaded_files')

    for replacement_digit in range(1, total):
        modified_url = replace_last_digit(original_url, replacement_digit)
        destination_file = f"downloaded_file_{replacement_digit}.mp4"
        download_file(modified_url, download_folder, destination_file)
        print(f"File downloaded: {destination_file}")

    if selection.lower() == 'yes':
        zip_file_path = os.path.join(base_path, 'downloaded_files.zip')
        zip_folder(download_folder, zip_file_path)
        print(f"All files downloaded and zipped to: {zip_file_path}")

if __name__ == "__main__":
    main()
