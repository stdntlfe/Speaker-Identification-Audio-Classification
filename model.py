import os
from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Conv2D, MaxPool2D, Flatten, LSTM
from keras.layers import Dropout, Dense, TimeDistributed
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.utils.class_weight import compute_class_weight
from tqdm import tqdm
from python_speech_features import mfcc

def build_rand_feat():
    X=[]
    y=[]
    _min,_max=float('inf'),-float('inf')
    for _ in tqdm(range(n_samples)):
        rand_class=np.random.choice(class_dist.index,p=prob_dist)
        file=np.random.choice(df[df.label==rand_class].index)
        rate,wav=wavfile.read('clean/'+file)
        label=df.at[file,'label']
        rand_index=np.random.randint(0,wav.shape[0]-config.step)
        sample=wav[rand_index:rand_index+config.step]
        X_sample=mfcc(sample,rate,numcep=config.nfeat,
                      nfilt=config.nfilt,nfft=config.nfft).T
        _min=min(np.amin(X_sample),_min)
        _max=max(np.amin(X_sample),_max)
        X.append(X_sample if config.mode=='conv' else X_sample.T)
        y.append(classes.index(label))
        X,y=np.array(X),np.array(y)
       # X=(X - _min) / (_max - _min)
        if config.mode=='conv':
            X=X.reshape(X.shape[0],X.shape[1],X.shape[2])
        elif config.mode=='time':
            X=X.reshape(X.shape[0],X.shape[1],X.shape[2])
        y=to_categorical(y,num_classes=10)
        return X,y
        
        
        
class Config:
    def __init__(self,mode='conv',nfilt=26,nfeat=13,nfft=512,rate=16000):
        self.mode=mode
        self.nfilt=nfilt
        self.nfeat=nfeat
        self.nfft=nfft
        self.rate=rate
        self.step=int(rate/10)

df = pd.read_csv('instruments.csv')
df.set_index('fname', inplace=True)

for f in df.index:
    rate, signal = wavfile.read('clean/'+f)
    df.at[f, 'length'] = signal.shape[0]/rate

classes = list(np.unique(df.label))
class_dist = df.groupby(['label'])['length'].mean()

n_samples=2*int(df['length'].sum()/0.1)
prob_dist=class_dist/class_dist.sum()
choices=np.random.choice(class_dist.index,p=prob_dist)

fig, ax = plt.subplots()
ax.set_title('Class Distribution', y=1.08)
ax.pie(class_dist, labels=class_dist.index, autopct='%1.1f%%',
       shadow=False, startangle=90)
ax.axis('equal')
plt.show()

config=Config(mode='conv')
if config.mode=='conv':
    X,y=build_rand_feat()
elif config.mode=='time':
    X,y=build_rand_feat()
    