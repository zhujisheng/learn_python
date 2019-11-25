from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bit.network import NetworkAPI

class MyWinClass(QMainWindow):

    def __init__(self):
        super().__init__()
        win = uic.loadUi("bitcoin_alpha.ui", self)
        win.show()
        self.pushButton.clicked.connect(self.get_account)

    def get_account(self):
        self.treeWidget.setHidden(True)
        self.pushButton.setEnabled(False)
        self.label_2.setText( '查询中......' )

        addr = self.lineEdit.text()
        unspents = NetworkAPI.get_unspent(addr)
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
