# imports 
import streamlit as st
from openai import OpenAI
import requests


# statics
api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key=api_key)

# methods
# methods
def story_response(prompt, client):
    try:
        story_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # system prompt and user prompt
            messages=[
                {"role": "system", "content": "You are a best seller story writer. You will take user prompt and generate a 150 words short story for adults age 25-35"},
                {"role": "user", "content": f'{prompt}'}
            ],
            max_tokens=400,
            temperature=0.8
        )
        story = story_response.choices[0].message.content
        return story
    except Exception as e:
        st.info('An error occurred while generating the image', icon="🚨")
        return None

def design_response(story, client):
    try:
        design_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # system prompt and user prompt
            messages=[
                {"role": "system", "content": "Based on the story given, you will design a detailed image prompt for the cover of this story. The image prompt should include the theme of the story with relevant color, suitable for adults. The output should be within 100 characters."},
                {"role": "user", "content": f'{story}'}
            ],
            max_tokens=400,
            temperature=0.8
        )
        design_prompt = design_response.choices[0].message.content
        return design_prompt
    except Exception as e:
        st.info('An error occurred while generating the image', icon="🚨")
        return None

def cover_response(design_prompt, client):
    try:
        cover_response = client.images.generate(
            model='dall-e-2',
            prompt=f"{design_prompt}",
            size="256x256",
            quality="standard",
            n=1
        )
        image_url = cover_response.data[0].url
        return image_url
    except Exception as e:
        st.info('An error occurred while generating the image', icon="🚨")
        return None

# Inject custom CSS for the gradient text
st.markdown(
    """
    <style>
    .gradient-text {
        background: -webkit-linear-gradient(#ee7752, #e73c7e, #23a6d5, #23d5ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
    }
    .normal-text {
        display: inline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the text with the gradient and the star beside it
st.markdown('<h1><span class="gradient-text">AI Prompt Image Generator</span> <span class="normal-text">✨</span></h1>', unsafe_allow_html=True)

success_state = False

st.markdown("""---""")
with st.form('test'):
    st.write("This is for the user to key in information")
    msg = st.text_input(label = "Enter your story here: ")

    submitted = st.form_submit_button(label = "Submit")
    if submitted:
        if len(msg) == 0:
            st.info('No message Input given', icon="🚨")

        else:
            story = story_response(msg, client)
            if story is not None:
                st.markdown("""---""")
                st.write(story)
                st.markdown("""---""")
                design_prompt = design_response(story, client)
                if design_prompt is not None:
                    image_url = cover_response(design_prompt, client)
    
                    if image_url is not None:
                        # Inject custom CSS to center the image
                        st.markdown(
                            """
                            <style>
                            .centered-image {
                                display: flex;
                                justify-content: center;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
            
                        # Display the image centered
                        st.markdown(
                            f'<div class="centered-image"><img src="{image_url}" width="400"></div>',
                            unsafe_allow_html=True
                        )
                        st.write(design_prompt)
                        st.markdown("""---""")
            
                        st.success('You have successfully generated a story and an image prompt for the cover of the story 👏👏👏', icon="✅")
                        success_state = True
            
                        st.snow()

if success_state:
    st.info('Thank you for using this AI Prompter', icon="ℹ️")


            





