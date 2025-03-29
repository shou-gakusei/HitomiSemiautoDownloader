from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
import zipfile

def screenshot_compress(reader_id,quantities):
    with zipfile.ZipFile(reader_id,"w") as zipF:
        for screenshot_count in range(quantities):
            zipF.write(reader_id,os.path.basename(str(reader_id+"_"+str(screenshot_count+1)+".png")))

def save_images(url, folder,img_count,driver):
    # 先检测本地有没有这张图片
    while not os.path.exists("C:/Users/shou_gakusei/PycharmProjects/hitomidownloader/images/"+str(folder)+"_"+str(img_count)+".png"):
        print("opening page:"+url)
        img_path = "C:/Users/shou_gakusei/PycharmProjects/hitomidownloader/images/"+str(folder)+"_"+str(img_count)+".png"
        try:
            driver.get(url)
            # 等待页面加载完成（可根据需要调整等待时间）
            time.sleep(5)
            # 获取页面高度
            total_height = driver.execute_script("return document.body.scrollHeight")
            # 设置窗口大小以匹配页面高度
            driver.set_window_size(1920, total_height + 200)  # 留出滚动条空间
            # 滚动到页面顶部
            driver.execute_script("window.scrollTo(0, 0);")
            # 等待内容加载
            time.sleep(5)
            # 保存全屏截图
            driver.save_screenshot(img_path)
            print("\r"+f'截图已保存为：{os.path.abspath(img_path)}')
        except :
            print("你的网络有问题！换个节点！！！！")
            pass
    else:
        print("\r"+str(url)+"图片已存在")
        
def save_reader_images(reader_id,quantities):
    # 定义Hitomi.la的Reader页面URL
    hitomi_url = "https://hitomi.la/reader/"
    reader_url = ".html#"
    img_count = 0
    # 初始化浏览器驱动
    # 配置Chrome浏览器选项
    options = Options()
    options.headless = True  # 启用无头模式（后台运行）
    options.add_argument('--disable-gpu')  # 禁用GPU加速（某些环境下需要）
    options.add_argument('--window-size=1920,1080')  # 设置浏览器窗口大小
    chrome_driver_path = "chromedriver-win64/chromedriver.exe" #指定本地chromedriver路径
    # 创建Service对象并指定ChromeDriver路径
    service = Service(executable_path=chrome_driver_path)
    # 启动Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)
    while img_count < quantities:
        # 这里没想到什么好主意用for遍历
        img_count+=1
        try:
            print("\r"+"downloading image:"+str(img_count))
            save_images(hitomi_url+str(reader_id)+reader_url+str(img_count),folder=str(reader_id),img_count=img_count+1,driver=driver)
        except:
            img_count -= 1
            pass
    driver.quit()


# 测试用
image_series_list = ["3278803.html#960", "3267537.html#1445", "3269200.html#255", "3257320.html#865"]
save_reader_images(3269200,255)
