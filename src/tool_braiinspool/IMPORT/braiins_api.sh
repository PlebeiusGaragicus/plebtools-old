# if [ -f ./env ]; then
#     . ./env
#     fi

# if API_TOKEN isn't set, show helpful error
if [ -z "$BRAIINS_TOKEN" ]; then
    echo "BRAIINS_TOKEN environment variable is not set - refer to README.md"
    exit
    fi

callSlushAPI()
{
    #local var='func1 local'
    curl -s $1 -H "SlushPool-Auth-Token: $BRAIINS_TOKEN"
}

# Provides information about pool performance and recently found blocks
URLstats='https://pool.braiins.com/stats/json/btc/'
# Provides information about users performance and rewards
URLprofile='https://pool.braiins.com/accounts/profile/json/btc/'
# Provides information about rewards for the last 90 days
URLrewards='https://pool.braiins.com/accounts/rewards/json/btc/'
# Provides performance data for each one of users worker
URLworkers='https://pool.braiins.com/accounts/workers/json/btc/'
# Provides information about block rewards
# https://pool.braiins.com/accounts/block_rewards/json/btc?from=2022-05-01&to=2022-05-07 
# FROMDATE=123
# TODATE=123
# URLblockrewards='https://pool.braiins.com/accounts/block_rewards/json/btc?from=$fromdate&to=$todate'
