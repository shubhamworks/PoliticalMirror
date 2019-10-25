import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import *
import numpy as np

dictionary_size=1000

#X_train=[]
#Y_train=[]

#x_train = np.array(x_train, 'float32')
#y_train = np.array(y_train, 'float32')

#x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
#x_train = x_train.astype('float32')




def create_models():
  #Get a sequence of indexes of words as input:
  # Keras supports dynamic input lengths if you provide (None,) as the 
  #  input shape
  inp = Input((None,))
  #Embed words into vectors of size 10 each:
  # Output shape is (None,10)
  embs = Embedding(dictionary_size, 10)(inp)
  # Run LSTM on these vectors and return output on each timestep
  # Output shape is (None,5)
  lstm = LSTM(5, return_sequences=True)(embs)
  ##Attention Block
  #Transform each timestep into 1 value (attention_value) 
  # Output shape is (None,1)
  attention = TimeDistributed(Dense(1))(lstm)
  #By running softmax on axis 1 we force attention_values
  # to sum up to 1. We are effectively assigning a "weight" to each timestep
  # Output shape is still (None,1) but each value changes
  attention_vals = Softmax(axis=1)(attention)
  # Multiply the encoded timestep by the respective weight
  # I.e. we are scaling each timestep based on its weight
  # Output shape is (None,5): (None,5)*(None,1)=(None,5)
  scaled_vecs = Multiply()([lstm,attention_vals])
  # Sum up all scaled timesteps into 1 vector 
  # i.e. obtain a weighted sum of timesteps
  # Output shape is (5,) : Observe the time dimension got collapsed
  

  context_vector = Lambda(lambda x: tf.reduce_sum(x,axis=1))(scaled_vecs)


  ##Attention Block over
  # Get the output out
  out = Dense(1,activation='sigmoid')(context_vector)

  model = Model(inp, out)
  model_with_attention_output = Model(inp, [out, attention_vals])
  model.compile(optimizer='adam',loss='binary_crossentropy')
  return model, model_with_attention_output

model,model_with_attention_output = create_models()


model.fit(np.array([[1,2,3]]),[1],batch_size=1)
print ('Attention Over each word: ',model_with_attention_output.predict(np.array([[1,2,3]]),batch_size=1)[1])
