
# nanoGPT训练
参考开源nanoGPT代码，使用transformer架构和清华新闻数据集体育部分（THUCNews），训练了一个128.84M参数量的续写模型，进行了30000轮次训练，模型的训练损失率和测试损失率均降到2.5左右。并成功实现语义明确的续写。

参考网址：https://github.com/karpathy/nanoGPT

## 环境：
#### 训练设备
- GPU: 4080 显卡

#### Anaconda 环境配置
- [Python 3.10.15](https://www.python.org/downloads/release/python-31015/)
- [numpy 2.1.2](https://pypi.org/project/numpy/2.1.2/)
- [datasets 2.21.0](https://pypi.org/project/datasets/2.21.0/)
- [torch 2.5.0+cu124](https://pytorch.org/get-started/previous-versions/)
- [tiktoken 0.8.0](https://pypi.org/project/tiktoken/0.8.0/)
- [tqdm 3.8.0](https://pypi.org/project/tqdm/3.8.0/)
- [transformers 4.46.0](https://pypi.org/project/transformers/4.46.0/)
- [wandb 0.18.5](https://pypi.org/project/wandb/0.18.5/)


## 初次试错：
使用红楼梦的txt文件作为训练集，效果并不理想。（文件夹中的sidamingzhu均为与之相关的文件）  
问题：过拟合明显。 
```
step 2000: train loss 1.1798, val loss 5.1980  
step 3000: train loss 0.2954, val loss 6.4054  
step 4000: train loss 0.1332, val loss 7.1862
```

使用的训练参数如下：
```
--device=cuda --compile=False --eval_iters=200 --log_interval=10 --block_size=256 --batch_size=32 --n_layer=24 --n_head=8 --n_embd=512 --max_iters=5000 --lr_decay_iters=5000 --dropout=0.2
```
原因分析：（1）数据集过小，（2）dropout过小，（3）学习率过大。  
于是换清华大学新闻数据集，将dropout改为0.4，并将学习率设置为2e-5。

## 数据集处理：
数据集路径：**.\nanoGPT\data\TH\input.txt**  
（数据集使用UTF-8编码方式，而开源代码中在windows下自动选择gbk解码方式所以修改了prepare.py文件）  
命令行：（用于生成train.bin和val.bin文件）
```
python data/TH/prepare.py
```
数据集大小：**length of dataset in characters: 171,967,843**  
不同的字符数：**vocab size: 5,791**  
将10%作为测试集，90%作为训练集。

## 模型训练:
使用40层，8个多头注意力机制的头，进行30000轮训练，学习率为2e-5。详细参数如下：
![image](https://github.com/user-attachments/assets/59d66458-ec2a-4d84-be36-b20e5c7bf9f6)  
图1，训练参数情况。

命令行：
```
python train.py config/train_TH.py --device=cuda --compile=False --eval_iters=200 --log_interval=10 --block_size=256 --batch_size=32 --n_layer=40 --n_head=8 --n_embd=512 --max_iters=30000 --lr_decay_iters=30000 --dropout=0.4
```

模型参数大小为128MB左右。（4080显卡训练大约需要3小时）

![image](https://github.com/user-attachments/assets/3fcb9663-a80a-42d3-892e-420f6d896bd7)  
图2，部分训练情况。

最终训练30000轮时：**train loss 和 val loss 都在2.5左右。**  
  
## 调用模型进行续写
sample.py中设置的是生成十段续写的语句。

命令行：
```
python sample.py --out_dir=TH_out
```
（可以加--start=xxx参数进行续写开头的定义，“xxx”为续写开头汉字，例如“皇马”）  
若使用cpu进行续写，则要加上  
```
--device=cpu
```

#### 生成续写展示：
```
皇马主帅伊尔戈米对这位德国国家队成员说：“我们会竭尽所能地留在德国，为他们的球迷们加油，我们能够充分地信任他们。”
　　伊尔戈米的经纪人AIGlend透露，在拉伊奥拉与皇马进行转会谈判后，皇马正在积极的反对方向国际米兰提出报价。在被问到伊尔戈米的未来时，伊尔戈米表示：“我们会在和沙尔戈和马尔戈俱乐部签约，但现在我确定合同到期，我们正在向马尔戈进行协议，伊尔戈米 具体的到期合同还有剩下两年，这样我们还需要再说，我们只能是按照他的计划来决定。”
　　当然，伊尔戈米也承认，“因为他们的合同还有一年一年才结束的时间很长，如果马尔蒂尼的合同期为一年的到期，我们也想做出决定，这是我们所愿意看到的。”
```

