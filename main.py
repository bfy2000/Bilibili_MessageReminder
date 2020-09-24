import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QCheckBox, QListWidgetItem, QAbstractItemView
from PyQt5 import QtCore,QtWidgets
from PyQt5.Qt import QThread
from functools import partial
import time
import widget
import driver_spider
import sqlite3
import traceback
import NoteEdit
import TitleEdit
import SetColName
import datetime
from customize_class import ListItem_with_id,ListItem_with_content


# load messages with spider based on webdriver

info_list = {}
reversed_info_list = {}
all_rec_list=[]


def load_info():
    global info_list
    info_list = driver_spider.get_message()

# set logic functions in mainwindow

class NewCheckBox(QCheckBox):
    def __init__(self,param,content):
        super().__init__(param)
        self.content=content

    def mouseDoubleClickEvent(self,QMouseEvent):
        QMessageBox.about(Mainwindow, '详细内容', self.content)

def show_raw_msg(item):
    user_str = item.text()
    Mainwindow_ui.Msginfo.clear()
    for msg in info_list[user_str]:
        box = NewCheckBox(msg.replace("\n", ";;"),msg)
        item = ListItem_with_content(msg)
        item.setSizeHint(QtCore.QSize(20, 50))
        Mainwindow_ui.Msginfo.addItem(item)
        Mainwindow_ui.Msginfo.setItemWidget(item, box)

def show_raw_record(page,item):
    full_rec="USER: {}\nTITLE: {}\nCONTENT: {}\nNOTE: {}\nTIME: {}".format(item.USER,item.TITLE,item.CONTENT,item.NOTE,item.TIME)
    eval("Mainwindow_ui.detail{}.setText(full_rec)".format(page))



def delete_rec(page):

    reclist_widget = eval("Mainwindow_ui.msg_page{}".format(page))
    reclist = list(reclist_widget.selectedItems())
    try:
        for item in reclist:
            #数据库删除
            cur.execute(
                "delete from column{} where id={}".format(page, item.ID))
            sqlconnection.commit()
            #列表删除
            reclist_widget.takeItem(reclist_widget.row(item))

            eval("Mainwindow_ui.detail{}.clear()".format(page))

    except BaseException as ex:
        QMessageBox.about(Mainwindow, '咋回事', '删不掉啊，溜了溜了')
        traceback.print_exc()
        sqlconnection.rollback()

def add_note():
    Mainwindow.setEnabled(False)
    Noteedit.show()

def add_title():
    Mainwindow.setEnabled(False)
    Titleedit.show()

def get_title():
    try:
        new_title=Titleedit_ui.TitleContent.toPlainText()

        #若新标题为空
        if new_title=="" :
            QMessageBox.about(Mainwindow, '怎么个意思？', '好家伙，好歹给事件起个标题吧？')
            Mainwindow.setEnabled(True)
            return

        page=Mainwindow_ui.tabWidget.currentIndex()
        SelectedItem = eval("Mainwindow_ui.msg_page{}.currentItem()".format(page))

        if not SelectedItem:
            QMessageBox.about(Mainwindow, '？？', "什么都没选，添加个锤子")
            Mainwindow.setEnabled(True)
            Titleedit_ui.TitleContent.setText("")
            return

        #更新数据库
        cur.execute("update column{} set title=\"{}\" where id={}".format(page,new_title,SelectedItem.ID))
        sqlconnection.commit()
        #更新显示
        SelectedItem.TITLE=new_title
        show_raw_record(page,SelectedItem)
        Titleedit_ui.TitleContent.setText("")
        Mainwindow.setEnabled(True)
        SelectedItem.setText(new_title)
    except BaseException as ex:
        traceback.print_exc()
        Mainwindow.setEnabled(True)
        sqlconnection.rollback()


def get_note():
    try:
        new_note=Noteedit_ui.NoteContent.toPlainText()
        page=Mainwindow_ui.tabWidget.currentIndex()
        SelectedItem=eval("Mainwindow_ui.msg_page{}.currentItem()".format(page))

        if not SelectedItem:
            QMessageBox.about(Mainwindow, '？？', "什么都没选，添加个锤子")
            Mainwindow.setEnabled(True)
            Titleedit_ui.TitleContent.setText("")
            return

        #更新数据库
        cur.execute("update column{} set note=\"{}\" where id={}".format(page,new_note,SelectedItem.ID))
        sqlconnection.commit()
        #更新显示
        SelectedItem.NOTE=new_note
        show_raw_record(page,SelectedItem)
        Noteedit_ui.NoteContent.setText("")
        Mainwindow.setEnabled(True)
    except BaseException as ex:
        traceback.print_exc()
        Mainwindow.setEnabled(True)
        sqlconnection.rollback()

def free_mainwindow():
    Mainwindow.setEnabled(True)

