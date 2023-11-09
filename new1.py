import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import sqlite3

#Page title #DONE
st.set_page_config(
    page_title ="Connecting Construction Experts: EnhanCEd Online Bidding Platform",
    page_icon="👷‍♀️🤝👷",)

#Sidebar
st.sidebar.title("Connecting Construction Experts: EnhanCEd Online Bidding Platform👷‍♀️‍🤝👷")
st.sidebar.write("🏗Bidding Smarter, Building Together🏗")

with st.sidebar:
    selected= option_menu(
        menu_title= 'Table of Contents',
        options= ["Profile", "Home", "Bidding", "About", "FAQS", "Feedback", "Report", "Code of Conduct", "Contacts"])
st.sidebar.header("To reach our company, contact us through: ")
st.sidebar.write("📧Email : civiltech.innovators@gmail.com")
st.sidebar.write("📞Phone # : +639364824532")
st.sidebar.write("☎️Landline : 402 - 2915")
st.sidebar.write("👍Facebook Page: CivilTech Innovators")
st.sidebar.write("🐦Twitter: @CivilTechInnovators")

# Function to hash the password
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to verify the hashed password
def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

# Function to create the user table if it doesn't exist
def create_user_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')
    conn.commit()

# Streamlit app
def main():
    st.title("Authentication Login and Registration")

    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    create_user_table(conn)

    # Streamlit login form
    st.header("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if the user exists in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (login_username,))
        user = cursor.fetchone()

        if user and verify_password(login_password, user[2]):
            st.success("Login Successful!")

            # Redirect to another page or tab after successful login
            st.experimental_set_query_params(login_success=True)
        else:
            st.error("Invalid username or password")

    # Streamlit registration form
    st.header("Register")
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        # Hash the password before storing
        hashed_password = hash_password(register_password)

        # Insert data into the users table
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (register_username, hashed_password))
            conn.commit()
            st.success("Registration Successful!")
        except sqlite3.IntegrityError:
            st.error("Username already exists. Please choose another.")

if __name__ == "__main__":
    main()

