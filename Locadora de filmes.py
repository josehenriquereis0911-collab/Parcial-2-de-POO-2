from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QToolBar, QLineEdit, 
                               QTableWidget,QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QComboBox,QSpinBox, QDialogButtonBox, 
                                QHeaderView,QGroupBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QObject, QRunnable, QThreadPool, Signal, Slot
from datetime import date, timedelta

class Filme:

    def __init__(self, id_filme, titulo, genero, diretor, quantidade, classificacao):
        self.id = id_filme
        self.titulo = titulo
        self.genero = genero
        self.diretor = diretor
        self.quantidade = quantidade
        self.classificacao = classificacao

class Cliente:

    def __init__(self, id_cliente, nome, cpf, telefone, email):
        self.id = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email

class Locacao:

    def __init__(self, id_locacao, cliente, filme, data_locacao, data_prevista):
        self.id = id_locacao
        self.cliente = cliente
        self.filme = filme
        self.data_locacao = data_locacao
        self.data_prevista = data_prevista
        self.devolvida = False

class DialogoCadastroCliente(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Cliente")
        self.resize(420, 250)
        self.campo_nome = QLineEdit()
        self.campo_cpf = QLineEdit()
        self.campo_telefone = QLineEdit()
        self.campo_email = QLineEdit()
        formulario = QFormLayout()
        formulario.addRow("Nome:", self.campo_nome)
        formulario.addRow("CPF:", self.campo_cpf)
        formulario.addRow("Telefone:", self.campo_telefone)
        formulario.addRow("E-mail:", self.campo_email)
        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botoes.accepted.connect(self.validar_dados)
        botoes.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addLayout(formulario)
        layout.addWidget(botoes)
        self.setLayout(layout)

    def validar_dados(self):
        nome = self.campo_nome.text().strip()
        cpf = self.campo_cpf.text().strip()
        if nome == "":
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o nome do cliente."
            )
            self.campo_nome.setFocus()
            return
        if cpf == "":
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o CPF do cliente."
            )
            self.campo_cpf.setFocus()
            return
        janela = self.parent()
        if janela is not None and hasattr(janela, "lista_clientes"):
            for cliente in janela.lista_clientes:
                if cliente.cpf == cpf:
                    QMessageBox.warning(
                        self,
                        "CPF já cadastrado",
                        "Já existe um cliente cadastrado com esse CPF."
                    )
                    self.campo_cpf.setFocus()
                    return
        self.accept()

    def obter_dados(self):
        return {
            "nome": self.campo_nome.text().strip(),
            "cpf": self.campo_cpf.text().strip(),
            "telefone": self.campo_telefone.text().strip(),
            "email": self.campo_email.text().strip()
        }

