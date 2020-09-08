from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import mysql.connector
from reportab.pdfgen import canvas

"""conexao ao banco de dados"""

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_controle"
)





def novo_cadastro():
    categoria = ''
    item = cadastro.lineEdit.text()
    descricao = cadastro.lineEdit_2.text()
    valor = cadastro.lineEdit_4.text()
    data_temp = cadastro.dateEdit.date()
    data = (data_temp.toPyDate()).strftime('%d/%m/%Y')
    
    if len(item) == 0:
        QMessageBox.about(cadastro, 'ERRO', 'Campo ITEM em branco!')
    
    elif len(valor) == 0:
        QMessageBox.about(cadastro, 'ERRO', 'Campo VALOR em branco!')
    
    elif cadastro.radioButton.isChecked():
        categoria = 'Gastos pessoais'
    elif cadastro.radioButton_2.isChecked():
        categoria = 'Motocicleta'
    elif cadastro.radioButton_3.isChecked():
        categoria = 'Despesas'
    elif cadastro.radioButton_4.isChecked():
        categoria = 'Outros'
    else:
        QMessageBox.about(cadastro, 'ERRO', 'DADOS INCOMPLETOS!')
        sys.exit()
        
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO controle (item, descricao, valor, categoria, data) VALUES (%s, %s, %s, %s, %s)"
    dados = (str(item) , str(descricao), str(valor), str(categoria), str(data))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    

def sair():
    sys.exit()


def gerar_pdf():
    print('pdf')
    


def segunda_tela():
    listar_dados.show()
    listar_dados.pushButton.clicked.connect(sair)
    listar_dados.pushButton_2.clicked.connect(gerar_pdf)

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM controle"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    listar_dados.tableWidget.setRowCount(len(dados_lidos))
    listar_dados.tableWidget.setColumnCount(6)

    for i in range(0,len(dados_lidos)):
        for j in range(0,6):
            listar_dados.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



app = QtWidgets.QApplication([])
cadastro = uic.loadUi('cadastro.ui')
listar_dados = uic.loadUi('listar.ui')
cadastro.pushButton.clicked.connect(novo_cadastro)
cadastro.pushButton_2.clicked.connect(segunda_tela)

cadastro.show()
app.exec()
