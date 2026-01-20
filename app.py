import streamlit as st
from datetime import date
from num2words import num2words
import datetime
import requests, json
# import pandas as pd
import time
from fpdf import FPDF


#####################
#### VERSION 2.0 ####
#####################


################################################################################

passcode_key = {
    "ak1" : "Ashish Goyal",
    "hg1" : "Himanshu Goyal"
}

################################################################################

## airtable.py
token = "pat3fppRKREzKvAC4.7b3e3e6d2d2477af4b334bf98eb9fb34930713b1f82ac86944b2d30d2041acc7"
table_name = "tblCjsKzBgz7WexCL"
airtable_url = "https://api.airtable.com/v0/appwUzDMekCAdu0CI/Table%201"

# ### Grabintel2
# token = "paty3aZlpH8vhTPXX.0ed9ca67273354044cda3b57a19587df47673a3b16632665de401881b81d4b16"
# airtable_url = "https://api.airtable.com/v0/appzUuXVK7BZLDw3Y/tbl2o9Ktflclik554"

# ### Grabintel17 - tab grab1
# token = "patLTGpATLKnvKcx2.5aaa4259982cc7e2d5a1beef122388760f90fc61fa095427340456b0291d4216"
# airtable_url = "https://api.airtable.com/v0/appLYbLlMddk5i6ct/tbl0Z5xv9g8yVv7dM"

################################################################################


def fetch_records(token, fieldnames):

    headers = {'Authorization': 'Bearer %s' % token}

    fields = []; params = []; pp = 1

    while 1:
        try:
            page = requests.get(airtable_url,headers=headers, params = params)
            mdata = json.loads(page.content)
            # print(mdata)
            data = mdata["records"]            

            for each in data:
                if len(each["fields"]) > 0:

                    temp = []
                    for ff in fieldnames:
                        try:
                            temp.append(each["fields"][ff])
                        except:
                            temp.append(None)
                    fields.append(temp)

            try:            
                check = mdata["offset"]
                if len(check)>5:
                    params = [("offset",check)]
                else:
                    break           
            except:
                break
            pp = pp + 1
        except Exception as e:
            print(e)
            time.sleep(5)

    return fields

    # db = pd.DataFrame(fields, columns = fieldnames)
    # return(db)


def create_record(token, json_data):

    headers = {'Authorization': 'Bearer %s' % token}

    fields = []; params = []; pp = 1


    json_data = {
        'records': [
            {
                'fields': json_data
            },
        ],
    }
    page = requests.post(airtable_url,headers=headers, json = json_data)
    mdata = json.loads(page.content)

    print(mdata)


################################################################################
## CREATEPDF.py
border = 0