class JanelaClientes(QMainWindow):

    def __init__(self, janela_principal):
        super().__init__()
        self.janela_principal = janela_principal
        self.setWindowTitle("Clientes")
        self.resize(800, 450)
        # QWidget central da QMainWindow
        central = QWidget()
        titulo = QLabel("Gerenciamento de Clientes")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 8px;"
        )
        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText(
            "Pesquisar por nome ou CPF..."
        )
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Nome", "CPF", "Telefone", "E-mail"]
        )
        self.tabela.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        self.tabela.setSelectionMode(
            QTableWidget.SingleSelection
        )
        self.tabela.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        botao_novo = QPushButton("Cadastrar cliente")
        botao_excluir = QPushButton("Excluir selecionado")
        botao_fechar = QPushButton("Fechar")
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(botao_novo)
        layout_botoes.addWidget(botao_excluir)
        layout_botoes.addStretch()
        layout_botoes.addWidget(botao_fechar)
        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.campo_pesquisa)
        layout.addWidget(self.tabela)
        layout.addLayout(layout_botoes)
        # QMainWindow precisa de um QWidget central
        central.setLayout(layout)
        self.setCentralWidget(central)
        # Sinais e slots
        botao_novo.clicked.connect(
            self.cadastrar_cliente
        )
        botao_excluir.clicked.connect(
            self.excluir_cliente
        )
        botao_fechar.clicked.connect(
            self.close
        )
        self.campo_pesquisa.textChanged.connect(
            self.atualizar_tabela
        )
        self.atualizar_tabela()

    def atualizar_tabela(self):
        texto = self.campo_pesquisa.text().strip().lower()
        clientes = self.janela_principal.lista_clientes
        if texto:
            clientes = [
                cliente for cliente in clientes
                if texto in cliente.nome.lower()
                or texto in cliente.cpf.lower()
            ]
        self.tabela.setRowCount(0)
        for cliente in clientes:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)
            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(str(cliente.id))
            )
            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(cliente.nome)
            )
            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(cliente.cpf)
            )
            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(cliente.telefone)
            )
            self.tabela.setItem(
                linha,
                4,
                QTableWidgetItem(cliente.email)
            )

    def cadastrar_cliente(self):
        dialogo = DialogoCadastroCliente(
            self.janela_principal
        )
        if dialogo.exec():
            dados = dialogo.obter_dados()
            novo_cliente = Cliente(
                self.janela_principal.proximo_id_cliente,
                dados["nome"],
                dados["cpf"],
                dados["telefone"],
                dados["email"]
            )
            self.janela_principal.lista_clientes.append(
                novo_cliente
            )
            self.janela_principal.proximo_id_cliente += 1
            self.atualizar_tabela()
            QMessageBox.information(
                self,
                "Cadastro realizado",
                "Cliente cadastrado com sucesso."
            )

    def excluir_cliente(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum cliente selecionado",
                "Selecione um cliente para excluir."
            )
            return
        id_cliente = int(
            self.tabela.item(linha, 0).text()
        )
        cliente = next(
            (
                c for c in self.janela_principal.lista_clientes
                if c.id == id_cliente
            ),
            None
        )
        if cliente is None:
            return
        possui_locacao_aberta = any(
            locacao.cliente.id == cliente.id
            and not locacao.devolvida
            for locacao in self.janela_principal.lista_locacoes
        )
        if possui_locacao_aberta:
            QMessageBox.warning(
                self,
                "Cliente com locação ativa",
                "Não é possível excluir um cliente que "
                "possui locação em aberto."
            )
            return
        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Deseja excluir o cliente '{cliente.nome}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            self.janela_principal.lista_clientes.remove(
                cliente
            )

class DialogoNovaLocacao(QDialog):

    def __init__(self, janela_principal, filme_preselecionado=None):
        super().__init__(janela_principal)
        self.janela_principal = janela_principal
        self.setWindowTitle("Nova Locação")
        self.resize(450, 260)
        self.combo_cliente = QComboBox()
        for cliente in janela_principal.lista_clientes:
            self.combo_cliente.addItem(
                f"{cliente.nome} - CPF: {cliente.cpf}",
                cliente.id
            )
        self.combo_filme = QComboBox()
        for filme in janela_principal.lista_filmes:
            if filme.quantidade > 0:
                self.combo_filme.addItem(
                    f"{filme.titulo} - disponíveis: {filme.quantidade}",
                    filme.id
                )
        if filme_preselecionado is not None:
            indice = self.combo_filme.findData(filme_preselecionado.id)
            if indice >= 0:
                self.combo_filme.setCurrentIndex(indice)
        self.campo_dias = QSpinBox()
        self.campo_dias.setMinimum(1)
        self.campo_dias.setMaximum(30)
        self.campo_dias.setValue(7)
        formulario = QFormLayout()
        formulario.addRow("Cliente:", self.combo_cliente)
        formulario.addRow("Filme:", self.combo_filme)
        formulario.addRow("Prazo (dias):", self.campo_dias)
        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addLayout(formulario)
        layout.addWidget(botoes)
        self.setLayout(layout)

    def obter_dados(self):
        return {
            "id_cliente": self.combo_cliente.currentData(),
            "id_filme": self.combo_filme.currentData(),
            "dias": self.campo_dias.value()
        }

