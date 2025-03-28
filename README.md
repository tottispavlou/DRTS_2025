# DRTS simulator

This readme file briefly describes how to run the DRTS simulator implementing RTA and VSS

## Running VSS

The Very Simple Simulator takes a csv test file as well as the simulation time (basically how many times the time is advanced) as input. In the subfolder _Exercise_, three csv files that can be used are located. If we want to run the simulator with _TC3_, and a simulation time of 1000, the following command can be used:

`python VSS.py "Exercise/exercise-TC3.csv" 1000`

## Running RTA

The Response Time Analysis simulator is run the same way as the VSS simulator, although the simulation time is not included. Thus the same command would look like this:

`python RTA.py "Exercise/exercise-TC3.csv"`