#Profile page
if selected == "Profile": #INSERT CODE FOR THIS
    st.header("My Profile")
    # Construction Project
    conn = sqlite3.connect('construction_projects.db')
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                budget REAL
            )
        ''')
    conn.commit()
    #Profile Tab
    def user_profile():
      st.subheader("My Profile")
      name = st.text_input("Name")
      age = st.number_input("Age")
      email = st.text_input("Email")
      address = st.text_area("Address")
      completed_project = st.text_area("Completed Project")

      user_profile()

    # Function to add a new project
    def add_project(name, description, budget):
        cursor.execute('INSERT INTO projects (name, description, budget) VALUES (?, ?, ?)', (name, description, budget))
        conn.commit()


    # Streamlit app
    st.title("Construction Project Upload")

    st.header("Upload a New Project")
    project_name = st.text_input("Project Name")
    project_description = st.text_area("Project Description")
    project_budget = st.number_input("Project Budget", min_value=0)

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "pdf", "jpg", "png", "zip"])

    if uploaded_file is not None:
        st.write("File Details:")
        file_details = {
            "Filename": uploaded_file.name,
            "File Size": f"{uploaded_file.size} bytes",
            "File Type": uploaded_file.type,
        }
        st.write(file_details)

        # Display the uploaded file
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            st.image(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            st.pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            st.text(uploaded_file.read().decode("utf-8"))
        else:
            st.warning("Unsupported file type. Please upload a supported file.")


    if st.button("Add Project") and project_name.strip() and project_budget > 0:
        add_project(project_name, project_description, project_budget)
        st.success(f"Project '{project_name}' added successfully.")
    else:
        st.warning("Please enter a valid project name and a project budget.")

    st.header("List of Projects")
    projects_df = pd.read_sql_query('SELECT id, name, description, budget FROM projects', conn)
    st.table(projects_df)

    # Close the database connection when done
    conn.close()



#Home page
elif selected== "Home":  #INSERT CODE FOR ANIMATION, INTRODUCTION, AND PROPOSED PROJECTS
    st.header('Connecting Construction Experts: EnhanCEd Online Bidding Platform👷‍♀️🤝👷')
    st.write('Are you a contractor seeking the perfect team for your construction project, or a skilled subcontractor eager to collaborate on exciting ventures? '
             'Look no further! Our Online Construction Project Bidding Platform is the bridge that connects your project dreams with the right expertise.')
    st.write('At the heart of our platform is a simple yet powerful goal – to foster collaboration between contractors (project owners) and subcontractors. Contractors use '
             'our platform to showcase their construction projects, complete with project names, descriptions, locations, budget ranges, and bid submission deadlines. '
             'Subcontractors, on the other hand, can browse these projects, submit their bids, and upload essential pricing details and documents.')
    st.write('Our platform transforms the construction industry by enabling contractors to access a vast network of subcontractors, making it easier than ever to bring '
             'their projects to life. For subcontractors, it is a doorway to exciting opportunities and the chance to work with contractors who value their expertise. Our '
             'platform not only fosters collaboration but also promotes competitive bidding, driving down project costs and ensuring that contractors get the best value for '
             'their construction projects.')
    st.write('Join us and be part of a thriving community where contractors and subcontractors unite, projects flourish, and the construction industry evolves. Welcome to '
             'a platform that is dedicated to your success in construction project bidding and beyond.')

#Bidding page
elif selected== "Bidding": #AAYUSIN PA
    # Create a SQLite database and table to store project details
    conn = sqlite3.connect('construction_bidding.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            budget REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY,
            project_id INTEGER,
            bidder_name TEXT,
            bid_amount REAL
        )
    ''')

    conn.commit()
    # Function to add a new project
    def add_project(name, description, budget):
        cursor.execute('INSERT INTO projects (name, description, budget) VALUES (?, ?, ?)', (name, description, budget))
        conn.commit()
    # Function to place a bid for a project
    def place_bid(project_id, bidder_name, bid_amount):
        cursor.execute('INSERT INTO bids (project_id, bidder_name, bid_amount) VALUES (?, ?, ?)',
                       (project_id, bidder_name, bid_amount))
        conn.commit()
    # Function to get project details and associated bids
    def get_project_details(project_id):
        cursor.execute('SELECT name, description, budget FROM projects WHERE id = ?', (project_id,))
        project_details = cursor.fetchone()

        cursor.execute('SELECT bidder_name, bid_amount FROM bids WHERE project_id = ?', (project_id,))
        bids = cursor.fetchall()

        return project_details, bids

    st.title("Construction Bidding Project")
    # Add a new project
    st.header("Add a New Project")
    project_name = st.text_input("Project Name")
    project_description = st.text_area("Project Description")
    project_budget = st.number_input("Project Budget", min_value=0)

    if st.button("Add Project"):
        if project_name.strip() and project_budget > 0:
            add_project(project_name, project_description, project_budget)
            st.success(f"Project '{project_name}' added successfully.")
        else:
            st.warning("Please enter a valid project name and a project budget.")

        if project_description.strip():
            st.success("Description valid")
        else:
            st.warning("Please provide project description")

    # Display a list of projects
    st.header("List of Projects")
    projects_df = pd.read_sql_query('SELECT id, name, description, budget FROM projects', conn)
    st.table(projects_df)

    # Allow bidders to place bids for a project
    st.header("Place a Bid")
    selected_project_id = st.selectbox("Select a Project", projects_df["name"], format_func=lambda x: f"{x}")
    bidder_name = st.text_input("Your Name")
    bid_amount = st.number_input("Bid Amount", min_value=0)
    if st.button("Place Bid"):
        place_bid(selected_project_id, bidder_name, bid_amount)
        st.success(
            f"{bidder_name} placed a bid of ${bid_amount} for '{projects_df[projects_df['id'] == selected_project_id]['name'].values[0]}'")

    # Display bids for a selected project
    st.header("Bids for Selected Project")
    selected_project_id = st.selectbox("Select a Project to View Bids", projects_df["name"],
                                       format_func=lambda x: f"{x}")
    project_details, bids = get_project_details(selected_project_id)
    st.write("Project Details:")
    st.write(f"Name: {project_details[0]}")
    st.write(f"Description: {project_details[1]}")
    st.write(f"Budget: ${project_details[2]:,.2f}")
    st.write("Bids:")
    if bids:
        bids_df = pd.DataFrame(bids, columns=["Bidder Name", "Bid Amount"])
        st.table(bids_df)
    else:
        st.info("No bids have been placed for this project yet.")

    # Close the database connection when done
    conn.close()

