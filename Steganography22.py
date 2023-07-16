from io import BytesIO
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox, filedialog
import os
from PIL import Image
from PIL import ImageTk
import mysql.connector

mydb=mysql.connector.connect(host='localhost',user='root',password='harshu',database='file_details')
if mydb.is_connected():
    print("connected")
else:
    print("not connected")
mycursor=mydb.cursor()


class Steganography:
    def main(self,root):
        root.title(" Image Steganography")
        root.geometry('700x600')
        f=Frame(root,bg='black')

        title=Label(f,text='Image Steganography')
        title.config(font=('Bold',35),fg='white',bg='black')
        title.grid(padx=100,pady=40)
        b1=Button(f,text="Hide Message",command=lambda:self.hide_menu(f),width=12,height=1)
        b1.config(font=("Bold",18))
        b2=Button(f,text="Show Message",command=lambda:self.show_menu(f))
        b2.config(font=("Bold",18))
        f.pack(fill='both',expand=1)

        title.grid(row=1)
        b1.grid(row=3,pady=50)
        b2.grid(row=7,pady=20)

    def home(self,frame):
        frame.destroy()
        self.main(root)

    def hide_menu(self,f):
        f.destroy()
        f2=Frame(root,bg='black')
        l1=Label(f2,text="  \n\nSelect the Image in which you want \nto hide the text : ",width=30,height=4)
        l1.config(font=('Bold',30),bg='black',fg='white')
        l1.grid()
        b_select=Button(f2,text='Select',command=lambda : self.hide_menu2(f2),width=12,height=1)
        b_select.config(font=("Bold',32"))
        b_select.grid(row=10,pady=50)
        b_cancel = Button(f2, text='Cancel', command=lambda: Steganography.home(self,f2),width=12,height=1)
        b_cancel.config(font=("Bold',20"))
        b_cancel.grid(pady=30)
        f2.pack(fill='both', expand=1)

    def hide_menu2(self,f2):
        f3=Frame(root,bg='black')
        The_file=filedialog.askopenfilename(title='Select a file',filetypes=([('png','*.png'),('jpeg','*.jpeg'),('jpg','*.jpg'),('All Files','*.*')]))
        if not The_file:
            messagebox.showerror("Errot","You have not selected anything !!!")
        else :
            img1=Image.open(The_file)
            img2=img1.resize((300,200))
            img=ImageTk.PhotoImage(img2)
            l1_f3=Label(f3,text='Selected Image',bg='black',fg='white')
            l1_f3.config(font=("'Bold',30"))
            l1_f3.grid()
            panel=Label(f3,image=img)
            panel.image=img
            self.output_image_size = os.stat(The_file)
            self.o_image_w, self.o_image_h=img1.size
            panel.grid()
            l2_f3=Label(f3,text="Enter the message to hide :",bg='black',fg='white')
            l2_f3.config(font=('Bold',18))
            l2_f3.grid(pady=15)
            text_area=Text(f3,width=80,height=10)
            text_area.grid()
            encode_button= Button(f3,text="Encode",bg='black',fg='white',command=lambda : [self.encode_fun(text_area,img1,The_file),Steganography.home(self,f3)])
            encode_button.config(font=('Bold',11))
            data = text_area.get('1.0', 'end-1c')
            cancel_button=Button(f3,text='Cancel',bg='black',fg='white',command=lambda : Steganography.home(self,f3))
            cancel_button.config(font=("Bold",11))
            cancel_button.grid()
            encode_button.grid(pady=15)
            f3.pack(fill='both', expand=1)
            f2.destroy()

    def encode_fun(self,text_area,img1,The_file):
        data=text_area.get('1.0','end-1c')
        if (len(data)==0):
            messagebox.showinfo("Kindly enter the text in TextBox")
        else:
            new_img=img1.copy()
            self.encode_function(new_img,data)
            my_file=BytesIO()
            temp=os.path.splitext(os.path.basename((img1.filename))[0])
            p=tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=([('png', '*.png')]),defaultextension=".png")
            new_img.save(p)

            self.d_image_size=my_file.tell()
            self.d_image_w,self.d_image_h=new_img.size
            r=os.path.basename((p))
            print(p)
            print("print " ,r)

            self.insert_db(The_file,p)

            messagebox.showinfo("","Successfully Encoded \nFile is saved in the same directory")
    def encode_function(self,new_img,data):
        w=new_img.size[0]
        (x,y)=(0,0)
        for pixel in self.modify_pixel(new_img.getdata(),data):
            new_img.putpixel((x,y),pixel)
            if(x==w-1):
                x=0
                y+=1
            else:
                x+=1

    def generate_data(self,data):
        new_data=[]
        for i in data:
            new_data.append(format(ord(i),'08b'))   #ord returns unicode char then formats it to 8 bit binary
        return new_data

    def modify_pixel(self,pix,data):
        datalist=self.generate_data(data)
        len_data=len(datalist)
        img_data=iter(pix)
        for i in range(len_data):
            #extract 3 pixels of the image at a time
            pix=[value for value in img_data.__next__()[:3]+img_data.__next__()[:3]+img_data.__next__()[:3]]

            for j in range(0,8):
                if (datalist[i][j] == '0') and (pix[j]%2!=0):
                    if (pix[j]%2 != 0):
                        pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j]%2 == 0):
                    pix[j] -= 1

            if (i == len_data-1):
                if (pix[-1]%2 ==0):
                    if (pix[-1] !=0):
                        pix[-1] -=1
                    else:
                        pix[-1] +=1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix=tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def show_menu(self,f):
        f.destroy()
        f4=Frame(root,bg='black')
        l1_f4=Label(f4,text='Select the Image with the Hidden text : ',bg='black',fg='white')
        l1_f4.config(font=('Bold',24))
        l1_f4.place(relx=0.5,rely=0.2,anchor='center')
        select2_button = Button(f4, text='Select', command=lambda: self.show_menu2(f4))
        select2_button.config(font=('Bold',18))
        select2_button.place(x=260,y=220)
        cancel_button = Button(f4,text='Cancel',command=lambda : Steganography.home(self,f4))
        cancel_button.config(font=('Bold',18))
        cancel_button.place(x=260,y=320)
        f4.pack(fill='both', expand=1)

    def show_menu2(self,f4):
        f5=Frame(root,bg='black')
        myfile=tkinter.filedialog.askopenfilename(filetypes=([('png','*.png'),('jpeg','*.jpeg'),('jpg','*.jpg'),('All Files','*.*')]))
        print(myfile)
        if not myfile:
            messagebox.showerror("Error",'You have selected nothing !')
        else:
            imgs= Image.open(myfile)
            imag=imgs.resize((300,200))
            img1=ImageTk.PhotoImage(imag)
            l1_f5=Label(f5,text='Selected image :',bg='black',fg='white')
            l1_f5.config(font=('Bold',18))
            l1_f5.grid(padx=250,pady=10)
            panel1=Label(f5, image = img1)
            panel1.image=img1
            panel1.grid()
            hidden_data=self.decode(imgs)
            l2_f5=Label(f5,text='Hidden data is : ',bg='black',fg='white')
            l2_f5.config(font=('Bold',18))
            l2_f5.grid(pady=10)
            text_area=Text (f5,width=70,height=12)
            text_area.insert(INSERT,hidden_data)
            text_area.configure(state='disabled')
            text_area.grid()
            cancel_button=Button(f5,text='Cancel',command=lambda : self.lastPage(f5))
            cancel_button.config(font=('Bold',11))
            cancel_button.grid(pady=15)
            img_info=Button(f5,text='More info about image',command=lambda : self.info(myfile))
            img_info.config(font=('Bold',11))
            img_info.grid()
            f5.pack(fill='both', expand=1)
            f4.destroy()

    def decode(self,image):
        data=''
        imgdata=iter(image.getdata())

        while(True):
            pixels=[value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
            binstr=''
            for i in pixels[:8]:
                if i%2==0:
                    binstr+='0'
                else:
                    binstr+='1'
            data+=chr(int(binstr,2))
            if pixels[-1]%2!=0:
                return data
    def lastPage(self,frame):
        frame.destroy()
        self.main(root)

    def info(self,image_info):
        file_s=os.stat(image_info)
        im= os.path.basename((image_info))
        print("info ",im)
        mycursor.execute("SELECT * FROM `names` WHERE `new_file`='"+im+"'")
        c=0
        t=()
        for i in mycursor:
            t=i
        l=list(t)
        try:
            str = 'original image:-%s\nsize of original image:%f mb\ndecoded image:- %s\nsize of decoded image: %f mb\n'%(l[0],l[1],l[2],l[3])
            messagebox.showinfo('info',str)
        except:
            messagebox.showinfo('Info','Unable to get the information')

    def insert_db(self,in_file,out_file):
        i=os.stat(in_file)
        ib=os.path.basename(in_file)
        o=os.stat(out_file)
        ob=os.path.basename(out_file)
        i_size=(i.st_size)/(1024*1024)
        o_size = (o.st_size) / (1024 * 1024)
        sql=("INSERT INTO `names`(`o_file`, `o_size`, `new_file`, `new_size`) VALUES (%s,%s,%s,%s)")
        val=(ib,i_size,ob,o_size)
        mycursor.execute(sql,val)
        mydb.commit()
root=Tk()
obj=Steganography()
obj.main(root)
root.mainloop()