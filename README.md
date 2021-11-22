# Chart to swing converter
As seen in https://twitter.com/i_winxd/status/1462220493558366214

A program written in python that converts a chart from 4/4 time to 6/8 time a.k.a. from steady tempo to swing tempo.

## How do I use this?
Prerequisites:
* A windows 10 computer (I don't know how this works for mac users but if you've ran a python app before you'll likely know how)
1. Download the ``.py`` file.
2. Drag it into the folder of your choice. I will be assuming you're dragging it into ``C:\Users\<YOUR NAME>\Documents\swing_playground``
3. Drag your ``.json`` chart into the directory I just mentioned.
4. Whip up command prompt by typing ``cmd`` in the start menu.
5. Type ``cd <the file directory of where you put that .py file in>``. Alternatively, in Windows' file explorer, navigate to the folder where you have that ``.py`` file in, click on the 'address bar', and type ``cmd``. Has the same effect as ``cd <whatever>``.
6. **IF YOU HAVE NOT INSTALLED PYTHON YET:** Type ``python`` in the command line. The Windows 10 Microsoft store will prompt you to install python. Sometimes, if you have python installed, it may not be installed to your command prompt.
7. Type ``python chart_to_swing.py <THE CHART YOU WANT TO CONVERT>`` in the command line, where ``<THE CHART YOU WANT TO CONVERT>`` is the file name of the chart you want to convert. The file should be in the same directory as the ``.py`` file you downloaded, or in a folder of that directory, then your file name becomes ``<the folder within the folder of your .py file>/<THE CHART YOU WANT TO CONVERT>``.

FOR EXAMPLE: I want to convert the json named ``madness-hard.json`` to swing. I will type in the command prompt ``python chart_to_swing.py madness-hard.json``.

9. In the same directory of your ``.py`` file, a new ``.json`` file with the name``<NAME OF YOUR SONG>-swing.json`` should pop up. That is your converted file. Note that the name of the song is based on the song name in the chart, not the file name of the original ``json``.

**IMPORTANT: IF THE CHART YOU WANT TO CONVERT CONTAINS THE WORD 'swing' ANYWHERE IN IT (all lowercase) IT WILL DO A REVERSE CONVERSION (FROM SWING TO REGULAR TEMPO)**
*This will obviously not work if your song has tempo changes, even if you have BPM changes integrated with the chart.*

I couldn't package this to an EXE file because I didn't have time to learn how to do that. Someone please make a pull request telling me how to.
## Okay. How do I put the audio in swing tempo?
Watch this tutorial: https://www.youtube.com/watch?v=FURoa6NKQIo

## Contributions
You can make a pull request if you want to contribute to this.

## Licensing
Please credit/cite if you're using this / taking any of the source code!!! It lets other know of this (very cool) utility!!

## Other stuff I've made:
https://github.com/i-winxd/SNIFF - A fork of a FnF midi to chart converter that supports Kade/Psych engine parameters.

https://github.com/i-winxd/FnF-Spritesheet-to-PNG-seq - A tool that converts a Friday Night Funkin' sprite sheet into an image sequence, which you can then use with EzGif to create a gif out of it.