def section(pdf,_amount,gst,amount_in_words,name,flat_number,flat_config,mode,reference,invoice_num,date_invoice):

    pdf.set_font('', '', 10)

    pdf.cell(20, 5, ln = 1, border = border)
    pdf.cell(25, 10, txt = "Invoice No. :" , ln = 0, border = border)

    pdf.set_font('', 'B', 12)
    pdf.cell(30, 10, txt = str(invoice_num) , ln = 0, border = 0, align = 'C')
    pdf.set_font('', '', 10)

    pdf.cell(35, 10, ln = 0, border = border)
    pdf.cell(15, 10, txt = "Date :" , ln = 0, border = border)

    pdf.set_font('', 'B', 12)
    pdf.cell(30, 10, txt = date_invoice , ln = 1, border = 0, align = 'L')
    pdf.set_font('', '', 10)

    pdf.cell(35, 5, ln = 1, border = border)


    text = f"Received with thanks a sum of Rs {_amount + gst}/- in words Rs {amount_in_words} Only from {name} on account of Skyline Developers"
    
    pdf.multi_cell(0,5, txt = text, border = border)

    pdf.cell(20, 5, ln = 1, border = border)

    pdf.cell(25, 7, txt = "Amount", ln = 0, border = border)
    pdf.cell(30, 7, txt = "Rs " + str(_amount) + "/-" , ln = 0, border = 1, align = 'L')


    pdf.cell(45, 7, ln = 1, border = border)

    pdf.cell(25, 7, txt = "GST", ln = 0, border = border)
    pdf.cell(30, 7, txt = "Rs " + str(gst) + "/-", ln = 1, border = 1, align = 'L')

    pdf.cell(25, 7, txt = "Flat", ln = 0, border = border)
    pdf.cell(30, 7, txt = f"{flat_number}", ln = 0, border = 1, align = 'L')

    pdf.set_font('', 'I', 8)
    pdf.cell(55, 7, txt = f"{flat_config}", ln = 1, border = border)
    pdf.set_font('', '', 10)


    pdf.cell(25, 7, txt = "Mode", ln = 0, border = border)
    pdf.cell(30, 7, txt = mode , ln = 0, border = 1, align = 'L')

    pdf.cell(45, 7, ln = 1, border = border)

    pdf.cell(25, 7, txt = "Reference No.", ln = 0, border = border)
    pdf.set_font('', '', 8)

    if len(reference) > 90:
        refer1 = reference[0:90]
        refer2 = reference[90:]
        pdf.cell(150, 5, txt = refer1, border = border, ln = 1, align = 'L')
        pdf.cell(25, 7, txt = "", ln = 0, border = border)
        pdf.cell(150, 5, txt = refer2, border = border, ln = 1, align = 'L')

    else:
        pdf.cell(150, 7, txt = reference, border = border, ln = 1, align = 'L')


    pdf.cell(40, 5, ln = 1, border = border)
    pdf.cell(40, 5, txt = "Skyline Developers", ln = 1, border = border)
    pdf.cell(40, 5, txt = "Authorized Signature:", ln = 0, border = border)

    pdf.cell(40, 5, txt = "___________________________", ln = 1, border = border)

    text = "NOTE: This receipt will only be deemed valid once the Check/DD/RTGS has been successfully cleared"

    pdf.set_font('arial', 'I', 8)
    pdf.cell(95, 10, txt = text, ln = 1, border = border)


    return pdf

def pdf_first_page(_amount,gst,amount_in_words,name,flat_number,flat_config,mode,reference,invoice_num,date_invoice):

    pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')

    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.set_margins(20,20)


    pdf.rect(x = 10, y = 10 , w = 190, h= 130, style = "")
    pdf.rect(x = 10, y = 145, w = 190, h= 130, style = "")

    pdf.image('logo.png', x = 25, y = 20, w = 75, h = 25, type = '')

    pdf.set_fill_color(r = 57, g = 107, b = 109)
    pdf.rect(x = 30, y = 45, w = 150, h= 1.5, style = "F")

    pdf.set_fill_color(r = 57, g = 107, b = 109)

    pdf.set_font('', 'I', 6)
    text = ""

    pdf.cell(105, 10, ln = 0, border = border)
    pdf.cell(85,  10, ln = 1, border = border)

    pdf.cell(105, 10, ln = 0, border = border)
    pdf.cell(75, 10, txt = "Customer Copy", ln = 1, border = border, align="R")

    pdf.set_font('', '', 8)
    text = ""

    pdf.cell(95,  5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "Skyline Elevate", ln = 1, border = border)

    pdf.cell(95,  5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "PR7 Airport Road, Zirakpur", ln = 1, border = border)

    pdf.cell(95,  5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "M: +91-7710444010", ln = 1, border = border)

    pdf.cell(95,  5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "E-mail: info@skylineelevate.com", ln = 1, border = border)

    pdf.cell(95, 5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "www.skylineelevate.com", ln = 1, border = border)


    ########################################################################
    ########################################################################
    # pdf.set_font('', '', 10)

    pdf = section (pdf,_amount,gst,amount_in_words,name,flat_number,flat_config,mode,reference,invoice_num,date_invoice)

    ############################
    # pdf.cell(95, 5, txt = "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", ln = 1, border = border)
    ############################

    pdf.image('logo.png', x = 25, y = 150, w = 75, h = 25, type = '')

    pdf.set_fill_color(r = 57, g = 107, b = 109)
    pdf.rect(x = 30, y = 175, w = 150, h= 1.5, style = "F")

    pdf.set_fill_color(r = 57, g = 107, b = 109)

    pdf.set_font('', '', 8)
    text = ""

    pdf.cell(105, 10, ln = 0, border = border)
    pdf.cell(105, 10, ln = 1, border = border)

    pdf.cell(95, 5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "Skyline Elevate", ln = 1, border = border)

    pdf.cell(95, 5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "PR7 Airport Road, Zirakpur", ln = 1, border = border)

    pdf.cell(95,  5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "M: +91-7710444010", ln = 1, border = border)

    pdf.cell(95,  5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "E-mail: info@skylineelevate.com", ln = 1, border = border)

    pdf.cell(95, 5, ln = 0, border = border)
    pdf.cell(95, 5,txt = "www.skylineelevate.com", ln = 1, border = border)

    pdf = section(pdf,_amount,gst,amount_in_words,name,flat_number,flat_config,mode,reference,invoice_num,date_invoice)

    pdf.set_font('', 'I', 6)
    text = ""

    pdf.cell(105, 5, ln = 0, border = border)
    pdf.cell(75,  5, txt = "For Office Use", ln = 1, border = border, align="R")

    pdf.output('Receipt.pdf', 'F')

    with open("Receipt.pdf", "rb") as pdf_file:
        encoded_string = pdf_file.read()
    
    return encoded_string

