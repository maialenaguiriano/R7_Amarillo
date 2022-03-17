from unicodedata import name
from scipy.fft import fftfreq
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import numpy as np
import funciones as fn
import pickle

with open('../Modelos/model_general.pkl', 'rb') as handle:
    modelo_general = pickle.load(handle)

with open('../Modelos/model_sector.pkl', 'rb') as handle:
    modelo_sector = pickle.load(handle)

with open('../Modelos/model_pequeñas.pkl', 'rb') as handle:
    modelo_pequeñas = pickle.load(handle)

with open('../Modelos/model_medianas.pkl', 'rb') as handle:
    modelo_medianas = pickle.load(handle)

with open('../Modelos/model_grandes.pkl', 'rb') as handle:
    modelo_grandes = pickle.load(handle)



app = Flask(__name__)

app.secret_key = 'ksdjdnnjksd'

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        nombre = request.form['name'] 
        session['name'] = nombre
        models = request.form['models'] 
        session['models'] = models
        if len(nombre) == 9:
            if models == 'tamaño':
                return redirect('/introducir_datos_tamaño')
            else:
                return redirect('/introducir_datos') 
        else:
            msg = 'El NIF debe contener 9 caracteres'
            return render_template('login.html', msg = msg)
 



@app.route('/introducir_datos', methods = ['GET', 'POST'])    
def introducir_datos():
    if request.method == 'GET':
        return render_template('introducir_datos.html', nombre = session['name'])
    else:
        a_circulante = request.form['a_circulante'] 
        session['a_circulante'] = a_circulante

        p_liquido = request.form['p_liquido'] 
        session['p_liquido'] = p_liquido

        total_a = request.form['total_a'] 
        session['total_a'] = total_a

        total_p = request.form['total_p'] 
        session['total_p'] = total_p

        r_de_e = request.form['r_de_e'] 
        session['r_de_e'] = r_de_e

        f_p = request.form['f_p'] 
        session['f_p'] = f_p

        otros_a_liquidos = request.form['otros_a_liquidos'] 
        session['otros_a_liquidos'] = otros_a_liquidos

        deudores = request.form['deudores'] 
        session['deudores'] = deudores

        # deuda_neta = request.form['deuda_neta'] 
        # session['deuda_neta'] = deuda_neta

        ebitda = request.form['ebitda'] 
        session['ebitda'] = ebitda

        c_f = request.form['c_f'] 
        session['c_f'] = c_f

        tesoreria = request.form['tesoreria'] 
        session['tesoreria'] = tesoreria

        return redirect('introducir_datos_3')



@app.route('/introducir_datos_3', methods = ['GET', 'POST'])    
def introducir_datos_3():
    if request.method == 'GET':
        return render_template('introducir_datos_3.html', nombre = session['name'])
    else:
        a_circulante3 = request.form['a_circulante3'] 
        session['a_circulante3'] = a_circulante3

        p_liquido3 = request.form['p_liquido3'] 
        session['p_liquido3'] = p_liquido3

        total_a3= request.form['total_a3'] 
        session['total_a3'] = total_a3

        total_p3 = request.form['total_p3'] 
        session['total_p3'] = total_p3

        r_de_e3 = request.form['r_de_e3'] 
        session['r_de_e3'] = r_de_e3

        f_p3 = request.form['f_p3'] 
        session['f_p3'] = f_p3

        otros_a_liquidos3 = request.form['otros_a_liquidos3'] 
        session['otros_a_liquidos3'] = otros_a_liquidos3

        deudores3 = request.form['deudores3'] 
        session['deudores3'] = deudores3

        # deuda_neta3 = request.form['deuda_neta3'] 
        # session['deuda_neta3'] = deuda_neta3

        ebitda3 = request.form['ebitda3'] 
        session['ebitda3'] = ebitda3

        c_f3 = request.form['c_f3'] 
        session['c_f3'] = c_f3

        tesoreria3 = request.form['tesoreria3'] 
        session['tesoreria3'] = tesoreria3

        if session['models'] == 'general':
            return redirect('prediccion_general') 

        elif session['models'] == 'sector':
            return redirect('prediccion_sector')
        else:
            pass


