"""
Functions which assign multiple non-overlapping teams of students
"""
from random import shuffle
from helpers import overlaps
from scoring import assignment_cost, team_compatibility


def assign_teams_greedy(four_cliques, five_cliques, n_4, n_5):
    """
    Assign students into the specified numbers of teams of 4 and 5 using a 
    greedy algorithm.

    Returns a list of cliques representing the chosen teams.
    """
    # Define assigned_students in case no 4-cliques are needed, in which case
    # it would not be initialized in the 4-clique loop
    assigned_students = set()
    # List to store chosen teams of 4 - also needs to be pre-defined in case
    # 4-cliques loop is skipped
    teams_of_4 = []
    # What index the greedy algorithm will start at - if the algorithm reaches
    # the end of the clique list without finding enough non-overlapping
    # cliques, this will be incremented and it will try again
    start_at = 0
    while len(teams_of_4) < n_4:
        # While there aren't enough 4-cliques, empty the collector variables
        assigned_students = set()
        teams_of_4 = []
        # For this loop, start by choosing the team at index start_at
        team_idx = start_at
        # While there are still 4-cliques left to choose...
        while team_idx < len(four_cliques):
            # Pick current one as the next team to consider
            curr_team = four_cliques[team_idx]
            # Check whether this team overlaps with previously selected students
            if not overlaps(curr_team.nodes, assigned_students):
                # If not, add it to the list of chosen teams
                teams_of_4.append(curr_team)
                # Add students in this team to assigned_students
                assigned_students |= curr_team.nodes
                # If you have now collected enough 4-cliques, exit inner loop
                if len(teams_of_4) == n_4:
                    break
            # If the last team overlapped or you still need more 4-cliques,
            # increment the team index and continue
            team_idx += 1
        # If you ran out of 4-cliques to look at but there are not enough chosen
        # 4-cliques yet, repeat the process starting with the next best team
        start_at += 1

    # Make a copy of the students have been assigned into teams of 4. This
    # provides a point to reset to any time the greedy process for choosing
    # teams of 5 needs to start over.
    prev_assigned_students = set(assigned_students)
    # List to store chosen teams of 5
    teams_of_5 = []
    # Since this is looking at a whole new list, reset the start_at index
    start_at = 0
    while len(teams_of_5) < n_5:
        # While there aren't enough 5-cliques, empty the collector variables
        assigned_students = prev_assigned_students
        teams_of_5 = []
        # For this loop, start by choosing the team at index start_at
        team_idx = start_at
        # While there are still 5-cliques left to choose...
        while team_idx < len(five_cliques):
            # Pick current one as the next team to consider
            curr_team = five_cliques[team_idx]
            # Check whether this team overlaps with previously selected students
            if not overlaps(curr_team.nodes, assigned_students):
                # If not, add it to the list of chosen teams
                teams_of_5.append(curr_team)
                # Add students in this team to assigned_students
                assigned_students |= curr_team.nodes
                # If you have now collected enough 5-cliques, exit inner loop
                if len(teams_of_5) == n_5:
                    break
            # If the last team overlapped or you still need more 5-cliques,
            # increment the team index and continue
            team_idx += 1
        # If you ran out of 5-cliques to look at but there are not enough chosen
        # 5-cliques yet, repeat the process starting with the next best team
        start_at += 1

    return teams_of_4 + teams_of_5


