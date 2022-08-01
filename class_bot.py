
from flask import request, abort, send_from_directory, url_for
from flask import Response as response
from flask.views import MethodView
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
from googlesearch import search
from main import app

from pytube import YouTube
import os


#@app.route("/", methods=["POST"])
class BotWhatsapp():

    commands = ["!play", "!help"]
    error = None

    def __init__(self):
        self.response = MessagingResponse()
        self.message = Message()

    #@app.route("/", methods=["POST"])
    def get_user_msg(self):
        try:
            msg_split = request.values.get('Body', '').lower().split(" ", 1)

            self.instruction = msg_split[0]

            if self.instruction not in self.commands:
                self.response.message("Por favor ingrese un comando valido, teclea !help para conocer los comandos")

                self.error =  str(self.response)
            else:
                if msg_split[0] == "!play": 
                    self.user_msg = msg_split[1]
                elif msg_split[0] == "elif":
                    if request.values.get("MediaContentType0").endswith('.png', '.jpg', '.jpeg'):
                        self.media_Data = request.values.get("MediaUrl0", '')
                    else:
                        self.response.message("El archivo no es una imagen :(")

                        self.error = str(self.response)

        except:
            self.response.message("Por favor ingrese una sentencia para el comando")

            self.error = str(self.response)


    #@app.route("/", methods=["POST"])
    def play(self):
                    # User Query
            q = self.user_msg + " music.youtube.com"
        
            result = []
        

            # searching and storing urls
            for i in search(q, tld='co.in', num=1, stop=1):
               result.append(i)
        
            yt = YouTube(result[0])

            video = yt.streams.filter(only_audio=True)
            print(video.first())
            out_file = video.first().download()
            base, ext = os.path.splitext(out_file)
            dirname, basename = base.replace(" ", "").rsplit("/", 1)
            dirname = dirname + "/media/"
            filename = basename + ".mp3"
            new_file = dirname + filename
            os.rename(out_file, new_file)
            send_from_directory(path='media', 
                            directory=dirname,
                            filename=filename)
            
            print(out_file.split(" ", 1)[0])
            self.message.body(basename)
            self.message.media(url_for('static', filename=filename))
            self.response.append(self.message)
            return str(self.response)

    def help(self):
        for command in self.commands:
            self.response.message(command)
        
        return str(self.response)


#app.add_url_rule('/', methods=["POST"], view_func=BotWhatsapp().as_view(""))