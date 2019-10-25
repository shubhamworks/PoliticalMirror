import numpy
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical

def training():
	# load ascii text and covert to lowercase
	filename = "./training_text.txt"
	raw_text = open(filename, 'r',encoding = 'unicode_escape').read()
	raw_text = raw_text.lower()


	# create mapping of unique chars to integers
	chars = sorted(list(set(raw_text.split())))
	char_to_int = dict((c, i) for i, c in enumerate(chars))


	n_chars = len(raw_text)
	n_vocab = len(chars)
	# print ("Total Characters: ", n_chars)
	# print ("Total Vocab: ", n_vocab)


	# prepare the dataset of input to output pairs encoded as integers
	seq_length = 5

	dataX = []
	dataY = []


	words= str(raw_text).split(" ")
	len_words=len(words)
	for i in range(0,len_words-seq_length-2,1):
		seq_in=words[i:i+5]
		seq_out=words[i+6]
		dataX.append([char_to_int[char] for char in seq_in])
		dataY.append(char_to_int[seq_out])


	n_patterns = len(dataX)
	# print ("Total Patterns: ", n_patterns)
	# print(dataX)

	# reshape X to be [samples, time steps, features]
	X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
	# normalize
	X = X / float(n_vocab)
	# one hot encode the output variable
	y = to_categorical(dataY)

	# define the LSTM model
	model = Sequential()
	model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
	model.add(Dropout(0.2))
	model.add(Dense(y.shape[1], activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam')

	# define the checkpoint
	filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
	checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
	callbacks_list = [checkpoint]

		
	model.fit(X, y, epochs=20, batch_size=128, callbacks=callbacks_list)


def prediction(pattern):
	try:
		filename = "weights-improvement-19-1.2793.hdf5"
		model=tf.keras.models.load_model(filename)
		# model.load_weights("./weights-improvement-19-1.2793.hdf5")
		# model.compile(loss='categorical_crossentropy', optimizer='adam')

		# load ascii text and covert to lowercase
		filename = "./training_text.txt"
		raw_text = open(filename, 'r', encoding = 'unicode_escape').read()
		raw_text = raw_text.lower()
		raw_text = raw_text.replace("\n"," ")
		chars = sorted(list(set(raw_text.split())))
		char_to_int = dict((c, i) for i, c in enumerate(chars))
		int_to_char = dict((i, c) for i, c in enumerate(chars))
		n_chars = len(raw_text)
		n_vocab = len(chars)

		# pick a random seed
		#start = numpy.random.randint(0, len(dataX)-1)
		# print ("Seed:")
		# print(pattern)
		pattern=[char_to_int[char] for char in pattern.split()]
		

		# generate characters
		#for i in range(1):
		x = numpy.reshape(pattern, (1, len(pattern), 1))
		x = x / float(n_vocab)
		prediction = model.predict(x, verbose=0)

		final_dict={}
		for key,value in zip(int_to_char.values(),prediction[0]):
			final_dict[key]=value

		return(final_dict)
	except:
		return None


# pattern = "sport sport sport sport sport"
# print(prediction(pattern))
# training()