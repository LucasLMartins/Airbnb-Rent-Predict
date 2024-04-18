import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import random

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

# Utilizar o modelo treinado para fazer previsões com os dados pré-informados
pre_informed_data = pd.DataFrame({
    'titulo': [random.choice(['Apartmento acochegante', 'Casa tranquila', 'Condominio tranquilo']) for _ in range(3)],
    'tipo': [random.choice(['Apartamento', 'Casa', 'Condominio']) for _ in range(3)],
    'cidade': [random.choice(['Curitiba', 'Pinhais', 'São José dos Pinhais']) for _ in range(3)],
    'estado': [random.choice(['Paraná']) for _ in range(3)],
    'hospedes': [random.randint(1, 10) for _ in range(3)],
    'quartos': [random.randint(1, 5) for _ in range(3)],
    'camas': [random.randint(1, 10) for _ in range(3)],
    'banheiros': [random.randint(1, 5) for _ in range(3)],
    'Elevador': [random.randint(0, 1) for _ in range(3)],
    'Cozinha': [random.randint(0, 1) for _ in range(3)],
    'Microondas': [random.randint(0, 1) for _ in range(3)],
    'Fogão': [random.randint(0, 1) for _ in range(3)],
    'Mesadejantar': [random.randint(0, 1) for _ in range(3)],
    'Wi-Fi': [random.randint(0, 1) for _ in range(3)],
    'Ar-condicionado': [random.randint(0, 1) for _ in range(3)],
    'TV': [random.randint(0, 1) for _ in range(3)],
    'Secadordecabelo': [random.randint(0, 1) for _ in range(3)],
    'Xampu': [random.randint(0, 1) for _ in range(3)],
    'Condicionador': [random.randint(0, 1) for _ in range(3)],
    'Saboneteparaocorpo': [random.randint(0, 1) for _ in range(3)],
    'Águaquente': [random.randint(0, 1) for _ in range(3)],
    'MáquinadeLavar': [random.randint(0, 1) for _ in range(3)],
    'Secadora': [random.randint(0, 1) for _ in range(3)],
    'Café': [random.randint(0, 1) for _ in range(3)],
    'Fechadurainteligente': [random.randint(0, 1) for _ in range(3)],
    'Refrigerador': [random.randint(0, 1) for _ in range(3)],
    'Permitidoanimais': [random.randint(0, 1) for _ in range(3)],
    'Permitidofumar': [random.randint(0, 1) for _ in range(3)],
    'Banheira': [random.randint(0, 1) for _ in range(3)],
    'Produtosdelimpeza': [random.randint(0, 1) for _ in range(3)],
    'Básico': [random.randint(0, 1) for _ in range(3)],
    'Cabides': [random.randint(0, 1) for _ in range(3)],
    'Roupadecama': [random.randint(0, 1) for _ in range(3)],
    'Cinema': [random.randint(0, 1) for _ in range(3)],
    'Lareirainterna': [random.randint(0, 1) for _ in range(3)],
    'Espaçodetrabalhoexclusivo': [random.randint(0, 1) for _ in range(3)],
    'Itensbásicosdecozinha': [random.randint(0, 1) for _ in range(3)],
    'Louçasetalheres': [random.randint(0, 1) for _ in range(3)],
    'Frigobar': [random.randint(0, 1) for _ in range(3)],
    'Lavalouças': [random.randint(0, 1) for _ in range(3)],
    'Cafeteira': [random.randint(0, 1) for _ in range(3)],
    'Torradeira': [random.randint(0, 1) for _ in range(3)],
    'Entradaprivada': [random.randint(0, 1) for _ in range(3)],
    'Áreadejantarexterna': [random.randint(0, 1) for _ in range(3)],
    'Churrasqueira': [random.randint(0, 1) for _ in range(3)],
    'Estacionamentoincluído': [random.randint(0, 1) for _ in range(3)],
    'Jacuzziprivativa': [random.randint(0, 1) for _ in range(3)],
    'Vistaparaojardim': [random.randint(0, 1) for _ in range(3)],
})
print("Pre-informed data:")
for data in pre_informed_data.values:
    print(data)


# Align the columns of pre_informed_data with the training data
pre_informed_data_aligned = pre_informed_data.reindex(columns=X_train_encoded.columns, fill_value=0)

# Make predictions with the aligned data
predictions_pre_informed = model_encoded.predict(pre_informed_data_aligned)

print('Predicted values:', predictions_pre_informed)
