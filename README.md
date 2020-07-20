# discord-bot-server-manager
This is a discord bot that enables users in a discord server to easily start and stop various game servers such as minecraft and terraria.

Requirements:
Linux computer/server with the following:
  Python
  Discord python module
  Internet connection
  Good enough specs to host game servers (Check publisher websites for specifics)
  SSH (Highly recommended but not required)
Knowledge of how to set up game servers
Knowledge of how to set up a discord bot

Installation & Setup:
Create a new directory, place main_bot.py, server_commands.py, and bot_config.json inside
Create a new discord project and corresponding bot, copy the bot key into the corresponding spot in bot_config.json(Keep the "")
Finish filling out bot_config.json, you may delete or add port items to fit what you need (game library uses python list synatx EX: ["minecraft", "terraria"]
Download and setup the game servers in a different directory, and test to ensure that they work
Create the necessary .sh files. They should be named with simply the game title and .sh EX: minecraft.sh OR terraria.sh
The .sh files should contain the following: 1. The line defining it as a bash script 2. A line to change the directory to where the server is located 3. A line to run the server
EX:
#!/bin/bash
cd /home/phreakester/minecraft_server
java -Xmx1G -Xms1G -jar server.jar nogui
The, give them permission to run by using the command "chmod +x the_file_name" when in the directory as the .sh file
Run main_bot.py and you should be up and running! Use the "$help" command in discord to see how to use the bot

NOTE:
For terraria servers, a configuration file must be used to avoid the setup process each time the server is started
For modded servers, the name mc_modded and t_modded should be used

If you have any questions feel free to let me know through GitHub
