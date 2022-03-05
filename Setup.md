# Install

## Verify you python version


```sh
python --version
Python 3.8.12
```

It should be 3.8.X

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


## Install pip

Install pip first

```
sudo apt-get install python3-pip
```

## Install virtualenv

Then install virtualenv using pip3
```
sudo pip3 install virtualenv 
```

## Create a virtualenv

```sh
python3.8 -m venv venv
```

## Install direnv for not having to think about your virtualenv anymore

See this link: https://direnv.net/docs/installation.html

## Initialize direnv

```sh
echo "source venv/bin/activate" > .envrc
direnv allow .
```