@app.route('/prediccion_general')    
def prediccion_general():
    x = np.array(fn.calcular_ratios(session['a_circulante'], session['a_circulante3'], session['p_liquido'],session['p_liquido3'],session['total_a'],session['total_a3'],session['total_p'],session['total_p3'],session['r_de_e'],session['r_de_e3'],
    session['f_p'],session['f_p3'], session['otros_a_liquidos'], session['otros_a_liquidos3'],session['deudores'], session['deudores3'],session['ebitda'],session['ebitda3'],session['c_f'],session['c_f3'],session['tesoreria'], session['tesoreria3'])).reshape(1,-1)

    y = modelo_general.predict(x)
    z= int(y[0])
    
    if z == 0:
        y = 'La calidad crediticia de la empresa es estable, hay un riesgo bajo de default.'
    else:
        y = 'El riesgo crediticio es alto, no es aconsejable conceder un aval.'

    return render_template('prediccion_general.html', y = y, nombre = session['name'])

@app.route('/prediccion_sector')    
def prediccion_sector():
    x = np.array(fn.calcular_ratios(session['a_circulante'], session['a_circulante3'], session['p_liquido'],session['p_liquido3'],session['total_a'],session['total_a3'],session['total_p'],session['total_p3'],session['r_de_e'],session['r_de_e3'],
    session['f_p'],session['f_p3'], session['otros_a_liquidos'], session['otros_a_liquidos3'],session['deudores'], session['deudores3'],session['ebitda'],session['ebitda3'],session['c_f'],session['c_f3'],session['tesoreria'], session['tesoreria3'])).reshape(1,-1)

    y = modelo_sector.predict(x)
    z = int(y[0])

    if z == 0:
        y = 'La calidad crediticia de la empresa es estable, hay un riesgo bajo de default.'
    else:
        y = 'El riesgo crediticio es alto, no es aconsejable conceder un aval.'
    
    return render_template('prediccion_sector.html', y = y, nombre = session['name'])


@app.route('/introducir_datos_tamaño', methods = ['GET', 'POST'])    
def introducir_datos_tamaño():
    if request.method == 'GET':
        return render_template('introducir_datos_tamaño.html', nombre = session['name'])
    else:
        a_circulante_t = request.form['a_circulante_t'] 
        session['a_circulante_t'] = a_circulante_t

        p_liquido_t = request.form['p_liquido_t'] 
        session['p_liquido_t'] = p_liquido_t

        total_a_t = request.form['total_a_t'] 
        session['total_a_t'] = total_a_t

        total_p_t = request.form['total_p_t'] 
        session['total_p_t'] = total_p_t

        r_de_e_t = request.form['r_de_e_t'] 
        session['r_de_e_t'] = r_de_e_t

        f_p_t = request.form['f_p_t'] 
        session['f_p_t'] = f_p_t

        otros_a_liquidos_t = request.form['otros_a_liquidos_t'] 
        session['otros_a_liquidos_t'] = otros_a_liquidos_t

        deudores_t = request.form['deudores_t'] 
        session['deudores_t'] = deudores_t

        # deuda_neta_t = request.form['deuda_neta_t'] 
        # session['deuda_neta_t'] = deuda_neta_t

        ebitda_t = request.form['ebitda_t'] 
        session['ebitda_t'] = ebitda_t

        c_f_t = request.form['c_f_t'] 
        session['c_f_t'] = c_f_t

        tesoreria_t = request.form['tesoreria_t'] 
        session['tesoreria_t'] = tesoreria_t

        tamaños = request.form['tamaños'] 
        session['tamaños'] = tamaños

        return redirect('introducir_datos_tamaño3')

