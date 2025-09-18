"""
Banco v2 – Sistema modular com usuários e contas

Regras principais deste módulo:
- saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques) -> keyword-only
- deposito(saldo, valor, extrato, /) -> positional-only
- criar_usuario, criar_conta_corrente e utilitários para listar/selecionar

Observações:
- Os dados são mantidos em memória (listas). Não há persistência em disco.
- Para operar (depositar/sacar/extrato), selecione uma conta corrente ativa.
"""

from textwrap import dedent

AGENCIA_PADRAO = "0001"
LIMITE_SAQUES_PADRAO = 3
LIMITE_SAQUE_VALOR_PADRAO = 500.0

# ----------------------------- UTILITÁRIOS ----------------------------- #

def limpar_cpf(cpf: str) -> str:
    """Mantém apenas dígitos do CPF."""
    return "".join(ch for ch in cpf if ch.isdigit())

def encontrar_usuario_por_cpf(usuarios: list[dict], cpf: str):
    cpf = limpar_cpf(cpf)
    for u in usuarios:
        if u["cpf"] == cpf:
            return u
    return None

def pausar():
    input("\nPressione ENTER para continuar...")

# ----------------------------- OPERAÇÕES ------------------------------ #

def deposito(saldo: float, valor: float, extrato: list, /):
    """Depósito: argumentos apenas por posição. Retorna (saldo, extrato)."""
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato

    saldo += valor
    extrato.append(f"Depósito: R$ {valor:.2f}")
    print(f"Depósito realizado: R$ {valor:.2f}")
    return saldo, extrato

def saque(*, saldo: float, valor: float, extrato: list, limite: float,
          numero_saques: int, limite_saques: int):
    """Saque: argumentos APENAS por nome. Retorna (saldo, extrato, numero_saques)."""
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques

    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato.append(f"Saque: R$ {valor:.2f}")
    numero_saques += 1
    print(f"Saque realizado: R$ {valor:.2f}")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo: float, extrato: list):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for linha in extrato:
            print(linha)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("========================================")

# ----------------------------- CADASTROS ------------------------------ #

def criar_usuario(usuarios: list[dict]):
    """Cadastra um usuário (nome, data_nascimento, cpf, endereco)."""
    print("\n=== Novo usuário ===")
    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    cpf = limpar_cpf(input("CPF (somente números ou qualquer formato): ").strip())

    if not cpf:
        print("CPF inválido.")
        return

    if encontrar_usuario_por_cpf(usuarios, cpf):
        print("Já existe usuário com este CPF.")
        return

    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
    })
    print("Usuário criado com sucesso!")

def listar_usuarios(usuarios: list[dict]):
    print("\n=== Usuários cadastrados ===")
    if not usuarios:
        print("(vazio)")
        return
    for u in usuarios:
        print(f"- {u['nome']} | CPF: {u['cpf']} | Nasc.: {u['data_nascimento']} | End.: {u['endereco']}")

