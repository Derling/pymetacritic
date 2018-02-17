# PyMetaCritic
Python Api for retrieving critic and user scores from metacritic

## Installation
First, clone this repository using [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) </br>
`
git clone https://github.com/Derling/pymetacritic
`</br>
**Make sure [Python 3](https://www.python.org/downloads/) is installed on your system** </br>
Secondly, install the dependencies, **I recommend creating and using a [virtualenv](https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-Python-s-virtualenv-using-Python-3) before this step**</br>
*open a terminal and cd into the repositories root folder*
```python
pip install -r requirement.txt
```

### Usage

You can create a file in the same directory as this project and imoprt it as if it were a package
```python
from metacritic import MetaCritic as mc

mc_data = mc.MetaCritic('tv', 'game of thrones')
print(mc_data.user_reviews) # all user reviews
print(mc_data.critic_reviews) # all critic reviews
```
