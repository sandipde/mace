import hashlib
import json
import mlflow
import logging
from typing import Dict, Any

from pip._internal.operations import freeze


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def package_list() -> list:
    pkgs = freeze.freeze()
    req=[pkg for pkg in pkgs]
    return req

def check_hash(args_dict, experiment):
    """Check for hash value of args for existing runs"""
    param_hash=dict_hash(args_dict)
    args_dict["param_hash"]=param_hash

    ## Check for existing run with same params using the hash paramter value
    filter_string = "params.param_hash = '{}'".format(param_hash) 
    #print(expt.experiment_id)
    runs = mlflow.search_runs(experiment_names=[args_dict["mlflow_project"]], filter_string=filter_string)
    run_ids=[run[1].run_id for run in runs.iterrows()]
    #print(run_ids)
    if len(run_ids)>0:
        logging.info(f"Found {len(run_ids)} runs with same params, using latest run")
        run_id=run_ids[-1]
        mlflow.start_run(experiment_id=experiment.experiment_id, run_id=run_id)
        logging.info(f"Continuing run with id {run_id} in experiment {experiment.name}")
    else:
        mlflow.start_run(experiment_id=experiment.experiment_id)
        logging.info("No previous runs found with same params, starting new run")

    return mlflow.log_params(args_dict)    