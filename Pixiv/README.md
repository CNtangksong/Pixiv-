# Pixiv批量爬取图片

[pixiv类镜像站](https://pixivic.com)  
如果只是想随意看下图片，那么这个网站已经可以满足大部分需求了

##如何使用
1.使用git 命令克隆项目到本地，配置电脑和文件所需要的环境(本人使用python3.8,文件需要的  pip install 下载即可)  
2.运行down_img.py文件，根据画师图片或id进行批量爬取

  
##为什么有这个项目
本次爬取的网站对显示图片和画师有一定的限制，无法直接在网站中浏览，并且网站加载图片十分缓慢。  
但网站本质是反代理，可以通过api即可准确查找对应图片在pixiv的地址，进而通过地址的拼接更换成其他更快速的网址进行访问和爬取

##关于我本人
本人大二学生，第一次写爬虫，对很多知识点及技术的运用并不是很熟练，大佬轻喷。如果有一些更好的想法可以告知我，共同学习  

如果项目对您有帮助，希望各位大大能给个star  :)


