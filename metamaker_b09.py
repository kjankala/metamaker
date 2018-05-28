# coding: utf8
import Tkinter as tk
import tkFileDialog
from datetime import datetime
import ScrolledText as st
from os import getcwd
from copy import deepcopy
import reportlab
from reportlab.pdfgen import canvas

#Version
version="Beta 0.9"

#Define data in main panel using dictionary
global dict_main
dict_main={
    'tb_name':"",
    'tb_date':"",
    'tb_PI':"",
    'tb_PI_email':"",
    'tb_place':"",
    'tb_logbook_name':"",
    'tb_logbook_location':"",
    'tb_data_location':"",
    'tb_data_PID':"",
    'sb_description':"",
    'sb_participators':"",
    'sb_instrument':"",
    'sb_notes':"",
    'sb_tags':""}

#Define data in dataset using dictionary
global dict_dataset
dict_dataset={
    'tb_name':"",
    'tb_files':"",
    'tb_spectrometer':"",
    'tb_publ':"",
    'sb_sample':"",
    'sb_settings':"",
    'sb_description':"",
    'sb_notes':""}

#Class to hold all data
class AllData:
    def __init__(self):
        #Dictionary for data in main panel
        self.main=dict(dict_main)
        #Array of dictionaries for data in dataset panel
        self.datasets=[]

    #Save variable data to file
    def save_data(self,filename):
        f_obj=open(filename,"w")
        f_obj.write('\n   - Metadata file created using METAMAKER, Version: '+version+' -\n\n')
        f_obj.write(('Metadata name        : '+self.main['tb_name']+'\n').encode('utf8'))
        f_obj.write(('Date                 : '+self.main['tb_date']+'\n').encode('utf8'))
        f_obj.write(('Measurement location : '+self.main['tb_place']+'\n').encode('utf8'))
        f_obj.write(('Contact person       : '+self.main['tb_PI']+'\n').encode('utf8'))
        f_obj.write(('Email                : '+self.main['tb_PI_email']+'\n').encode('utf8'))
        f_obj.write(('Logbook file name    : '+self.main['tb_logbook_name']+'\n').encode('utf8'))
        f_obj.write(('Logbook location     : '+self.main['tb_logbook_location']+'\n').encode('utf8'))
        f_obj.write(('Raw data location    : '+self.main['tb_data_location']+'\n').encode('utf8'))
        f_obj.write(('Raw data PID         : '+self.main['tb_data_PID']+'\n').encode('utf8'))
        f_obj.write( 'Number of datasets   : '+str(len(self.datasets)))
        f_obj.write('\n----Participators----\n'+self.main['sb_participators'].rstrip('\n').encode('utf8'))
        f_obj.write('\n----Data description-\n'+self.main['sb_description'].rstrip('\n').encode('utf8'))
        f_obj.write('\n----Instrument-------\n'+self.main['sb_instrument'].rstrip('\n').encode('utf8'))
        f_obj.write('\n----Notes------------\n'+self.main['sb_notes'].rstrip('\n').encode('utf8'))
        f_obj.write('\n----Tags / Keywords--\n'+self.main['sb_tags'].rstrip('\n').encode('utf8'))
        for dtst in self.datasets:
            f_obj.write('\n\n#### -DATASET- ####\n')
            f_obj.write(('Dataset name         : '+dtst['tb_name']+'\n').encode('utf8'))
            f_obj.write(('Dataset files        : '+dtst['tb_files']+'\n').encode('utf8'))
            f_obj.write(('Spectrometer         : '+dtst['tb_spectrometer']+'\n').encode('utf8'))
            f_obj.write(('Is data publishable  : '+dtst['tb_publ']).encode('utf8'))
            f_obj.write('\n----Sample description-----\n'+dtst['sb_sample'].rstrip('\n').encode('utf8'))
            f_obj.write('\n----Experiment settings----\n'+dtst['sb_settings'].rstrip('\n').encode('utf8'))
            f_obj.write('\n----Experiment description-\n'+dtst['sb_description'].rstrip('\n').encode('utf8'))
            f_obj.write('\n----Notes / Problems-------\n'+dtst['sb_notes'].rstrip('\n').encode('utf8'))
        f_obj.write('\n\n###################')
        f_obj.close()
        
    #Load from file to variable data 
    def load_data(self,filename):
        global dtst_ddmenu
        dtst_ddmenu=['New dataset']
        cntmax=10000
        f_obj=open(filename,"r")
        f_obj.readline()
        f_obj.readline()
        f_obj.readline()
        str_arr=['tb_name',
                 'tb_date',
                 'tb_place',
                 'tb_PI',
                 'tb_PI_email',
                 'tb_logbook_name',
                 'tb_logbook_location',
                 'tb_data_location',
                 'tb_data_PID']
        for i in str_arr:
            self.main[i]=(f_obj.readline().rstrip('\n')).split(":")[1].lstrip(' ')    
        dtst_count=int((f_obj.readline().rstrip('\n')).split(":")[1])   
        str_arr=['sb_participators',
                 'sb_description',
                 'sb_instrument',
                 'sb_notes',
                 'sb_tags']
        f_obj.readline()
        for i in str_arr:  
            self.main[i]=""
            cnt=0
            while True:
                ln=f_obj.readline()
                if ln[0:4]=="----" or ln[0:4]=="####":
                    break
                self.main[i]+=ln
                cnt+=1
                if cnt==cntmax:
                    exit()
                    
            self.main[i]=self.main[i].rstrip('\n')
        for dtst_n in range(dtst_count):
            dataset=dict(dict_dataset)
            str_arr=['tb_name',
                     'tb_files',
                     'tb_spectrometer',
                     'tb_publ']
            for i in str_arr:
                dataset[i]=(f_obj.readline().rstrip('\n')).split(":")[1].lstrip(' ')
            str_arr=['sb_sample',
                     'sb_settings',
                     'sb_description',
                     'sb_notes']
            f_obj.readline()
            for i in str_arr:
                dataset[i]=""
                cnt=0
                while True:
                    ln=f_obj.readline()
                    if ln[0:4]=="----" or ln[0:4]=="####":
                        break
                    dataset[i]+=ln
                    cnt+=1
                    if cnt==cntmax:
                        exit()
                        
                dataset[i]=dataset[i].rstrip('\n')
            self.datasets.append(dict(dataset))
            dtst_ddmenu.append(dataset['tb_name'])
        f_obj.close()

