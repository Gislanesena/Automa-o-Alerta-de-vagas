import os 
import requests
from dotenv import load_dotenv


load_dotenv()

DISCORD_WEBHOOK_URL = os.environ.get ("DISCORD_WEBHOOK_URL")

TERMOS_BUSCA = ["data", "python", "information system", "cybersecurity"]

def buscar_vagas_por_termo(termo):
    """Busca as 3 vagas mais recentes na API da Remotive para um termo específico."""
    url = f"https://remotive.com/api/remote-jobs?search={termo}"
    
    print(f"Buscando vagas para o termo: {termo}...")
    response = requests.get(url)
    
    
    if response.status_code == 200:
        dados = response.json()
        
        return dados.get("jobs", [])[:3]
    else:
        print(f"Erro ao buscar vagas para {termo}: Status {response.status_code}")
        return []
    
def enviar_para_discord(vaga, termo):
        """Envia um cartão formatado (Embed) para o seu canal do Discord."""
        payload = {
            "username": "Bot Alerta de Vagas",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/3850/3850285.png",
            "embeds": [
                {
                    "title": vaga.get("title"),
                    "url": vaga.get("url"),
                    "description": f"**Área buscada:** {termo.upper()}\n**Empresa:** {vaga.get('company_name')}\n**Tipo:** {vaga.get('job_type')}",
                    "color": 3447003,  # Cor azul no Discord
                    "footer": {
                        "text": f"Publicado em: {vaga.get('publication_date')[:10]}"
                    }
                }
            ]
        }
    
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    
def main():
        
            if not DISCORD_WEBHOOK_URL:
                print("⚠️ ERRO: A variável DISCORD_WEBHOOK_URL não foi encontrada!")
                print("Configure a variável antes de rodar o script.")
            return
    
for termo in TERMOS_BUSCA:
            vagas = buscar_vagas_por_termo(termo)
        
            for vaga in vagas:
                enviar_para_discord(vaga, termo)
            
print("✅ Busca e envios concluídos com sucesso!")

if __name__ == "__main__":
        main()