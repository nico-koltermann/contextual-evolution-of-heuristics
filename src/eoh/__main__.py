# Copyright (c) 2025
#           Thomas Bömer (thomas.bömer@tu-dortmund.de)
#           Nico Koltermann (nico.koltermann@tu-dortmund.de) 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import json
import click
import logging

from dotenv import load_dotenv

import src.eoh.eoh as eoh

from src.eoh.utils.getParas import Paras
from src.eoh.llm.models import get_model_info

###################################################################

@click.group()
@click.pass_context
def main(ctx):
    pass

@main.command()
@click.argument("problem")
@click.option('--model_name', default="llama3.1:70b", help='LLM model')
@click.option('--use_example', default=1, help='Use Example for LMM request')
def run(problem, model_name, use_example):

    bool_use_example = bool(use_example)

    # Parameter initilization #
    paras = Paras()

    load_dotenv()

    api_key = ""

    if api_key == None:
        print('##########################################')
        print(' -- No LLM API Key is set. -- ')
        print(' -- Have a look into the .env file! -- ')
        print('##########################################')


    llm_api_endpoint, add_url_info, api_key, llm_use_local = \
         get_model_info(model_name)

    local_llm_endpoint = ""
    if llm_use_local:
        local_llm_endpoint = llm_api_endpoint

    # Set parameters

    paras.set_paras(
        eoh_experiment_file = "exp_1.json",
        llm_api_key=api_key,
        llm_api_endpoint=llm_api_endpoint,
        llm_use_local=llm_use_local,
        llm_url_info=add_url_info,
        method="eoh",  # ['eoh']
        problem=problem,
        llm_model=model_name,
        llm_local_url=local_llm_endpoint,
        ec_pop_size=20,  # number of samples in each population
        ec_operators=['e1', 'e2', 'm1', 'm2'],  # operators in EoH
        ec_use_example=bool_use_example,
        ec_n_pop=20,  # number of populations
        exp_n_proc=1,  # number of parallel processes
        ec_m = 5,  # number of parents for 'e1' and 'e2' operators, default = 2
        exp_debug_mode=False,
        eva_numba_decorator=False,
        exp_continue_pop_nr = 20,
        exp_continue_folder = "results_20241220_123725_multibay_reshuffle_qwen25coder32b_ueTrue",
        exp_use_continue = False,
        llm_temperature=None,
    )

    # initilization
    evolution = eoh.EVOL(paras)

    current_folder = os.environ["CURRENT_EXPERIMENT"]

    # let logging
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level to DEBUG or INFO as needed
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=os.path.join(current_folder, 'parallel_log.log'),  # Specify a log file
        filemode='w'  # Use 'w' to overwrite the log file each time, or 'a' to append
    )

    # Save all experiments
    paras_json = vars(paras).copy()
    paras_json['llm_api_key'] = "---"
    with open(os.path.join(current_folder, "setup.json"), 'w+') as f:
        json.dump(paras_json, f, indent=5)

    experiment_path = os.path.join(os.getenv('BASE_PATH'), "eoh_experiment")

    experiments = []
    if paras.eoh_experiment_file != "":
        f_exp = open(os.path.join(experiment_path, paras.eoh_experiment_file))
        experiments.append(json.load(f_exp))

    with open(os.path.join(current_folder, "evaluation_experiments.json"), 'w+') as f:
        json.dump('{ experiments: '+ str(experiments) +' }', f, indent=5)

    # run
    evolution.run()
