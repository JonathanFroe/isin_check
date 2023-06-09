import database

import pandas as pd
from pandas.io import clipboard
import shutil
from sys import exit


length_isin = 12
delta_days = 1

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
import sys
import design
from os.path import exists

import threading
class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.sortedby = "isin"
        self.sorted_desc = False
        ok = self.load_action(first_load=True)
        if ok:
            self.setupUi(self)
            self.data()
        else:
            exit(0)

    def load_action(self, first_load=False):
        ok = False
        if exists("config-isincheck.conf") and first_load:
            with open("config-isincheck.conf", 'r') as fi:
                self.filename = fi.read()
            if exists(self.filename):
                ok = True
        if ok is False:
            self.filename = ""
            self.filename, ok = QtWidgets.QFileDialog.getOpenFileName(self, "Load database (Press >Cancle< to create new one)", "" , "SQLite files (*.db)")
            if self.filename == "":
                self.filename, ok = QtWidgets.QFileDialog.getSaveFileName(self, "Create new database", "" , "SQLite files (*.db)")
            with open("config-isincheck.conf", 'w') as fi:
                fi.write(self.filename)
        database.close_db()
        database.init_db(self.filename)
        if not first_load:
            self.refreshbutton_action()
        return ok
    
    def save_as_action(self):
        new_filename, ok = QtWidgets.QFileDialog.getSaveFileName(self, "Save database", "" , "SQLite files (*.db)")
        if ok:
            database.close_db()
            shutil.move(self.filename, new_filename)
            self.filename = new_filename
            database.init_db(self.filename)
            with open("config-isincheck.conf", 'w') as fi:
                fi.write(self.filename)
            
    def addbutton_action(self):
        isin, ok = QtWidgets.QInputDialog.getText(self, "Add ISIN", "Enter ISIN: ")
        self.progress.setValue(0)
        if ok and len(isin)==length_isin:
            task = threading.Thread(target=self.do_update_task, args=(isin, 1,))
            task.start()
        
    def addmultiplebutton_action(self):
        isins, ok = QtWidgets.QInputDialog.getMultiLineText(self, "Add ISINs", "Enter ISINs (With newline seperated!): ")
        self.progress.setValue(0)
        if ok and len(isins)>0:
            isin_list = isins.replace(" ", "").splitlines()
            for isin_number in range(len(isin_list)):
                isin = isin_list[isin_number]
                if len(isin) == length_isin:
                    task = threading.Thread(target=self.do_update_task, args=(isin, len(isin_list),))
                    task.start()
        
    def editbutton_action(self):
        tagnumber, ok = QtWidgets.QInputDialog.getInt(self, "Which Tag", "Enter Number (1-3)")
        if tagnumber >=1 and tagnumber <=3 and ok:
            new_tag, ok = QtWidgets.QInputDialog.getText(self, "Change Tag", "Enter new Tag: ")
            if ok:
                for index in self.tableWidget.selectedIndexes():
                    isin = self.tableWidget.item(index.row(), 0).text()
                    database.change_tag_in_database(isin, new_tag, tagnumber)
            self.refreshbutton_action()
            
    def onCellDoubleClicked(self, row, column):
        print(self.tableWidget.item(row, column).text())
        msgbx = QtWidgets.QMessageBox
        clipboard.copy(self.tableWidget.item(row, column).text())
        msgbx.information(self, "Copied", "'" + self.tableWidget.item(row, column).text() + "'" + " was copied to clipboard", msgbx.Ok)
        
        
    def deletebutton_action(self):
        self.progress.setValue(0)
        qm = QtWidgets.QMessageBox
        ret = qm.question(self, "Delete", "Are you sure to delete %s objects?"%str(len(self.tableWidget.selectedIndexes())), qm.Yes | qm.No)
        if ret == qm.Yes:
            for index in self.tableWidget.selectedIndexes():
                isin = self.tableWidget.item(index.row(), 0).text()
                database.delete_from_database(isin)
            self.progress.setValue(100)
        self.refreshbutton_action()
    
    def refreshbutton_action(self):
        self.data()
       
       
    def do_update_task(self, isin, taskcount):
        database.update_in_database(isin)
        print("updated:" + isin)
        print(str(100-(threading.active_count()-2)/taskcount*100)+"%")
        self.progress.setValue(100-int((threading.active_count()-2)/taskcount*100)) # get status of update by the count of threads 
        
    
    def updateallbutton_action(self):
        self.progress.setValue(0)
        isins = database.get_all_data(self.sortedby, self.sorted_desc)
        if isins is None:
            return False
        for isin_number in range(len(isins)):
            isin = isins[isin_number]
            task = threading.Thread(target=self.do_update_task, args=(isin.isin, len(isins),))
            task.start()         
        
    def updatebutton_action(self):
        self.progress.setValue(0)
        indexes = self.tableWidget.selectedIndexes()
        if indexes is None:
            return False
        for index_number in range(len(indexes)):
            index = indexes[index_number]
            isin = self.tableWidget.item(index.row(), 0).text()
            task = threading.Thread(target=self.do_update_task, args=(isin, len(indexes),))
            task.start()
              
    def to_dict(self, row):
        if row is None:
            return None

        rtn_dict = dict()
        keys = row.__table__.columns.keys()
        for key in keys:
            rtn_dict[key] = getattr(row, key)
        return rtn_dict

    def exportbutton_action(self):
        filename, ok = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "" , "Excel files (*.xlsx)")
        if ok:
            data = database.get_all_data(self.sortedby, self.sorted_desc)
            data_list = [self.to_dict(item) for item in data]
            df = pd.DataFrame(data_list)
            df.drop(df.columns[[16]], axis=1)
            writer = pd.ExcelWriter(filename)
            df.to_excel(writer,  index=False)
            writer.save()

    def show_Info_action(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("This App was made and is owned by Jonathan Fröhlich. This is a private Project. Do not distribute this software!")
        msgBox.setWindowTitle("Information about this App")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()
    
    def sortbylist_action(self, item):
        text = item.text()
        print(self.sorted_desc)
        if text == "ISIN":
            if self.sortedby == "isin":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "isin"
        if text == "WKN":
            if self.sortedby == "wkn":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "wkn"
        if text == "Name":
            if self.sortedby == "name":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "name"
        if text == "URL":
            if self.sortedby == "url":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "url"
        if text == "Vola 1m":
            if self.sortedby == "vola_1m":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "vola_1m"
        if text == "Vola 3m":
            if self.sortedby == "vola_3m":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "vola_3m"
        if text == "Vola 1y":
            if self.sortedby == "vola_1y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "vola_1y"
        if text == "Vola 3y":
            if self.sortedby == "vola_3y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "vola_3y"
        if text == "Vola 5y":
            if self.sortedby == "vola_5y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "vola_5y"
        if text == "Vola 10y":
            if self.sortedby == "vola_10y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "vola_10y"
        if text == "Perf 1m":
            if self.sortedby == "perf_1m":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "perf_1m"
        if text == "Perf 3m":
            if self.sortedby == "perf_3m":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "perf_3m"
        if text == "Perf 1y":
            if self.sortedby == "perf_1y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "perf_1y"
        if text == "Perf 3y":
            if self.sortedby == "perf_3y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "perf_3y"
        if text == "Perf 5y":
            if self.sortedby == "perf_5y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "perf_5y"
        if text == "Perf 10y":
            if self.sortedby == "perf_10y":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "perf_10y"
        if text == "Tag1":
            if self.sortedby == "tag1":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "tag1"
        if text == "Tag2":
            if self.sortedby == "tag2":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "tag2"
        if text == "Tag3":
            if self.sortedby == "tag3":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "tag3"
        if text == "Last Update":
            if self.sortedby == "lastupdate":
                self.sorted_desc = not self.sorted_desc
            self.sortedby = "lastupdate"
        self.data()
    
    def data(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(20)
        
        self.tableWidget.setHorizontalHeaderLabels(['ISIN', 'WKN', 'Name', 'URL', 'Vola 1m', 'Vola 3m', 'Vola 1y', 'Vola 3y', 'Vola 5y', 'Vola 10y', 'Perf 1m', 'Perf 3m', 'Perf 1y', 'Perf 3y', 'Perf 5y', 'Perf 10y', 'Tag1', 'Tag2', 'Tag3', 'Last Update'])
        
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        
        data = database.get_all_data(self.sortedby, self.sorted_desc)
        self.tableWidget.setRowCount(len(data))
        for element_number in range(len(data)):
            element = data[element_number]
            self.tableWidget.setItem(element_number,0, QtWidgets.QTableWidgetItem(element.isin))
            self.tableWidget.setItem(element_number,1, QtWidgets.QTableWidgetItem(element.wkn))
            self.tableWidget.setItem(element_number,2, QtWidgets.QTableWidgetItem(element.name))
            self.tableWidget.setItem(element_number,3, QtWidgets.QTableWidgetItem(element.url))
            self.tableWidget.setItem(element_number,4, QtWidgets.QTableWidgetItem(str(element.vola_1m)))
            self.tableWidget.setItem(element_number,5, QtWidgets.QTableWidgetItem(str(element.vola_3m)))
            self.tableWidget.setItem(element_number,6, QtWidgets.QTableWidgetItem(str(element.vola_1y)))
            self.tableWidget.setItem(element_number,7, QtWidgets.QTableWidgetItem(str(element.vola_3y)))
            self.tableWidget.setItem(element_number,8, QtWidgets.QTableWidgetItem(str(element.vola_5y)))
            self.tableWidget.setItem(element_number,9, QtWidgets.QTableWidgetItem(str(element.vola_10y)))
            self.tableWidget.setItem(element_number,10, QtWidgets.QTableWidgetItem(str(element.perf_1m)))
            self.tableWidget.setItem(element_number,11, QtWidgets.QTableWidgetItem(str(element.perf_3m)))
            self.tableWidget.setItem(element_number,12, QtWidgets.QTableWidgetItem(str(element.perf_1y)))
            self.tableWidget.setItem(element_number,13, QtWidgets.QTableWidgetItem(str(element.perf_3y)))
            self.tableWidget.setItem(element_number,14, QtWidgets.QTableWidgetItem(str(element.perf_5y)))
            self.tableWidget.setItem(element_number,15, QtWidgets.QTableWidgetItem(str(element.perf_10y)))
            self.tableWidget.setItem(element_number,16, QtWidgets.QTableWidgetItem(element.tag1))
            self.tableWidget.setItem(element_number,17, QtWidgets.QTableWidgetItem(element.tag2))
            self.tableWidget.setItem(element_number,18, QtWidgets.QTableWidgetItem(element.tag3))
            self.tableWidget.setItem(element_number,19, QtWidgets.QTableWidgetItem(str(element.lastupdate)))
  

def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()