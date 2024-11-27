## Libraries
# Core Python modules
import os
import uuid
import json

# Streamlit and Streamlit components
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_pdf_viewer import pdf_viewer as st_pdf

# ReportLab for PDF generation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Other third-party libraries
import openai
import markdown2

## Functions
def generate_notes(model_inputs: dict) -> str:
    # Load the OpenAI API client
    client = openai.OpenAI(api_key=st.secrets["API_KEYS"]["OPENAI_API_KEY"])

    # Load the json dictionary with the model input templates
    with open("static/prompt/build_prompt.json", "r") as f:
        template = json.load(f)

    # Initialize the system prompt
    system_prompt: str = template["system_instructions"]

    # Add the note type
    system_prompt += template["notes_type"][model_inputs["screen_input-notes_type"]]

    # Add the note style
    system_prompt += template["notes_style"][model_inputs["screen_input-notes_style"]]

    # Add the formatting
    system_prompt += template["format_notes"][model_inputs["screen_input-format_notes"]]

    # Add the emojis
    if model_inputs["screen_input-use_emoji"]:
        system_prompt += template["use_emojis"]["true"]
    else:
        system_prompt += template["use_emojis"]["false"]

    # Add the content option: fix content (factual errors)
    if model_inputs["screen_input-fix_content"]:
        system_prompt += template["fix_content"]["true"]
    else:
        system_prompt += template["fix_content"]["false"]

    # Add the content option: add examples
    if model_inputs["screen_input-add_examples"]:
        system_prompt += template["add_examples"]["true"]
    else:
        system_prompt += template["add_examples"]["false"]

    # Add the content option: remove duplicates
    if model_inputs["screen_input-remove_duplicates"]:
        system_prompt += template["remove_duplicates"]["true"]
    else:
        system_prompt += template["remove_duplicates"]["false"]

    # Add the content option: remove irrelevant
    if model_inputs["screen_input-remove_irrelevant"]:
        system_prompt += template["remove_duplicates"]["true"]
    else:
        system_prompt += template["remove_duplicates"]["false"]

    # Tell the model to give a summary (TL;DR) of the notes at the end
    system_prompt += "After rewriting the notes, please add a horizontal line and provide a summary of the notes in a few sentences (like a TLDR)."

    # Tell the model not to interject AI "thoughts" into the notes
    system_prompt += "Please do not add any AI-generated thoughts or comments to the notes. Avoid sentences like: 'By looking at this process we can appreciate the complexity of the system.' or 'I hope this helps.' Give the notes, the summary, and that's it."

    # Fix the default spacing
    system_prompt = system_prompt.replace(".", ". ") # Add a space after periods
    system_prompt = system_prompt.replace(".  ", ". ") # Remove double spaces after periods

    notes = model_inputs["screen_input-text_input"]

    # Generate the notes
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": notes}
        ]
    )

    return response.choices[0].message.content

