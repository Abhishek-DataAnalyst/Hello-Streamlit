import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64

pd.options.display.max_rows = 5

login_status = st.session_state.get('login_status', False)

if not login_status:
    # If not logged in, ask for credentials
    st.image("https://ramseyelbasheer.files.wordpress.com/2021/07/b56bf-1mdvspoblumxt4i7vswzq8q.png?w=2181", width=300)
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        # Replace with secure credentials
        if username == "Abhi" and password == "Abhi@123":
            st.success("Login Successful!, Please CLick on login button again to continue")
            st.session_state.login_status = True
        else:
            st.error("Invalid Username or Password")
else:
    def home_page():
        # Title
        st.title("Hello, Streamlit!")

        # Text
        st.write("Hello, Streamlit!")

        # Image
        st.image("https://ramseyelbasheer.files.wordpress.com/2021/07/b56bf-1mdvspoblumxt4i7vswzq8q.png?w=2181", width=300)

        # Text input 
        user_name = st.text_input("Enter your name:")

        # Display personalized greeting
        if user_name:
            st.success(f"Hello, {user_name}! Welcome to Streamlit!")

        # Add a Button
        Toggle_Button = st.button("Toggle Button")

        if Toggle_Button:
            st.write("Welcome to Streamlit!")
        else:
            st.write("Hello, Streamlit!")


    def data_exploration_page():
        # File Upload
        uploaded_file = st.file_uploader("Choose a CSV file to upload Employee Data", type="csv")

        # Display the contents file as a Pandas DataFrame
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Uploaded Dataset:")
                st.write(df)

                # Allow users to sort and filter the table
                sort_column = st.selectbox("Sort by:", df.columns)
                filtered_df = df.sort_values(by=sort_column)

                # Display the sorted and filtered table
                st.dataframe(filtered_df)

                # Allow users to filter by department
                department_filter = st.multiselect("Filter by Department:", df['Department'].unique())
                if department_filter:
                    filtered_df = filtered_df[filtered_df['Department'].isin(department_filter)]

                # Display the final table
                st.dataframe(filtered_df)

                # Data Editing
                st.header("Edit an Employee Record")
                row_index_to_edit = st.number_input("Enter the Employee ID to edit:", min_value=1, max_value=len(df), step=1)
                row_index_to_edit -= 1
                # Create placeholders for user input
                new_employeeid = st.number_input("Enter new Employee ID:", value=df.loc[row_index_to_edit, 'EmployeeID'])
                new_name = st.text_input("Enter new Name:", df.loc[row_index_to_edit, 'Name'])
                new_position = st.text_input("Enter new Position:", df.loc[row_index_to_edit, 'Position'])
                new_department = st.text_input("Enter new Department:", df.loc[row_index_to_edit, 'Department'])
                new_salary = st.number_input("Enter new Salary:", value=df.loc[row_index_to_edit, 'Salary'])

                if st.button("Edit Record"):
                    # Update the DataFrame with edited values
                    df.at[row_index_to_edit, 'Name'] = new_name
                    df.at[row_index_to_edit, 'Department'] = new_department
                    df.at[row_index_to_edit, 'Position'] = new_position
                    df.at[row_index_to_edit, 'Salary'] = new_salary
                    df.at[row_index_to_edit, 'EmployeeID'] = new_employeeid

                    # Display the updated data table
                    st.success("Record updated successfully!")
                    st.dataframe(df)

                # Section for adding new records
                st.header("Add New Employee Record")

                # Form for adding new records
                new_employeeID_form = st.number_input("Enter new employee ID:")
                new_name_form = st.text_input("Enter new name:")
                new_position_form = st.text_input("Enter new position:")
                new_department_form = st.text_input("Enter new department:")
                new_salary_form = st.number_input("Enter new salary:")

                # Button to add new record
                if st.button("Add New Record"):
                    # Add a new row to the DataFrame
                    new_record = {'EmployeeID': new_employeeID_form, 'Name': new_name_form, 'Position': new_position_form, 'Department': new_department_form, 'Salary': new_salary_form}
                    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)

                    # Display the updated data table
                    st.success("New record added successfully!")
                    st.dataframe(df)

                # Allow users to delete specific records
                row_index_to_delete = st.number_input("Enter the Employee ID to delete:", min_value=1, max_value=len(df), step=1)
                row_index_to_delete -= 1

                if st.button("Delete Record"):
                    # Delete the specified row
                    df = df.drop(index=row_index_to_delete).reset_index(drop=True)

                    # Display the updated data table
                    st.warning("Record deleted successfully!")
                    st.dataframe(df)

                # Data Visualization Section
                st.header("Data Visualization")

                # Salary Distribution Plot
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.subheader("Salary Distribution")
                sns.histplot(df['Salary'], bins=20, kde=True)
                st.pyplot()

                # Department-wise Employee Count
                st.subheader("Department-wise Employee Count")
                fig, ax = plt.subplots()
                sns.countplot(x='Department', data=df, ax=ax)
                st.pyplot(fig)

                # Advanced Filtering Section
                st.header("Advanced Filtering")

                # Filter by Department and Salary Range
                selected_department = st.selectbox("Filter by Department:", ['All'] + list(df['Department'].unique()))
                selected_salary_range = st.slider("Filter by Salary Range:", min_value=int(df['Salary'].min()), max_value=int(df['Salary'].max()), value=(int(df['Salary'].min()), int(df['Salary'].max())))

                # Apply filters
                filtered_df = df.copy()
                if selected_department != 'All':
                    filtered_df = filtered_df[filtered_df['Department'] == selected_department]
                filtered_df = filtered_df[(filtered_df['Salary'] >= selected_salary_range[0]) & (filtered_df['Salary'] <= selected_salary_range[1])]

                # Display the filtered data table
                st.dataframe(filtered_df)

                # Data Export Section
                st.header("Data Export")

                # Button to export data as CSV
                if st.button("Export Data as CSV"):
                    csv_data = filtered_df.to_csv(index=False)
                    b64 = base64.b64encode(csv_data.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="employee_data.csv">Download CSV File</a>'
                    st.markdown(href, unsafe_allow_html=True)

            # Error Handling    
            except pd.errors.ParserError:
                st.error("Unable to parse the CSV file. Please make sure it's a valid CSV file.")

        # Slider to adjust a numerical value
        st.header("Interactive Slider")
        slider_value = st.slider("Select a numerical value:", min_value=1, max_value=10, value=5)

        # Display the selected value
        st.write(f"Selected Value: {slider_value}")

        # Create a line chart with the adjusted numerical value
        x = np.linspace(0, 10, 100)
        y = x ** 2
        y_adjusted = x ** slider_value

        fig, ax = plt.subplots()
        ax.plot(x, y_adjusted, label=f'y = x^{slider_value}')
        ax.legend()
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')

        # Show the plot using Streamlit's st.pyplot() function
        st.pyplot(fig)


    def settings_page():
        st.title("Settings Page")
        st.write("Configure your app settings here.")


    def feedback_page():
        # Feedback System
        st.header("Feedback System")

        feedback = st.text_area("Submit your feedback:")
        submit_feedback = st.button("Submit Feedback")

        if submit_feedback:
            # Process and store feedback (you can customize this part)
            st.success("Feedback submitted successfully!")


    # Multiple Pages
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ("Home", "Data Exploration", "Settings", "Feedback"))

    if page == "Home":
        home_page()
    elif page == "Data Exploration":
        data_exploration_page()
    elif page == "Settings":
        settings_page()
    elif page == "Feedback":
        feedback_page()
