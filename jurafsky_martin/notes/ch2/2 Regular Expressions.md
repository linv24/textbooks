# 2. Regular Expressions, Text Normalization, Edit Distance

# Intro

ELIZA: simple NLP system developed by Romanian psychologist Weizenbaum

Simple algorithm for generating responses, but felt real to those who interacted with it

Chatbots

Text normalization: breaking text into workable parts for computation

Tokenization: Breaking words into tokens

Spaces usually sufficient, but not always (eg New York)

Regular expressions

Lemmatization: determining if two words have the same word (eg stemming)

# Regular Expressions

## Basic regular expression patterns

Regular expressions: language for specifying text search strings 

Concatenation: `/asdlfkjz/`, simple string of characters

Disjunction: `[abc]`, group of characters

Range: `[0-9]`

Kleene *: `*`, “cleany star”

Kleene +: `+`

Anchors: `[^$\b]`, define word boundaries 

## Disjunction, grouping, and precedence

Disjunction operator: `|`

Parentheses used to group expressions

Operator precedence hierarchy: PEMDAS for regex

Parentheses → Counters (`*?+{}`) → Sequences/Anchors → Disjunction 

Greedy (default) vs non-greedy (specified by `?`)

## A simple example

`/the/` → won’t match capitals (false neg)

`/[tT]he/` → will match in middle of words (false pos)

`/\b[tT]he\b/` → might still want to match things like underscores or `the25` where there are still characters (false neg)

`/[^a-zA-Z][tT]he[^a-zA-Z]/` → won’t match the at beginning of line (false neg)

`/(^|[^a-zA-Z])[tT]he[^a-zA-Z]/` → good!

False positive: strings that are incorrectly matches

Precision: minimizing false positives

False negative: strings that are incorrectly missed

Recall: minimizing false negatives 

## More operators

Reference some regex page/table for other operators 

## A more complex example

Want to match prices under $999.99

`/$[0-9]+/` → won’t match cents (FN). Note that `$` here is actually a dollar sign

`/$[0-9]+\.[0-9]{2}/` → now it won’t match things without cents (FN). Also ensure word boundary

`/(^|\W)$[0-9]+(\.[0-9]{2})?\b/` → matches prices that are too large!

`/(^|\W)$[0-9]{0,3}(\.[0-9]{2})?\b/`

## Substitution, capture groups, and ELIZA

Substitutions: `s/expr/sub/`

Number operator: `\1`, reference previous group

Capture group: parentheses to mark groups

Register: capture group stored in register for reference, numbered in linear order

Non-capturing group: might want to use parentheses for grouping but not capture group

Use `?:` after open paren to denote, `(?: expr)`

ELIZA used substitutions and a hierarchy of rules to simulate a conversation. More on ELIZA’s architecture in chapter 15

## Lookahead assertions

Positive lookahead: `(?= expr)`, returns true if expr occurs

Negative lookahead: `(?! expr)`, similar 

# Words

Words might have different definitions (ie cutoffs) based on the context; not always just any punctuation marks

Disfluencies: non grammatical utterances

Fragment: cut off word

Fillers: “uh”, “um”

Lemma: set of lexical forms that have the same stem, same part of speech, and same word-sense

Word-form: fully inflected or derived form of a word

Word types: number of unique words (if a vocabulary has V words, number of word types = |V|)

Tokens: total number of words in an utterance/sentence, nonunique

Herdan’s Law: equation for the relationship between word types $V$ and tokens $N$:

$|V| = kN^\beta$, where $k$ and $\beta$ are positive constants, with $0 < \beta < 1$

# Corpora

One of the most important dimensions of language is its variation

Language variation: testing NLP algos on languages **********************************other than English**********************************

Code switching: when speakers switch between languages mid sentence

Genre variation: the genre in which a text is written can affect the vernacular, tone, etc. of the text

Datasheet/data statement: specifies properties of a corpus to define the context in which it was written/collected

Motivation

Situation

Language variety

Speaker demogrphics

Collection process

Annotation process

Distibution 

# Data Normalization

Normalization process typically involves at least three tasks:

1. Tokenizing into words
2. Normalization word formats
3. Segmenting sentences

## Unix tools for crude tokenization and normalization

Get crude word count using `tr, sort, uniq`

Show that most common words in Shakespeare, as per most texts, are function words, like articles, pronouns, prepositions 

## Word tokenization

Whereas the Unix version simply removed all punctuations and numbers for analysis, tokenization typically wants to keep most of this. Here lies the problem of determining what punctuation to throw away (ending periods) vs keep (periods within contractions like Ph.D)

Different tokenizers may be built for different purposes

Tokenizers can even help with expanding clitic contractions, where a clitic is a word that only makes sense in combination with another word/clitic (eg the ‘m in I’m)

