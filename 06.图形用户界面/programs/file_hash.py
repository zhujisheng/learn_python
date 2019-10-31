import tkinter as tk
from tkinter import filedialog, messagebox

import hashlib

def file_hash( input_filename, method):
    """计算文件的HASH值"""
    with open(input_filename, 'rb') as fp:
        if( method==1 ):
            hashfunc = hashlib.md5()
        elif( method==2 ):
            hashfunc = hashlib.sha256()
        elif( method==3 ):
            hashfunc = hashlib.blake2b(digest_size=32)
        else:
            return

        while True:
            c = fp.read(10240)
            if not c:
                break
            hashfunc.update(c)

        return hashfunc.hexdigest()

def get_filename():
    name= filedialog.askopenfilename()
    FILENAME.set(name)
    HASH.set('')

def cal_hash():
    if not FILENAME.get():
        messagebox.showwarning("警告","请先选择文件!")
        return
    r = file_hash( FILENAME.get(), METHOD.get())
    HASH.set(r)


# 整个窗口
root = tk.Tk()
root.title("计算文件HASH值")
root.maxsize(1600, 800)

# 全局变量与设置函数
FILENAME = tk.StringVar()
METHOD = tk.IntVar()
HASH = tk.StringVar()

# 左右两个frame
w_frame_l = tk.Frame(root, bg="#e0f8f8")
w_frame_r = tk.Frame(root)

# 显示选择的文件名
w_label_filename = tk.Label(w_frame_l,
                            bg= "#e0f8f8",
                            fg='green',
                            font=('times', 16, 'italic'),
                            textvariable=FILENAME)

# 文件选择按钮
w_button_fileselect = tk.Button(w_frame_l, text="选择文件", font=('times', 16),
                                command=get_filename)
w_button_fileselect.config(width=40)

# 算法标题
w_label_method = tk.Label(w_frame_l,
                          bg="#e0f8f8",
                          font=('times', 20),
                          text="算法：")

# 算法单选钮
w_radio1 = tk.Radiobutton(w_frame_l, text="MD5", bg="#e0f8f8", font=('times', 16),
                          variable=METHOD, value=1)
w_radio2 = tk.Radiobutton(w_frame_l, text="SHA256", bg="#e0f8f8", font=('times', 16),
                          variable=METHOD, value=2)
w_radio3 = tk.Radiobutton(w_frame_l, text="BLAKE2b256", bg="#e0f8f8", font=('times', 16),
                          variable=METHOD, value=3)

# 计算按钮
w_button_cal = tk.Button(w_frame_l, text="计算", width=15, font=('times', 16),
                         command=cal_hash)

# 关闭按钮
w_button_close = tk.Button(w_frame_l, text="关闭",width=15, font=('times', 16),
                           command=root.destroy)

# 计算结果标题
w_label_text1 = tk.Label(w_frame_r,
                         font=('times',40),
                         text="计算结果")

# 文件标题
w_label_text2 = tk.Label(w_frame_r,
                         font=('times', 20 ),
                         text="文件:")

# 选择的文件名
w_label_text3 = tk.Label(w_frame_r,
                         fg='red',
                         font=('times', 20, 'italic' ),
                         textvariable=FILENAME)

# HASH值标题
w_label_text4 = tk.Label(w_frame_r,
                         font=('times', 20 ),
                         text="哈希值:")

# 计算获得的结果
w_label_text5 = tk.Label(w_frame_r,
                         fg='red',
                         font=('times', 16, 'italic' ),
                         textvariable=HASH)

# 显示widget
w_frame_l.pack(side=tk.LEFT)
w_frame_r.pack(side=tk.LEFT, fill=tk.Y)
w_label_filename.pack(fill=tk.X)
w_button_fileselect.pack(padx=100,pady=20)
w_label_method.pack(anchor=tk.W, padx=20, pady=20)
w_radio1.pack(anchor=tk.W, padx=50)
w_radio2.pack(anchor=tk.W, padx=50)
w_radio3.pack(anchor=tk.W, padx=50)
w_button_cal.pack(side=tk.LEFT, padx=100, pady=50)
w_button_close.pack(side=tk.RIGHT, padx=100, pady=50)
w_label_text1.pack(anchor=tk.S, pady=40)
w_label_text2.pack(anchor=tk.W, padx=30)
w_label_text3.pack(anchor=tk.N, pady=20)
w_label_text4.pack(anchor=tk.W, padx=30, pady=20)
w_label_text5.pack(anchor=tk.N, padx=50, pady=20)

root.mainloop()
