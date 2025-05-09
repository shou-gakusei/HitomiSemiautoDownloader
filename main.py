# 添加必要的import语句
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib import request
import time
import os
import zipfile
from pathlib import Path

def delete_files(directory):
    file_list = os.listdir(directory)
    for file in file_list:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def create_folder_pathlib(folder_path):
    path = Path(folder_path)
    try:
        path.mkdir(parents=True, exist_ok=True)  
        # parents=True 允许递归创建，exist_ok=True 避免存在时报错
        print(f"文件夹已创建: {folder_path}",end="")
    except Exception as e:
        print(f"创建失败: {e}",end="")

def screenshot_compress(reader_id: str, quantities: int):
    with zipfile.ZipFile(file="zips_p2sw0rd_114514/"+reader_id+".zip", mode="w") as zipF:
        zipF.setpassword(b'114514')
        for screenshot_count in range(0,quantities):
            zipF.write("images/"+reader_id+"_"+str(screenshot_count+1)+".png", os.path.basename(str(reader_id + "_" + str(screenshot_count + 1) + ".png")))
            print("\rzipped image:"+"images/"+reader_id+"_"+str(screenshot_count+1)+".png",end="")
        zipF.close()

def img_name_formating(num,length):
    # 这里得点名感谢一下安卓的智障文件排序算法
    num_digit = len(str(num))
    if num_digit<length:
        str_zero_counts = length-num_digit
        str_output = "0"*str_zero_counts+str(num)
    else:
        str_output = str(num)
    return str_output


def save_images(url, folder, img_count, driver, sleep_time,quantities):
    # 设置浏览器选项
    img_count_length = len(str(quantities))
    img_count_formatted = img_name_formating(num=img_count, length=img_count_length)
    while not os.path.exists("images/" + str(folder) + "_" + img_count_formatted + ".png"):
        # 初始化浏览器驱动
        try:
            driver.get(url)
            print("\ropening page:" + url,end="")
            # 等待页面加载完成（可根据需要调整等待时间）
            time.sleep(sleep_time)
            # 获取页面高度
            total_height = driver.execute_script("return document.body.scrollHeight")
            # 设置窗口大小以匹配页面高度
            driver.set_window_size(1920, total_height + 200)  # 留出滚动条空间
            # 滚动到页面顶部
            driver.execute_script("window.scrollTo(0, 0);")
            # 等待内容加载
            time.sleep(sleep_time)
            # 保存全屏截图
            img_path = "images/" + str(folder) + "_" + img_count_formatted + ".png"
            driver.save_screenshot(os.path.abspath(img_path))
            print("\r" + f'截图已保存为：{os.path.abspath(img_path)}',end="")
        except:
            print("你的网络有问题！换个节点！！！！",end="")
            pass
    else:
        print("\r" + str(url) + "图片已存在",end="")

def save_reader_images(reader_id, quantities, mode):
    # 用例
    # save_reader_images(3257320,865,"下载")
    # save_reader_images(3257320,865,"缺失图片补齐")

    if mode == "下载":
        sleep_time = 5
    else:
        sleep_time = 7.5
    # 定义Hitomi.la的Reader页面URL
    hitomi_url = "https://hitomi.la/reader/"
    reader_url = ".html#"
    img_count = 0
    # 配置Chrome浏览器选项
    options = Options()
    options.headless = True  # 启用无头模式（后台运行）
    options.add_argument('--disable-gpu')  # 禁用GPU加速（某些环境下需要）
    options.add_argument('--window-size=1920,1080')  # 设置浏览器窗口大小
    chrome_driver_path = "chromedriver-win64/chromedriver.exe"  #指定本地chromedriver路径
    # 创建Service对象并指定ChromeDriver路径
    service = Service(executable_path=chrome_driver_path)
    # 启动Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(hitomi_url + str(reader_id) + reader_url + "1")
    time.sleep(sleep_time)
    while img_count < quantities:
        img_count += 1
        try:
            print("\r" + "downloading image:" + str(img_count),end="")
            save_images(hitomi_url + str(reader_id) + reader_url + str(img_count),
                        folder=str(reader_id), img_count=img_count,
                        driver=driver, sleep_time=sleep_time,quantities=quantities)
        except:
            pass
    driver.quit()

def download_file_urllib(download_url, save_path):
    try:
        request.urlretrieve(download_url, save_path)
        print(f"文件已下载到 {save_path}",end="")
    except Exception as e:
        print(f"下载失败: {e}",end="")

def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"文件已解压到 {extract_to}",end="")
    except Exception as e:
        print(f"解压失败: {e}",end="")

def download_gallery_images(url_input):
    # NOT RECOMMENDED
    list_url_split = url_input.split("/")
    for splits in list_url_split:
        if ".html#" in splits:
            hitomi_gallery_id, hitomi_gallery_count = splits.split(".html#")
    hitomi_gallery_id = int(hitomi_gallery_id)
    hitomi_gallery_count = int(hitomi_gallery_count)
    save_reader_images(hitomi_gallery_id, hitomi_gallery_count, "下载")
    screenshot_compress(reader_id=str(hitomi_gallery_id), quantities=hitomi_gallery_count)
    delete_files("images")

# 先检查driver是否安装
create_folder_pathlib("chromedriver-win64")
create_folder_pathlib("temp")
if not os.path.exists("chromedriver-win64/chromedriver.exe"):
    download_file_urllib(
        "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/win64/chromedriver-win64.zip",
        "temp/chromedriver-win64.zip")
    unzip_file("temp/chromedriver-win64.zip", "hitomidownloader")







# 测试用例
'''
gallery_list = [
    "https://hitomi.la/reader/3329775.html#2000",
    "https://hitomi.la/reader/3328352.html#475",
    "https://hitomi.la/reader/3328768.html#249",
    "https://hitomi.la/reader/3329041.html#189",
    "https://hitomi.la/reader/3326723.html#194",
    "https://hitomi.la/reader/3326640.html#589",
    "https://hitomi.la/reader/3327301.html#177",
    "https://hitomi.la/reader/3327241.html#103",
    "https://hitomi.la/reader/3327910.html#1509",
    "https://hitomi.la/reader/3328072.html#313",
    "https://hitomi.la/reader/3331765.html#1404",
    "https://hitomi.la/reader/2629813.html#153",
    "https://hitomi.la/reader/3331841.html#799",
    "https://hitomi.la/reader/3331970.html#269",
    "https://hitomi.la/reader/3332193.html#620",
    "https://hitomi.la/reader/3330952.html#356",
    "https://hitomi.la/reader/3332721.html#175"]
for gallery_url in gallery_list:
    download_gallery_images(gallery_url)
'''
