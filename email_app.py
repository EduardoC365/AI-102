import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

# Pasamos las credenciales del .env a las variable siguientes.
apikey = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("OPENAI_ENDPOINT")
api_version = os.getenv("api_version")

# Crear el cliente con las credenciales
client = AzureOpenAI(
    azure_endpoint= endpoint, 
    api_key= apikey,  
    api_version= api_version
)
# Título de la aplicación
st.title("Asistente de email")
st.write("Pone el contenido de tu email, primero pon el contenido y da al botón que quieras.")
# Entrada del correo electrónico
email_content = st.text_area("Introduce el correo electrónico:", height=200)

# Botones para generar el resumen o la respuesta
if st.button("Generar resumen"):
    if email_content.strip():
        with st.spinner("Generando resumen..."):
            try:
                # Llamada al modelo de Azure OpenAI para generar un resumen
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Asegúrate de usar el modelo que configuraste
                    messages=[
                        {"role": "system", "content": "Actúa como un asistente que resume correos electrónicos."},
                        {"role": "user", "content": f"Resume este correo: {email_content}"}
                    ]
                )
                summary = response.choices[0].message.content
                st.success("Resumen generado:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error al generar el resumen: {e}")
    else:
        st.warning("Por favor, introduce el contenido del correo.")

if st.button("Generar respuesta"):
    if email_content.strip():
        with st.spinner("Generando respuesta..."):
            try:
                # Llamada al modelo de Azure OpenAI para generar una respuesta
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Asegúrate de usar el modelo que configuraste
                    messages=[
                        {"role": "system", "content": "Actúa como un asistente que responde correos electrónicos de manera profesional. Con un maximo de 5 lineas."},
                        {"role": "user", "content": f"Redacta una respuesta para este correo: {email_content}"}
                    ]
                )
                reply = response.choices[0].message.content
                st.success("Respuesta generada:")
                st.write(reply)
            except Exception as e:
                st.error(f"Error al generar la respuesta: {e}")
    else:
        st.warning("Por favor, introduce el contenido del correo.")
