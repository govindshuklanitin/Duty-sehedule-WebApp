import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

def generate_schedule(employee_names, first_duties, month, num_days, start_day, rest_days):
    shifts = ["A", "C", "B", "G"]
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    schedule = {"Date": [], "Day": []}
    
    for name in employee_names:
        schedule[name] = []
    
    start_index = days_of_week.index(start_day)
    for day in range(1, num_days + 1):
        current_day = days_of_week[(start_index + day - 1) % 7]
        schedule["Date"].append(day)
        schedule["Day"].append(current_day)
        
        for i, name in enumerate(employee_names):
            if current_day == rest_days[name]:
                schedule[name].append("Rest")
            else:
                shift_index = shifts.index(first_duties[i])
                schedule[name].append(shifts[shift_index])
                if current_day == "Sun":
                    first_duties[i] = shifts[(shift_index + 1) % 3]
    
    return pd.DataFrame(schedule)

def create_excel(df, month):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=f"{month} Schedule")
        writer.book.close()
    return output.getvalue()

st.title("Duty Schedule Generator")

month = st.text_input("Enter Month:")
num_days = st.number_input("Enter number of days in the month:", min_value=28, max_value=31, step=1)
start_day = st.selectbox("Select the first day of the month:", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
num_employees = st.number_input("Enter number of employees:", min_value=1, step=1)

employees = []
first_duties = []
rest_days = {}

for i in range(num_employees):
    name = st.text_input(f"Enter name of Employee {i+1}:")
    duty = st.selectbox(f"Select first duty for {name}:", ["A", "C", "B", "G"])
    rest_day = st.selectbox(f"Select rest day for {name}:", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    employees.append(name)
    first_duties.append(duty)
    rest_days[name] = rest_day

if st.button("Generate Schedule"):
    df = generate_schedule(employees, first_duties, month, num_days, start_day, rest_days)
    st.dataframe(df)
    excel_data = create_excel(df, month)
    st.download_button(label="Download Excel File", data=excel_data, file_name=f"{month}_Duty_Schedule.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