class DialogoLocacoes(QDialog):

    def __init__(self, janela_principal):
        super().__init__(janela_principal)
        self.janela_principal = janela_principal
        self.setWindowTitle("Locações")
        self.resize(900, 480)
        titulo = QLabel("Gerenciamento de Locações")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px;")
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Cliente",
            "Filme",
            "Classificação",
            "Data da locação",
            "Devolução prevista",
            "Status",
            "CPF"
        ])
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        botao_nova = QPushButton("Nova locação")
        botao_devolver = QPushButton("Registrar devolução")
        botao_fechar = QPushButton("Fechar")
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(botao_nova)
        layout_botoes.addWidget(botao_devolver)
        layout_botoes.addStretch()
        layout_botoes.addWidget(botao_fechar)
        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.tabela)
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
        botao_nova.clicked.connect(self.nova_locacao)
        botao_devolver.clicked.connect(self.registrar_devolucao)
        botao_fechar.clicked.connect(self.accept)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.tabela.setRowCount(0)
        for locacao in self.janela_principal.lista_locacoes:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)
            status = "Devolvido" if locacao.devolvida else "Em aberto"
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(locacao.id)))
            self.tabela.setItem(linha, 1, QTableWidgetItem(locacao.cliente.nome))
            self.tabela.setItem(linha, 2, QTableWidgetItem(locacao.filme.titulo))
            self.tabela.setItem(linha, 3, QTableWidgetItem(locacao.filme.classificacao))
            self.tabela.setItem(
                linha, 4,
                QTableWidgetItem(locacao.data_locacao.strftime("%d/%m/%Y"))
            )
            self.tabela.setItem(
                linha, 5,
                QTableWidgetItem(locacao.data_prevista.strftime("%d/%m/%Y"))
            )
            self.tabela.setItem(linha, 6, QTableWidgetItem(status))
            self.tabela.setItem(linha, 7, QTableWidgetItem(locacao.cliente.cpf))

    def nova_locacao(self):
        self.janela_principal.iniciar_nova_locacao()
        self.atualizar_tabela()

    def registrar_devolucao(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhuma locação selecionada",
                "Selecione uma locação para registrar a devolução."
            )
            return
        id_locacao = int(self.tabela.item(linha, 0).text())
        locacao = next(
            (l for l in self.janela_principal.lista_locacoes if l.id == id_locacao),
            None
        )
        if locacao is None:
            return
        if locacao.devolvida:
            QMessageBox.information(
                self,
                "Locação encerrada",
                "Essa locação já foi devolvida."
            )
            return
        resposta = QMessageBox.question(
            self,
            "Confirmar devolução",
            f"Registrar a devolução do filme '{locacao.filme.titulo}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            locacao.devolvida = True
            locacao.filme.quantidade += 1
            self.janela_principal.atualizar_tabela()
            self.atualizar_tabela()
            QMessageBox.information(
                self,
                "Devolução registrada",
                "A devolução foi registrada e o estoque do filme foi atualizado."
            )

class DialogoRanking(QDialog):
    
    def __init__(self, lista_locacoes, lista_filmes, parent=None):
        super().__init__(parent)

        self.lista_locacoes = lista_locacoes
        self.lista_filmes = lista_filmes

        self.setWindowTitle("Ranking dos Filmes Mais Alugados")
        self.resize(500, 300)

        layout_ranking = QVBoxLayout()

        self.ranking = QTableWidget()
        self.ranking.setColumnCount(3)
        self.ranking.setHorizontalHeaderLabels([
            "Posição",
            "Filme",
            "Quantidade de Aluguéis"
        ])

        self.ranking.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ranking.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout_ranking.addWidget(self.ranking)
        self.setLayout(layout_ranking)

        # Conta quantas vezes cada filme foi alugado.
        filme_alugueis = {}

        for locacao in self.lista_locacoes:
            id_filme = locacao.filme.id

            if id_filme in filme_alugueis:
                filme_alugueis[id_filme] += 1
            else:
                filme_alugueis[id_filme] = 1

        # Ordena do mais alugado para o menos alugado.
        ranking = sorted(
            filme_alugueis.items(),
            key=lambda item: item[1],
            reverse=True
        )[:3]

        # Cria um dicionário para encontrar os filmes pelo ID.
        filmes_por_id = {
            filme.id: filme
            for filme in self.lista_filmes
        }

        # Cria somente as linhas necessárias.
        self.ranking.setRowCount(len(ranking))

        # Preenche a tabela com o Top 3.
        for linha, (id_filme, quantidade) in enumerate(ranking):

            filme = filmes_por_id.get(id_filme)

            if filme is None:
                continue

            valores = [
                str(linha + 1),
                filme.titulo,
                str(quantidade)
            ]

            for coluna, valor in enumerate(valores):
                self.ranking.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor)
                )

        # Se ainda não houver locações, informa na tabela.
        if not ranking:
            self.ranking.setRowCount(1)
            self.ranking.setSpan(0, 0, 1, 3)
            self.ranking.setItem(
                0,
                0,
                QTableWidgetItem(
                    "Ainda não há locações registradas."
                )
            )

