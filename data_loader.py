"""
Deals with importing data from survey results and converting to Student
objects.

When run as a main program, saves graph and clique data created from a sample
of the loaded data.
"""
import itertools as it
import joblib
import networkx as nx
import pandas as pd
import random
from clique_finding import find_k_clique
from helpers import violates_anti_prefs
from student import Student


def load_student_data(filename):
    """
    Loads student responses from a survey results file and returns a list of
    Student objects representing each student's data.
    """
    # Read csv data into dataframe
    data = pd.read_csv(filename)
    # Create empty list to store students
    students = []
    # Count # of students as # of rows in dataframe
    # Header row is not counted by default.
    num_students = len(data)

    # Create a random list of commitment scores for students from 1-5, weighted
    # so that extreme scores are less common (but 5s are more common than 1s,
    # because Oliners love biting off more than they can chew.)
    # This data is theoretically collected in the survey, but was not included
    # in the anonymized data we obtained.
    commitments = random.choices(
        range(1, 6), weights=[1, 3, 4, 3, 1.5], k=num_students)

    # Each row represents a student
    for idx, row in data.iterrows():
        # Get data from AntiPrefs column
        anti_prefs_data = row["AntiPrefs"]
        # If anti preferences column is not empty:
        if str(anti_prefs_data) != "nan":
            # Make a set of the names, split by ";" and stripped of whitespace
            anti_prefs = set(
                [anti_pref.strip()
                 for anti_pref in str(anti_prefs_data).split(";")]
            )
        # If the column is empty, set it as an empty set
        else:
            anti_prefs = set()

        # Get data from Prefs column
        prefs_data = row["Prefs"]
        # If preferences column is not empty:
        if str(prefs_data) != "nan":
            # Make a set of the names, split by ";" and stripped of whitespace
            preferences = set([pref.strip()
                              for pref in str(prefs_data).split(";")])
        # If the column is empty, set it as an empty set
        else:
            preferences = set()

        # Get data from ProjTopics column
        topics_data = row["ProjTopics"]
        # If project topics column is not empty:
        if str(topics_data) != "nan":
            # Make a set of the topics, split by ";" and stripped of whitespace
            topics = set([intr.strip()
                         for intr in str(topics_data).split(";")])
        # If the column is empty, set it as an empty set
        else:
            topics = set()

        # Create Student object with all the data collected above
        s = Student(
            name=row["Student"],
            pronouns=row["Pronouns"],
            commitment=commitments[idx],
            topics=topics,
            preferences=preferences,
            anti_prefs=anti_prefs,
            intr_mgmt=row["IntLeadership"],
            exp_mgmt=row["ExpLeadership"],
            intr_elec=row["IntElecProto"],
            exp_elec=row["ExpElecProto"],
            intr_prog=row["IntProg"],
            exp_prog=row["ExpProg"],
            intr_cad=row["IntMechCAD"],
            exp_cad=row["ExpMechCAD"],
            intr_fab=row["IntMechFab"],
            exp_fab=row["ExpMechFab"],
        )
        # Add student to output list
        students.append(s)

    return students


def create_student_graph(students):
    """
    Given a list of Student objects, creates a graph connecting all students
    except those that have a silver bullet between them

    Arguments:
        a list containing Student objects

    Returns:
        a networkx Graph object where the nodes are Student objects and the edges
        are possible (non-silver-bulleted) connections
    """
    # Add all the students as nodes in the graph
    student_graph = nx.Graph()
    student_graph.add_nodes_from(students)

    # Add edges between students that have no anti-preferences between them
    for student1, student2 in it.combinations(students, 2):
        if not student1.dislikes(student2) and not student2.dislikes(student1):
            student_graph.add_edge(student1, student2)

    return student_graph


def create_save_k_cliques(k, student_graph, suffix):
    """
    Generate all k-cliques from a student graph and save the list of cliques.

    Ensures that no clique puts students together where one of them listed the
    other as an anti-preference.

    Suffix will be a character or string that should correspond to the data
    table from which the input graph of students was generated, plus a number
    indicating the number of students sampled from the data table to create the
    graph.
    """
    # Create file name to store k-cliques data
    k_cliques_filename = "data/%i_cliques_%s" % (k, suffix)
    # Compute all possible k-cliques
    print("Generating %i-cliques..." % k)
    k_cliques = find_k_clique(student_graph, k)
    print("%i %i-cliques found." % (len(k_cliques), k))

    # Do not save any cliques that put anti-preferences together
    # They shouldn't make it this far, but checking can save a lot of time
    k_cliques = [team for team in k_cliques if not violates_anti_prefs(team)]
    print("%i valid %i-cliques found." % (len(k_cliques), k))

    # Save list of k-cliques in file determined above
    joblib.dump(k_cliques, k_cliques_filename)
    print("%i-cliques saved in %s" % (k, k_cliques_filename))


if __name__ == "__main__":
    # Ask for suffix to choose which section of anonymized survey data the
    # students will be pulled from
    survey_file_suffix = input(
        "Enter suffix for survey data filename: anonymized_surveys_")
    survey_filename = "data/anonymized_surveys_" + survey_file_suffix + ".csv"

    # Parse data from survey to create Student objects
    try:
        students = load_student_data(survey_filename)
    except FileNotFoundError:
        print("File %s not found. Please check your working folder and spelling." %
              survey_filename)
        exit()
    print("%i students loaded from %s." % (len(students), survey_filename))

    # Ask for number of students to include in the sample
    num_students = int(input("Enter a number of students: "))

    # Create a random sample of students of the size specified
    students_sample = random.sample(students, num_students)

    # Create the graph from the previously-loaded students, using Student
    # objects as vertices and making an edge between each pair of students that
    # do not have an anti-preference between them
    sample_student_graph = create_student_graph(students_sample)

    # Create a suffix to represent the data from this batch of students, using
    # the suffix associated with the chosed survey data and the number of
    # students in the sample
    sample_suffix = survey_file_suffix + str(num_students)

    # Create a file name to save the graph, identified by the sample suffix
    graph_filename = "data/student_graph_" + sample_suffix

    # Save graph in file determined above
    joblib.dump(sample_student_graph, graph_filename)
    print("Saving", graph_filename)

    # Create and save k-cliques for k=[4, 5] to represent the possible teams
    # that can be formed from this graph
    create_save_k_cliques(4, sample_student_graph, sample_suffix)
    create_save_k_cliques(5, sample_student_graph, sample_suffix)
