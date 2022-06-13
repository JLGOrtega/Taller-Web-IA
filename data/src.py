import streamlit as st
@st.cache
def get_caption(image_url):
    import warnings
    warnings.filterwarnings('ignore')
    import pandas as pd
    import keras
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.image import load_img, img_to_array
    from keras.applications.vgg16 import preprocess_input
    from keras.preprocessing.sequence import pad_sequences
    import numpy as np

    dcaptions = pd.read_csv("data/dcaptions.csv", index_col=0).values.reshape(8092,)
    nb_words = 6000
    tokenizer = Tokenizer(nb_words=nb_words)
    tokenizer.fit_on_texts(dcaptions)
    vocab_size = len(tokenizer.word_index) + 1
    dtexts = tokenizer.texts_to_sequences(dcaptions)
    index_word = dict([(index,word) for word, index in tokenizer.word_index.items()])
    model_url = 'data/Image_Caption_Generator.h5'
    model = keras.models.load_model(model_url)
    modelvgg2 = keras.models.load_model("data/vggmodel.h5")

    

    npix = 224 #image size is fixed at 224 because VGG16 model has been pre-trained to take that size.
    target_size = (npix,npix,3)
    image = load_img(image_url, target_size=target_size)
    image = img_to_array(image)
    nimage = preprocess_input(image)

    y_pred = modelvgg2.predict(nimage.reshape( (1,) + nimage.shape[:3]))
    image_feats = y_pred.flatten()
    maxlen=30

    def predict_caption(image):
        '''
        image.shape = (1,4462)
        '''
        in_text = 'startseq'
        for iword in range(maxlen):
            sequence = tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence],maxlen)
            yhat = model.predict([image,sequence],verbose=0)
            yhat = np.argmax(yhat)
            newword = index_word[yhat]
            in_text += " " + newword
            if newword == "endseq":
                break
        return(in_text)

    return predict_caption(image_feats.reshape(1,len(image_feats)))[9:-7]