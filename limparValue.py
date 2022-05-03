value = 'R$ 1.000,12%'

def cleanValue(value):
    value = value.text.replace('R$', '').replace('%', '').replace('.', '').replace(',', '.').strip()
    return value
preco = float(cleanValue(value))
print(preco)