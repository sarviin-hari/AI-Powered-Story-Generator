# imports 
import streamlit as st
from openai import OpenAI
import requests


# statics
api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key=api_key)

# methods
def story_response(prompt, client):
  story_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # system prompt and user prompt
    messages=[
      {"role": "system", "content": "You are a best seller story writer. You will take user prompt and generate a 150 words short story for adults age 25-35"},
      {"role": "user", "content": f'{prompt}'}
    ],
    max_tokens = 400,  
    temperature = 0.8
  )

  story = story_response.choices[0].message.content
  return story

def design_response(story, client):

  design_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # system prompt and user prompt
    messages=[
      {"role": "system", "content": "Based on the story given, you will design a detailed image prompt for the cover of this story. The image prompt should include the theme of the story with relevant color, suitable for adults. The output should be within 100 characters."},
      {"role": "user", "content": f'{story}'}
    ],
    max_tokens = 400,  
    temperature = 0.8
  )

  design_prompt = design_response.choices[0].message.content
  return design_prompt

def cover_response(design_prompt, client):
  cover_response = client.images.generate(
      model='dall-e-2',
      prompt = f"{design_prompt}",  # in anime style
      size = "256x256",
      quality = "standard",
      n = 1
      # , response_format = "url"
  )

  image_url = cover_response.data[0].url
  print(image_url)
  return image_url

st.markdown("# AI Prompt Image Generator")

st.markdown("""---""")
with st.form('jesus_with_coffee'):
    st.write("This is for the user to key in information")
    msg = st.text_input(label = "Enter your story here: ")

    submitted = st.form_submit_button(label = "Submit")
    if submitted:
        if len(msg) == 0:
            st.write("No message input!")
        else:
            story = story_response(msg, client)
            st.markdown("""---""")
            st.write(story)
            st.markdown("""---""")
            design_prompt = design_response(story, client)
            st.write(design_prompt)
            st.markdown("""---""")
            image_url = cover_response(design_prompt, client)
            st.image(
                requests.get(image_url).content,
                width=400
            )

# design_prompt = design_response(story, client)
# st.write(design_prompt)
# image_url = cover_response(design_prompt, client)
# Disp.Image(requests.get(image_url).content) # Method 2
