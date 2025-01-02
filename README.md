# Small Enemy Spider
A bit of a joke Discord Bot meant to play music from either Youtube or recorded music stored as .wav files.

<hr>
<h1>HOW TO USE</h1>
<hr>

First, you'll need to use the Developer Portal on Github in order to create a new Discord Bot, which will give you an API key. Place that API key into apikeys.py, stored as the single variable there. From there, create two empty folders, "Storage" and "Audio". Finally, run main.py. If it complains about FFMpeg, consider downloading and placing FFMpeg into the folder.

<hr>
<h1>BOT COMMANDS</h1>
<hr>

Anything in [] is mandatory, while anything in {} is optional.

<ul>
  <li>: play [YOUTUBE LINK] {START} {END} - Plays a song from Youtube, cropping it between the start and end if provided. Both are in seconds.</li>
  <li>: play_storage [PATH] - Plays a song from the Storage folder. The path to said song starts inside of the storage folder, so if you have a song named "music.wav" inside of the folder, the comamnd is "play_storage music".</li>
  <li>: join - Join the current call that you are in. It also automatically does this if you just run "play" or "play_storage"</li>
  <li>: stop - Stop the current song.</li>
  <li>: resume - Resume the song that was currently being played.</li>
  <li>: leave - Leave the current call that the bot is in.</li>
</ul>