@app.route('/introducir_datos_tamaño3', methods = ['GET', 'POST'])    
def introducir_datos_tamaño3():
    if request.method == 'GET':
        return render_template('introducir_datos_tamaño3.html', nombre = session['name'], tamaños = session['tamaños'])
    else:
        
        a_circulante_t3 = request.form['a_circulante_t3'] 
        session['a_circulante_t3'] = a_circulante_t3

        p_liquido_t3 = request.form['p_liquido_t3'] 
        session['p_liquido_t3'] = p_liquido_t3

        total_a_t3= request.form['total_a_t3'] 
        session['total_a_t3'] = total_a_t3

        total_p_t3 = request.form['total_p_t3'] 
        session['total_p_t3'] = total_p_t3

        r_de_e_t3 = request.form['r_de_e_t3'] 
        session['r_de_e_t3'] = r_de_e_t3

        f_p_t3 = request.form['f_p_t3'] 
        session['f_p_t3'] = f_p_t3

        otros_a_liquidos_t3 = request.form['otros_a_liquidos_t3'] 
        session['otros_a_liquidos_t3'] = otros_a_liquidos_t3

        deudores_t3 = request.form['deudores_t3'] 
        session['deudores_t3'] = deudores_t3

        # deuda_neta_t3 = request.form['deuda_neta_t3'] 
        # session['deuda_neta_t3'] = deuda_neta_t3

        ebitda_t3 = request.form['ebitda_t3'] 
        session['ebitda_t3'] = ebitda_t3

        c_f_t3 = request.form['c_f_t3'] 
        session['c_f_t3'] = c_f_t3

        tesoreria_t3 = request.form['tesoreria_t3'] 
        session['tesoreria_t3'] = tesoreria_t3

        if session['tamaños'] == 'pequeña':
            return redirect('prediccion_pequeñas') 

        elif session['tamaños'] == 'mediana':
            return redirect('prediccion_medianas')
        else:
            return redirect('prediccion_grandes')



@app.route('/prediccion_pequeñas')    
def prediccion_pequeñas():
    x = np.array(fn.calcular_ratios(session['a_circulante_t'], session['a_circulante_t3'], session['p_liquido_t'],session['p_liquido_t3'],session['total_a_t'],session['total_a_t3'],session['total_p_t'],session['total_p_t3'],session['r_de_e_t'],session['r_de_e_t3'],
    session['f_p_t'],session['f_p_t3'], session['otros_a_liquidos_t'], session['otros_a_liquidos_t3'],session['deudores_t'], session['deudores_t3'],session['ebitda_t'],session['ebitda_t3'],session['c_f_t'],session['c_f_t3'],session['tesoreria_t'], session['tesoreria_t3'])).reshape(1,-1)

    y = modelo_pequeñas.predict(x)
    z= int(y[0])
    if z == 0:
        y = 'La calidad crediticia de la empresa es estable, hay un riesgo bajo de default.'
    else:
        y = 'El riesgo crediticio es alto, no es aconsejable conceder un aval.'
    return render_template('prediccion_pequeñas.html', y = y, nombre = session['name'])

@app.route('/prediccion_medianas')    
def prediccion_medianas():
    x = np.array(fn.calcular_ratios(session['a_circulante_t'], session['a_circulante_t3'], session['p_liquido_t'],session['p_liquido_t3'],session['total_a_t'],session['total_a_t3'],session['total_p_t'],session['total_p_t3'],session['r_de_e_t'],session['r_de_e_t3'],
    session['f_p_t'],session['f_p_t3'], session['otros_a_liquidos_t'], session['otros_a_liquidos_t3'],session['deudores_t'], session['deudores_t3'],session['ebitda_t'],session['ebitda_t3'],session['c_f_t'],session['c_f_t3'],session['tesoreria_t'], session['tesoreria_t3'])).reshape(1,-1)

    y = modelo_medianas.predict(x)
    z = int(y[0])
    if z == 0:
        y = 'La calidad crediticia de la empresa es estable, hay un riesgo bajo de default.'
    else:
        y = 'El riesgo crediticio es alto, no es aconsejable conceder un aval.'
        
    return render_template('prediccion_medianas.html', y = y, nombre = session['name'])

@app.route('/prediccion_grandes') 
def prediccion_grandes():
    x = np.array(fn.calcular_ratios_log(session['a_circulante_t'], session['a_circulante_t3'], session['p_liquido_t'],session['p_liquido_t3'],session['total_a_t'],session['total_a_t3'],session['total_p_t'],session['total_p_t3'],session['r_de_e_t'],session['r_de_e_t3'],
    session['f_p_t'],session['f_p_t3'], session['otros_a_liquidos_t'], session['otros_a_liquidos_t3'],session['deudores_t'], session['deudores_t3'],session['ebitda_t'],session['ebitda_t3'])).reshape(1,-1)

    y = modelo_grandes.predict(x)
    z = int(y[0])
    if z == 0:
        y = 'La calidad crediticia de la empresa es estable, hay un riesgo bajo de default.'
    else:
        y = 'El riesgo crediticio es alto, no es aconsejable conceder un aval.'
    
    return render_template('prediccion_grandes.html', y = y, nombre = session['name'])


if __name__ == '__main__':
    app.run(debug=True)

