"""
Functions for scoring team assignments on different metrics
"""
import numpy as np
from math import perm
from helpers import (
    count_met_partner_prefs,
    percent_strongly_skilled,
    exp_deficiency,
    intr_deficiency,
    skill_deficiency,
    sorted_topic_votes,
    violates_anti_prefs
)


def assignment_cost(teams):
    """
    Calculate the overall cost (badness) of a selection of teams.

    Returns a cost value where lower is better and higher is worse.
    """
    try:
        # Assume teams is a list of subgraphs, and convert to a list of lists
        teams = [list(clique.nodes) for clique in teams]
        # Compute list of squared errors
        costs = [team_evaluation(clique)**2 for clique in teams]
    except:
        # Catch if it's already a list
        # Compute list of squared errors
        costs = [team_evaluation(team)**2 for team in teams]
    # return sum of squared errors
    return sum(costs)


def team_evaluation(team):
    """
    Evaluate how good the algorithm has done on forming a specific team.

    Returns a cost value where lower is better and higher is worse.
    """
    try:
        # Assume team is a subgraphs, and convert to a lists of nodes
        team = list(team.nodes)
    except:
        # If it's a list and doesn't have "nodes", no action is needed since
        # this function is designed for lists
        pass
    # Determine if one student was a "filler student"
    # Count how many students were not requested by their teammates when their
    # Teammates mostly requeste each other
    filler_students = 0
    # Figure out how many preferences were met between ALL students on the team
    full_team_cohesion = count_met_partner_prefs(team)

    # For each position in the team
    for i in range(len(team)):
        # Try removing the student at that position
        test_team = team[:i-1] + team[i+1:]
        # Count met partner prefs when that student is excluded (so, between
        # all their teammates)
        test_team_cohesion = count_met_partner_prefs(test_team)
        # Determine if the rest of the team is clique-ish: for all possible
        # ordered pairs of the other teammates, 75% of those pairs are
        # accounted for as met opertner preferences
        if test_team_cohesion >= perm(len(test_team), 2) * .75:
            # Then, determine if including the test student would not increase
            # the number of met partner preferences (if any of their teammates
            # preferred them, including them would increase that number)
            if full_team_cohesion == test_team_cohesion:
                # That student was probably a filler
                filler_students += 1

    # This is only really a bad thing if it happens to exaclty one student.
    # Normalize to 0 (good) -> 1 (bad)
    odd_person_out = 1 if filler_students == 1 else 0

    # Find deficiencies in technical areas, both in experience and in interest
    intr_defncy = intr_deficiency(team)
    exp_defncy = exp_deficiency(team)
    # Check if they are lacking a "good" (interest + experience > 8) PM
    # Find the best (intr+exp) PM score of any student on the team
    max_pm = max([student.mgmt for student in team])
    # Calculate how deficient the best PM score is, if 8 is considered
    # sufficient. Set a lower limit of 0 and normalize to 0 (good) -> 1 (bad)
    pm_defncy = max(0, 8-max_pm) / 8

    # Return weighted cost as sum of squared errors
    # Lower (good) -> higher (bad)
    return (
        4 * odd_person_out ** 2 +
        3 * pm_defncy ** 2 +
        2 * exp_defncy ** 2 +
        2 * intr_defncy ** 2
    )


def team_compatibility(team):
    """
    Computes a score for 1 team.

    Returns a value where lower is worse and higher is better.
    If any 2 students have an anti-preference between them, returns 0.
    """
    try:
        # Assume team is a subgraphs, and convert to a lists of nodes
        team = list(team.nodes)
    except:
        # If it's a list and doesn't have "nodes", no action is needed since
        # this function is designed for lists
        pass

    # If any students have an anti-preference between them, immediately return 0
    if violates_anti_prefs(team):
        return 0

    # Evaluate team on commitment, topic agreement, partner prefs,
    # skill deficiency & skill distribution

    # Variance is lower -> better
    commitment_variance = np.var([student.commitment for student in team])

    # Get list of vote counts for topics, sorted from most to least
    topic_votes = sorted_topic_votes(team)
    # How many topics (max 2) the considered votes are distributed over
    num_topics_considered = max(2, len(topic_votes))
    # How many votes did the best (up to) 2 topics get (Higher -> better)
    top_2_topic_votes = sum(topic_votes[:2])

    # Calculate how many partner preferences were met (Higher -> better)
    met_partner_prefs = count_met_partner_prefs(team)
    # Calculate how deficient the team is in combined interest + experience for
    # each area (0 (good) -> 1 (bad))
    skill_defncy = skill_deficiency(team)
    # Calculate what fraction of students on the team have a high combined
    # interest + experience in some skill area (0 (bad) -> 1 (good))
    skill_distribution = percent_strongly_skilled(team)

    # Normalize all values to be 0 (worst possible) -> 1 (best possible)

    # Max value for variance is 4, and lower means less variance which we want
    scaled_commitment = (4 - commitment_variance) / 4
    # Divide votes for top 2 topics by # of teammates and # of topics considered
    scaled_topics = top_2_topic_votes / (len(team) * num_topics_considered)
    # Divide met partner prefs by number of pairs of students who could have
    # preferred each other
    scaled_preference = met_partner_prefs / perm(len(team), 2)
    # Skill deficiency is already scaled, just need to invert it
    skill_sufficiency = 1 - skill_defncy

    # Return weighted score (yep, we're normalizing and then weighting them)
    return (
        3 * scaled_commitment +
        3 * skill_sufficiency +
        3 * skill_distribution +
        2 * scaled_topics +
        5 * scaled_preference
    )
