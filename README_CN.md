# JNSEC PWN  

- zh_CN [简体中文](README_CN.md)
- en [English](README.md)

JNSEC PWN 训练题目仓库  

## 使用方法  

### Step0.  

fork 本项目  

### Step1.  

确保准备好以下文件  

- **[必须] 题目信息**
- **[必须] 源码**  
- **[必须] 附件**  
- **[必须] exp**  
- [可选] libc等其他做题可能需要的文件  

使用项目 https://github.com/CTF-Archives/ctf-docker-template 搭建docker文件夹，无需构建（以下假设为 `pwn-ubuntu_22.04` ）

### Step2.  

在**你认为该题目的难度的对应文件夹**中，以 `[题目类型] + 题目名` 格式创建文件夹  

将所有需要的文件按照如下结构放入文件夹  

```
[ret2text] testyourpayload # Challenge  
├─ doc.json # Challenge Information  
├─ pwn-ubuntu_22.04 # Docker Source Files  
|  └─ ...
└─ challenge  
   ├─ attachment # Attachments  
   ├─ exp.py # Exp  
   ├─ other file # Other Files (such as libc)  
   └─ src  
      └─ attachment.c # Challenge Source Code (adjust as needed)
```

### Step3.  

PR  

## doc.json 示例  

```json
{
    "author": "gubai",
    "challenge": {
        "difficulty": "Base",
        "category": "ret2text",
        "name": "testyourpayload",
        "introduction": "a challenge to test your payload",
        "...(other information)": "(other information)"
    }
}
```
