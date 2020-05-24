# Speech Recognition
Speech Recognition using HMM, GMM

# Task Description
Recognize continuous english digits(numbers) through HMM(Hidden Markov Model), GMM(Gaussian Mixture Model)
Using our modeled word and universal utterance HMM, implement the Viterbi Algorithm and find out the most likely sequence of words.
We will follow the following stages to reach our desired state
![stages](/pictures/stages.png)

# phone HMM
A phone stands for the smallest unif for our language. Each word consists of one or more phones
In our hmm header, we have the transition probabilities predefined for every phone.
Each phone is divided into three HMM states. In our model we have 2 pdfs for one state.
The probability matrix will be 5 * 5 to include prior probabilities that come into the phone.

The silent "sp" phone will exceptionally have 1 state
![phones](/pictures/threeStateHMM.PNG)

# word HMM
With the phone HMM we have constructed, we bind them together to make our word HMM.
The dictionary text file defines how the words are composed.
When we construct the word HMM, we will have to recalculate the transition probabilities by recalculating them.
![wordHMM](/pictures/wordHMM.png)

# Continuous Universal Utterance HMM
In order to recognize several digits continuously, we again combine word HMMs to complete our Universal Utterance HMM.
Instead of placing the silent phones "sil" and "sp" each in the start and end, we move "sil" as a seperate word.
For the transition probability, we will have to utilize the word probabilities from the unigram & bigram textfiles.
![wordHMM](/pictures/continuousHMM.PNG)

# GMM
To calculate the observation probability, we use GMM(Gaussian Mixture Model).
When we actually implement it in code, there is a possibility that underflow will occur.
To solve this problem, we use logarithms to prevent underflow from happening.
At the last level, we combine all the pdfs with the weights into one state.
![GMM](/pictures/gmm.png)

# Viterbi
After all the calculation and constructing of the HMMs are done, we have to find the best state sequence so that the program will be able to recognize the words.
The words(speech) will be transformed into "MFCC vectors" which is of 39 dimension.
![mfcc](/pictures/mfcc.PNG)

After calculating the cumulative probability and state sequence, we use the viterbi algorithm to convert the numbers back into an actual word.
![viterbi](/pictures/viterbi.png)



# Reference
* [HMM](https://untitledtblog.tistory.com/97)
* [medium](https://medium.com/@jonathan_hui/speech-recognition-gmm-hmm-8bb5eff8b196)
* [medium](https://medium.com/@jonathan_hui/speech-recognition-acoustic-lexicon-language-model-aacac0462639)
* [medium](https://medium.com/@jonathan_hui/speech-recognition-asr-decoding-f152aebed779)
* [medium](https://medium.com/@jonathan_hui/speech-recognition-weighted-finite-state-transducers-wfst-a4ece08a89b7)
* [medium](https://medium.com/@jonathan_hui/speech-recognition-asr-model-training-90ed50d93615)
* [Speech Recognition – HMM](http://www.fit.vutbr.cz/~grezl/ZRE/lectures/09_hmm_en.pdf)
* Pawar, Ganesh S, and Sunil S Morade. "Realization Of Hidden Markov Model For English Digit Recognition". 2014.
* Uchat, Nirav S. "Hidden Markov Model And Speech Recognition(slide)". Department Of Computer Science And Engineering Indian Institute Of Technology, Bombay Mumbai.
* Wayne Ward HIDDEN MARKOV MODELS IN SPEECH RECOGNITION(slide) . Carnegie Mellon University Pittsburgh, PA
* Michael Picheny, Bhuvana Ramabhadran, Stanley F. Chen, Markus Nussbaum-Thom "Gaussian Mixture Models and Introduction to HMM’s(slide)". Watson Group IBM T.J. Watson Research Center
* Michael Picheny, Bhuvana Ramabhadran, Stanley F. Chen, Markus Nussbaum-Thom "The Big Picture/Language Modeling(slide)". Watson Group IBM T.J. Watson Research Center
