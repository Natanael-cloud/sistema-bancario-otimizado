# Sistema Bancário Otimizado

Este projeto é um sistema bancário simples, modular e totalmente em memória, desenvolvido em Python. Ele permite o cadastro de usuários, criação de contas correntes, depósitos, saques e consulta de extrato.

## Funcionalidades

- Cadastro de usuários com nome, data de nascimento, CPF e endereço
- Criação de contas correntes vinculadas a usuários existentes
- Depósitos e saques com regras de limite de valor e quantidade de saques diários
- Consulta de extrato da conta ativa
- Listagem de usuários e contas cadastradas
- Interface de menu interativo via terminal

## Como executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/sistema_bancario_otimizado.git
   ```
3. Acesse a pasta do projeto:
   ```sh
   cd sistema_bancario_otimizado
   ```
4. Execute o sistema:
   ```sh
   python sistema.py
   ```

## Estrutura do Projeto

- `sistema.py`: Arquivo principal com toda a lógica do sistema bancário.

## Observações

- Os dados são mantidos apenas em memória (listas). Não há persistência em disco.
- Para operar (depositar, sacar, consultar extrato), selecione uma conta corrente ativa.

<br> <br>

## Exemplos de Entradas e Saídas

### 1. Cadastro de Usuário

**Entrada:**
```
[nu]
Nome completo: João Silva
Data de nascimento (DD/MM/AAAA): 01/01/1990
CPF (somente números ou qualquer formato): 123.456.789-00
Endereço (logradouro, nro - bairro - cidade/UF): Rua A, 10 - Centro - Cidade/UF
```

**Saída:**
```
Usuário criado com sucesso!
```

---

### 2. Criação de Conta Corrente

**Entrada:**
```
[nc]
CPF do titular: 12345678900
```

**Saída:**
```
Conta criada com sucesso! Agência 0001 | Nº 1 | Titular: João Silva
```

---

### 3. Depósito

**Entrada:**
```
[sc]
Informe o número da conta que deseja selecionar: 1

[d]
Informe o valor do depósito: 200
```

**Saída:**
```
Conta 1 selecionada.
Depósito realizado: R$ 200.00
```

---

### 4. Saque

**Entrada:**
```
[s]
Informe o valor do saque: 50
```

**Saída:**
```
Saque realizado: R$ 50.00
```

---

### 5. Extrato

**Entrada:**
```
[e]
```

**Saída:**
```
================ EXTRATO ================
Depósito: R$ 200.00
Saque: R$ 50.00

Saldo: R$ 150.00
