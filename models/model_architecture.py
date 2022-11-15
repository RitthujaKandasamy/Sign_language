import torch.nn as nn
import torch.nn.functional as F
import torch



n_features = 42
hidden_size = [128, 64, 32, 16]
n_classes = 20


class MLP(nn.Module):
    def __init__(self, n_features, n_classes, hidden_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(n_features, hidden_size[0])
        self.fc2 = nn.Linear(hidden_size[0], hidden_size[1])
        self.fc3 = nn.Linear(hidden_size[1], hidden_size[2])
        self.fc4 = nn.Linear(hidden_size[2], hidden_size[3])
        self.output = nn.Linear(hidden_size[3], n_classes)

        # Define proportion or neurons to dropout
        self.dropout = nn.Dropout(0.25)

        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.tanh(self.fc2(x))
        x = self.dropout(x)
        x = torch.tanh(self.fc3(x))
        x = self.dropout(x)
        x = F.relu(self.fc4(x))
        #x = self.dropout(x)

        return F.softmax(self.output(x), dim = 1)



model = MLP(n_features, n_classes, hidden_size)