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

# # Fazer previsões com os dados codificados
# predictions_encoded = model_encoded.predict(X_test_encoded)

# # Calcular o erro quadrático médio
# mse_encoded = mean_squared_error(y_test_encoded, predictions_encoded)
# rmse = np.sqrt(mse_encoded)
# print('Mean Squared Error (Encoded):', mse_encoded)
# print('Root Mean Squared Error:', rmse)

# titulo = input("Digite o título do imóvel: ")
tipo = input("Digite o tipo do imóvel (Casa, Apartamento): ")
# cidade = input("Digite a cidade: (Curitiba, Pinhais, São José dos Pinhais)")
hospedes = input("Digite a quantidade de hóspedes: ")
quartos = input("Digite a quantidade de quartos: ")
camas = input("Digite a quantidade de camas: ")
banheiros = input("Digite a quantidade de banheiros: ")

# Utilizar o modelo treinado para fazer previsões com os dados pré-informados
pre_informed_data = pd.DataFrame({
    'titulo': ['Imóvel teste' for _ in range(1)],
    'tipo': [tipo for _ in range(1)],
    'cidade': ['Curitiba' for _ in range(1)],
    'estado': ['Paraná' for _ in range(1)],
    'hospedes': [int(hospedes) for _ in range(1)],
    'quartos': [int(quartos) for _ in range(1)],
    'camas': [int(camas) for _ in range(1)],
    'banheiros': [int(banheiros) for _ in range(1)],
    'Elevador': [random.randint(0, 1) for _ in range(1)],
    'Cozinha': [random.randint(0, 1) for _ in range(1)],
    'Microondas': [random.randint(0, 1) for _ in range(1)],
    'Fogão': [random.randint(0, 1) for _ in range(1)],
    'Mesadejantar': [random.randint(0, 1) for _ in range(1)],
    'Wi-Fi': [random.randint(0, 1) for _ in range(1)],
    'Ar-condicionado': [random.randint(0, 1) for _ in range(1)],
    'TV': [random.randint(0, 1) for _ in range(1)],
    'Secadordecabelo': [random.randint(0, 1) for _ in range(1)],
    'Xampu': [random.randint(0, 1) for _ in range(1)],
    'Condicionador': [random.randint(0, 1) for _ in range(1)],
    'Saboneteparaocorpo': [random.randint(0, 1) for _ in range(1)],
    'Águaquente': [random.randint(0, 1) for _ in range(1)],
    'MáquinadeLavar': [random.randint(0, 1) for _ in range(1)],
    'Secadora': [random.randint(0, 1) for _ in range(1)],
    'Café': [random.randint(0, 1) for _ in range(1)],
    'Fechadurainteligente': [random.randint(0, 1) for _ in range(1)],
    'Refrigerador': [random.randint(0, 1) for _ in range(1)],
    'Permitidoanimais': [random.randint(0, 1) for _ in range(1)],
    'Permitidofumar': [random.randint(0, 1) for _ in range(1)],
    'Banheira': [random.randint(0, 1) for _ in range(1)],
    'Produtosdelimpeza': [random.randint(0, 1) for _ in range(1)],
    'Básico': [random.randint(0, 1) for _ in range(1)],
    'Cabides': [random.randint(0, 1) for _ in range(1)],
    'Roupadecama': [random.randint(0, 1) for _ in range(1)],
    'Cinema': [random.randint(0, 1) for _ in range(1)],
    'Lareirainterna': [random.randint(0, 1) for _ in range(1)],
    'Espaçodetrabalhoexclusivo': [random.randint(0, 1) for _ in range(1)],
    'Itensbásicosdecozinha': [random.randint(0, 1) for _ in range(1)],
    'Louçasetalheres': [random.randint(0, 1) for _ in range(1)],
    'Frigobar': [random.randint(0, 1) for _ in range(1)],
    'Lavalouças': [random.randint(0, 1) for _ in range(1)],
    'Cafeteira': [random.randint(0, 1) for _ in range(1)],
    'Torradeira': [random.randint(0, 1) for _ in range(1)],
    'Entradaprivada': [random.randint(0, 1) for _ in range(1)],
    'Áreadejantarexterna': [random.randint(0, 1) for _ in range(1)],
    'Churrasqueira': [random.randint(0, 1) for _ in range(1)],
    'Estacionamentoincluído': [random.randint(0, 1) for _ in range(1)],
    'Jacuzziprivativa': [random.randint(0, 1) for _ in range(1)],
    'Vistaparaojardim': [random.randint(0, 1) for _ in range(1)],
})
print("Pre-informed data:")
for data in pre_informed_data.values:
    print(data)

# Align the columns of pre_informed_data with the training data
pre_informed_data_aligned = pre_informed_data.reindex(columns=X_train_encoded.columns, fill_value=0)

# Make predictions with the aligned data
predictions_pre_informed = model_encoded.predict(pre_informed_data_aligned)

print('Predicted values:', predictions_pre_informed)
