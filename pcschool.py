import os
import requests
from tqdm import tqdm  # 進度條套件

# 禁用不安全请求警告
# requests.packages.urllib3.disable_warnings()

# 資料夾名稱和保存路徑
folder_name = input("請輸入資料夾名稱：")
desktop_path = os.path.expanduser(r"~\Desktop")
save_folder = os.path.join(desktop_path, folder_name)

# 嘗試創建資料夾，如果已存在則顯示提示訊息並結束指令
try:
    os.makedirs(save_folder)
except FileExistsError:
    print("資料夾已存在，請重新選擇資料夾名稱！")
    exit()

# 讓用戶選擇是要下載單一影片還是多個影片
download_mode = input("請選擇下載模式（單一影片/多個影片）：").strip().lower()

if download_mode == "單一影片":
    index = 1
    while True:
        video_name = f"第{index}部錄影檔.mp4"
        save_path = os.path.join(save_folder, video_name)
        
        if not os.path.exists(save_path):
            break
            
        index += 1
    
    video_url = input("請輸入巨匠直播錄影檔連結: ")
    response = requests.get(video_url, verify=False, stream=True)  # 加入 stream=True 參數
    
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        
        with open(save_path, "wb") as f, tqdm(
            desc=video_name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                pbar.update(len(data))
        
        print("影片已成功下載")
    else:
        print("無法下載影片，請再試一次！")

elif download_mode == "多個影片":
    num_videos = int(input("請輸入總共幾部影片: "))
    existing_videos = len([name for name in os.listdir(save_folder) if name.endswith(".mp4")])
    
    for index in range(1, num_videos + 1):
        video_name = f"第{existing_videos + index}部錄影檔.mp4"
        save_path = os.path.join(save_folder, video_name)
        
        video_url = input(f"請輸入要下載的第{index}部影片連結: ")
        response = requests.get(video_url, verify=False, stream=True)  # 加入 stream=True 參數
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            
            with open(save_path, "wb") as f, tqdm(
                desc=video_name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))
            
            print(f"要下載的第{index}部影片已成功下載")
        else:
            print(f"要下載的第{index}部影片無法下載")
else:
    print("無效的選擇，請再試一次！")