################################################################################

## Downloading logo from AWS
try:
    url = "https://skylineelevate.s3.ap-south-1.amazonaws.com/logo.png"
    image = requests.get(url)
    with open("logo.png","wb") as f:
        f.write(image.content)
except:
    url = "https://picsum.photos/200/300?grayscale"
    image = requests.get(url)
    with open("logo.png","wb") as f:
        f.write(image.content)


###################

auth_name = "Admin"
authentication_status = True

# if authentication_status:
#     # st.write(f'Welcome *{auth_name}*')
#     st.write(f'Welcome')
#     pass
# elif authentication_status is False:
#     st.error('Username/password is incorrect')
# elif authentication_status is None:
#     st.warning('Please enter your username and password')
###################
###################



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Skyline Elevate Reciepts", page_icon=":bar_chart:")
# st.image("Logo.png", caption=None, width=250, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


st.session_state.disabled = True
st.session_state.pdf = ""


### Updates DataBase to be shown depending on Selected Flat
def show_db():

    master_database = st.session_state.master

    database = []
    for x in master_database:
        if (x[0] == st.session_state["selected_flat"]) or (x[0] == str(st.session_state["selected_flat"])):
            if x[-2] is None:
                database.append(x)

    # database = master_database[(master_database.Flat == st.session_state["selected_flat"]) | (master_database.Flat == str(st.session_state["selected_flat"]))]

    st.session_state.db = database

    st.session_state.disabled = True
    st.session_state.pdf = ""



if "db" not in st.session_state:

    st.session_state.token = token
    st.session_state.columns = ["Flat", "Reciept","Name","Date","Amount","Mode","Reference No", "created_by", "Cancel", "IFMS"]

    master_data = fetch_records(st.session_state.token, st.session_state.columns)

    st.session_state.invoice = "Sky-" + f"{len(master_data)+1:03}"
    st.session_state.invoice_num = len(master_data)

    st.session_state.master = master_data
    st.session_state["selected_flat"] = 101

    show_db()



def invoice_generated():

    if st.session_state.invoicename != "" and st.session_state.amount > 0:
        try:
            json_data = {
                "Flat"   : str(st.session_state.selected_flat),
                "Reciept": st.session_state.invoice,
                "Name"   : st.session_state.invoicename,
                "Date"   : str(date.today()),
                "Amount" : str(st.session_state.amount),
                "Mode"   : st.session_state.mode,
                "Reference No": st.session_state.reference,
                "created_by"  : passcode_key[st.session_state.passcode],
                "IFMS" : st.session_state.IFMS_MARKER
                }

            create_record(st.session_state.token, json_data)

            master_data = fetch_records(st.session_state.token, st.session_state.columns)
            st.session_state.master = master_data
            show_db()

            st.session_state.invoice = "Sky-" + f"{len(master_data)+1:03}"
            st.session_state.invoice_num = len(master_data)

            st.session_state.filename = f'Skyline-{st.session_state.selected_flat}-{st.session_state.invoice}.pdf'

            st.session_state.success = "Yes"
        except Exception as e:
            print(e)
            st.session_state.success = "No"



