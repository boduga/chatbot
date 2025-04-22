import streamlit as st
# Import the Google Generative AI library
import google.generativeai as genai

# Siebar with a dropdown to select data source
st.sidebar.title("Select Data Source")
selected_data_source = st.sidebar.selectbox(
    "Select a dataset",
    ("Table A", "Table B")
)

# Write the selected data source to the main page
st.write(f"You selected: {selected_data_source}")


# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
    "To use this app, you need to provide a Google Cloud API key with the Gemini API enabled, "
    "or a Google AI Studio API key. You can get one [here](https://makersuite.google.com/app/apikey). "
    "This code is adapted from a Streamlit tutorial on building conversational apps."
)

# Ask user for their Google API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Configure the Google Generative AI client.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("The 'GOOGLE_API_KEY' is missing in your secrets configuration. Please add it to the .streamlit/secrets.toml file.")
    st.stop()

# Choose the model - gemini-pro is suitable for text chat
# You might check available models with genai.list_models()
model_name = "models/gemini-2.5-pro-exp-03-25"
model = genai.GenerativeModel(model_name)

#Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns. Initialize with a greeting from the assistant.
if "messages" not in st.session_state:
    # Gemini's chat history expects alternating user/model roles.
    # We'll store them in a list similar to the OpenAI example, but adapt for Gemini's format later.
    st.session_state.messages = []
    # Add an initial greeting if you like, but be mindful of the alternating role requirement for the API.
    # For simplicity in matching the original structure, we'll let the first user prompt start the actual API chat history.
    # If you wanted a system-like instruction or initial assistant message, you'd handle that differently
    # when preparing messages for the Gemini API call.

# Display the existing chat messages via `st.chat_message`.
# We display all messages stored in session_state.
for message in st.session_state.messages:
    # Map 'assistant' role to 'model' for internal handling if needed,
    # but for display, we can keep 'assistant' as it's common in UI.
    role = message["role"] if message["role"] != "model" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# Generator function to stream text from Gemini response chunks
def stream_data(response_object):
    for chunk in response_object:
        yield chunk.text

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    # Store as 'user' role for display purposes
    st.session_state.messages.append({"role": "user", "content": prompt + ". The user selected "})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the chat history for the Gemini API call.
    # The Gemini API expects messages in alternating 'user' and 'model' roles.
    # We need to convert our stored messages format if necessary, and ensure the history
    # sent to the API alternates correctly.
    # A simpler approach for a basic turn-based chat is to pass the history
    # directly if it already alternates user/assistant (model).
    # If the history might have non-alternating roles (e.g., multiple assistant
    # messages in a row), you might need to preprocess `st.session_state.messages`.
    # Assuming simple user-assistant turns:
    chat_history_for_gemini = []
    for msg in st.session_state.messages:
        # Convert 'assistant' to 'model' for the Gemini API
        role = msg["role"] if msg["role"] != "assistant" else "model"
        chat_history_for_gemini.append({"role": role, "parts": [msg["content"]]})


    # Start a chat session with the model, providing the history.
    # This allows the model to maintain context.
    chat_session = model.start_chat(history=chat_history_for_gemini[:-1]) # Exclude the current user message as it's the prompt

    # Generate a response using the Gemini API.
    # Send the latest user prompt to the chat session.
    try:
        # Use generate_content on the chat session
        response = chat_session.send_message(prompt, stream=True)
    except Exception as e:
        st.error(f"Error generating response from Gemini: {e}")
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
        with st.chat_message("assistant"):
            st.markdown(f"Error: {e}")
        st.stop() # Stop if API call fails


    # Stream the response to the chat using `st.write_stream`, then store it in
    # session state.
    # The Gemini response object handles streaming iteration.
    with st.chat_message("assistant"):
        # Gemini's response is iterable when stream=True
        response_text = st.write_stream(stream_data(response))

    # Store the full assistant response in session state with 'assistant' role for display.
    st.session_state.messages.append({"role": "assistant", "content": response_text})
