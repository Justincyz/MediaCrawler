# import argparse

# import config
# from tools.utils import str2bool


# async def parse_cmd():
#     # 读取command arg
#     parser = argparse.ArgumentParser(description='Media crawler program.')
#     parser.add_argument('--platform', type=str, help='Media platform select (xhs | dy | ks | bili | wb | tieba)',
#                         choices=["xhs", "dy", "ks", "bili", "wb", "tieba"], default=config.PLATFORM)
#     parser.add_argument('--lt', type=str, help='Login type (qrcode | phone | cookie)',
#                         choices=["qrcode", "phone", "cookie"], default=config.LOGIN_TYPE)
#     parser.add_argument('--type', type=str, help='crawler type (search | detail | creator)',
#                         choices=["search", "detail", "creator"], default=config.CRAWLER_TYPE)
#     parser.add_argument('--start', type=int,
#                         help='number of start page', default=config.START_PAGE)
#     parser.add_argument('--keywords', type=str,
#                         help='please input keywords', default=config.KEYWORDS)
#     parser.add_argument('--get_comment', type=str2bool,
#                         help='''whether to crawl level one comment, supported values case insensitive ('yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0')''', default=config.ENABLE_GET_COMMENTS)
#     parser.add_argument('--get_sub_comment', type=str2bool,
#                         help=''''whether to crawl level two comment, supported values case insensitive ('yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0')''', default=config.ENABLE_GET_SUB_COMMENTS)
#     parser.add_argument('--save_data_option', type=str,
#                         help='where to save the data (csv or db or json)', choices=['csv', 'db', 'json'], default=config.SAVE_DATA_OPTION)
#     parser.add_argument('--cookies', type=str,
#                         help='cookies used for cookie login type', default=config.COOKIES)

#     args = parser.parse_args()

#     # override config
#     config.PLATFORM = args.platform
#     config.LOGIN_TYPE = args.lt
#     config.CRAWLER_TYPE = args.type
#     config.START_PAGE = args.start
#     config.KEYWORDS = args.keywords
#     config.ENABLE_GET_COMMENTS = args.get_comment
#     config.ENABLE_GET_SUB_COMMENTS = args.get_sub_comment
#     config.SAVE_DATA_OPTION = args.save_data_option
#     config.COOKIES = args.cookies


import tkinter as tk
from tkinter import ttk, messagebox
import config
from tools.utils import str2bool

from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler

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


    
async def run_crawler():

    global platform_var, lt_var, type_var, start_page_var, keywords_var
    global get_comment_var, get_sub_comment_var, save_data_option_var, cookies_var


    root = tk.Tk()
    root.title("Media Crawler Program")

    # 平台选择
    ttk.Label(root, text="选择平台:").grid(row=0, column=0, sticky=tk.W)
    platform_var = tk.StringVar(value=config.PLATFORM)
    ttk.Combobox(root, textvariable=platform_var, values=["xhs", "dy", "ks", "bili", "wb", "tieba"]).grid(row=0, column=1, padx=10, pady=5)

    # 登录类型
    ttk.Label(root, text="登录类型:").grid(row=1, column=0, sticky=tk.W)
    lt_var = tk.StringVar(value=config.LOGIN_TYPE)
    ttk.Combobox(root, textvariable=lt_var, values=["qrcode", "phone", "cookie"]).grid(row=1, column=1, padx=10, pady=5)

    # 爬虫类型
    ttk.Label(root, text="爬虫类型:").grid(row=2, column=0, sticky=tk.W)
    type_var = tk.StringVar(value=config.CRAWLER_TYPE)
    ttk.Combobox(root, textvariable=type_var, values=["search", "detail", "creator"]).grid(row=2, column=1, padx=10, pady=5)

    # 起始页
    ttk.Label(root, text="起始页:").grid(row=3, column=0, sticky=tk.W)
    start_page_var = tk.StringVar(value=str(config.START_PAGE))
    tk.Entry(root, textvariable=start_page_var).grid(row=3, column=1, padx=10, pady=5)

    # 关键词
    ttk.Label(root, text="关键词:").grid(row=4, column=0, sticky=tk.W)
    keywords_var = tk.StringVar(value=config.KEYWORDS)
    tk.Entry(root, textvariable=keywords_var).grid(row=4, column=1, padx=10, pady=5)

    # 是否抓取一级评论
    ttk.Label(root, text="抓取一级评论:").grid(row=5, column=0, sticky=tk.W)
    get_comment_var = tk.StringVar(value=str(config.ENABLE_GET_COMMENTS))
    ttk.Combobox(root, textvariable=get_comment_var, values=["yes", "no"]).grid(row=5, column=1, padx=10, pady=5)

    # 是否抓取二级评论
    ttk.Label(root, text="抓取二级评论:").grid(row=6, column=0, sticky=tk.W)
    get_sub_comment_var = tk.StringVar(value=str(config.ENABLE_GET_SUB_COMMENTS))
    ttk.Combobox(root, textvariable=get_sub_comment_var, values=["yes", "no"]).grid(row=6, column=1, padx=10, pady=5)

    # 数据保存选项
    ttk.Label(root, text="数据保存方式:").grid(row=7, column=0, sticky=tk.W)
    save_data_option_var = tk.StringVar(value=config.SAVE_DATA_OPTION)
    ttk.Combobox(root, textvariable=save_data_option_var, values=["csv", "db", "json"]).grid(row=7, column=1, padx=10, pady=5)

    # Cookies
    ttk.Label(root, text="Cookies:").grid(row=8, column=0, sticky=tk.W)
    cookies_var = tk.StringVar(value=config.COOKIES)
    tk.Entry(root, textvariable=cookies_var).grid(row=8, column=1, padx=10, pady=5)

    # 运行按钮
    tk.Button(root, text="运行", command=check).grid(row=9, column=0, columnspan=2, pady=10)


    
    root.mainloop()

async def check():
    parse_cmd()
    crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
    await crawler.start()
