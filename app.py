from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import logging

app = Flask(__name__)

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

# Cargar el modelo entrenado, scaler y las características seleccionadas
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')  # Asegúrate de tener tu scaler guardado
selected_features = joblib.load('selected_features.pkl')  # Cargar las características seleccionadas
app.logger.debug('Modelo, scaler y características cargados correctamente.')

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recibir datos del formulario
        datos = {
            'age': float(request.form['age']),
            'height': float(request.form['height']),
            'weight': float(request.form['weight']),
            'waistline': float(request.form['waistline']),
            'sight_left': float(request.form['sight_left']),
            'sight_right': float(request.form['sight_right']),
            'hear_left': float(request.form['hear_left']),
            'hear_right': float(request.form['hear_right']),
            'SBP': float(request.form['SBP']),
            'DBP': float(request.form['DBP']),
            'BLDS': float(request.form['BLDS']),
            'tot_chole': float(request.form['tot_chole']),
            'HDL_chole': float(request.form['HDL_chole']),
            'LDL_chole': float(request.form['LDL_chole']),
            'triglyceride': float(request.form['triglyceride']),
            'hemoglobin': float(request.form['hemoglobin']),
            'urine_protein': float(request.form['urine_protein']),
            'serum_creatinine': float(request.form['serum_creatinine']),
            'SGOT_AST': float(request.form['SGOT_AST']),
            'SGOT_ALT': float(request.form['SGOT_ALT']),
            'gamma_GTP': float(request.form['gamma_GTP']),
            'SMK_stat_type_cd': float(request.form['SMK_stat_type_cd']),
            'sex_Female': float(request.form['sex_Female']),
            'sex_Male': float(request.form['sex_Male'])
        }
        
        # Crear un DataFrame con los datos
        data_df = pd.DataFrame([datos])
        # Imprimir los datos a predecir
        app.logger.debug(f'Datos a predecir: {datos}')
        
        # Escalar los datos del nuevo DataFrame usando el mismo scaler que usaste para escalar los datos de entrenamiento
        scaled_nuevo_objeto_data = scaler.transform(data_df)
        
        # Crea un nuevo DataFrame con los datos escalados
        scaled_nuevo_objeto_df = pd.DataFrame(scaled_nuevo_objeto_data, columns=data_df.columns)
        
        # Selecciona las características relevantes para el modelo
        X_nuevo_objeto = scaled_nuevo_objeto_df[selected_features]
        
        # Realiza la predicción con el modelo entrenado
        predicciones = model.predict(X_nuevo_objeto)
        
        # Devolver la predicción como respuesta JSON
        return jsonify({'prediccion': predicciones[0]})
    
    except Exception as e:
        app.logger.error(f'Error en la predicción: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
