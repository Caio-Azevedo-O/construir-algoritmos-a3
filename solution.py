
import os
import requests
import folium
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv("SPTRANS_TOKEN")
CODIGO_LINHA = 841
API = "http://api.olhovivo.sptrans.com.br/v2.1"

s = requests.Session()

#region Auth
res = s.post(f"{API}/Login/Autenticar?token={TOKEN}")
res.raise_for_status()

if res.json() is not True:
    raise Exception("Falha na autenticação com a SPTrans.")

#endregion

#region Stops
res = s.get(
    f"{API}/Parada/BuscarParadasPorLinha?codigoLinha={CODIGO_LINHA}"
)
res.raise_for_status()
paradas = res.json()

#endregion

#region Positions
res = s.get(
    f"{API}/Posicao/Linha?codigoLinha={CODIGO_LINHA}"
)
res.raise_for_status()
posicoes = res.json()["vs"]
#endregion

#region Map
if paradas:
    centro = [paradas[0]["py"], paradas[0]["px"]]
elif posicoes:
    centro = [posicoes[0]["py"], posicoes[0]["px"]]
else:
    raise Exception("Nenhuma parada ou posição encontrada.")

m = folium.Map(location=centro, zoom_start=13)

for parada in paradas:
    folium.Marker(
        location=[parada["py"], parada["px"]],
        popup=parada["np"],
        icon=folium.Icon(color="red", icon="map-pin")
    ).add_to(m)

for onibus in posicoes:
    folium.Marker(
        location=[onibus["py"], onibus["px"]],
        popup=f"Ônibus {onibus['p']}",
        icon=folium.Icon(color="blue", icon="bus", prefix="fa")
    ).add_to(m)

m.save("mapa_onibus.html")

print("Mapa salvo em mapa_onibus.html")
#endregion
