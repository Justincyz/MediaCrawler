import asyncio
import sys

import cmd_arg
import config
import db
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from tkinter import ttk, messagebox
import tkinter as tk
from tools.utils import str2bool

# class CrawlerFactory:
#     CRAWLERS = {
#         "xhs": XiaoHongShuCrawler,
#         "dy": DouYinCrawler,
#         "ks": KuaishouCrawler,
#         "bili": BilibiliCrawler,
#         "wb": WeiboCrawler,
#         "tieba": TieBaCrawler
#     }

#     @staticmethod
#     def create_crawler(platform: str) -> AbstractCrawler:
#         crawler_class = CrawlerFactory.CRAWLERS.get(platform)
#         if not crawler_class:
#             raise ValueError("Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
#         return crawler_class()


# async def main():
#     # parse cmd
#     await cmd_arg.parse_cmd()

#     # init db
#     if config.SAVE_DATA_OPTION == "db":
#         await db.init_db()

#     crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
#     await crawler.start()

#     if config.SAVE_DATA_OPTION == "db":
#         await db.close()


# if __name__ == '__main__':
#     try:
#         # asyncio.run(main())
#         asyncio.get_event_loop().run_until_complete(main())
#     except KeyboardInterrupt:
#         sys.exit()


# import asyncio
# import tkinter as tk
# from tkinter import ttk, messagebox
# import config
# from tools.utils import str2bool
# from media_platform.bilibili import BilibiliCrawler
# from media_platform.douyin import DouYinCrawler
# from media_platform.kuaishou import KuaishouCrawler
# from media_platform.tieba import TieBaCrawler
# from media_platform.weibo import WeiboCrawler
# from media_platform.xhs import XiaoHongShuCrawler
# import db

class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        "bili": BilibiliCrawler,
        "wb": WeiboCrawler,
        "tieba": TieBaCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError("Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
        return crawler_class()

async def run_crawler():
    try:
        # 初始化数据库
        if config.SAVE_DATA_OPTION == "db":
            await db.init_db()
        print("start")
        root.title("Crawler is running...")
        crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
        await crawler.start()
        print("end")
        if config.SAVE_DATA_OPTION == "db":
            await db.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_crawler():
    
    parse_cmd()
    # 在事件循环中创建异步任务
    asyncio.run(run_crawler())
    root.title("Media Crawler Program")

def parse_cmd():
    # 获取用户输入的值并更新配置
    config.PLATFORM = platform_var.get()
    config.LOGIN_TYPE = lt_var.get()
    config.CRAWLER_TYPE = type_var.get()
    config.START_PAGE = int(start_page_var.get())
    config.KEYWORDS = keywords_var.get()
    config.ENABLE_GET_COMMENTS = str2bool(get_comment_var.get())
    config.ENABLE_GET_SUB_COMMENTS = str2bool(get_sub_comment_var.get())
    config.SAVE_DATA_OPTION = save_data_option_var.get()
    config.COOKIES = cookies_var.get()



def run_gui():
    global platform_var, lt_var, type_var, start_page_var, keywords_var, root
    global get_comment_var, get_sub_comment_var, save_data_option_var, cookies_var

    root = tk.Tk()
    root.title("Media Crawler Program")

    # 创建各个界面元素
    ttk.Label(root, text="选择平台:").grid(row=0, column=0, sticky=tk.W)
    platform_var = tk.StringVar(value=config.PLATFORM)
    ttk.Combobox(root, textvariable=platform_var, values=["xhs", "dy", "ks", "bili", "wb", "tieba"]).grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(root, text="登录类型:").grid(row=1, column=0, sticky=tk.W)
    lt_var = tk.StringVar(value=config.LOGIN_TYPE)
    ttk.Combobox(root, textvariable=lt_var, values=["qrcode", "phone", "cookie"]).grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(root, text="爬虫类型:").grid(row=2, column=0, sticky=tk.W)
    type_var = tk.StringVar(value=config.CRAWLER_TYPE)
    ttk.Combobox(root, textvariable=type_var, values=["search", "detail", "creator"]).grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(root, text="起始页:").grid(row=3, column=0, sticky=tk.W)
    start_page_var = tk.StringVar(value=str(config.START_PAGE))
    tk.Entry(root, textvariable=start_page_var).grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(root, text="关键词:").grid(row=4, column=0, sticky=tk.W)
    keywords_var = tk.StringVar(value=config.KEYWORDS)
    tk.Entry(root, textvariable=keywords_var).grid(row=4, column=1, padx=10, pady=5)

    ttk.Label(root, text="抓取一级评论:").grid(row=5, column=0, sticky=tk.W)
    get_comment_var = tk.StringVar(value=str(config.ENABLE_GET_COMMENTS))
    ttk.Combobox(root, textvariable=get_comment_var, values=["yes", "no"]).grid(row=5, column=1, padx=10, pady=5)

    ttk.Label(root, text="抓取二级评论:").grid(row=6, column=0, sticky=tk.W)
    get_sub_comment_var = tk.StringVar(value=str(config.ENABLE_GET_SUB_COMMENTS))
    ttk.Combobox(root, textvariable=get_sub_comment_var, values=["yes", "no"]).grid(row=6, column=1, padx=10, pady=5)

    ttk.Label(root, text="数据保存方式:").grid(row=7, column=0, sticky=tk.W)
    save_data_option_var = tk.StringVar(value=config.SAVE_DATA_OPTION)
    ttk.Combobox(root, textvariable=save_data_option_var, values=["csv", "db", "json"]).grid(row=7, column=1, padx=10, pady=5)

    ttk.Label(root, text="Cookies:").grid(row=8, column=0, sticky=tk.W)
    cookies_var = tk.StringVar(value=config.COOKIES)
    tk.Entry(root, textvariable=cookies_var).grid(row=8, column=1, padx=10, pady=5)

    tk.Button(root, text="运行", command=start_crawler).grid(row=9, column=0, columnspan=2, pady=10)
    #button = tk.Button(root, text="运行", command=button_clicked).grid(row=9, column=0, columnspan=2, pady=10)

    print("reach")
    root.mainloop()


if __name__ == '__main__':
    run_gui()
