import importlib
import argparse
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


def get_rec_exp_scores(user_args, user_id):

    parser = argparse.ArgumentParser()
    """
    # config 객체 쓰지말고 그냥 여기서 끝내야될듯
    lr, batch_size, hidden_dim? explainer모델마다 필요한거 정리해야됨
        """
    parser.add_argument("--model", type=str, default=None,
                        help="Specifies the name of the explainer model.")
    parser.add_argument("--recommender", type=str, default=None,
                        help="Specifies the name of the recommender file.")

    parser.add_argument("--optim", type=str, default="Adam",
                        help="Specifies the name of the optimizer; defaults to 'Adam'.")
    parser.add_argument("--lr", type=float, default=0.001,
                        help="Sets the learning rate.")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Defines the number of epochs for training.")
    parser.add_argument("--hidden_size", type=int, default=64,
                        help="Defines the hidden size of model.")
    parser.add_argument("--train_batch_size", type=int,
                        default=64, help="Sets the batch size for training.")
    parser.add_argument("--checkpoint", type=str, default=None,
                        help="Specifies the path for saving the training checkpoint.")
    parser.add_argument("--weight_decay", type=float,
                        default=0.0, help="Sets the weight decay factor.")

    parser.add_argument("--loss_function", type=str, default="MSE",
                        help="Defines the loss function to be used.")
    parser.add_argument("--device", type=str, choices=[
                        'cuda', 'cpu'], default="cpu", help="Sets the device for training (either 'cuda' or 'cpu').")
    parser.add_argument("--enable_scaler", action='store_true',
                        help="Enables the gradient scaler for mixed precision training.")
    parser.add_argument("--enable_amp", action='store_true',
                        help="Enables automatic mixed precision (AMP) training.")

    parser.add_argument("--eval_batch_size", type=int,
                        default=64, help="Sets the batch size for evaluation.")
    parser.add_argument("--eval_step", type=int, default=1,
                        help="Specifies the epoch interval for conducting evaluations.")
    parser.add_argument("--valid_metric", type=str, default="loss",
                        help="Specifies the validation metric to be used.")
    parser.add_argument("--valid_metric_bigger", action='store_true',
                        help="Determines whether a larger validation metric indicates better performance.")

    parser.add_argument("--checkpoint_dir", type=str, default="saved",
                        help="Specifies the directory where checkpoints are saved.")
    parser.add_argument("--save_model", action='store_true',
                        help="Determines whether to save the model.")
    args, _ = parser.parse_known_args()

    args_dict = vars(args)
    for key in user_args.keys():
        args_dict[key] = user_args[key]

    args = argparse.Namespace(**args_dict)
    config = vars(args)

    global df_ready, dataset_name, file_path, items_df
    model_name = args.model
    recommender = args.recommender

    recommender_config, recommender, dataset, train_data, valid_data, test_data = load_data_and_recommender(
        recommender)

    init_seed(recommender_config["seed"],
              recommender_config["reproducibility"])

    if model_name == "LXR":
        config['num_items'] = train_data.dataset.item_num
    trainer = getattr(importlib.import_module("xbole.trainer"),
                      model_name + "_Trainer")(config, model_name, recommender)

    # imageURL:token	item_id::token	categories:token	title:token	price:token	brand:token
    if not df_ready:
        dataset_name = recommender_config['data_path'].split('/')[-1]
        file_path = f'dataset/{dataset_name}/{dataset_name}.item'
        items_df = pd.read_csv(file_path, sep='\t', names=[
                               'imageURL', 'item_id', 'categories', 'title', 'price', 'brand'])
        df_ready = True

    user_interaction_raw = get_user_interaction(test_data, 19)
    user_interaction = user_interaction_raw[1][user_interaction_raw[0] == 0]

    for interaction in train_data:
        user_info = interaction

        rec_scores = trainer.model.recommender.full_sort_predict(user_info)
        explanation_scores = trainer.model.explain(user_info)

    user_rec_scores = rec_scores[user_id]
    explanation_scores = explanation_scores[user_id]

    return user_rec_scores, explanation_scores, user_interaction, items_df
