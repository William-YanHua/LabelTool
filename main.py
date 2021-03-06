'''
@File     : main.py
@Copyright: 
@author   : lxt
@Date     : 2020/8/29
@Desc     :
'''
import PyQt5
from PyQt5.QtWidgets import *
import pygame
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from uiwindow import Ui_MainWindow
import sys
import os
import pandas as pd

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./icon/icon.ico'))
        self.setWindowTitle("标注小民工[可跳转版]")
        self.data = None
        self.data_index = None
        self.totalindex = 0
        self.index_num = 0
        self.file_name = ""
        self.emotion_value = self.emotion_list[0]
        self.sarcasm = None
        self.metaphor = None
        self.exaggeration = None
        self.homophonic = None
        self.symbolism = None
        self.sentiment = None
        self.save_curr_flag = False
        self.current_qian = 0
        self.nums = 0
        # add action
        self.actionfileopen.triggered.connect(self._openFile)
        self.cb_6.currentIndexChanged[str].connect(self._selectEmotion)
        self.tiao_btn.clicked.connect(self._clickJump)
        self.save_btn.clicked.connect(self._saveData)
        self.next_btn.clicked.connect(self._clickNext)
        self.bg1.buttonClicked.connect(self.rbclicked)
        self.bg2.buttonClicked.connect(self.rbclicked)
        self.bg3.buttonClicked.connect(self.rbclicked)
        self.bg4.buttonClicked.connect(self.rbclicked)
        self.bg5.buttonClicked.connect(self.rbclicked)
        self.bg7.buttonClicked.connect(self.rbclicked)

    def _openFile(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.csv)")
        self._reset()
        self.caifu.setText("财富：{} 毛".format(self.current_qian))
        self.file_path.setText(file_name)
        self.file_name = file_name
        self._loadFile(file_name)
        # self._showData()
        self._loadData()

    def _reset(self):
        self.data = None
        self.data_index = None
        self.totalindex = 0
        self.file_name = ""
        self.save_curr_flag = False
        self._resetSelection()

    def _resetSelection(self):
        self.tiao_btn.setVisible(True)
        self.index.setVisible(True)
        self.emotion_value = self.emotion_list[0]
        self.sarcasm = None
        self.metaphor = None
        self.exaggeration = None
        self.homophonic = None
        self.symbolism = None
        self.sentiment = None
        self._cleanText()


    def _selectEmotion(self, i):
        self.emotion_value = i

    def _loadFile(self, file_path):
        try:
            self.data = pd.read_csv(file_path, encoding='utf-8')
        except Exception as e:
            self.data = pd.read_csv(file_path, encoding='gbk')
        self.data_index = self.data.index
        self.nums = self.data.shape[0]
        print("loading data", len(self.data_index))
        print("loading data", self.data.shape)

    def _tricks(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./music/123.wav")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

    def _showData(self):
        nums = self.data.shape[0]
        is_operate = False
        for i in range(self.totalindex, nums):
            df = self.data.iloc[i]
            f1, f2, f3, f4, f5, f6, f7, f8 = df['sarcasm'], df['metaphor'], df['exaggeration'], df['homophonic'], df['symbolism'], df['emotion'], df['sentiment'], df['other_subtext']
            if pd.isnull(f1) or pd.isnull(f2) or pd.isnull(f3) or pd.isnull(f4) or pd.isnull(f5) or pd.isnull(f7) or pd.isnull(f8):
                if 'question' not in self.data.columns:
                    self.comment_text.setText(str(df['comment']))
                    self.content_text.setText("{}".format(df['content']))
                else:
                    self.comment_text.setText(str(df['comment']))
                    self.content_text.setText("{}\n{}".format(df['question'], df['content']))
                self.totalindex = i
                is_operate = True
                self._setLabel()
                break
            else:
                continue
        if is_operate == False:
            self._showMessage(message="文件为空或者文件已经标注完")

    def _loadData(self):
        try:
            nums = self.nums
            if nums == 0:
                is_operate = False
            else:
                i = self.totalindex
                df = self.data.iloc[i]
                f1, f2, f3, f4, f5, f6, f7, f8 = df['sarcasm'], df['metaphor'], df['exaggeration'], df['homophonic'], df[
                    'symbolism'], df['emotion'], df['sentiment'], df['other_subtext']
                if pd.isnull(f1) or pd.isnull(f2) or pd.isnull(f3) or pd.isnull(f4) or pd.isnull(f5) or pd.isnull(
                        f7) or pd.isnull(f8):
                    self._resetSelection()
                else:
                    self.sarcasm = self._splitAndFillTxt(f1, [[self.radio11, self.radio12, self.radio13], self.inputtext_1])
                    self.metaphor = self._splitAndFillTxt(f2, [[self.radio21, self.radio22, self.radio23], self.inputtext_21, self.inputtext_22])
                    self.exaggeration = self._splitAndFillTxt(f3, [[self.radio31, self.radio32, self.radio33], self.inputtext_3])
                    self.homophonic = self._splitAndFillTxt(f4, [[self.radio41, self.radio42, self.radio43], self.inputtext_41, self.inputtext_42])
                    self.symbolism = self._splitAndFillTxt(f5, [[self.radio51, self.radio52, self.radio53], self.inputtext_51, self.inputtext_52])
                    [self.radio71, self.radio72, self.radio73][self._helper(f7)].setChecked(True)
                    self.sentiment = str(int(f7))
                    self.input_8.setText(f8 if f8 !='-' else '')
                    cb_index = self.emotion_dict[f6]
                    self.cb_6.setCurrentIndex(cb_index)
                    self.emotion_value = f6
                if 'question' not in self.data.columns:
                    self.comment_text.setText(str(df['comment']))
                    self.content_text.setText("{}".format(df['content']))
                else:
                    self.comment_text.setText(str(df['comment']))
                    self.content_text.setText("{}\n{}".format(df['question'], df['content']))
                # print(self.inputtext_1.text())
                is_operate = True
                self._setLabel()
            if is_operate == False:
                self._showMessage(message="文件为空或者文件已经标注完")
        except Exception as e:
            print(e)

    def _splitAndFillTxt(self, text, kongjian):
        label_text = text.split(';')
        nums = len(label_text)
        kongjian[0][self._helper(label_text[0])].setChecked(True)
        for i in range(nums - 1):
            kongjian[i+1].setText(label_text[i+1] if label_text[i+1] != '-' else '')
        return label_text[0]

    def _helper(self, flag):
        flag = str(int(flag))
        if flag == '1':
            return 0
        elif flag == '-1':
            return 1
        elif flag == '0':
            return 2


    def suanqian(self):
        self.nums += 1
        self.current_qian = self.nums * 5
        self.caifu.setText("财富：{} 毛".format(self.current_qian))

    def _clickNext(self):
        flag = self._saveDataJust()
        if flag == True:
            if self.totalindex + 1 >= self.data.shape[0]:
                self._showMessage(message="文件已经标注完")
                return
            self._tricks()
            self.suanqian()
            self.totalindex += 1
            # self._showData()
            self._loadData()
            self.save_curr_flag = False
            if (self.totalindex+1) % 10 == 0:
                self._saveToFile()

    def _clickJump(self):
        flag = self._saveDataJust(nextOrNot=False)
        index = self.index.text()
        if index.isdigit():
            index = int(index)
            if index < 0:
                self._showMessage(message="跳转输入必须是正整数")
            elif index > self.nums:
                self._showMessage(message="跳转过头了呢")
            else:
                self.totalindex = index
        else:
            self._showMessage(message="跳转输入必须是整数")
        #
        self.index.setText("")
        self._loadData()
        # self._resetSelection()
        self.save_curr_flag = False


    def _showMessage(self, message):
        QtWidgets.QMessageBox.information(self, "信息提示框", message, QtWidgets.QMessageBox.Yes)

    def _setLabel(self):
        self.curr_label.setText("当前条:{}".format(self.totalindex))

    def _saveDataJust(self, nextOrNot=True):
        if self.data is None:
            self._showMessage(message="请选择并打开文件")
            return False
        if self.save_curr_flag == True:
            return True
        l1, sent1 = self.sarcasm, self.inputtext_1.text()
        f1, data1 = self._constructor(l1, sents=sent1, flag=2)
        l2, sent21, sent22 = self.metaphor, self.inputtext_21.text(), self.inputtext_22.text()
        f2, data2 = self._constructor(l2, sents=sent21, sents2=sent22, flag=3)
        l3, sent3 = self.exaggeration, self.inputtext_3.text()
        f3, data3 = self._constructor(l3, sents=sent3, flag=2)
        l4, sent41, sent42 = self.homophonic, self.inputtext_41.text(), self.inputtext_42.text()
        f4, data4 = self._constructor(l4, sents=sent41, sents2=sent42, flag=3)
        l5, sent51, sent52 = self.symbolism, self.inputtext_51.text(), self.inputtext_52.text()
        f5, data5 = self._constructor(l5, sents=sent51, sents2=sent52, flag=3)
        data6 = self.emotion_value
        f7, data7 = self._constructor(self.sentiment, flag=1)
        data8 = self.input_8.text() if self.input_8.text() != "" else "-"
        # print(data1, data2, data3, data4, data5, data6, data7, data8)
        if f1 and f2 and f3 and f4 and f5 and f7:
            self.data.loc[self.data_index[self.totalindex], 'sarcasm'] = data1
            self.data.loc[self.data_index[self.totalindex], 'metaphor'] = data2
            self.data.loc[self.data_index[self.totalindex], 'exaggeration'] = data3
            self.data.loc[self.data_index[self.totalindex], 'homophonic'] = data4
            self.data.loc[self.data_index[self.totalindex], 'symbolism'] = data5
            self.data.loc[self.data_index[self.totalindex], 'emotion'] = data6
            self.data.loc[self.data_index[self.totalindex], 'sentiment'] = data7
            self.data.loc[self.data_index[self.totalindex], 'other_subtext'] = data8
            self.save_curr_flag = True
            return True
        if nextOrNot is False:
            return True
        self._showMessage(message="输入不符合格式")
        return False

    def _saveData(self):
        if self.data is None:
            self._showMessage(message="请选择并打开文件")
            return False
        if self.save_curr_flag == True:
            return True
        l1, sent1 = self.sarcasm, self.inputtext_1.text()
        f1, data1 = self._constructor(l1, sents=sent1, flag=2)
        l2, sent21, sent22 = self.metaphor, self.inputtext_21.text(), self.inputtext_22.text()
        f2, data2 = self._constructor(l2, sents=sent21, sents2=sent22, flag=3)
        l3, sent3 = self.exaggeration, self.inputtext_3.text()
        f3, data3 = self._constructor(l3, sents=sent3, flag=2)
        l4, sent41, sent42 = self.homophonic, self.inputtext_41.text(), self.inputtext_42.text()
        f4, data4 = self._constructor(l4, sents=sent41, sents2=sent42, flag=3)
        l5, sent51, sent52 = self.symbolism, self.inputtext_51.text(), self.inputtext_52.text()
        f5, data5 = self._constructor(l5, sents=sent51, sents2=sent52, flag=3)
        data6 = self.emotion_value
        f7, data7 = self._constructor(self.sentiment, flag=1)
        data8 = self.input_8.text() if self.input_8.text() != "" else "-"
        # print(data1, data2, data3, data4, data5, data6, data7, data8)
        if f1 and f2 and f3 and f4 and f5 and f7:
            self.data.loc[self.data_index[self.totalindex],'sarcasm'] = data1
            self.data.loc[self.data_index[self.totalindex],'metaphor'] = data2
            self.data.loc[self.data_index[self.totalindex], 'exaggeration'] = data3
            self.data.loc[self.data_index[self.totalindex], 'homophonic'] = data4
            self.data.loc[self.data_index[self.totalindex], 'symbolism'] = data5
            self.data.loc[self.data_index[self.totalindex], 'emotion'] = data6
            self.data.loc[self.data_index[self.totalindex], 'sentiment'] = data7
            self.data.loc[self.data_index[self.totalindex], 'other_subtext'] = data8
            self.save_curr_flag = True
            self._saveToFile()
            return True
        self._showMessage(message="输入不符合格式")
        return False

    def rbclicked(self):
        sender = self.sender()
        if sender == self.bg1:
            self.sarcasm = self.radio_list[self.bg1.checkedId()]
        elif sender == self.bg2:
            self.metaphor = self.radio_list[self.bg2.checkedId()]
        elif sender == self.bg3:
            self.exaggeration = self.radio_list[self.bg3.checkedId()]
        elif sender == self.bg4:
            self.homophonic = self.radio_list[self.bg4.checkedId()]
        elif sender == self.bg5:
            self.symbolism = self.radio_list[self.bg5.checkedId()]
        elif sender == self.bg7:
            self.sentiment = self.radio_list[self.bg7.checkedId()]


    def _saveToFile(self):
        self.data.to_csv(self.file_name, index=False)

    def _constructor(self, label, sents=None, flag=2, sents2=None):
        if label not in ["-1", "0", "1"]:
            return False, None
        if flag == 2:
            sents = "-" if label == "-1" or label == '0' else sents
            sents = "-" if label == "1" and sents == "" else sents
            return True, "{};{}".format(label, sents)
        elif flag == 3:
            sents = "-" if label == "-1" or label == '0' else sents
            sents2 = "-" if label == "-1" or label == '0' else sents2
            sents = "-" if label == "1" and sents == "" else sents
            sents2 = "-" if label == "1" and sents2 == "" else sents2

            return True, "{};{};{}".format(label, sents, sents2)
        else:
            return True, str(label)+" "

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '信息', '确认退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print("save")
            self._saveToFile()
        else:
            event.ignore()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())

    # import sys
    # sys.setrecursionlimit(10000)