# 3. N-Gram Language Models

<aside>
<img src="https://www.notion.so/icons/help-alternate_gray.svg" alt="https://www.notion.so/icons/help-alternate_gray.svg" width="40px" /> General maximum likelihood estimation (MLE)

</aside>

# N-Grams

Example sentence: *****its water is so transparent that*****…

Probability of ***the*** following the sentence is $P(the | \textit{(its water is so transparent that}))$

Very low probability of finding this sentence at all, let alone the combination of the sentence itself, because **************************************language is creative**************************************

Notation:

Random variables: $P(X_i = the) = P(the)$

Sequence of words: $w_1,…,w_n = w_{1:n}$ 

Joint prob: $P(w_1, w_2,…)$

Using the chain rule, $P(w_{1:n}) = P(w_1) P(w_2|w_1) P(w_3| w_2, w_1)… = \Pi^n_{k=1}P(w_k|w_{1:k})$

Still doesn’t help us with the problem of long sequences!

Introducing n-grams: approximate the history using the last ********few******** words only

Bigrams: approximate the probability of a word given all previous words, $P(w_n | w_{1:n})$, using only the conditional probability of the preceding word, $P(w_n|w_{n-1})$

Approximation: $P(w_n|w_{1:n}) \approx P(w_n|w_{n-1})$

Dependent on the Markov assumption, where we can assume the probability of a future unit doesn’t depend on too far into the past

Generalize to trigrams, looking 2 words behind, or n-grams, looking n-1 words behind

n-gram approximation, with N = n-gram size: $P(w_n|w_{1:n}) \approx P(w_n | w_{n-N+1:n-1})$

$P(w_{1:n}) \approx \Pi^n_{k=1} P(w_k | w_{k-N+1:k-1})$, allowing for extra padding at edges 

How do we estimate the bigram/n-gram probabilities: maximum likelihood estimation

MLE is achieved by taking the bigram count $C(w_{n-1}\;w_n)$ and normalizing it by the total number of bigrams that start with $w_n$ ⇒ $P(w_n | w_{n-1}) = \frac{C(w_{n-1}\;w_n)}{\sum_w C(w_{n-1}\;w)}$

Note that the number of bigrams starting with a word is equal to the unigram count of that word, so $\sum_w C(w_{n-1} \; w) = C(w_{n-1})$

⇒ $P(w_n | w_{n-1}) = \frac{C(w_{n-1}\;w_n)}{C(w_{n-1})}$

Bigram example: `<s> I am Sam </s>` 

Note the special start/end of sentence symbols, `<s>, </s>`

![Screen Shot 2023-05-30 at 4.09.39 PM.jpg](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.09.39_PM.jpg)

General case of MLE n-gram parameter estimation: (just replacing $w_{n-1}$ with $w_{n-N+1}$)

