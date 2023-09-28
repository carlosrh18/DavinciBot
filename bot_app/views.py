from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Messages
import requests
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from storage import dropbox_folder_from, save_on_dropbox
import datetime
import emoji
import random
import numpy
import json
import random 



@csrf_exempt
def index(request):
    
        
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        num_media = int(request.values['NumMedia'])
        media = request.values.get('MediaContentType0', '')
        user_phone_number = request.values['From']
        print([media, num_media, user_phone_number])
        incoming_msg = request.POST['Body'].lower()
        print(incoming_msg)
        davincimsg = Messages(body=str(incoming_msg))
        davincimsg.save()
        
        
        

        # create Twilio XML response
        
        resp = MessagingResponse()
        msg = resp.message()

        responded = False

        if incoming_msg == 'hola' or incoming_msg == 'volver':
            response = emoji.emojize("""
*Bienvenidos a Café La Brisa* :wave:
Selecciona una opción :wave:
Desarrollado por www.roblesoft.com :deciduous_tree:
Contáctanos en facebook.com/roblesoft  :camera:

Opciones:
 :small_blue_diamond: *'Bebidas':* Explora nuestro menú de bebidas :coffee:
 :small_blue_diamond: *'Postres'*: Explora nuestro menú de postres :cake:
 :small_blue_diamond: *'Pizzas'*: Explora nuestro variado menú de pizzas :pizza:
 :small_blue_diamond: *'Hamburguesas'*: Explora nuestro variado menú de hamburguesas :hamburger:
 :small_blue_diamond: *'Horario'*: Consulta nuestros horarios :clock10:
 :small_blue_diamond: *'Pago':* Pagar usando paypal :credit_card:
 :small_blue_diamond: *'Ordenar':* Llamar a mesero para ordenar :credit_card:
 :small_blue_diamond: *'Politicas':* Politicas sanitarias respecto a la situación del COVID-19 :bulb:
 :small_blue_diamond: *'Meme':* Diviértete con los mejores memes mientras esperas tu orden :penguin:
  :small_blue_diamond: *'Fotos':* Explora las fotos de nuestros platillos y bebidas :camera:

""", use_aliases=True)
            msg.body(response)
            responded = True

        elif incoming_msg == 'bebidas':
            # return drinks menu
            response = emoji.emojize("""
*Menú de Bebidas* :coffee:


Opciones:
 :small_blue_diamond: *Café americano* --- $45 :coffee:
 :small_blue_diamond: *Refresco* --- $15 :cocktail:
 :small_blue_diamond: *Vino tinto* --- $250 :wine_glass:
 Regresar al menu principal: *volver* :arrow_backward:
 

""", use_aliases=True)
            msg.body(response)
            responded = True



        elif incoming_msg == 'postres':
            # return drinks menu
            response = emoji.emojize("""
*Menú de Postres* :coffee:


Opciones:
 :small_blue_diamond: *Pastel* --- $45 :coffee:
 :small_blue_diamond: *Brownie* --- $15 :cocktail:

 Regresar al menu principal: *volver* :arrow_backward:
 

""", use_aliases=True)

            msg.body(response)
            responded = True


        elif incoming_msg == 'pizzas':
            # return drinks menu
            response = emoji.emojize("""
*Menú de Pizzas* :coffee:


Opciones:
 :small_blue_diamond: *Hawaiiana* --- $200 :coffee:
 :small_blue_diamond: *Italiana* --- $235 :cocktail:
 
 Regresar al menu principal: *volver* :arrow_backward:
 

""", use_aliases=True)
            msg.body(response)
            responded = True


        elif incoming_msg == 'hamburguesas':
            # return drinks menu
            response = emoji.emojize("""
*Menú de Hamburguesas* :coffee:


Opciones:
 :small_blue_diamond: *Doble* --- $120 :coffee:
 :small_blue_diamond: *Sencilla* --- $80 :cocktail:
 
 Regresar al menu principal: *volver* :arrow_backward:
 

""", use_aliases=True)
            msg.body(response)
            responded = True

            



        elif incoming_msg == 'frase':
            # returns a quote
            r = requests.get('https://api.quotable.io/random')

            if r.status_code == 200:
                data = r.json()
                quote = f'{data["content"]} ({data["author"]})'

            else:
                quote = 'I could not retrieve a quote at this time, sorry.'

            msg.body(quote)
            responded = True

        elif incoming_msg == 'gato':
            # return a cat pic
            msg.media('https://cataas.com/cat')
            responded = True
            
        elif 'sigmoid' in incoming_msg:
            # return sigmoid function of input
            num = int(incoming_msg.split('d')[1])
            sigmoid = 1/(1+numpy.exp(-num))
            msg.body('La funcion sigmoid de {:.2f} es {:.2f}'.format(num,sigmoid))
            
                
            
            responded = True
            
        elif 'sum' in incoming_msg:
            # return a cat pic
            flags = incoming_msg.split('m')[1].split('+')
            num1 = flags[0]
            num2 = flags[1]
            msg.body('La suma de {:.2f} y {:.2f} es {:.2f}'.format(int(num1),int(num2),int(num1)+int(num2)))
            print(int(num1)+int(num2))
            responded = True
            
        elif 'gatogif' in incoming_msg:
            #return a cat gif
            if len(incoming_msg) > 7:
                msg.media('https://cataas.com/cat/says/'+incoming_msg.split('f',1)[1])
            else:
                msg.media('https://cataas.com/cat/gif')
            responded = True

        elif incoming_msg == 'perro':
            # return a dog pic
            r = requests.get('https://dog.ceo/api/breeds/image/random')
            data = r.json()
            msg.media(data['message'])
            responded = True
            
        elif incoming_msg == 'ya puedo salir?':
                # return a dog pic
            
            msg.body('Si, pero con cubrebocas, guardando sana distancia. Si no es necesario, no salgas')
            responded = True

        elif incoming_msg == 'horario':
                # return a dog pic
            
            msg.body('De 9 de la mañana a 10 de la noche de Lunes a Jueves')
            responded = True

        elif incoming_msg == 'ordenar':
                # return a dog pic
            
            msg.body('Un mesero viene en camino a tomar tu orden')
            responded = True

        elif incoming_msg == 'ya puedo salir?':
                # return a dog pic
            
            msg.body('Si, pero con cubrebocas, guardando sana distancia. Si no es necesario, no salgas')
            responded = True
            

        elif incoming_msg.startswith('recipe'):

            # search for recipe based on user input (if empty, return featured recipes)
            search_text = incoming_msg.replace('recipe', '')
            search_text = search_text.strip()
            
            data = json.dumps({'searchText': search_text})
            
            result = ''
            # updates the Apify task input with user's search query
            r = requests.put('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/input?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1', data = data, headers={"content-type": "application/json"})
            if r.status_code != 200:
                result = 'Sorry, I cannot search for recipes at this time.'

            # runs task to scrape Allrecipes for the top 5 search results
            r = requests.post('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')
            if r.status_code != 201:
                result = 'Sorry, I cannot search Allrecipes.com at this time.'

            if not result:
                result = emoji.emojize("I am searching Allrecipes.com for the best {} recipes. :fork_and_knife:".format(search_text),
                                        use_aliases = True)
                result += "\nPlease wait for a few moments before typing 'get recipe' to get your recipes!"
            msg.body(result)
            responded = True

        elif incoming_msg == 'get recipe':
            # get the last run details
            r = requests.get('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs/last?token=qTt3H59g5qoWzesLWXeBKhsXu')
            
            if r.status_code == 200:
                data = r.json()

                # check if last run has succeeded or is still running
                if data['data']['status'] == "RUNNING":
                    result = 'Sorry, your previous query is still running.'
                    result += "\nPlease wait for a few moments before typing 'get recipe' to get your recipes!"

                elif data['data']['status'] == "SUCCEEDED":

                    # get the last run dataset items
                    r = requests.get('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')
                    data = r.json()

                    if data:
                        result = ''

                        for recipe_data in data:
                            url = recipe_data['url']
                            name = recipe_data['name']
                            rating = recipe_data['rating']
                            rating_count = recipe_data['ratingcount']
                            prep = recipe_data['prep']
                            cook = recipe_data['cook']
                            ready_in = recipe_data['ready in']
                            calories = recipe_data['calories']

                            result += """
*{}*
_{} calories_

Rating: {:.2f} ({} ratings)
Prep: {}
Cook: {}
Ready in: {}
Recipe: {}
""".format(name, calories, float(rating), rating_count, prep, cook, ready_in, url)

                    else:
                        result = 'Sorry, I could not find any results for {}'.format(search_text)

                else:
                    result = 'Sorry, your previous search query has failed. Please try searching again.'

            else:
                result = 'I cannot retrieve recipes at this time. Sorry!'

            msg.body(result)
            responded = True

        elif incoming_msg == 'news':
            r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news,the-washington-post,the-wall-street-journal,cnn,fox-news,cnbc,abc-news,business-insider-uk,google-news-uk,independent&apiKey=3ff5909978da49b68997fd2a1e21fae8')
            
            if r.status_code == 200:
                data = r.json()
                articles = data['articles'][:5]
                result = ''
                
                for article in articles:
                    title = article['title']
                    url = article['url']
                    if 'Z' in article['publishedAt']:
                        published_at = datetime.datetime.strptime(article['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
                    else:
                        published_at = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                    result += """
*{}*
Read more: {}
_Published at {:02}/{:02}/{:02} {:02}:{:02}:{:02} UTC_
""".format(
    title,
    url, 
    published_at.day, 
    published_at.month, 
    published_at.year, 
    published_at.hour, 
    published_at.minute, 
    published_at.second
    )

            else:
                result = 'I cannot fetch news at this time. Sorry!'

            msg.body(result)
            responded = True

        elif incoming_msg.startswith('covid'):
            # runs task to aggregate data from Apify Covid-19 public actors
            requests.post('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/run-sync?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')
            
            # get the last run dataset items
            r = requests.get('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')
            
            if r.status_code == 200:
                data = r.json()

                country = incoming_msg.replace('covid', '')
                country = country.strip()
                country_data = list(filter(lambda x: x['country'].lower().startswith(country), data))

                if country_data:
                    result = ''

                    for i in range(len(country_data)):
                        data_dict = country_data[i]
                        last_updated = datetime.datetime.strptime(data_dict.get('lastUpdatedApify', None), "%Y-%m-%dT%H:%M:%S.%fZ")

                        result += """
*Statistics for country {}*
Infected: {}
Tested: {}
Recovered: {}
Deceased: {}
Last updated: {:02}/{:02}/{:02} {:02}:{:02}:{:03} UTC
""".format(
    data_dict['country'], 
    data_dict.get('infected', 'NA'), 
    data_dict.get('tested', 'NA'), 
    data_dict.get('recovered', 'NA'), 
    data_dict.get('deceased', 'NA'),
    last_updated.day,
    last_updated.month,
    last_updated.year,
    last_updated.hour,
    last_updated.minute,
    last_updated.second
    )
                else:
                    result = "Country not found. Sorry!"
            
            else:
                result = "I cannot retrieve statistics at this time. Sorry!"

            msg.body(result)
            responded = True

        elif incoming_msg.startswith('meme'):
            r = requests.get('https://www.reddit.com/r/memes/top.json?limit=20?t=day', headers = {'User-agent': 'your bot 0.1'})
            
            if r.status_code == 200:
                data = r.json()
                memes = data['data']['children']
                random_meme = random.choice(memes)
                meme_data = random_meme['data']
                title = meme_data['title']
                image = meme_data['url']

                msg.body(title)
                msg.media(image)
            
            else:
                msg.body('No puedo darte memes en este momento bro..')

            responded = True


        elif incoming_msg.startswith('fotos'):
            r = requests.get('https://www.reddit.com/r/foodphotography/top.json?limit=20?t=day', headers = {'User-agent': 'your bot 0.1'})
            
            if r.status_code == 200:
                data = r.json()
                memes = data['data']['children']
                random_meme = random.choice(memes)
                meme_data = random_meme['data']
                title = meme_data['title']
                image = meme_data['url']

                msg.body(title)
                msg.media(image)
            
            else:
                msg.body('No puedo acceder a las fotos en este momento..')

            responded = True
            
        elif incoming_msg == 'como estas?':
            msg.body("Bien gracias, no me quejo")
            
            responded = True


        elif incoming_msg == 'pago':
            msg.body("Para configurar la función de pago paypal contacta a www.roblesoft.com")
            
            responded = True

        elif incoming_msg == 'Quien es el mejor tio?':
            a = ["Tio Luis","Tio Medico","Tio Carlos"]
            tio = random.choice(a)
            msg.body(tio)

            responded = True
            

            

        if not responded:
             msg.body("No te entiendo, escribe hola para empezar")

        return HttpResponse(str(resp))
    
    if request.method == 'GET':
        
        flag = []
        mensajes = Messages.objects.all()
        for mensaje in mensajes:
            flag.append(mensaje)
            
        flagdict = {str(i): str(flag[i]) for i in range(0,len(flag))}
        print(flagdict)
        
        return JsonResponse(flagdict)
    
   
        