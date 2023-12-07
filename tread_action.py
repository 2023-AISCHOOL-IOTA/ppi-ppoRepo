import os
from multiprocessing import Process

def process_file(file_name):
    print(f"Processing {file_name}")
    os.system(f"python3 {file_name}")  # 파일 실행
    print(f"Finished processing {file_name}")

if __name__ == "__main__":
    file_names = ['/home/pi/project/request.py','/home/pi/project/flask_command.py', '/home/pi/project/button_control.py', '/home/pi/project/arduino_serial.py']
    processes = []

    for file_name in file_names:
        proc = Process(target=process_file, args=(file_name,))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    print("All files have been processed.")
    
#'/home/pi/project/arduino_serial.py'