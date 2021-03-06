"""
use pretrained module
but to train a new module
"""

import random
import os
import numpy as np
import torch
from torchvision import transforms
from scipy.misc import imread
from keras.preprocessing.sequence import pad_sequences
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torch.autograd import Variable
from torchvision.utils import make_grid,save_image
from sklearn.metrics import roc_curve, auc
from scipy import spatial
import torch.nn as nn
from torch.autograd import Variable
import math
import torch.nn.functional as F
import torch.optim as optim
from torchvision.utils import make_grid,save_image
import argparse
from torch.autograd import Variable
from torch.utils.data import DataLoader
import itertools
import scipy.io as sio
from tensorboardX import SummaryWriter
from scipy.stats import itemfreq

# class CASIAB-NEW(object):
#
#     def __init__(self,
#                  train,
#                  data_root,
#                  glr_views,
#                  prb_views,
#                  sequence_len,
#                  image_width,
#                  image_height,
#                  n_train,
#                  seed=1,
#                  ):
#
#         np.random.seed(seed)
#         self.train = train
#         self.data_root = data_root
#         self.sequence_len = sequence_len
#         self.image_width = image_width
#         self.image_height = image_height
#         self.n_train = n_train
#
#         self.glr_views = glr_views
#         self.prb_views = prb_views
#
#         self.transform = transforms.Compose([
#             transforms.ToPILImage(),
#             # transforms.Pad((50, 0)),
#             transforms.Resize((image_height,image_width)),
#             transforms.ToTensor()
#         ])
#
#         subjects = list(range(1, 124 + 1))
#         self.train_subjects = subjects[:n_train]
#         self.test_subjects = subjects[n_train:]
#         # self.test_subjects = subjects[:n_train]
#         # self.train_subjects = subjects[:5]
#         # self.test_subjects = subjects[:5]
#         print('training_subjects', self.train_subjects, np.sum(self.train_subjects), len(self.train_subjects))
#         print('testing_subjects', self.test_subjects, np.sum(self.test_subjects), len(self.test_subjects))
#
#     def __getitem__(self, index):
#
#         def random_chose():
#             if self.train:
#                 si_idx = np.random.choice(self.train_subjects)
#                 label = self.train_subjects.index(si_idx)
#             else:
#                 si_idx = np.random.choice(self.test_subjects)
#                 label = self.test_subjects.index(si_idx)
#
#             cond1 = np.random.choice([1,2])
#             if cond1 == 1:
#                 senum1 = np.random.choice(list(range(1, 2 + 1)))
#             else:
#                 senum1 = np.random.choice(list(range(1, 2 + 1)))
#
#             cond2 = np.random.choice([1,2])
#             if cond2 == 1:
#                 senum2 = np.random.choice(list(range(1, 2 + 1)))
#             else:
#                 senum2 = np.random.choice(list(range(1, 2 + 1)))
#
#             # view_idx1 = np.random.choice(list(range(0, 180 + 1, 18)))
#             # view_idx2 = np.random.choice(list(range(0, 180 + 1, 18)))
#
#             view_idx1 = np.random.choice([90])
#             view_idx2 = np.random.choice([90])
#
#             return si_idx,(cond1,senum1,view_idx1),(cond2,senum2,view_idx2),label
#
#         def random_length(dirt, length):
#             files = sorted(os.listdir(dirt))
#             num = len(files)
#             # if num - length < 2:
#             #     return 0, 0, []
#             # start = np.random.randint(1, num - length)
#             start = 0
#             end = start + num
#             return start, end, files
#
#         def read_frames(video_in, start, end, files):
#             shape = [end-start, 3, self.image_height, self.image_width]
#             ims = np.zeros(shape, np.float32)
#
#             for i in range(start, end):
#                 im = imread(os.path.join(video_in, files[i]))
#                 im = self.transform(im)
#                 # im = self.img_random_color(im,ns)
#                 ims[i - start] = im
#             return ims
#
#         si_idx, param1, param2, label = random_chose()
#         video_in_nm = os.path.join(self.data_root,
#                                    '%03d-%1d-%02d-%03d' % (si_idx,
#                                                            param1[0],
#                                                            param1[1],
#                                                            param1[2]))
#         start_nm, end_nm, files_nm = random_length(video_in_nm, self.sequence_len)
#
#         video_in_cl = os.path.join(self.data_root,
#                                    '%03d-%1d-%02d-%03d' % (si_idx,
#                                                            param2[0],
#                                                            param2[1],
#                                                            param2[2]))
#         start_cl, end_cl, files_cl = random_length(video_in_cl, self.sequence_len)
#
#         # while True:
#         #     if start_nm == end_nm == 0 or start_cl == end_cl == 0:
#         #         si_idx, param1, param2, label = random_chose()
#         #         video_in_nm = os.path.join(self.data_root,
#         #                                    '%03d-%1d-%02d-%03d' % (si_idx,
#         #                                                            param1[0],
#         #                                                            param1[1],
#         #                                                            param1[2]))
#         #         start_nm, end_nm, files_nm = random_length(video_in_nm, self.sequence_len)
#         #
#         #         video_in_cl = os.path.join(self.data_root,
#         #                                    '%03d-%1d-%02d-%03d' % (si_idx,
#         #                                                            param2[0],
#         #                                                            param2[1],
#         #                                                            param2[2]))
#         #         start_cl, end_cl, files_cl = random_length(video_in_cl, self.sequence_len)
#         #     else:
#         #         break
#
#         imgs_nm = read_frames(video_in_nm, start_nm, end_nm, files_nm)
#         imgs_nm = np.transpose(imgs_nm,(1,0,2,3))
#         imgs_nm = pad_sequences(imgs_nm, maxlen=200, dtype='float32', padding='post')
#         imgs_nm = np.transpose(imgs_nm,(1,0,2,3))
#
#         imgs_cl = read_frames(video_in_cl, start_cl, end_cl, files_cl)
#         imgs_cl = np.transpose(imgs_cl, (1, 0, 2, 3))
#         imgs_cl = pad_sequences(imgs_cl, maxlen=200, dtype='float32', padding='post')
#         imgs_cl = np.transpose(imgs_cl, (1, 0, 2, 3))
#
#         TF = np.random.choice([True, False])
#         if TF:
#             imgs_mx = imgs_nm
#         else:
#             imgs_mx = imgs_cl
#
#         return imgs_nm, imgs_cl,imgs_mx, label
#
#     def get_eval_data(self,train=False):
#         test_data_glr_list = []
#         test_data_prb_list = []
#
#         def read_frames_(si, ci, sei, vi):
#             video_in = os.path.join(self.data_root, '%03d-%1d-%02d-%03d' % (si, ci, sei, vi))
#             files = sorted(os.listdir(video_in))
#             shape = [len(files), 3, self.image_height, self.image_width]
#             data = np.zeros(shape, np.float32)
#             for i in range(len(files)):
#                 try:
#                     img = imread(os.path.join(video_in, files[i]))
#                     img = self.transform(img)
#                     data[i] = img
#                 except:
#                     print('FOUND A BAD IMAGE, SKIPPED')
#             return data
#
#         if train:
#             data_type = self.train_subjects
#         else:
#             data_type = self.test_subjects
#
#         conditions = [1,2]
#         ###########################################################
#         #gallry
#         for vi in self.glr_views:
#             test_data_glr_this = []
#             for i, id in enumerate(data_type):
#                 test_data_glr_this.append(read_frames_(id, conditions[0], 1, vi))
#                 print(vi, i)
#             test_data_glr_this = pad_sequences(test_data_glr_this, maxlen=70, dtype='float32', padding='post')
#             test_data_glr_list.append(test_data_glr_this)
#
#
#         ###########################################################
#         # probe
#         for vi in self.prb_views:
#             test_data_prb_this = []
#             for i, id in enumerate(data_type):
#                 print(vi, i)
#                 test_data_prb_this.append(read_frames_(id, conditions[1], 1, vi))
#             test_data_prb_this = pad_sequences(test_data_prb_this, maxlen=70, dtype='float32', padding='post')
#             test_data_prb_list.append(test_data_prb_this)
#
#         return torch.tensor(test_data_glr_list).permute(0, 2, 1, 3, 4, 5), \
#                torch.tensor(test_data_prb_list).permute(0, 2, 1, 3, 4, 5)
#
#     def __len__(self):
#         if self.train:
#             return len(self.train_subjects)*110
#         else:
#             return len(self.test_subjects)*110