def get_col_name():
    Colrename_ui.PageSelect.setCurrentIndex(0)
    Colrename.show()
    

def set_col_name():
    try:
        page=Colrename_ui.PageSelect.currentIndex()
        page+=1
        new_name=Colrename_ui.textEdit.toPlainText()
        cur.execute("update column_name set c{}_name=\"{}\"".format(page,new_name))
        sqlconnection.commit()
        Mainwindow_ui.tabWidget.setTabText(page,new_name)
        Colrename_ui.textEdit.setText("")
    except BaseException as ex:
        traceback.print_exc()
        sqlconnection.rollback()



def set_Dialog():
    Noteedit.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    Titleedit.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    Colrename.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    Noteedit_ui.CommitNote.accepted.connect(get_note)
    Titleedit_ui.CommitTitle.accepted.connect(get_title)
    Noteedit_ui.CommitNote.rejected.connect(free_mainwindow)
    Titleedit_ui.CommitTitle.rejected.connect(free_mainwindow)

    Colrename_ui.CommitChange.clicked.connect(set_col_name)


def show_msg_text(item):
    QMessageBox.about(Mainwindow, '详细内容', item.CONTENT)


def set_Mainwindow():

    # function of userlist 
    Mainwindow_ui.Userlist.itemClicked.connect(show_raw_msg)
    Mainwindow_ui.Addtopage.clicked.connect(add_to_page)
    Mainwindow_ui.Loadspider.clicked.connect(load_spider_btn)
    Mainwindow_ui.Msginfo.itemDoubleClicked.connect(show_msg_text)

    #透明度
    op = QtWidgets.QGraphicsOpacityEffect()
    op.setOpacity(0.8)
    Mainwindow_ui.tabWidget.setGraphicsEffect(op)
    Mainwindow_ui.tabWidget.setAutoFillBackground(True)

    
    global all_rec_list

    # function of loading records from database

    try:
        tabnames = list(cur.execute("select * from column_name"))
    except BaseException as ex:
        traceback.print_exc()
        sqlconnection.rollback()


    for i in range(1,10):
        try:
            
            #设置每页的名称,实际只有一行
            Mainwindow_ui.tabWidget.setTabText(i, tabnames[0][i-1])
            

            #每页的记录表
            reclist = eval("Mainwindow_ui.msg_page{}".format(i))

            #记录表改成多选模式
            reclist.setSelectionMode(
                QAbstractItemView.ExtendedSelection)

            #记录表项点击事件
            reclist.itemClicked.connect(partial(show_raw_record,i))

            #删除按钮点击事件
            eval("Mainwindow_ui.deleteRec{}.clicked.connect(partial(delete_rec,{}))".format(i,i))

            eval("Mainwindow_ui.Addnote{}.clicked.connect(add_note)".format(i))
            eval("Mainwindow_ui.Addtitle{}.clicked.connect(add_title)".format(i))


            #显示初始数据
            select_res = cur.execute(
                "SELECT id,user,title,note,content,time from column{} ".format(i))
            for row in select_res:
                item = ListItem_with_id(
                    row[0], row[1], row[2], row[3], row[4], row[5],)
                item.setSizeHint(QtCore.QSize(20, 40))
                reclist.addItem(item)

            #设置菜单
            Mainwindow_ui.rename_column.triggered.connect(get_col_name)

                
        except:
            traceback.print_exc()
            sqlconnection.rollback()



# load spider info


def load_spider_btn():
    Mainwindow.thread_1=Thread_1()
    Mainwindow.thread_1.start()

    

# Set logic functions in startup dialog


