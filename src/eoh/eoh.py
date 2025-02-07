
import random

from .utils import createFolders
from .methods import methods
from .problems import problems

# main class for AEL
class EVOL:

    # initilization
    def __init__(self, paras, prob=None, **kwargs):

        print("----------------------------------------- ")
        print("---              Start EoH            ---")
        print("-----------------------------------------")
        # Create folder #
        createFolders.create_folders(paras.exp_output_path, paras.ec_use_example)
        print("- output folder created -")

        self.paras = paras

        print("-  parameters loaded -")

        self.prob = prob

        # Set a random seed
        random.seed(2024)

        
    # run methods
    def run(self):

        problemGenerator = problems.Probs(self.paras)

        problem = problemGenerator.get_problem() #problem evaluation function

        methodGenerator = methods.Methods(self.paras, problem) # parent_selection, pop_manager

        method = methodGenerator.get_method() # eoh, funsearch, reevo

        method.run()

        print("> End of Evolution! ")
        print("----------------------------------------- ")
        print("---     EoH successfully finished !   ---")
        print("-----------------------------------------")

        exit(1)
