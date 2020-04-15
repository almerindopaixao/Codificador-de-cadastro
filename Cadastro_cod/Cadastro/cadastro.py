class Cadastro(object):
    def __init__(self):
        self.__nome = ''
        self.__idade = ''
        self.__RG = ''
        self.__CPF = ''
        self.__email = ''

    def cadastrarPessoa(self):
        nome = input('Digite o nome do indivíduo\n').lower()
        self.__nome = nome

        while True:
            try:
                idade = int(input('Digite a idade do indivíduo\n'))
                break
            except ValueError:
                print('Valor Inválido!! por favor digite novamente!!')

        self.__idade = idade

        self.__pegaRG()
        self.__pegaCPF()
        self.__pegaEmail()

    def __pegaRG(self):
        while True:
            RG = input('Digite o RG do indivíduo\n')
            try:
                separado = RG.split('.')
                primeiro_dois = separado[0]
                segundo_tres = separado[1]
                terceiro_tres = separado[2].split('-')[0]
                ultimo = separado[2].split('-')[1]

                if not (primeiro_dois.isdigit() and segundo_tres.isdigit() and terceiro_tres.isdigit() and ultimo.isdigit()):
                    print('Digite apenas números!!')
                    continue

                elif len(primeiro_dois) != 2 or len(segundo_tres) != 3 or len(terceiro_tres) != 3 or len(ultimo) != 1:
                    print('Número de algarismos está errado, digite novamente!!')
                    continue

            except IndexError:
                print('Entrada Inválida!!')

            except Exception as E:
                print(E)

            else:
                self.__RG = int(primeiro_dois + segundo_tres + terceiro_tres + ultimo)
                break

    def __pegaCPF(self):
        while True:
            CPF = input('Digite o CPF do indíviduo\n')
            try:
                separado = CPF.split('.')
                primeiro_tres = separado[0]
                segundo_tres = separado[1]
                terceiro_tres = separado[2].split('/')[0]
                ultimo_dois = separado[2].split('/')[1]

                if not (primeiro_tres.isdigit() and segundo_tres.isdigit() and terceiro_tres.isdigit() and ultimo_dois.isdigit()):
                    print('Digite apenas números!!')
                    continue

                elif len(primeiro_tres) != 3 or len(segundo_tres) != 3 or len(terceiro_tres) != 3 or len(ultimo_dois) != 2:
                    print('Número de algarismos está errado, digite novamente!!')
                    continue

            except IndexError:
                print('Entrada Inválida')

            except Exception as E:
                print(E)

            else:
                self.__CPF = int(primeiro_tres + segundo_tres + terceiro_tres + ultimo_dois)
                break

    def __pegaEmail(self):
        while True:
            email = input('Digite o email do indivíduo\n')
            try:
                separado = email.split('.')

                if (separado[1] != 'com' or separado[1] != 'br') and '@' not in separado[0]:
                    print('Erro na digitação do email!!')
                    continue

            except IndexError:
                print('Entrada Inválida')

            except Exception as E:
                print(E)

            else:
                self.__email = email
                break

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @property
    def idade(self):
        return self.__idade

    @idade.setter
    def idade(self, valor):
        self.__idade = valor

    @property
    def rg(self):
        return self.__RG

    @rg.setter
    def rg(self, valor):
        self.__RG = valor

    @property
    def cpf(self):
        return self.__CPF

    @cpf.setter
    def cpf(self, valor):
        self.__CPF = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        self.__email = valor


import struct
from copy import copy


class ManipulaCadastro(object):
    pessoas = []

    @classmethod
    def salvarPessoas(cls):
        with open('pessoas.cod', 'wb') as arquivo:
            for nome in cls.pessoas:
                chars_nome = len(nome.nome)
                chars_email = len(nome.email)
                num_data = struct.pack('I', chars_nome)
                num_data2 = struct.pack('I', chars_email)
                arquivo.write(num_data)
                arquivo.write(b'\n')
                arquivo.write(num_data2)
                arquivo.write(b'\n')

                info_data = struct.pack(f'{chars_nome}s {chars_email}s I Q Q', nome.nome.encode(), nome.email.encode(), nome.idade, nome.rg, nome.cpf)

                arquivo.write(info_data)
                arquivo.write(b'\n')

    @classmethod
    def carregaListaDeCadastrados(cls):
        try:
            arquivo = open('pessoas.cod', 'rb')
        except IOError:
            cls.pessoas = []
        else:
            try:
                for nums_char in arquivo:
                    #Primeiro dado -> numero de chars do nome
                    num_char_nome = nums_char.split(b'\n')[0]

                    #Segundo dado -> numero de chars do email
                    num_char_email = arquivo.readline().split(b'\n')[0]

                    # Terceiro dado --> nome
                    # Quarto dado --> email
                    # Quinto dado --> idade
                    # Sexto dado --> RG
                    # Setimo dado --> CPF

                    decode_num_chars = struct.unpack('I', num_char_nome)
                    decode_num_chars2 = struct.unpack('I', num_char_email)
                    decode = f'{decode_num_chars[0]}s {decode_num_chars2[0]}s I Q Q'

                    data = arquivo.readline().split(b'\n')[0]
                    info = struct.unpack(decode, data)
                    pessoa = Cadastro()
                    pessoa.nome = info[0].decode()
                    pessoa.email = info[1].decode()
                    pessoa.idade = info[2]
                    pessoa.rg = info[3]
                    pessoa.cpf = info[4]
                    cls.pessoas.append(copy(pessoa))

            except Exception as E:
                print(E)
                cls.pessoas = []

    @classmethod
    def pegaCadastro(cls):
        while True:
            name = input('Digite o nome da pessoa\n').lower()

            for pessoa in cls.pessoas:
                if name == pessoa.nome:
                    cls.__formataCadastro(pessoa)
                    return

            print('Pessoa não encontrada em nossa base de dados')
            break

    @staticmethod
    def __formataCadastro(pessoa):
        print(f'Nome: {pessoa.nome}')
        print(f'Idade: {pessoa.idade}')
        print(f'Email: {pessoa.email}')
        ManipulaCadastro().imprimeRG(pessoa)
        ManipulaCadastro().imprimeCPF(pessoa)
        print('')

    @staticmethod
    def colocaZero(num, palavra):
        if len(palavra) < num:
            return (num - len(palavra))*'0' + palavra
        else:
            return palavra

    @staticmethod
    def imprimeRG(pessoa):
        RG = pessoa.rg

        ultimo = str(RG % 10)
        RG //= 10
        terceiro_tres = ManipulaCadastro().colocaZero(3, str(RG % 1000))
        RG //= 1000
        segundo_tres = ManipulaCadastro().colocaZero(3, str(RG % 1000))
        RG //= 1000
        primeiro_dois = ManipulaCadastro().colocaZero(2, str(RG % 100))

        print(f'RG: {primeiro_dois}.{segundo_tres}.{terceiro_tres}-{ultimo}')

    @staticmethod
    def imprimeCPF(pessoa):
        CPF = pessoa.cpf

        ultimos_dois = ManipulaCadastro().colocaZero(2, str(CPF % 100))
        CPF //= 100
        terceiro_tres = ManipulaCadastro().colocaZero(3, str(CPF % 1000))
        CPF //= 1000
        segundo_tres = ManipulaCadastro().colocaZero(3, str(CPF % 1000))
        CPF //= 1000
        primeiros_tres = ManipulaCadastro().colocaZero(3, str(CPF % 1000))

        print(f'CPF: {primeiros_tres}.{segundo_tres}.{terceiro_tres}/{ultimos_dois}')
