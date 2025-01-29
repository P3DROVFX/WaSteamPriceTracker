# Steam Price Tracker para Whatsapp

**Script para monitoramento de jogos ou programas da steam com notificação através de mensagem usando whatsapp**

###Script utiliza a api para whatsapp: [Green API](https://green-api.com/en/docs/api/)

Abra o script pelo editor para configurar seus IDs da api do whatsapp, número de telefone ou id do grupo do whatsapp, link dos jogos a monitorar e seu preço mínimo.
**Utilize o agendador de tarefas do windows ou outra alternativa para iniciar o script, eu configurei para inicializar toda vez ao fazer login**
Exemplo de código para o arquivo .bat que irá rodar:
```
@echo off
cd D:\PYTHON\ScriptSteam
python PriceCheck.py
```
