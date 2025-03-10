from tkinter import * 
from tkinter import ttk 

#-------------------------------------
# variables
#-------------------------------------

root = Tk()
root.title('Bond valuation project')
root.resizable(False,False)

coupon = IntVar()
discount_rate = IntVar()
face_value = IntVar()
nb_period = IntVar()
bond_currency = StringVar()
is_bi_annual = BooleanVar()

#-------------------------------------
# GUI & Entry fields
#-------------------------------------

currency_label = Label(root, text = 'Bond currency :')
currency_label.grid(row =0, column=0, sticky = W)
currency = ttk.Combobox(root, values = ['$', '€', '£'], width=7, textvariable=bond_currency)
currency.set('$')
currency.grid(row = 0, column = 1, sticky = W)

semi_annual_payments = Checkbutton(root, text='bi-annual coupon', variable = is_bi_annual)
semi_annual_payments.grid(row =5, column = 1, sticky=W)

coupon_label = Label(root, text='Bond coupon per period')
coupon_label.grid(row = 1, column=0)
coupon_field = Entry(root, textvariable = coupon)
coupon_field.grid(row = 1, column = 1)
additional_text1 = Label(root, text=bond_currency.get())
additional_text1.grid(row = 1, column=2, sticky=W)

discount_rate_label = Label(root, text='Discount rate')
discount_rate_label.grid(row =2, column = 0, sticky = W)
discount_rate_field = Entry(root, textvariable = discount_rate)
discount_rate_field.grid(row = 2, column = 1)
additional_text2 = Label(root, text='%')
additional_text2.grid(row = 2, column = 2, sticky=W)


face_value_label = Label(root, text='Face value')
face_value_label.grid(row = 3, column=0, sticky=W)
face_value_field = Entry(root, textvariable=face_value)
face_value_field.grid(row = 3, column=1)
additional_text3 = Label(root, text=bond_currency.get())
additional_text3.grid(row = 3, column = 2, sticky=W)

def update_currency(event):
    additional_text1.config(text= bond_currency.get())
    additional_text3.config(text= bond_currency.get())
currency.bind("<<ComboboxSelected>>", update_currency)


nb_period_label = Label(root, text='Number of years')
nb_period_label.grid(row = 4, column=0, sticky = W)
nb_period_field = Entry(root, textvariable=nb_period)
nb_period_field.grid(row = 4, column=1)
additional_text4 = Label(root, text='yrs')
additional_text4.grid(row = 4, column=2, sticky=W)

screen = Canvas(root, width=300, height=100, bg='white')
screen.grid(row = 0, rowspan=5, column=3)


#-------------------------------------
# Valuation Function
#-------------------------------------

def valuation(coupon, discount_rate, face_value, nb_period, is_bi_annual):
    if is_bi_annual:
        discount_rate /= 2  # Adjust rate for semi-annual payments
        nb_period *= 2  # Double the number of periods

    present_value = sum(coupon / ((1 + discount_rate) ** i) for i in range(1, nb_period + 1))
    present_value += face_value / ((1 + discount_rate) ** nb_period)

    return present_value

# Function to update the bond price in the canvas
def update_bond_price():
        # Get user input values
        coupon_value = coupon.get()
        discount_rate_value = discount_rate.get() / 100  # Convert percentage to decimal
        face_value_value = face_value.get()
        nb_period_value = nb_period.get()
        bi_annual = is_bi_annual.get()

        # Calculate bond price
        bond_price = valuation(coupon_value, discount_rate_value, face_value_value, nb_period_value, bi_annual)

        # Update the canvas with the new bond price
        screen.itemconfig(price_text, text=f"Bond Price: {bond_price:.2f} {bond_currency.get()}")


#-------------------------------------
# Button to Trigger Calculation
#-------------------------------------

valuation_button = Button(root, text='Price my bond', command=update_bond_price)
valuation_button.grid(row=6, column=0, columnspan=4, pady=10)

price_text = screen.create_text(150, 50, text="Bond Price: ", font=("Helvetica", 10), fill="black")

#-------------------------------------
# Opening position of the window
#-------------------------------------

root.update_idletasks()
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
w = root.winfo_reqwidth()
h = root.winfo_reqheight()

x = (ws // 2) - (w // 2)
y = (hs // 2) - (h // 2)

root.geometry(f"+{x}+{y}")


root.mainloop()