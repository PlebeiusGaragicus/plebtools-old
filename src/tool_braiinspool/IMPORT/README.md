# BraiinsPoolAPI

https://help.braiins.com/en/support/solutions/articles/77000433512

This repo utilizes the above API from Braiins Pool.

It periodically passes data to your Adafruit IO dashboard and can set triggers (future development needed) in order to alert you in case of a disruption to your bitcoin miners.

# step 1 - download and setup python environment

```sh
git clone https://github.com/suchdatums/BraiinsPoolAPI.git
cd BraiinsPoolAPI

#apt-get install python3-venv
python3 -m venv venv/
source venv/bin/activate

python3 -m pip install --upgrade pip
pip install -r requirements.txt

chmod +x ./run
```

# step 2  - Braiins Pool API access

setup your Braiins Pool account for API access and get your access 'token' (refer to the guide above)

# step 3 - store access token

Place that secret access token in either one of two places:

Edit the file `env.example` in the repo folder to include the token **and rename the file to: `env` (remove the '.example')

# step 4 - Adafruit IO setup

Do the exact same as above for your Adafruit IO username/key

Also, you need to make a corresponding 'feed' for each miner.  These feeds need to be named "braiins_username.workername" - whatever your Braiins pool user name is, then a dot, then the worker name for that machine.

Then, create a dashboard and include a graph block that pulls from each miner feed.  This way you can view your dashboard and see a real-time graph of your machines.

# how to use this project

There are a few scripts you can call to query Braiins Pool and send specific metrics to Adafruit IO to graph

To get metrics from every miner and send all at once, do this:

```sh
./run update_all_workers
```

You can setup a cron job to run a script periodically
