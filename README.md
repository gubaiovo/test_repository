# JNSEC PWN  

- zh_CN [简体中文](README_CN.md)
- en [English](README.md)

JNSEC PWN Training Challenge Repository  

## Usage Instructions  

### Step0.  

Fork this project  

### Step1.  

Ensure the following files are prepared  

- **[Required] Challenge information**
- **[Required] Source code**  
- **[Required] Attachments**  
- **[Required] Exp**  
- [Optional] Other files that may be needed (e.g., libc)  

Use the project https://github.com/CTF-Archives/ctf-docker-template to set up the Docker folder (no need to build; assumed here as `pwn-ubuntu_22.04`).  

### Step2.  

In **the folder corresponding to the challenge's difficulty**, create a directory named in the format `[Challenge Type] + Challenge Name`.  

Place all necessary files in the following structure  

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

## doc.json Example  

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

