from tkinter import *
from tkinter import ttk

#-------------------------------------
# Initial Setup and Variable Declarations
#-------------------------------------

# Creating the main application window
root = Tk()
root.title('Bond Valuation Project')
root.resizable(False, False)

# Variables to store user inputs
coupon = IntVar()
discount_rate = IntVar()
face_value = IntVar()
nb_period = IntVar()
bond_currency = StringVar()
is_bi_annual = BooleanVar()

#-------------------------------------
# GUI Components & Entry Fields
#-------------------------------------

# Currency Selection
currency_label = Label(root, text='Bond currency:')
currency_label.grid(row=0, column=0, sticky=W)
currency = ttk.Combobox(root, values=['$', '€', '£'], width=7, textvariable=bond_currency)
currency.set('$')
currency.grid(row=0, column=1, sticky=W)

# Semi-annual Coupon Checkbox
semi_annual_payments = Checkbutton(root, text='Bi-annual coupon', variable=is_bi_annual)
semi_annual_payments.grid(row=5, column=1, sticky=W)

# Coupon Input
coupon_label = Label(root, text='Bond coupon per period:')
coupon_label.grid(row=1, column=0)
coupon_field = Entry(root, textvariable=coupon)
coupon_field.grid(row=1, column=1)
additional_text1 = Label(root, text=bond_currency.get())
additional_text1.grid(row=1, column=2, sticky=W)

# Discount Rate Input
discount_rate_label = Label(root, text='Discount rate:')
discount_rate_label.grid(row=2, column=0, sticky=W)
discount_rate_field = Entry(root, textvariable=discount_rate)
discount_rate_field.grid(row=2, column=1)
additional_text2 = Label(root, text='%')
additional_text2.grid(row=2, column=2, sticky=W)

# Face Value Input
face_value_label = Label(root, text='Face value:')
face_value_label.grid(row=3, column=0, sticky=W)
face_value_field = Entry(root, textvariable=face_value)
face_value_field.grid(row=3, column=1)
additional_text3 = Label(root, text=bond_currency.get())
additional_text3.grid(row=3, column=2, sticky=W)

# Function to dynamically update currency symbol in labels
def update_currency(event):
    additional_text1.config(text=bond_currency.get())
    additional_text3.config(text=bond_currency.get())

currency.bind("<<ComboboxSelected>>", update_currency)

# Number of Years Input
nb_period_label = Label(root, text='Number of years:')
nb_period_label.grid(row=4, column=0, sticky=W)
nb_period_field = Entry(root, textvariable=nb_period)
nb_period_field.grid(row=4, column=1)
additional_text4 = Label(root, text='yrs')
additional_text4.grid(row=4, column=2, sticky=W)

# Canvas to Display Bond Price
screen = Canvas(root, width=300, height=100, bg='white')
screen.grid(row=0, rowspan=5, column=3)

#-------------------------------------
# Bond Valuation Function
#-------------------------------------

def valuation(coupon, discount_rate, face_value, nb_period, is_bi_annual):
    if is_bi_annual:
        discount_rate /= 2  # Adjust discount rate for semi-annual payments
        nb_period *= 2      # Adjust periods for semi-annual payments

    # Calculate present value of future coupon payments
    present_value = sum(coupon / ((1 + discount_rate) ** i) for i in range(1, nb_period + 1))
    # Add present value of face value repayment
    present_value += face_value / ((1 + discount_rate) ** nb_period)

    return present_value

# Function to Update Bond Price Display

def update_bond_price():
    # Retrieve values from user input fields
    coupon_value = coupon.get()
    discount_rate_value = discount_rate.get() / 100  # Convert to decimal
    face_value_value = face_value.get()
    nb_period_value = nb_period.get()
    bi_annual = is_bi_annual.get()

    # Calculate bond price
    bond_price = valuation(coupon_value, discount_rate_value, face_value_value, nb_period_value, bi_annual)

    # Update canvas with calculated bond price
    screen.itemconfig(price_text, text=f"Bond Price: {bond_price:.2f} {bond_currency.get()}")

#-------------------------------------
# Button to Trigger Bond Price Calculation
#-------------------------------------

valuation_button = Button(root, text='Price my bond', command=update_bond_price)
valuation_button.grid(row=6, column=0, columnspan=4, pady=10)

# Initial bond price text on canvas
price_text = screen.create_text(150, 50, text="Bond Price: ", font=("Helvetica", 10), fill="black")

#-------------------------------------
# Centering Application Window
#-------------------------------------

root.update_idletasks()
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
w = root.winfo_reqwidth()
h = root.winfo_reqheight()

x = (ws // 2) - (w // 2)
y = (hs // 2) - (h // 2)

root.geometry(f"+{x}+{y}")

# Launch the main event loop
root.mainloop()
