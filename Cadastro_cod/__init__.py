from Cadastro_cod.Cadastro.cadastro import *
from copy import copy


def main():
    ManipulaCadastro().carregaListaDeCadastrados()
    while True:
        print(ManipulaCadastro().pessoas)
        comando = recebeComando()
        print(comando)

        if comando.startswith('n'):
           adicionaCadastro()

        elif comando.startswith('p'):
            if len(ManipulaCadastro().pessoas) == 0:
                print('Não há nenhum cadastro')
            else:
                pass
        else:
            break
    ManipulaCadastro().salvarPessoas()


def pegaCadastro(pessoas):
    pass


def carregarListaDeCadastrados():
    return ManipulaCadastro().carregaListaDeCadastrados()


def adicionaCadastro():
    pessoa = Cadastro()
    pessoa.cadastrarPessoa()
    ManipulaCadastro.pessoas.append(copy(pessoa))


def recebeComando():
    while True:
        cmd = input('''Deseja adicionar um novo cadastro(n/novo) ou procurar as 
informações de um cadastro(p/procurar) ou sair(s/sair)?\n''').lower()

        if not cmd.isalpha():
            print('Digite apenas letras!!')
        elif cmd.startswith('n') or cmd.startswith('p') or cmd.startswith('s'):
            return cmd
        else:
            print('Não entendi seu comando!!')


if __name__ == '__main__':
    main()
