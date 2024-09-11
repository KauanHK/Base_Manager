'''Exemplo de uso do gerenciador de banco de dados'''
from base import Base


# Para criar uma tabela no banco de dados, basta criar uma classe que herda 'Base'
# A tabela é criada somente quando o primeiro elemento é criado (quando é criada uma instância da classe)
class Usuario(Base):

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


# Criar um objeto
# Há duas formas de criar um objeto

# Criar diretamente
Usuario.objects.create(
    nome = 'Carlos',
    idade = 20
)

# Criar uma instância, e depois salvar
rect = Usuario(10, 7)
rect.save()


# Selecionar todos os objetos de uma banco de dados
# Vamos criar alguns usuários aleatórios...
import random
nomes = ['Bob', 'Luiz', 'Claudio', 'Leonardo', 'Cleiton', 'Roberto']
for nome in nomes:
    Usuario.objects.create(
        nome = nome,
        idade = random.randint(15,40)
    )

# Vamos pegar todos os usuários e imprimí-los
usuarios = Usuario.objects.all()

print('Lista com todos os usuários:')
print(*usuarios, sep='\n')
print()

# Para pegar um objeto específico
# Por ID
usuario = Usuario.objects.get(id = 3)
print(f'Usuário de ID = 3: {usuario}')

# Se for passado um ID que não é de nenhum usuário, uma exceção será gerada
try:
    Usuario.objects.get(id = 100)
except ValueError as e:
    print(f'Erro: {e}')

# Por valor de alguma coluna
# Vamos pegar o usuário do Claudio
usuario = Usuario.objects.get(nome = 'Claudio')
print(usuario)