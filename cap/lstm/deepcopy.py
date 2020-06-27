import nltk
import numpy as np
import srt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from cap import asr


def prepare_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)


with open('../manual_subtitles/manual_2.srt') as f:
    subs = list(srt.parse(f))

with open('../manual_subtitles/manual_1.srt') as f:
    subs_2 = list(srt.parse(f))


def create_data(subs):
    data = []
    for content in subs:
        with_tags = nltk.pos_tag(nltk.word_tokenize(content.content.lower()), tagset='universal')
        sentence = [x[0] for x in with_tags]
        tags = [x[1] for x in with_tags]

        # Last tag must be
        tags[-1] = 'NL'

        data.append((sentence, tags))

    return data

training_data1 = create_data(subs)
training_data2 = create_data(subs_2)
training_data1[-1:-1] = training_data2
training_data = training_data1

transcript = asr.ASR('../asr/asrOutput.json').transcript()
transcript_tags = nltk.pos_tag(nltk.word_tokenize(transcript.lower()), tagset='universal')

sentence = [x[0] for x in transcript_tags]
tags = [x[1] for x in transcript_tags]

test_data = [(sentence, tags)]


word_to_ix = {}
for sent, tags in training_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

for sent, tags in test_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

# test_data = [("into a high-performance computer .".split(), ["ADP", "DET", "ADJ", "ADJ", "NOUN", "."])]

tag_to_ix = {"VERB": 0,
             "NOUN": 1,
             "PRON": 2,
             "ADJ": 3,
             "ADV": 4,
             "ADP": 5,
             "CONJ": 6,
             "DET": 7,
             "NUM": 8,
             "PRT": 9,
             "X": 10,
             ".": 11,
             "NL": 12}




# These will usually be more like 32 or 64 dimensional.
# We will keep them small, so we can see how the weights change as we train.
EMBEDDING_DIM = 32
HIDDEN_DIM = 32

class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim

        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)

        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word_to_ix), len(tag_to_ix))
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)


with torch.no_grad():
    inputs = prepare_sequence(training_data[0][0], word_to_ix)
    tag_scores = model(inputs)

for epoch in range(1000):  # again, normally you would NOT do 300 epochs, it is toy data
    for sentence, tags in training_data:
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()

        # Step 2. Get our inputs ready for the network, that is, turn them into
        # Tensors of word indices.
        sentence_in = prepare_sequence(sentence, word_to_ix)
        targets = prepare_sequence(tags, tag_to_ix)

        # Step 3. Run our forward pass.
        tag_scores = model(sentence_in)

        # Step 4. Compute the loss, gradients, and update the parameters by
        #  calling optimizer.step()
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

# See what the scores are after training
with torch.no_grad():
    inputs = prepare_sequence(test_data[0][0], word_to_ix)
    tag_scores = model(inputs)

    # The sentence is "the dog ate the apple".  i,j corresponds to score for tag j
    # for word i. The predicted tag is the maximum scoring tag.
    # Here, we can see the predicted sequence below is 0 1 2 0 1
    # since 0 is index of the maximum value of row 1,
    # 1 is the index of maximum value of row 2, etc.
    # Which is DET NOUN VERB DET NOUN, the correct sequence!

    count = 0
    for score, word in zip(tag_scores.numpy(), test_data[0][0]):
        print(f"{word} ", end="")
        if np.argmax(score) == 12:
            print("<BR>")