Parameter: $P(w_n | w_{n-N+1}) = \frac{C(w_{n-N+1}:w_{n-1}\;w_n)}{C(w_{n-N+1}:w_{n-1}}$

Relative frequency: ratio of the observed frequency of a sequence over the observed frequency of a prefix (like the MLE estimate for the n-gram parameter)

Example: Berkeley Restaurant Project (defunct): dialogue system that answered questions about restaurants in Berkeley, CA

![Sample sentences](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.20.26_PM.jpg)

Sample sentences

![Bigram counts](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.20.46_PM.jpg)

Bigram counts

![Unigram counts ⇒ Normalized counts](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.21.13_PM.jpg)

Unigram counts ⇒ Normalized counts

This table allows us to calculate the the probability of *******************I want English food******************* by multiplying bigram probabilities:

$P(\texttt{<s> I want English food </s>}) = P(\texttt{I | <s>}) P(\texttt{want | I}) P(\texttt{English | want}) P(\texttt{food | English}) P(\texttt{</s> | food}) = .000031$

Bigrams are usually not sufficient, so trigrams, or even 4-grams or 5-grams, are used with sufficient data

Probability are always representing in log format to produce log probabilities

This is because multiplying many small number results in even smaller numbers, resulting in numerical underflow (result of a computation is too precise for a computer to accurately represent in memory)

Log space results in slightly larger numbers, and combining probabilities is the addition of them. Converting back to a real probability is just the exponentiation of the log sum

$p_1 \times p_2 \times p_3 = \exp (\log{p_1} + \log{p_2}  + \log{p_3})$

# Evaluating Language Models

Extrinsic evaluation: performing end-to-end evaluations given an application

Intrinsic evaluation: performance evaluations of the model independent of the application

Useful bc end-to-end evals for LLMs are expensive

Common intrinsic evaluation: train & test sets

Train models on train sets, test which model produces the highest probability for the test set

Devset: test set that a model truly hasn’t seen, in case we use a particular test set too often 

Typically 80-10-10 for train-test-dev

## Perplexity (PPL)

Perplexity on a test set = inverse probability of the test set, normalized by the number of words

For test set $W = w_1\;w_2\;…\;w_N$:

$$
\begin{align*}
\text{perplexity}(W) &= P(w_1\;w_2\;...\;w_N)^{-1/N}\\
&= \sqrt[N]{\frac{1}{P(w_1\;w_2\;...\;w_N)}}\\
&= \sqrt[N]{\Pi^n_{i=1}\frac{1}{P(w_i | w_{1:i-1})}}\\
\end{align*}
$$

Parameter depends on n-gram model used 

Bigram: 

$$
\text{perplexity}(W) = \sqrt[N]{\Pi^n_{i=1}\frac{1}{P(w_i | w_{i-1})}}\\
$$

Since a higher conditional probability results in a lower perplexity ******************************************minimizing perplexity****************************************** is the goal of evaluation

Perplexity can also be interpreted as the weighted average branching factor of a language

Example: digits 1-10, each with prob 1/10

$$
\begin{align*}
\text{perplexity}(W) &= P(w_1\;...\;w_N)^{-1/N}\\
&= ((1/10)^N)^{-1/N}\\
&= (1/10)^-1\\
&= 10
\end{align*}
$$

Consider instead, that the digit 0 occurs much more frequently, so a test set like `000030000` is more reasonable ⇒ inner conditional prob would be higher (not even distributed) ⇒ perplexity would be lower ⇒ branching factor the same, but **************weighted************** branching factor is lower 

Since perplexity is a function of both the test set and ************the model************, we can evaluate different n-gram models:

![Screen Shot 2023-05-30 at 4.50.15 PM.jpg](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.50.15_PM.jpg)

Results: trigram performs the best, as it has the most information. Since it has the most context, it is less surprised than the other two models by a novel test sequence and, thus, assigns a higher probability for the sequence and, therefore, has a lower perplexity

Lower perplexity ⇒ better predictor 

Note: perplexities can be arbitrarily low if the train set leaks into the test set. Be careful!

Intrinsic improvement in perplexity doesn’t guarantee extrinsic improvement in the application, but its a good metric and correlation in general

NOTE: **********************************************************************perplexities can only be compared across models that have the same vocabularies********************************************************************** 

# Sampling Sentences from a Language Model

Sampling: choose random points in a model given their likelihood to generate (weighted) random sequences and evaluate its knowledge base 

Allows for visualization of knowledge of a model

Example: unigram case

Sampling from text of textbook, random generating a number in (0,1) to produce a interval of probability for words until `</s>` is reached

![Screen Shot 2023-05-30 at 4.57.33 PM.jpg](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.57.33_PM.jpg)

# Generalization and Zeros

Generalization grows more powerful for n-gram models as N is increased

![Screen Shot 2023-05-30 at 4.59.18 PM.jpg](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_4.59.18_PM.jpg)

Great dependence on training set: important to choose a similar genre as test

Dialect/variety of text is just as important as genre when training a model

Important problem: sparsity and zeros

Wall Street Journal corpus sample seqs: 

denied the allegations: 5
denied the speculation: 2
denied the rumors: 1
denied the report: 1

A model trained on these may assign the seq ****************denied the offer**************** a probability of 0 , since $P(offer | denied\;the) = 0$ !

Zeros may lead to model underestimating all sorts of word combinations

Even worse, any word that has a probability of 0 in the test will zero out the entire probability 

Solution: smoothing/discounting (discussed later)

## Unknown words

Two ways to handle unknown words in a test set (aka out-of-vocabulary (OOV) words):

Closed vocabulary system: test set contains only words in the training vocabulary (assumes we know the entire vocabulary already)

Open vocabulary: allows for unknown words (much more useful); model unknown words with a pseudo-word called `<UNK>`

Two methods for incorporating `<UNK>`:

Go back to a closed vocab:

1. Choose a vocabulary
2. Preprocess training set to convert all unknown words to <UNK> before training
3. Estimate probabilities for <UNK> like any other word

Build a vocab implicitly by either:

- Making any word occurring fewer than n times an <UNK> word
- Choosing the top V words to keep in vocab, make everything else <UNK>

In either case, train model with <UNK> as normal

# Smoothing

What do we do with words that are in the vocab, but appear in contexts that aren’t in training? Avoid zeroing out probs?

Smoothing/discounting: shave off prob of more frequent events to give to events we’ve never seen 

Four methods here:

1. Laplace (add-one) smoothing
2. add-k smoothing
3. Stupid backoff
4. Kneser-Ney smoothing 

## Laplace smoothing

Simply add one to all word counts (not good enough for practical uses, but pedagogical nonetheless)

Recall the unigram MLE: $P(w_i) = \frac{c_1}{N}$, for N tokens in corpus

Laplace adds one to all counts, so adjust num and denom accordingly:

$$
P_{\text{laplace}}(w_i) = \frac{c_i + 1}{N + V}
$$

Add V to denom, since each count is +1, and there are N unique counts (ie. unique words, unigram model)

Adjusted/discounted count: count that’s easier to compare to MLE counts, and can be easier turned into a probability by normalizing (dividing) by N. Denoted by $c^*$.

$$
c^*_i = (c_i + 1) \frac{N}{N+V}
$$

Note that normalizing by N will give us exactly $P_{laplace}(w_i)$, a probability 

Discounting: lowering some non-zero counts to get probability mass that will be assigned to zero counts

Alternative: discount ratio, $d_c$, ratio of discounted count to original count

$$
d_c = \frac{c*}{c}
$$

![Laplace smoothed, probabilities from above. Note the change in the calculation of the MLE bc of add-one smoothing ](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_8.03.47_PM.jpg)

Laplace smoothed, probabilities from above. Note the change in the calculation of the MLE bc of add-one smoothing 

![Reconstructed count matrix from Figure 3.1, using the discounted count equation. Note the drastic changes in the larger counts from before, because too much prob mass was shaved off](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_8.05.35_PM.jpg)

Reconstructed count matrix from Figure 3.1, using the discounted count equation. Note the drastic changes in the larger counts from before, because too much prob mass was shaved off

## Add-k smoothing

Instead of add-one, add a fraction for shave off a bit less

$$
P^*_{\text{add-k}}(w_n | w_{n-1}) = \frac{C(w_{n-1}\;w_n) + k}{C(w_{n-1}) + kV}
$$

Useful for some tasks, but still not good enough for language modeling

## Backoff and interpolation

Backoff: if the probability for a particular n-gram doesn’t exist, backoff and use the probability for the (n-1)-gram, or the (n-2)-gram, etc

Interpolation: ************always************ mix the (weighted) probability estimates from all n-gram estimators 

Linear interpolation: each n-gram gets a constant factor, $\lambda$

$$
\begin{align*}
\hat{P}(w_n|w_{n-1}\;w_{n-1}) = &\lambda_1P(w_n) \\
&+ \lambda_2P(w_n|w_{n-1}) \\
&+ \lambda_3P(w_n|w_{n-2} \; w_{n-1})
\end{align*}
$$

More sophisticatedly, each $\lambda$ is a function that’s weighted based on the context, so that if the trigram is more confident, the trigram will have more weight in the interpolated estimate

$$
\begin{align*}
\hat{P}(w_n|w_{n-1}\;w_{n-1}) = &\lambda_1(w_{n-2}:w_{n-1})P(w_n) \\
&+ \lambda_2(w_{n-2}:w_{n-1})P(w_n|w_{n-1}) \\
&+ \lambda_3(w_{n-2}:w_{n-1})P(w_n|w_{n-2} \; w_{n-1})
\end{align*}
$$

Hyperparameters are determined by using a held-out corpus, or a corpus from the training set that is withheld from the model until after it’s been trained on the remaining training set

Hyperparameters are set such that they maximize accuracy on the held-out corpus. Like an intermediary test set 

When using backoff, we must discount the higher order probabilities for the lower order n-grams

Katz backoff: solves this by using $P^*$ as seen above if the n-gram exists, or backs off to some other probability distribution, properly distributed by some function $\alpha$

$$
P_{BO}(w_n | w_{n-N+1}:w_{n-1}) = \begin{cases}
P^*(w_n | w_{n-N+1}:w_{n-1}) &\text{if} \;C(w_{n-N+1}) > 0\\
\alpha(w_{n-N+1}:w_{n-1})P_{BO}(w_n | w_{n-N+2}:w_{n-1}), & \text{otherwise}
\end{cases}
$$

Often combined with smoothing method called Good-Turing backoff

# Huge Language Models and Stupid Backoff

Huge corpora generated from the Internet

Web 1 Trillion 5-gram corpus: released by Google

Collection of 1-gram to 5-gram of all five word sequences found in >40 books, in English

Google Books Ngrams: released by Google

Larger corpora of their collections of books in many languages for many different n-grams

Corpus of Contemporary American English (COCA)

Balanced across English genres

Storage of large language models:

Words stored in memory, word strings represented as 64-bit hash numbers of word, probabilities stored in 4-8 bits, n-grams stored as reverse tries

Stupid backoff: in huge language models, sufficient to give up on creating a proper prob distribution

Backoff to lower n-grams without discounting. Results in not a distribution

![Screen Shot 2023-05-30 at 10.09.59 PM.jpg](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_10.09.59_PM.jpg)

# Advanced: Kneser-Ney Smoothing

# Advanced: Perplexity’s Relation to Entropy

# Summary

![Screen Shot 2023-05-30 at 10.14.54 PM.jpg](3%20N-Gram%20Language%20Models%201b9c22c3cd754872b87ea3c04f65bc31/Screen_Shot_2023-05-30_at_10.14.54_PM.jpg)

# Bibliography and History

Some good papers to reference here, see textbook