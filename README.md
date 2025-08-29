# pybiwenger
![alt text](https://github.com/pablominue/pybiwenger/blob/main/image.jpg?raw=true)

pybiwenger is a Python Library that allows to interact with the Soccer Fantasy Game Biwenger.

## Installation

You can either install it via cloning the repository:

```bash
git clone https://github.com/pablominue/pybiwenger.git
```

or via pip

```bash
pip install pybiwenger
```

To be able to use the modules and tools this library provides, you will need to authenticate after importing the library:

```python
import pybiwenger

pybiwenger.authenticate(
    username="your_biwenger_email",
    password="your_biwenger_passowrd"
)
```

These credentials will only be stored in your local environment variables
