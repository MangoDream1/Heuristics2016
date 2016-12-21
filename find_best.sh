# Save start time
echo "Start time:" > find_best_time.txt
date >> find_best_time.txt

# Run all python commands
python3 run4.py -i 500 -n 100 && # Start off with 500 swap hill climbers with a noProgressLimit of 100
python3 run4.py -i 100 -p && # Improve the best 100 with a noProgressLimit of 100
python3 run4.py -i 12 -p -n 10000 && # Improve 12 again but with nPl of 10000
python3 run4.py -i 4 -p -n 100000 && # Improve 4 again but with nPl of 100000
python3 run4.py -i 4 -p -s -n 10000 # Improve with student optimizatioon with nPl of 100000

# Save end time
echo "End time:" >> find_best_time.txt
date >> find_best_time.txt
