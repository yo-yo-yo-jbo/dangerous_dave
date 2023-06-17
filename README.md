# A very dangerous Dave
This is an unusual blogpost about a bug (vulnerability?) that has been bothering me for years.  
When I was a kid I used to play tons of old DOS games. [Commander Keen](https://en.wikipedia.org/wiki/Commander_Keen)? With pleasure! [SkyRoads](https://en.wikipedia.org/wiki/SkyRoads_(video_game))? I remember most stages by heart. [AlleyCat](https://en.wikipedia.org/wiki/Alley_Cat_(video_game))? Oh yes!  
Well, one of the most remembered games from that era is [https://en.wikipedia.org/wiki/Dangerous_Dave](Dangerous Dave).  
You see, Dangerous Dave was a platformer - it had 10 levels, with each one your goal is to get to a trophy and pass through a door.  
Some of these levels had `Warp Zones` which are "secret levels", and you get to them by going out-of-bounds.  
Being an inquisitive young boy, I tried to find all warp zones, and I accidently found an unexpected one in level 6, which caused an unexpected behavior.  
Here is a video recording of that:
https://github.com/yo-yo-yo-jbo/dangerous_dave/raw/main/dave_oobr.mp4

The idea of level 6 was to go right, take the trophy and touch the door, however, *the door is treated as empty space if you still do not have the trophy*.  
I believe this was an obvious [out-of-bounds-read](https://cwe.mitre.org/data/definitions/125.html), but as a kid I never investigated it further.  
MANY years went by, until finally I had some spare time to try and understand what happens there.  
This led me to an interesting rabbit hole that I'd like to share today!

## LZEXE
The game comes packed in one file only - `DAVE.EXE` (sha1 = `b0e70846c31d651b53c2f5490f516d8fd4844ed7`), its size is merely 76597 bytes!  
I was hoping to see many strings, but didn't see any. Opening it in IDA revealed it might be packed... I noticed it resolves some interrupt handlers from the interrupt handler table and even hooks the "divide by zero" handler (I talked about the subject [in the past](https://github.com/yo-yo-yo-jbo/mbr_analysis/).  
It was later clear to me the code was compressed, and while I could have worked my way through it, I decided to search online.  
That led me to a thriving modding community - [shikadi.net](https://moddingwiki.shikadi.net/wiki/Dangerous_Dave) (if you don't know what a "Shikadi" is, you should play more [Commander Keen](https://en.wikipedia.org/wiki/Commander_Keen)). They had very complete records of the file format(s) and even a link to one Ghidra project file with some important notes. I can honestly say it saved me tons of work, and that's an important lesson too - it's cheaper to search online rather than embark on heavy reverse-engineering on your own.  
