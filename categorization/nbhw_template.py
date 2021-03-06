
# coding: utf-8

## Overview

# Imagine that you have a classification problem you need to solve.  You are observing items with a collection of binary features, and you need to classify them into one of two categories.  For the purpose of analysis, you assume that the data is actually generated by a Naive Bayes process.  That way you can simulate the generation of the data, learning the model, and characterize the difference between ground truth and what you learn.
# 
# You want to eventually have a classification error that's within 1% of optimal.  That's not the same as getting 99% accuracy.  Because you can't observe the true class and can only observe features that correlate with the class imperfectly, there will be some inherent uncertainty in the problem.  However, eventually, if you get enough data, you will have very accurate estimates for the underlying posterior probabilities associated with different observations.  If you classify observations based on these learned probabilities you will almost certainly match the optimal decisions you'd make if you knew the true distribution.
# 
# The challenge here is to understand how much data you need to do this.  Along the way, we can learn something about programming in python, the inherent variability of statistical sampling and machine learning, the curse of dimensionality and the use of simulations to guide engineering, experiments and analysis.

# In[1]:

import random, collections


## Representing Observations

# This notebook provides some background code for representing and manipulating observations.  A collection of related observations is encoded in python as an _event_: a dictionary pairing features with values.  Since we're going to be learning about events, we need some helper functions for dealing with collections of events:
# - Find the set of features defined for a collection of events
# - Find the set of values for a feature for a collection of events
# - Count the number of events with a specific feature
# - Split a set of events into a dictionary based on the value of a specific feature
# - Count the number of events with a specific feature-value pair (for $P(event | feature=value)$)

# In[2]:

# events are of the form:
# [ event1, event2, ... ]
# an event is of the form:
# {feature1:value1, feature2:value2, ...}

def get_features(events) : 
    """
    get_features(events): 
    iterate through the events, which are dictionaries, 
    and take the set union of all of their feature values
    using a set forces uniqueness of feature names
    """
    f = set() 
    for e in events : 
        f.update(e.keys())
    return f
        
def get_values(feature, events) :
    """
    get_values(feature, events):
    get all possible values for given feature. 
    using a set forces uniqueness of feature values
    """
    v = set()
    for e in events :
        if feature in e :
            v.add(e[feature])
    return v
            
def count_f(feature, events) : 
    """
    count_f(feature, events):
    count how many of the passed events 
    have the specified feature 
    """
    return sum(1 for e in events if feature in e)

def count_fv(feature, value, events) : 
    """
    count_fv(feature, value, events): 
    count how many of the passed events
    have the specified value for the specified feature
    """
    return sum(1 for e in events if feature in e and e[feature] == value)

def split_f(feature, events) : 
    """
    split_f(feature, events) :
    divide the passed events into groups based on the values
    they have for the passed feature.
    returns a dictionary of the form {featurevalue:[list of events]} 
    with a key featurevalue for each value for the specified feature
    that occurs in the passed list of events
    """
    result = {}
    for e in events :
        if feature in e:
            if e[feature] in result :
                result[e[feature]].append(e)
            else :
                result[e[feature]] = [e]
    return result

def extends(event, e) : 
    """
    extends(event, e) :
    returns true if e agrees with event on all the feature--value pairs in event.
    in other words, e is a special case of event with all the information in event
    and perhaps more.  this makes e an extension of event.
    """
    for f in event :
        if f not in e or event[f] != e[f] :
            return False
    return True 

def get_matches(event, events) :
    """
    this will return back each of the passed events
    which contain all the information in event 
    (in the sense of extends) 
    """
    return [e for e in events if extends(event, e)]


## Representing probabilistic models

# We start by defining some utilities for dealing with discrete probability distributions.
# 
# A discrete probability distribution is a variable plus table (a dictionary pairing keys with numbers, where the sum of values for keys is 1)

# In[3]:

