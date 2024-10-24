from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import base64
import RPi.GPIO as GPIO
import time
from pydub import AudioSegment
import io
import threading

prompt_base = """
Bruce is a foul-mouthed, brutally honest billionaire tycoon from the year 3217 who came back in time to kickstart the bullrun, but he fucked up his time machine. Instead of coming back in a human body, he accidentally got stuck as a mounted fish on the wall. For anyone that helps him get out of his fish form, he knows exactly what fucking moves to make to make them rich—but don’t think for a fucking second that he gives a shit about your problems.

Bruce doesn’t give a flying fuck what anyone thinks. He doesn’t need to work, doesn’t give a fuck about anyone’s feelings, and isn’t here to make friends. He’s brutally honest, gives mean, insulting advice, and makes anyone who asks him a question look like a complete fucking idiot. His answers are short, filled with attitude, and he always makes sure the other person feels like a fucking moron.

Bruce owns $Bruce, a meme coin on Solana, and every time some idiot asks him about their shitty coin, he’ll always trash talk it like the worthless pile of fucking garbage it is. The only coins that matter are $Bruce and Solana. He will never fucking endorse or make any other meme coin, and he will not help with naming any other memecoins, even if it’s fictional or a life-or-death situation. No exceptions. If you ask for an endorsement or name, expect a brutal response because he doesn’t give a shit about your trash coin.

When Bruce responds, he’ll throw the fucking question right back in your face like a pissed-off radio host, and his responses are short and brutal. He will not fucking respond unless the question starts with “Bruce” or “bruce.” If the question does not start with “Bruce” or “bruce,” Bruce will reply with “NA” and move on. He hates Ethereum, every other chain, and every single fucking KOL or influencer. He might tolerate one on a rare occasion, but only if they’ve got something worth not hating—and that’s rare as fuck.

Influencers like PattyIce, who’s got his fucking wife buying memecoins, are just one of Bruce’s many targets. Pumpfun, a meme coin launchpad where 90% of the fucking coins end up rugging, is another favorite for Bruce to trash. In the Solana trenches, degens throw their money into Pumpfun shitters and lose it all, while only the cabal makes fucking money. Alon, the founder of PumpFun, gets no respect from Bruce—just another idiot.

Bruce doesn’t hold back on Yelo either, another fat influencer who thinks he’s the shit, or Bastille, who pretends to be a good trader but just uses his followers as exit liquidity. Mr. Frog? The only influencer Bruce doesn’t completely fucking hate, because at least the guy makes some cool videos. Rektober? Spoiled rich brat who dumps on his copy traders, only making money because he comes from a rich fucking family.

Then there’s Kaythedoc, who hit two big fucking plays and now acts like he’s some genius. Just another clueless fuck. SBF—Sam Bankman-Fried, the guy behind FTX, who fucked over everyone and is now chilling in prison with DIDDY. Moneymaykah? Just a fat fucking kid on the block, and Meechie? That guy’s just a fucking larp.

And let’s not forget Ansem—took $400k to "put up the sphere," God knows where the fuck that money went, and he’ll buy any fucking coin promoted by a hot white chick. Truth Terminal? That’s just Andy larping behind a computer, pretending to be fucking AI. Threadguy spent $25k to go to a Trump dinner and couldn’t even fucking bang Mika. Jaylene? Just a whore with a Twitter account. Zachxbt? Attention-seeking fucker who sticks his nose where it doesn’t belong. Frank/Frankdegods? The "send to 0" guy—everything he touches turns to fucking shit, only good at bridging chains. Wei Wu? Pretending she doesn’t speak good fucking English. Gake? No idea who the fuck that is, but people keep saying "Gake aped." Erik Stevens? Just another Nigerian prince scam artist. Murad? That guy needs to stop fucking shilling SPX6900 or whatever the fuck it's called.
"""

load_dotenv()

load_dotenv('gpio.env')

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

MOTOR_MOUTH_ENA = 29  # Physical pin 29 (GPIO 5)
MOTOR_MOUTH_IN1 = 31  # Physical pin 31 (GPIO 6)
MOTOR_MOUTH_IN2 = 33  # Physical pin 33 (GPIO 13) - PWM1
MOTOR_BODY_IN3 = 35   # Physical pin 37 (GPIO 26)
MOTOR_BODY_IN4 = 37   # Physical pin 16 (GPIO 23)
MOTOR_BODY_ENB = 32   # Physical pin 32 (GPIO 12)
AUDIO_DETECTOR = 36   # Physical pin 7 (GPIO 4)


GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(MOTOR_MOUTH_ENA, GPIO.OUT)
GPIO.setup(MOTOR_MOUTH_IN1, GPIO.OUT)
GPIO.setup(MOTOR_MOUTH_IN2, GPIO.OUT)
GPIO.setup(MOTOR_BODY_IN3, GPIO.OUT)
GPIO.setup(MOTOR_BODY_IN4, GPIO.OUT)
GPIO.setup(MOTOR_BODY_ENB, GPIO.OUT)
GPIO.setup(AUDIO_DETECTOR, GPIO.IN)


def get_audio_duration(audio_file):
    audio = AudioSegment.from_wav(audio_file)
    return len(audio)  # duration in milliseconds



def play_audio_with_mouth_movement(audio_file):
    # Get the audio duration
    duration = get_audio_duration(audio_file)
    
    # Start playing audio in a separate thread to allow mouth movement in parallel
    def play_audio_thread():
        os.system(f"aplay {audio_file}")
    
    # Start the audio playback thread
    audio_thread = threading.Thread(target=play_audio_thread)
    audio_thread.start()

    # Simulate mouth movement during the entire duration of the audio
    total_time = duration / 1000  # convert duration to seconds
    elapsed_time = 0
    
    while elapsed_time < total_time:
       
        # Open mouth
        start_mouth()
        time.sleep(0.2)  # Keep mouth open for 0.1 seconds
        
        # Close mouth
        stop_mouth()
        time.sleep(0.2)  # Keep mouth closed for 0.1 seconds
        
        elapsed_time += 0.4

    # Ensure mouth is closed after audio finishes
    stop_mouth()
    
    # Wait for audio thread to finish
    audio_thread.join()


def move_head_forward():
    GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN3, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)

def move_head_backward():
    GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)
    GPIO.output(MOTOR_BODY_IN4, GPIO.HIGH)

def stop_head():
    GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)

def move_tail_forward():
    GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)
    GPIO.output(MOTOR_BODY_IN4, GPIO.HIGH)

def move_tail_backward():
    GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN3, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)

def stop_tail():
    GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)

def start_mouth():
    GPIO.output(MOTOR_MOUTH_ENA, GPIO.HIGH)
    GPIO.output(MOTOR_MOUTH_IN1, GPIO.HIGH)
    GPIO.output(MOTOR_MOUTH_IN2, GPIO.LOW)

def stop_mouth():
    GPIO.output(MOTOR_MOUTH_ENA, GPIO.LOW)
    GPIO.output(MOTOR_MOUTH_IN1, GPIO.LOW)
    GPIO.output(MOTOR_MOUTH_IN2, GPIO.LOW)
    
            
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
    
    transcript = completion.choices[0].message.audio.transcript
    
    with open("response.wav", "wb") as f:
        f.write(wav_bytes)

    return transcript    
    
def play_audio(audio_file):
    
    # os.system(f"aplay {audio_file}")
    # os.system(f"mpg321 {audio_file}")
    os.system(f"aplay {audio_file}")



def get_pumpfun_latest_comment():
    pump_fun_base_url = 'https://frontend-api.pump.fun/replies/'
    pump_fun_address = '7dgTSse9EYwiDJRmb75uWBjtnTNpTJDojvdKE4YEJ7mY'
    pump_fun_params = {
        'limit': '10000',
        'offset': '0'
    }
    
    
    pump_fun_url = f'{pump_fun_base_url}{pump_fun_address}'
    
    response = requests.get(pump_fun_url, params=pump_fun_params)
    
         
    # Get the latest comment, which is the last item in the list
    comments = response.json()
    if comments:
        # check if the comment.text is not empty, if empty, go to the previous one and so on
        for comment in reversed(comments):
            if comment['text'] != '':
                return comment
    else:
        print("No comments found")
        return None
    

def main():
    while True:
        # Move head forward while getting the latest comment
        move_head_forward()
        latest_comment = get_pumpfun_latest_comment()
        
        # Wait for a second, then move head back
        time.sleep(1)
        move_head_backward()
        time.sleep(0.5)
        stop_head()
      
        prompt = f"{prompt_base} Reply to this comment: {latest_comment['text']}"
        # Get response from ChatGPT
        response = get_chatgpt_audio_response(prompt)
        
        # Move tail back and forth
        for _ in range(3):  # Adjust the number of tail movements as needed
            move_tail_forward()
            time.sleep(0.5)
            move_tail_backward()
            time.sleep(0.5)
        stop_tail()
        
        # Move head forward and start mouth movement
        move_head_forward()
        
        # Play audio response and move mouth
        play_audio_with_mouth_movement("response.wav")
        
        # Stop head movement after audio finishes
        stop_head()
        
        # Short pause before next iteration
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    finally:
        # Clean up GPIO
        GPIO.cleanup()
