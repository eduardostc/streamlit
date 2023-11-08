import sys
sys.path.append('/path/to/openai')
import openai # import explícito
import streamlit as st
from streamlit_chat import message as msg #melhora a aparencia do chat
import io #criar, editar e salvar documento do word dentro do streamlit (não precisa de instalação)
import docx #processar arquivo texto

# Configurando a chave da API do OpenAI
openai.api_key = "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"

# Título da página web
st.title("ChatGPT do Vestibular da Unicamp")
st.write("***")

# Subtítulo
st.subheader("Chat")

# Verifica se a sessão contém o histórico da conversa
if 'hst_conversa' not in st.session_state:
    st.session_state.hst_conversa = [] #criado para guardar o historico de conversa

# Adicione um componente de upload de arquivo para que o usuário possa carregar o arquivo com o conteúdo a ser consultado
arquivo = st.file_uploader("Carregar arquivo de conteúdo", type=[".txt", ".docx"])

# Carregue o arquivo e o conteúdo do arquivo
conteudo_arquivo = None
if arquivo: #verificando se um arquivo foi carregado pelo usuário
    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Se o arquivo for um arquivo DOCX, leia o conteúdo do arquivo
        docx_file = docx.Document(io.BytesIO(arquivo.read()))
        conteudo_arquivo = "\n".join(paragraph.text for paragraph in docx_file.paragraphs)
    elif arquivo.type == "text/plain":
        # Se o arquivo for um arquivo de texto simples (TXT), leia o conteúdo do arquivo
        conteudo_arquivo = arquivo.read().decode("utf-8")
    else:
        st.write("Tipo de arquivo não suportado. Use um arquivo .docx ou .txt.")

# Chave exclusiva para o widget streamlit_chat (criando uma chave única para o widget do chat com base no número de itens no histórico de conversas).
widget_key = "chat_widget_" + str(len(st.session_state.hst_conversa))

# Caixa de entrada para o usuário digitar uma pergunta
conversa = st.text_area("Digite a pergunta:")

# Botão para enviar mensagem
btn_enviar_msg = st.button("Enviar Mensagem")

if btn_enviar_msg: #Verifica se um arquivo foi carregado e se a pergunta do usuário está contida no conteúdo do arquivo.
    if conteudo_arquivo:
        # Verifique se a pergunta do usuário está no conteúdo do arquivo
        if conversa in conteudo_arquivo:
            # Encontre a resposta correspondente no arquivo
            respostas = []
            lines = conteudo_arquivo.split("\n")
            for i in range(len(lines) - 1):
                if lines[i].startswith("P:") and lines[i + 1].startswith("R:"):
                    pergunta = lines[i][3:].strip()
                    resposta = lines[i + 1][3:].strip()
                    respostas.append((pergunta, resposta))

            # Procure a pergunta correspondente no arquivo
            resposta_encontrada = None
            for pergunta, resposta in respostas:
                if pergunta == conversa:
                    resposta_encontrada = resposta
                    break

            if resposta_encontrada:
                st.session_state.hst_conversa.append({"role": "user", "content": conversa})
                st.session_state.hst_conversa.append({"role": "assistant", "content": resposta_encontrada})
            else:
                st.write("Essa pergunta não existe no arquivo específico.")
        else:
            st.write("Essa pergunta não existe no arquivo específico.")
    else:
        st.write("Carregue um arquivo antes de fazer uma pergunta.")

# Exibe o histórico da conversa na interface
if len(st.session_state.hst_conversa) > 0:
    for i in range(len(st.session_state.hst_conversa)):
        if st.session_state.hst_conversa[i]["role"] == "user":
            msg("Você: " + st.session_state.hst_conversa[i]['content'], is_user=True, key=widget_key + str(i))
        else:
            msg("Resposta IA: " + st.session_state.hst_conversa[i]['content'], key=widget_key + str(i))