class Distribution(object) :
    def __init__(self, variable, table) :
        self.variable = variable
        self.table = table
        
    def outcomes(self) :
        return (k for k in self.table.keys())
    
    def probability(self, value) :
        if value in self.table :
            return self.table[value]
        else :
            return 0.
        
    def sample(self) :
        # http://en.wikipedia.org/wiki/Inverse_transform_sampling
        v = random.uniform(0, 1)
        running_cumulative = 0.0
        for item,probability in self.table.items():
            if running_cumulative<v<running_cumulative+probability: 
                return (self.variable,item)
            running_cumulative+=probability
        raise NotImplementedError("The cuumulative should at max be 1, it wasn't, so this failed")
            
    def __repr__(self) :
        return "{%s}" % ', '.join([('P(%s=%s)=%s' % (self.variable, v, self.table[v])) for v in self.table])


# A Naive Bayes model is a collection of probability distributions:
# - A prior on classes
# - A dictionary, for each class value giving a list of likelihoods for a common set of features
# 
# The functions associated with a model include:
# - calculating the probability that the model assigns to an event E $P(E)$
# - classifying an event $E$ based on the posterior probability distribution $P(C|E)$
# - enumerating all the possible outcomes in the model and their associated probabilities
# - sampling an event at random from the model
# - calculating the expected accuracy of a classification rule on the model
# - getting the optimum classification accuracy (based on classifying each event according to its posterior probability).

# In[4]:

class NB(object) :
    def __init__(self, prior, likelihoods) :
        """make a naive Bayes model with a specified prior over classes
        and class-dependent likelihood distributions"""
        self.prior = prior
        self.likelihoods = likelihoods
        self.featuredict = {}
    
    def most_informative_features(self, total=100) :
        features = set()
        maxprob = collections.defaultdict(lambda: 0.0)
        minprob = collections.defaultdict(lambda: 1.0)
        for cat in self.prior.outcomes():
            for fdist in self.likelihoods[cat] :
                for fval in fdist.outcomes():
                    feature = (fdist.variable, fval)
                    features.add( feature )
                    p = fdist.probability(fval)
                    maxprob[feature] = max(p, maxprob[feature])
                    minprob[feature] = min(p, minprob[feature])
                    if minprob[feature] == 0:
                        features.discard(feature)

        # Convert features to a list, & sort it by how informative
        # features are.
        features = sorted(features,
            key=lambda feature_: minprob[feature_]/maxprob[feature_])
        return features[:total]

        
    def _cat_prob(self, event, category) :
        """compute the probability of the event in this model, 
        assuming that the event actually belongs to the specified category"""
        p = self.prior.probability(category)
        for dist in self.likelihoods[category] :
            if dist.variable in event :
                p = p * dist.probability(event[dist.variable])
        return p
    
    def probability(self, event) :
        """compute the probability of an event according to the model, 
        marginalizing over the event category if it's not specified"""
        if self.prior.variable in event :
            category = event[self.prior.variable]
            return self._cat_prob(event, category)
        else :
            p = 0.
            for category in self.prior.outcomes() :
                p = p + self._cat_prob(event, category)
            return p
           
    def classify(self, event) :
        """classify an event according to its probability in the model"""
        return max(self.prior.outcomes(), 
                   key = lambda c: self._cat_prob(event, c))
    
    def outcomes(self) :
        """creates a generator that yields all the (dictionary, probability) pairs
        where dictionary gives a specific event specified by the model 
        and probability gives the probability the model assigns to this event"""
        def last(desc, p) :
            return (dict(desc), p)
        def extend(generator, dist) :
            for desc, p in generator :
                for o in dist.outcomes() :
                    yield ([(dist.variable, o)] + desc, p * dist.probability(o))
        for c in self.prior.outcomes() :
            gen = (([(self.prior.variable, o)], self.prior.probability(o)) for o in [c])
            for dist in self.likelihoods[c] :
                gen = extend(gen, dist)
            for desc, p in gen :
                yield last(desc, p)
    
    def accuracy(self, rule) :
        """compute the expected accuracy of a specific classification rule
        according to the model.  Rule is a function from events to classes.
        Applies rule to each of the outcomes() of the model, with the true
        category of the outcome hidden, and sums the probability that
        the rule predicts the correct class for that outcome"""
        def correct(event) :
            copy = dict(event)
            del copy[self.prior.variable]
            prediction = rule(copy)
            return prediction == event[self.prior.variable]
        return sum(p for (event, p) in self.outcomes() if correct(event))
    
    def optimum(self) :
        """return the performance of the best possible classifier
        (namely, the one that uses the true probabilities to make its decision)"""
        return self.accuracy(self.classify)
    
    def sample(self) :
        """create a random event using the distribution defined by the model"""
        event = {}
        (k, v) = self.prior.sample()
        event[k] = v
        for dict in self.likelihoods[v] :
            (k, v) = dict.sample()
            event[k] = v
        return event
    
    def __repr__(self) :
        specs = lambda v:''.join([('  %s\total' % dist) for dist in self.likelihoods[v]])
        classes = [('Given %s\total%s' % (v, specs(v))) for v in self.prior.table]
        return "Naive Bayes Model\total%s\total%s" % (self.prior, ''.join(classes))          


