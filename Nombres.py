import json
import requests
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.secret_key = "Esto no debería ir aqui."

@app.route("/")
def index():
     response = requests.get("https://api.genderize.io?name=peter")
     if(response.status_code == 200):
        response.json()
     return render_template("inicio.html")
     
@app.route("/datos",methods=["POST"])
def nombre():
   name = request.form.get("name", "Batman")
   broma = request.form.get("aburrido", "")
   response = requests.get("https://api.genderize.io?name="+name)
   response2 = requests.get("https://api.agify.io?name="+name)
   response3 = requests.get("https://api.nationalize.io?name="+name)
   if(response.status_code == 200):
        datos = response.json()
        datos["probability"] = round(datos["probability"] *100)
        if(response2.status_code == 200):
           datos.update(response2.json())
           if(response3.status_code == 200):
               response3 = response3.json()["country"]
               listapaises = []
               for i in response3:
                  response3Prob = i["probability"]
                  response3Prob = round(response3Prob*100)
                  response4 = requests.get("https://restcountries.com/v3.1/alpha/"+i["country_id"])
                  if(response4.status_code == 200):
                     response4 = response4.json()
                     response4[0]["ProbPais"] = response3Prob
                     listapaises.append(response4)
                  else:
                     return render_template("notFound.html")
               if(broma == "yes"):
                  response5 = requests.get("https://geek-jokes.sameerkumar.website/api?format=json")
                  if(response5.status_code == 200):
                     datos["broma"] = response5.json()["joke"]
                  else:
                     return render_template("notFound.html")
               else:
                  datos["broma"] = ""
               datos["listaPaises"] = listapaises
               return render_template("Resultados.html", datos = datos)
   return render_template("notFound.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)