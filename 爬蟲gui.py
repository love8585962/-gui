import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTextEdit
import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent

# 使用 pyinstaller 打包成 exe 時的指令
# pyinstaller --onefile test.py
# 若要生成的 exe 不顯示 cmd 視窗，可以使用以下指令
# pyinstaller --onefile --noconsole test.py
# 使用fake_useragent直接匯出exe會報錯 因此在打包時需要直接指定fake_useragent整個資料夾連同打包才不會報錯
# pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/user/Desktop/python/1.ico" --add-data "C:/Users/user/AppData/Local/Programs/Python/Python312/Lib/site-packages/fake_useragent;fake_useragent/"  "C:/Users/user/Desktop/python/爬蟲gui.py"
# 使用 pip install auto-py-to-exe 打包更為方便
# cmd 輸入 auto-py-to-exe 即可啟動
class WebScraperApp(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化 UI
        self.init_ui()

    def init_ui(self):
        # 創建控件
        # 創建 URL 標籤和輸入框，設置提示文字為 "ex: http://abc.com"
        self.url_label = QLabel('URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('ex: http://abc.com')

        # 創建標籤標籤和輸入框，設置提示文字為 "ex: div"
        self.target_label = QLabel('標籤:')
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText('ex: div')

        # 創建關鍵字標籤和輸入框
        self.keyword_label = QLabel('關鍵字:')
        self.keyword_input = QLineEdit()

        # 創建結果輸出文本框，並設置為只讀模式
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # 創建啟動爬取按鈕，並連接到爬取函數
        self.scrape_button = QPushButton('Start')
        self.scrape_button.clicked.connect(self.scrape_data)

        # 創建垂直佈局
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_input)
        layout.addWidget(self.keyword_label)
        layout.addWidget(self.keyword_input)
        layout.addWidget(self.scrape_button)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

        # 設置應用程序視窗
        self.setWindowTitle('爬蟲')
        self.setGeometry(200, 200, 600, 400)

    def scrape_data(self):
        url = self.url_input.text()

        # 檢查是否輸入了有效的 URL
        if not url:
            self.result_output.setPlainText('請輸入URL')
            return

        try:
            ua = UserAgent()
            headers = {'User-Agent': ua.random}

            # 設置超時時間為 5 秒，你可以根據需要進行調整
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # 檢查是否發生錯誤

            soup = BeautifulSoup(response.text, 'lxml')

            target_tag = self.target_input.text()
            paragraphs = soup.find_all(target_tag) if target_tag else soup.find_all('p')

            keyword = self.keyword_input.text()
            desired_paragraphs = []
            for paragraph in paragraphs:
                if keyword in paragraph.text:
                    desired_paragraphs.append(paragraph.text)

            result_text = '\n'.join(desired_paragraphs)
            self.result_output.setPlainText(result_text)

        except requests.exceptions.Timeout:
            # 處理超時錯誤
            self.result_output.setPlainText('ERROR: 請求超時')
            return

        except requests.exceptions.RequestException as e:
            # 處理錯誤
            self.result_output.setPlainText(f'ERROR: 請檢查是否為有效網址 {e}')
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebScraperApp()
    window.show()
    sys.exit(app.exec_())
