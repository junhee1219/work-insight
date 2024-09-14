from datetime import datetime
import os
import shutil

def create_folder(path):
    # 폴더가 이미 있으면 삭제
    if os.path.exists(path):
        shutil.rmtree(path)
    # 새로운 폴더 생성
    os.makedirs(path)

def generate_unique_foldername(client_requests):
    client_ip = client_requests.remote_addr

    # 현재 시각 가져오기 (YYYYMMDD_HHMMSS 형식으로)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S') + f"_{datetime.now().microsecond}"

    # 폴더 이름: IP주소_현재시각
    folder_name = f"{client_ip}_{current_time}"

    return folder_name



def make_zip(folder_path, output_filename):
    # shutil.make_archive(파일명, 압축 형식, 압축할 폴더 경로) : 확장자없이쓰면됨
    shutil.make_archive(output_filename, 'zip', folder_path)
    return output_filename+".zip"

def del_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)