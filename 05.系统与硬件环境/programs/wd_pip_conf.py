import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler, LoggingEventHandler

FILE_NAME = '/etc/pip.conf'
DEFAULT_CONTENT = """[global]
index-url=https://mirrors.aliyun.com/pypi/simple/
extra-index-url=https://www.piwheels.org/simple
"""

def create_default_pip_conf():
    """创建缺省的pip.conf"""
    with open(FILE_NAME,'wt') as f:
        f.write(DEFAULT_CONTENT)
    logging.warning("Default pip.conf created again!")

class MyEventHandler(RegexMatchingEventHandler, LoggingEventHandler):
    """定义一个自己的事件处理类"""
    def on_deleted(self, event):
        create_default_pip_conf()
    def on_moved(self, event):
        create_default_pip_conf()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = MyEventHandler([r'^/etc/pip\.conf$'])

    # 开始监控
    observer = Observer()
    observer.schedule(event_handler, "/etc/", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # 结束监控
        observer.stop()
        observer.join()