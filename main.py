# 添加必要的import语句
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib import request
import time
import os
import zipfile
from pathlib import Path


def create_folder_pathlib(folder_path):
    path = Path(folder_path)
    try:
        path.mkdir(parents=True, exist_ok=True)  # parents=True 允许递归创建，exist_ok=True 避免存在时报错
        print(f"文件夹已创建: {folder_path}")
    except Exception as e:
        print(f"创建失败: {e}")


def screenshot_compress(reader_id: str, quantities: int):
    with zipfile.ZipFile(file="zips_p2sw0rd_114514/"+reader_id, mode="w") as zipF:
        for screenshot_count in range(quantities):
            zipF.write(reader_id, os.path.basename(str(reader_id + "_" + str(screenshot_count + 1) + ".png")))
    zipF.setpassword(b'114514')
    zipF.close()

def save_images(url, folder, img_count, driver, sleep_time):
    # 设置浏览器选项
    while not os.path.exists("images/" + str(folder) + "_" + str(img_count) + ".png"):
        # 初始化浏览器驱动
        try:
            driver.get(url)
            print("\ropening page:" + url)
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
            img_path = "images/" + str(folder) + "_" + str(img_count) + ".png"
            driver.save_screenshot(os.path.abspath(img_path))
            print("\r" + f'截图已保存为：{os.path.abspath(img_path)}')
        except:
            print("你的网络有问题！换个节点！！！！")
            pass
    else:
        print("\r" + str(url) + "图片已存在")


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
            print("\r" + "downloading image:" + str(img_count))
            save_images(hitomi_url + str(reader_id) + reader_url + str(img_count),
                        folder=str(reader_id), img_count=img_count,
                        driver=driver, sleep_time=sleep_time)
        except:
            img_count -= 1
            pass
    driver.quit()


def download_file_urllib(download_url, save_path):
    try:
        request.urlretrieve(download_url, save_path)
        print(f"文件已下载到 {save_path}")
    except Exception as e:
        print(f"下载失败: {e}")


def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"文件已解压到 {extract_to}")
    except Exception as e:
        print(f"解压失败: {e}")


# 先检查driver是否安装
create_folder_pathlib("chromedriver-win64")
create_folder_pathlib("temp")
if not os.path.exists("chromedriver-win64/chromedriver.exe"):
    download_file_urllib(
        "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/win64/chromedriver-win64.zip",
        "temp/chromedriver-win64.zip")
    unzip_file("temp/chromedriver-win64.zip", "hitomidownloader")

image_series_list = ["3278803.html#960", "3267537.html#1445", "3269200.html#255", "3257320.html#865"]


# 示例用法
def download_gallery_images(url_input):
    # 不打算写类型检查
    # example_url:https://hitomi.la/reader/1588234.html#90
    list_url_split = url_input.split("/")
    for splits in list_url_split:
        if ".html#" in splits:
            hitomi_gallery_id, hitomi_gallery_count = splits.split(".html#")
    hitomi_gallery_id = int(hitomi_gallery_id)
    hitomi_gallery_count = int(hitomi_gallery_count)
    save_reader_images(hitomi_gallery_id, hitomi_gallery_count, "下载")
    save_reader_images(hitomi_gallery_id, hitomi_gallery_count, "缺失图片补齐")
    screenshot_compress(reader_id=str(hitomi_gallery_id), quantities=hitomi_gallery_count)
    os.removedirs("images")



'''
测试用例
gallery_list = [
    "https://hitomi.la/reader/1588234.html#90" ,"https://hitomi.la/reader/3309782.html#234",
    "https://hitomi.la/reader/3029387.html#208","https://hitomi.la/reader/3029387.html#208",
    "https://hitomi.la/reader/3292388.html#974","https://hitomi.la/reader/3323377.html#195",]
for gallery_url in gallery_list:
    download_gallery_images(gallery_url)
'''