class CASIAB(object):

    def __init__(self,
                 train,
                 data_root,
                 glr_views,
                 prb_views,
                 sequence_len,
                 image_width,
                 image_height,
                 n_train,
                 seed=1,
                 ):

        np.random.seed(seed)
        self.train = train
        self.data_root = data_root
        self.sequence_len = sequence_len
        self.image_width = image_width
        self.image_height = image_height
        self.n_train = n_train

        self.glr_views = glr_views
        self.prb_views = prb_views

        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            # transforms.Pad((50, 0)),
            transforms.Resize((image_height,image_width)),
            transforms.ToTensor()
        ])

        subjects = list(range(1, 124 + 1))
        self.train_subjects = subjects[:n_train]
        self.test_subjects = subjects[n_train:]
        # self.test_subjects = subjects[:n_train]
        # self.train_subjects = subjects[:5]
        # self.test_subjects = subjects[:5]
        print('training_subjects', self.train_subjects, np.sum(self.train_subjects), len(self.train_subjects))
        print('testing_subjects', self.test_subjects, np.sum(self.test_subjects), len(self.test_subjects))

    def __getitem__(self, index):
        shape = [self.sequence_len, 3, self.image_height, self.image_width]

        def random_chose():
            if self.train:
                si_idx = np.random.choice(self.train_subjects)
                label = self.train_subjects.index(si_idx)
            else:
                si_idx = np.random.choice(self.test_subjects)
                label = self.test_subjects.index(si_idx)

            cond1 = np.random.choice([1, 2])
            if cond1 == 1:
                senum1 = np.random.choice(list(range(1, 2 + 1)))
            else:
                senum1 = np.random.choice(list(range(1, 2 + 1)))

            cond2 = np.random.choice([1, 2])
            if cond2 == 1:
                senum2 = np.random.choice(list(range(1, 2 + 1)))
            else:
                senum2 = np.random.choice(list(range(1, 2 + 1)))

            # view_idx1 = np.random.choice(list(range(0, 180 + 1, 18)))
            # view_idx2 = np.random.choice(list(range(0, 180 + 1, 18)))

            view_idx1 = np.random.choice([90])
            view_idx2 = np.random.choice([90])

            return si_idx,(cond1,senum1,view_idx1),(cond2,senum2,view_idx2),label

        def random_length(dirt, length):
            files = sorted(os.listdir(dirt))
            num = len(files)
            if num - length < 2:
                return 0, 0, []
            start = np.random.randint(1, num - length)
            end = start + length
            return start, end, files

        def read_frames(video_in, start, end, files):
            ims = np.zeros(shape, np.float32)

            for i in range(start, end):
                im = imread(os.path.join(video_in, files[i]))
                im = self.transform(im)
                # im = self.img_random_color(im,ns)
                ims[i - start] = im
            return ims

        si_idx, param1, param2, label = random_chose()
        video_in_nm = os.path.join(self.data_root,
                                   '%03d-%1d-%02d-%03d' % (si_idx,
                                                           param1[0],
                                                           param1[1],
                                                           param1[2]))
        start_nm, end_nm, files_nm = random_length(video_in_nm, self.sequence_len)

        video_in_cl = os.path.join(self.data_root,
                                   '%03d-%1d-%02d-%03d' % (si_idx,
                                                           param2[0],
                                                           param2[1],
                                                           param2[2]))
        start_cl, end_cl, files_cl = random_length(video_in_cl, self.sequence_len)

        while True:
            if start_nm == end_nm == 0 or start_cl == end_cl == 0:
                si_idx, param1, param2, label = random_chose()
                video_in_nm = os.path.join(self.data_root,
                                           '%03d-%1d-%02d-%03d' % (si_idx,
                                                                   param1[0],
                                                                   param1[1],
                                                                   param1[2]))
                start_nm, end_nm, files_nm = random_length(video_in_nm, self.sequence_len)

                video_in_cl = os.path.join(self.data_root,
                                           '%03d-%1d-%02d-%03d' % (si_idx,
                                                                   param2[0],
                                                                   param2[1],
                                                                   param2[2]))
                start_cl, end_cl, files_cl = random_length(video_in_cl, self.sequence_len)
            else:
                break

        TF = np.random.choice([True, False])
        if TF:
            video_in_mx, start_mx, end_mx, files_mx = \
                video_in_nm, start_nm, end_nm, files_nm
        else:
            video_in_mx, start_mx, end_mx, files_mx = \
                video_in_cl, start_cl, end_cl, files_cl

        imgs_nm = read_frames(video_in_nm, start_nm, end_nm, files_nm)
        imgs_cl = read_frames(video_in_cl, start_cl, end_cl, files_cl)
        imgs_mx = read_frames(video_in_mx, start_mx, end_mx, files_mx)
        return imgs_nm, imgs_cl,imgs_mx, label

    def get_eval_data(self,train=False):
        test_data_glr_list = []
        test_data_prb_list = []

        def read_frames_(si, ci, sei, vi):
            video_in = os.path.join(self.data_root, '%03d-%1d-%02d-%03d' % (si, ci, sei, vi))
            files = sorted(os.listdir(video_in))
            shape = [len(files), 3, self.image_height, self.image_width]
            data = np.zeros(shape, np.float32)
            for i in range(len(files)):
                try:
                    img = imread(os.path.join(video_in, files[i]))
                    img = self.transform(img)
                    data[i] = img
                except:
                    print('FOUND A BAD IMAGE, SKIPPED')
            return data

        if train:
            data_type = self.train_subjects
        else:
            data_type = self.test_subjects

        conditions = [1,2]
        ###########################################################
        #gallry
        for vi in self.glr_views:
            test_data_glr_this = []
            for i, id in enumerate(data_type):
                test_data_glr_this.append(read_frames_(id, conditions[0], 1, vi))
                print(vi, i)
            test_data_glr_this = pad_sequences(test_data_glr_this, maxlen=70, dtype='float32', padding='post')
            test_data_glr_list.append(test_data_glr_this)


        ###########################################################
        # probe
        for vi in self.prb_views:
            test_data_prb_this = []
            for i, id in enumerate(data_type):
                print(vi, i)
                test_data_prb_this.append(read_frames_(id, conditions[1], 1, vi))
            test_data_prb_this = pad_sequences(test_data_prb_this, maxlen=70, dtype='float32', padding='post')
            test_data_prb_list.append(test_data_prb_this)

        return torch.tensor(test_data_glr_list).permute(0, 2, 1, 3, 4, 5), \
               torch.tensor(test_data_prb_list).permute(0, 2, 1, 3, 4, 5)

    def __len__(self):
        if self.train:
            return len(self.train_subjects)*110
        else:
            return len(self.test_subjects)*110


