# 📝 QuickTarefas

**QuickTarefas** é um aplicativo simples e intuitivo de produtividade desenvolvido com **Python** e **KivyMD**. Ele combina um **gerenciador de tarefas** com um **temporizador Pomodoro**, ideal para ajudar na organização e foco nas atividades do dia a dia.

---

## ⚙️ Funcionalidades

- ✅ Adicionar, editar e excluir tarefas.
- ⏰ Temporizador Pomodoro (25 minutos) com opções de iniciar, pausar e reiniciar.
- 💾 Salvamento automático de tarefas usando `pickle`.
- 📦 Interface com navegação entre telas (Tarefas, Temporizador e Sobre).
- ⚠️ Limite de até 7 tarefas simultâneas.

---

## 📱 Interface

O app possui três telas principais:
- **Tarefas:** permite cadastrar tarefas com data e marcação de conclusão.
- **Temporizador:** controle do tempo com o estilo Pomodoro.
- **Sobre:** seção descritiva ou informativa sobre o app.

---

## 🚀 Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Kivy](https://kivy.org/#home)
- [KivyMD](https://kivymd.readthedocs.io/en/latest/) — para componentes com Material Design.

---

## 🛠️ Como Executar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/rodrigosantana24/quicktarefas.git
   cd quicktarefas
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o app:**

   ```bash
   python main.py
   ```

---

## 📌 Observações

- O arquivo `tarefas.pkl` é criado automaticamente para armazenar as tarefas localmente.
- É possível personalizar o tempo do temporizador facilmente alterando o valor inicial no código.

---

## 📃 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🙋‍♂️ Autor

Desenvolvido por **Rodrigo Santana**  
📧 Contato: rodrigosantana.dev@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/rodrigo-santana-280928233/)

---
