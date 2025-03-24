# 添加必要的import语句
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def save_images(url, folder,img_count):
    # 设置浏览器选项
    options = webdriver.ChromeOptions()
    options.headless = True  # 无头模式
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')  # 设置窗口大小

    # 初始化浏览器驱动
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

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
        time.sleep(1)

        # 保存全屏截图
        img_path = str(folder)+"_"+str(img_count)+".png"
        driver.save_screenshot(img_path)
        print(f'截图已保存为：{os.path.abspath(img_path)}')

    except Exception as e:
        print(f'截图失败：{str(e)}')
    finally:
        driver.quit()


# 使用示例





def save_reader_images(reader_id,quantities):
    hitomi_url = "https://hitomi.la/reader/"
    reader_url = ".html#"
    for img_count in range(quantities-1):
        save_images(hitomi_url+str(reader_id)+reader_url+str(img_count+1),folder=str(reader_id),img_count=img_count+1)
      # save_reader_images(3267993,451)
      # 如果有啥不理解的直接看代码
