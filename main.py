from twilio.twiml.messaging_response import MessagingResponse, TwiML
from flask import Flask, request, url_for, jsonify

app = Flask(__name__, static_folder='media')


import class_bot



@app.route("/", methods=["POST", "GET"])
def main():
    data = request.json
    print(jsonify(data))
    print(request.form.to_dict(flat=False))
    commands = ['!play']

    bot = class_bot.BotWhatsapp()
    
    bot.get_user_msg()

    if not bot.error:
       instruction = bot.instruction
       if instruction == "!play":
           return bot.play()
       elif instruction == "!help":
           return bot.help()
    
    else:
       return bot.error

if __name__ == '__main__':
    app.run()