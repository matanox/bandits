# A notebook exemplifying Thompson Sampling 

Thompson Sampling is an algorithm for learning  the best reward-carrying action from a set of such actions to choose from, where the reward from each action is _a random variable_. For a mathematical delineation of the optimality characteristics of this algorithm, I recommend reading [here](http://proceedings.mlr.press/v23/agrawal12/agrawal12.pdf). There are many introductory posts on Medium on the topic, for example the following ones which greatly overlap:
([1](https://towardsdatascience.com/the-multi-armed-bandits-problem-bba9ea35a1e4
), [2](https://towardsdatascience.com/solving-multiarmed-bandits-a-comparison-of-epsilon-greedy-and-thompson-sampling-d97167ca9a50), [3](https://towardsdatascience.com/solving-multiarmed-bandits-a-comparison-of-epsilon-greedy-and-thompson-sampling-d97167ca9a50)).

## Why this repo?
This code should be tentatively more conducive to further experimentation of intriguing variants than [the equivalent code and article that inspired it](https://peterroelants.github.io/posts/multi-armed-bandit-implementation/). 

### Running on google colaboratory

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matanster/bandits/blob/master/thompson%20sampling%20mab.ipynb)

### Running locally 

To run it locally after cloning the repo, perhaps with different parameters or other enticing changes, you need to have its python dependencies available in your python environment. Using a custom virtual environment with Anaconda, I have exported the environment definition and you can pull it together after cloning this repo, e.g. via:

```
conda env create --name mab -f environment.yml
```

You may replace the name `mab` with any name you'd like to have for this virtual environment.
Of course, this assumes you have Anaconda installed. You'd then activate the environment on your end in the usual way, [the syntax subtly varies depending on your OS](https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

Alternatively use the `requirements.txt` file for setting up directly with pip3.

Or, just install whatever packages that come up as import errors, as my environment has many items unnecessary for running this project.