def assign_teams_random(four_cliques, five_cliques, n_4, n_5):
    """
    Randomly assign students into the specified numbers of teams of 4 and 5.

    The only restriction is that teams cannot have overlapping students.
    Returns a list of cliques representing the chosen teams.
    """
    # Copy and randomly shuffle cliques to be chosen from - shuffle is in-place,
    # so we don't want to modify the original clique lists which may be passed
    # to another algorithm
    four_cliques = four_cliques[:]
    five_cliques = five_cliques[:]
    shuffle(four_cliques)
    shuffle(five_cliques)

    # Define assigned_students in case no 5-cliques are needed, in which case
    # it would not be initialized in the 5-clique loop
    assigned_students = set()
    # List to store chosen teams of 5 - also needs to be pre-defined in case
    # 5-cliques loop is skipped
    teams_of_5 = []
    # What index the random algorithm will start at - if the algorithm reaches
    # the end of the clique list without finding enough non-overlapping
    # cliques, this will be incremented and it will try again
    start_at = 0
    while len(teams_of_5) < n_5:
        # While there aren't enough 5-cliques, empty the collector variables
        assigned_students = set()
        teams_of_5 = []
        # For this loop, start by choosing the team at index start_at
        team_idx = start_at
        # While there are still 5-cliques left to choose...
        while team_idx < len(five_cliques):
            # Pick current one as the next team to consider
            curr_team = five_cliques[team_idx]
            # Check whether this team overlaps with previously selected students
            if not overlaps(curr_team.nodes, assigned_students):
                # If not, add it to the list of chosen teams
                teams_of_5.append(curr_team)
                # Add students in this team to assigned_students
                assigned_students |= curr_team.nodes
                # If you have now collected enough 5-cliques, exit inner loop
                if len(teams_of_5) == n_5:
                    break
            # If the last team overlapped or you still need more 5-cliques,
            # increment the team index and continue
            team_idx += 1
        # If you ran out of 5-cliques to look at but there are not enough chosen
        # 5-cliques yet, repeat the process starting with the next best team
        start_at += 1

    # Make a copy of the students have been assigned into teams of 5. This
    # provides a point to reset to any time the process for choosing teams of 4
    # needs to start over.
    prev_assigned_students = set(assigned_students)
    # List to store chosen teams of 4
    teams_of_4 = []
    # Since this is looking at a whole new list, reset the start_at index
    start_at = 0
    while len(teams_of_4) < n_4:
        # While there aren't enough 4-cliques, empty the collector variables
        assigned_students = prev_assigned_students
        teams_of_4 = []
        # For this loop, start by choosing the team at index start_at
        team_idx = start_at
        # While there are still 4-cliques left to choose...
        while team_idx < len(four_cliques):
            # Pick current one as the next team to consider
            curr_team = four_cliques[team_idx]
            # Check whether this team overlaps with previously selected students
            if not overlaps(curr_team.nodes, assigned_students):
                # If not, add it to the list of chosen teams
                teams_of_4.append(curr_team)
                # Add students in this team to assigned_students
                assigned_students |= curr_team.nodes
                # If you have now collected enough 4-cliques, exit inner loop
                if len(teams_of_4) == n_4:
                    break
            # If the last team overlapped or you still need more 4-cliques,
            # increment the team index and continue
            team_idx += 1
        # If you ran out of 4-cliques to look at but there are not enough chosen
        # 4-cliques yet, repeat the process starting with the next best team
        start_at += 1

    return teams_of_4 + teams_of_5

# TODO: This doesn't quite work yet, but I would really like to get it working
# in the future!
def assign_teams_rec(four_cliques, five_cliques, i, chosen_cliques, assigned_students, num_students, n):
    """
    Assign students into the specified numbers of teams of 4 and 5 using a 
    recursive backtracking algorithm.

    Returns a list of cliques representing the chosen teams.
    """
    num_students_left = num_students - len(assigned_students)
    # If you can divide remaining students by 4, but not 5,
    if (num_students_left % 4 == 0) and (num_students_left % 5 != 0):
        # Start picking from 4-cliques
        cliques = four_cliques
        # And make it impossible to go back to 5-cliques
        five_cliques = four_cliques
    else:
        cliques = five_cliques

    # Base case: no more cliques to choose from
    if i >= len(cliques):
        return 10000, None
    # Base case: no more cliques required -> return cost & choices
    if n == 0:
        print(0, chosen_cliques)
        return assignment_cost(chosen_cliques), chosen_cliques[:]

    # Additional base case: choose the next best clique of unassigned students
    if n == 1:
        if num_students-len(assigned_students) < 4:
            # Can't create any more teams, so just score what you have
            return assignment_cost(chosen_cliques), chosen_cliques[:]

        j = i
        # Find the first team of unassigned students, since they are sorted
        # by score
        while j < 1000 and overlaps(cliques[j].nodes, assigned_students):
            j += 1
        if j >= len(cliques):
            # There are no cliques with the remaining students without silver
            # bullets
            return 10000, None

        new_cliques = chosen_cliques + [cliques[j]]
        # Calculate the overall score
        cost = assignment_cost(new_cliques)
        return cost, new_cliques

    # Recursive case:
    # Get current clique
    curr_clique = cliques[i]
    # Set costs for including or excluding very high by default
    cost_incl, cost_excl = 10000, 10000
    # Set both team options to None
    teams_incl, teams_excl = None, None
    # If ith clique does not overlap:
    if not overlaps(curr_clique.nodes, assigned_students):
        #   Get cost & choices for including ith clique
        new_cliques = chosen_cliques + [curr_clique]
        new_assigned_students = assigned_students | curr_clique.nodes
        cost_incl, teams_incl = assign_teams_rec(
            four_cliques, five_cliques, i+1, new_cliques, new_assigned_students, num_students, n-1)

    if not teams_incl or team_compatibility(teams_incl[-1]) < 8:
        # Get cost & choices for excluding ith clique
        cost_excl, teams_excl = assign_teams_rec(
            four_cliques, five_cliques, i+1, chosen_cliques, assigned_students, num_students, n)

    if cost_excl > cost_incl:
        cost, teams = cost_incl, teams_incl
    else:
        cost, teams = cost_excl, teams_excl
    return cost, teams