def init_weights(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1 or classname.find('Linear') != -1:
        m.weight.data.normal_(0.0, 0.02)
        m.bias.data.fill_(0)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

def process_confusion_matrix(matrix,n_class,n_sample):
    matrix = np.reshape(matrix,(n_class*n_class*n_sample))
    def make_labels():
        matrix = [np.eye(n_class, n_class)[j] for j in range(n_class) for _ in range(n_sample)]
        return np.concatenate(matrix)
    labels = make_labels()
    labels = np.reshape(labels,(n_class*n_class*n_sample))
    fpr, tpr, _ = roc_curve(labels,matrix)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr,roc_auc

def plot_roc(fpr,tpr,roc_auc):
    plt.figure()
    lw = 3
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.01])
    plt.xlabel('False Alarm Rate/ False Positive Rate')
    plt.ylabel('True Accept Rate/ True Positive Rate')
    plt.title('ROC')
    plt.legend(loc="lower right")
    plt.show()

def find_idx(fpr,tpr,threthold=[0.01,0.05,0.1],ifround=True):
    outptut = []
    for i in threthold:
        item = fpr[fpr<i+0.005].max()
        idx = np.where(fpr==item)
        val = tpr[idx][-1]
        if ifround:
            val = round(val,2)
        outptut.append(val)
    return outptut

