import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

def generate_schedule(employees, first_duties, month, num_days, start_day, rest_days):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start_index = days_of_week.index(start_day)
    
    schedule = []
    
    for i in range(num_days):
        date = datetime.date(2025, 2, i+1)  # Example year & month, modify accordingly
        day_of_week = days_of_week[(start_index + i) % 7]
        row = [date.strftime("%d-%m-%Y"), day_of_week]
        
        for j, name in enumerate(employees):
            if day_of_week == rest_days[name]:
                row.append("Rest")
            else:
                row.append(first_duties[j])
                
                # Rotate shift except for 'G'
                if first_duties[j] != "G":
                    first_duties[j] = "A" if first_duties[j] == "C" else "C" if first_duties[j] == "B" else "B"
        
        schedule.append(row)
    
    columns = ["Date", "Day"] + employees
    return pd.DataFrame(schedule, columns=columns)

def create_excel(df, month):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=f"{month} Schedule")
        writer.book.close()
    return output.getvalue()

# Streamlit UI
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
