# Tracking Donkhouse

Full-stack project which serves as a tracker (player nets, stats, etc.) of Yale poker online games; currently publicly deployed.

First uses Python Selenium (download_files.py) and Github Actions to run a scheduled script which navigates to donkhouse.com (home of YPC 
online server) and automatically downloads new ledgers and hand histories. It loops through every NLH table and automatically clicks on the desired files through the 
provided coordinates. 

This script fills an artifact directory called "logs" with pairs of files representing the ledger and hand history log for each game parsed. These pairs of files are then 
fed into parse_downloads.py as command line arguments, which connects to our MySQL database. We use Python OOP and regex to identify when certain phenomenons are occuring 
when parsing the hand history script. This script eventually updates our database with the games and stats from the new 3 hour block (stats inlcuding VPIP, PFR, 3-bet %,
4-bet %, Fold to 3-bet %, C-bet %, Donk-bet on Flop %, Limp Freq). Further, this parser stores each game through a game table, which contains information on which 
players played in a given game and what their game-specific nets were. This is accomplished through a many-to-many relationship, which automatically fills a PlayerGame
association table as a game gets inserted into the table. Our database schema can be viewed in schema.py.

We then use React.js with a Node backend to develop and deploy our website, so all Yale Poker club members can visualize what's happening in the online games (or any curious 
onlookers). Check it out by clicking the link below!

[TrackingDonkhouse](www.trackingdonkhouse.com)
