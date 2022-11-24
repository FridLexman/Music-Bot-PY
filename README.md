# Music-Bot-PY

This is a simple music bot for discord using discord.py and FFMpeg.
This is an extremely lightweight bot, which is my main reason for writing this besides the expreience.
This bot is free for all use. 

Need To Install -

- Discord Bot Key (From your Dev Portal after setting up an application)
- FFMpeg inside the bot's root dir
- Must installed Discord.py (using pip install)
- Must install Youtube_dl (using pip install)


commands list(prefix = ".") = 

Music Commands:

play[Song name or youtube link] (Start playing songs in the queue over VOIP)
pause[No paramaters] (Pauses current song)
resume[No paramaters] (Resumes the current song)
stop[No paramaters] (Stop VOIP, doesn't disconnect, but does delete current song)
disconnect[No paramaters] (Disconnects the bot from voice channel)
clear_q[No paramaters] (Clears active song queue)

Other Commands:
clear[No paramaters] (clears 25 lins of the chat)

