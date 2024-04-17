import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# Carregar os dados
data = pd.read_excel('dados_tratados.xlsx')

# Aplicar codificação One-Hot a todas as variáveis categóricas
data_encoded = pd.get_dummies(data, columns=['cidade','estado','titulo'])

# Dividir os dados em conjuntos de treinamento e teste
X_encoded = data_encoded.drop(['tipo','valor','url'], axis=1)
y_encoded = data_encoded['valor']
X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# Inicializar e treinar o modelo de regressão linear com os dados codificados
model_encoded = LinearRegression()
model_encoded.fit(X_train_encoded, y_train_encoded)

# Fazer previsões com os dados codificados
predictions_encoded = model_encoded.predict(X_test_encoded)

# Calcular o erro quadrático médio
mse_encoded = mean_squared_error(y_test_encoded, predictions_encoded)
rmse = np.sqrt(mse_encoded)
print('Mean Squared Error (Encoded):', mse_encoded)
print('Root Mean Squared Error:', rmse)

# Salvar o conjunto de dados com as previsões em um novo arquivo CSV
X_test_encoded['previsao_valor'] = predictions_encoded
X_test = data.loc[X_test_encoded.index, :]
X_test['previsao_valor'] = X_test_encoded['previsao_valor']
X_test.to_excel('previsao_valores.xlsx', index=False)
