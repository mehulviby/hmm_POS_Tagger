# Hidden Markov POS Tagger

There are two programs : `hmmlearn.py` will learn a hidden Markov model from the training data, and `hmmdecode.py` will use the model to tag new data. 

To train the model use command: `python hmmlearn.py /path/to/input`

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called `hmmmodel.txt`. The format of the model is a dictionary saved as a json format.

To decode a file and tag each word use the command: `python hmmdecode.py /path/to/input` 

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file `hmmmodel.txt`, tag each word in the test data, and write the results to a text file called `hmmoutput.txt` in the same format as the training data. 
