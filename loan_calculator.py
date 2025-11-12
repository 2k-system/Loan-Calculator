import tkinter as tk
from tkinter import messagebox
import datetime
import math

# ------------------------- Core Functions (Unchanged) -------------------------

def validate_inputs(balance, monthly_payment, interest_rate, end_date):
    """Validates common input constraints based on which mode is running."""
    try:
        # Use a high number instead of None for validation when the field is being calculated
        temp_mp = monthly_payment if monthly_payment is not None else 1000000 
        temp_ir = interest_rate if interest_rate is not None else 100
        
        if balance <= 0:
            return "Balance must be a positive number."
        if temp_mp <= 0:
            return "Monthly Payment must be greater than zero."
        if temp_ir <= 0:
            return "Interest Rate must be greater than zero."
            
        if end_date and not isinstance(end_date, datetime.date):
            return "Invalid End Date format."
        if end_date and end_date <= datetime.date.today():
            return "End Date must be in the future."
            
    except Exception as e:
        return f"Validation Error: {e}"
    return None

def calculate_monthly_payment(balance, interest_rate, end_date):
    """Calculates the fixed monthly payment using the annuity formula."""
    today = datetime.date.today()
    months = (end_date.year - today.year) * 12 + (end_date.month - today.month)
    if months <= 0:
        return None
    monthly_rate = (interest_rate / 100) / 12
    try:
        if monthly_rate == 0:
             payment = balance / months
        else:
             payment = (balance * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
        return round(payment, 2)
    except:
        return None

def calculate_end_date(balance, monthly_payment, interest_rate):
    """Calculates the numberA of months required to repay the loan (iteratively)."""
    if monthly_payment <= 0:
        return None
    monthly_rate = (interest_rate / 100) / 12
    current = datetime.date.today()
    count = 0
    max_months = 1200
    
    while balance > 0 and count < max_months:
        interest = balance * monthly_rate
        # Check for payment smaller than interest
        if monthly_payment <= interest and count > 0:
             return None # Unrepayable
             
        principal_paid = monthly_payment - interest
        balance -= principal_paid
        balance = max(0, round(balance, 2))
        current = increment_month(current)
        count += 1
        
    return current if count < max_months else None

def calculate_interest_rate(balance, monthly_payment, end_date):
    """Estimates the interest rate using the Bisection method."""
    today = datetime.date.today()
    months = (end_date.year - today.year) * 12 + (end_date.month - today.month)
    if months <= 0 or monthly_payment <= 0:
        return None

    if monthly_payment <= balance / months:
        return None # Payment is too small even for 0% interest

    low = 0.0001
    high = 100.0
    for _ in range(300):
        mid = (low + high) / 2
        estimated = calculate_monthly_payment(balance, mid, end_date)
        if estimated is None:
            return None
        if abs(estimated - monthly_payment) < 0.01:
            return round(mid, 4)
        if estimated > monthly_payment:
            high = mid
        else:
            low = mid
    return None

def calculate_interest_breakdown(balance, monthly_payment, interest_rate, end_date):
    """Generates a month-by-month amortization schedule."""
    monthly_rate = (interest_rate / 100) / 12
    result = ["Date       | Payment ($) | Interest ($) | Principal ($) | Balance ($)"]
    current_date = increment_month(datetime.date.today()) # Start counting from the next month
    total_interest_paid = 0
    
    # Calculate the total months required using the provided payment
    end_date_calc = calculate_end_date(balance, monthly_payment, interest_rate)
    
    # Handle the case where calculate_end_date returns None (unrepayable)
    if end_date_calc is None:
        return "Breakdown cannot be generated: Monthly payment does not cover interest."
    
    # Loop up to the calculated end date
    while balance > 0 and current_date <= end_date_calc:
        interest = balance * monthly_rate
        
        is_final_payment = (current_date.year == end_date_calc.year and current_date.month == end_date_calc.month)
        
        if is_final_payment or balance < monthly_payment:
            # Final payment calculation
            principal_paid = balance
            payment = principal_paid + interest
            balance = 0
        else:
            principal_paid = monthly_payment - interest
            payment = monthly_payment
            balance -= principal_paid
        
        # Ensure we don't try to subtract interest from a zero or near-zero balance in the next iteration
        balance = max(0, round(balance, 2))
        interest = round(interest, 2)
        principal_paid = round(principal_paid, 2)
        payment = round(payment, 2)
        total_interest_paid += interest
        
        result.append(f"{current_date.strftime('%Y-%m-%d')} | {payment:.2f}     | {interest:.2f}      | {principal_paid:.2f}     | {balance:.2f}")
        
        if balance == 0:
            break
            
        current_date = increment_month(current_date)
        
    result.insert(1, "-" * 85)
    result.append("\n" + f"Total Interest Paid: ${round(total_interest_paid, 2):,.2f}")
    
    return "\n".join(result)

def increment_month(date):
    """Increments date by one month, setting day to 1."""
    year = date.year + (date.month // 12)
    month = (date.month % 12) + 1
    return datetime.date(year, month, 1)

# ------------------------- GUI Functions (Refactored to Hide/Show Button) -------------------------

def check_fields_and_toggle_button(event=None):
    """Checks if all required fields for the current mode are filled and toggles the button visibility."""
    
    # Map mode to the required entry widgets (entry objects themselves)
    required_map = {
        "Monthly Payment": [entry_balance, entry_interest_rate, entry_end_date],
        "End Date": [entry_balance, entry_monthly_payment, entry_interest_rate],
        "Interest Rate": [entry_balance, entry_monthly_payment, entry_end_date],
        "Interest Breakdown": [entry_balance, entry_monthly_payment, entry_interest_rate, entry_end_date]
    }
    
    required_entries = required_map.get(current_mode, [])
    
    all_filled = True
    for entry in required_entries:
        # Check if the field is visible (enabled) and empty
        if entry['state'] == tk.NORMAL and not entry.get().strip():
            all_filled = False
            break
            
    if all_filled and current_mode:
        # Show the button if all required fields are filled
        button_submit.pack(side=tk.LEFT, padx=10)
    else:
        # Hide the button if not all required fields are filled
        button_submit.pack_forget()


def reset_fields():
    """Resets all input fields and the result area."""
    # Ensure all fields are editable before clearing
    for entry in [entry_balance, entry_interest_rate, entry_monthly_payment, entry_end_date]:
         entry.config(state=tk.NORMAL)
         entry.delete(0, tk.END)

    # Set default values
    entry_end_date.insert(0, (datetime.date.today() + datetime.timedelta(days=365)).strftime('%Y-%m-%d'))
    
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    text_result.config(state=tk.DISABLED)
    check_fields_and_toggle_button() # Re-check button state after reset

def set_mode(mode):
    """Sets the calculation mode and disables the field being calculated."""
    global current_mode
    current_mode = mode
    reset_fields()
    
    label_title.config(text=f"Calculator Mode: {mode}")

    # Reset all to normal, then disable the calculated field
    for entry in [entry_balance, entry_interest_rate, entry_monthly_payment, entry_end_date]:
         entry.config(state=tk.NORMAL)

    if mode == "Monthly Payment":
        entry_monthly_payment.config(state=tk.DISABLED, bg="#F0F0F0")
    elif mode == "Interest Rate":
        entry_interest_rate.config(state=tk.DISABLED, bg="#F0F0F0")
    elif mode == "End Date":
        entry_end_date.config(state=tk.DISABLED, bg="#F0F0F0")
    elif mode == "Interest Breakdown":
         # All fields are required and remain active
         pass 

    # Set background color back to white for enabled fields
    for entry in [entry_balance, entry_interest_rate, entry_monthly_payment, entry_end_date]:
        if entry['state'] == tk.NORMAL:
            entry.config(bg="white")

    check_fields_and_toggle_button() # Initial check after setting mode


def run_calculation():
    """Reads inputs, runs the calculation based on mode, and displays the result."""
    try:
        # 1. Gather all inputs, ensuring conversion to float/date is possible
        balance = float(entry_balance.get()) if entry_balance.get() else 0
        
        # Get values only if the input field is enabled (tk.NORMAL)
        interest_rate = float(entry_interest_rate.get()) if entry_interest_rate['state'] == tk.NORMAL and entry_interest_rate.get() else None
        monthly_payment = float(entry_monthly_payment.get()) if entry_monthly_payment['state'] == tk.NORMAL and entry_monthly_payment.get() else None
        
        # Parse date only if the input field is enabled
        end_date_str = entry_end_date.get()
        end_date = None
        if entry_end_date['state'] == tk.NORMAL and end_date_str:
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Fill in the missing value with a placeholder for the calculation logic
        mp_for_calc = monthly_payment if monthly_payment is not None else 1 
        ir_for_calc = interest_rate if interest_rate is not None else 1 
        
        # 2. Validate inputs and run calculation
        if current_mode == "Monthly Payment":
            error = validate_inputs(balance, mp_for_calc, interest_rate, end_date)
            if error: return messagebox.showerror("Error", error)
            
            calculated_payment = calculate_monthly_payment(balance, interest_rate, end_date)
            result = f"Required Monthly Payment: ${calculated_payment:,.2f}" if calculated_payment is not None else "[Error] Payment could not be calculated. Check if dates are too close or payment is too low."

        elif current_mode == "End Date":
            error = validate_inputs(balance, monthly_payment, ir_for_calc, None)
            if error: return messagebox.showerror("Error", error)
            
            end = calculate_end_date(balance, monthly_payment, interest_rate)
            
            if isinstance(end, datetime.date):
                 result = f"Calculated End Date: {end.strftime('%Y-%m-%d')}"
            else:
                 result = "[Error] Unable to determine end date. The payment might not cover the interest."

        elif current_mode == "Interest Rate":
            error = validate_inputs(balance, monthly_payment, ir_for_calc, end_date)
            if error: return messagebox.showerror("Error", error)
            
            rate = calculate_interest_rate(balance, monthly_payment, end_date)
            
            if rate:
                result = f"Estimated Interest Rate (APR): {rate:.4f}%"
            else:
                result = "[Error] Could not determine interest rate. Try increasing the monthly payment or extending the end date."

        elif current_mode == "Interest Breakdown":
            error = validate_inputs(balance, monthly_payment, interest_rate, end_date)
            if error: return messagebox.showerror("Error", error)
            
            result = calculate_interest_breakdown(balance, monthly_payment, interest_rate, end_date)

        else:
            result = "Please select a calculation mode."

        # 3. Display Result
        text_result.config(state=tk.NORMAL)
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, result)
        text_result.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all required fields are filled with valid numbers (or date in YYYY-MM-DD format).")
    except Exception as e:
        messagebox.showerror("System Error", f"An unexpected error occurred: {e}")

# ------------------------- GUI Setup -------------------------

# Basic Styling Configuration
BG_COLOR = "#f4f7f6" # Light grey background
BUTTON_COLOR = "#007bff" # Blue for primary buttons
BUTTON_TEXT_COLOR = "white"
TITLE_FONT = ("Arial", 18, "bold")
LABEL_FONT = ("Arial", 10)
ENTRY_FONT = ("Arial", 10)

root = tk.Tk()
root.title("Smart Loan Calculator")
root.geometry("750x700")
root.config(bg=BG_COLOR)
root.resizable(False, False)

# Main Title Label (Removed emoji from title)
label_title = tk.Label(root, text="Loan Amortization Calculator", font=("Arial", 20, "bold"), bg=BG_COLOR, fg="#333333")
label_title.pack(pady=(20, 10))

# --- Frame 1: Mode Selection ---
mode_frame = tk.Frame(root, bg=BG_COLOR, padx=10, pady=10, bd=1, relief=tk.GROOVE)
mode_frame.pack(pady=10)

tk.Label(mode_frame, text="Select Calculation Mode:", font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=0, columnspan=4, pady=(0, 10))

# Custom Button Style
button_options = {
    'bg': BUTTON_COLOR, 
    'fg': BUTTON_TEXT_COLOR, 
    'font': LABEL_FONT, 
    'width': 22, 
    'height': 2
}

tk.Button(mode_frame, text="Calculate Monthly Payment", command=lambda: set_mode("Monthly Payment"), **button_options).grid(row=1, column=0, padx=5, pady=5)
tk.Button(mode_frame, text="Calculate End Date", command=lambda: set_mode("End Date"), **button_options).grid(row=1, column=1, padx=5, pady=5)
tk.Button(mode_frame, text="Calculate Interest Rate", command=lambda: set_mode("Interest Rate"), **button_options).grid(row=1, column=2, padx=5, pady=5)
tk.Button(mode_frame, text="Amortization Breakdown", command=lambda: set_mode("Interest Breakdown"), **button_options).grid(row=1, column=3, padx=5, pady=5)


# --- Frame 2: Input Fields ---
input_frame = tk.Frame(root, bg="white", padx=20, pady=20, bd=2, relief=tk.SUNKEN)
input_frame.pack(pady=20, padx=40, fill=tk.X)

# Loan Balance
tk.Label(input_frame, text="Loan Balance ($):", font=LABEL_FONT, bg="white").grid(row=0, column=0, sticky='w', padx=10, pady=10)
entry_balance = tk.Entry(input_frame, font=ENTRY_FONT, width=25, justify='right')
entry_balance.grid(row=0, column=1, padx=10, pady=10, sticky='e')
entry_balance.bind("<KeyRelease>", check_fields_and_toggle_button) # Bind for live check

# Interest Rate
tk.Label(input_frame, text="Annual Interest Rate (%):", font=LABEL_FONT, bg="white").grid(row=1, column=0, sticky='w', padx=10, pady=10)
entry_interest_rate = tk.Entry(input_frame, font=ENTRY_FONT, width=25, justify='right')
entry_interest_rate.grid(row=1, column=1, padx=10, pady=10, sticky='e')
entry_interest_rate.bind("<KeyRelease>", check_fields_and_toggle_button) # Bind for live check

# Monthly Payment
tk.Label(input_frame, text="Monthly Payment ($):", font=LABEL_FONT, bg="white").grid(row=2, column=0, sticky='w', padx=10, pady=10)
entry_monthly_payment = tk.Entry(input_frame, font=ENTRY_FONT, width=25, justify='right')
entry_monthly_payment.grid(row=2, column=1, padx=10, pady=10, sticky='e')
entry_monthly_payment.bind("<KeyRelease>", check_fields_and_toggle_button) # Bind for live check

# End Date
tk.Label(input_frame, text="Target End Date (YYYY-MM-DD):", font=LABEL_FONT, bg="white").grid(row=3, column=0, sticky='w', padx=10, pady=10)
entry_end_date = tk.Entry(input_frame, font=ENTRY_FONT, width=25, justify='right')
entry_end_date.insert(0, (datetime.date.today() + datetime.timedelta(days=365)).strftime('%Y-%m-%d'))
entry_end_date.grid(row=3, column=1, padx=10, pady=10, sticky='e')
entry_end_date.bind("<KeyRelease>", check_fields_and_toggle_button) # Bind for live check

# Configure column weights for centering
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)


# --- Frame 3: Action and Output ---
action_frame = tk.Frame(root, bg=BG_COLOR)
action_frame.pack(pady=10)

button_submit = tk.Button(action_frame, text="RUN CALCULATION", command=run_calculation, 
                          bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=30, height=2)
# Initially, the button is not packed (hidden)

button_reset = tk.Button(action_frame, text="RESET", command=reset_fields, 
                          bg="#dc3545", fg="white", font=("Arial", 12), width=15, height=2)
button_reset.pack(side=tk.RIGHT, padx=10) # Always show Reset button

# Output Text Area
tk.Label(root, text="Results:", font=("Arial", 14, "bold"), bg=BG_COLOR).pack(pady=(10, 5))
text_result = tk.Text(root, height=15, width=85, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", bd=1, relief=tk.SOLID, font=("Courier New", 9))
text_result.pack(padx=20, pady=10)

# Initial setup
current_mode = ""
reset_fields()
label_title.config(text="Welcome! Choose a calculation mode.")
root.mainloop()
