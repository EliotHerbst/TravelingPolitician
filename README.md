# TravelingPolitician
A politician hopes to become the president of the United States. Their campaign starts with the presidential primaries in the capital of Iowa. The politician then wants to visit the capital of every U.S. state to campaign before ending in the White House in the nation’s capital of Washington, D.C. The politician does not want to visit any capital more than once. They would like to campaign in every capital one and only once. To be efficient and save on time and money, they would like to do this in as short a path as possible. The Traveling Politician Problem aims to find this shortest path. The map can be thought of as a graph with 51 points (the capitals of all 50 U.S. states, plus Washington, D.C.) and a set of distances between each of them. The starting point and ending point are already set (the capital of Iowa and Washington, D.C., respectively). This leaves 49 points to be visited in between the starting and ending points, this does not include the start and end points.

This problem is much harder than it may sound. The main solution to the problem is factorial time—that is, the time it takes to solve will be proportional to 49!. It is not 51! because the starting and ending cities are already set. After starting in Iowa, one of the 49 remaining capitals can be chosen as the first one to travel to. Now that one of the 49 has been chosen as the first, one of the remaining 48 capitals can be chosen as the second to travel to. Now there are 47 remaining capitals to choose as the third, and so on. The total number of paths to be compared will be 49\*48\*47\* … \*3\*2\*1, which is 49! (49 factorial). This evaluates to around 6\*10^62 different total paths to be compared. That’s around a trillion trillion trillion trillion trillion. 

This problem is based on the “Traveling Salesman Problem”, which is a well-known graph theory problem that has been heavily studied by mathematicians. Many resources are available to study this problem under the title “Traveling Salesman Problem”.

https://en.wikipedia.org/wiki/Travelling_salesman_problem

## Getting Started 

### Prerequisites

In order to run this file you must have selenium and geopy installed. This can be done via the command

```
pip install selenium
pip install geopy
```

In a conda environment selenium can be installed with
```
conda install -c conda-forge --name myenv selenium 
conda install -c conda-forge geopy
```

### Installing chromedriver 

Depending on your environment you may have to change the chromedriver.exe file. If you already have a chromedriver installed, you can delete this file and set path_to_chromedriver in TravelingPolitician.py equal to the file path for your chromedriver ie:
```
path_to_chromedriver = "Your FilePath Here"
```

#### Windows
The chromedriver.exe file currently in the project is compatible with Windows Systems

#### Linux and Mac

Download the correct chromedriver binaries for your system here: https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/ then extract the chromedriver file and replace chromedriver.exe with it.

In the TravelingPolitician.py file you must change file_path to

```
file_path = os.path.join(this_dir, 'chromedriver')
```

### Running

#### Windows
Open the command line (cmd) and enter the following command
```
py YOURFILELOCATION/TravelingPolitician.py YOURJSONINPUTLOCATION YOURDESIREDOUTPUTLOCATION
```
#### Linux and Mac
Run the following command from terminal
```
python3 YOURFILELOCATION/TravelingPolitician.py YOURJSONINPUTLOCATION YOURDESIREDOUTPUTLOCATION
```
If you are using linux and you would like to avoid explicity calling the interpreter you can add #!/usr/bin/env python as the first line of TravelingPolitician.py and enter the following command
```
chmod +x YOURFILELOCATION.py
```
It can then be run as
```
./YOURFILELOCATION.py YOURJSONINPUTLOCATION YOURDESIREDOUTPUTLOCATION
```

Take care when specifying the desired output location as if a file already exists in that location it will be overwritten.

The JSON input should be formatted as follows
```
{
  "start": "Starting State",
  "middle": "Middle States Seperated by a Comma",
  "end" :  "Ending States"
}
```
The JSON output will be in the following form
```
{
    "Total Distance": Total Distance as a numeric value,
    "Path": "The Path from start to finish with each state seperated by a ->"
}
```

If you would like to see the google searches being performed, you can remove the following three lines in the TravelingPolitician.py file (Some environments will not support this)

```
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
```

### Authors 
* **Eliot Herbst** - *TravelingPolitician.py* - https://github.com/EliotHerbst
* **Verbus Counts** - https://github.com/verbus
