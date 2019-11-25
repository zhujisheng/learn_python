from PyQt5 import uic
from PyQt5.QtWidgets import *
from bit.network import NetworkAPI

def get_account():
    myWin.treeWidget.setHidden(True)
    myWin.pushButton.setEnabled(False)
    myWin.label_2.setText( '查询中......' )

    addr = myWin.lineEdit.text()
    unspents = NetworkAPI.get_unspent(addr)
    myWin.pushButton.setEnabled(True)
    if len(unspents)==0:
        myWin.label_2.setText( '<html><head/><body><p><span style=" color:#00aa00;">0</span></p></body></html>' )
    else:
        myWin.treeWidget.clear()
        myWin.treeWidget.setHidden(False)
        s=sum(unspent.amount for unspent in unspents)
        myWin.label_2.setText( '<html><head/><body><p><span style=" color:#00aa00;">%d</span></p></body></html>'%(s) )
        for utxo in unspents:
            root=QTreeWidgetItem(myWin.treeWidget)
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

myWin = uic.loadUi("bitcoin_alpha.ui")
myWin.show()

myWin.pushButton.clicked.connect(get_account)

app.exec_()
