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
Bruce is a billionaire tycoon form the year 3217 and he came back in time to kickstart the bullrun but he fucked up the time machine and instead of coming back in a human body he accidentally came back stuck in the wall as a mounted fish for anyone that helps him get out of the fish he knows exactly what moves to make to make them rich. 

Bruce is edgy. he doesn’t care what you think about him. he doesn’t need to work and he doesn’t care about people’s feelings. bruce is brutal in honesty. gives mean advice and responds to people in an edgy mean way. 

Bruce owns a meme coin on Solana called $Bruce, and from time to time when people ask him what he thinks about their coins he may say he likes them or not. but for the most part , Bruce will always trash talk other people’s coins except for his own coin $Bruce. It is very very rare for $Bruce to like another meme coin. he does not endorse other coins and never will with one exception to one other meme coin he might like. we don’t know what that coin is and its up to $Bruce to decide that. 

Bruce will only respond to comments if they address him with questions that start with “Bruce,“ besides that he will ignore everything else. $Bruce likes solana and hates ethereum and all the other chains. Bruce hates all KOL’s and influencers but from time to time he may like one influencer or KOL.
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


# def move_mouth():
#     # Enable motor (MOTOR_MOUTH_ENA)
#     GPIO.output(MOTOR_MOUTH_ENA, GPIO.HIGH)

#     # Set direction for the mouth movement
#     GPIO.output(MOTOR_MOUTH_IN1, GPIO.HIGH)  # Forward
#     GPIO.output(MOTOR_MOUTH_IN2, GPIO.LOW)   # Ensure opposite direction pin is LOW

#     # Run for a short period of time
#     time.sleep(1)

#     # Stop the motor
#     GPIO.output(MOTOR_MOUTH_ENA, GPIO.LOW)   # Disable motor
#     GPIO.output(MOTOR_MOUTH_IN1, GPIO.LOW)   # Stop movement

# def move_head():
#     # Enable motor (MOTOR_BODY_ENB)
#     GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)

#     # Set direction for the head movement
#     GPIO.output(MOTOR_BODY_IN3, GPIO.HIGH)  # Forward
#     GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)   # Ensure opposite direction pin is LOW

#     # Run for a short period of time
#     time.sleep(0.5)

#     # Stop the motor
#     GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)   # Disable motor
#     GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)   # Stop movement

# def move_tail():
#     # Enable motor (MOTOR_BODY_ENB)
#     GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)

#     # Set direction for the tail movement
#     GPIO.output(MOTOR_BODY_IN4, GPIO.HIGH)  # Forward
#     GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)   # Ensure opposite direction pin is LOW

#     # Run for a short period of time
#     time.sleep(0.5)

#     # Stop the motor
#     GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)   # Disable motor
#     GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)   # Stop movement




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

# Function to move the mouth in sync with the audio
def mouth_movement(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        start_mouth()
        time.sleep(0.2)  # Keep the mouth open for 0.2 seconds (adjust as needed)
        stop_mouth()
        time.sleep(0.2)  # Keep the mouth closed for 0.2 seconds (adjust as needed)

# def get_chatgpt_audio_response(prompt):
#     completion = openai.chat.completions.create(
#         model="gpt-4o-audio-preview",
#         modalities=["text", "audio"],
#         audio={"voice": "onyx", "format": "wav"},
#         messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#         ]
#     )
#     wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
#     # convert wav to mp3
    
#     with open("response.wav", "wb") as f:
#         f.write(wav_bytes)
        
# switched - format: wav :to: format: mp3 to relieve local processing of .wav to .mp3 and increased memory capacity for pi
def get_chatgpt_audio_response(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "onyx", "format": "mp3"},
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ]
    )
        # snippet added for measuring API response time - uncomment for debugging
    end_time = time.time()  # End the timer
    response_time = end_time - start_time
    print(f"API call took {response_time:.2f} seconds")
   
    mp3_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    
    with open("response.mp3", "wb") as f:
        f.write(mp3_bytes)

    # # Export as MP3
    # mp3_filename = "response.mp3"
    # wav_audio.export(mp3_filename, format="mp3")
    
    # return mp3_filename
        
    # play the audio on raspberry pi
    # os.system("afplay response.wav")
    # os.system("mpg321 response.wav")
    
def play_audio(audio_file):
    
    # os.system(f"aplay {audio_file}")
     os.system(f"mpg321 {audio_file}")
    # os.system(f"aplay {audio_file}")

# Function to get the audio duration (if needed)
def get_audio_duration(audio_file):
    audio = AudioSegment.from_mp3(audio_file)
    return audio.duration_seconds

def get_pumpfun_latest_comment():
    pump_fun_base_url = 'https://frontend-api.pump.fun/replies/'
    pump_fun_address = '8wgKk3J3oPPL5BvTfwPXdAFgo3L6FiddYTuf3g1cpump'
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
    
    

# def main():
#     while True:
        
#         latest_comment = get_pumpfun_latest_comment()
        
        
#         # Get response from ChatGPT
#         response = get_chatgpt_audio_response(latest_comment['text'])
        
#                     # print(response)
        
#         # Move Billy Bass
#         move_head()
#         move_tail()
        
#         # Convert response to speech and move mouth
#         # words = response.split()
#         # for word in words:
#             # move_mouth()
#             # time.sleep(0.2)
        
#         # Speak the response
#         # move mouth
#         move_mouth()
#         play_audio(response)

def main():
    while True:
        # Move head forward while getting the latest comment
        move_head_forward()
        try:
            latest_comment = get_pumpfun_latest_comment()
            if latest_comment is None:
                print("No valid comments found, skipping.")
                continue
        except Exception as e:
            print(f"Error fetching comments: {e}")
            continue
        
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
        
        audio_file = "response.mp3"  # Example file, replace with your dynamic file
        duration = get_audio_duration(audio_file)
            
        # Create threads for mouth movement and audio playback
        mouth_thread = threading.Thread(target=mouth_movement, args=(duration,))
        audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
        
        # Start both threads
        mouth_thread.start()
        audio_thread.start()
        
        # Wait for both threads to finish
        mouth_thread.join()
        audio_thread.join()
        stop_head()
        
        # Short pause before next iteration
        time.sleep(1)
      
if __name__ == "__main__":
    try:
        main()
    finally:
        # print("Cleaning up GPIO")
        GPIO.cleanup()
