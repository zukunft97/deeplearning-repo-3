import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pandas as pd
import numpy as np
from ultralytics import YOLO

from_class = uic.loadUiType("pyqt.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("food")

        self.foodlist=[]
        self.cooklist=[]

        self.ingredientbox.setReadOnly(True)
        self.linkbox.setReadOnly(True)

        self.fooddf = pd.read_excel('food.xlsx')
        self.foodrange = len(self.fooddf)

        self.file.clicked.connect(self.file_Clicked)
        # 모든 목록 지우기
        self.reset.clicked.connect(self.reset_Clicked)
        # 음식을 만드는데 필요한 재료가 모두 있어야지만 음식 추천
        self.suggestion.clicked.connect(self.jo)
        self.suggestion.clicked.connect(self.suggestion_Clicked)
        # 음식을 만드는데 필요한 재료가 1개라도 있다면 음식 추천
        self.suggestion2.clicked.connect(self.suggestion2_Clicked)
        # 음식의 추천 목록을 이전,이후걸로 넘기기
        self.since.clicked.connect(self.since_Clicked)
        self.next.clicked.connect(self.next_Clicked)
        # 재료를 직접 입력하여 리스트에 추가
        self.add.clicked.connect(self.add_Clicked)
        self.lineEdit.returnPressed.connect(self.add_Clicked)
        # combobox의 값이 변경될때마다 링크 변경
        self.foodbox.currentTextChanged.connect(self.Lnk)

        self.pixmap = QPixmap()


    def file_Clicked(self):
        name_list = ['어묵', '김밥햄', '연근', '깻잎', '흰버섯', '멸치', '아스파라거스', '아보카도', '베이컨', '양배추', '콩', '콩나물', ' 소고기', '비트', '청경채', '브로콜리', '우엉', '오징어', '꽁치통조림', '참치캔', '당근', '치즈', '닭고기', '부추', '조개' , '옥수수', '게', '오이', '강황', '오리고기', '만두', '계란', '가지', '팽이버섯', '키조개', '인삼', '대파', ' 갈치', '김치', '양갈비', '고등어', '국물용고기', '우유', '배추', '누룽지', '양파', '굴', '느타리버섯', '파프리카', '파스타면' , '피클', '돼지고기', '감자', '무', '생갈비', '떡', '연어', '소시지', '가리비', '미역', '스팸', '호박', ' 고구마', '토마토', '토마토소스', '미나리']
        list = []
        file_path = QFileDialog.getOpenFileName(self, 'Open file', './', "Images (*.png *.jpg *.jpeg)")[0]
        self.pixmap.load(file_path)
        self.pixmap = self.pixmap.scaled(self.Pixmap.width(), self.Pixmap.height())

        model = YOLO('./best.pt')
        results = model(file_path)
        end = results[0].boxes.cls.tolist()
        end_len = len(end)
        for i in range(end_len):
            name = name_list[int(end[i])]
            self.ingredientbox.append(name)
            
        self.Pixmap.setPixmap(self.pixmap)

        try:
            a = self.ingredientbox.toPlainText()
            self.foodlist = []
            self.foodlist.append(a)
            self.foodlist = self.foodlist[0].split('\n')
            # 문자열 중복제거 
            # 전에 코드는 self.foodlist = list(set(self.foodlist[0]))으로 리스트 첫번째 문자만들 중복제거해서 이상하게 되었음.
            self.foodlist = list(set(self.foodlist))
            print(self.foodlist)
        except:
            print("x")

    def reset_Clicked(self):
        self.ingredientbox.clear()
        self.linkbox.clear()
        self.foodbox.clear()
        self.lineEdit.clear()

        self.foodlist = []
        self.cooklist = []

        self.linkbox.clear()
        self.linkbox_2.clear()
        self.linkbox_3.clear()
        self.linkbox_4.clear()
    
    def suggestion_Clicked(self):
        self.cooklist = []
        self.foodbox.clear()
        
        for n in range(0,self.foodrange, 1):
            a = self.fooddf.iloc[n,1:].values
            a = np.array2string(a)
            a = a[2:]
            a = a[:-2]
            a = a.split(',')
            b = list(set(self.foodlist) & set(a))
            if a == b:
                c = self.fooddf.iloc[n,:1].values
                c = np.array2string(c)
                c = c[2:]
                c = c[:-2]
                self.cooklist.append(c)
        x = len(self.cooklist)
        for n in range(0,x,1):
            self.foodbox.addItem(self.cooklist[n])
            
    def suggestion2_Clicked(self):
        self.cooklist = []
        self.foodbox.clear()        
        for n in range(0,self.foodrange, 1):
            a = self.fooddf.iloc[n,1:].values
            a = np.array2string(a)
            a = a[2:]
            a = a[:-2]
            a = a.split(',')
            b = list(set(a) & set(self.foodlist))
            b = len(b)
            if  b >= 1 :
                c = self.fooddf.iloc[n,:1].values
                c = np.array2string(c)
                c = c[2:]
                c = c[:-2]
                self.cooklist.append(c)
        x = len(self.cooklist)
        for n in range(0,x,1):
            self.foodbox.addItem(self.cooklist[n])
 
    def since_Clicked(self):
        # 현제 combobox의 인덱스를 구함
        current_index = self.foodbox.currentIndex()
        # 인덱스의 값을 변환
        # % self.foodbox.count() 콤보박스의 총 항목 수로 현재 인덱스를 나눈 나머지를 반환합니다.
        # 이렇게하면 사용자가 항목의 끝에 도달해서 한번더 누르더라도 인덱스가 combobox 항목의 범위내에서 유지됩니다.
        since_index = (current_index - 1) % self.foodbox.count()
        # 구한 인덱스 위치로 combobox 변환
        self.foodbox.setCurrentIndex(since_index)

    def next_Clicked(self):
        current_index = self.foodbox.currentIndex()
        next_index = (current_index + 1) % self.foodbox.count()
        self.foodbox.setCurrentIndex(next_index)

    def add_Clicked(self):
        input = self.lineEdit.text()
        self.lineEdit.clear()
        self.ingredientbox.append(input)
        try:
            a = self.ingredientbox.toPlainText()
            self.foodlist = []
            self.foodlist.append(a)
            self.foodlist = self.foodlist[0].split('\n')
            # 문자열 중복제거 
            # 전에 코드는 self.foodlist = list(set(self.foodlist[0]))으로 리스트 첫번째 문자만들 중복제거해서 이상하게 되었음.
            self.foodlist = list(set(self.foodlist))
        except:
            print("x")

    # def av(self):
    #     try:
    #         a = self.ingredientbox.toPlainText()
    #         self.foodlist = []
    #         self.foodlist.append(a)
    #         self.foodlist = self.foodlist[0].split('\n')
    #         self.foodlist = list(set(self.foodlist))
    #         b = len(self.foodlist)
    #         for i in range(b):
    #             self.ingredientbox.append(self.foodlist[i])
    #     except:
    #         print("x")


    def jo(self):
        a = self.ingredientbox.toPlainText()
        self.foodlist.append(a)
        self.foodlist = self.foodlist[-1].split('\n')
        # 문자열 중복제거 
        self.foodlist = list(set(self.foodlist))

        if self.check1.isChecked() == True:
            self.foodlist.append('식용유')

        if self.check2.isChecked() == True:
            self.foodlist.append('고춧가루')
            self.foodlist.append('설탕')
            self.foodlist.append('소금')
            self.foodlist.append('다시다')

        if self.check3.isChecked() == True:
            self.foodlist.append('고추장')
            self.foodlist.append('된장')
            self.foodlist.append('간장')
            self.foodlist.append('쌈장')

        if self.check4.isChecked() == True:
            self.foodlist.append('참기름')
            self.foodlist.append('들기름')
            
        if self.check5.isChecked() == True:
            self.foodlist.append('물엿')
            
        if self.check6.isChecked() == True:
            self.foodlist.append('케찹')
            
        if self.check7.isChecked() == True:
            self.foodlist.append('머스타드')
            
        if self.check8.isChecked() == True:
            self.foodlist.append('마늘')
            
        if self.check9.isChecked() == True:
            self.foodlist.append('밀가루')
            self.foodlist.append('빵가루')
            self.foodlist.append('튀김가루')
            
        if self.check10.isChecked() == True:
            self.foodlist.append('감자전분')
            self.foodlist.append('옥수수전분')
            
        if self.check11.isChecked() == True:
            self.foodlist.append('고추')
            
        if self.check12.isChecked() == True:
            self.foodlist.append('올리고당')

    def Lnk(self):
        self.linkbox.clear()
        self.linkbox_2.clear()
        self.linkbox_3.clear()
        self.linkbox_4.clear()

        try:
            self.linkbox.anchorClicked.disconnect()
            self.linkbox_2.anchorClicked.disconnect()
            self.linkbox_3.anchorClicked.disconnect()
            self.linkbox_4.anchorClicked.disconnect()
        except:
            print("x")    

        # self.linkbox.setPlainText("만개의레시피")
        link = self.foodbox.currentText()
        self.linkbox.setPlainText("https://www.10000recipe.com/recipe/list.html?q="+link)

        cursor = self.linkbox.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len("https://www.10000recipe.com/recipe/list.html?q="+link))

        format = QTextCharFormat()
        format.setAnchor(True)
        format.setAnchorHref("https://www.10000recipe.com/recipe/list.html?q="+link)

        cursor.setCharFormat(format)

        # Connect the linkClicked signal to open the link in the default browser
        self.linkbox.anchorClicked.connect(lambda link_2: QDesktopServices.openUrl(QUrl(link_2)))


        # self.linkbox.setPlainText("google")
        self.linkbox_2.setPlainText("https://www.google.com/search?q="+link)

        cursor = self.linkbox_2.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len("https://www.google.com/search?q="+link))

        format = QTextCharFormat()
        format.setAnchor(True)
        format.setAnchorHref("https://www.google.com/search?q="+link)

        cursor.setCharFormat(format)

        # Connect the linkClicked signal to open the link in the default browser
        self.linkbox_2.anchorClicked.connect(lambda link_2: QDesktopServices.openUrl(QUrl(link_2)))

        # self.linkbox.setPlainText("naver")
        self.linkbox_3.setPlainText("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="+link)

        cursor = self.linkbox_3.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="+link))

        format = QTextCharFormat()
        format.setAnchor(True)
        format.setAnchorHref("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="+link)

        cursor.setCharFormat(format)

        # Connect the linkClicked signal to open the link in the default browser
        self.linkbox_3.anchorClicked.connect(lambda link: QDesktopServices.openUrl(QUrl(link.toString())))

        # self.linkbox.setPlainText("daum")
        self.linkbox_4.setPlainText("https://search.daum.net/search?w=site&nil_search=btn&DA=NTB&enc=utf8&lpp=10&q="+link)

        cursor = self.linkbox_4.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len("https://search.daum.net/search?w=site&nil_search=btn&DA=NTB&enc=utf8&lpp=10&q="+link))

        format = QTextCharFormat()
        format.setAnchor(True)
        format.setAnchorHref("https://search.daum.net/search?w=site&nil_search=btn&DA=NTB&enc=utf8&lpp=10&q="+link)

        cursor.setCharFormat(format)

        # Connect the linkClicked signal to open the link in the default browser
        self.linkbox_4.anchorClicked.connect(lambda link: QDesktopServices.openUrl(QUrl(link.toString())))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())