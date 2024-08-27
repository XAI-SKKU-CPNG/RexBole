
import importlib

from recbole.utils import (
    init_seed
)
from recbole.quick_start import load_data_and_model

def run_xbole(
    args
    ):
    """
    seed, dataset : recommender와 동일하게 사용
    logger는 사용하지않음
    """
    model_name = args.model
    recommender = args.recommender

    recommender_config, recommender, dataset, train_data, valid_data, test_data = load_data_and_recommender(recommender)

    init_seed(recommender_config["seed"], recommender_config["reproducibility"])
    
    config = vars(args)

    if model_name == "LXR":
        config['num_items'] = train_data.dataset.item_num 
    trainer = getattr(importlib.import_module("xbole.trainer"), model_name + "_Trainer")(config, model_name, recommender)

    trainer.train(train_data, valid_data)




def load_data_and_recommender(recommender):
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file=f'saved/{recommender}',
    )
    return config, model, dataset, train_data, valid_data, test_data