def calculate_cosine_similarity(a, b):
    score = 1 - spatial.distance.cosine(a, b)
    return score

def calculate_cosine_similarity_multidim(a, b):
    score = 0
    for i in range(len(a)):
        score += spatial.distance.cosine(a[i], b[i])
    return score/len(a)

def calculate_identication_rate_single(glrs,aprb,trueid,rank=1):
    scores = []
    for i in glrs:
        scores.append(calculate_cosine_similarity(i,aprb))
    max_val = max(scores)
    max_idx = scores.index(max_val)

    right,predicted = trueid,max_idx
    print(right,predicted )


    if max_idx in trueid:
        return 1,[right,predicted]
    else:
        return 0,[right,predicted]

def adjust_white_balance(x):

    avgR = np.average(x[0,:,:])
    avgG = np.average(x[1,:,:])
    avgB = np.average(x[2,:,:])

    avg = (avgB + avgG + avgR) / 3

    x[0,:,:] = np.minimum(x[0] * (avg / avgR), 1)
    x[1,:,:] = np.minimum(x[1] * (avg / avgG), 1)
    x[2,:,:] = np.minimum(x[2] * (avg / avgB), 1)

    return x

def adjust_(x):
    x = transforms.functional.adjust_brightness(x, 1.5)
    x = transforms.functional.adjust_contrast(x, 1.5)
    return x
#################################################################################################################

class vgg_layer(nn.Module):
    def __init__(self, nin, nout):
        super(vgg_layer, self).__init__()
        self.main = nn.Sequential(
                nn.Conv2d(nin, nout, 3, 1, 1),
                nn.BatchNorm2d(nout),
                nn.LeakyReLU(0.2)
                )

    def forward(self, input):
        return self.main(input)
class dcgan_conv(nn.Module):
    def __init__(self, nin, nout):
        super(dcgan_conv, self).__init__()
        self.main = nn.Sequential(
                nn.Conv2d(nin, nout, 4, 2, 1),
                nn.BatchNorm2d(nout),
                nn.LeakyReLU(0.2),
                )

    def forward(self, input):
        return self.main(input)
class dcgan_upconv(nn.Module):
    def __init__(self, nin, nout):
        super(dcgan_upconv, self).__init__()
        self.main = nn.Sequential(
                nn.ConvTranspose2d(nin, nout, 4, 2, 1,),
                nn.BatchNorm2d(nout),
                nn.LeakyReLU(0.2),
                )

    def forward(self, input):
        return self.main(input)
class encoder(nn.Module):
    def __init__(self, nc=3):
        super(encoder, self).__init__()
        self.em_dim = opt.em_dim
        nf = 64
        self.main = nn.Sequential(
            dcgan_conv(nc, nf),
            vgg_layer(nf, nf),

            dcgan_conv(nf, nf * 2),
            vgg_layer(nf * 2, nf * 2),

            dcgan_conv(nf * 2, nf * 4),
            vgg_layer(nf * 4, nf * 4),

            dcgan_conv(nf * 4, nf * 8),
            vgg_layer(nf * 8, nf * 8),

            vgg_layer(nf * 8, nf * 8),
            vgg_layer(nf * 8, nf * 8),

            # nn.Conv1d(nf * 8, self.em_dim, 4, 1, 0),
            # nn.BatchNorm2d(self.em_dim),
        )

        self.flatten = nn.Sequential(
            nn.Linear(nf * 8 * 2 * 4,self.em_dim),
            nn.BatchNorm1d(self.em_dim),
        )

        # self.ha_fc = nn.Sequential(
        #     nn.LeakyReLU(),
        #     nn.Linear(self.em_dim, self.em_dim // 2),
        #     nn.BatchNorm1d(self.em_dim // 2),
        #
        #     nn.LeakyReLU(),
        #     nn.Linear(self.em_dim // 2, self.em_dim // 2),
        #     nn.BatchNorm1d(self.em_dim // 2),
        #
        #     nn.LeakyReLU(),
        #     nn.Linear(self.em_dim // 2, opt.ha_dim),
        #     nn.BatchNorm1d(opt.ha_dim)
        # )

        # self.hg_fc = nn.Sequential(
        #     nn.LeakyReLU(),
        #     nn.Linear(self.em_dim, self.em_dim // 2),
        #     nn.BatchNorm1d(self.em_dim // 2),
        #
        #     nn.LeakyReLU(),
        #     nn.Linear(self.em_dim // 2, self.em_dim // 2),
        #     nn.BatchNorm1d(self.em_dim // 2),
        #
        #     nn.LeakyReLU(),
        #     nn.Linear(self.em_dim // 2, opt.hg_dim),
        #     nn.BatchNorm1d(opt.hg_dim)
        # )

    def forward(self, input):
        embedding = self.main(input).view(-1, 64 * 8 * 2 * 4)
        embedding = self.flatten(embedding)
        ha, hg = torch.split(embedding, [opt.ha_dim, opt.hg_dim], dim=1)
        return ha, hg, embedding


