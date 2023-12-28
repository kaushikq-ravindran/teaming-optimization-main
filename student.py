class Student:
    """
    Represents a student. Contains data about their skills, experience and
    preferences as described in a survey data file.
    """
    def __init__(self, name, pronouns, commitment=0, topics=None,
                 preferences=None, anti_prefs=None, intr_mgmt=0, exp_mgmt=0,
                 intr_elec=0, exp_elec=0, intr_prog=0, exp_prog=0, intr_cad=0,
                 exp_cad=0, intr_fab=0, exp_fab=0):
        
        self.name = name
        self.pronouns = pronouns
        self.commitment = commitment

        # Create empty sets for these if no input is given
        self.topics = topics or set()
        self.preferences = preferences or set()
        self.anti_prefs = anti_prefs or set()

        # For each skill area, store interest and experience rating from 1-5
        self.intr_mgmt = intr_mgmt
        self.exp_mgmt = exp_mgmt
        # Also create a combined rating for this skill, from 2-10
        self.mgmt = intr_mgmt + exp_mgmt

        self.intr_elec = intr_elec
        self.exp_elec = exp_elec
        self.elec = intr_elec + exp_elec

        self.intr_prog = intr_prog
        self.exp_prog = exp_prog
        self.prog = intr_prog + exp_elec

        self.intr_cad = intr_cad
        self.exp_cad = exp_cad
        self.cad = intr_cad + exp_cad

        self.intr_fab = intr_fab
        self.exp_fab = exp_fab
        self.fab = intr_fab + exp_fab

        # Create a mechanical skill area as the average of CAD and fabrication
        self.intr_mech = (intr_cad + intr_fab) / 2
        self.exp_mech = (exp_cad + exp_fab) / 2
        self.mech = self.intr_mech + self.exp_mech

    def __repr__(self):
        return self.name

    def __hash__(self):
        """
        Students with the same name should be hashed the same.
        This way, copies of one student in different cliques loaded from a file 
        will be seen as the same if they have the same name.
        """
        return hash(self.name)

    def __eq__(self, other):
        """
        Students with the same name should be considered equal.
        This way, copies of one student in different cliques loaded from a file 
        will be seen as overlapping if they have the same name.
        """
        return self.name == other.name

    def prefers(self, other_student):
        """
        Returns True if other_student is one of this student's preferred
        partners, False otherwise.
        """
        if other_student.name in self.preferences:
            return True
        return False

    def dislikes(self, other_student):
        """
        Returns True if this student has requested not to work with
        other_student, False otherwise.
        """
        if other_student.name in self.anti_prefs:
            return True
        return False
