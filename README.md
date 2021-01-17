# Command Line Interface for Automation Anywhere Control Room
A simple command line interface for Automation Anywhere's platform

## How to use it

1. Clone this repository
2. Authenticate (you can pass a Session Name or let it generate one at random):

```
python ./crcli.py login -u myUser -p "myPassword" -r "http://MyControlRoom.com"
python ./crcli.py login -u myUser -p "myPassword" -r "http://MyControlRoom.com" -s DevDSM
```

3. Check CLI Help to look at available Commands:

```
python ./crcli.py -h
```

4. Check CLI Help to look at available subcommands for a given command:

```
python ./crcli.py auth -h
```

5. Check CLI Help to look at available parameters for a given subcommand:
```
python ./crcli.py auth login -h
```

## Things to know:

Before you can run any of the commands, you need to **authenticate** using *python ./crcli.py auth login*:

```
python ./crcli.py auth login -u myUser -p "myPassword" -r "http://MyControlRoom.com"
```

The **authentication token** along with the **URL** and CR Version passed in the authentication call are **stored locally** and **do not need to be passed as parameters beyond the first authentication call**.

The **Session Name** needs to be passed in all calls (it serves to retrieve the URL and Authentication Token dynamically)

Apart from the initial authentication call, each call should contain **at least 1 option**: **-s** (**-s** is used to specify the **Session Name**.)

The output format can be set to CSV, DF (DataFrame) or JSON (Default) by using the -f option in addition to the -s option


## Commands & Subcommands Currently Available:

* auth
  * login: authenticate to CR
  * logout: logout of CR
  * list: list existing Sessions
* device
  * list
* role
  * list
* activity
  * list
* user
  * list
  * create: create a CR user
  * delete
  * setlogin: change the default credentials of a user
  * bot
    * list
    * show: show bot definition as JSON
    * update: update bot definition (from JSON file)
## Examples
```
# Authenticate
./crcli.py auth login -u myUser -p "myPassword" -r "http://192.168.1.100"
```

## TO DO

add more stuff, feel free to request!
