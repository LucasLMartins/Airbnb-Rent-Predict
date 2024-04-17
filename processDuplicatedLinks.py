import pandas as pd

# Read the Excel file
file_path = 'airbnb_links.xlsx'
df = pd.read_excel(file_path)

# Extrair o número após "rooms/" e antes do próximo "/"
df['Room_Number'] = df['Link'].str.extract(r'rooms/(\d+)?')

# Remover duplicatas com base no número do quarto
df = df.drop_duplicates(subset=['Room_Number'])

# Remover a coluna auxiliar 'Room_Number'
df = df.drop(columns=['Room_Number'])

# Salvar o DataFrame modificado de volta para o arquivo Excel
df.to_excel(file_path, index=False)

print("Duplicatas removidas e arquivo atualizado com sucesso.")