def criar_conta_corrente(contas: list[dict], usuarios: list[dict], agencia_padrao: str = AGENCIA_PADRAO):
    """Cria uma conta vinculada a um usuário existente (pelo CPF)."""
    print("\n=== Nova conta corrente ===")
    cpf = limpar_cpf(input("CPF do titular: ").strip())
    usuario = encontrar_usuario_por_cpf(usuarios, cpf)

    if not usuario:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")
        return

    numero_conta = len(contas) + 1  # sequencial iniciando em 1

    conta = {
        "agencia": agencia_padrao,
        "numero": numero_conta,
        "cpf": usuario["cpf"],  # vínculo por CPF
        # Estado financeiro da conta
        "saldo": 0.0,
        "extrato": [],
        "numero_saques": 0,
        "limite_saque_valor": LIMITE_SAQUE_VALOR_PADRAO,
        "limite_saques": LIMITE_SAQUES_PADRAO,
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência {conta['agencia']} | Nº {conta['numero']} | Titular: {usuario['nome']}")

def listar_contas(contas: list[dict], usuarios: list[dict]):
    print("\n=== Contas cadastradas ===")
    if not contas:
        print("(vazio)")
        return

    for c in contas:
        user = encontrar_usuario_por_cpf(usuarios, c["cpf"]) or {"nome": "<desconhecido>"}
        print(
            f"Agência: {c['agencia']} | Conta: {c['numero']} | Titular: {user['nome']} | "
            f"Saldo: R$ {c['saldo']:.2f} | Saques usados: {c['numero_saques']}/{c['limite_saques']}"
        )

def selecionar_conta(contas: list[dict]):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None
    try:
        numero = int(input("Informe o número da conta que deseja selecionar: ").strip())
    except ValueError:
        print("Número inválido.")
        return None

    for c in contas:
        if c["numero"] == numero:
            print(f"Conta {numero} selecionada.")
            return c
    print("Conta não encontrada.")
    return None

# ----------------------------- INTERFACE ------------------------------ #

def menu_principal():
    return dedent(
        """
        \n=========== MENU ===========
        [nu] Novo usuário
        [nc] Nova conta
        [lu] Listar usuários
        [lc] Listar contas
        [sc] Selecionar conta ativa
        --------------------------
        [d]  Depositar
        [s]  Sacar
        [e]  Extrato
        [q]  Sair
        ==========================
        => """
    )

def mostrar_cabecalho_conta(conta: dict, usuarios: list[dict]):
    if not conta:
        print("\nNenhuma conta ativa. Selecione uma conta (opção [sc]).")
        return
    user = encontrar_usuario_por_cpf(usuarios, conta["cpf"]) or {"nome": "<desconhecido>"}
    print(
        f"\nConta ativa: Agência {conta['agencia']} | Nº {conta['numero']} | Titular: {user['nome']}"
    )

# ----------------------------- APLICAÇÃO ------------------------------ #

def main():
    usuarios: list[dict] = []
    contas: list[dict] = []
    conta_ativa: dict | None = None

    while True:
        mostrar_cabecalho_conta(conta_ativa, usuarios)
        opcao = input(menu_principal()).strip().lower()

        if opcao == "nu":
            criar_usuario(usuarios)
            pausar()

        elif opcao == "nc":
            criar_conta_corrente(contas, usuarios)
            pausar()

        elif opcao == "lu":
            listar_usuarios(usuarios)
            pausar()

        elif opcao == "lc":
            listar_contas(contas, usuarios)
            pausar()

        elif opcao == "sc":
            conta_ativa = selecionar_conta(contas)
            pausar()

        elif opcao == "d":
            if not conta_ativa:
                print("Selecione uma conta ativa primeiro (opção [sc]).")
                pausar()
                continue
            valor = float(input("Informe o valor do depósito: ").strip())
            conta_ativa["saldo"], conta_ativa["extrato"] = deposito(
                conta_ativa["saldo"], valor, conta_ativa["extrato"]
            )
            pausar()

        elif opcao == "s":
            if not conta_ativa:
                print("Selecione uma conta ativa primeiro (opção [sc]).")
                pausar()
                continue
            valor = float(input("Informe o valor do saque: ").strip())
            conta_ativa["saldo"], conta_ativa["extrato"], conta_ativa["numero_saques"] = saque(
                saldo=conta_ativa["saldo"],
                valor=valor,
                extrato=conta_ativa["extrato"],
                limite=conta_ativa["limite_saque_valor"],
                numero_saques=conta_ativa["numero_saques"],
                limite_saques=conta_ativa["limite_saques"],
            )
            pausar()

        elif opcao == "e":
            if not conta_ativa:
                print("Selecione uma conta ativa primeiro (opção [sc]).")
            else:
                exibir_extrato(conta_ativa["saldo"], conta_ativa["extrato"])
            pausar()

        elif opcao == "q":
            print("Saindo... Até mais!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            pausar()

if __name__ == "__main__":
    main()
# Fim do arquivo sistema.py