import requests
import re
import json
from whatsapp_api_client_python import API


#INSIRA AQUI O idInstance E O apiTokenInstance DA API
#SITE: https://green-api.com/en
greenAPI = API.GreenAPI(
    "idInstance", "apiTokenInstance"
)

#MUDE A MOEDA QUE DESEJAR AQUI, PADRÃO É BRL
CURRENCY = "BRL" 
PRICE_FILE = "last_price.json" #NOME DO ARQUIVO QUE FICARÁ SALVO OS ÚLTIMOS PREÇOS
TELEPHONE_NUMBER = "012345678900"  #SEU NÚMERO DE TELEFONE AQUI NO FORMATO CÓDIGO DO PAÍS + DDD + NUMERO, EX: 552140028922

#SUBSTITUA AQUI COM O LINK DO JOGO E O PREÇO DESEJADO EM SEGUIDA, NO FORMATO "LINK": VALOR
games = {
    "https://store.steampowered.com/app/242760/The_Forest/?curator_clanid=4777282": 20.00, #EXEMPLO PARA THE FOREST, SUBSTITUA COM O SEU
    "https://store.steampowered.com/app/1144200/Ready_or_Not/": 60.00 
}



def extract_game_id(url):
    match = re.search(r"store\.steampowered\.com/app/(\d+)", url)
    return match.group(1) if match else None


def check_price(GAME_ID):
    API_PRICE_URL = f"https://store.steampowered.com/api/appdetails?filters=price_overview&appids={GAME_ID}&currency={CURRENCY}"
    response = requests.get(API_PRICE_URL)
    data = response.json()
    
    if str(GAME_ID) in data and data[str(GAME_ID)]["success"]:
        price_info = data[str(GAME_ID)]["data"]["price_overview"]
        current_price = price_info["final"] / 100  #convertendo de centavos para reais
        
        #print(f"Preço atual em R$ {current_price}")
        return current_price
        

def get_game_info(GAME_ID):
    API_INFO_URL = f"https://store.steampowered.com/api/appdetails?appids={GAME_ID}&cc=us&filters=basic"
    response = requests.get(API_INFO_URL)
    data = response.json()
    if str(GAME_ID) in data and data[str(GAME_ID)]["success"]:
        game_data = data[str(GAME_ID)]["data"]
        game_name = game_data.get("name", "Nome Desconhecido")
        game_image = game_data.get("header_image", "Imagem Desconhecida")
        
        return game_name, game_image
        #print(f"Nome do Jogo: {game_name}")
        #print(f"Imagem do Jogo: {game_image}")
        
        
def save_current_price(price_data):
    with open(PRICE_FILE, "w") as file:
        json.dump(price_data, file, indent=4)        
        

def load_last_price():
    try:
        with open(PRICE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

    
def send_messages():
    last_price = load_last_price()
    current_price = {}
    
    for url, target_price in games.items():
        game_id = extract_game_id(url)
        
        if not game_id:
            print(f"Não foi possível extrair o ID do jogo da URL: {url}")
            continue
        
        game_name, game_image = get_game_info(game_id)
        game_price = check_price(game_id)
        mensagem = f"*Seu jogo atingiu o valor desejado!*\n_Nome do jogo:_ *{game_name}*\n_Preço atual do jogo:_ *R${game_price}*\n_Preço mínimo:_ R${target_price}\n"
        
        current_price[game_id] = game_price
        for_last_price = last_price.get(game_id)
        
        
        #IMPORTANTE RESSALTAR QUE, SE VOCÊ ALTERAR O PREÇO MÍNIMO DEPOIS E COM ISSO ELE NÃO ENVIAR A MENSAGEM MESMO COM O JOGO ABAIXO DO VALOR, O 
        #PROGRAMA SÓ ENVIARÁ A MENSAGEM QUANDO O VALOR DO JOGO SE ALTERAR OU SE VOCÊ APAGAR O ARQUIVO CRIADO
        if (for_last_price is None and game_price <= target_price) or (for_last_price is not None and game_price < for_last_price) or (for_last_price is not None and game_price > for_last_price and game_price <= target_price):
            response = greenAPI.sending.sendFileByUrl(f"{TELEPHONE_NUMBER}@c.us", game_image, "header_image", mensagem)
            print(response.data)
        else:
            print("Preço do jogo não atingiu o valor desejado.")
    save_current_price(current_price)
    

send_messages()