class decoder(nn.Module):
    def __init__(self, nc=3):
        super(decoder, self).__init__()
        nf = 64
        self.em_dim = opt.em_dim

        self.trans = nn.Sequential(
            nn.Linear(self.em_dim, nf * 8 * 2 * 4),
            nn.BatchNorm1d(nf * 8 * 2 * 4),
        )

        self.main = nn.Sequential(
            # nn.ConvTranspose2d(self.em_dim, nf * 8, 4, 1, 0),
            # nn.BatchNorm2d(nf * 8),
            nn.LeakyReLU(0.2),
            # vgg_layer(nf * 8, nf * 8),

            dcgan_upconv(nf * 8, nf * 4),
            # vgg_layer(nf * 4, nf * 4),

            dcgan_upconv(nf * 4, nf * 2),
            # vgg_layer(nf * 2, nf * 2),

            dcgan_upconv(nf * 2, nf),
            # vgg_layer(nf, nf),

            nn.ConvTranspose2d(nf, nc, 4, 2, 1),
            nn.Sigmoid()
            # because image pixels are from 0-1, 0-255
        )



    def forward(self, ha, hg):
        hidden = torch.cat([ha, hg], 1).view(-1, opt.em_dim)
        small = self.trans(hidden).view(-1, 64 * 8, 4, 2)
        img = self.main(small)
        return img

