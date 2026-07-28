from fastapi import FastAPI

app = FastAPI()

@app.get('/') # quando chegar um .get na rota (''/'')...

def raiz(): # ...me devolva um dicionario
    return {'Mensagem': 'API de Escola no ar'}

@app.get('/status')

def status():
    return {'status': 'OK', 'Versão': '1.0'}