class DialogoCadastroFilme(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Filme")
        self.resize(400, 250)
        self.campo_titulo = QLineEdit()
        self.campo_diretor = QLineEdit()
        self.combo_genero = QComboBox()
        self.combo_genero.addItems([
            "Ação",
            "Aventura",
            "Comédia",
            "Drama",
            "Ficção",
            "Terror",
            "Romance"
        ])
        self.combo_classificacao = QComboBox()
        self.combo_classificacao.addItems([
            "Livre",
            "10 anos",
            "12 anos",
            "14 anos",
            "16 anos",
            "18 anos"
        ])
        self.campo_quantidade = QSpinBox()
        self.campo_quantidade.setMinimum(1)
        self.campo_quantidade.setMaximum(100)
        self.campo_quantidade.setValue(1)
        formulario = QFormLayout()
        formulario.addRow("Título:", self.campo_titulo)
        formulario.addRow("Diretor:", self.campo_diretor)
        formulario.addRow("Gênero:", self.combo_genero)
        formulario.addRow("Classificação indicativa:", self.combo_classificacao)
        formulario.addRow("Quantidade:", self.campo_quantidade)
        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botoes.accepted.connect(self.validar_dados)
        botoes.rejected.connect(self.reject)
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(formulario)
        layout_principal.addWidget(botoes)
        self.setLayout(layout_principal)

    def validar_dados(self):
        titulo = self.campo_titulo.text().strip()
        diretor = self.campo_diretor.text().strip()
        if titulo == "":
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o título do filme."
            )
            self.campo_titulo.setFocus()
            return
        if diretor == "":
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o diretor do filme."
            )
            self.campo_diretor.setFocus()
            return
        self.accept()

    def obter_dados(self):
        return {
            "titulo": self.campo_titulo.text().strip(),
            "diretor": self.campo_diretor.text().strip(),
            "genero": self.combo_genero.currentText(),
            "classificacao": self.combo_classificacao.currentText(),
            "quantidade": self.campo_quantidade.value()
        }


class SinaisVerificacao(QObject):
    """Comunicação da tarefa com a janela, sem acessar widgets no worker."""
    resultado = Signal(list)
    erro = Signal(str)
    finalizado = Signal()



class WorkerAtrasos(QRunnable):
    """Verifica uma cópia dos dados das locações em uma thread do pool."""


    def __init__(self, dados, hoje):
        super().__init__()
        self.dados = dados
        self.hoje = hoje
        self.sinais = SinaisVerificacao()

    @Slot()

    def run(self):
        try:
            atrasadas = []
            for id_locacao, cliente, filme, prevista, devolvida in self.dados:
                if not devolvida and prevista < self.hoje:
                    dias = (self.hoje - prevista).days
                    atrasadas.append((id_locacao, cliente, filme, prevista, dias))
            self.sinais.resultado.emit(atrasadas)
        except Exception as erro:
            self.sinais.erro.emit(str(erro))
        finally:
            self.sinais.finalizado.emit()



