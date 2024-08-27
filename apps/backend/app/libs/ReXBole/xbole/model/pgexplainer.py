import torch
import torch.nn as nn
import torch.nn.functional as F
# from codes.forgraph.graph_config_torch import args

class PG_Explainer(nn.Module):
    """
    args 필요한것들
    -coff_size
    -coff_ent
    -hiddensize(이건 모델이랑 동일해야할거같은데)
    
    """
    def __init__(self, model, nodesize):
        super(PG_Explainer, self).__init__()
        hiddensize = 25
        self.elayers = nn.Sequential(
            nn.Linear(hiddensize * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.ReLU()
        )
        self.model = model
        self.nodesize = nodesize
        self.diag_mask = torch.ones(nodesize, nodesize) - torch.eye(nodesize)

        rc = torch.arange(nodesize).unsqueeze(0).repeat(nodesize, 1)
        self.row = rc.transpose(0, 1).reshape(-1)
        self.col = rc.reshape(-1)
        self.mask_act = 'sigmoid'

        self._initialize_weights()

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.uniform_(m.weight, a=-0.0001, b=0.0001)
                nn.init.constant_(m.bias, 0)

    def concrete_sample(self, log_alpha, beta=1.0, training=True):
        if training:
            bias = 0.0  # Adjust bias as needed
            random_noise = torch.rand(log_alpha.shape, device=log_alpha.device) * (1.0 - 2 * bias) + bias
            gate_inputs = torch.log(random_noise) - torch.log(1.0 - random_noise)
            gate_inputs = (gate_inputs + log_alpha) / beta
            gate_inputs = torch.sigmoid(gate_inputs)
        else:
            gate_inputs = torch.sigmoid(log_alpha)
        return gate_inputs

    def forward(self, inputs, training=None):
        x, embed, adj, tmp, label = inputs

        # print(label)
        self.label = torch.argmax(label.float(), dim=-1)
        self.tmp = tmp
        
        # self.row.shape = [625] = [[0,24]*625]
        # self.col.shape = [625] = [[0,24]*625]
        # embed.shape = [25,25], 각 노드에 대한 embedding, hidden dim 25인듯?
        f1 = embed[self.row]
        f2 = embed[self.col]
        
        f12self = torch.cat([f1, f2], dim=-1)
        
        h = f12self.requires_grad_(True)
        h = self.elayers(h)
        self.h = h

        self.values = h.view(-1)
        values = self.concrete_sample(self.values, beta=tmp, training=training)
        indices = torch.stack([self.row, self.col], dim=0).to(values.device)
        sparsemask = torch.sparse_coo_tensor(indices, values, torch.Size([self.nodesize, self.nodesize])).to_dense()
        sym_mask = sparsemask.to_dense()
        self.mask = sym_mask


        sym_mask = (sym_mask + sym_mask.transpose(0, 1)) / 2
        masked_adj = adj * sym_mask.to(adj.device)
        self.masked_adj = masked_adj
        x = x.unsqueeze(0)
        adj = self.masked_adj.unsqueeze(0)

        # with torch.no_grad():
        output = self.model((x, adj))
        res = F.softmax(output, dim=-1)
        return res

    def loss(self, pred, pred_label):
        pred_reduce = pred[0]
        gt_label_node = self.label
        logit = pred_reduce[gt_label_node]
        pred_loss = -torch.log(logit)
        mask = self.mask
        if self.mask_act == "sigmoid":
            mask = torch.sigmoid(self.mask)
        elif self.mask_act == "ReLU":
            mask = F.relu(self.mask)

        size_loss = args.coff_size * torch.sum(mask)

        mask = mask * 0.99 + 0.005
        mask_ent = -mask * torch.log(mask) - (1.0 - mask) * torch.log(1.0 - mask)
        mask_ent_loss = args.coff_ent * torch.mean(mask_ent)

        loss = pred_loss + size_loss + mask_ent_loss
        return loss


