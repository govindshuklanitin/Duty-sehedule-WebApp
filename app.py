import streamlit as st

# Title of the web app
st.title("Duty Schedule Generator")

# Input: Number of employees
num_employees = st.number_input("Enter the number of employees:", min_value=1, step=1)

# Lists to store employee details
employees = []
first_duties = []
rest_days = {}

# Input form for each employee
for i in range(num_employees):
    name = st.text_input(f"Enter name of Employee {i+1}:", key=f"name_{i}")
    duty = st.selectbox(f"Select first duty for {name}:", ["A", "C", "B", "G"], key=f"duty_{i}")
    rest_day = st.selectbox(f"Select rest day for {name}:", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], key=f"rest_day_{i}")

    employees.append(name)
    first_duties.append(duty)
    rest_days[name] = rest_day

# Button to generate schedule
if st.button("Generate Schedule"):
    st.write("### Generated Duty Schedule:")
    
    # Sample logic for generating schedule
    for i in range(num_employees):
        st.write(f"Employee: **{employees[i]}** - First Duty: **{first_duties[i]}** - Rest Day: **{rest_days[employees[i]]}**")
