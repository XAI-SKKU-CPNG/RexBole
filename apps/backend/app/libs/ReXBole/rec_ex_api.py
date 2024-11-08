import importlib
import pandas as pd
from xbole.quick_start import load_data_and_recommender
from recbole.utils import (
    init_seed
)

df_ready = False
dataset_name = None
file_path = None
items_df = None

def get_user_interaction(data, user_id):
    for interaction in data:
        user_ids = interaction[0]['user_id']
        for userid in user_ids:
            if userid == user_id:
                return interaction[1]


def get_rec_exp_scores(args, user_id):
    global df_ready, dataset_name, file_path, items_df
    model_name = args.model
    recommender = args.recommender

    recommender_config, recommender, dataset, train_data, valid_data, test_data = load_data_and_recommender(recommender)

    init_seed(recommender_config["seed"], recommender_config["reproducibility"])
    

    config = vars(args)


    if model_name == "LXR":
        config['num_items'] = train_data.dataset.item_num 
    trainer = getattr(importlib.import_module("xbole.trainer"), model_name + "_Trainer")(config, model_name, recommender)


    if not df_ready:
        dataset_name = recommender_config['data_path'].split('/')[-1]
        file_path = f'dataset/{dataset_name}/{dataset_name}.item'
        items_df = pd.read_csv(file_path, sep='\t', names=['item_id', 'movie_title', 'release_year', 'class'])
        df_ready = True
    
    user_interaction_raw = get_user_interaction(test_data, 3)
    user_interaction = user_interaction_raw[1][user_interaction_raw[0]==1]
    
    
    for interaction in train_data:
        user_info = interaction

        rec_scores = trainer.model.recommender.full_sort_predict(user_info)
        explanation_scores = trainer.model.explain(user_info)
    
    user_rec_scores = rec_scores[user_id]
    explanation_scores = explanation_scores[user_id]

    # print(user_rec_scores.shape)
    # print(explanation_scores.shape)
    # print(user_interaction)
    # exit()
    return user_rec_scores, explanation_scores, user_interaction, items_df
