import itertools


def num_size_teams(num_students):
    """
    Takes in a number of students and calculate how many 4 and 5 person teams
    they should be on.

    Returns a tuple of (5-person teams, 4-person teams).
    """
    # Count how many teams will be missing 1 person compared to a 5-person team
    teams_of_4 = - num_students % 5

    # If there are not enough students to make that many 4-person teams, it
    # won't be possbile to evenly put people on 4 and 5 person teams
    if num_students // 4 < teams_of_4:
        return 0, 0

    # Calculate number of 5-person teams based on how many are left after making
    # 4-person teamsn
    teams_of_5 = (num_students - 4 * teams_of_4) // 5

    return teams_of_5, teams_of_4


def violates_anti_prefs(team):
    """
    Checks if there is an anti-preference for any student in a list from any 
    other student in the list.
    """
    all_anti_prefs = set()
    # Loop through all team members and add their anti-preferences to a set
    for student in team:
        all_anti_prefs |= student.anti_prefs
    # Loop through all team members again, and check if they are in the set.
    for student in team:
        # If so, that means they were anti-preferenced by another team member.
        if student.name in all_anti_prefs:
            return True
    return False


def list_met_partner_prefs(team):
    """
    Counts the number of instances where a student on a team had requested to
    work with another student on that team.

    For example, if Alice and Bob are on a team and Alice requested to work with Bob, that gets a 1.

    If Alice and Bob both requested each other, that gets a 2.

    If Alice, Bob and Carol are on a team and Alice requested to work with Bob
    and Carol, that gets a 2.

    If Alice, Bob and Carol all mutually rquested each other, that gets a 6.
    """
    # This will store the ordered pairs of met preferences between teammates
    met_partner_prefs = []

    # Find all possoble ordered pairs of teammates
    # Includes both (A, B) and (B, A), because preferences are directional: even
    # if A prefers B, B may not prefer A
    teammate_pairs = itertools.permutations(team, 2)

    # Loop through the possible pairs of students who could have preferred each
    # other, and see if the first one actually did prefer the second
    for studentA, studentB in teammate_pairs:
        # If so, add that ordered pair to the output list
        if studentA.prefers(studentB):
            met_partner_prefs.append((studentA, studentB))

    return met_partner_prefs


def count_met_partner_prefs(team):
    """
    Counts the number of instances where a student on a team had requested to
    work with another student on that team.

    For example, if Alice and Bob are on a team and Alice requested to work with Bob, that gets a 1.

    If Alice and Bob both requested each other, that gets a 2.

    If Alice, Bob and Carol are on a team and Alice requested to work with Bob
    and Carol, that gets a 2.

    If Alice, Bob and Carol all mutually rquested each other, that gets a 6.
    """
    # Create a dictionary where the keys are each student in the team members'
    # preference lists, and the values are the number of students on the team
    # who listed the key student as a preference
    all_preferences = {}

    # This will count the number of directional preferences that are satisfied
    # between the members on this team
    num_met_partner_prefs = 0

    # Count up times each student (even non-teammates) was listed as a
    # preference by someone on this team
    for student in team:
        # Loop through each team member's preferences
        for pref in student.preferences:
            # Increment the count for this preference by 1
            all_preferences[pref] = all_preferences.get(pref, 0) + 1

    # Loop through the students specifically who are on this team, and add up
    # how many times they were listed as preferences by their teammates
    for student in team:
        num_met_partner_prefs += all_preferences.get(student.name, 0)

    return num_met_partner_prefs


def count_mutual_partner_prefs(team):
    """
    Counts the number of instances where two students on a team both requested
    to work with each other.

    For example, if Alice and Bob are on a team and Alice requested to work with Bob, that gets a 0.

    If Alice and Bob both requested each other, that gets a 1.

    If Alice, Bob and Carol all mutually rquested each other, that gets a 3.
    """
    # This will count the number of mutual preferences that are satisfied
    # within the team
    mutual_partner_prefs = 0

    # Find all possoble unordered pairs of teammates. Should be unordered
    # because mutual preferences are bidirectional: Checking if (A, B) have a
    # mutual preference will involve checking if they both prefer each other
    teammate_pairs = itertools.combinations(team, 2)

    # Loop through the possible pairs of students who could have preferred each
    # other, and see if they both preferred each other
    for studentA, studentB in teammate_pairs:
        if studentA.prefers(studentB) and studentB.prefers(studentA):
            # If so, increment the count by 1
            mutual_partner_prefs += 1

    return mutual_partner_prefs


def skill_deficiency(team):
    """
    Calculates how much a team is lacking overall in 4 key areas:
    management, electrical, programming, and mechanical (CAD + fabrication).

    Returns value from 0 (good) to 1 (bad).

    Assumes that the team's ability in an area is equal to the ability of
    the strongest student in that area. Currently this is the sum of interest
    and experience, and a score of 8 is considered to be completely sufficient
    for any given area.

    For example, if a team has a student with 3 interest in programming and 5
    experience, or 4 and 4, that team will be considered to be sufficiently
    covered for programming.

    The overall deficiency is calculated as the distance that a team is from
    having at least 8 in each area, with each area treated like a dimension.
    **This means that having a small deficiency in several areas is better than
    having a big deficiency in 1 area.**
    """
    # Find out how good (interested + experienced) the best student on the team
    # is for each area
    max_mgmt = max(student.mgmt for student in team)
    max_elec = max(student.elec for student in team)
    max_prog = max(student.prog for student in team)
    max_mech = max(student.mech for student in team)

    # If the best student in an area handles each area, how deficient will the
    # team be if a score of 8 counts as complete sufficiency?
    # max(0, n) puts 0 as a lower bound, otherwise (8-10)**2 = 4 would be
    # considered deficient
    deficient_mgmt = max(0, 8-max_mgmt)**2
    deficient_elec = max(0, 8-max_elec)**2
    deficient_prog = max(0, 8-max_prog)**2
    deficient_mech = max(0, 8-max_mech)**2

    # Compute the sum of squared errors compared to complete sufficiency
    overall_deficiency = sum(
        [deficient_mgmt, deficient_elec, deficient_prog, deficient_mech]
    )

    # Max possible is 144, so normalize to 0 (good) -> 1 (bad)
    return overall_deficiency / 144


