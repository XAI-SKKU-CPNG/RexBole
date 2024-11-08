
import importlib

from recbole.utils import (
    init_seed
)
from recbole.quick_start import load_data_and_model
import pandas as pd

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

    # trainer.train(train_data, valid_data)



    # -----------
    dataset_name = recommender_config['data_path'].split('/')[-1]
    
    file_path = f'dataset/{dataset_name}/{dataset_name}.item'
    items_df = pd.read_csv(file_path, sep='\t', names=['item_id', 'movie_title', 'release_year', 'class'])
    result = items_df[items_df['item_id'] == '2']
    
    for interaction in test_data:
        user_info = interaction[0]

        rec_scores = trainer.model.recommender.full_sort_predict(user_info)
        print(rec_scores.shape)
        explanation_scores = trainer.model.explain(user_info)
        print(explanation_scores.shape)
        print('---')

        
    # for interaction in train_data:
    #     user_info = interaction

    #     rec_scores = trainer.model.recommender.full_sort_predict(user_info)
    #     print(rec_scores.shape)
    #     explanation_scores = trainer.model.explain(user_info)
    #     print(explanation_scores.shape)
    #     print('---')
    exit()


def load_data_and_recommender(recommender):
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file=f'saved/{recommender}',
    )
    return config, model, dataset, train_data, valid_data, test_data