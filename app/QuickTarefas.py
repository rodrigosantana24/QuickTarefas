from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from datetime import datetime
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
import pickle


class TelaTemporizador(Screen):
    pass


class TelaTarefas(Screen):  
    def adicionar_tarefa(self):
        self.dialog = MDDialog(
            title = "Adicionar Tarefa",
            type = "custom",
            content_cls = MDTextField(hint_text = "Digite a tarefa"),
            buttons = [
                MDRaisedButton(
                    text = "Cancelar",
                    on_release = self.fecha_dialog
                ),
                MDRaisedButton(
                    text = "Adicionar",
                    on_release = self.salvar_tarefa
                )
            ]
        )
        self.dialog.open()

    def fecha_dialog(self, instance):
        self.dialog.dismiss()

    def salvar_tarefa(self, instance):
        texto_tarefa = self.dialog.content_cls.text
        if texto_tarefa.strip():
            tarefas = [widget for widget in self.ids.tarefas_container.children if isinstance(widget, Tarefa)]
            if len(tarefas) >= 7:
                self.mostrar_erro("Você não pode adicionar mais de 7 tarefas.")
            else:
                tarefa = Tarefa(texto = texto_tarefa)
                self.ids.tarefas_container.add_widget(tarefa)
                self.salvar_tarefas()
                self.dialog.dismiss()
        else:
            print("Digite uma tarefa!")
    
    def salvar_tarefas(self):
        tarefas = [widget.texto for widget in self.ids.tarefas_container.children if isinstance(widget, Tarefa)]
        with open('tarefas.pkl', 'wb') as file:
            pickle.dump(tarefas, file)

    def carregar_tarefas(self):
        try:
            with open('tarefas.pkl', 'rb') as file:
                tarefas = pickle.load(file)
                for texto in tarefas:
                    tarefa = Tarefa(texto = texto)
                    self.ids.tarefas_container.add_widget(tarefa)
        except FileNotFoundError:
            pass
    
    def salvar_edicao(self, novo_texto, dialog):
        if novo_texto.strip():
            self.texto = novo_texto
            self.label.text = novo_texto
            self.salvar_tarefas()  # Adicione esta linha
            dialog.dismiss()
        else:
            print("Digite um texto válido!")


class TelaSobre(Screen):
    pass


class GerenciadorDeTelas(ScreenManager):
    pass


class Temporizador:
    def __init__(self, tempo):
        self.tempo = tempo * 60

    def DiminuiTempo(self):
        self.tempo -= 1
        return self.tempo

    def __str__(self):
        return '{:02d}:{:02d}'.format(*divmod(self.tempo, 60))


class MostraTemporizador(MDFloatLayout):
    tempo_string = StringProperty('25:00')
    botao_string = StringProperty('Iniciar')
    running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._time = Temporizador(tempo = 25)
        self.atualiza_tempo_na_tela()

    def inicia(self):
        self.botao_string = 'Pausar'
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.atualizar_tempo, 1)

    def pausa(self):
        self.botao_string = 'Reiniciar'
        if self.running:
            self.running = False
            Clock.unschedule(self.atualizar_tempo)

    def zerar(self):
        if self.running:
            self.pausa()
        self._time = Temporizador(tempo=25)
        self.atualiza_tempo_na_tela()
        self.botao_string = 'Iniciar'

    def click(self):
        if self.running:
            self.pausa()
        else:
            self.inicia()

    def atualizar_tempo(self, *args):
        time = self._time.DiminuiTempo()
        self.tempo_string = str(self._time)
        if time <= 0:
            self.pausa()

    def atualiza_tempo_na_tela(self):
        self.tempo_string = str(self._time)


class Tarefa(MDBoxLayout):
    texto = StringProperty('Nova Tarefa')
    data_criacao = StringProperty('')
    completo = BooleanProperty(False)

    def __init__(self, texto='', **kwargs):
        super().__init__(**kwargs)
        self.texto = texto
        self.data_criacao = datetime.now().strftime('%d-%m-%y')
        self.orientation = 'horizontal'
        self.spacing = dp(10) 
        self.size_hint_y = None
        self.height = dp(60)

        self.checkbox = MDCheckbox(size_hint_x=None, width=dp(40), size_hint_y=None, height=dp(40))
        self.checkbox.pos_hint = {'center_y': 0.5}
        self.add_widget(self.checkbox)

        self.label = MDLabel(text=self.texto, size_hint_x=0.6, valign='middle', halign='left')
        self.label.bind(size=self.label.setter('text_size'))  # Ajusta o texto para caber no espaço
        self.label.pos_hint = {'center_y': 0.5}
        self.add_widget(self.label)

        self.data_label = MDLabel(text=self.data_criacao, size_hint_x=0.2, valign='middle', halign='right')
        self.data_label.bind(size=self.data_label.setter('text_size'))
        self.data_label.pos_hint = {'center_y': 0.5}
        self.add_widget(self.data_label)

        self.edit_botao = MDIconButton(icon = "pencil", size_hint_x = None, width = dp(40), size_hint_y = None, height = dp(40))
        self.edit_botao.pos_hint = {'center_y': 0.5}
        self.edit_botao.bind(on_release = self.editar_tarefa)
        self.add_widget(self.edit_botao)

        self.delete_botao = MDIconButton(icon="delete", size_hint_x=None, width=dp(40), size_hint_y=None, height=dp(40))
        self.delete_botao.pos_hint = {'center_y': 0.5}
        self.delete_botao.bind(on_release=self.excluir_tarefa)
        self.add_widget(self.delete_botao)

    def editar_tarefa(self, instance):
        content = MDTextField(hint_text = "Editar a tarefa", text = self.texto)
        dialog = MDDialog(
            title = "Editar Tarefa",
            type = "custom",
            content_cls = content,
            buttons = [
                MDRaisedButton(
                    text = "Cancelar",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text = "Salvar",
                    on_release = lambda x: self.salvar_edicao(content.text, dialog)
                )
            ]
        )
        dialog.open()

    def salvar_edicao(self, novo_texto, dialog):
        if novo_texto.strip():
            self.texto = novo_texto
            self.label.text = novo_texto
            dialog.dismiss()
        else:
            print("Digite um texto válido!")

    def excluir_tarefa(self, instance): 
        self.parent.remove_widget(self)


class QuickTarefas(MDApp):
    def build(self):
        return Builder.load_file('layout.kv')
    
    def on_start(self):
        self.root.get_screen('tela_tarefas').carregar_tarefas()

    def tela(self, *args):
        self.root.current = 'tela_temporizador'

    def tela1(self, *args):  
        self.root.current = 'tela_sobre'

    def tela2(self, *args): 
        self.root.current = 'tela_tarefas'