#About page
elif selected == "About": #DONE SA CONTENT
    st.title("ABOUT US🤔💭")
    #INSERT CODE FOR ANIMATION
    st.title("📌VISION")
    st.write("To be the leading and most innovative Online Construction Project Bidding Platform, connecting contractors and subcontractors worldwide, revolutionizing the construction industry through collaboration, efficiency, and value-driven solutions.")
    st.write("-------------------------------------")

    st.title("📌MISSION")
    st.write("To provide a user-friendly and efficient online platform that bridges the gap between contractors and subcontractors, offering a seamless experience for project owners and bidders. We strive to enable project owners to find the best teams for their construction projects and empower subcontractors to grow their businesses. We are committed to facilitating competitive bidding, enhancing project transparency, and driving down costs, ultimately ensuring the success of every construction endeavor.")
    st.write("-------------------------------------")

    st.title("📌GOAL")
    st.write("To enable seamless collaboration between contractors (project owners) and subcontractors through our online construction project bidding platform, fostering a thriving construction ecosystem. The platform aims to provide a user-friendly interface where contractors can showcase their projects, including project details and bid deadlines, while subcontractors can efficiently submit their bids, complete with pricing details and necessary documents. The ultimate goal is to expand the network of subcontractors available to contractors, promoting effective project development and encouraging competitive bidding to optimize project costs, thereby delivering the best value for construction projects.")
    st.write("-------------------------------------")

    st.title("📌VALUES")
    st.header("Collaboration ")
    st.write("We value fostering partnerships and teamwork between contractors and subcontractors, promoting synergy and shared success.")

    st.header("Efficiency  ")
    st.write("We are committed to streamlining the project bidding process, making it easier for users to manage projects and submit bids swiftly and effectively.")

    st.header("Transparency ")
    st.write("We prioritize open communication and transparency in project details and pricing, ensuring trust and fairness in the bidding process.")

    st.header("Quality ")
    st.write("We strive to facilitate the selection of the most qualified subcontractors, leading to high-quality construction outcomes for project owners.")

    st.header("Innovation ")
    st.write("We continuously seek innovative solutions to enhance the construction industry, providing tools and features that adapt to evolving needs.")

    st.header("Cost-Effectiveness ")
    st.write("We aim to drive down project costs by promoting competitive bidding, helping project owners obtain the best value for their construction projects.")

    st.header("Community Building ")
    st.write("We aim to drive down project costs by promoting competitive bidding, helping project owners obtain the best value for their construction projects.")

#FAQS page
elif selected == "FAQS": #DADAGDAGAN PA AND MAY INSERT CODE FOR ANIMATION
    st.title("FREQUENTLY ASKED QUESTIONS")
    st.write("Your questions, answered. ")

    st.header("1. What exactly is Connecting Construction Experts: EnhanCEd Online Bidding Platform? ")
    st.write("This online construction project bidding platform connects contractors (project owners) with subcontractors. Contractors can list their projects with details "
             "like project name, description, location, budget range, and bid deadline. Subcontractors can bid on projects and upload pricing and documents. "
             "The platform encourages collaboration, broadens subcontractor networks, and promotes competitive bidding to reduce project costs, providing the best value for "
             "owners. It streamlines project bidding, fostering cooperation and cost-efficiency in the construction industry.")

    st.header("2. How does competitive bidding work on the platform? ")
    st.write("Competitive bidding is facilitated by allowing subcontractors to submit their bids, driving down project costs. This helps contractors get the best value for "
             "their construction projects. ")

    st.header("3. Is there a fee to use this tool or is it free?")
    st.write("Registration and use of our Online Construction Project Bidding Platform are entirely free of charge. We believe in fostering collaboration and "
             "facilitating connections within the construction industry without imposing any fees on our users. You can enjoy the full range of features and benefits "
             "without incurring any costs.")

    st.header("4. Is the platform open to all contractors and subcontractors, or is it invitation-based? ")
    st.write("It is open to all contractors and subcontractors, providing an inclusive environment for professionals in the construction industry to connect, "
             "collaborate, and participate in competitive bidding. ")

    st.header("5. Can I cancel my bid after submission? ")
    st.write("While we encourage careful consideration before submitting a bid, we understand that circumstances may change. Users on our platform have the option to cancel "
             "or edit their bids after submission. ")

#Feedback page
elif selected == "Feedback": #INSERT CODE FOR ANIMATION
    feedback = st.text_area("Your Feedback")
    rating = st.slider("⭐️Rate the Application (1-5)⭐️", 1, 5)
    if st.button("Submit Feedback"):
        if rating == 5:
            st.write("Wow! Thanks for the 5-star rating! We're thrilled to have exceeded your expectations. Your support is greatly appreciated. ")
        elif rating == 4:
            st.write("We're glad you had a positive experience! Your 4-star rating motivates us to continue providing great service. ️")
        elif rating == 3:
            st.write("Thank you for your feedback, it helps us identify areas for improvement and provide a better experience. ")
        elif rating == 2:
            st.write("We apologize for falling short of your expectations. Your feedback will help us enhance our application. ")
        elif rating == 1:
            st.write("We're truly sorry for your disappointing experience. Your feedback is invaluable to us and will be used to make improvements. ")

