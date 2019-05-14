## How to use this Python script which functions as a Datadog custom Agent check

Use [this](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#overview) reference URL for detailed documentation.

#### This section will set up the agent so that it can use the custom check.
1. On the system running the Datadog agent go to the /etc/datadog-agent/conf.d directory.
2. Create a file called `custom_miistatus.yaml` inside the directory and add the following content inside the file.
- **Note:** The `min_collection_interval` attribute controls how often the agent check will run in units of seconds.
~~~~
init_config:

instances:
  - min_collection_interval: 30
~~~~

#### This section provides the custom Python script to the agent for use.
1. On the system running the Datadog agent go to the /etc/datadog-agent/checks.d directory.
2. Copy the file from this repository `custom_miistatus.py` into the directory.

#### This section describes which lines in the script **need to be modified** to reflect your environment.
- line 25: `dir = "/home/ubuntu/bonding"` 
    - Change the value of `dir` to match your platform, for example use `/proc/net/bonding`
- lines 80, 88, 101 and 108: `"owner:et"`
    - Change this tag which is a key:value pair to whatever is desired to reflect your environment.

#### ***Once the above steps are followed, restart the agent.***
