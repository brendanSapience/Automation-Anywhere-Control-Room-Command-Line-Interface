# Command Line Interface for Automation Anywhere Control Room & IQ Bot
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
python ./iqcli.py -h
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

* Control Room Commands (crcli):
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

  * wlm
    * list
    * show

  * workitem
      * list
      * add
      * show
      * delete

  * creds (credentials)
      * list
      * show

* IQ Bot Commands (iqcli):
  * li (learning Instance)
    * list
    * show
    * list_files
    * list_groups
  * group
    * list
    * update (activate or deactivate)

## Examples
```
# Authenticate
python ./crcli.py auth login -u myUser -p "myPassword" -r "http://192.168.1.100"
```

```
# List all Learning Instances (and display as DataFrame)
python ./iqcli.py -s RedDog -f DF li list
```

```
# List files under a Learning Instance with ID 0e832b48-f016-4401-8c6b-0f56fa0afa00 (and display list as CSV)
python ./iqcli.py -s RedDog -f CSV li list_files -i 0e832b48-f016-4401-8c6b-0f56fa0afa00
```

```
# List files in Validation under a Learning Instance with ID de0c78da-7700-4fe8-b05e-4de8982a9cd1 (and display list as JSON)
python ./iqcli.py -s RedDog li list_files -i de0c78da-7700-4fe8-b05e-4de8982a9cd1 -t VALIDATION
```


```
# List groups in Learning Instance with ID de0c78da-7700-4fe8-b05e-4de8982a9cd1 (and display as DataFrame)
python ./iqcli.py -s RedDog -f DF li list_groups -i de0c78da-7700-4fe8-b05e-4de8982a9cd1
```

```
# Turn On all Groups in Learning Instance with ID 5e098ba6-9e74-4457-bd49-65853f713da7 (and display result as DataFrame)
python ./iqcli.py -s RedDog -f DF group update -i 5e098ba6-9e74-4457-bd49-65853f713da7 -g ALL -s ON
```

```
# Update the content of a Bot
# Step 1: list existing bots to get Bot ID
python ./crcli.py -s PurpleEagle -f DF bot list -l "Api"

  desc    id               name parentId                                               path                          type
0        661           API Bots       10                  Automation Anywhere\Bots\API Bots  application/vnd.aa.directory
1        662  API_Triggered_Bot      661  Automation Anywhere\Bots\API Bots\API_Triggere...    application/vnd.aa.taskbot
2       1031           MyApiBot      661         Automation Anywhere\Bots\API Bots\MyApiBot    application/vnd.aa.taskbot

# Step 2: Get Bot definition as JSON
python ./crcli.py -s PurpleEagle bot show -i 1031 > Bot1031.json

# Step 3: Modify the JSON file as needed

# Step 4: Update the Bot with the new JSON Definition
python ./crcli.py -s PurpleEagle bot update -i 1031 -d ./Bot1031.json
```

```
# Add 2 workitems to a queue
python ./crcli.py -s ${CRSESSIONNAME} -f DF workitem add -i 3 -w "{'workItems':[{'json': {'firstname': 'Yli','lastname': 'Z','dob': '1111111','membershipnumber': '1'}},{'json': {'firstname': 'Linus','lastname': 'Z','dob': '1111111','membershipnumber': '2'}}]}"
```

```
# Delete 3 workitems from a queue (ids 25, 26 and 27)
python ./crcli.py -s ${CRSESSIONNAME} -f CSV workitem delete -i 3 -w 25,26,27
```


```
# Update the Password Settings for CR
# Step 1: get current settings
python ./crcli.py -s AdminEagle admin show -t password > ./currentSettings.json

# Step 2: Modify the JSON file as needed (ex: set securityQuestionsEnabled to false)

# Step 3: Update the settings with the new JSON Definition
python ./crcli.py -s PurpleEagle admin update -t password -d ./currentSettings.json
```

```
# Update the SMTP Settings for CR
# Step 1: get current settings
python ./crcli.py -s AdminEagle admin show -t smtp > ./smtpSettings.json

# Step 2: Modify the JSON file as needed

# Step 3: Update the settings with the new JSON Definition
python ./crcli.py -s PurpleEagle admin update -t smtp -d ./smtpSettings.json
```


## TO DO

  * Update Workitem (Status or content)
  * Credential vault import
  * Credential vault export

feel free to request additional items
