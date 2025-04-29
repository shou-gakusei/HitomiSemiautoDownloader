# HitomiDownloader
automatically download images from hitomi.la without annoying downloading procedure
# features may add in next few versions
多线程（对网速有超级高要求） 自动压缩打包 
# Read before use  
先下载chormedriver到项目文件夹内并解压
[chormedriver官方下载网址](https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/win64/chromedriver-win64.zip)  
# 已完成/重构的部分
类断点续传 使用了本地的chormedriver并重构了driver相关的代码优化了一部分性能  
顺手做了本地保存之后对图片编号的格式化（手机看起来更方便了）  
自动检测/下载chormedriver 下好自动压缩（密码默认114514）
# 目前已知的问题与解决方案
网络环境不稳定导致获得的截图全是黑屏  
解决方案：尽量找靠谱的科学上网节点+调高里面time.sleep()里的数值
# 画饼：  
黑屏的问题后面想办法用pyautogui解决  
其他功能
