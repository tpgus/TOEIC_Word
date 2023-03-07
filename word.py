import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import random

import os

class_form=uic.loadUiType('word.ui')[0]

class MyWord(QMainWindow,class_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.total_word_files = os.listdir('./')
        self.comboBox.addItems(self.total_word_files)
        self.start.clicked.connect(self.start_clicked)
        self.btn_prev.clicked.connect(self.btn_prev_clicked)
        self.btn_next.clicked.connect(self.btn_next_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_clicked)
        self.btn_addition_incorrectWord.clicked.connect(self.btn_addtionIncorrectWord_clicked)
        self.btn_search.clicked.connect(self.btn_search_clicked)
        self.btn_correction.clicked.connect(self.showDialog)
        self.btn_random.clicked.connect(self.btn_random_clicked)
        self.btn_integration.clicked.connect(self.btn_integration_clicked)
        self.btn_easyWord.clicked.connect(self.btn_easyWord_clicked)
        self.btn_recover.clicked.connect(self.btn_recover_clicked)

        self.radioButton_1.setChecked(True)
        self.radioButton_1.clicked.connect(self.radio_clicked)
        self.radioButton_2.clicked.connect(self.radio_clicked)
        self.move.clicked.connect(self.move_clicked)
        self.btn_save.clicked.connect(self.btn_save_clicked)
        self.btn_save_currently_state.clicked.connect(self.currently_state_clicked)


        self.pushButton.clicked.connect(self.today)
        self.statusbar=QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.word_list_copy=None
        self.word_list=None
        self.idx=None

    def start_clicked(self):
        self.choosed_word_file=self.comboBox.currentText()
        if self.choosed_word_file=='easyWord.txt':
            self.btn_recover.setEnabled(True)
        else:
            self.btn_recover.setEnabled(False)
        self.idx = 0
        self.word=[]
        self.mean=[]
        self.label_mean.setText('')
        if self.radioButton_1.isChecked():
            self.file_path='./%s'%self.choosed_word_file
        else:
            self.file_path='./틀린단어/%s'%self.choosed_word_file
        try:
            with open('%s'%self.file_path,'r',encoding='UTF-8') as file:
                self.word_list=file.readlines()
                for j,i in enumerate(self.word_list):
                    if i=='\n':
                        pass
                    else:
                        self.word.append(i.split('`')[0])
                        self.mean.append(i.split('`')[1])
                        if i[-1] != '\n':
                            self.word_list[j]+='\n'

                self.word_list_copy=self.word_list.copy() #수정할 때 쓰려고
                self.word_list_copy_for_easyWord=self.word_list.copy()
                word=self.word[0]
                self.textEdit.setText(word)
                self.label_number.setText('1/%d'%len(self.word_list))
                self.show_mean_flag=1
                self.btn_next.setEnabled(True)
                self.btn_prev.setEnabled(True)
        except:
            self.textEdit.setText('파일 내용이 비어있음\n문자 ` 에 대한 split 에러 ')


    def btn_prev_clicked(self):
        if self.show_mean_flag==0:
            self.idx=self.idx-1
            if self.idx<0:
                self.idx=(len(self.word)-1)
            self.textEdit.setText(self.word[self.idx])
            self.label_number.setText('%d/%d'%(self.idx+1,len(self.word)))
            self.label_mean.setText('')
            self.show_mean_flag = 1

        else:
            self.label_mean.setText(self.mean[self.idx])
            self.show_mean_flag = 0
            self.textEdit.setText(self.word_list[self.idx])

    def btn_next_clicked(self):
        if self.show_mean_flag==0:
            self.idx = self.idx + 1
            if self.idx>(len(self.word)-1):
                self.idx=0
            self.textEdit.setText(self.word[self.idx])
            self.label_number.setText('%d/%d' % (self.idx + 1, len(self.word)))
            self.label_mean.setText('')
            self.show_mean_flag=1
        else:
            self.label_mean.setText(self.mean[self.idx])
            self.show_mean_flag=0
            self.textEdit.setText(self.word_list[self.idx])
        self.btn_delete.setEnabled(True)
        self.btn_easyWord.setEnabled(True)
        self.btn_recover.setEnabled(True)


    def btn_delete_clicked(self):
        self.btn_delete.setEnabled(False)
        self.word_list.pop(self.idx)
        self.word.pop(self.idx)
        self.mean.pop(self.idx)
        self.idx-=1
        if len(self.word_list)==0:
            self.textEdit.setText("한 번 더 누르면 에러뜬다");
            self.btn_next.setEnabled(False)
            self.btn_prev.setEnabled(False)
        self.show_mean_flag=0

    def btn_save_clicked(self):
        text, ok = QInputDialog.getText(self, '저장하기','파일명 입력(.txt 제외)')

        if self.radioButton_1.isChecked(): #라디오 버튼이 클릭됨에 따라 경로설절 하고 현재 경로에 저장
            self.dir='./'
        else:
            self.dir='./틀린단어/'

        text=self.dir+text

        if ok:
            with open('%s.txt'%text,'w',encoding='UTF8') as file:
                for i in self.word_list:
                    file.write(i)

    def move_clicked(self):
        try:
            word=self.textEdit.toPlainText()
            self.idx=self.word.index(word)
            self.textEdit.clear()
            self.textEdit.append(self.word[self.idx])
            self.label_number.setText('%d/%d'%(self.idx+1,len(self.word)))
        except:
            self.textEdit.append('에러발생')

    def btn_random_clicked(self):
        self.textEdit.clear()
        self.word=[]
        self.mean = []
        self.idx=0

        self.label_mean.setText('')
        random.shuffle(self.word_list)

        for j, i in enumerate(self.word_list):
            self.word.append(i.split('`')[0])
            self.mean.append(i.split('`')[1])
            if i[-1] != '\n':
                self.word_list[j] += '\n'

        word = self.word[0]
        self.textEdit.setText(word)
        self.label_number.setText('1/%d' % len(self.word_list))
        self.show_mean_flag = 1

    def btn_addtionIncorrectWord_clicked(self):
        b = self.comboBox.currentText().replace('.txt','')
        a = '%s_오답.txt' % b
        self.listWidget.clear()

        self.label_mean.setText(self.mean[self.idx])
        self.show_mean_flag = 0
        self.textEdit.setText(self.word_list[self.idx])

        with open('./틀린단어/%s' % a,'a',encoding='UTF8') as q:
            if self.word_list[self.idx][-1]!='\n':
                q.write(self.word_list[self.idx]+'\n')
            else:
                q.write(self.word_list[self.idx])

        with open('./틀린단어/%s'%a,'r',encoding='UTF8') as q:
            c=q.readlines()
            self.listWidget.addItems(c)

    def currently_state_clicked(self):
        b = self.comboBox.currentText().replace('.txt', '')
        if b.find('오답')==-1:
            a = '%s_오답.txt' % b
        else:
            a='%s.txt'%b

        self.listWidget.clear()

        # if os.path.exists('./틀린단어/%s'%a):
        #     pass
        # else:
        #     with open('./틀린단어/%s'%a, 'w', encoding='UTF8') as p:
        #         pass
        if b.find('오답')!=-1:
            with open('./틀린단어/%s'%a,'w',encoding='UTF8') as q:
                q.writelines(self.word_list)

        else:
            word_list=[]
            with open('./틀린단어/%s'%a,'r',encoding='UTF8') as q:
                ww=q.readlines()
                for i in self.word_list:
                    if i in ww:
                        pass
                    else:
                        word_list.append(i)

            with open('./틀린단어/%s'%a,'a+',encoding='UTF8') as q:
                 q.writelines(word_list)

        with open('./틀린단어/%s' % a, 'r', encoding='UTF8') as q:
            c = q.readlines()
            self.listWidget.addItems(c)

    def btn_search_clicked(self):
        self.listWidget.clear()
        search_word=self.lineEdit.text()
        with open('./total.txt','r',encoding='UTF8') as file:
            word_list=file.readlines()
            for i in word_list:
                if search_word in i:
                    self.listWidget.addItem(i.strip('\n'))


    def radio_clicked(self):
        if self.radioButton_1.isChecked():
            self.total_word_files = os.listdir('./')
        else:
            self.total_word_files=os.listdir('./틀린단어/')

        self.comboBox.clear()
        self.comboBox.addItems(self.total_word_files)

    def today(self):
        a=self.lineEdit_2.text()
        a = int(a)%30
        b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30]
        c = [a, b[a - 2], b[a - 3],b[a-4], b[a - 6], b[a - 10], b[a - 16]]
        c.sort()
        self.statusbar.showMessage(str(c))

    def showDialog(self):
        text, ok = QInputDialog.getText(self, '단어 수정하기',self.word_list[self.idx])

        if ok:
            idx=self.word_list_copy.index(self.word_list[self.idx])
            self.word_list_copy[idx]=text+'\n'
            self.word_list[self.idx]=text+'\n'
            self.word[self.idx]=text.split('`')[0]
            self.mean[self.idx]=text.split('`')[1]
            self.textEdit.setText(self.word_list[self.idx])
            self.label_mean.setText(self.mean[self.idx])
            self.show_mean_flag=0

            with open('%s'%self.file_path,'w',encoding='UTF8') as file:
                for i in self.word_list_copy:
                    file.write(i)

    def btn_integration_clicked(self):
        a=[]
        file_list=os.listdir('.')
        if 'total.txt' in file_list:
            os.remove('./total.txt')

        for i in file_list:
            if 'word_' in i:
                a.append(i)

        for i in a:
            with open('./%s'%i,'r',encoding='UTF8') as p:
                b=p.readlines()
            with open('./total.txt','a',encoding='UTF8') as p:
                p.writelines(b)

    def btn_easyWord_clicked(self):
        self.btn_easyWord.setEnabled(False)
        a=self.comboBox.currentText()
        a=a.split('_')
        a=a[1].split('.')
        with open('./easyWord.txt','a',encoding='UTF8') as p:
            p.write(self.word_list[self.idx].rstrip('\n')+'@'+a[0]+'\n')

        a=self.word_list_copy_for_easyWord.index(self.word_list[self.idx])
        self.word_list_copy_for_easyWord.pop(a)
        self.word_list.pop(self.idx)
        self.word.pop(self.idx)
        self.mean.pop(self.idx)
        self.idx-=1

        with open('./%s'%self.comboBox.currentText(),'w',encoding='UTF8') as p:
            p.writelines(self.word_list_copy_for_easyWord)
        if len(self.word_list)==0:
            self.textEdit.setText("한 번 더 누르면 에러뜬다");
            self.btn_next.setEnabled(False)
            self.btn_prev.setEnabled(False)
        self.show_mean_flag=0

    def btn_recover_clicked(self):
        a=self.word_list[self.idx]
        a=a.split('@')
        b=a[1].rstrip('\n')
        with open('./word_%s.txt'%b,'a',encoding='UTF8') as p:
            p.write(a[0]+'\n')

        self.word_list.pop(self.idx)
        self.word.pop(self.idx)
        self.mean.pop(self.idx)
        self.idx -= 1

        with open('./%s'%self.comboBox.currentText(),'w',encoding='UTF8') as p:
            p.writelines(self.word_list)

        if len(self.word_list) == 0:
            self.textEdit.setText("한 번 더 누르면 에러뜬다");
            self.btn_next.setEnabled(False)
            self.btn_prev.setEnabled(False)
        self.show_mean_flag = 0
        self.btn_recover.setEnabled(False)

if __name__=='__main__':
    app=QApplication(sys.argv)
    myword=MyWord()
    myword.show()
    myword.btn_recover.setEnabled(False)
    app.exec_()