def add_to_page():
    msg_count = Mainwindow_ui.Msginfo.count()  # 得到每个人消息的条数
    cb_list = [Mainwindow_ui.Msginfo.itemWidget(Mainwindow_ui.Msginfo.item(i))
               for i in range(msg_count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox

    Curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if len(cb_list) == 0 :
        QMessageBox.about(Mainwindow, '干啥呢？', '在？什么都不选添加个锤子？')
        return

    #page number
    page_num=Mainwindow_ui.Pageselect.currentText()[4:5]

    #get id
    res_maxid = cur.execute("SELECT max_id  from MAXID")
    maxid=0
    for row in res_maxid:
        maxid=row[0]
    curr_id=maxid
    #get username
    username = list(Mainwindow_ui.Userlist.selectedItems())[0].text()


    try:
        for cb in cb_list:  # type:QCheckBox
            if cb.isChecked():

                #get content
                content=cb.text().replace(";;","\n")

                #set title
                title=''
                if len(cb_list)>16:
                    title=content[0:16].replace('\n',' ')
                else:
                    title=content.replace('\n',' ')

                cur.execute("INSERT INTO column{0} (id,user,title,note,content,time) VALUES ({1}, \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\" )".format(page_num, curr_id, username, title,'还没有备注！', content, Curr_time))

                sqlconnection.commit()

                curr_id+=1

                # 把记录放过去
                reclist=eval("Mainwindow_ui.msg_page{}".format(page_num))
                
                item=ListItem_with_id(curr_id,username,title,"还没有记录！",content,Curr_time)
                item.setSizeHint(QtCore.QSize(20, 40))
                reclist.addItem(item)

        cur.execute("UPDATE MAXID set max_id = {} ".format(curr_id))
        sqlconnection.commit()
        
    except BaseException as ex:
        traceback.print_exc()
        sqlconnection.rollback()

        cur.execute("UPDATE MAXID set max_id = {} ".format(curr_id))
        sqlconnection.commit()

        QMessageBox.about(Mainwindow, '危', '部分记录已存在，请勿重复插入')


class NewDialog(QDialog):
    def closeEvent(self, event):
        Mainwindow.setEnabled(True)
        event.accept()


class Thread_1(QThread):  # 线程1
    def __init__(self):
        super().__init__()

    def run(self):
        load_info()
        # info_list['user1'] = ['1222', 'a安全网若a', '223333去玩儿33333']
        # info_list['user2'] = ['1123512', 'aaaa请问二吞吞吐吐a', '2233231咕咕咕333333']
        # info_list['user3'] = ['121341232122', 'aaaa高个体户a', '22333333热发发发333']
        # info_list['user4'] = ['11231231222', 'aaa344盖个盖aa', '2233333为取翁群翁3333']
        # info_list['user5'] = ['12131231231222', 'aaa退欧11aa', '2233其他应用3333333']
        # show users list
        for user in info_list:
            user_name = QListWidgetItem(user)
            user_name.setSizeHint(QtCore.QSize(20, 50))
            Mainwindow_ui.Userlist.addItem(user_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create Mainwindow
    Mainwindow = QMainWindow()
    Mainwindow_ui = widget.Ui_MainWindow()
    Mainwindow_ui.setupUi(Mainwindow)
    #Create TitleEdit Dialog
    Titleedit=NewDialog()
    Titleedit_ui=TitleEdit.Ui_Dialog()
    Titleedit_ui.setupUi(Titleedit)
    #Create NoteEdit Dialog
    Noteedit=NewDialog()
    Noteedit_ui=NoteEdit.Ui_Remark()
    Noteedit_ui.setupUi(Noteedit)
    #Create Column Rename Dialog
    Colrename=NewDialog()
    Colrename_ui=SetColName.Ui_Dialog()
    Colrename_ui.setupUi(Colrename)


    sqlconnection = sqlite3.connect('backup.db')
    cur = sqlconnection.cursor()

    # for i in range(1,10):
    #     cur.execute("""CREATE TABLE column{}
    #                 (id     INT PRIMARY KEY  NOT NULL,
    #                 user    TEXT  NOT NULL,
    #                 title   TEXT  NOT NULL,
    #                 note    TEXT,
    #                 content  TEXT,
    #                 time   TEXT)""".format(i))
    # cur.execute("CREATE TABLE MAXID (max_id int primary key not null)")
    # cur.execute("INSERT INTO MAXID (max_id) VALUES (0) ")
    # cur.execute("UPDATE MAXID set max_id = 2 ")
    # cur.execute("delete from column1 ")
    # cur.execute("delete from column2 ")
    # cur.execute("delete from column3 ")
    # cur.execute("delete from column4 ")
    # cur.execute("delete from column5 ")
    # cur.execute("delete from column6 ")
    # cur.execute("delete from column7 ")
    # cur.execute("delete from column8 ")
    # cur.execute("delete from column9 ")
    # sqlconnection.commit()

    # cur.execute("""CREATE TABLE column_name
    #             (c1_name  TEXT  NOT NULL,
    #             c2_name  TEXT  NOT NULL,
    #             c3_name  TEXT  NOT NULL,
    #             c4_name  TEXT  NOT NULL,
    #             c5_name  TEXT  NOT NULL,
    #             c6_name  TEXT  NOT NULL,
    #             c7_name  TEXT  NOT NULL,
    #             c8_name  TEXT  NOT NULL,
    #             c9_name  TEXT  NOT NULL)""")

    # cur.execute("insert into column_name (c1_name,c2_name,c3_name,c4_name,c5_name,c6_name,c7_name,c8_name,c9_name) values (\"page1\",\"page2\",\"page3\",\"page4\",\"page5\",\"page6\",\"page7\",\"page8\",\"page9\")")
    # sqlconnection.commit()

    set_Dialog()
    set_Mainwindow()
    Mainwindow.show()
    app.exec_()

    cur.close()
    sqlconnection.close()


    

