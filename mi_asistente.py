"""

Asistente de voz desde el cual se puede consultar la fecha y la hora actuales, abrir Youtube, abrir el navegador
buscar en Wikipedia, buscar información en Google, reproducir directamente videos de Youtube o contar un chiste,
indicando todas estas ordenes por voz.

"""

import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opciones de voz/idioma
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# escuchar microfono y devolucion de audio en texto
def transformar_audio_en_texto():

    # almacenar reconocedor en una variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.5

        # informar que comenzo la grabacion
        print("Ya puedes hablar")

        # guardar audio
        audio = r.listen(origen)

        try:
            # buscar en google lo escuchado
            pedido = r.recognize_google(audio, language="es-es")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de no comprender el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("No entendí el audio")

            # devolver error
            return "Sigo esperando"

        # en caso de no devolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("No hay servicio")

            # devolver error
            return "Sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print("Algo ha salido mal")

            # devolver error
            return "Sigo esperando"

# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# informar dia de la semana
def pedir_dia():
    # variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    # crear variable para dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

# informar de la hora
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    # decir la hora
    hablar(hora)

# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour >20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 12:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    #decir el saludo
    hablar(f"{momento}, soy Helena tu asistente personal, Por favor dime en que te puedo ayudar")

# funcion central del asistente
def pedir_cosas():

    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    #loop central
    while comenzar:

        #activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        # abrir youtube
        if 'abrir youtube' in pedido or 'abre youtube' in pedido:
            hablar('Por supuesto, estoy abriendo Youtube')
            webbrowser.open('https://www.youtube.com/')
            continue

        # abrir navegador
        elif 'abrir navegador' in pedido or 'abre navegador' in pedido:
            hablar('Por supuesto, estoy abriendo el navegador')
            webbrowser.open('https://www.google.es/')
            continue

        # consultar el dia de hoy
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue

        # consultar la hora
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        # buscar en wikipedia
        elif 'busca en wikipedia' in pedido:
            hablar('Dame un segundo, estoy buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar(f'Wikipedia dice lo siguiente: {resultado}')
            continue

        # buscar información en google
        elif 'busca información' in pedido:
            hablar('Dame un segundo')
            pedido = pedido.replace('busca información', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue

        # reproducir video de youtube
        elif 'reproducir' in pedido:
            hablar('Buena idea, empiezo a reproducirlo')
            pedido = pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            continue

        # contar chiste
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        # consultar precio de las acciones
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'bitcoin':'BTC',
                       'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual} dólares')
                continue
            except:
                hablar("Perdón pero no la he encontrado")
                continue

        # cerrar la aplicación
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break

pedir_cosas()