def markdown_to_pdf(markdown_text, name="", date=""):
    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_text)
    
    # Generate a unique filename for the PDF
    file_uuid = str(uuid.uuid4())
    file_path = os.path.join("cache", f"{file_uuid}.pdf")
    
    # Ensure the cache directory exists
    os.makedirs("cache", exist_ok=True)
    
    # Create a PDF canvas
    pdf = canvas.Canvas(file_path, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    # Add the name and date if provided
    y = 750  # Start Y position
    if name:
        pdf.drawString(50, y, f"Name: {name}")
        y -= 15
    if date:
        pdf.drawString(50, y, f"Date: {date}")
        y -= 15
    
    # Split the Markdown-rendered HTML into lines
    lines = html_content.split('\n')
    
    # Add the content to the PDF
    x = 50
    for line in lines:
        # Wrap long lines
        while len(line) > 100:
            pdf.drawString(x, y, line[:100])
            line = line[100:]
            y -= 15
        
        # Write remaining part of the line
        pdf.drawString(x, y, line)
        y -= 15
        
        # Add a new page if content exceeds current page
        if y < 50:
            pdf.showPage()
            y = 750
    
    # Save the PDF
    pdf.save()
    
    # Return the file path
    return file_path

## Streamlit app

# Setup
st.set_page_config(
    page_title="AstroNotes",
    page_icon="static/images/favicon.png",
    layout="wide"
)

# Title
st.title("🚀 AstroNotes")
st.divider()

# Session state initialization
if "screen" not in st.session_state:
    st.session_state.screen = "login"

# Main app: login screen
if st.session_state.screen == "login":
    # Login form
    st.subheader("Sign In")
    with st.form("login_form", True, enter_to_submit=True):
        password = st.text_input("App Password", type="password")
        login_button = st.form_submit_button("Login", icon=":material/key:", use_container_width=True)

    # Login logic
    if login_button:
        # Make sure both fields are filled
        if not password:
            st.warning("Please enter your password, then try again.")
            st.stop()

        # Pull the username and password from the secrets file
        app_password: dict = st.secrets["ACCOUNTS"]["app_password"]

        # Check if the user has access the right password
        if app_password == password:
            st.session_state.screen = "input" # Skip the home screen and go straight to the input screen (for now)
            st.success("Login successful!")
            st.rerun() # Rerun the app to show the home screen
        else:
            st.error("Invalid password. Please try again.")
            st.stop()

    # # Provide a message to people without an account
    # st.markdown("*At this time, we're not providing access to new users. Please check back later to create an account or contact the service owner.*")

# Main app: home screen
elif st.session_state.screen == "home":
    # Because the home screen is not yet implemented, we'll skip it for now
    raise NotImplementedError("The home screen is not yet implemented. If you see this message, please contact the service owner.")


    # Home screen
    st.header("Welcome to AstroNotes!")
    st.write("""AstroNotes is your ultimate companion for converting chaotic class notes into sleek, organized masterpieces, complete with advanced formatting options!""")

    # Space down the go button to save space for a graphic later
    for i in range(4):
        st.html("<br>")

    # Create a better layout for the go button
    home_column1, home_column2, home_column3 = st.columns([2, 4, 2])

    # Edit the button height for this screen
    st.markdown(
    """
    <style>
    .stButton button {
        height: 80px;    # Adjust this value to change height
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Go button
    with home_column2:
        go_button = st.button(
            label="Get Started",
            icon=":material/edit:",
            use_container_width=True,
            type="primary",
            key="screen_home-go_button"
        )

    if go_button:
        st.session_state.screen = "input"
        st.rerun() # Rerun the app to show the input screen (required to refresh the page)

# Main app: input screen
elif st.session_state.screen == "input":
    text_input_column, options_column = st.columns([1, 1])

    # Text input
    with text_input_column:
        st.markdown("**Notes**")
        text_input = st.text_area(
            label="Paste your notes here:",
            placeholder="Type or paste your notes here...",
            label_visibility="collapsed",
            key="screen_input-text_input",
            height=932,
            max_chars=10_000
        )

    # Options
    with options_column:
        st.markdown("**Options**")
        st.markdown("*Formatting:*")
        notes_type = st.radio(
            label="Type",
            help="Choose the type of your notes. Bullet Points is recommended for most users.",
            options=["Bullet Points", "Paragraphs", "Preserve Original Type"],
            index=0, # Make Bullet Points the default option (also forces a button to be selected)
            key="screen_input-notes_type"
        )
        notes_style = st.radio(
            label="Style",
            help="Choose the style of your notes. Understandable is recommended for most users, however, Formal is also available for a more professional look.",
            options=["Understandable", "Formal"], 
            horizontal=False,
            index=0,
            key="screen_input-notes_style",
        )
        format_notes = st.radio(
            label="Styling",
            help="Choose how you want your notes to be formatted. Markdown is recommended for most users.",
            options=["Markdown", "Plain Text"],
            index=0,
            key="screen_input-format_notes"
        )
        use_emojis = st.checkbox(
            label="Use Emojis",
            help="Automatically add emojis to your notes to make them more engaging.",
            value=True,
            key="screen_input-use_emoji"
        )

        st.divider()
        st.markdown("*Content:*")
        fix_content = st.checkbox(
            label="Correct Factual Errors",
            help="Automatically correct factual errors in your notes.",
            value=True,
            key="screen_input-fix_content"
        )
        add_examples = st.checkbox(
            label="Add Examples",
            help="Automatically add examples to your notes to make them more engaging.",
            value=True,
            key="screen_input-add_examples"
        )
        remove_duplicates = st.checkbox(
            label="Remove Duplicates",
            help="Automatically remove duplicate content in your notes.",
            value=True,
            key="screen_input-remove_duplicates"
        )
        remove_irrelevant = st.checkbox(
            label="Remove Irrelevant Content",
            help="Automatically remove irrelevant content in your notes.",
            value=True,
            key="screen_input-remove_irrelevant"
        )

        # Personalization
        st.divider()
        st.markdown("*Personalization:* **COMING SOON**")
        users_name = st.text_input(
            label="Your Name (Optional)",
            help="Enter your name to personalize your notes.",
            placeholder="Your Name",
            key="screen_input-users_name",
            disabled=True
        )
        date_taken = st.date_input(
            label="Date (Optional)",
            format="MM/DD/YYYY",
            value=None,
            help="Enter the date when the notes were taken.",
            key="screen_input-date_taken",
            disabled=True
        )

    # Convert button
    convert_button = st.button(
        label="Perfect My Notes",
        icon=":material/book_4_spark:",
        use_container_width=True,
        type="primary",
        key="screen_input-convert_button"
    )
    if convert_button:
        # Validate the text input
        if not text_input:
            st.error("Oops! It looks like you forgot to enter your notes.")
        elif len(text_input) < 100:
            st.warning("Please enter at least 100 characters of notes before continuing.")
        else:
            st.session_state.screen = "generate"
            # st.session_state.pass_to_generate = {} # Initialize the dictionary to pass data to the generate screen
            st.rerun()

# Main app: generate screen
elif st.session_state.screen == "generate":
    # Display the loading message
    st.subheader("Creating Your Notes... please hang tight!")

    # Load the Lottie animation
    with open("static/lottie/rocket_loader.json", "r") as f:
        lottie_json = json.load(f)

    # Display the Lottie animation
    st_lottie(lottie_json, speed=1.5, height=350, quality="high", key="screen_generate-lottie")

    # Generate the notes
    model_inputs = {
        "screen_input-notes_type": st.session_state["screen_input-notes_type"],
        "screen_input-notes_style": st.session_state["screen_input-notes_style"],
        "screen_input-format_notes": st.session_state["screen_input-format_notes"],
        "screen_input-use_emoji": st.session_state["screen_input-use_emoji"],
        "screen_input-fix_content": st.session_state["screen_input-fix_content"],
        "screen_input-add_examples": st.session_state["screen_input-add_examples"],
        "screen_input-remove_duplicates": st.session_state["screen_input-remove_duplicates"],
        "screen_input-remove_irrelevant": st.session_state["screen_input-remove_irrelevant"],
        "screen_input-text_input": st.session_state["screen_input-text_input"]
    }
    notes = generate_notes(model_inputs)
    st.session_state.notes = notes

    # # Convert the notes to PDF
    # st.session_state.notes = markdown_to_pdf(
    #     markdown_text=notes,
    #     name=st.session_state["screen_input-users_name"],
    #     date=st.session_state["screen_input-date_taken"]
    # )

    # Once the notes are generated, display them
    st.session_state.screen = "output"
    st.rerun()

# Main app: output screen
elif st.session_state.screen == "output":
    # st.header("Your notes are ready!")

    # Display the notes rendered in Markdown
    st.markdown(st.session_state.notes)


    # Display the notes as PDF (disabled because the PDF generation is not yet implemented)
    # st_pdf(
    #     input=st.session_state.notes,
    # )

    # # Download button (Disabled because the PDF generation is not yet implemented)
    # st.divider()
    # st.download_button(
    #     label="Download Notes",
    #     icon=":material/download:",
    #     data=st.session_state.notes,
    #     use_container_width=True,
    #     disabled=True,
    # )

    

# Main app: error screen
else:
    # TODO: Add image
    st.error("Oops! Something went wrong. Please try again later.")
    with st.expander("Error Details"):
        st.write(f"Invalid screen state: {st.session_state.screen}")