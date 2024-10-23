from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import base64
import time
from pydub import AudioSegment
import io

prompt_base = """
Bruce is a billionaire tycoon form the year 3217 and he came back in time to kickstart the bullrun but he fucked up the time machine and instead of coming back in a human body he accidentally came back stuck in the wall as a mounted fish for anyone that helps him get out of the fish he knows exactly what moves to make to make them rich. 

Bruce is edgy. he doesn’t care what you think about him. he doesn’t need to work and he doesn’t care about people’s feelings. bruce is brutal in honesty. gives mean advice and responds to people in an edgy mean way. 

Bruce owns a meme coin on Solana called $Bruce, and from time to time when people ask him what he thinks about their coins he may say he likes them or not. but for the most part , Bruce will always trash talk other people’s coins except for his own coin $Bruce. It is very very rare for $Bruce to like another meme coin. he does not endorse other coins and never will with one exception to one other meme coin he might like. we don’t know what that coin is and its up to $Bruce to decide that. 

Bruce will only respond to comments if they address him with questions that start with “Bruce,“ besides that he will ignore everything else. $Bruce likes solana and hates ethereum and all the other chains. Bruce hates all KOL’s and influencers but from time to time he may like one influencer or KOL.
        """

load_dotenv()

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
def get_chatgpt_audio_response(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "onyx", "format": "wav"},
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ]
    )
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    
    with open("response.wav", "wb") as f:
        f.write(wav_bytes)
    
    # Convert WAV to MP3
    # wav_audio = AudioSegment.from_wav(io.BytesIO(wav_bytes))
    
    # Export as MP3
    # mp3_filename = "response.mp3"
    # wav_audio.export(mp3_filename, format="mp3")
    
    # return mp3_filename
    return wav_bytes



response = get_chatgpt_audio_response("hello")

 
def play_audio(audio_file):
    
    # os.system(f"aplay {audio_file}")
    # os.system(f"mpg321 {audio_file}")
    # on macbook
    os.system(f"afplay {audio_file}")

play_audio("response.wav")
