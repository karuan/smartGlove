import time
from pydub import AudioSegment
from pydub.playback import play


song = AudioSegment.from_mp3("neverGonnaGiveYouUp.mp3")

play(song)

time.sleep(2)




