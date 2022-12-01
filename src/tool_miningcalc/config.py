APP_TITLE = "Bitcoin Mining Profitability Calculator"

APP_DESCRIPTION = "This app needs a description."

node_path = None
pruned = None
pruned_height = None

# TODO change these to 0, not none.  Init to a safe state that won't cause an error when the user tinkers with the input fields before loading state from the network completes.
height = None
difficulty = None
price = None

# the number of projections that we've run.
# so we can increment the number when they are all displayed.
analysis_number = 0

# Luxor's API key
apikey = None
