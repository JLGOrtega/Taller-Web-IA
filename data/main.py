import streamlit as st
from textblob import Word, TextBlob
from data.src import get_caption
import os

st.set_page_config(page_title="AI App", page_icon=":rocket:", layout="wide")
st.title("AI App")

menu = st.sidebar.selectbox(
    "Seleccione una opcion del menu",
    ('Home', 'Speller', "Captioner"))

if menu == "Home":

    st.subheader("Home")
    st.image('img/ai.png')
    st.subheader("App Options:")
    st.caption("(Hacer click en las opciones para ver mas detalles)**")

    with st.expander("- Speller"):
        st.write("""Esta app nos permite corregir errores de spelling en palabras/frases 
                    (solo en ingles!).""")

    with st.expander("- Captioner"):
        st.write("""Esta app nos permite obtener una breve descripcion de la palabra seleccionada.""")

elif menu=="Speller":

    st.subheader("Speller")
    word = st.text_input("Introduzca la palabra")
    sentence = st.text_input("Introduzca la frase")
    if st.button("Ejecutar"):
        if word is not None:
            word = Word(word).correct()
            st.text(f"La palabra corregida es: {word}")
        if sentence is not None:
            sentence = TextBlob(sentence).correct()
            st.text(f"La frase corregida es: {sentence}")
            
elif menu=="Captioner":
    st.subheader("Classifier")
    #title = st.text_input('Ruta a la imagen:', 'Add route')
    title = "img/" + st.selectbox("Elija imagen", ["Add route"]+os.listdir("img/"))
    if title != "img/Add route":
        caption = get_caption(title)
        st.image(title, width=300)
    else:
        caption = "No data"
    st.subheader("Output:")
    st.text(caption)