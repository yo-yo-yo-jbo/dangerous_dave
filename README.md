# A very dangerous Dave
This is an unusual blogpost about a bug (vulnerability?) that has been bothering me for years.  
When I was a kid I used to play tons of old DOS games. [Commander Keen](https://en.wikipedia.org/wiki/Commander_Keen)? With pleasure! [SkyRoads](https://en.wikipedia.org/wiki/SkyRoads_(video_game))? I remember most stages by heart. [AlleyCat](https://en.wikipedia.org/wiki/Alley_Cat_(video_game))? Oh yes!  
Well, one of the most remembered games from that era is [https://en.wikipedia.org/wiki/Dangerous_Dave](Dangerous Dave).  
You see, Dangerous Dave was a platformer - it had 10 levels, with each one your goal is to get to a trophy and pass through a door.  
Some of these levels had `Warp Zones` which are "secret levels", and you get to them by going out-of-bounds.  
Being an inquisitive young boy, I tried to find all warp zones, and I accidently found an unexpected one in level 6, which caused an unexpected behavior.  
Here is a video recording of that:
<video src='dave_oob.mp4' width=180/>

I believe this was an obvious [out-of-bounds-read](https://cwe.mitre.org/data/definitions/125.html), but as a kid I never investigated it further.  
MANY years went by, until finally I had some spare time to try and understand what happens there.  
This led me to an interesting rabbit hole that I'd like to share today!

## LZEXE
The game comes packed in one file only - `DAVE.EXE` (sha1 = `b0e70846c31d651b53c2f5490f516d8fd4844ed7`), its size is merely 76597 bytes!  
I was hoping to see many strings, but didn't see any. Opening it in IDA revealed it might be packed - and so I started searching online.  
That led me to a thriving modding community - [shikadi.net](https://moddingwiki.shikadi.net/wiki/Dangerous_Dave) (if you don't know what a "Shikadi" is, you should play more [Commander Keen](https://en.wikipedia.org/wiki/Commander_Keen)). They had very complete records of 
