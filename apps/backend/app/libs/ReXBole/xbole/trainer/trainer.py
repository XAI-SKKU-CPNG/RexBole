import os
from time import time
import importlib

import torch
import torch.nn as nn
import torch.optim
import torch.cuda.amp as amp
import numpy as np

from tqdm import tqdm

from recbole.utils import (
    ensure_dir,
    get_local_time,
    # early_stopping,
    # calculate_valid_score,
    # dict2str,
    # EvaluatorType,
    # KGDataLoaderState,
    # get_tensorboard,
    # set_color,
    # get_gpu_usage,
    # WandbLogger,
)

class AbstractTrainer(object):
    def __init__(self, config, model_name, recommender):
        """_summary_

        Args:
            model_name (str): 그냥 이름임 모델아님 어차피 모델마다 trainer도 달라서 의미없긴한데
            recommender (nn.Module): 이건 ㄹㅇ모델 학습 되어있는거고 학습할때 가중치 안변하는지 확인해봐야됨
        """
        self.config = config
        self.model_name = model_name
        self.recommender = recommender
    
    def load_explainer(self):
        """
        Load explainer and save as self.model
        """
        
        raise NotImplementedError
    def train(self, train_data):
        """
        """
        raise NotImplementedError
    
    def evaluate(self, eval_data):
        """
        """
        raise NotImplementedError


