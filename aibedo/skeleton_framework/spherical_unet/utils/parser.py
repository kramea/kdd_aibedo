"""Command Line Parser realated functions.
One function creates the parser.
Another function allows hybird usage of:
- a yaml file with predefined parameters
and
- user inputted parameters through the command line.
"""

import argparse

import yaml


def create_parser():
    """Creates a parser with all the variables that can be edited by the user.

    Returns:
        parser: a parser for the command line
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", dest="config_file", type=argparse.FileType(mode="r"))

    parser.add_argument("--pooling_class", default=None, type=str)
    #parser.add_argument("--n_pixels", default=None, type=int)
    parser.add_argument("--depth", default=None, type=int)
    parser.add_argument("--laplacian_type", default=None, type=str)
    parser.add_argument("--time_lag", default=None, type=int)
    parser.add_argument("--time_length", default=None, type=int)
    

    parser.add_argument("--type", default=None, type=str)
    parser.add_argument("--sequence_length", default=None, type=int)
    parser.add_argument("--prediction_shift", default=None, type=int)

    parser.add_argument("--partition", default=None, nargs="+")
    parser.add_argument("--loss_weight", default = None, nargs="+")
    parser.add_argument("--batch_size", default=None, type=int)
    parser.add_argument("--learning_rate", default=None, type=float)
    parser.add_argument("--n_epochs", default=None, type=int)
    parser.add_argument("--kernel_size", default=None, type=int)

    parser.add_argument("--input_file", default=None, type=str)
    parser.add_argument("--output_file", default=None, type=str)
    parser.add_argument("--mean_file", default=None, type=str)
    parser.add_argument("--std_file", default=None, type=str)
    parser.add_argument("--pe_err", default=None, type=str)
    parser.add_argument("--pe_std", default=None, type=str)
    parser.add_argument("--ps_err", default=None, type=str)
    parser.add_argument("--ps_std", default=None, type=str)
    #parser.add_argument("--model_file", default=None, type=str)
    parser.add_argument("--output_path", default="output_sunet", type=str)
    parser.add_argument("--input_vars", default=None, nargs="+")
    parser.add_argument("--output_vars", default=None, nargs="+")
    parser.add_argument("--loss_vars", default=None, nargs="+")
    parser.add_argument("--meanstd_vars", default=None, nargs="+")
    parser.add_argument("--generation_only", default=False, type=bool)


    parser.add_argument("--earlystopping_patience", default=None, type=int)

    parser.add_argument("--gpu", dest="device", nargs="*")
    parser.add_argument("--seed", default=7, type=int)

    return parser


def parse_config(parser):
    """Takes the yaml file given through the command line
    Adds all the yaml file parameters, unless they have already been defined in the command line.
    Checks all values have been set else raises a Value error.
    Args:
        parser (argparse.parser): parser to be updated by the yaml file parameters
    Raises:
        ValueError: All fields must be set in the yaml config file or in the command line. Raises error if value is None (was not set).
    Returns:
        dict: parsed args of the parser
    """
    args = parser.parse_args()
    arg_dict = args.__dict__
    if args.config_file:
        data = yaml.load(args.config_file, Loader=yaml.FullLoader)
        delattr(args, "config_file")
        arg_dict = args.__dict__
        for key, value in data.items():
            # add only those not specified by the user through command line
            if isinstance(value, dict):
                for tag, element in value.items():
                    if arg_dict[tag] is None:
                        arg_dict[tag] = element

            else:
                if arg_dict[key] is None:
                    arg_dict[key] = value
    for key, value in arg_dict.items():
        if key!="meanstd_vars" and key != "device" and key != "type" and key != "sequence_length" and key != "prediction_shift" and key != "mean_file" and key!="std_file"  and arg_dict[key] is None:
            raise ValueError("The value of {} is set to None. Please define it in the config yaml file or in the command line.".format(key))
    return args