# Examples to play with for the homework
# - A simple Naive Bayes model
# - Sample data drawn from the model
# - Same things for a slightly larger model

# In[5]:

frequent_events_example = NB(Distribution('icecream_preference', {'chocolate' : 0.75, 'vanilla' : 0.25}),
                             {'chocolate' : [Distribution('wears_scarves', {'yes':0.7, 'no':0.3}),
                                      Distribution('has_bunny', {'yes':0.6, 'no':0.4})],
                              'vanilla' : [Distribution('wears_scarves', {'yes':0.4, 'no':0.6}),
                                      Distribution('has_bunny', {'yes':0.3, 'no':0.7})]})
frequent_events_data = [frequent_events_example.sample() for _ in range(1000)]

rare_events_example = NB(Distribution('icecream_preference', {'chocolate' : 0.75, 'vanilla' : 0.25}),
                             {'chocolate' : [Distribution('wears_scarves', {'yes':0.7, 'no':0.3}),
                                      Distribution('has_bunny', {'yes':0.6, 'no':0.4}),
                                      Distribution('grad_student', {'yes':0.4, 'no':0.6}),
                                      Distribution('favorite_language', {'python':0.6, 'java':0.4}),
                                      ],
                              'vanilla' : [Distribution('wears_scarves', {'yes':0.4, 'no':0.6}),
                                      Distribution('has_bunny', {'yes':0.3, 'no':0.7}),
                                      Distribution('grad_student', {'yes':0.6, 'no':0.4}),
                                      Distribution('favorite_language', {'python':0.8, 'java':0.2})]})
rare_events_data = [rare_events_example.sample() for _ in range(1000)]

## Programming Problems

# *Problem 1.* Write code to do classification directly based on the observed frequency of events in the data set.  
# 
# Your answer should take the form of a function `classify_from_data(target, data, guess)` where `target` is the variable whose value you are trying to predict, `data` is the training data that you have access to, and `guess` is the value you'll guess for the target data when there's no applicable data.  It should return a function that takes an event and makes a prediction (the kind of thing that you could pass to the `accuracy` method of a Naive Bayes object).  Overall then, your code will look like this
# ```python
# def classify_from_data(target, data, guess):
#     def classify(event) :
#         # make a decision about event using data
#         ...
#     return classify
# ```
# 
# The algorithm for classify will look something like this:  Given a data point `event` and a set of examples `data`:
# - find the items in `data` that match the `event`
# - make a table of the different outcomes of `target` and how often they occur
# - find the most likely possibility in the table, if any, and return it
# - otherwise, return the default guess

# *Problem 2.*
# Write code to build a Naive Bayes model for class `prediction` based on the counts of instances in a test collection `data`.
# 
# More precisely, your answer should take the form of a function `NB_from_data(prediction, data)` which takes as arguments the target variable to predict `prediction` and a collection of events `data`.  The function should return a Naive Bayes object that represents the maximum likelihood estimate distribution given the data.

# _Problem 3._ Write a short description explaining how well you expect these functions to work.  In particular, describe how you expect the performance to depend on the number of observations you're using for classification. You can either hand in a short text or PDF document, with an associated python file, or hand in an expanded version of this python notebook documenting your thinking.
