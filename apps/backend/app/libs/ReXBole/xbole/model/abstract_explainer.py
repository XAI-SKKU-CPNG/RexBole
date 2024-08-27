import numpy as np
import torch
import torch.nn as nn

from abc import ABC, abstractmethod, abstractproperty

class AbstractExplainer(nn.Module):
    def __init__(self, recommender):
        super(AbstractExplainer, self).__init__()
        self.recommender = recommender
        

    def calculate_loss(self):
        """loss

        """
        raise NotImplementedError
    
    def explain(self):
        """실제 explain

        Returns:
            torch.Tensor: Predicted scores or subgraph, etc.
        """
        raise NotImplementedError

    def prepare_recommender(self):
        """
        adapter 쓸수있으면 쓰고 안되면 여기서 직접..
        """
        raise NotImplementedError



class AbstractAdapter(ABC):
    """
    recommender 함수를 override 해줘야됨
    """
    def __init__(self):
        super(AbstractAdapter, self).__init__()

    def adapt_recommender(self):
        """
        full_sort_predict -> masked_full_sort_predict로 override
        get_user_embed, get_item_embed 함수 추가
        """

        raise NotImplementedError
        
    def __call__(self, recommender):
        return self.adapt_recommender(recommender)