class LXR_Trainer(AbstractTrainer):
    def __init__(self, config, model_name, recommender):
        super(LXR_Trainer, self).__init__(config, model_name, recommender)

        self.optim = config["optim"] # optimizer
        self.lr = config["lr"]
        self.epochs = config['epochs']
        self.train_batch_size = config['train_batch_size']
        self.checkpoint = config["checkpoint"] # 모델 파일명, 아직 불러오는 로직은 구현안함
        self.weight_decay = config["weight_decay"]
        self.loss = config["loss_function"]

        self.device = torch.device("cuda" if torch.cuda.is_available() and config["device"] == "cuda" else "cpu")
        self.enable_scaler = torch.cuda.is_available() and config["enable_scaler"] and self.device =="cuda"
        self.enable_amp = config["enable_amp"]

        self.eval_batch_size = config['eval_batch_size']
        self.eval_step = min(config["eval_step"], self.epochs) # evaluate 할 epoch 주기, -1이면 eval disabled
        self.valid_metric = config["valid_metric"].lower()
        self.best_valid_score = -np.inf if config['valid_metric_bigger'] else np.inf

        self.checkpoint_dir = config["checkpoint_dir"] # default to "saved"
        ensure_dir(self.checkpoint_dir)
        saved_model_file = "{}-{}.pth".format(self.config["model"], get_local_time())
        self.saved_model_file = os.path.join(self.checkpoint_dir, saved_model_file)
        self.save_model = config['save_model'] # t/f, 모델 저장할지 안할지

        self.model = self._load_explainer()
        self.set_device()
        self.optimizer = self._build_optimizer()
        self.loss_function = self._build_loss()

    def set_device(self):
        """
        move models to self.device
        """
        self.model = self.model.to(self.device)
        self.model.recommender.device = self.device
        self.model.recommender = self.model.recommender.to(self.device)

    def _load_explainer(self):
        """
        load LXR
        """
        user_size = self.config['num_items']
        item_size = self.config['num_items']
        hidden_size = self.config['hidden_size']
        model = getattr(importlib.import_module("xbole.model"), self.model_name + "_Explainer")(self.recommender, user_size, item_size, hidden_size)
        return model

    def _build_optimizer(self, **kwargs):
        r"""Init the Optimizer

        """
        params = [param for name, param in self.model.named_parameters() if 'recommender' not in name]
        optim = kwargs.pop("optim", self.optim)
        learning_rate = kwargs.pop("lr", self.lr)
        weight_decay = kwargs.pop("weight_decay", self.weight_decay)

        if optim.lower() == "adam":
            optimizer = torch.optim.Adam(params, lr=learning_rate, weight_decay=weight_decay)
        elif optim.lower() == "adamw":
            optimizer = torch.optim.AdamW(params, lr=learning_rate, weight_decay=weight_decay)
        elif optim.lower() == "sgd":
            optimizer = torch.optim.SGD(params, lr=learning_rate, weight_decay=weight_decay)
        elif optim.lower() == "adagrad":
            optimizer = torch.optim.Adagrad(
                params, lr=learning_rate, weight_decay=weight_decay
            )
        elif optim.lower() == "rmsprop":
            optimizer = torch.optim.RMSprop(
                params, lr=learning_rate, weight_decay=weight_decay
            )
        elif optim.lower() == "sparse_adam":
            optimizer = torch.optim.SparseAdam(params, lr=learning_rate)
        else:
            optimizer = torch.optim.Adam(params, lr=learning_rate)
        return optimizer

    def _build_loss(self, **kwargs):
        loss_func = self.loss
        loss_func = loss_func.lower() 
        loss_function = None

        if loss_func == 'mse':
            loss_function = nn.MSELoss()
        elif loss_func == 'crossentropy' or loss_func == 'ce':
            loss_function = nn.CrossEntropyLoss()
        elif loss_func == 'bce':
            loss_function = nn.BCELoss()
        elif loss_func == 'bcewithlogits':
            loss_function = nn.BCEWithLogitsLoss()
        elif loss_func == 'kldiv':
            loss_function = nn.KLDivLoss(reduction='batchmean')
        elif loss_func == 'hinge':
            loss_function = nn.HingeEmbeddingLoss()
        elif loss_func == 'margin':
            loss_function = nn.MarginRankingLoss()
        elif loss_func == 'softmargin':
            loss_function = nn.SoftMarginLoss()
        elif loss_func == 'multilabelsoftmargin':
            loss_function = nn.MultiLabelSoftMarginLoss()
        elif loss_func == 'cosine':
            loss_function = nn.CosineEmbeddingLoss()
        else:
            # default로 mse라는거 logging으로 알려줘야될거같은데
            loss_function = nn.MSELoss()

        return loss_function

    def _train_epoch(self, train_data, epoch, loss_function):
        r"""Train the model in an epoch
        """
        self.model.train()
        loss_func = self.model.calculate_loss
        scaler = amp.GradScaler(enabled=self.enable_scaler)

        total_loss = 0.0
        self.optimizer.zero_grad()
        for batch_idx, interaction in enumerate(train_data):
            interaction = interaction.to(self.device)
            with torch.autocast(device_type=self.device.type, enabled=self.enable_amp):
                loss = loss_func(interaction, loss_function)
            
            total_loss += loss.item()
            self._check_nan(loss)
            scaler.scale(loss).backward()
            scaler.step(self.optimizer)
            scaler.update()
        return total_loss

    def train(self, train_data, eval_data):
        """
        """
        for epoch in range(1, self.epochs + 1):
            training_start_time = time()
            train_loss = self._train_epoch(
                train_data, epoch, self.loss_function
            )
            training_end_time = time()
            print("time : ",  training_end_time-training_start_time, "train_loss : ", train_loss)

            # loss관련 로깅 추가

            if self.eval_step > 0 and ((epoch+1) % self.eval_step == 0):
                eval_start_time = time()
                self.evaluate(eval_data)
                eval_end_time = time()
                # best 나올때마다 save?
                self._save_checkpoint(epoch)
            
    @torch.no_grad()
    def evaluate(self, eval_data, model_file=None):
        """
        metric이 fidelity랑 loss랑..뭐가있지
        일단은 loss만

        Args:
            eval_data (DataLoader): ㄷㅇㅌ
            model_file (str, optional): If set, it loads saved model_file
                                        otherwise evaluate the current self.model
        """
        self.model.eval()
        total_loss = 0.0
        total_samples = 0

        for batch_idx, interaction in enumerate(eval_data):
            print(interaction)
            interaction = interaction.to(self.device)
            loss = self.model.calculate_loss(interaction, self.loss_function)
            total_loss += loss.item() * interaction.size(0)
            total_samples += interaction.size(0)
        average_loss = total_loss / total_samples
        return average_loss

    def _check_nan(self, loss):
        if torch.isnan(loss):
            raise ValueError("Training loss is nan")

    def _save_checkpoint(self, epoch, verbose=True, **kwargs):
        r"""
        config, epoch, best_valid_score, state_dict(explainer), optimizer
        recommender는 그냥 모델 이름만 저장해놓으면 되고
        """
        saved_model_file = self.saved_model_file
        state = {
            "config": self.config,
            "epoch": epoch,
            "best_valid_score": self.best_valid_score,
            "state_dict": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "recommender": self.config['recommender']
        }
        torch.save(state, saved_model_file)