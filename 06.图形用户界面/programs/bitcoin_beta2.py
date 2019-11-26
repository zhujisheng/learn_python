from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bit.network import NetworkAPI
import threading

class MyWinClass(QMainWindow):

    # 一个自定义的信号
    sig_unspents_arrived = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        win = uic.loadUi("bitcoin_beta.ui", self)
        win.show()

    def get_account(self):
        # 查询中界面设置
        self.treeWidget.setHidden(True)
        self.pushButton.setEnabled(False)
        self.label_2.setText( '查询中......' )

        # 启动新的线程进行查询
        addr = self.lineEdit.text()
        t=threading.Thread(target=self.get_utxo,args=(addr,))
        t.start()

    def get_utxo(self, addr):
        """查询，当返回时发射信号sig_unspents_arrived"""
        unspents = NetworkAPI.get_unspent(addr)
        self.sig_unspents_arrived.emit(unspents)

    def handle_unspents_arrived(self, unspents):
        """根据查询结果调整界面显示"""
        self.pushButton.setEnabled(True)

        if len(unspents)==0:
            self.label_2.setText( '<html><head/><body><p><span style=" color:#00aa00;">0</span></p></body></html>' )
        else:
            self.treeWidget.clear()
            self.treeWidget.setHidden(False)
            s=sum(unspent.amount for unspent in unspents)
            self.label_2.setText( '<html><head/><body><p><span style=" color:#00aa00;">%d</span></p></body></html>'%(s) )
            for utxo in unspents:
                root=QTreeWidgetItem(self.treeWidget)
                root.setText(0,'amount')
                root.setText(1,str(utxo.amount))
                txid = QTreeWidgetItem(root)
                txid.setText(0,'txid')
                txid.setText(1,utxo.txid)
                txindex = QTreeWidgetItem(root)
                txindex.setText(0,'txindex')
                txindex.setText(1,str(utxo.txindex))
                script = QTreeWidgetItem(root)
                script.setText(0,'script')
                script.setText(1,utxo.script)
                confirmations = QTreeWidgetItem(root)
                confirmations.setText(0,'confirmations')
                confirmations.setText(1,str(utxo.confirmations))
                segwit = QTreeWidgetItem(root)
                segwit.setText(0,'segwit')
                segwit.setText(1,str(utxo.segwit))

app = QApplication([])
myWin = MyWinClass()

app.exec_()