class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Locadora de Filmes - Inhuma")
        self.resize(950, 600)
        self.lista_filmes = []
        self.proximo_id = 1
        self.lista_clientes = []
        self.proximo_id_cliente = 1
        self.lista_locacoes = []
        self.proximo_id_locacao = 1
        # Pool e estado da tarefa de verificação de atrasos.
        self.threadpool = QThreadPool(self)
        self.verificacao_em_andamento = False
        self.worker_atrasos = None
        self.acao_atrasos = QAction("Verificar atrasos", self)
        self.acao_atrasos.triggered.connect(self.verificar_atrasos)
        self.criar_menu()
        self.criar_barra_ferramentas()
        self.criar_interface()
        self.criar_dados_exemplo()
        self.statusBar().showMessage("Sistema pronto.")
    @Slot()

    def verificar_atrasos(self):
        """Captura os dados atuais e inicia uma tarefa sem bloquear a janela."""
        if self.verificacao_em_andamento:
            return
        
        # Tuplas com valores imutáveis: o worker não acessa os objetos vivos.
        dados = tuple(
            
            (locacao.id, locacao.cliente.nome, locacao.filme.titulo,
             locacao.data_prevista, locacao.devolvida)#cada indice da tupla recebe um campo de cada locacao
            for locacao in self.lista_locacoes#for que enche a tupla.

        )

        self.verificacao_em_andamento = True
        self.acao_atrasos.setEnabled(False)
        self.statusBar().showMessage("Verificando locações atrasadas...")
        self.worker_atrasos = WorkerAtrasos(dados, date.today())

        self.worker_atrasos.sinais.resultado.connect(
            self.mostrar_atrasos, Qt.ConnectionType.QueuedConnection)
        
        self.worker_atrasos.sinais.erro.connect(
            self.mostrar_erro_verificacao, Qt.ConnectionType.QueuedConnection)
        
        self.worker_atrasos.sinais.finalizado.connect(
            self.finalizar_verificacao, Qt.ConnectionType.QueuedConnection)
        
        self.threadpool.start(self.worker_atrasos)

    @Slot(list)

    def mostrar_atrasos(self, atrasadas):
        """Exibe na thread principal o resultado referente ao início da consulta."""
        self.statusBar().showMessage(
            f"Verificação concluída: {len(atrasadas)} locação(ões) atrasada(s).")
        # Janela não modal para permitir o processamento do sinal finalizado.
        dialogo = QDialog(self)
        dialogo.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        dialogo.setWindowTitle("Locações atrasadas")
        dialogo.resize(850, 400)
        layout = QVBoxLayout(dialogo)
        texto = (f"{len(atrasadas)} locação(ões) atrasada(s). "
                 "Dados do início da verificação."
                 if atrasadas else "Nenhuma locação atrasada encontrada.")
        layout.addWidget(QLabel(texto))
        tabela = QTableWidget(len(atrasadas), 5)
        tabela.setHorizontalHeaderLabels(
            ["ID", "Cliente", "Filme", "Devolução prevista", "Dias de atraso"])
        tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for linha, (identificador, cliente, filme, prevista, dias) in enumerate(atrasadas):
            valores = [str(identificador), cliente, filme,
                       prevista.strftime("%d/%m/%Y"), str(dias)]
            for coluna, valor in enumerate(valores):
                tabela.setItem(linha, coluna, QTableWidgetItem(valor))
        layout.addWidget(tabela)
        fechar = QPushButton("Fechar")
        fechar.clicked.connect(dialogo.close)
        layout.addWidget(fechar)
        self.dialogo_atrasos = dialogo
        dialogo.show()

    @Slot(str)

    def mostrar_erro_verificacao(self, mensagem):
        """Informa uma falha sem acessar a interface a partir do worker."""
        self.statusBar().showMessage("Erro ao verificar atrasos.")
        QMessageBox.warning(self, "Erro na verificação", mensagem)

    @Slot()

    def finalizar_verificacao(self):
        """Libera uma nova consulta após o término da tarefa."""
        self.verificacao_em_andamento = False
        self.acao_atrasos.setEnabled(True)
        self.worker_atrasos = None


    def criar_menu(self):
        menu_barra = self.menuBar()
        menu_arquivo = menu_barra.addMenu("Arquivo")
        menu_cadastros = menu_barra.addMenu("Cadastros")
        menu_ajuda = menu_barra.addMenu("Ajuda")
        acao_novo_filme = QAction("Novo filme", self)
        acao_novo_filme.setShortcut("Ctrl+N")
        acao_novo_filme.triggered.connect(self.abrir_cadastro_filme)
        acao_sair = QAction("Sair", self)
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.triggered.connect(self.close)
        acao_clientes = QAction("Clientes", self)
        acao_clientes.triggered.connect(self.abrir_clientes)
        acao_locacoes = QAction("Locações", self)
        acao_locacoes.triggered.connect(self.abrir_locacoes)
        acao_sobre = QAction("Sobre o sistema", self)
        acao_sobre.triggered.connect(self.mostrar_sobre)
        menu_arquivo.addAction(acao_novo_filme)
        menu_arquivo.addSeparator()
        menu_arquivo.addAction(acao_sair)
        menu_cadastros.addAction(acao_novo_filme)
        menu_cadastros.addAction(acao_clientes)
        menu_cadastros.addAction(acao_locacoes)
        menu_cadastros.addAction(self.acao_atrasos)
        menu_ajuda.addAction(acao_sobre)

    def criar_barra_ferramentas(self):
        barra = QToolBar("Barra de ferramentas")
        barra.setMovable(False)
        self.addToolBar(barra)
        acao_filmes = QAction("Novo Filme", self)
        acao_filmes.triggered.connect(self.abrir_cadastro_filme)
        acao_clientes = QAction("Clientes", self)
        acao_clientes.triggered.connect(self.abrir_clientes)
        acao_locacoes = QAction("Locações", self)
        acao_locacoes.triggered.connect(self.abrir_locacoes)
        acao_excluir = QAction("Excluir Filme", self)
        acao_excluir.triggered.connect(self.excluir_filme)
        acao_sair = QAction("Sair", self)
        acao_sair.triggered.connect(self.close)
        barra.addAction(acao_filmes)
        barra.addAction(acao_clientes)
        barra.addAction(acao_locacoes)
        barra.addAction(self.acao_atrasos)
        barra.addSeparator()
        barra.addAction(acao_excluir)
        barra.addSeparator()
        barra.addAction(acao_sair)

    def criar_interface(self):
        central = QWidget()
        layout_principal = QVBoxLayout()
        titulo = QLabel("Locadora de Filmes - Inhuma")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            "font-size: 24px; font-weight: bold; padding: 10px;"
        )
        descricao = QLabel(
            "Cadastre, consulte e gerencie os filmes disponíveis."
        )
        descricao.setAlignment(Qt.AlignCenter)
        grupo_pesquisa = QGroupBox("Pesquisa de filmes")
        layout_pesquisa = QHBoxLayout()
        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText(
            "Digite o título ou diretor para pesquisar."
        )
        botao_pesquisar = QPushButton("Pesquisar")
        botao_limpar = QPushButton("Limpar pesquisa")
        layout_pesquisa.addWidget(self.campo_pesquisa)
        layout_pesquisa.addWidget(botao_pesquisar)
        layout_pesquisa.addWidget(botao_limpar)
        grupo_pesquisa.setLayout(layout_pesquisa)
        self.tabela_filmes = QTableWidget()
        self.tabela_filmes.setColumnCount(6)
        self.tabela_filmes.setHorizontalHeaderLabels([
            "ID",
            "Título",
            "Gênero",
            "Classificação",
            "Diretor",
            "Quantidade"
        ])
        self.tabela_filmes.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        self.tabela_filmes.setSelectionMode(
            QTableWidget.SingleSelection
        )
        self.tabela_filmes.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.tabela_filmes.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout_botoes = QHBoxLayout()

        #CRIAÇÃO DOS BOTÕES:
        botao_novo = QPushButton("Cadastrar filme")
        botao_excluir = QPushButton("Excluir selecionado")
        botao_detalhes = QPushButton("Ver detalhes")

        botao_alugar = QPushButton("Alugar Filme")

        #BOTAO RANKING FILMES MAIS ALUGADOS:
        botao_ranking_mais_alugados = QPushButton("Filmes mais Alugados")

        layout_botoes.addWidget(botao_novo)
        layout_botoes.addWidget(botao_excluir)
        layout_botoes.addWidget(botao_detalhes)
        layout_botoes.addWidget(botao_alugar)
        layout_botoes.addWidget(botao_ranking_mais_alugados)#adicionado ao layout:


        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)
        layout_principal.addWidget(grupo_pesquisa)
        layout_principal.addWidget(self.tabela_filmes)
        layout_principal.addLayout(layout_botoes)
        central.setLayout(layout_principal)
        self.setCentralWidget(central)

        botao_novo.clicked.connect(self.abrir_cadastro_filme)
        botao_excluir.clicked.connect(self.excluir_filme)
        botao_detalhes.clicked.connect(self.mostrar_detalhes)
        #BOTAO ALUGAR:
        botao_alugar.clicked.connect(self.alugar_filme)


        #vou conectar a algum método
        botao_ranking_mais_alugados.clicked.connect(self.ver_ranking_mais_alugados)

        botao_pesquisar.clicked.connect(self.pesquisar_filmes)
        botao_limpar.clicked.connect(self.limpar_pesquisa)
        self.campo_pesquisa.textChanged.connect(self.pesquisar_filmes)
        self.tabela_filmes.cellDoubleClicked.connect(self.mostrar_detalhes)

    def criar_dados_exemplo(self):
        filme1 = Filme(
            self.proximo_id,
            "O Senhor dos Anéis",
            "Aventura",
            "Peter Jackson",
            3,
            "12 anos"
        )
        self.lista_filmes.append(filme1)
        self.proximo_id += 1
        filme2 = Filme(
            self.proximo_id,
            "Interestelar",
            "Ficção",
            "Christopher Nolan",
            2,
            "10 anos"
        )
        self.lista_filmes.append(filme2)
        self.proximo_id += 1
        self.atualizar_tabela()

    def abrir_cadastro_filme(self):
        dialogo = DialogoCadastroFilme(self)
        if dialogo.exec():
            dados = dialogo.obter_dados()
            novo_filme = Filme(
                self.proximo_id,
                dados["titulo"],
                dados["genero"],
                dados["diretor"],
                dados["quantidade"],
                dados["classificacao"]
            )
            self.lista_filmes.append(novo_filme)
            self.proximo_id += 1
            self.atualizar_tabela()
            QMessageBox.information(
                self,
                "Cadastro realizado",
                "Filme cadastrado com sucesso."
            )
            self.statusBar().showMessage(
                "Novo filme cadastrado."
            )

    def atualizar_tabela(self, filmes=None):
        if filmes is None:
            filmes = self.lista_filmes
        self.tabela_filmes.setRowCount(0)
        for filme in filmes:
            linha = self.tabela_filmes.rowCount()
            self.tabela_filmes.insertRow(linha)
            self.tabela_filmes.setItem(
                linha, 0, QTableWidgetItem(str(filme.id))
            )
            self.tabela_filmes.setItem(
                linha, 1, QTableWidgetItem(filme.titulo)
            )
            self.tabela_filmes.setItem(
                linha, 2, QTableWidgetItem(filme.genero)
            )
            self.tabela_filmes.setItem(
                linha, 3, QTableWidgetItem(filme.classificacao)
            )
            self.tabela_filmes.setItem(
                linha, 4, QTableWidgetItem(filme.diretor)
            )
            self.tabela_filmes.setItem(
                linha, 5, QTableWidgetItem(str(filme.quantidade))
            )
    # slot que se conecta com o botão de alugar

    def alugar_filme(self):
        linha = self.tabela_filmes.currentRow()
        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum filme selecionado",
                "Selecione um filme na tabela para alugar."
            )
            return
        id_filme = int(self.tabela_filmes.item(linha, 0).text())
        filme_selecionado = next(
            (filme for filme in self.lista_filmes if filme.id == id_filme),
            None
        )
        if filme_selecionado is None:
            return
        if filme_selecionado.quantidade <= 0:
            QMessageBox.warning(
                self,
                "Filme esgotado",
                "Não há unidades disponíveis desse filme."
            )
            return
        self.iniciar_nova_locacao(filme_selecionado)







    def ver_ranking_mais_alugados(self):
        if not self.lista_locacoes:
            QMessageBox.warning(
                self,
                "Não há Alocações feitas no momento", 
                "Faça uma pra ver o Ranking dos filmes mais Alugados"
            )
        else:
            dialogo_raking = DialogoRanking(self.lista_locacoes, self.lista_filmes)
            dialogo_raking.exec()







    def iniciar_nova_locacao(self, filme_preselecionado=None):
        if len(self.lista_clientes) == 0:
            QMessageBox.warning(
                self,
                "Nenhum cliente cadastrado",
                "Cadastre pelo menos um cliente antes de realizar uma locação."
            )
            return False
        filmes_disponiveis = [
            filme for filme in self.lista_filmes if filme.quantidade > 0
        ]
        if len(filmes_disponiveis) == 0:
            QMessageBox.warning(
                self,
                "Sem filmes disponíveis",
                "Não há filmes disponíveis para locação."
            )
            return False
        dialogo = DialogoNovaLocacao(self, filme_preselecionado)
        if not dialogo.exec():
            return False
        dados = dialogo.obter_dados()
        cliente = next(
            (c for c in self.lista_clientes if c.id == dados["id_cliente"]),
            None
        )
        filme = next(
            (f for f in self.lista_filmes if f.id == dados["id_filme"]),
            None
        )
        if cliente is None or filme is None:
            return False
        if filme.quantidade <= 0:
            QMessageBox.warning(
                self,
                "Filme esgotado",
                "O filme selecionado não possui unidades disponíveis."
            )
            return False
        hoje = date.today()
        prevista = hoje + timedelta(days=dados["dias"])
        nova_locacao = Locacao(
            self.proximo_id_locacao,
            cliente,
            filme,
            hoje,
            prevista
        )
        self.lista_locacoes.append(nova_locacao)
        self.proximo_id_locacao += 1
        filme.quantidade -= 1
        self.atualizar_tabela()
        QMessageBox.information(
            self,
            "Locação realizada",
            f"Locação registrada com sucesso.\n\n"
            f"Cliente: {cliente.nome}\n"
            f"Filme: {filme.titulo}\n"
            f"Devolução prevista: {prevista.strftime('%d/%m/%Y')}"
        )
        self.statusBar().showMessage("Nova locação registrada.")
        return True

    def pesquisar_filmes(self):
        texto = self.campo_pesquisa.text().strip().lower()
        if texto == "":
            self.atualizar_tabela()
            return
        filmes_encontrados = []
        for filme in self.lista_filmes:
            if (
                texto in filme.titulo.lower()
                or texto in filme.diretor.lower()
            ):
                filmes_encontrados.append(filme)
        self.atualizar_tabela(filmes_encontrados)
        self.statusBar().showMessage(
            f"{len(filmes_encontrados)} filme(s) encontrado(s)."
        )

    def limpar_pesquisa(self):
        self.campo_pesquisa.clear()
        self.atualizar_tabela()
        self.statusBar().showMessage("Pesquisa limpa.")

    def excluir_filme(self):
        linha = self.tabela_filmes.currentRow()
        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum filme selecionado",
                "Selecione um filme na tabela para excluir."
            )
            return
        id_filme = int(
            self.tabela_filmes.item(linha, 0).text()
        )
        filme_selecionado = None
        for filme in self.lista_filmes:
            if filme.id == id_filme:
                filme_selecionado = filme
                break
        if filme_selecionado is None:
            return
        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Deseja excluir o filme "
            f"'{filme_selecionado.titulo}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            self.lista_filmes.remove(filme_selecionado)
            self.atualizar_tabela()
            QMessageBox.information(
                self,
                "Filme excluído",
                "O filme foi excluído com sucesso."
            )

    def mostrar_detalhes(self):
        linha = self.tabela_filmes.currentRow()
        if linha < 0:
            QMessageBox.information(
                self,
                "Detalhes",
                "Selecione um filme para visualizar os detalhes."
            )
            return
        id_filme = int(
            self.tabela_filmes.item(linha, 0).text()
        )
        for filme in self.lista_filmes:
            if filme.id == id_filme:
                mensagem = (
                    f"ID: {filme.id}\n"
                    f"Título: {filme.titulo}\n"
                    f"Gênero: {filme.genero}\n"
                    f"Classificação indicativa: {filme.classificacao}\n"
                    f"Diretor: {filme.diretor}\n"
                    f"Quantidade disponível: {filme.quantidade}"
                )
                QMessageBox.information(
                    self,
                    "Detalhes do filme",
                    mensagem
                )
                return

    def abrir_clientes(self):
        self.janela_clientes = JanelaClientes(self)
        self.janela_clientes.show()

    def abrir_locacoes(self):
        dialogo = DialogoLocacoes(self)
        dialogo.exec()

    def mostrar_sobre(self):
        QMessageBox.about(
            self,
            "Sobre o sistema",
            "Locadora de Filmes - Inhuma\n\n"
            "Sistema desenvolvido em Python utilizando PySide6."
        )

    #trata  os ventos de teclado  da janela:
    def keyPressEvent(self, evento):#POSSO FZR PRAA QUALQUER TECLA QUE EU QUIZER!!!!
        #pega o evento como parametro:
        if evento.key() == Qt.Key_Delete:#ver se é igual a tecla delete
            self.excluir_filme()
        elif evento.key() == Qt.Key_Escape:#se for igual esc faz o clear
            self.campo_pesquisa.clear()
        else:
            super().keyPressEvent(evento)

    def closeEvent(self, evento):
        
        if self.verificacao_em_andamento or self.threadpool.activeThreadCount() > 0:
            self.statusBar().showMessage("Aguarde a verificação terminar antes de sair.")
            evento.ignore()
            return
        
        resposta = QMessageBox.question(
            self,
            "Sair",
            "Deseja realmente sair do sistema?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            #aceita o evento de fechar
            evento.accept()
        else:
            #ignora o evento e n fecha:
            evento.ignore()

if __name__ == "__main__":
    app = QApplication([])
    janela = JanelaPrincipal()
    janela.show()
    app.exec()

