import streamlit as st  # Importa la biblioteca Streamlit para crear la interfaz de usuario
from groq import Groq  # Importa la clase Groq para interactuar con el modelo de IA


# Configuración básica de la aplicación
st.set_page_config(page_title="LITHEK", page_icon="9️⃣", layout="centered")  # Configura el título, ícono y diseño de la página


# Entrada de texto para el nombre del usuario
nombre = st.text_input("¿Cuál es tu nombre?")  # Crea un campo para que el usuario ingrese su nombre


# Botón para mostrar un saludo al usuario
if st.button("Saludar"):  # Si el usuario hace clic en el botón "Saludar"
    st.subheader(f"Hola {nombre}! gracias por venir a LITHEK")  # Muestra un saludo personalizado


# Lista de modelos de IA disponibles
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']  # Define los modelos de IA


def configurar_pagina():  # Función para configurar la página
    st.title("LITHEK")  # Establece un título principal en la página
    st.sidebar.title("Configuración de la IA")  # Crea un título en el sidebar
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)  # Crea un menú desplegable para elegir un modelo
    return elegirModelo  # Devuelve el modelo seleccionado


# Función para crear un cliente de Groq
def crear_usuario_groq():
    claveSecreta = st.secrets["CLAVE_API"]  # Recupera la clave de API del archivo de secretos
    return Groq(api_key=claveSecreta)  # Crea y devuelve un cliente de Groq


# Función para configurar el modelo de IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(  # Llama al modelo para obtener una respuesta
        model=modelo,  # Especifica el modelo
        messages=[{"role": "user", "content": mensajeDeEntrada}],  # Pasa el mensaje del usuario
        stream=True  # Habilita el streaming de la respuesta
    )


# Función para inicializar el estado de la aplicación
def inicializar_estado():
    if "mensajes" not in st.session_state:  # Verifica si "mensajes" no está en el estado de la sesión
        st.session_state.mensajes = []  # Inicializa "mensajes" como una lista vacía


# Función para actualizar el historial de mensajes
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})  # Agrega un nuevo mensaje al historial


# Función para mostrar el historial de mensajes
def mostrar_historial():
    for mensaje in st.session_state.mensajes:  # Itera sobre cada mensaje en el historial
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):  # Crea un mensaje en el chat con el rol y el avatar
            st.markdown(mensaje["content"])  # Muestra el contenido del mensaje


# Función para crear el área de chat
def area_chat():
    chat_container = st.container()  # Crea un contenedor para el área de chat
    with chat_container:
        mostrar_historial()  # Muestra el historial de mensajes


# Función para generar respuestas del modelo de IA
def generar_respuesta(chat_completo):
    respuesta_completa = ""  # Inicializa una cadena para almacenar la respuesta completa
    for frase in chat_completo:  # Itera sobre cada parte de la respuesta
        if frase.choices[0].delta.content:  # Verifica si hay contenido en la respuesta
            respuesta_completa += frase.choices[0].delta.content  # Agrega el contenido a la respuesta completa
            yield frase.choices[0].delta.content  # Genera el contenido en partes
    return respuesta_completa  # Devuelve la respuesta completa


# Función principal de la aplicación
def main():
    modelo = configurar_pagina()  # Configura la página y obtiene el modelo seleccionado


    clienteUsuario = crear_usuario_groq()  # Crea el cliente de Groq
    inicializar_estado()  # Inicializa el estado de la sesión


    mensaje = st.chat_input("Escribí tu mensaje: ")  # Crea un campo de entrada para el mensaje del usuario


    area_chat()  # Muestra el área de chat
    if mensaje:  # Si el usuario ha ingresado un mensaje
        actualizar_historial("user", mensaje, "🧑‍💻")  # Agrega el mensaje del usuario al historial


        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)  # Configura el modelo con el mensaje del usuario


        if chat_completo:  # Si hay una respuesta del modelo
            with st.chat_message("assistant"):  # Crea un mensaje del asistente
                respuesta_generada = st.write_stream(generar_respuesta(chat_completo))  # Muestra la respuesta del modelo
                actualizar_historial("assistant", respuesta_generada, "🤖")  # Agrega la respuesta al historial


    # El rerun puede no ser necesario dependiendo de cómo manejes el estado.
    # st.rerun()  # Reinicia la aplicación para reflejar las nuevas interacciones


# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    main()  # Llama a la función principal