Tokenization often tied to named entity recognition, or the recognition that phrases (eg. separated by spaces) like “New York” or “rock ‘n’ roll” are phrases and should be kept as a single “word”

Penn Treebank tokenization standard: standard used by the Linguistic Data Consortium (LDC) to tokenize sentences

Separates clitic contractions (doesn’t → does n’t), keeps hyphenated words as a single word, and separates (**********************not removes**********************) punctuation

Tokenizers are the first process in NLP, so they must be fast

Built using regex in deterministic algorithms, compiled into very efficient finite state automata 

For languages like Japanese or Thai, where the individual characters are too short to represents any meaning at the morpheme level, word segmentation is performed using neural sequence models

### Byte-pair encoding for tokenization

Instead of delimiting words by spaces or by characters, we can use the data to determine tokens for us

Eg. to deal with unknown words by making subwords, where “lower” is turned into “low” and “-er”

Tokenization scheme: token learner (given a corpus, build vocab), token segmenter (given a sentence, generate tokens)

Three main algorithms:

Byte-pair encoding

Unigram language modeling

WordPiece

Byte-pair encoding (BPE):

First start with a set of all unique characters (including a word end character “_”)

Count all adjacent pairs of characters, determine the most common

Form a new word by combining the most common adjacent words/characters, add to vocab

Form *k* new words total, parameterized by k

![Screen Shot 2023-05-26 at 2.20.11 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_2.20.11_PM.jpg)

Segmentation: given a sentence, apply the rules learned earlier ************************************************************in the order they were learned************************************************************ to form tokens in the sentence. After many merges, most common full words will be represented as tokens, and rare words will have to be tokenized by their parts

## Word normalization, lemmatization, and stemming

Normalization: choosing a standard format to represent words

Options: case-folding (not generally used), making morphologically similar words function similarly (singluar vs plural nouns are pretty similar)

Lemmatization: determining that two words have the same stems, despite their surface forms

Usually done through morphological parsing and separating words into their stems and affixes to generate a better vocab

### The Porter stemmer

A simple stemmer that applies simple rules in succession to generate a somewhat accurate lemmatized sentences (removing s, ational → ate, ing → $\epsilon$)

Easily over/under-generalizes 

![Screen Shot 2023-05-26 at 2.26.53 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_2.26.53_PM.jpg)

## Sentence segmentation

Determining how to separate individual sentences, usually by punctuation

? and ! very unambiguous, but periods are a challenge (distinguishing between abbreviations and punctuating periods)

This can be done through rules, ML, abbreviation dictionaries 

# Minimum Edit Distance

Minimum edit distance: min number of editing operations needed to transform one string into another 

Coreference: deciding whether two strings reference the same entity (Stanford President Marc Tessier-Lavigne vs Stanford University President Marc Tessier-Lavigne)

Alignment: visual correspondence between substrings of two sequences

Operation list: abbreviated forms of different edit operations 

![Screen Shot 2023-05-26 at 3.17.38 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_3.17.38_PM.jpg)

Three operations here: deletion, insertion, and substitution

Levenshtein distance: simplest cost of operations, each have cost 1

Alternative: substitutions not allowed ⇒ equivalent to a deletion, then insertion, ie. cost 2 for substitution 

## The Minimum Edit Distance Algorithm

Solve via dynamic programming (used in many common NLP algorithms) 

Solved by a tabular method

MEDA named by **************************************************Wagner and Fischer (1974)**************************************************, but independently discovered by various people

Base case: source length i, target length 0 ⇒ i deletes; source length 0, target length j ⇒ j inserts

Bottom-up approach, tabulation 

$$
D[i,j] = \text{min} 
\begin{cases}
D[i-1,j] +\text{del-cost}(source[i]) \\
D[i,j-1] + \text{ins-cost}(target[j]) \\
D[i-1,j-1] + \text{sub-cost}(source[i], target[j])
\end{cases}
$$

![Screen Shot 2023-05-26 at 3.29.01 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_3.29.01_PM.jpg)

### Alignment

MED has important implication in minimum cost alignment, used in speech recognition and machine translation

Alignment generated by visualizing edit distance in table, where same row = insertion (from source) and same column = deletion 

![Screen Shot 2023-05-26 at 3.31.03 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_3.31.03_PM.jpg)

Computing the min cost alignment: 

Augment MED algo to store backpointers in each cell pointing to originating cell (cells may have multiple backpointers)

Perform a backtrace by following paths from the final cell to the initial cell (all min cost)

![Screen Shot 2023-05-26 at 3.34.14 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_3.34.14_PM.jpg)

# Summary

![Screen Shot 2023-05-26 at 3.35.13 PM.jpg](2%20Regular%20Expressions,%20Text%20Normalization,%20Edit%20Di%2032e456c95cdc489f87c6ee1656430741/Screen_Shot_2023-05-26_at_3.35.13_PM.jpg)