class lstm(nn.Module):
    def __init__(self, hidden_dim=128, tagset_size=74):
        super(lstm, self).__init__()
        self.source_dim = opt.hg_dim
        self.hidden_dim = hidden_dim
        self.tagset_size = tagset_size
        self.lens = 0
        self.lstm = nn.LSTM(self.source_dim, hidden_dim, 3)
        self.fc1 = nn.Sequential(
            nn.BatchNorm1d(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.LeakyReLU(0.2),

        )
        self.main = nn.Sequential(
            # nn.Dropout(),
            nn.Linear(self.hidden_dim, tagset_size),
            nn.BatchNorm1d(tagset_size),
        )
    def forward(self, batch):
        lens = batch.shape[0]
        lstm_out, _ = self.lstm(batch.view(lens,-1,self.source_dim))
        lstm_out_test = self.fc1(torch.mean(lstm_out.view(lens,-1,self.hidden_dim),0))
        lstm_out_train = self.main(lstm_out_test).view(-1, self.tagset_size)
        return lstm_out_train,lstm_out_test,lstm_out

#################################################################################################################
# HYPER PARAMETERS INITIALIZING
parser = argparse.ArgumentParser()
gpu_num = int(input('Tell me the gpu you wanna use for this experiment:'))
parser.add_argument('--gpu', type=int, default=gpu_num)
parser.add_argument('--siter', type=int, default=10800, help='number of itr to start with')
parser.add_argument('--lr', default=0.0001, type=float, help='learning rate')
parser.add_argument('--data_root',
                     default='/home/tony/Research/CASIAB-OLD-RGB-BS/',
                     help='root directory for data')
parser.add_argument('--seed', default=1, type=int, help='manual seed')
parser.add_argument('--batch_size', default=16, type=int, help='batch size')
parser.add_argument('--em_dim', type=int, default=320, help='size of the pose vector')
parser.add_argument('--ha_dim', type=int, default=288, help='size of the appearance vector')
parser.add_argument('--hg_dim', type=int, default=32, help='size of the gait vector')
parser.add_argument('--image_width', type=int, default=32, help='the width of the input image to network')
parser.add_argument('--image_height', type=int, default=64, help='the height of the input image to network')
parser.add_argument('--max_step', type=int, default=30, help='maximum distance between frames')
parser.add_argument('--data_threads', type=int, default=2, help='number of parallel data loading threads')
parser.add_argument('--normalize', action='store_true', help='if true, normalize pose vector')
parser.add_argument('--num_train',type=int, default=74, help='')
parser.add_argument('--glr_views',type=list, default=[90], help='')
parser.add_argument('--prb_views',type=list, default=[90], help='')

# import datetime
# time_now = str(datetime.datetime.now())
time_now = "alignment3"
parser.add_argument('--signature', default=time_now)
parser.add_argument('--savedir', default='./runs')
opt = parser.parse_args()
print(opt)
os.environ["CUDA_VISIBLE_DEVICES"] = str(opt.gpu)
print("Random Seed: ", opt.seed)
random.seed(opt.seed)
torch.manual_seed(opt.seed)
torch.cuda.manual_seed_all(opt.seed)
os.makedirs('%s/analogy/%s'%(opt.savedir,opt.signature), exist_ok=True)
os.makedirs('%s/modules/%s'%(opt.savedir,opt.signature), exist_ok=True)
#################################################################################################################
# MODEL PROCESS
netE_use = encoder()
netE = encoder()
netD = decoder()
lstm = lstm()
netE.apply(init_weights)
netE_use.apply(init_weights)
netD.apply(init_weights)
lstm.apply(init_weights)
if opt.siter is not 0:
    checkpoint = torch.load('%s/modules/%s/%d.pickle' % (opt.savedir,opt.signature, opt.siter))
    netE_use.load_state_dict(checkpoint['netE'])
    # netD.load_state_dict(checkpoint['netD'])
    # lstm.load_state_dict(checkpoint['lstm'])
    print('model loadinged successfully')
optimizerE = optim.Adam(netE.parameters(), lr=opt.lr, betas=(0.9, 0.999),weight_decay=0.001)
optimizerD = optim.Adam(netD.parameters(), lr=opt.lr, betas=(0.9, 0.999),weight_decay=0.001)
optimizerLstm = optim.Adam(lstm.parameters(), lr=opt.lr, betas=(0.9, 0.999),weight_decay=0.001)

# optimizerE = optim.Adam(netE.parameters(), lr=opt.lr, betas=(0.9, 0.999))
# optimizerD = optim.Adam(netD.parameters(), lr=opt.lr, betas=(0.9, 0.999))
# optimizerLstm = optim.Adam(lstm.parameters(), lr=opt.lr, betas=(0.9, 0.999))

mse_loss = nn.MSELoss()
bce_loss = nn.BCELoss()
cse_loss = nn.CrossEntropyLoss()
trp_loss = nn.TripletMarginLoss(margin=2.0)
netE.cuda()
netE_use.cuda()
netD.cuda()
lstm.cuda()
mse_loss.cuda()
bce_loss.cuda()
cse_loss.cuda()
trp_loss.cuda()

# l1_crit = nn.L1Loss(size_average=False)
# reg_loss = 0
# for param in netE.parameters():
#     reg_loss += l1_crit(param)
#
# factor = 0.0005
# loss = factor * reg_loss
# #################################################################################################################
# DATASET PREPARATION
def get_training_batch(data_loader):
    while True:
        for sequence in data_loader:
            batch = sequence[0].cuda(),sequence[1].cuda(),sequence[2].cuda(),sequence[3].cuda()
            yield batch


train_data1 = CASIAB(
    train=True,
    data_root=opt.data_root,
    sequence_len=opt.max_step,
    glr_views=opt.glr_views,
    prb_views=opt.prb_views,
    image_height=opt.image_height,
    image_width=opt.image_width,
    n_train=opt.num_train
)
train_loader1 = DataLoader(train_data1,
                          num_workers=opt.data_threads,
                          batch_size=opt.batch_size,
                          shuffle=True,
                          drop_last=True,
                          pin_memory=True)

training_batch_generator1 = get_training_batch(train_loader1)

test_data = CASIAB(
    train=False,
    data_root=opt.data_root,
    sequence_len=opt.max_step,
    glr_views=opt.glr_views,
    prb_views=opt.prb_views,
    image_height=opt.image_height,
    image_width=opt.image_width,
    n_train=opt.num_train
)
test_loader = DataLoader(test_data,
                         num_workers=opt.data_threads,
                         batch_size=opt.batch_size,
                         shuffle=True,
                         drop_last=True,
                         pin_memory=True)
testing_batch_generator = get_training_batch(test_loader)
#################################################################################################################

def make_analogy(x):
    # (B, L, C, H, W)
    # (   B, C, H, W)
    netE.eval()
    netD.eval()

    def rand_idx():
        return np.random.randint(0, opt.batch_size)
        # return 0

    def rand_step():
        return np.random.randint(0, opt.max_step)
        # return 0

    none = torch.zeros([1, 3, 64, 64]).cuda()
    x_gs = torch.stack([i for i in [x[0][rand_step()], x[0][rand_step()], x[0][rand_step()], x[0][rand_step()],
                                    x[rand_idx()][rand_step()], x[rand_idx()][rand_step()], x[rand_idx()][rand_step()],
                                    x[rand_idx()][rand_step()]]]).cuda()
    h_gs = netE(x_gs)[1]
    # h_gs = torch.zeros(8,20).cuda()

    x_as = torch.stack([x[i][rand_step()] for i in [0, rand_idx(), rand_idx(), rand_idx(), rand_idx()]]).cuda()
    # x_as = torch.stack([x[i][0] for i in [2, 2, 2, 2, 2]]).cuda()

    h_as = netE(x_as)[0]
    # h_as = torch.ones(5,128).cuda()


    gene = [netD(torch.stack([i] * 8).cuda(), h_gs) for i in h_as]
    row0 = torch.cat([none, x_gs])
    rows = [torch.cat([e.unsqueeze(0), gene[i]]) for i, e in enumerate(x_as)]
    to_plot = torch.cat([row0] + rows)


    img = make_grid(to_plot,9)
    return img

def plot_anology(train,test,epoch):
    train_anology = make_analogy(train)
    test_anology = make_analogy(test)
    all = torch.cat([train_anology,test_anology],dim=1)
    writer.add_image('Image', all, epoch)
    fname = '%s/analogy/%s/%d.png' % (opt.savedir,opt.signature,epoch)
    save_image(all, fname, 9)

def eval_lstm_cmc(glr, prb):
    pb_vecs = []
    gr_vecs = []
    for pb in prb:
        fg_pb = [netE(pb[i].cuda())[1].detach() for i in range(len(pb))]
        fg_pb = torch.stack(fg_pb, 0).view(len(fg_pb), -1, opt.hg_dim)
        pb_vec = lstm(fg_pb)[1].detach().cpu().numpy()
        pb_vecs.append(pb_vec)

    for gr in glr:
        fg_gr = [netE(gr[i].cuda())[1].detach() for i in range(len(gr))]
        fg_gr = torch.stack(fg_gr, 0).view(len(fg_gr), -1, opt.hg_dim)
        gr_vec = lstm(fg_gr)[1].detach().cpu().numpy()
        gr_vecs.append(gr_vec)

    scores_all = []
    for pb_idx,pv in enumerate(pb_vecs):
        scores_this_pv = []
        for gv_idx,gv in enumerate(gr_vecs):
                score = []
                for i in range(len(pv)):
                    id = i
                    id_range = list(range(id,id+1))
                    score.append(calculate_identication_rate_single(gv, pv[i], id_range)[0])
                score = sum(score) / float(len(score))
                scores_this_pv.append(score)
        scores_this_pv = sum(scores_this_pv) / float(len(scores_this_pv))
        scores_all.append(scores_this_pv)
    return scores_all
def show_img(im1, im2,itr):
    all = torch.cat([im1[0], im2[0]], dim=0)
    fname = '%s/analogy/%s/%d.png' % (opt.savedir,opt.signature,itr)
    save_image(all, fname, 20)

# fname = '%s/analogy/%s/%d.png' % (opt.savedir,opt.signature,epoch)
#     save_image(all, fname, 9)

def write_tfboard(vals,itr,name):
    for idx,item in enumerate(vals):
        writer.add_scalar('data/%s%d'%(name,idx), item, itr)

#################################################################################################################
# TRAINING FUNCTION DEFINE
def train_main(Xn, Xc, Xmx, l):
    l2 = l+ opt.num_train
    # l2 = l
    Xn, Xc, Xmx = Xn.transpose(0, 1), Xc.transpose(0, 1), Xmx.transpose(0, 1)
    # accu = []
    hgs_n = []
    hgs_c = []

    self_rec_loss = 0
    loss_out_haha = 0
    for i in range(5, len(Xn)):
        netE.zero_grad()
        netD.zero_grad()
        lstm.zero_grad()
        rp = torch.randperm(opt.batch_size).cuda()
        rdm = torch.LongTensor(1).random_(5, len(Xn))[0]
        # ------------------------------------------------------------------
        xmx0, xmx1 = Xmx[rdm], Xmx[i]
        hamx0, hgmx0, emmx0 = netE(xmx0)
        hamx1, hgmx1, emmx1 = netE(xmx1)
        # accu.append(hamx1)
        # ------------------------------------------------------------------
        xmx1_ = netD(hamx0, hgmx1)
        self_rec_loss += mse_loss(xmx1_, xmx1)
        # ------------------------------------------------------------------
        xn1, xc1 = Xn[i], Xc[i]
        han1, hgn1, _ = netE(xn1)
        hac1, hgc1, _ = netE(xc1)
        # loss_out_haha += mse_loss(hgn1, hgc1)
        hgs_n.append(hgn1)
        hgs_c.append(hgc1)

    # accu = torch.stack(accu)
    # accu = torch.mean(accu, 0)
    # out = clfer(accu, 1)
    # loss_out = cse_loss(out, l2) / 20

    hgs_n = torch.stack(hgs_n)
    # hgs_n = torch.mean(hgs_n, 0)

    hgs_c = torch.stack(hgs_c)
    # hgs_c = torch.mean(hgs_c, 0)

    # out_hgs_n = clfer(hgs_n,2)
    # loss_out_haha = cse_loss(out_haha, l) / 20
    loss_out_haha = mse_loss(hgs_n, hgs_c) / 100

    # xmx1_ = netD(hamx0,hgmx1)
    # cross_rec_loss = mse_loss(xmx1_,xmx1)

    # ------------------------------------------------------------------
    # xn0, xn1, xc0, xc1 = Xn[rdm], Xn[i], Xc[rdm], Xc[i]
    # # han0, hgn0 = netE(xn0)
    # han1, hgn1, emn1 = netE(xn1)
    # # hac0, hgc0 = netE(xc0)
    # hac1, hgc1, emc1 = netE(xc1)
    # ------------------------------------------------------------------

    # loss = loss_out + self_rec_loss + loss_out_haha
    loss = self_rec_loss + loss_out_haha

    loss.backward()
    optimizerE.step()
    optimizerD.step()

    # writer.add_image('xn1_', xn1_, itr)
    # writer.add_image('xc1_', xc1_, itr)
    return [loss.data.cpu().numpy(),
            loss_out_haha.data.cpu().numpy(),
            self_rec_loss.data.cpu().numpy()]


def train_lstm(x_n,x_c,x_mx,l):
    x_n = x_n.transpose(0, 1)
    x_c = x_c.transpose(0, 1)
    x_mx = x_mx.transpose(0, 1)
    cse=0
    mse = 0
    trp = 0
    hgs_nm = []
    hgs_cl = []
    hgs_mx = []
    for i in range(0, len(x_n)):
        netE.zero_grad()
        netD.zero_grad()
        lstm.zero_grad()
        factor = (i/5)**2/10

        # rp = torch.randperm(opt.batch_size).cuda()

        xmx = x_mx[i]
        hgs_mx.append(netE(xmx)[1])
        lstm_out_mx = lstm(torch.stack(hgs_mx))[0]
        cse += cse_loss(lstm_out_mx,Variable(l))*factor

        xn = x_n[i]
        hgs_nm.append(netE(xn)[1])
        hgs_nm_ = torch.stack(hgs_nm)
        lstm_out_n = lstm(hgs_nm_)[1]

        xc = x_c[i]
        hgs_cl.append(netE(xc)[1])
        lstm_out_c = lstm(torch.stack(hgs_cl))[1]
        mse += mse_loss(lstm_out_n,lstm_out_c.detach())*factor

        # trp += 0.1*trp_loss(out_n,out_c,out_c[rp,:])

    cse /= opt.max_step
    cse *= 0.1
    mse /= opt.max_step
    mse *= 0.1

    los = cse
    los.backward()
    optimizerLstm.step()
    optimizerE.step()
    return [cse.data.cpu().numpy(),mse.data.cpu().numpy()]

#################################################################################################################
def return_clip(fg1,fg2,length):
    end_=length
    max = calculate_cosine_similarity_multidim(fg1, fg2[0:length])
    for end in range(length, len(fg2)):
        start = end-length
        fg2_clip = fg2[start:end]
        if calculate_cosine_similarity_multidim(fg1, fg2_clip) > max:
            end_ = end
            max = calculate_cosine_similarity_multidim(fg1, fg2_clip)
    return (end_-length,end_)




def alignment_and_clip(clip1, clip2, length):
    start = np.random.randint(0, clip2.shape[1] - length)
    clip1_ = clip1[:, start:start+length, :, :, :]
    # start = np.random.randint(0, clip2.shape[1] - length)
    # clip2_ = clip2[:, start:start + length, :, :, :]

    clip1_fg = [netE_use(clip1_[i].cuda())[1].detach().cpu().numpy() for i in range(len(clip1_))]
    clip2_fg = [netE_use(clip2[i].cuda())[1].detach().cpu().numpy() for i in range(len(clip2))]
    clip2_=[]
    for sbi in range(len(clip1_)):
        start,end = return_clip(clip1_fg[sbi],clip2_fg[sbi],length)
        clip2_.append(clip2[sbi,start:end,:,:,:])
    clip2_ = torch.stack(clip2_)
    return clip1_, clip2_


#################################################################################################################
# FUN TRAINING TIME !
train_eval = test_data.get_eval_data(True)
test_eval = test_data.get_eval_data(False)
writer = SummaryWriter('%s/logs/%s'%(opt.savedir,opt.signature))
itr = opt.siter
while True:
    netE_use.eval()
    netE.train()
    netD.train()
    lstm.train()

    im_nm, im_cl,im_mx,lb = next(training_batch_generator1)
    im_nm,im_cl = alignment_and_clip(im_nm, im_cl, 20)
    # show_img(im_nm,im_cl,itr)


    print(lb)
    losses1 = train_main(im_nm, im_cl,im_mx,lb)
    write_tfboard(losses1,itr,name='EDLoss')
    losses3 = train_lstm(im_nm,im_cl,im_mx,lb)
    write_tfboard(losses3, itr, name='LstmLoss')
    print(itr)

    # ----------------EVAL()--------------------
    if itr % 50 == 0:
        # with torch.no_grad():
        netD.eval()
        netE.eval()
        lstm.eval()
        scores_cmc_cl = eval_lstm_cmc(train_eval[0], train_eval[1])
        write_tfboard(scores_cmc_cl, itr, name='train_accu_rank1_cl')
        scores_cmc_cl = eval_lstm_cmc(test_eval[0], test_eval[1])
        write_tfboard(scores_cmc_cl, itr, name='test_accu_rank1_cl')

        # ----------------SAVE MODEL--------------------
    if itr % 200 == 0 and itr != opt.siter:
        torch.save({
            'netD': netD.state_dict(),
            'netE': netE.state_dict(),
            'lstm':lstm.state_dict(),
            },
            '%s/modules/%s/%d.pickle'%(opt.savedir,opt.signature,itr),)

    itr+=1


