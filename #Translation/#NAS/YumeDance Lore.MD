# YumeDance
YumeDance (夢ダンス) uses lucid dreaming as a form of entertainment.

Basically: Mostly a way to expand lore on this game by showing games/entertainment played in the game's world.

```
YumeDance is a new form of entertainment that uses your mind to truly immerse you into the game world.
・Use all of your five senses: Sight, Sound, Touch, Smell, Taste
・No controllers needed, just move with your body, directly interact with objects in the game world.
・Now doesn't require any Enabler to enjoy, just a PostTome.
・And get a good night's sleep as you have fun.
```


```
"I've heard that YumeDance is the newest medium for entertainment and it allows you to learn stuff way faster than games and books. One of my friends just gave me one of her PostTomes which doesn't have anything on it yet. Got any list of programs I should check out?"
```

```
"・All of the MaBouru user guides, they'll teach you how to use spells that your enabler has. They also make for good training tools for people without an Enabler too so they can learn it innately.
・Auto Rapido 2 is a great driving sim with really realistic physics and absolutely aggressive yet competitive AI. Just don't crash (or do, the damage is probably the most realistic I've seen).
・Strike Ops just got a YumeDance port. Way better experience than on PC VR since you have all five senses working. You can sniff out an enemy and kill them before they see you.
・If you want an RPG or something more story-based, go play PopuVille. Big city crime simulator, do whatever the hell you want, but I mainly like fucking around with the cops.
・H games? Gensou Deuru Onani. You can have sex with anyone in Gensokyo, and do anything to them too. Tie them up, beat them to a pulp, make them piss a river (with the Pamper Emporium mod), whatever you want.

In Gensokyo you're connecting to online servers over at Tokyo, which is probably better than having to connect to servers at the Seihou World. Lunar Capital and Makai have their own servers.
Danmaku World also has their own program called Danmaku World Recollection (DWR)."
```

```
"You can buy programs over at the YumeDance site (yumedance.jp). Most games are around ¥3500, though I've seen some at ¥8000, but that's mainly the AAA stuff (I'm talking about you Pipeworks)
If you can't afford it you can always just pirate the programs. They're just advanced computer programs which anyone can upload.
MORERO is the main cracking group for YumeDance stuff. They mainly focus on R-18 and R-18G things but they still release a lot of General rated programs.
To use a YumeDance program you need a PostTome. Gensou-chan seems to be the main importer of these. To transfer a program to a PostTome just use the included USB-C PHYSlink port and plug it into a computer."
```


- "Recollection" bug: When a YumeDance program is played enough times by the same user, it can cause normal lucid dreams that behave mostly like a YumeDance program. This is an inherent flaw of the system and cannot be patched as it's a brain issue.

# Glossary

- `orngw`: Ogiso's Register Next Generation Web domain
    - mainly a way of saying that these domains aren't real ones.
