# Loan-Calculator
Smart Loan Amortization Calculator (₹)

The Smart Loan Amortization Calculator is a Python-based desktop application built with Tkinter. It provides multiple financial calculation modes to help users analyze and plan their loan repayments, focusing on the Indian Rupee (₹) currency.

✨ Features

This calculator goes beyond basic functions, allowing you to solve for any missing loan variable:

Calculate Monthly Payment: Determine the fixed Equated Monthly Installment (EMI) required to repay the loan by a specific target date.

Calculate End Date: Find out exactly when the loan will be fully paid off, given a fixed monthly payment.

Calculate Interest Rate (APR): Estimate the Annual Percentage Rate (APR) required to meet a specific repayment schedule.

Amortization Breakdown: Generate a detailed month-by-month schedule showing the principal, interest, and remaining balance for the entire loan term.

💻 Requirements

To run this application, you need:

Python: Version 3.x

Tkinter: Tkinter is typically included with standard Python installations. No external libraries are strictly required.

🚀 How to Run

Save the provided code as a Python file (e.g., smart_loan_calculator_inr.py).

Open your terminal or command prompt.

Navigate to the directory where you saved the file.

Run the script using the Python interpreter:

python smart_loan_calculator_inr.py


📝 Usage Instructions

Upon launching, you must select one of the four calculation modes.

General Inputs

All numerical inputs (Balance, Payment, Rate) must be positive values. The date must be in the format YYYY-MM-DD.

Selecting a Mode

When you click a mode button:

The calculator automatically disables and greys out the input field that is being calculated.

The remaining required fields become active and must be filled in.

The "RUN CALCULATION" button will only appear once all necessary inputs for the selected mode are provided.

Mode Selected

Disabled Input

Required Inputs

Monthly Payment

Monthly Payment

Balance, Interest Rate, Target End Date

End Date

Target End Date

Balance, Monthly Payment, Interest Rate

Interest Rate

Interest Rate

Balance, Monthly Payment, Target End Date

Amortization Breakdown

None

All four fields are required

Viewing Results

Results will be displayed in the Results text area, providing either a single calculated value (Payment, Date, Rate) or the full monthly breakdown.

🇮🇳 Currency

This calculator is configured to display monetary values using the Indian Rupee (₹) symbol.
