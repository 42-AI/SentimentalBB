# Setup

- [Install](#install)
  - [Verify your python version](#verify-your-python-version)
  - [Install pip](#install-pip)
  - [Install virtualenv](#install-virtualenv)
  - [Create a virtualenv](#create-a-virtualenv)
  - [Install direnv for not having to think about your virtualenv anymore](#install-direnv-for-not-having-to-think-about-your-virtualenv-anymore)
  - [Initialize direnv](#initialize-direnv)
- [Initialize your repository:](#initialize-your-repository-)
- [Verify you can launch the project:](#verify-you-can-launch-the-project-)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Tools to Install

All these steps install tools to your computer, you will use them for this project, but you will also use them for your futur data-science projects !

## Python

```sh
python3 --version
Python 3.8.12
```

It should be 3.8.XX


If it's not follow these instructions:

<details>
  <summary>Click to expand!</summary>
  
1. Run the following commands as root or user with sudo access to update the packages list and install the prerequisites:
	```sh
	sudo apt update
	sudo apt install software-properties-common
	```

2. Add the deadsnakes PPA to your system’s sources list:
	```sh
	sudo add-apt-repository ppa:deadsnakes/ppa
	```
	When prompted press `Enter` to continue:
	```sh
	Output
	Press [ENTER] to continue or Ctrl-c to cancel adding it.
	```

3. Once the repository is enabled, install Python 3.8 with:
	```sh
	sudo apt install python3.8
	```


4. Verify that the installation was successful by typing:
	```sh
	python3.8 --version
	```
	```sh
	Output
	Python 3.8.X
	```

</details>


## pip

Install pip first

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.8 get-pip.py
```

If you want to learn more about pip, here is a great place: <https://realpython.com/what-is-pip/>

## Install virtualenv

Then install virtualenv using pip3
```
python3.8 -m pip install --user virtualenv
```

For more explanation on this tool you should read this page <https://virtualenv.pypa.io/en/latest/>

## Install direnv for not having to think about your virtualenv anymore

See this link: https://direnv.net/docs/installation.html

It should be something like `curl -sfL https://direnv.net/install.sh | bash` depending on your OS.

For more explanation on this tool you should read this page: <https://direnv.net/>.


# Initialize your repository:

Now all these steps are specifics to this project, and this project only !

You should first `git clone` this project, and then `cd` to it's top directory for running all the following commands.

## Create a virtualenv

```sh
python3.8 -m venv venv
```

## Initialize direnv

```sh
echo "source venv/bin/activate" > .envrc
direnv allow .
```

Now everytime you use `python` in this project it will call the binary in `venv/bin/python3.8`.

## Launch the script to initialize your project 

If it's not with execute rights, you should add them
```sh
chmod +x .42AI/init.sh
```

Then you can run the script
```sh
.42AI/init.sh
```

## Launch the project:

with this command

```sh
python -m src
```

and this one:

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```
