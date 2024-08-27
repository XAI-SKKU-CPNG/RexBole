import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recbole.quick_start import run_recbole, load_data_and_model

config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
    model_file="saved/BPR-Aug-13-2024_15-47-15.pth",
)

print(config)
print(model)
print(dataset)
print(train_data)
print(valid_data)
print(test_data)

