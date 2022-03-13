# Setup

- [Setup](#setup)
- [Tools to Install](#tools-to-install)
  * [Python](#python)
  * [Poetry](#poetry)
  * [direnv](#direnv)
  * [AWS CLI](#aws-cli)
- [Initialize your repository](#initialize-your-repository)
  * [Initialize direnv](#initialize-direnv)
  * [Launch the script to initialize your project](#launch-the-script-to-initialize-your-project)
  * [Verify you can launch the project](#verify-you-can-launch-the-project)

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


## Poetry

Install poetry, wich will help us manage python depedencies. 

This command should work:

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
By default, the installer installs the poetry tool to Poetry’s bin directory. which is located at `$HOME/.poetry/bin` on Unix.
To specify a location, one only needs to create an environment variable `POETRY_HOME` before to run the command line above:
```sh
export POETRY_HOME=/sgoinfre/goinfre/Perso/$USER/.poetry # Or any other desired location
```

For the installation you can follow detailed steps here: <https://python-poetry.org/docs/#installation>

If you want to learn more about poetry, here is a great place: <https://realpython.com/dependency-management-python-poetry/>


## AWS CLI

The AWS Command Line Interface will be necessary to push your data to the remote s3 storage.

Here are the steps you should follow for this: <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>


# Initialize your repository

Now all these steps are specifics to this project, and this project only !

You should first `git clone` this project, and then `cd` to it's top directory for running all the following commands.

## Initialize twitter credential key

```sh
echo "<name_of_key:
  	endpoint: <URL_OF_ENDPOINT>
  	bearer_token: <YOUR_BEARER_TOKEN>
  	consumer_key: <YOUR_CONSUMER_KEY>
  	consumer_secret: <YOUR_CONSUMER_SECRET>" > .twitter_keys.yaml
```


## Launch the script to initialize your project

If it's not with execute rights, you should add them

```sh
chmod +x .42AI/init.sh
```

Then you can run the script

```sh
.42AI/init.sh
```

For Hydra, wich is installed from requirements.txt, java is required,think to install it if you are on a fresh ubuntu.

## Verify you can launch the project

with this command

```sh
poetry run python -m src
```

and this one:

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```
