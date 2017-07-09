# mattermost-wunderground-slash-command
Return simple weather information from wunderground

It requires python3 and supervisor on your system.

The final result is something like this

![final_result](https://github.com/mlongo4290/mattermost-wunderground-slash-command/blob/master/wunderground-weather.info.png?raw=true)

# Initial configuration
* Setup and configure supervisor. In ubuntu use `**sudo apt-get install supervisor**`
* Put the wunderground-slash-command.conf file in the conf file of supervisor. Normally is in /etc/supervisor/conf.d
* Create a virtualenv in a folder. I choosed **/srv/mattermost**
  `python3 -m venv /srv/mattermost/venv`
* Put the file **wunderground-slash-command.py** in the root folder of the project (in this case **/srv/mattermost**)
* Restart supervisor
* Configure the slash command in your mattermost team. Follow [the official doc](https://docs.mattermost.com/developer/slash-commands.html) to know how.