#CODE OF CONDUCT PAGE
elif selected == "Code of Conduct":
    st.header("Connecting Construction Experts: EnhanCEd Online Bidding Platform's Code of Conduct" )
    st.write("The Online Construction Project Bidding Platform aims to connect contractors (project owners) and subcontractors, fostering collaboration, "
             "and promoting competitive bidding. To maintain the integrity of the platform and ensure a positive experience for all users, we have established "
             "this Bidding Code of Conduct. By participating in the platform, users agree to abide by the following guidelines.")

    st.subheader("📌FOR CONTRACTORS")
    st.subheader("Accurate Project Information")
    st.write("Contractors are responsible for providing accurate and detailed project information, including project name, description, location, budget range, and "
             "bid submission deadline. Misleading or false information is strictly prohibited.")

    st.subheader("Non-Discrimination")
    st.write("Contractors must not discriminate against subcontractors based on factors such as race, gender, nationality, or any other protected characteristics.")

    st.subheader("Fair Assessment")
    st.write("Contractors should evaluate subcontractor bids objectively, considering factors like qualifications, pricing, and experience, rather than biased judgments.")

    st.subheader("Timely Communication")
    st.write("Contractors should maintain open and timely communication with subcontractors regarding project details and expectations.")

    st.subheader("Payment and Contract Fulfillment")
    st.write("Contractors should uphold their commitments, including timely payment and fulfillment of the awarded contracts.")
    st.write("-------------------------------------")

    st.subheader("📌FOR SUBCONTRACTORS")
    st.subheader("Honest Bidding")
    st.write("Subcontractors should submit bids with accurate and honest pricing details, adhering to the provided budget range.")

    st.subheader("Qualification")
    st.write("Subcontractors must have the necessary qualifications and experience to complete the projects they bid on.")

    st.subheader("Timely Submission")
    st.write("Subcontractors are expected to submit bids within the specified bid submission deadline.")

    st.subheader("Professionalism")
    st.write("Subcontractors should maintain professionalism in their communication and interactions with contractors and other users on the platform.")

    st.subheader("Non-Interference")
    st.write("Subcontractors should not engage in collusion or interference with other subcontractors' bids or contractors' decisions.")
    st.write("-------------------------------------")

    st.subheader("📌FOR ALL USERS")
    st.subheader("No Fake Identities")
    st.write("Users must not create fake identities or provide false information on the platform.")

    st.subheader("No Misrepresentation")
    st.write(" Users must not misrepresent their qualifications, experience, or any other information related to their profile.")

    st.subheader("No Harassment or Abuse")
    st.write("Harassment, abusive language, or any form of bullying is strictly prohibited.")

    st.subheader("Legal Compliance")
    st.write("All users must comply with relevant laws and regulations in their jurisdiction.")

    st.subheader("Feedback and Reporting")
    st.write("Users are encouraged to provide feedback on their experiences and report any violations of the code of conduct.")

    st.subheader("Consequences of Violations")
    st.write("Violation of this code of conduct may result in temporary or permanent suspension from the platform.")

#REPORT PAGE
elif selected == "Report" :
        st.header("Report a User")
        user_to_report = st.text_input("Enter the username of the user that you want to report")
        reason = ["Select here", "Misrepresentation", "Inappropriate Content", "Suspicious or Fraudulent Activity",
                  "Intellectual Property Violations", "Non-Compliance with Codes of Conduct", "Privacy Violations", "Others"]
        select_reason = st.selectbox("Select a reason", reason)
        others = ""
        if select_reason == "Others":
            others = st.text_area("If you have another reason, state it here")
        if st.button("Submit"):
            if user_to_report.strip() and select_reason != "Select here":
                report_message = (f"User '{user_to_report}' reported successfully for '{select_reason}'. ")
                if others:
                    report_message += (f" Additional reason: '{others}'")
                st.success(report_message)
            else:
                st.warning("Please provide a valid username and select a reason.")

#Contacts Page
elif selected == "Contacts" :
    st.header("CivilTech Innovators🦺")
    st.header("Please Contact Us If You Have Any Concern")
    st.subheader("👷Engr. Clarince Julius S. Canillo")
    st.write("📱Contact Number: ")
    st.write("📧Email: 22-05547@g.batstate-u.edu.ph ")
    st.write("-------------------------------------")
    st.subheader("👷Engr. Kim Biner G. Deomampo")
    st.write("📱Contact Number: ")
    st.write("📧Email: 22-03442@g.batstate-u.edu.ph ")
    st.write("-------------------------------------")
    st.subheader("👷‍♀️Engr. Kaye Aira P. De Leon")
    st.write("📱Contact Number: 09602115398")
    st.write("📧Email: 22-01191@g.batstate-u.edu.ph ")
    st.write("-------------------------------------")
    st.subheader("👷Engr. Rainiel E. Reyes")
    st.write("📱Contact Number: ")
    st.write("📧Email: 22-04086@g.batstate-u.edu.ph ")
    st.write("-------------------------------------")
    st.subheader("👷Engr. Kim James Rodriguez")
    st.write("📱Contact Number: ")
    st.write("📧Email: 22-06174@g.batstate-u.edu.ph ")
