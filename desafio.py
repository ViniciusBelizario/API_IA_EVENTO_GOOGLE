import flet as ft
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyD3E0wv_kll3-XtP56U_0I2N9ia7fG91bA"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.0-pro")

def main(pagina):

    def entrar_no_chat(event):
        pagina.remove(titulo)
        pagina.remove(botao_iniciar)
        janela.open = False
        pagina.add(chat_list_view)
        pagina.add(linha_mensagem)
        mensagem = f"{campo_nome_usuario.value} entrou no chat"
        pagina.pubsub.send_all(mensagem)
        pagina.update()

    def enviar_mensagem_tunel(mensagem):
        mensagem_usuario = ft.Text(value=mensagem)
        chat_list_view.controls.append(mensagem_usuario)
        chat_list_view.update()
        chat_list_view.scroll_to(len(chat_list_view.controls) - 1)  # Garante rolagem automática para a última mensagem

    def responder_mensagem(nome_usuario, texto_mensagem):
        resposta_modelo = model.generate_content(texto_mensagem)
        resposta_texto = f"Bot: {resposta_modelo.text}"
        mensagem_completa = f"{nome_usuario}: {texto_mensagem}\n{resposta_texto}"
        pagina.pubsub.send_all(mensagem_completa)
        pagina.update()

    def enviar_mensagem(event):
        texto_mensagem = campo_mensagem_usuario.value
        nome_usuario = campo_nome_usuario.value
        mensagem = f"{nome_usuario}: {texto_mensagem}"
        pagina.pubsub.send_all(mensagem)
        campo_mensagem_usuario.value = ""
        pagina.update()

    def acionar_ia(event):
        texto_mensagem = campo_mensagem_usuario.value
        nome_usuario = campo_nome_usuario.value
        responder_mensagem(nome_usuario, texto_mensagem)
        campo_mensagem_usuario.value = ""
        pagina.update()

    # Interface do usuário
    titulo = ft.Text("Zap")
    titulo_janela = ft.Text("Bem vindo ao Zap")
    campo_nome_usuario = ft.TextField(label="Escreva seu nome no chat")
    botao_entrar_no_chat = ft.ElevatedButton(text="Entrar no chat", on_click=entrar_no_chat)

    # Configurando a ListView para o chat
    chat_list_view = ft.ListView(expand=True)
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    campo_mensagem_usuario = ft.TextField(label="Digite sua mensagem")
    botao_enviar_mensagem = ft.ElevatedButton(text="Enviar", on_click=enviar_mensagem)
    botao_acionar_ia = ft.ElevatedButton(text="Acionar IA", on_click=acionar_ia)
    linha_mensagem = ft.Row([campo_mensagem_usuario, botao_enviar_mensagem, botao_acionar_ia])

    janela = ft.AlertDialog(title=titulo_janela, content=campo_nome_usuario, actions=[botao_entrar_no_chat])
    def iniciar_chat(event):
        pagina.dialog = janela
        janela.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton(text="Iniciar Chat", on_click=iniciar_chat)
    pagina.add(titulo)
    pagina.add(botao_iniciar)

ft.app(main, view=ft.WEB_BROWSER)