def invoice_downloaded():
    if not st.session_state.disabled:
        st.success("Invoice Downloaded")    


t1, t2 = st.tabs(["Generate", "Duplicate"])


if authentication_status:

    ###################
    first, second, third, fourth  = t1.columns(4)

    first.write(f"Invoice No. : {st.session_state.invoice}")
    third.write(f"Date : {date.today()}")
    ###################

    left, right = t1.columns(2)
    left.checkbox("IFMS_Marker", value = False, key="IFMS_MARKER", help="Check the box if IFMS", on_change = None, args=None, disabled=False)

    ###################
    left, right = t1.columns(2)

    nn = ""
    try:
        for each in st.session_state.master:
            if each[0] == str(st.session_state["selected_flat"]):
                nn = each[2]
                break
    except:
        nn = ""

    amount        = left.number_input("Amount", value = 0 , key = "amount")
    invoicename   = right.text_input("Name"   , value = nn, key = "invoicename", placeholder = "Receipt Name")


    _amount = round(amount/1.05*1)
    gst     = (amount-_amount)


    amount_in_words = num2words(amount, lang='en_IN').replace(",","").title()
    t1.write(f"*{amount_in_words}* Only")

    if st.session_state.IFMS_MARKER:
        _amount = amount
        gst = 0
    else:
        _amount = round(amount/1.05*1)
        gst     = (amount-_amount)

    t1.write(f"Amount : *{_amount}* | GST : {gst}")

    ###################

    ###################
    left, right = t1.columns(2)

    with left:
        flat_num = st.selectbox("Flat Number",
    			[101, 102, 103, 104, 201, 202, 203, 204, 301, 302, 303, 304, 401, 402, 403, 404, 501, 502, 503, 504, 601, 602, 603, 604, 701, 702, 703, 704, 801, 802, 803, 804, 901, 902, 903, 904, 1001, 1002, 1003, 1004, 1101, 1102, 1103, 1104, 1201, 1202, 1203, 1204, 1301, 1302, 1303, 1304, 1401, 1402, 1403, 1404,
    			105, 106, 107, 108, 205, 206, 207, 208, 305, 306, 307, 308, 405, 406, 407, 408, 505, 506, 507, 508, 605, 606, 607, 608, 705, 706, 707, 708, 805, 806, 807, 808, 905, 906, 907, 908, 1005, 1006, 1007, 1008, 1105, 1106, 1107, 1108, 1205, 1206, 1207, 1208, 1305, 1306, 1307, 1308, 1405, 1406, 1407, 1408],
                on_change = show_db,
                key="selected_flat",
    			)

    with right:
        if flat_num % 100 <= 4:
            flat_config = "4 BHK - Tower A - T2"
            st.text_input("-", placeholder = "*4 BHK - Tower A - T2*", disabled = True)
        else:
            flat_config = "3 BHK - Tower B - T1"
            st.text_input("-", placeholder = "*3 BHK - Tower B - T1*", disabled = True)
    ###################


    ###################
    left, right = t1.columns(2)
    with left:
        mode = st.selectbox("Mode of Payment", ["RTGS","DD","Cheque","NEFT","IMPS"], key = "mode")
    with right: 
        reference = st.text_input("Transaction Reference No.", max_chars = 150, key = "reference")
    ###################

    if st.session_state.IFMS_MARKER:
        try:
            reference = "IFMS : " + reference
        except:
            pass

    left, right = t1.columns(2)
    with left:
        passcode = st.text_input("Passcode - For Verification", max_chars = 20, key = "passcode", type="password")

    ###################
    st.session_state.filename = f'Temp.pdf'

    if 'but_generate' not in st.session_state:
        st.session_state.disabled = True
        st.session_state.pdf = ""
    ###################

    ###################
    left, right,r,t = t1.columns(4)

    generate = left.button("Generate Invoice", key='but_generate', on_click = invoice_generated)

    if generate:

        if passcode not in passcode_key.keys():
            t1.error("Incorrect Passcode")

        elif invoicename == "":
            t1.error("Please Enter the Name Field")
        elif amount == 0:
            t1.error("Please Enter an Amount")

        elif st.session_state.success == "Yes":
            t1.success("Invoice Generated")
            date_invoice = str(date.today())

            pdf = pdf_first_page(_amount, gst, amount_in_words, invoicename, flat_num, flat_config, mode, reference, f"Sky-{st.session_state.invoice_num:03}", date_invoice)

            st.session_state.filename = f'Skyline-{flat_num}-Sky-{st.session_state.invoice_num:03}.pdf'
            st.session_state.disabled = False
            st.session_state.pdf = pdf

        elif st.session_state.success == "No":
            t1.error("Could Not Generate Invoice")


    download_Invoice = right.download_button(label="Download Invoice", data = st.session_state.pdf, file_name= st.session_state.filename, mime='application/octet-stream', disabled = st.session_state.disabled, on_click = invoice_downloaded)

    # email = r.button("Email", disabled = st.session_state.disabled)

    t1.write(f"Total Reciepts for Flat-{flat_num}")

    _sum = 0
    for e in st.session_state.db:
        _sum += float(e[4])


    amount_in_words = num2words(_sum, lang='en_IN').replace(",","").title()
    t1.write(f"Sum : {_sum} | *{amount_in_words}* Only")

    # st.session_state.columns = ["Flat", "Reciept","Name","Date","Amount","Mode","Reference No", "created_by"]
    A, a, b, c, d, e, f = t1.columns(7)
    A.write("")
    a.write(st.session_state.columns[0])
    b.write(st.session_state.columns[1])
    c.write(st.session_state.columns[2])
    d.write(st.session_state.columns[3])
    e.write(st.session_state.columns[4])
    f.write(st.session_state.columns[6])

    for i,each in enumerate(st.session_state.db,1):
        A, a, b, c, d, e, f = t1.columns(7)
        A.write(i)
        a.write(each[0])
        b.write(each[1])
        c.write(each[2])
        d.write(each[3])
        e.write(each[4])
        f.write(each[6])
        t1.write("---------------------------------------------")


    # st.write

    # t1.table(st.session_state.db)


