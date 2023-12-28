Team Optimization
Final project for Discrete Math, Bachelors of Technology in Computer Science @ National Institute Of Technology, Karnataka (India's Top 10 Engineering)

By Kaushikq Ravindran.

## The Project

Developed an algorithm for forming effective teams in academic settings, focusing on leveraging mathematical optimization to ensure balanced team dynamics. The goal was to enhance collaborative efficiency and project outcomes.

Our goal was to create an algorithm for making teams of students in a class. We wanted to make it easier to form teams that had favorable qualities for ensuring the team would work well together.

##Usage

Requires networkx for graph-based data representation and pandas for handling survey data. The project involves generating graph and clique data from student surveys and applying optimization algorithms for team formation.

The program requires joblib for file management, networkx for graph-based student representations, and pandas for processing CSV survey data. To use it, generate graph and clique data from student surveys, with options to use existing data in /data or create custom subsets. Running python data_loader.py prepares the data, where you select data sections (A, B, or C) and student counts. Execute the assignment algorithm with python main.py, inputting the data suffix and student count. The program offers both random and greedy assignment methods and evaluates the resulting teams.


### On your own survey data

TBD: Make it more user friendly to use this algorithm on your own survey results.

## Components
`assignments.py` - Algorithms that take in a list of students and produce a team assignment go here. \
`clique_finding.py` - The algorithm used to find k-cliques in a graph. \
`data_loader.py` - Imports data from survey results and converts it to Students. Also creates and saves graphs and cliques of students from that data. \
`helpers.py` - Miscellaneous methods that might be useful in multiple contexts, including some functions to evaluate certain metrics that are used for scoring. \
`main.py` - Loads graph and clique data that was previously generated from a sample of students and runs assignment algorithms using that data. \
`scoring.py` - Functions for scoring team assignments on different metrics go here. \
`student.py` - The Student class. \
`test.py` - Code to test helper functions. Currently just tests `overlaps`, but additional tests should go here.
