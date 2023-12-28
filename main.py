"""
Generates possible teams from saved student data.

- Loads a graph representing a class of students, as well as the list of 4- and 
  5-cliques in that graph.
- Scores the cliques using the compatibility function and sorts them.
- Computes how many teams of 4 and 5 must be made for the number of students in 
  the graph.
- Runs assignment functions from `assignments.py` on the cliques to create
  non-overlapping teams.
- Scores the overall team list and prints data about the individual teams 
  created.
"""
import joblib
from assignments import (
    assign_teams_greedy, assign_teams_random, assign_teams_rec)
from helpers import list_met_partner_prefs, num_size_teams, sorted_topics
from clique_finding import find_k_clique
from scoring import (
    assignment_cost, team_compatibility, team_evaluation)


sample_suffix = input(
    "Enter suffix for graph and cliques filenames (i.e., 'A20'): ")

# Load a graph of students
student_graph_filename = "data/student_graph_" + sample_suffix
try:
    # Try to load file specified by suffix
    student_graph = joblib.load(student_graph_filename)
    print("%i students loaded" % len(student_graph.nodes))
except FileNotFoundError:
    # Print instructions and quit if file not found
    print("File '%s' not found. Please run data_loader.py to generate student graphs." %
          student_graph_filename)
    exit()

# Load all 4-cliques
four_cliques_filename = "data/4_cliques_" + sample_suffix
try:
    # Try to load file specified by suffix
    four_cliques = joblib.load(four_cliques_filename)
    print("%i 4-cliques loaded" % len(four_cliques))
except FileNotFoundError:
    # Print instructions and quit if file not found
    print("File '%s' not found. Please run data_loader.py to generate student graphs and cliques." %
          four_cliques_filename)
    exit()

# Load all 5-cliques
five_cliques_filename = "data/5_cliques_" + sample_suffix
try:
    # Try to load file specified by suffix
    five_cliques = joblib.load(five_cliques_filename)
    print("%i 5-cliques loaded" % len(five_cliques))
except FileNotFoundError:
    # Print instructions and quit if file not found
    print("File '%s' not found. Please run data_loader.py to generate student graphs and cliques." %
          five_cliques_filename)
    exit()

# This will re-assign compatibility scores, which are not saved with the clique
# data. This is a relatively fast operation, and if the compatibility function
# is being updated, doing this in main every time, rather than making it
# optional, makes it easier to ensure you're not using old compatibility scores.

# Find team compatability of each 4-clique
for team in four_cliques:
    # Compute team compatibility and store as a property of the graph
    team.graph['compat'] = team_compatibility(team.nodes)

# Find team compatability of each 5-clique
for team in five_cliques:
    # Compute team compatibility and store as a property of the graph
    team.graph['compat'] = team_compatibility(team.nodes)

# Filter out any 4-cliques with negative compatibility
four_cliques = [team for team in four_cliques if team.graph['compat'] > 0]
print("%i four-cliques loaded." % len(four_cliques))
# Filter out any 5-cliques with negative compatibility
five_cliques = [team for team in five_cliques if team.graph['compat'] > 0]
print("%i five-cliques loaded." % len(five_cliques))

# sort the cliques by highest compatibility scores
four_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)
five_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)

print("All cliques loaded and sorted.")

# Figure out how many groups of 4 and 5 to create
num_students = len(student_graph.nodes)
num_5teams, num_4teams = num_size_teams(num_students)
print("Students: %i; 4-teams: %i; 5-teams: %i" %
      (num_students, num_4teams, num_5teams))

# Randomly assign teams and score result
print("Running random assignments...")
rand_teams = assign_teams_random(
    four_cliques, five_cliques, num_4teams, num_5teams)
print("Cost: (lower is better): %.3f" % assignment_cost(rand_teams))
# Show more detailed info on members of each team
for team in rand_teams:
    print("\nCompat: %.2f Eval: %.2f" %
          (team.graph['compat'], team_evaluation(team)))
    # Show skill areas for each student
    for student in team.nodes:
        print("%s: %i/%i, %i/%i, %i/%i, %i/%i, %i/%i, %i" % (
            student.name,
            student.intr_mgmt, student.exp_mgmt,
            student.intr_prog, student.exp_prog,
            student.intr_elec, student.exp_elec,
            student.intr_cad, student.exp_cad,
            student.intr_fab, student.exp_fab,
            student.commitment
        ))
    # Show what topics the team had most in common
    print(sorted_topics(team)[:3])
    # List any partner requests satistifed by the team
    print(list_met_partner_prefs(team))


# Assign teams with greedy algorithm and score result
print("\n\nRunning greedy...")
# Greedily assign required numbers of teams of 4 and 5
# Set "best" cost yet to a very high (bad) value
best_greedy_teams, best_greedy_cost = None, 1000
# Run greedy algorithm with i values from 0-9, choosing the ith-best clique as
# the first team each time. Compare to previous results and keep track of the
# result that minimized the cost.
for i in range(10):
    # Note: 4-cliques are always selected first and they affect the options for
    # choosing 5-cliques, so don't worry about starting with the ith 5-clique.
    greedy_teams = assign_teams_greedy(
        four_cliques[i:], five_cliques, num_4teams, num_5teams)
    # Compute cost for this iteration
    cost = assignment_cost(greedy_teams)
    # Reassign best-yet values if this result is better than previous best
    if cost < best_greedy_cost:
        best_greedy_cost = cost
        best_greedy_teams = greedy_teams

# Show more detailed info on members of each team
print("Cost: (lower is better): %.3f" % best_greedy_cost)
for team in best_greedy_teams:
    print("\nCompat: %.2f Eval: %.2f" %
          (team.graph['compat'], team_evaluation(team)))
    # Show skill areas for each student
    for student in team.nodes:
        print("%s: %i/%i, %i/%i, %i/%i, %i/%i, %i/%i, %i" % (
            student.name,
            student.intr_mgmt, student.exp_mgmt,
            student.intr_prog, student.exp_prog,
            student.intr_elec, student.exp_elec,
            student.intr_cad, student.exp_cad,
            student.intr_fab, student.exp_fab,
            student.commitment
        ))
    # Show what topics the team had most in common
    print(sorted_topics(team)[:3])
    # List any partner requests satistifed by the team
    print(list_met_partner_prefs(team))


# NOTE: Possible future work, but doesn't quite work yet
# print("Running recursive backtracking...")

# # Demote 4-cliques so 5s will be chosen first
# for team in four_cliques:
#     team.graph['compat'] = team.graph['compat'] - 1

# # Make combination of all cliques
# all_cliques = five_cliques + four_cliques
# all_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)

# cost, teams = assign_teams_rec(
    #     four_cliques[:10000], five_cliques[:10000], 0, [], set(), num_students, num_5teams+num_4teams)

    # print("Cost: (lower is better): %.3f" % cost)
    # for team in teams:
    #     print(team.nodes, "\tCompat: %.2f Eval: %.2f" %
    #           (team.graph['compat'], team_evaluation(team)))