data_arr=AllData()

class Main_Panel:
    
    def __init__(self,main):
        self.main=main
        
        #Main panel name
        main.title("METAMAKER, Version: "+version)
        #Main panel default size
        main.geometry("870x540")

        txt_var=dict(dict_main)
        txt_ent=dict(dict_main)

        global dtst_ddmenu
        dtst_ddmenu=["New dataset"]
        global dataset_panel_active
        dataset_panel_active=False

        ##Textboxes start##
        col1=0
        col2=1
        tb_wid=30

        #Main panel title
        tk.Label(main,text="- MAIN PANEL -",font="-weight bold").grid(column=col2,row=0,padx=(50,0),pady=(0,0),sticky='NW')

        tk.Label(main,text="Metadata name").grid(column=col1,row=1,padx=(50,10),pady=(0,0),sticky='NW')
        txt_var['tb_name']=tk.StringVar(main)  
        txt_ent['tb_name']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_name'])
        txt_ent['tb_name'].grid(column=col1,row=1,padx=(50,10),pady=(25,0),sticky='NW')

        tk.Label(main,text="Date").grid(column=col1,row=1,padx=(50,10),pady=(53,0),sticky='NW')
        txt_var['tb_date']=tk.StringVar(value=str(datetime.now())[0:10])
        txt_ent['tb_date']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_date'])
        txt_ent['tb_date'].grid(column=col1,row=1,pady=(78,0),padx=(50,10),sticky='NW')
        
        tk.Label(main,text="Measurement location").grid(column=col1,row=1,padx=(50,10),pady=(106,0),sticky='NW')
        txt_var['tb_place']=tk.StringVar(main)
        txt_ent['tb_place']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_place'])
        txt_ent['tb_place'].grid(column=col1,row=1,padx=(50,10),pady=(131,0),sticky='NW')

        tk.Label(main,text="PI / Contact person").grid(column=col1,row=1,padx=(50,10),pady=(159,0),sticky='NW')
        txt_var['tb_PI']=tk.StringVar(main)
        txt_ent['tb_PI']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_PI'])
        txt_ent['tb_PI'].grid(column=col1,row=1,padx=(50,10),pady=(184,0),sticky='NW')
        
        tk.Label(main,text="Email").grid(column=col1,row=1,padx=(50,10),pady=(212,0),sticky='NW')
        txt_var['tb_PI_email']=tk.StringVar(main)
        txt_ent['tb_PI_email']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_PI_email'])
        txt_ent['tb_PI_email'].grid(column=col1,row=1,padx=(50,10),pady=(232,0),sticky='NW')
        
        tk.Label(main,text="Logbook file name").grid(column=col1,row=1,padx=(50,10),pady=(265,0),sticky='NW')
        txt_var['tb_logbook_name']=tk.StringVar(main)
        txt_ent['tb_logbook_name']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_logbook_name'])
        txt_ent['tb_logbook_name'].grid(column=col1,row=1,padx=(50,10),pady=(290,0),sticky='NW')
        
        tk.Label(main,text="Logbook location (URL, doi, etc.)").grid(column=col1,row=1,padx=(50,10),pady=(318,0),sticky='NW')
        txt_var['tb_logbook_location']=tk.StringVar(main)
        txt_ent['tb_logbook_location']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_logbook_location'])
        txt_ent['tb_logbook_location'].grid(column=col1,row=1,padx=(50,10),pady=(343,0),sticky='NW')
        
        tk.Label(main,text="Raw data location (URL, machine, etc.)").grid(column=col1,row=1,padx=(50,10),pady=(371,0),sticky='NW')
        txt_var['tb_data_location']=tk.StringVar(main)
        txt_ent['tb_data_location']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_data_location'])
        txt_ent['tb_data_location'].grid(column=col1,row=1,padx=(50,10),pady=(396,0),sticky='NW')
        
        tk.Label(main,text="Raw data PID").grid(column=col1,row=1,padx=(50,10),pady=(423,0),sticky='NW')
        txt_var['tb_data_PID']=tk.StringVar(main)
        txt_ent['tb_data_PID']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_data_PID'])
        txt_ent['tb_data_PID'].grid(column=col1,row=1,padx=(50,10),pady=(448,0),sticky='NW')
        ##Textboxes end##

        ##Scrollboxes start##
        sb_hgt=4
        sb_wid=35
        
        tk.Label(main,text="General description").grid(column=col2,row=1,padx=(50,10),pady=(0,0),sticky='NW')
        txt_var['sb_description']=st.ScrolledText(main,width=sb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_description'].grid(column=col2,row=1,padx=(50,10),pady=(25,0),sticky='NW')
        
        tk.Label(main,text="Participators").grid(column=col2,row=1,padx=(50,10),pady=(100,0),sticky='NW')
        txt_var['sb_participators']=st.ScrolledText(main,width=sb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_participators'].grid(column=col2,row=1,padx=(50,10),pady=(125,0),sticky='NW')
        
        tk.Label(main,text="Instrument description").grid(column=col2,row=1,padx=(50,10),pady=(200,0),sticky='NW')
        txt_var['sb_instrument']=st.ScrolledText(main,width=sb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_instrument'].grid(column=col2,row=1,padx=(50,10),pady=(225,0),sticky='NW')
        
        tk.Label(main,text="Notes").grid(column=col2,row=1,padx=(50,10),pady=(300,0),sticky='NW')
        txt_var['sb_notes']=st.ScrolledText(main,width=sb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_notes'].grid(column=col2,row=1,padx=(50,10),pady=(325,0),sticky='NW')
        
        tk.Label(main,text="Tags / Keywords").grid(column=col2,row=1,padx=(50,10),pady=(400,0),sticky='NW')
        txt_var['sb_tags']=st.ScrolledText(main,width=sb_wid,height=sb_hgt-1,borderwidth=2)
        txt_var['sb_tags'].grid(column=col2,row=1,padx=(50,10),pady=(425,0),sticky='NW')
        ##Scrollboxes end##

        ##Buttons start##
        #Button functions#
        #Click function load
        def load_click():
            file_dir=getcwd()
            filename=tkFileDialog.askopenfilename(initialdir=file_dir,title="Select file")
            if filename:
                data_arr.load_data(filename)
                mp.ddrefresh(dtst_ddmenu)
                set_data(txt_ent,txt_var,data_arr.main)

        #Click function save
        def save_click():
            file_dir=getcwd()
            filename=tkFileDialog.asksaveasfilename(initialdir=file_dir,title="Select file")
            if filename:
                get_data(txt_var,data_arr.main)
                data_arr.save_data(filename)
                
        #Click function make pdf
        def get_pdf(filename):
            
            c=canvas.Canvas(filename)
            c.setFont('Times-Roman', 12)
                        
            c.setTitle(filename)
            c.setCreator(data_arr.main['tb_PI'])
            c.setSubject(data_arr.main['tb_name'])
            #c=canvas.Canvas("Test.pdf")
            #c.setTitle("Test.pdf")
            global line,lastline
            firstline=780
            lastline=50
            mn=18    #Drop along y-axis
            xsft0=100
            xsft1=58
            xsft2=170
            xsft3=58

            line=firstline #Start line
            text="   - Metadata file created using METAMAKER, Version: "+version+" -"
            c.drawString(xsft0,line,text)
            line-=mn
            c.drawString(xsft1,line,'Metadata name')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_name'])
            line-=mn
            c.drawString(xsft1,line,'Date')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_date'])
            line-=mn
            c.drawString(xsft1,line,'Measurement location')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_place'])
            line-=mn
            c.drawString(xsft1,line,'Contact person')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_PI'])
            line-=mn
            c.drawString(xsft1,line,'Email')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_PI_email'])
            line-=mn
            c.drawString(xsft1,line,'Logbook file name')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_logbook_name'])
            line-=mn
            c.drawString(xsft1,line,'Logbook location')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_logbook_location'])
            line-=mn
            c.drawString(xsft1,line,'Raw data location')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_data_location'])
            line-=mn
            c.drawString(xsft1,line,'Raw data PID')
            c.drawString(xsft2,line,':  '+data_arr.main['tb_data_PID'])
            line-=mn
            c.drawString(xsft1,line,'Number of datasets')
            c.drawString(xsft2,line,':  '+str(len(data_arr.datasets)))
            line-=mn

            def pdf_scrollbox(head,text,xsft,mn):
                global line,lastline
                tmp_ln=deepcopy(line)-10-mn
                if tmp_ln<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline
                tmp_ln=deepcopy(line)
                for txt in text.split("\n"):
                    tmp_ln-=mn
                    if tmp_ln<=lastline:
                        c.showPage()
                        c.setFont('Times-Roman', 12)
                        line=firstline
                        break

                line-=10
                c.drawString(xsft1,line,head)
                line-=mn
                ls=deepcopy(line)
                for txt in text.split("\n"):
                    c.drawString(xsft,line,txt)
                    line-=mn
                le=deepcopy(line+mn-6)
                c.rect(xsft-5,le,480,ls-le+mn-5,fill=0)
                
            head='- Participators -'
            pdf_scrollbox(head,data_arr.main['sb_participators'],xsft3,mn)
            head='- Data description -'
            pdf_scrollbox(head,data_arr.main['sb_description'],xsft3,mn)
            head='- Instrument -'
            pdf_scrollbox(head,data_arr.main['sb_instrument'],xsft3,mn)
            head='- Notes -'
            pdf_scrollbox(head,data_arr.main['sb_notes'],xsft3,mn)
            head='- Tags / Keywords -'
            pdf_scrollbox(head,data_arr.main['sb_tags'],xsft3,mn)

            c.showPage()
            c.setFont('Times-Roman', 12)
            line=firstline

            def pdf_dataset(xsft1,xsft2,xsf3,mn,dtst,i):
                global line
                if line-5*mn<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline

                c.setFont('Times-Bold', 12)
                c.drawString(xsft1,line,"# - DATASET "+str(i+1)+" - #")
                c.setFont('Times-Roman', 12)
                line-=mn
                if line<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline
                c.drawString(xsft1,line,'Dataset name')
                c.drawString(xsft2,line,':  '+dtst['tb_name'])
                line-=mn
                if line<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline
                c.drawString(xsft1,line,'Dataset files')
                c.drawString(xsft2,line,':  '+dtst['tb_files'])
                line-=mn
                if line<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline
                c.drawString(xsft1,line,'Spectrometer')
                c.drawString(xsft2,line,':  '+dtst['tb_spectrometer'])
                line-=mn
                if line<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline
                c.drawString(xsft1,line,'Is data publishable')
                c.drawString(xsft2,line,':  '+dtst['tb_publ'])
                line-=mn
                if line<=lastline:
                    c.showPage()
                    c.setFont('Times-Roman', 12)
                    line=firstline

                head='- Sample description -'
                pdf_scrollbox(head,dtst['sb_sample'],xsft3,mn)
                head='- Experiment settings -'
                pdf_scrollbox(head,dtst['sb_settings'],xsft3,mn)
                head='- Experiment description -'
                pdf_scrollbox(head,dtst['sb_description'],xsft3,mn)
                head='- Notes / Problems -'
                pdf_scrollbox(head,dtst['sb_notes'],xsft3,mn)

            for i,dtst in enumerate(data_arr.datasets):
                line-=10
                pdf_dataset(xsft1,xsft2,xsft3,mn,dtst,i)
                
            c.showPage()
            c.save()

            
        def pdf_click():
            file_dir=getcwd()
            filename=tkFileDialog.asksaveasfilename(initialdir=file_dir,title="Select file")
            if filename:
                get_data(txt_var,data_arr.main)
                get_pdf(filename)

        #Click function help
        def help_click():
            help_win=tk.Toplevel(main)
            help_win.title("Help and About")
            help_win.geometry("598x350")
            help_win_box=st.ScrolledText(help_win,width=70,height=20)
            help_win_box.grid(padx=(10,0))
            help_win_box.insert(tk.END,help_text)
            help_win_box.config(state=tk.DISABLED)

        #Click function dataset
        def dataset_click():
            global dataset_panel_active
            if ddvar.get() in dtst_ddmenu and not dataset_panel_active:
                dataset_panel_active=True
                dt_panel=tk.Toplevel(self.main)
                Dataset_Panel(dt_panel,ddvar)
            elif ddvar.get()=="SELECT":
                popup_win("Select dataset")

        #Click function dataset
        #def dataset_ddmenu(self):
        #    global dataset_panel_active
        #    print ddvar.get()
        #    if ddvar.get() in dtst_ddmenu and not dataset_panel_active:
        #        dataset_panel_active=True
        #        dt_panel=tk.Toplevel(main)
        #        Dataset_Panel(dt_panel,ddvar)
                
        #Button functions end#

        bt_sft=33
        bt_col=3
        #Button for Open file
        tk.Button(main,text="Open",command=load_click,bg="light blue",width=8,bd=2)\
          .grid(column=bt_col,row=1,pady=(0,0),padx=(bt_sft,0),sticky='NW')
        #Button for Save file
        tk.Button(main,text="Save",command=save_click,bg="light blue",width=8,bd=2)\
          .grid(column=bt_col,row=1,pady=(40,0),padx=(bt_sft,0),sticky='NW')
        #Button for makign and saving pdf file
        tk.Button(main,text="Make PDF",command=pdf_click,bg="light blue",width=8,bd=2)\
          .grid(column=bt_col,row=1,pady=(80,0),padx=(bt_sft,0),sticky='NW')
        #Button for display help
        tk.Button(main,text="Help",command=help_click,bg="khaki",width=8,bd=2)\
          .grid(column=bt_col,row=1,pady=(140,0),padx=(bt_sft,0),sticky='NW')
        #Button for quit
        tk.Button(main,text="Quit",command=main.destroy,bg="orange red",width=8,bd=2)\
          .grid(column=bt_col,row=1,pady=(180,0),padx=(bt_sft,0),sticky='NW')
        #Button for opening dataset window
        tk.Button(main,text="EDIT DATASET",command=dataset_click,bg="dodger blue",bd=3,width=13)\
          .grid(column=bt_col,row=1,pady=(240,0),padx=(10,0),sticky='NW')
        ##Buttons end##

        ##Drop down menu##
        global ddvar,ddmenu
        ddvar=tk.StringVar(main)
        ddvar.set("SELECT")
        ddmenu=tk.OptionMenu(main,ddvar,*dtst_ddmenu)#,command=dataset_ddmenu(self))
        ddmenu.config(width=11,bd=3,bg="light steel blue")
        ddmenu.grid(column=bt_col,row=1,pady=(280,0),padx=(10,0),sticky='NW')
        ##Drop down menu end##

    def ddrefresh(self,new_set):
        ddvar.set("SELECT")
        ddmenu['menu'].delete(0,'end')
        for i in new_set:
            ddmenu['menu'].add_command(label=i,command=tk._setit(ddvar,i))
       

class Dataset_Panel:
    def __init__(self,main,ddvar):
        self.main=main

        #Dataset panel name
        if ddvar.get()==dtst_ddmenu[0]:
            main.title("New Dataset")
        else:
            main.title(ddvar.get())
        #Dataset panel default geometry
        main.geometry("530x720")

        txt_var=dict(dict_dataset)
        txt_ent=dict(dict_dataset)

        tb_wid=50
        tb_xsft=50
        sb_hgt=4
        sb_wid=35
    
        tk.Label(main,text="- DATASET PANEL -",font="-weight bold")\
          .grid(column=0,row=0,padx=(tb_xsft+120,0),pady=(0,0),sticky='NW')

        tk.Label(main,text="Dataset name").grid(column=0,row=1,padx=(tb_xsft,0),pady=(0,0),sticky='NW')
        txt_var['tb_name']=tk.StringVar(main)
        txt_ent['tb_name']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_name'])
        txt_ent['tb_name'].grid(column=0,row=2,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        
        tk.Label(main,text="Measurement files").grid(column=0,row=3,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['tb_files']=tk.StringVar(main)
        txt_ent['tb_files']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_files'])
        txt_ent['tb_files'].grid(column=0,row=4,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        
        tk.Label(main,text="Sample description").grid(column=0,row=5,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['sb_sample']=st.ScrolledText(main,width=tb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_sample'].grid(column=0,row=6,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        
        tk.Label(main,text="Spectrometer").grid(column=0,row=7,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['tb_spectrometer']=tk.StringVar(main)
        txt_ent['tb_spectrometer']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_spectrometer'])
        txt_ent['tb_spectrometer'].grid(column=0,row=8,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        
        tk.Label(main,text="Experimental settings").grid(column=0,row=9,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['sb_settings']=st.ScrolledText(main,width=tb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_settings'].grid(column=0,row=10,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        
        tk.Label(main,text="Measurement description").grid(column=0,row=11,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['sb_description']=st.ScrolledText(main,width=tb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_description'].grid(column=0,row=12,padx=(tb_xsft,0),pady=(5,0),sticky='NW')

        tk.Label(main,text="Notes / Problems").grid(column=0,row=13,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['sb_notes']=st.ScrolledText(main,width=tb_wid,height=sb_hgt,borderwidth=2)
        txt_var['sb_notes'].grid(column=0,row=14,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        
        tk.Label(main,text="Is data publishable?").grid(column=0,row=15,padx=(tb_xsft,0),pady=(5,0),sticky='NW')
        txt_var['tb_publ']=tk.StringVar(main)
        txt_ent['tb_publ']=tk.Entry(main,width=tb_wid,textvariable=txt_var['tb_publ'])
        txt_ent['tb_publ'].grid(column=0,row=16,padx=(tb_xsft,0),pady=(5,0),sticky='NW')

        #Insert existing dataset into textboxes
        if ddvar.get()!=dtst_ddmenu[0]:
            ss=str(ddvar.get())
            set_data(txt_ent,txt_var,data_arr.datasets[dtst_ddmenu.index(ss)-1])

        # Click event close
        def close_click():
            global dtst_ddmenu,dataset_panel_active
            mp.ddrefresh(dtst_ddmenu)
            main.destroy()
            dataset_panel_active=False
        tk.Button(main,text="Close",command=close_click,bg="orange red",width=6,bd=2).\
            grid(column=0,row=17,pady=(10,0),padx=(tb_xsft+327,0),sticky='NW')
                                                                                                

        # Click event save and close
        def save_close_click():
            global dtst_ddmenu,dataset_panel_active
            dataset=dict(dict_dataset)
            get_data(txt_var,dataset)
            if dataset['tb_name']=="":
                popup_win("Dataset name required")
            #elif dataset['tb_name'] in dtst_ddmenu:
            #   popup_win("Dataset name is in use")
            else:
                if ddvar.get()==dtst_ddmenu[0]:
                    data_arr.datasets.append(dict(dataset))
                    dtst_ddmenu.append(dataset['tb_name'])
                    mp.ddrefresh(dtst_ddmenu)
                else:
                    ss=str(ddvar.get())
                    data_arr.datasets[dtst_ddmenu.index(ss)-1]=dict(dataset)
                    dtst_ddmenu[dtst_ddmenu.index(ss)]=dataset['tb_name']
                    mp.ddrefresh(dtst_ddmenu)
                main.destroy()
                dataset_panel_active=False                
        tk.Button(main,text="Save and Close",command=save_close_click,bg="light blue",width=12,bd=2).\
            grid(column=0,row=17,pady=(10,0),padx=(tb_xsft,0),sticky='NW')


        # Click event delete
        def delete_click():
            global dtst_ddmenu,dataset_panel_active
            if ddvar.get() in dtst_ddmenu[1:len(dtst_ddmenu)]:
                ss=str(ddvar.get())
                dtst_indx=dtst_ddmenu.index(ss)
                data_arr.datasets.pop(dtst_indx-1)
                dtst_ddmenu.pop(dtst_indx)
            mp.ddrefresh(dtst_ddmenu)
            main.destroy()
            dataset_panel_active=False

        def select_import(self):
            if ddset.get() in dtst_ddmenu[1:len(dtst_ddmenu)]:
                #Insert imported dataset into textboxes
                ss=str(ddset.get())
                set_data(txt_ent,txt_var,data_arr.datasets[dtst_ddmenu.index(ss)-1])
                ddset.set("Import")
            
        # Add delete button if dataset exists
        if ddvar.get()!=dtst_ddmenu[0]:
            tk.Button(main,text="Delete",command=delete_click,bg="orange red",width=6,bd=2).\
                grid(column=0,row=17,pady=(10,0),padx=(tb_xsft+227,0),sticky='NW')
        #Add import menu if new dataset
        elif len(dtst_ddmenu)>1:
            ##Drop down menu##
            ddset=tk.StringVar(main)
            ddset.set("Import")
            ddmn=tk.OptionMenu(main,ddset,*dtst_ddmenu[1:len(dtst_ddmenu)],command=select_import)
            ddmn.config(width=8,bd=2,bg="light steel blue")
            ddmn.grid(column=0,row=17,pady=(10,0),padx=(tb_xsft+210,0),sticky='NW')
            ##Drop down menu end##
    

        # Redifine window default close button
        main.protocol('WM_DELETE_WINDOW',close_click)  
    
#Get data from textboxes and scrollboxes
def get_data(inp,out):
    for key in inp:
        if key[0:2]=="tb": #If textbox
            out[key]=deepcopy(inp[key].get()).rstrip('\n')
        elif key[0:2]=='sb': #If scrollbox
            out[key]=deepcopy(inp[key].get(1.0,tk.END)).rstrip('\n')

#Set loaded data into textboxes
def set_data(txt_ent,txt_box,inp):
    for key in inp:
        if key[0:2]=="tb": #If textbox
            txt_ent[key].delete(0,"end")
            txt_ent[key].insert(0,inp[key])
        elif key[0:2]=='sb': #If scrollbox
            txt_box[key].delete('1.0',tk.END)
            txt_box[key].insert(tk.END,inp[key])

#Window to display errors
def popup_win(text):
    pwin=tk.Toplevel(main)
    pwin.title('Error')
    pwin.geometry("300x70")
    tk.Label(pwin,text=text,font="-weight bold").grid(column=0,row=0,padx=(10,0),pady=(0,0),sticky='NW')
    # Click event close
    tk.Button(pwin,text="Close",command=pwin.destroy,bg="orange red",width=6,bd=2).\
        grid(column=0,row=1,pady=(0,0),padx=(80,0),sticky='NW')


##Text to display in Help window##
help_text="""
    ----------------------------
    - METAMAKER HELP AND ABOUT -
    ----------------------------

Program    : Metamaker
Version    : """+version+"""
Time       : 5/2018
Language   : Python 2.7.15
Character  : UTF-8
Written by : Kari Jänkälä, Univ. of Oulu, NANOMO
Contact    : kari.jankala@oulu.fi

The program uses the following Python2 packages:
Tkinter, tkFileDialog, datetime, ScrolledText, 
os, copy, reportlab

    --------
    - Help -
    --------

PROGRAM IDEA: 
 The aim of the program is to provide a standardized way to
 easily make and store metadata from experiments. The program 
 DOES NOT aim to replace logbook, its function is to provide 
 a file that gives an overview of the measurement session and 
 information on where the data and logbook are stored. 
 The files should be considered to be "metadata of metadata".

INPUT: Written text during measurement session.
OUTPUT: ASCII file of the metadata and optionally a PDF file.

MAIN PANEL:
 Write here the general parameters of your experiment. In this panel
 you can also save and load experiment files and open the dataset
 window. The window is opened by selecting the dataset 
 (new or existing) and pressing EDIT DATASET.

DATASET PANEL:
 Write here the parameters of your experiment session. The aim
 is that unique datasets are created for each experimental
 arrangement during the measurement session. When the dataset is 
 created, press SAVE and it will be save to internal dataset array. 
 It can be then modified later and it will be written into 
 the output file. An existing dataset can be also deleted in 
 this panel.


    ------------------------
    - Terms and Conditions -
    ------------------------
Copyright (C) 2018, Kari Jänkälä

This program is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details
(http://www.gnu.org/licenses/).
"""
##Help window text end##
        
##Main loop##
main=tk.Tk()
mp=Main_Panel(main)
main.mainloop()


    
