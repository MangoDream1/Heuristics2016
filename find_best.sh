# Save start time
echo "Start stage 1:" > find_best_time.txt
date >> find_best_time.txt

# Run all python commands

# Start off with 500 swap hill climbers with a noProgressLimit of 100
python3 run4.py -i 500 -n 100 &&

echo "Start stage 2:" >> find_best_time.txt
date >> find_best_time.txt

# Improve the best 100 with a noProgressLimit of 100
python3 run4.py -i 100 -p &&

echo "Start stage 3:" >> find_best_time.txt
date >> find_best_time.txt

# Improve 24 again but with nPl of 10000
python3 run4.py -i 24 -p -n 10000 &&

echo "Start stage 4:" >> find_best_time.txt
date >> find_best_time.txt

# Improve 8 again but with nPl of 100000
python3 run4.py -i 8 -p -n 100000 &&

echo "Start stage 5:" >> find_best_time.txt
date >> find_best_time.txt

# Improve with student optimization with nPl of 100000
python3 run4.py -i 4 -p -s -n 10000

# Save end time
echo "End time:" >> find_best_time.txt
date >> find_best_time.txt
