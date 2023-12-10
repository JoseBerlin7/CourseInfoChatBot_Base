import string
import pandas as pd
import spacy  #Spacy for stemming purpose
from data import data
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


class NLU:
    def __init__(self):
        self.input_txt = ""
        self.raw_data = data().get_data()
        self.vectorizer = CountVectorizer()
        self.nlu = spacy.load("en_core_web_sm")
        self.preprocessed_data = self.preprocessing(self.raw_data)
        self.intent_model = self.train_intent_model()

    # As I've created the dataset complete manually, I know that there are no null values, Therefore proceeding the datatype conversion and other preprocessing steps
    # NOte that we're using this same method for our dataset & user input data
    def preprocessing(self, raw_data):

        # Checking if raw_data is our dataset
        if isinstance(raw_data, pd.DataFrame):

            # Normalizing and performing lemmatization on our dataset
            for i in range(len(raw_data['sentence'])):
                # Removing all Punctuations from the dataset and converting all sentences to lowercase
                sentence = self.nlu(raw_data['sentence'][i].translate(str.maketrans("", "", string.punctuation)).lower())

                # Performing lemmatization on our dataset
                raw_data['sentence'][i] = " ".join([token.lemma_ for token in sentence])

                raw_data['intent'][i] = raw_data['intent'][i].translate(str.maketrans("", "", string.punctuation)).lower()
            preprocessed_data = raw_data
        else:
            sentence = self.nlu(raw_data.translate(str.maketrans("", "", string.punctuation)).lower())

            # Performing lemmatization on our input data
            preprocessed_data = " ".join([token.lemma_ for token in sentence])

        return preprocessed_data

    # Training our intent recognition model using our preprocessed data
    def train_intent_model(self):
        # Performing One-hot encoding on the sentence column
        x = self.vectorizer.fit_transform(self.preprocessed_data["sentence"])

        # Splitting the data as 90 -10 as we have less amount of data
        x_train, x_test, y_train, y_test = train_test_split(x, self.preprocessed_data['intent'], test_size=0.2,
                                                            random_state=42)

        # Creating our intent prediction model, we're using Logistic regression for that
        log_model = LogisticRegression(max_iter=1000)
        log_model.fit(x_train, y_train)

        y_pred = log_model.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred)
        # print(accuracy)

        return log_model

    def get_intent(self, inp):

        # Converting the input to all lower case and removing all punctuations in the input and making the input as an array
        processed_inp = [self.preprocessing(inp)]

        # One-hot encoding the inp data
        processed_inp = self.vectorizer.transform(processed_inp)

        # predicting the intent of the input text using the trained model
        intent = self.intent_model.predict(processed_inp)
        intent = str(intent[-1])

        # print(intent)
        return intent

    def all_intents(self):
        return self.preprocessed_data['intent'].unique()
