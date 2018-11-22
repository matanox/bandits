from .util import unique_argmax
import random

'''
extensible class hierarchy for bandits

naming (intentionally) mirrors mathy modularity more than terms of the genre, so for example
an arm is a Bandit and a MAB is a BanditsVec. This mirrors the ability to compose each of them 
with itself and with the other forming hierarchies, even though in standard introductory 
materials there's always only a MAB that has arms and no deeper compositions of them.
'''


class Bandit(object):
    pass
    
class Bernoulli(Bandit):
    
    def __init__(self, success_prob):
        self.success_prob = success_prob   
        
    def pull(self):
        if random.random() < self.success_prob:
            return 1
        else:
            return 0
    
    @staticmethod
    def     best_bandit(bernoulli_bandits):
        return unique_argmax(list(map(lambda bandit: bandit.success_prob, bernoulli_bandits)))

        
class BanditsVec(object):
    
    def __init__(self, bandits, best_bandit_fn):
        self.bandits = bandits
        self.num_of_bandits = len(bandits)
        self.best_bandit = best_bandit_fn(bandits)
        
    def pull(self, k):
        return self.bandits[k].pull()
       
    
class TestBanditsVec(object):
    def test_lln(self):   
        bandits = BanditsVec(list(map(Bernoulli, [0.05, 0.3, 0.35, 0.4, 0.9, 0.95])), Bernoulli.best_bandit)
        assert(bandits.best_bandit == 5)
        
        for k in range(bandits.num_of_bandits):
            results = []
            for _ in range(100000):
                results.append(bandits.pull(k))
            assert abs(np.mean(results) - bandits.bandits[k].success_prob) < bandits.bandits[k].success_prob/50
