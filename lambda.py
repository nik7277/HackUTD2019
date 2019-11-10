#------------------------------Part1--------------------------------
# In this part we define a list that contains the player names, and 
# a dictionary with player biographies

GAME_LIST = ["tennis", "squash", "badminton", "cricket"]

GAME_PLAYERS = [
{
"game":"tennis", 
"players":
[{"Andy":"2019-11-10"},{"Roger":"2019-11-11"},{"Novak":"2019-11-12"}]
},
{
"game":"squash", 
"players":
[{"Peter":"2019-11-13"},{"Mark":"2019-11-14"}]
},
{
"game":"badminton", 
"players":
[{"Changbin":"2019-11-15"},{"Jackie":"2019-11-16"}]
},
{
"game":"cricket", 
"players":
[{"Sachin":"2019-11-17"},{"Virat":"2019-11-18"},{"Rohit":"2019-11-18"}]
}
]
#------------------------------Part2--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).

def find_players(game,dt):
    players = []
    for dct in GAME_PLAYERS:
        if dct['game'] == game:
            for player in dct['players']:
                for k,v in player.items():
                    if v == dt:
                        players.append(k)

    return 'The players who are playing '+ game + ' on ' +  dt + 'are : '+ ','.join(players)                  

def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()#------------------------------Part3--------------------------------
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi, welcome to the book a game Alexa Skill. The Available games are : " + ', '.join(map(str, GAME_LIST)) + ". "\
    "If you would like to know who is looking to play a game at your preferred time slot, you could say for example: book a game of Tennis on 11-10-2019"
    reprompt_MSG = "Do you want to do anything else"
    card_TEXT = "Choose a Game and Date"
    card_TITLE = "Choose a Game and Date"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")
    
#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request. 
# Since we have a few different intents in our skill, we need to 
# configure what this function will do upon receiving a particular 
# intent. This can be done by introducing the functions which handle 
# each of the intents.

def intent_scheme(event):
    intent_name = event['request']['intent']['name']
    print('##############################################');
    print('The name of the intent is : ',intent_name);
    print('##############################################');
    if intent_name == "bookgame":
        return game_bio(event)        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)#---------------------------Part3.1.1-------------------------------
# Here we define the intent handler functions
def game_bio(event):
    game=event['request']['intent']['slots']['sport']['value']
    dt=event['request']['intent']['slots']['date']['value']
    game_list_lower=[w.lower() for w in GAME_LIST]
    if game.lower() in game_list_lower:
        reprompt_MSG = "Do you want to know who is looking to play a game at your preferred time slot ?"
        card_TEXT = "You've picked " + game.lower()
        card_TITLE = "You've picked " + game.lower()
        return output_json_builder_with_reprompt_and_card(find_players(game.lower(),dt), card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "You haven't used the correct game and date "
        reprompt_MSG = "Do you want to know who is looking to play a game at your preferred time slot ?"
        card_TEXT = "Use the correct game and date"
        card_TITLE = "Wrong game."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "You can choose among these games: " + ', '.join(map(str, GAME_LIST))
    reprompt_MSG = "Do you want to know who is looking to play a game at your preferred time slot ?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to know who is looking to play a game at your preferred time slot ?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format. 
# That is why in this part of the code we define the functions which 
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to 
# build the output.

def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
