import os
from time import time, strftime
from datetime import datetime

start_time = datetime.now()
print "start:", start_time.strftime("%Y-%m-%d %H:%M:%S")
os.system("python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4 --numGames 1000 --frameTime 0 --fixRandomSeed --q")
end_time = datetime.now()
print "done:", end_time.strftime("%Y-%m-%d %H:%M:%S")
print "time taken:",(end_time-start_time), "seconds"

