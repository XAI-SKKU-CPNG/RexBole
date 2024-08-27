import torch
import torch.nn as nn

from xbole.model.abstract_explainer import AbstractExplainer, AbstractAdapter

# 원본
class LXR_Explainer_old(nn.Module):
    """Trainer optimizer에 LXR_Explainer의 파라미터만 전달해줘야되는거 실수하면 안됨

    Args:
        nn (_type_): _description_
        user_size : recommender의 hidden size(user embedding)
        item_size : # of items in the dataset
        
    Returns:
        expl_score: [B, num_items], 각 item에 대한 mask 점수 
    """
    def __init__(self, user_size, item_size, hidden_size):
        super(LXR_Explainer_old, self).__init__()
        
        self.users_fc = nn.Linear(in_features = user_size, out_features=hidden_size)
        self.items_fc = nn.Linear(in_features = item_size, out_features=hidden_size)
        self.bottleneck = nn.Sequential(
            nn.Tanh(),
            nn.Linear(in_features = hidden_size*2, out_features=hidden_size),
            nn.Tanh(),
            nn.Linear(in_features = hidden_size, out_features=item_size),
            nn.Sigmoid()
        )
        
        
    def forward(self, user_tensor, item_tensor):
        user_output = self.users_fc(user_tensor.float())
        item_output = self.items_fc(item_tensor.float())
        combined_output = torch.cat((user_output, item_output), dim=-1)
        expl_scores = self.bottleneck(combined_output)
        return expl_scores


class LXR_Explainer(AbstractExplainer):
    """Trainer optimizer에 LXR_Explainer의 파라미터만 전달해줘야되는거 실수하면 안됨

    Args:
        nn (_type_): _description_
        user_size : recommender의 hidden size(user embedding)
        item_size : # of items in the dataset
        
    Returns:
        expl_score: [B, num_items], 각 item에 대한 mask 점수 
    """
    def __init__(self, recommender, user_size, item_size, hidden_size):
        super(LXR_Explainer, self).__init__(recommender)
        
        self.users_fc = nn.Linear(in_features = user_size, out_features=hidden_size)
        self.rec_fc = nn.Linear(in_features = item_size, out_features=hidden_size)
        self.bottleneck = nn.Sequential(
            nn.Tanh(),
            nn.Linear(in_features = hidden_size*2, out_features=hidden_size),
            nn.Tanh(),
            nn.Linear(in_features = hidden_size, out_features=item_size),
            nn.Sigmoid()
        )

        # config나 args받아서 동적으로
        # self.loss_function = nn.MSELoss()

        self.prepare_recommender(recommender)

    def calculate_loss(self, interaction, loss_function):
        """
        """
        # with torch.no_grad():
        original_rec = self.recommender.full_sort_predict(interaction)
        user_tensor = self.recommender.get_user_embed(interaction)
        
        mask = self.forward(user_tensor, original_rec)
        masked_rec = self.recommender.full_sort_predict(interaction, mask)
        loss = loss_function(masked_rec, original_rec)
        return loss

    @torch.no_grad()
    def explain(self, interaction):
        """
        """
        original_rec = self.recommender.full_sort_predict(interaction)
        user_tensor = self.recommender.get_user_embed(interaction)
        expl_scores = self.forward(user_tensor, original_rec)
        return expl_scores
        
    def prepare_recommender(self, recommender):
        """
        """
        self.adapter = CDAE_to_LXR()
        self.recommender = self.adapter(recommender)
        
    def forward(self, user_tensor, item_tensor):
        """derive mask
        """
        user_output = self.users_fc(user_tensor.float())
        rec_output = self.rec_fc(item_tensor.float())
        combined_output = torch.cat((user_output, rec_output), dim=-1)
        expl_scores = self.bottleneck(combined_output)
        return expl_scores



class CDAE_to_LXR(AbstractAdapter):
    """
    explainer에 있는 recommender를 수정해야함...
    이 아니고 애초에 수정된 recommender를 반환하게 하는게 맞는거같은데
    """
    def __init__(self):
        super(CDAE_to_LXR, self).__init__()
        

    def adapt_recommender(self, recommender):
        """
        """
        # for parameter in recommender.parameters():
        #     parameter.requires_grad_(False)
        
        def masked_full_sort_predict(self, interaction, mask=None):
            users = interaction[self.USER_ID]
            items = self.get_rating_matrix(users) # [B, num_items]
            if mask is not None:
                items = items * mask # 이거 곱하기가 아니라 cartesian product가 돼야하는데..
            predict = self.forward(items, users)
            predict = self.o_act(predict)
            return predict

        def get_user_embed(self, interaction):
            """_summary_

            Args:
                interaction (_type_): _description_
            """
            users = interaction[self.USER_ID]
            user_history = self.get_rating_matrix(users)
            return user_history

        recommender.full_sort_predict = masked_full_sort_predict.__get__(recommender)
        recommender.get_user_embed = get_user_embed.__get__(recommender)
        # self.recommender.get_item_embed = get_item_embed.__get__(self.recommender)
        
        return recommender
    