with t2:
    left, right = st.columns(2)
   
    all_receipts = []
    for each in st.session_state.master:
        all_receipts.append(each[1])

    sorted_all_receipts = sorted(all_receipts, key=lambda x: int(x.split('-')[1]))

    with left:
        flat_num = st.selectbox("Reciept No.", sorted_all_receipts,
                key="selected_reciept",
                )

    reciept_no = st.session_state.selected_reciept

    master_database = st.session_state.master

    for each in master_database:
        if each[1] == reciept_no:

            IFMS_MARKER = each[-1]
            if IFMS_MARKER:
                amount         = float(each[4])

                _amount = amount
                gst     = (amount-_amount)

            else:
                amount         = float(each[4])

                _amount = round(amount/1.05*1)
                gst     = (amount-_amount)

            amount_in_words = num2words(amount, lang='en_IN').replace(",","").title()

            invoicename     = each[2]
            flat_num        = each[0]
            if int(flat_num) % 100 <= 4:
                flat_config = "4 BHK - Tower A - T2"
            else:
                flat_config = "3 BHK - Tower B - T1"
            mode            = each[5]
            reference       = each[6]
            invoice_num     = each[1]
            date_invoice    = each[3]

            left, right = t2.columns(2)
            with left:
                passcode = st.text_input("Passcode - For Verification", max_chars = 20, key = "passcode_dup", type="password")

            ###################
            left, right,r = t2.columns(3)

            # generate = left.button("Generate Dup. Invoice", key='but_generate_dup', on_click = invoice_generated)
            generate = left.button("Generate Dup. Invoice", key='but_generate_dup')

            if generate:
                if passcode not in passcode_key.keys():
                    t2.error("Incorrect Passcode")

                elif invoicename == "":
                    t2.error("Please Enter the Name Field")
                elif amount == 0:
                    t2.error("Please Enter an Amount")

                else:
                    t2.success("Invoice Generated")

                    pdf = pdf_first_page(_amount, gst, amount_in_words, invoicename, flat_num, flat_config, mode, reference, invoice_num, date_invoice)

                    filename = f'Skyline-{flat_num}-{invoice_num}.pdf'

                    download_Invoice = right.download_button(label="Download Dup. Invoice", data = pdf, file_name= filename, mime='application/octet-stream', disabled = False, on_click = invoice_downloaded)






    
