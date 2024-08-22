import sys
import asyncio
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

import config
import db
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from tools.utils import str2bool
from constant.drop_down_selection import * 

platform_dict = {
    "小红书": "xhs",
    "抖音": "dy",
    "快手": "ks",
    "Bilibili": "bili",
    "微博": "wb",
    "贴吧": "tieba"
}

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
        if config.SAVE_DATA_OPTION == "db":
            await db.init_db()

        crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
        await crawler.start()

        if config.SAVE_DATA_OPTION == "db":
            await db.close()
    except Exception as e:
        print(f"An error occurred: {e}")

class CrawlerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # 创建并设置布局
        layout = QtWidgets.QGridLayout()

        # 平台选择
        layout.addWidget(QtWidgets.QLabel('选择平台:'), 0, 0)
        self.platform_var = QtWidgets.QComboBox()
        self.platform_var.addItems(["小红书", "抖音", "快手", "Bilibili", "微博", "贴吧"])
        layout.addWidget(self.platform_var, 0, 1)

        # 登录类型
        layout.addWidget(QtWidgets.QLabel('登录类型:'), 1, 0)
        self.lt_var = QtWidgets.QComboBox()
        self.lt_var.addItems(["qrcode", "phone", "cookie"])
        layout.addWidget(self.lt_var, 1, 1)

        # 爬虫类型
        layout.addWidget(QtWidgets.QLabel('爬虫类型:'), 2, 0)
        self.type_var = QtWidgets.QComboBox()
        self.type_var.addItems([HomeDropdownMenu.SEARCH_NOTE, 
                                HomeDropdownMenu.GET_NOTE_DETAIL_AND_COMMENTS, 
                                HomeDropdownMenu.GET_CREATOR_INFO_AND_NOTES_COMMENTS, 
                                HomeDropdownMenu.POST_COMMENT_UNDER_NOTE])
        layout.addWidget(self.type_var, 2, 1)

        # 起始页
        layout.addWidget(QtWidgets.QLabel('起始页:'), 3, 0)
        self.start_page_var = QtWidgets.QLineEdit(str(config.START_PAGE))
        layout.addWidget(self.start_page_var, 3, 1)

        # 关键词
        layout.addWidget(QtWidgets.QLabel('关键词:'), 4, 0)
        self.keywords_var = QtWidgets.QLineEdit(config.KEYWORDS)
        layout.addWidget(self.keywords_var, 4, 1)


        # 抓取一级评论
        layout.addWidget(QtWidgets.QLabel('抓取一级评论:'), 5, 0)
        self.get_comment_var = QtWidgets.QComboBox()
        self.get_comment_var.addItems(["yes", "no"])
        layout.addWidget(self.get_comment_var, 5, 1)

        # 抓取二级评论
        layout.addWidget(QtWidgets.QLabel('抓取二级评论:'), 6, 0)
        self.get_sub_comment_var = QtWidgets.QComboBox()
        self.get_sub_comment_var.addItems(["yes", "no"])
        layout.addWidget(self.get_sub_comment_var, 6, 1)

        # 数据保存方式
        layout.addWidget(QtWidgets.QLabel('数据保存方式:'), 7, 0)
        self.save_data_option_var = QtWidgets.QComboBox()
        self.save_data_option_var.addItems(["csv", "db", "json"])
        layout.addWidget(self.save_data_option_var, 7, 1)

        # Cookies
        layout.addWidget(QtWidgets.QLabel('Cookies:'), 8, 0)
        self.cookies_var = QtWidgets.QLineEdit(config.COOKIES)
        layout.addWidget(self.cookies_var, 8, 1)

        #TODO: test for xhs
        #为某一条帖子进行评论
        layout.addWidget(QtWidgets.QLabel('小红书帖子ID:'), 9, 0)
        #self.xhs_noteId_list_for_comments = QtWidgets.QLineEdit(config.XHS_NOTEID_LIST_FOR_COMMENTS)
        self.xhs_noteId_list_for_comments = QtWidgets.QListWidget()
        
        self.xhs_noteId_list_for_comments.addItems(config.XHS_NOTEID_LIST_FOR_COMMENTS)
        layout.addWidget(self.xhs_noteId_list_for_comments, 9, 1)

        #帖子内容
        layout.addWidget(QtWidgets.QLabel('评论内容'), 10, 0)
        self.xhs_post_comments_content = QtWidgets.QLineEdit(config.XHS_POST_COMMENTS_CONTENT)
        layout.addWidget(self.xhs_post_comments_content, 10, 1)

        # 运行按钮
        self.run_button = QtWidgets.QPushButton('运行')
        self.run_button.clicked.connect(self.start_crawler)
        layout.addWidget(self.run_button, 11, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('Media Crawler Program')

    def parse_cmd(self):
        config.PLATFORM = platform_dict[self.platform_var.currentText()]
        config.LOGIN_TYPE = self.lt_var.currentText()
        config.CRAWLER_TYPE = self.type_var.currentText()
        config.START_PAGE = int(self.start_page_var.text())
        config.KEYWORDS = self.keywords_var.text()
        config.ENABLE_GET_COMMENTS = str2bool(self.get_comment_var.currentText())
        config.ENABLE_GET_SUB_COMMENTS = str2bool(self.get_sub_comment_var.currentText())
        config.SAVE_DATA_OPTION = self.save_data_option_var.currentText()
        config.COOKIES = self.cookies_var.text()
        config.XHS_POST_COMMENTS_CONTENT = self.xhs_post_comments_content.text()
        print(config.PLATFORM)

    def start_crawler(self):
        self.parse_cmd()
        self.run_button.setEnabled(False)  # 禁用按钮防止重复点击
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_crawler())
        self.run_button.setEnabled(True)  # 任务完成后重新启用按钮

def run_app():
    app = QtWidgets.QApplication(sys.argv)
    crawler_app = CrawlerApp()
    crawler_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()