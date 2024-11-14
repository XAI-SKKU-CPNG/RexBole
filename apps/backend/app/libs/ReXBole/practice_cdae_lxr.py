from xbole.model.pgexplainer import PG_Explainer
# from recbole.model.knowledge_aware_recommender import KGCN
from xbole.model import LXR_Explainer
from recbole.quick_start import *

import torch
import torch.nn as nn

model_to_load = "saved/CDAE-Aug-17-2024_18-19-58.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# scores_tensor (Torch.Tensor): the output tensor of model with the shape of `(N, )`
# interaction(Interaction): batched eval data.
# positive_u(Torch.Tensor): the row index of positive items for each user.
#  positive_i(Torch.Tensor): the positive item id for each user.

# item_embed(rating matrix)랑 rec의 prediction을 받아서 rating matrix에 mask를..

# def __init__(self, recommender, user_size, item_size, hidden_size):
if __name__ == "__main__":
    # explainer = PG_Explainer()
    config, recommender, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_to_load)
    recommender = recommender.to(device)
    num_items = train_data.dataset.item_num
    # num_users = train_data.dataset.user_num

    # test_data.set_batch_size(64)
    explainer = LXR_Explainer(recommender, num_items,
                              num_items, 32).to(device)  # getattr
    optimizer = torch.optim.Adam([param for name, param in explainer.named_parameters(
    ) if 'recommender' not in name], lr=0.001)
    for epoch in range(1, 100):
        loss = 0.0
        sum_mask = 0.0
        optimizer.zero_grad()
        for i, data in enumerate(train_data):
            interaction = data.to(device)

            loss += explainer.calculate_loss(interaction)
        loss.backward()
        optimizer.step()
        print(f"epoch {epoch}, loss : {loss.item()}, sum_mask : {sum_mask}")
