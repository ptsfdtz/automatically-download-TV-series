import os
import requests
from tqdm import tqdm

user_input = input("视频集数,链接,存储路径（用逗号分隔）: ")
values = user_input.split(',')

total = int(values[0])
original_url = values[1]
path = values[2]

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

for replacement_digit in range(1, total):
    modified_url = replace_last_digit(original_url, replacement_digit)
    destination_file = f"downloaded_file_{replacement_digit}.mp4"
    download_file(modified_url, path, destination_file)
    print(f"File downloaded: {destination_file}")
