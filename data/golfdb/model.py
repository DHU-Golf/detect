import torch
import torch.nn as nn
from torch.autograd import Variable

import project_config as cf
from .MobileNetV2 import MobileNetV2
from .CBAM_blocks import CBAM



class EventDetector(nn.Module):
    def __init__(self, pretrain, width_mult, lstm_layers, lstm_hidden, bidirectional=True, dropout=True):
        super(EventDetector, self).__init__()
        self.width_mult = width_mult
        self.lstm_layers = lstm_layers
        self.lstm_hidden = lstm_hidden
        self.bidirectional = bidirectional
        self.dropout = dropout

        net = MobileNetV2(width_mult=width_mult)
        state_dict_mobilenet = torch.load(f'{cf.PROJECT_ROOT}data/golfdb/mobilenet_v2.pth.tar')
        if pretrain:
            net.load_state_dict(state_dict_mobilenet)

        # self.cnn = nn.Sequential(*list(net.children())[0][:19])
        self.cnn0 = list(net.children())[0][0]
        self.cnn1 = list(net.children())[0][1]
        self.cnn2 = list(net.children())[0][2:4]
        self.cnn3 = list(net.children())[0][4:7]
        self.cnn4 = list(net.children())[0][7:11]
        self.cnn5 = list(net.children())[0][11:14]
        self.cnn6 = list(net.children())[0][14:17]
        self.cnn7 = list(net.children())[0][17]
        self.cnn8 = list(net.children())[0][18]

        # 参数确定 from Moblie Net V2
        # self.atn0 = CBAM(32).cuda()
        # self.atn7 = CBAM(320).cuda()
        # self.atn8 = CBAM(1280).cuda()

        self.atn0 = CBAM(32)
        self.atn7 = CBAM(320)
        self.atn8 = CBAM(1280)

        self.rnn = nn.LSTM(int(1280 * width_mult if width_mult > 1.0 else 1280),
                           self.lstm_hidden, self.lstm_layers,
                           batch_first=True, bidirectional=bidirectional)
        if self.bidirectional:
            self.lin = nn.Linear(2 * self.lstm_hidden, 9)
        else:
            self.lin = nn.Linear(self.lstm_hidden, 9)
        if self.dropout:
            self.drop = nn.Dropout(0.5)

    def init_hidden(self, batch_size):
        # if self.bidirectional:
        #     return (
        #     Variable(torch.zeros(2 * self.lstm_layers, batch_size, self.lstm_hidden).cuda(), requires_grad=True),
        #     Variable(torch.zeros(2 * self.lstm_layers, batch_size, self.lstm_hidden).cuda(), requires_grad=True))
        # else:
        #     return (Variable(torch.zeros(self.lstm_layers, batch_size, self.lstm_hidden).cuda(), requires_grad=True),
        #             Variable(torch.zeros(self.lstm_layers, batch_size, self.lstm_hidden).cuda(), requires_grad=True))
        if self.bidirectional:
            return (
                Variable(torch.zeros(2 * self.lstm_layers, batch_size, self.lstm_hidden), requires_grad=True),
                Variable(torch.zeros(2 * self.lstm_layers, batch_size, self.lstm_hidden), requires_grad=True))
        else:
            return (Variable(torch.zeros(self.lstm_layers, batch_size, self.lstm_hidden), requires_grad=True),
                    Variable(torch.zeros(self.lstm_layers, batch_size, self.lstm_hidden), requires_grad=True))

    def forward(self, x, lengths=None):
        batch_size, timesteps, C, H, W = x.size()
        self.hidden = self.init_hidden(batch_size)

        # CNN forward
        c_in = x.view(batch_size * timesteps, C, H, W)
        # c_out = self.cnn(c_in)

        c_out = self.cnn0(c_in)
        c_out = self.atn0(c_out)
        c_out = self.cnn1(c_out)
        c_out = self.cnn2(c_out)
        c_out = self.cnn3(c_out)
        c_out = self.cnn4(c_out)
        c_out = self.cnn5(c_out)
        c_out = self.cnn6(c_out)
        c_out = self.cnn7(c_out)
        c_out = self.atn7(c_out)
        c_out = self.cnn8(c_out)
        c_out = self.atn8(c_out)

        c_out = c_out.mean(3).mean(2)
        if self.dropout:
            c_out = self.drop(c_out)

        # LSTM forward
        r_in = c_out.view(batch_size, timesteps, -1)
        r_out, states = self.rnn(r_in, self.hidden)
        out = self.lin(r_out)
        out = out.view(batch_size * timesteps, 9)

        return out
