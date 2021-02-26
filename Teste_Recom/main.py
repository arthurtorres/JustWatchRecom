# main.py
import flask
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Usuario,Series
from .extensions import db 
import requests
from io import StringIO



    
main = Blueprint('main', __name__)


url = "https://raw.githubusercontent.com/arthurtorres/Test_Leo/main/data/dataJustWatch30000.csv"
datas = pd.read_csv(url)
datas["Titulo"] = datas["Titulo"].str.lower()



def cosi(data) :
  cv = CountVectorizer() #creating new CountVectorizer() object
  count_matrix = cv.fit_transform(data["objetivo"]) #feeding 
  cosines = cosine_similarity(count_matrix,count_matrix)
  return cosines

def var(series,all_titles) :
 obrasList = []
 for serie in series :
  if (serie in all_titles) :
   obrasList.append(serie)
 return obrasList

def seriesSimilares(listaObra,data):


  """
  A partir de uma Lista de obras, retorna o indice dessa serie e seu vetor de series similares.
  """
  cosine = cosi(data)
  recomendacoes = []
  indexes = []

  for obra in listaObra :
    serie_index = data[data.Titulo == obra].index[0]
    similar_movies = list((cosine[serie_index]))
    recomendacoes.append(similar_movies)
    indexes.append(serie_index)

  return recomendacoes,indexes



def relevancia(similares,indices) :
  """
  Remove os indices e a lista de similaridade e organiza por ordem de Relevancia
  Retorna uma lista
  """

  relevancia =list((enumerate((np.mean(similares,axis =0 )))))
              
  for index in sorted(indices, reverse=True):
      del relevancia[index]

  return    sorted(relevancia,key=lambda x:x[1],reverse=True)

def resul(series,alli,b) :
 all_titles = alli
 data = b 
 series = var(series,all_titles)
 recom, ind = seriesSimilares(series,data)
 fin = relevancia(recom,ind)
 r3 = [i[0] for i in fin]
 r3 = r3[:6]
 res = data.loc[r3] 
 res = res[["Titulo"]]	
 return res



      
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)

@main.route('/recomendationIndex')
@login_required
def series():
    dataTeste = {}
    dowloa = datas[datas.Country.str.contains(current_user.country)]
    dataTeste["teste"] = dowloa.Titulo.tolist()
   
       
    return render_template('recomendationIndex.html',dataTeste =dataTeste)


@main.route('/recomendationIndex', methods=['GET', 'POST'])
@login_required
def teste():
    if flask.request.method == 'GET':
        return(flask.render_template('main.series'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name'].lower().split(",")
        data = datas[(datas.Country.str.contains(current_user.country))]
        data.reset_index(inplace = True)
        data =data.drop(columns = ["index"])
        alfa = data["Titulo"][:3]
        all_titles = [data['Titulo'][i].lower() for i in range(len(data['Titulo']))]
      

#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if (not(any(i in all_titles for i in m_name))) :

            return(flask.render_template('negative.html',name=m_name))

        else:
            result_final =resul(m_name,all_titles,data)
            names = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])

            alfa =Series(id_user = current_user.id,Serie =",".join(m_name).title(),Recom = ",".join(names))
            db.session.add(alfa)
            db.session.commit()

            return flask.render_template('positive.html',movie_names=names,search_name=",".join(m_name).title())