def exp_deficiency(team):
    """
    Like skill_deficiency, but focuses only on experience for technical areas.

    Returns value from 0 (good) to 1 (bad).
    """
    # Find out how experienced the most experienced student on the team is for
    # each area
    max_elec = max(student.exp_elec for student in team)
    max_prog = max(student.exp_prog for student in team)
    max_fab = max(student.exp_fab for student in team)
    max_cad = max(student.exp_cad for student in team)

    # If the best student in an area handles each area, how deficient will the
    # team be if a score of 4 counts as complete sufficiency?
    # max(0, n) puts 0 as a lower bound, otherwise (4-5)**2 = 1 would be
    # considered deficient
    deficient_elec = max(0, 4-max_elec)**2
    deficient_prog = max(0, 4-max_prog)**2
    deficient_fab = max(0, 4-max_fab)**2
    deficient_cad = max(0, 4-max_cad)**2

    # Compute the sum of squared errors compared to complete sufficiency
    overall_deficiency = sum(
        [deficient_elec, deficient_prog, deficient_fab, deficient_cad]
    )

    # Max possible is 36, so normalize to 0 (good) -> 1 (bad)
    return overall_deficiency / 36


def intr_deficiency(team):
    """
    Like skill_deficiency, but focuses only on interest for technical areas.

    Returns value from 0 (good) to 1 (bad).
    """
    # Find out how interested the most interested student on the team is for
    # each area
    max_elec = max(student.intr_elec for student in team)
    max_prog = max(student.intr_prog for student in team)
    max_fab = max(student.intr_fab for student in team)
    max_cad = max(student.intr_cad for student in team)

    # If the best student in an area handles each area, how deficient will the
    # team be if a score of 4 counts as complete sufficiency?
    # max(0, n) puts 0 as a lower bound, otherwise (4-5)**2 = 1 would be
    # considered deficient
    deficient_elec = max(0, 4-max_elec)**2
    deficient_prog = max(0, 4-max_prog)**2
    deficient_fab = max(0, 4-max_fab)**2
    deficient_cad = max(0, 4-max_cad)**2

    # Compute the sum of squared errors compared to complete sufficiency
    overall_deficiency = sum(
        [deficient_elec, deficient_prog, deficient_fab, deficient_cad]
    )

    # Max possible is 36, so normalize to 0 (good) -> 1 (bad)
    return overall_deficiency / 36


def percent_strongly_skilled(team):
    """
    Returns the percent of students on a team who are "strongly skilled" at 
    something.

    Returns value from 0 (bad) to 1 (good).

    "Strongly skilled" is defined as having a total score of 8 or more in
    combined interest and experience.
    The goal of this function is to find teams where a couple of students are
    strong in a lot of areas, and might end up with the responsibility of
    teaching their teammates a lot. **This is kind of a proxy for making sure
    that there is a separate student who can "lead" the team in each area.**

    If any student does not have a particular strong skill, this will return
    less than 1.
    """
    # Find the list of students who are "good" (interest + experience >= 8) in
    # each skill area
    good_mgmt_students = filter(lambda student: student.mgmt >= 8, team)
    good_elec_students = filter(lambda student: student.elec >= 8, team)
    good_prog_students = filter(lambda student: student.prog >= 8, team)
    good_mech_students = filter(lambda student: student.mech >= 8, team)

    # Find the set of students who are "good" in any of the skill areas
    specialized_students = set().union(
        good_mgmt_students, good_elec_students,
        good_prog_students, good_mech_students
    )

    # Return the fraction of students on the team that are "good" at something
    # Normalize to 0 (good) -> 1 (bad)
    return len(specialized_students) / len(team)


def sorted_topics(team):
    """
    Returns a list of (topic, votes) tuples sorted from highest to lowest number
    of votes.

    Represents the number of times each topic was voted for on a team.
    """
    # Create a dictionary where the keys are each topic liked by any of the team
    # members, and the values are the number of students on the team who voted
    # for that topic
    all_topics = {}

    # Loop through the team members
    for student in team:
        # For each topic they voted for, increment that topic's votes by 1
        for topic in student.topics:
            all_topics[topic] = all_topics.get(topic, 0) + 1

    # Return the list of (topics, votes) tuples from the dictionary, sorted
    # from highest to lowest number of votes
    return sorted(all_topics.items(), key=lambda item: item[1], reverse=True)


def sorted_topic_votes(team):
    """
    Returns a list of the numbers of students who voted for different topics,
    sorted by number of votes.

    For example, if 3 people on the team vote for a music-related project, 2
    vote for a robotics-related project, and 1 votes for an art-related project,
    this will return [3, 2, 1].

    By taking the first n items from the output, another function could figure
    out how much agreement there can be on the project topic if n topics could
    be incorporated into the project.
    """
    # Get the list of (topic, votes) tuples sorted from highest to lowest number
    # of votes.
    team_sorted_topics = sorted_topics(team)

    # Return a list of just the votes, sorted from most to least.
    return [votes for _, votes in team_sorted_topics]


def overlaps(nodes1, nodes2):
    """
    Returns True if the two sets of nodes share at least 1 common node, False if not.
    """
    # If cardinality of intersection of the node-sets is > 0, the node-sets
    # overlap
    return bool(len((nodes1 & nodes2)))
