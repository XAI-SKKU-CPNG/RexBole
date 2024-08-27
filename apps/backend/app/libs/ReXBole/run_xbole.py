import argparse

from xbole.quick_start import *

if __name__ == "__main__":
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

    # model은 explainer 모델
    run_xbole(
        args
    )