- `IA`: YumeDance store designation for an indie program or mod (like DLSite's `RJ` ID)
- `VA`: YumeDance store designation for a commercial program (like DLSite's `VJ` ID)
    - Examples:
        - Pipeworks Gaming Group
        - ZeccHou Soft Co. Ltd.
        - International Technology Co.
- Enabler: See the Enabler section
- PostTome: A hardware kit, around the size of a novel that allows the transmission of a YumeDance program and initiates the lucid dream process. A fingerprint reader is used to initialize YumeDance programs. A USB-C PSYSlink is available for faster initialization of programs for Enabler owners.
- Content Ratings:
    - N/A: This product has not been given an age rating by the publisher, or YumeDance.
        - It can be something as benign as something General rated or extreme at R-18G
    - General: Content made for all ages
        - Closest analogue: ESA ESRB E, PEGI 3, CERO A
    - 9+: Content made for people that are 9 years or older
        - Closest analogue: ESA ESRB E10, PEGI 7, CERO B
    - 12+: Content made for people that are 12 years or older
        - Closest analogue: ESA ESRB T, PEGI 12, CERO C
    - 15+: Content made for people that are 15 years or older
        - Closest analogue: ESA ESRB M, PEGI 16, CERO D
    - R-18: This program is for adults only and is not suitable for people under the age of 18. Mostly used for erotic games.
        - Closest analogue: DLSite's R-18 rating, PEGI 18, ESA ESRB AO
    - R-18G (G for grotesque): R-18 + contains extreme fetish content (ero guro, scat).
        - Closest analogue: Pixiv's R-18G rating

Dates are DD.M.YY, four month years:
- 22.2.15 -> 2015, Summer 15
- Months
    - 1: Spring
    - 2: Summer
    - 3: Fall
    - 4: Winter

## Enabler
Magic cybernetics that give people magic powers

- Old YumeDance files (YumeDance V1) required an enabler to play.
- YumeDance DreamSIM files no longer require an enabler but using one with it will increase transfer speed
- All in-head enablers, such as the MaBouru Gold, have PHYSlink via USB which drastically increases file transfer speed

### Enabler Data

Example MabAPI output
```
     Version:  MabAPI version (2.2 is the latest)
     Device:   Enabler Name (Enabler Core Name) (ID=PCI Device ID)
     Vendor:   Enabler Manufacturer
     RAM:      RAM in MB (1GB = 1024MB)
     Driver:   Version of the driver used. Currently this PostTome uses 4.0.99999.9999
```

#### YumeDance DreamSIM Embedded PostTome Enabler
`Using the same enabler core as the MaBouru Basic, the DreamSIM PostTome's main function is to act as a vector for user to interface with the YumeDance platform. Because it has to use physical biometrics without the assistance of an internal enabler, it's transfer speeds are very slow. It also cannot be used to cast magic. Connectivity is done via a palm sensor in which the data is transferred into the brain. This allows for users without an enabler to enjoy YumeDance.`

- MP Buff: None
- Youjutsu Enhancement: None
- RAM: 128GB shared
- PHYSlink: None

MabAPI output
```
     Version:  MabAPI 2.2
     Device:   YumeDance DreamSIM Embedded PostTome Enabler (ZUN) (ID=0x01a5)
     Vendor:   YumeDance Inc.
     RAM:      131072 MB
     Driver:   4.0.99999.9999
```

#### MaBouru Basic Mk.1 Youjutsu Enabler
`A magic box which allows for outsiders to use Youjutsu abilities, and can enhance a natural Youkai's Youjutsu capabilities. Not the most powerful enabler on the market, but capable of performing multiple tasks - even if it does require a little patience.`

- MP Buff: 500
- Youjutsu Enhancement: Lv.3 B
- RAM: 12GB
- PHYSlink: USB3.1 10 Gbit/s

MabAPI output
```
     Version:  MabAPI 2.2 [PHYSlink Active]
     Device:   MaBouru Basic (ZUN) (ID=0x00a2)
     Vendor:   MaBouru Youjutsu Enablers, LLC.
     RAM:      12000 MB
     Driver:   4.0.99999.9999
```

#### MaBouru Gold Mk.2 Youjutsu Enabler
`AIA statistics show this is the most common enabler for Outsider magic activity. Why? Because it's cost-effective, user-friendly and doesn't crap out when you need something done quickly and quietly.`

- MP Buff: 500
- Youjutsu Enhancement: Lv.4 A
- RAM: 16GB
- PHYSlink: USB3.1 10 Gbit/s

MabAPI output
```
	 Version:  MabAPI 2.2 [PHYSlink Active]
     Device:   MaBouru Gold (CROTE) (ID=0x00ba)
     Vendor:   MaBouru Youjutsu Enablers, LLC.
     RAM:      16384 MB
     Driver:   4.0.99999.9999
```

#### Youkai Mountain Kappa Armory Warfighter Mk.3
`The Youkai Mountain Kappa Armory takes pride in the fact that its enablers are indispensable in combat operations around Gensokyo. Even if it's not entirely true, one thing's for sure - these enablers are powerful, effective and optimized for offensive daemons`

- MP Buff: 1500
- Youjutsu Enhancement: Lv.5 S
- RAM: 32GB
- PHYSlink: USB3.2 20 Gbit/s

MabAPI output
```
     Version:  MabAPI 2.2 [PHYSlink Active]
     Device:   YMKA Warfighter (MITORI) (ID=0x00a2)
     Vendor:   Youkai Mountain Kappa Armory
     RAM:      32768 MB
     Driver:   4.0.99999.9999
```

#### Youkai Mountain Kappa Armory Assist Hand Mk.4
`This beauty's fit for champions. How come? Because every element of this enabler serves one goal - boosting your most powerful and advanced Youjutsu.`

- MP Buff: 4000
- Youjutsu Enhancement: Lv.6 Extra
- RAM: 64GB
- PHYSlink: USB3.2 20 Gbit/s

MabAPI output
```
     Version:  MabAPI 2.2 [PHYSlink Active]
     Device:   YMKA Assist Hand (NITORI) (ID=0x00bf)
     Vendor:   Youkai Mountain Kappa Armory
     RAM:      65536 MB
     Driver:   4.0.99999.9999
```

#### Gensou-chan Hypermancy Mk.5
`An Enabler used by the best Makai agents and a frightening beast in terms of its offensive capabilities. It's best if Reimu didn't catch you using this`

- MP Buff: 8000
- Youjutsu Enhancement: Lv.8 Overdrive
- RAM: 128GB
- PHYSlink: USB4 2.0 80 Gbit/s

MabAPI output
```
     Version:  MabAPI 2.2 [PHYSlink Active]
     Device:   Gensou-chan Hypermancy Mk.5 (EA100) (ID=0x0a37)
     Vendor:   Gensou-chan MakaiTech
     RAM:      131072 MB
     Driver:   4.0.99999.9999
```

# MORERO
MORERO is the main cracking group for YumeDance stuff. They mainly focus on R-18 and R-18G things but they still release a lot of General rated programs.

- DRM FREE means the program does not have any DRM. Most often seen by free and open source programs.

## Example
Example release post, trying to go for a game crack .nfo aesthetic.

```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「OWKC 2020 (c) OWKC Holdings Inc.」
=========================================================
「REPACK DATE: 02.4.21				LANGUAGE:	MULTi33」
「PROGRAM VER: 100a  				   DLC'S:	    ALL」
「   	GENRE: RACING		          RATING:	GENERAL」
「   CRACK BY: Hoshi		 	 REPACK SIZE:	 7.96GB」
「   	NOTES: .		  		  FINAL SIZE:	16.12GB」
「   		orngw://yumedance.jp/soft/VA43120/		   」
「   		orngw://owkc.com/game/owkc2020/		   」
「   MULTIPLAYER WORKING, USE YOUR YUMEDANCE ACCOUNT   」
======================DESCRIPTION========================
「Experience OWKC like no other. With the full 2020 season calendar with 24 tracks」
「, you can recreate Open Wheel Kart Championship battles, with spectacular battles and collisions.」
「Hyperrealistic driving physics make you feel like you're driving your own OWKC car」
「at over 260mph as you feel the wind push against you as you fight the vehicle's 1500BHP.」
=======================EXECUTION=========================
「TIME TIL DREAM:                                     」
「    - NO ENABLER: 5-7 MINUTES                       」
「    - MABOURU BASIC: 40-65 SECONDS                  」
「    - MABOURU GOLD: 18-30 SECONDS                   」
「    - MABOURU GOLD + PHYSlink: <1 SECOND            」
「      LARGE FILE, ENABLER STRONGLY RECOMMENDED      」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「IF YOU HAVE DIFFICULTIES LOADING THE FILE, USE PHYSlink USB-C CONNECTION」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
=======================GROUP INFO========================
「We are a cracking group for Lucid Dream programs offering you」
「clean rips while also saving you bandwidth and storage.」
「We repack any type of dream, from 0 to R-18G and between.」

「OMRKo・Hunt666・MPoops・Hoshi」

「For more fine cracked Lucid Dream programs visit:」
「orngw://morero.seihou」
=========================================================
==========LET'S LEAK!・漏れろ！・もれろ！・MORERO!===========
```


# Programs

## Games


### Strike Ops (c) Pipeworks Gaming Group
Real world references:
- Counter Strike: Global Offensive
- ArmA Reforger, ArmA 3
- Call of Duty MW2 (2009)
- Tom Clancy's Rainbow Six series
- H3VR
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Strike Ops (c) Pipeworks Gaming Group」
=========================================================
「REPACK DATE: 12.1.22				LANGUAGE:	MULTi33」
「PROGRAM VER: 1.24.2				   DLC'S:	    ALL」
「   	GENRE: FPS		              RATING:	    15+」
「   CRACK BY: AniMax		 	 REPACK SIZE:	18.64GB」
「   	NOTES: .		  		  FINAL SIZE:	29.31GB」
「   		orngw://yumedance.jp/soft/VA51600/		   」
「   		orngw://pipeworks.io/strikeops-yd/		   」
「   MULTIPLAYER WORKING, USE YOUR YUMEDANCE ACCOUNT   」
======================DESCRIPTION========================
「Strike Ops, the hit PCVR FPS hits YumeDance!」
「Feel every gunshot, every step, every hit you deal and take.」
「With tactical 5v5 gamemodes such as the E-Sport favorite Demotion or Gun Game」
「each and every gunfight will bring you to your brink.」
=======================EXECUTION=========================
「TIME TIL DREAM:                                     」
「    - NO ENABLER: 5-7 MINUTES                       」
「    - MABOURU BASIC: 40-65 SECONDS                  」
「    - MABOURU GOLD: 18-30 SECONDS                   」
「    - MABOURU GOLD + PHYSlink: <1 SECOND            」
「      LARGE FILE, ENABLER STRONGLY RECOMMENDED      」
「IF YOU HAVE DIFFICULTIES LOADING THE FILE, USE PHYSlink USB-C CONNECTION」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
```

#### Forum

> #2
>
> "Okay I just downloaded Strike Ops from the YD site. It's a really great time, other than that my heart's beating out of my chest. It seems to trigger my fight and flight response so hard.
I tried to use my magic powers but it just doesn't seem to work and I kept getting killed."

### PopuVille (c) Pipeworks Gaming Group
Real world references:
- Grand Theft Auto Online
- Mafia
- VRChat
- Second Life
- The Sims
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「PopuVille (c) Pipeworks Gaming Group」
=========================================================
「REPACK DATE: 07.2.22				LANGUAGE:	MULTi33」
「PROGRAM VER: 1.39 				   DLC'S:	    ALL」
「   	GENRE: SIMULATION		      RATING:	    15+」
「   CRACK BY: Hunt666		 	 REPACK SIZE:	48.01GB」
「   	NOTES: .		  		  FINAL SIZE:  119.38GB」
「   		orngw://yumedance.jp/soft/VA2970/		   」
「   		orngw://pipeworks.io/popuville/		   」
「   MULTIPLAYER WORKING, USE YOUR YUMEDANCE ACCOUNT   」
======================DESCRIPTION========================
「A premier life simulation brought you from the devs of Strike Ops.」
「Be anyone you want. Be the law, or fight the law.」
「Explore the city of PopuVille, with over 270 km2 of area to play」
「with, complete with licensed brands like Kiera, EFun, Franklin, and Gensou-chan.」
=======================EXECUTION=========================
「TIME TIL DREAM:                                     」
「    - NO ENABLER: 9-15 MINUTES                      」
「    - MABOURU BASIC: 1-3 MINUTES                    」
「    - MABOURU GOLD: 27-90 SECONDS                   」
「    - MABOURU GOLD + PHYSlink: 2-6 SECONDS          」
「      LARGE FILE, ENABLER STRONGLY RECOMMENDED      」
「IF YOU HAVE DIFFICULTIES LOADING THE FILE, USE PHYSlink USB-C CONNECTION」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
```

### OWKC 2020 (c) OWKC Holdings Inc.
Real world equivalents:
- Formula 1 CodeMasters games
- EA NASCAR games

```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「OWKC 2020 (c) OWKC Holdings Inc.」
=========================================================
「REPACK DATE: 02.4.21				LANGUAGE:	MULTi20」
「PROGRAM VER: 100a  				   DLC'S:	    ALL」
「   	GENRE: RACING		          RATING:	GENERAL」
「   CRACK BY: Hoshi		 	 REPACK SIZE:	 7.96GB」
「   	NOTES: .		  		  FINAL SIZE:	16.12GB」
「   		orngw://yumedance.jp/soft/VA43120/		   」
「   		orngw://owkc.com/game/owkc2020/		   」
「   MULTIPLAYER WORKING, USE YOUR YUMEDANCE ACCOUNT   」
======================DESCRIPTION========================
「Experience OWKC like no other. With the full 2020 season calendar with 24 tracks」
「, you can recreate Open Wheel Kart Championship battles, with spectacular battles and collisions.」
「Hyperrealistic driving physics make you feel like you're driving your own OWKC car」
「at over 260mph as you feel the wind push against you as you fight the vehicle's 1500BHP.」
=======================EXECUTION=========================
「TIME TIL DREAM:                                     」
「    - NO ENABLER: 5-7 MINUTES                       」
「    - MABOURU BASIC: 40-65 SECONDS                  」
「    - MABOURU GOLD: 18-30 SECONDS                   」
「    - MABOURU GOLD + PHYSlink: <1 SECOND            」
「      LARGE FILE, ENABLER STRONGLY RECOMMENDED      」
「IF YOU HAVE DIFFICULTIES LOADING THE FILE, USE PHYSlink USB-C CONNECTION」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
```

### Auto Rapido 2 (c) Mercia Lang GmbH
Real world equivalents:
- IRacing
- Assetto Corse
- BeamNG.drive

```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Auto Rapido 2 (c) Mercia Lang GmbH」
=========================================================
「REPACK DATE: 29.1.21				LANGUAGE:	MULTi16」
「PROGRAM VER: 3.2.2  				   DLC'S:	    ALL」
「   	GENRE: RACING		          RATING:	GENERAL」
「   CRACK BY: Hunt666		 	 REPACK SIZE:	14.33GB」
「   	NOTES: .		  		  FINAL SIZE:	22.55GB」
「   		orngw://yumedance.jp/soft/VA22620/		   」
「   MULTIPLAYER WORKING, USE YOUR YUMEDANCE ACCOUNT   」
======================DESCRIPTION========================
「Auto Rapido 2 is the sequel to the well loved Auto Rapio, developed with YumeDance in mind.」

「With 2000hz soft body simulation, cars feels visceral, yet realistic and easy to drive. Every bump and skid is super noticeable.」
「Even crashing your car feels like the real thing, just without the injury.」
「Race against super competitive AI trained by the greatest drivers in motorsport, or play with your」
「friends in multiplayer, or compete online in ranked races to see who's the best.」

「Take a drive in one of the game's crusing maps and chill.」
「Or crash your car into walls and watch the parts fly. We don't care.」
=======================EXECUTION=========================
「TIME TIL DREAM:                                     」
「    - NO ENABLER: 8-11 MINUTES                       」
「    - MABOURU BASIC: 40-65 SECONDS                  」
「    - MABOURU GOLD: 18-30 SECONDS                   」
「    - MABOURU GOLD + PHYSlink: <1 SECOND            」
「      LARGE FILE, ENABLER STRONGLY RECOMMENDED      」
「IF YOU HAVE DIFFICULTIES LOADING THE FILE, USE PHYSlink USB-C CONNECTION」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
```


## H Games
Erotic or fetish games, aka「eroge」. Adults only!!!

### 幻想デルルオナニー (c) ZeccHou Soft Co. Ltd.
Think of these games mixed:
- Custom Maid 3D2
- Megami Tensei
- Any one of many VR sex simulators
- Garry's Mod
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Gensou Deruru Onani (c) ZeccHou Soft Co. Ltd.」
=========================================================
「REPACK DATE: 14.4.22				LANGUAGE:    MULTi4」
「PROGRAM VER: 2022.4.12 		       DLC'S:	    ALL」
「   	GENRE: SIMULATION       	 RATING:	   R-18」
「   CRACK BY: OMRKo    		 REPACK SIZE:	11.32GB」
「   	NOTES: .		  		  FINAL SIZE:	26.99GB」
「             HAPPY VALENTINES DAY 2022!              」
「     REDOWNLOAD IF YOU HAVE AND OLD GAME VERSION     」
「   		orngw://yumedance.jp/soft/VA620/		   」
「               JP Title: 幻想デルルオナニー             」
======================DESCRIPTION========================
「Do anything to any character you want in the land of Gensokyo in Gensou Deruru Onani (GDO).」
「We have representations of characters such as Hakurei Reimu, Yakumo Yukari, Izayoi Sakuya, and even updated for characters like Kudamaki Tsukasa.」
「Engage in lovey dovey sex, or go hard to get and train up your real world combat skills by fighting them.」
「We have replicated Gensokyo's Youjutsu system in GDO, so go crazy trying out spells.」
「GDO's a platform made for complete expandability and customization, with full script and asset mod support.」
=======================EXECUTION=========================
「TIME TIL DREAM:                                     」
「    - NO ENABLER: 8-11 MINUTES                      」
「    - MABOURU BASIC: 40-65 SECONDS                  」
「    - MABOURU GOLD: 17-36 SECONDS                   」
「    - MABOURU GOLD + PHYSlink: 1-3 SECONDS          」
「      LARGE FILE, ENABLER STRONGLY RECOMMENDED      」
「IF YOU HAVE DIFFICULTIES LOADING THE FILE, USE PHYSlink USB-C CONNECTION」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
```

#### Forum

> #2
>
> "Big props for shoutting out GDO. Really great game for learning about the fighters here and how to beat them. I don't really do the H elements, just a lot of fighting."

#### Boot
```
Welcome to Gensou Deruru Onani v2022.4.12
(c) ZeccHou Soft Co. Ltd 2018-2022 All Rights Reserved
COMMERCIAL SOFTWARE. DO NOT REDISTRIBUTE

Initialize engine version: 2022.3.05 (6a3d17)
Saving log on PostTome dir: /home/sdm/.config/zecchou-gdo/log/2023101-1200.log
MabClient: creating device client threaded=1 jobified=1
MabAPI:
	 Version:  MabAPI 2.2 [PHYSlink Active]
     Device:   MaBouru Gold (CROTE) (ID=0x00ba)
     Vendor:   MaBouru Youjutsu Enablers, LLC.
     RAM:      16384 MB
     Driver:   4.0.99999.9999

Logging into YumeDance via biometrics
Pinging servers:
Closest server: orngw://tokyo.host.yumedance.jp
Welcome reiuji.utsuho.37! Downloading saves from cloud backup.
Downloaded saves to /tmp/yumedance-save/37/VA620/

Loading Mods
Loaded(-100) jp.zecchou.gensouderuruonani - Gensou Deruru Onani 2022.4.12
Loaded(0) seihou.morero.pamperemporium - [PE] Pamper Emporium 15.03.22
Loaded(1) sktr.nukime.ttt - [PE] Toyohime's Torture Trainer v1.2
Loaded(2) jp.yumedance.blacklamps.easy-scenario-quickstart - Easy Scenario Quickstart 2021.2.13
Loaded(3) gsk.scarletbank.sdmtool - PostTome Library Tools Build 112
Loaded(4) mods.expire6442.gdo.strykr - EFun Strykr Wand Vibrator for GDO 1.0
Loaded(5) mods.expire6442.gdo.efnegotator - EFun Negotiator Shock Wand for GDO 1.0
Initialization finished in 6.21 seconds

[PE] Pamper Emporium 15.03.22 - Welcome to Niaobu-sama's Fan Club
[Easy Quickstart] Starting Scenario Toyohime's Torture Trainer from [PE] Toyohime's Torture Trainer

Loading save data /tmp/yumedance-save/37/VA620/ttt-auto.sav
Loading map /home/sdm/Games/Gensou Deruru Onani/mods/TTT v1.2/scenario/toyo-sub-torture.gdoscene
Spawned entity Utsuho Reiuji
Assuming control of entity Utsuho Reiuji to the player
Spawned entity Toyohime Watatsuki
Removing clothes from Utsuho Reiuji
[PE] Force equipping Gensou-chan "FantastaBab" thick printed diaper to entity Utsuho Reiuji
Level loaded in 2.65 seconds
[MabAPI] Injecting level into user's mind.
```

### オムマンの扱い方 (c) Unimu Incontinence Products
Sandbox dressing room game focused on Unimu's diapers

Description is meant to have that MTL feel.
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Omuman no Atsukai Kata (c) Unimu Incontinence Products」
=========================================================
「REPACK DATE: 01.3.21				LANGUAGE:  JAPANESE」
「PROGRAM VER: 566.553 				   DLC'S:	    N/A」
「   	GENRE: SANDBOX       		  RATING:	  R-18G」
「   CRACK BY: DRM FREE    		  REPACK SIZE:	 1.23GB」
「   	NOTES: .		  		  FINAL SIZE:	 4.35GB」
「        orngw://unimu.jp/program/atsukaikata/        」
「               JP Title: オムマンの扱い方               」
「MORERO forum guys been waiting for this one for a while.」
「Be glad this doesn't call any of the bladder releasing functions unlike the GDO mods.」
「Description is MTLed using Planck Translate, game is in Japanese.」
======================DESCRIPTION========================
「Enjoy Unimu's Omuman diapers with this lovely program. The new evolution of diaper samples.」
「Learn how to put on diapers, wipe wetness and mess, change diapers, and potty training.」
「You can even do omorashi in them, pee and poop and feel the mess stain them.」
「Will you enjoy the cute panty diaper Panman, the robust tape type diaper Tapeman, or try toilet training with Torepanman.」
「Need more protection? Try out our OmumanTai diapers complete with boosters and soak in the crinkling bulk.」
「Even our suppliments like the Fukinai rash cream or Kusanai baby powder are implemented.」
=======================EXECUTION=========================
「TIME TIL DREAM: 12-25 SECONDS」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR THE YUMEDANCE JINGLE AND PROMPTLY FALL ASLEEP.」
```

#### Forum

> #2
>
> >be Unimu
> >tease a diaper showcase program for YumeDance
> >main intention is to allow you to sample diapers before buying them, and how to put on and change diapers.
> >there's an omorashi feature in the trailer.
> >omo fans and abdls rejoice
> >they beg unimu to release it for like a couple of months.
> >unimu actually releases the fucking thing.
> >R-18G warning when opening the program (it's gonna be spicy).
> >it has it and even has leaks and blowouts.
> ABOSOLUTE UNIMU VICTORY

> #3
>
> They released it!!! Free and fully uncensored too!!! I see full ass genitals and brown poop when opening poopy pamps. YAYYYY. No Gensou-chan stuff though sadly. I loved the FantastaBab's prints. Can someone go and port the assets from here and make them compatible with GDO's PE?

> #4
>
> They really did not have to go full ABDL mode with this one. But they did. I fucking love Unimu now.
> Normies are going to see this and think why is their "interractive diaper brochure" fetishized to hell but eh that's what makes it so good.
> Omutsu-sama's eating good with this one holy.

> #5
>
> Yayyyy! I love the Unimus but I don't have the money to keep buying cases of TapemanTai with boosters. This is a great way to get my diaper fix without the real world mess or the cost.

> #6
>
> Can we get an English translation?



### Excretion Youjutsu Training Program (c) Gensou-chan MakaiTech
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Excretion Youjutsu Training Program (c) Gensou-chan MakaiTech」
=========================================================
「REPACK DATE: 25.4.22				LANGUAGE:    MULTi3」
「PROGRAM VER: 2022.3.31 			   DLC'S:	    N/A」
「   	GENRE: SLG, TRAINING          RATING:	  R-18G」
「   CRACK BY: OMRKo    		 REPACK SIZE:	 3.89GB」
「   	NOTES: .		  		  FINAL SIZE:	 2.12GB」
「                 MERRY CHRISTMAS 2022!               」
「         USES `HOUNYOU` and `HOUBEN` FUNCTIONS       」
「   Your pants will most likely end up wet or messy!  」
「 Thanks from tested3936 for providing us the files!  」
======================DESCRIPTION========================
「tested3936 calls this like that one "Don't Shit Your Pants" flash game.」
「"Move your character who needs to go potty badly to the toilet.".」
「"You have text commands that you use to control your character.".」
「"It's really weird since you're basically controlling someone else using your tools".」
=======================EXECUTION=========================
「TIME TIL DREAM: 9-17 SECONDS」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR THE YUMEDANCE JINGLE AND PROMPTLY FALL ASLEEP.」
```

#### Forum
> #2
>
> "UOOOOHHHHH MOMMY SHINKI."

> #3
>
> "I finished the game onces but I didn't get my Youjutsu. Do I have to play it again?."

> #4
>
> "You have to go and collect the endings that you can get during a run. You can check what endings you have gotten in that scenario for by starting the program, and going into the menu after doing your first run. There's 33 endings in total throughout the 3 scenarios, you only need 16 in total. First and second scenario has 12, third one has 8."

> #5
>
> "Spoilers for the third scenario. Holy shit. I feel like I've got such as fucking power trip since the third scenario has you in a crib with pretty much all of the magic you want to cast, so you can cast literally fucking anything. I just casted Megido on some adult baby and she just fucking died lol."


## Mods for 幻想デルルオナニー
### [PE] Pamper Emporium (c) MPoops@MORERO
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「[PE] Pamper Emporium (c) MPoops@MORERO」
=========================================================
「REPACK DATE: 15.3.22				LANGUAGE:	ENGLISH」
「PROGRAM VER: 15.3.22				   DLC'S:	    N/A」
「   	GENRE: MOD		  	          RATING:	  R-18G」
「   CRACK BY: DRM FREE		 	 REPACK SIZE:	  773MB」
「   	NOTES: .		  		  FINAL SIZE:	 1.36GB」
「   		   orngw://morero.seihou/pe/   		       」
「orngw://gitland.morero.seihou/mpoops/pamper-emporium 」
「              MORERO OFFICIAL CREATION               」
=======================DESCRIPTION=======================
「Welcome to Pamper Emporium, an omorashi and diaper lover's dream for GDO.」
「While GDO has a basic urination system involving diuretics, we were severely underwealmed with the omo fetish stuff and the lack of diapers.」

「Pamper Emporium addes a full pee and poo need system with the ability to go potty anywhere.」
「You can go potty in toilets, potty chairs, outside, even on other people and on food and cups.」
「If you don't make it in time, you'll end up soiling your clothes with wetness and mess, and you'll be known as a piddle pants.」

「Such piddle pants enjoyers can also wrap themselves in the many diapers we have, including classic tape-ons, discreet pull-ups, reusable cloth diapers,」
「as well as diaper covers, rompers, and absorbency bosoting pads such as diaper boosters and inner diapers.」
「We have diapers from many companies such as Gensou-chan, Unimu, LastLeak, and more.」
「Have little troubles with your pee? There's also pads for underwear to deal with these little leaks.」
「Gain continence as you make it to the toilet. Lose continence as you repeatibly use your diapers and eventually become incontinent.」

「Want to add your own diapers or improve on this mod? Go crazy! We released the source code for anyone to fork and make changes on.」
「Thanks for Unimu and Gensou-chan for giving their assets to us!」
=======================EXECUTION========================
「THIS IS A MOD FOR GENSOU DERURU ONANI. GDO 2022.3.01 OR LATER IS REQUIRED」
「1....: EXTRACT TO YOUR GDO `mods` DIRECTORY」
「2....: RUN GDO AND MAKE SURE THE MOD IS ENABLED」
```

### [PE] Jiko Aftermath (c) NukimeSKTR
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「[PE] Jiko Aftermath (c) NukimeSKTR」
=========================================================
「REPACK DATE: 06.2.22				LANGUAGE:    MULTi4」
「PROGRAM VER: 1.2.7 		           DLC'S:	    N/A」
「   	GENRE: MOD OF MODS     	      RATING:	  R-18G」
「   CRACK BY: OMRKo    		 REPACK SIZE:	  886MB」
「   	NOTES: .		  		  FINAL SIZE:	 1.86GB」
「   		orngw://yumedance.jp/soft/IA31390/		   」
「         USES `HOUNYOU` and `HOUBEN` FUNCTIONS       」
「   Your pants will most likely end up wet or messy!  」
======================DESCRIPTION========================
「There's a lot of H programs where you're trying to not have an accident...」
「But not one where you deal with the consequences of one.」
「Jiko Aftermarth drops you into one of many unfortunate situations where you didn't make it」
「and your objective is to clean yourself up. Using one of many ways to do so, can you」
「keep your dignity intact, or will you end up laughed at and put into diapers.」
=======================EXECUTION=========================
「THIS IS A MOD FOR GENSOU DERURU ONANI. GDO 2022.1.15 OR LATER IS REQUIRED」
「PAMPER EMPORIUM 2021.4.29 OR LATER IS REQUIRED」
「1....: EXTRACT TO YOUR GDO `mods` DIRECTORY」
「2....: RUN GDO AND MAKE SURE THE MOD IS ENABLED」
```

### Toyohime's Torture Trainer (c) NukimeSKTR
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Toyohime's Torture Trainer (c) NukimeSKTR」
=========================================================
「REPACK DATE: 15.3.21				LANGUAGE:	ENGLISH」
「PROGRAM VER: 2.1.2				   DLC'S:	    N/A」
「   	GENRE: MOD		  	          RATING:	   R-18」
「   CRACK BY: OMRKo		 	 REPACK SIZE:	  564MB」
「   	NOTES: .		  		  FINAL SIZE:	  915MB」
「   		orngw://yumedance.jp/soft/IA16800/		   」
======================DESCRIPTION========================
「eraReverse style training. You're the one being trained, but can you call your own Intervention?」
「Toyohime has you bound to a cross and you're stuck with her torturing you for fun.」
「While it may seem hopeless, you have one saving grace: You willpower.」
「Resist her advances to gain willpower, and when you have enough, you can call for Intervention.」
=======================EXECUTION========================
「THIS IS A MOD FOR GENSOU DERURU ONANI. GDO 2021.3.05 OR LATER IS REQUIRED」
「1....: EXTRACT TO YOUR GDO `mods` DIRECTORY」
「2....: RUN GDO AND MAKE SURE THE MOD IS ENABLED」
「2....: THIS IS A SCENARIO MOD. SCENARIOS CAN BE LAUNCHED VIA THE SCENARIOS TAB.」
```

### Broughton M602 Assault Rifle Series for GDO (c) expire6442
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Broughton M602 Assault Rifle Series for GDO (c) expire6442」
=========================================================
「REPACK DATE: 15.3.21				LANGUAGE:	ENGLISH」
「PROGRAM VER: 1.0				      DLC'S:	    N/A」
「   	GENRE: MOD		  	          RATING:	    12+」
「   CRACK BY: DRM FREE		 	 REPACK SIZE:	  773MB」
「   	NOTES: .		  		  FINAL SIZE:	 1.36GB」
「   		orngw://expire6442.mods/gdo/m600/		   」
======================DESCRIPTION========================
「Introducing the Broughton Model 602 US service rifle onto GDO.」
「This mod adds the M602 and many variants such as the M920 and M921 carbines, the S602 semi-automatic rifle,」
「the M231 Firing Port Weapon, the super short M609 carbine, the Averdeen ALS 75 light support weapon with it's 100-round drum, and more」
「The M602 is a fully-automatic assault rifle chambered in 5.56x45mm NATO firing at 700rpm and has a 30-round magazine.」
「True to life mechanisms such as the recipricating bolt, safety selector, T-pull bolt, trigger calibrated to the same sensitivity as the real unit.」
「Weapons can be bought from traders or spawned via the spawn menu in Free H」
=======================EXECUTION========================
「THIS IS A MOD FOR GENSOU DERURU ONANI. GDO 2019.2.18 OR LATER IS REQUIRED」
「1....: EXTRACT TO YOUR GDO `mods` DIRECTORY」
「2....: RUN GDO AND MAKE SURE THE MOD IS ENABLED」
```

### [DWR] Danmaku World Recollection (c) danmaku.world
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「[DWR] Danmaku World Recollection (c) danmaku.world」
=========================================================
「REPACK DATE: 26.4.22				LANGUAGE:	ENGLISH」
「PROGRAM VER: 2.1.2				   DLC'S:	    N/A」
「   	GENRE: MOD		  	          RATING:	    N/A」
「   CRACK BY: DRM FREE		 	 REPACK SIZE:	 9.43GB」
「   	NOTES: .		  		  FINAL SIZE:	18.35GB」
「   	orngw://danmaku.world/recollection-mod/		   」
======================DESCRIPTION========================
「Train your way to become a better fighter using this modpack for GDO 2022.04.12.」
「Every mod has been tested for mod conflicts and conigured to fully replicate the real-life Danmaku World experience.」
「Included are many gun mods full of the weapons that much of our Danmaku World combatants use and more.」
「Mods Included:」
「- Broughton M602 Assault Rifle Series for GDO (c) expire6442」
「- Gryzov Assault Rifle Series for GDO (c) expire6442」
「- Tricorne CCW Pistol Series for GDO (c) expire6442」
「- ArmTeck SPA Assault Rifle for GDO (c) expire6442」
「- LUNINCO LAC1 Laser Rifle for GDO (c) expire6442」
「- LUNINCO LAC2 Laser Pistol for GDO (c) expire6442」
「- LUNINCO LAC9 Laser Shotgun for GDO (c) expire6442」
「- Haru Type 13 Rifle for GDO (c) expire6442」
「- Haru Type 99 Imperial Rifle for GDO (c) expire6442」
「- LUNINCO LAC33 Rifle Series for GDO (c) expire6442」
「- Gensou-chan's Official Armory (c) Gensou-chan MakaiTech」
「- Keiga Youjyuu Magic Guns for GDO (c) expire6442」
「- Renov PG and Rika's Arms Ares Machine Guns for GDO (c) expire6442」
「- Brennan LRS Anti-Material Rifle for GDO (c) expire6442」
「- Akatsuki -hiken Musket Series for GDO (c) expire6442」
「- [PE] Pamper Emporium (c) MPoops@MORERO」
=======================EXECUTION========================
「THIS IS A MOD PACK FOR GENSOU DERURU ONANI. GDO 2022.04.12 OR LATER IS REQUIRED」
「DISABLE ALL MODS AND BACK THEM UP TO A NEW DIRECTORY BEFORE INSTALLING」
「1....: EXTRACT THE MOD PACK TO YOUR GDO `mods` DIRECTORY」
「2....: RUN GDO AND MAKE SURE THE MODS ARE ENABLED」
```

## Other Shit

### iNgenunity AIX Showcase (c) iNgenunity Technologies
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「iNgenunity AIX Showcase (c) iNgenunity Technologies」
=========================================================
「REPACK DATE: 16.3.19				LANGUAGE:	MULTi33」
「PROGRAM VER: 1.00 				   DLC'S:	    N/A」
「   	GENRE: DEMO		              RATING:	    12+」
「   CRACK BY: DRM FREE    		 REPACK SIZE:	 3.56GB」
「   	NOTES: .		  		  FINAL SIZE:	 5.57GB」
「orngw://ingenunity.com/blog/2019-3-15-aix-showcase-yd/」
「Free download, just sharing if you're on Gensokyo or Lunar Capital」
「and if Planck internet decides to block the iNgenunity website.」
======================DESCRIPTION========================
「iNgenunity presents all new AIX graphical processing cards for ray-tracing and AI」
「purposes. Explore 3D like nothing else, worlds that seem unreal, and lighting th-」
「-at feels 10 years ahead of anyone else.」

「Experience our top of the line cards like the 900 AIX 24GB, or 850 AIX 24GB bring」
「a new era of gaming, or go for something more modest like the 700 AIX 10GB, the gamer」
「ready 600 AIX 8GB with 1.5x the performance of the previous generation GPU, the NGP 660 6GB.」
「Or try out the compact 500 AIX 6GB that can easilly fit in a low profile system.」

「Demos included are War Master 2230, Crime3D AIX, and OWKC 2020.」
=======================EXECUTION=========================
「TIME TIL DREAM: 30-45 SECONDS」
「YumeDance V1 FILE! ENABLER REQUIRED!!」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR THE YUMEDANCE JINGLE AND PROMPTLY FALL ASLEEP.」
```

### Virtual Office 2023 (c) International Technology Co.
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Virtual Office 2023 (c) International Technology Co.」
=========================================================
「REPACK DATE: 15.2.22				LANGUAGE:	MULTi64」
「PROGRAM VER: 22H1 				   DLC'S:	    N/A」
「   	GENRE: OFFICE       		  RATING:	GENERAL」
「   CRACK BY: MPoops    		 REPACK SIZE:	 3.56GB」
「   	NOTES: .		  		  FINAL SIZE:	 5.57GB」
「  orngw://itc.com/product/virt-office-2023-edition/  」
======================DESCRIPTION========================
「Virtual Office brings your office to the dream world with the power of YumeDance.」
「Write documents, create charts, draw pictures, edit video using our vast suite of programs.」
「Included apps are Canvas (art program), Rollerball (writer), Stacker (spreadsheet maker),」
「Live Mix (video editor), Presenter (presentation maker)」
=======================EXECUTION=========================
「TIME TIL DREAM: 4-10 SECONDS」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR 「MORERO!」 AND PROMPTLY FALL ASLEEP.」
```

### Welcome to YumeDance (c) YumeDance Inc.
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「Welcome to YumeDance (c) YumeDance Inc.」
=========================================================
「REPACK DATE: 02.2.22				LANGUAGE:	MULTi17」
「PROGRAM VER: 22H1 				   DLC'S:	    N/A」
「   	GENRE: DEMO       	    	  RATING:	GENERAL」
「   CRACK BY: DRM FREE    		   REPACK SIZE:	   63MB」
「   	NOTES: .		  		 FINAL SIZE:	  235MB」
「  orngw://yumedance.jp/firmware/howto/  」
======================DESCRIPTION========================
「Welcome to YumeDance!」
「This is a short little program that teaches people how YumeDance works, and how to get new」
「programs with the YumeDance store and to load them onto their PostTome.」
「Also included is a short demo that displays everything YumeDance does over conventional entertainment」
=======================EXECUTION=========================
「TIME TIL DREAM: <1 SECOND」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR THE YUMEDANCE JINGLE AND PROMPTLY FALL ASLEEP.」
```

### The【Agi】Book (c) MaBouru Youjutsu Enablers LLC.
```
====================MORERO PRESENTS======================
===========ANOTHER AMAZING LUCID DREAM PROGRAM===========
「The【Agi】Book (c) MaBouru Youjutsu Enablers LLC.」
=========================================================
「REPACK DATE: 02.2.22				LANGUAGE:	 MULTi7」
「PROGRAM VER: master-d43f9a 		   DLC'S:	    N/A」
「   	GENRE: TRAINING       	      RATING:	GENERAL」
「   CRACK BY: DRM FREE    		 REPACK SIZE:	 1.12GB」
「   	NOTES: .		  		  FINAL SIZE:	 2.35GB」
「        orngw://git.mabouru.gsk/learning/agi/        」
======================DESCRIPTION========================
「The Agi book teaches new users of MaBouru how to cast fire magic safely, and efficiently.」
「Don't want to burn your house down? Taking the time to use this program as a learning resource」
「will teach you how to cast, when to cast, and where not to cast it, and how to improve at magic.」
「It also allows you to try out more advanced spells within the comfort of a lucid space.」
=======================EXECUTION=========================
「TIME TIL DREAM: 2-6 SECONDS」
「Uses YumeDance DreamSIM, NO ENABLER NEEDED」
「1....: PLACE FINGER ON THE POSTTOME'S READER. FILES WILL BE STREAMED TO YOUR MIND.」
「2....: IF EXECUTED PROPERLY YOU SHOULD HEAR THE YUMEDANCE JINGLE AND PROMPTLY FALL ASLEEP.」
```

Other stuff:
- The【Bufu】Book: Ice magic
- The【Zio】Book: Electricity magic
- The【Dia】Book: Healing magic
- The【-kaja】Book: Buffing magic
- The【-nda】Book: Debuff magic