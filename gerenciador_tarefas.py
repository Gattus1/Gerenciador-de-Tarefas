#!/usr/bin/env python3
"""
Gerenciador de Tarefas - Versão final pronta para GitHub

Funcionalidades implementadas:
- Título, Descrição, Prioridade, Status, Origem, Data de Criação, Data de Conclusão, ID
- Menu, validações, try/except, debug prints no início das funções
- Persistência: tarefas.json e tarefas_arquivadas.json (criadas automaticamente)
- Arquivamento automático (>7 dias), exclusão lógica, relatórios
- Docstrings e comentários explicativos
"""

import json
import os
import datetime
from typing import List, Dict, Optional

PRIORIDADES = ["Urgente", "Alta", "Média", "Baixa"]
ORIGENS = ["E-mail", "Telefone", "Chamado do Sistema"]
STATUS_POSSIVEIS = ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"]

TAREFAS_FILE = "tarefas.json"
TAREFAS_ARQUIVADAS_FILE = "tarefas_arquivadas.json"

tarefas: List[Dict] = []
tarefas_arquivadas: List[Dict] = []
id_contador: int = 1


def debug(msg: str):
    """Print padronizado para rastrear execução (debug)."""
    print(f"[DEBUG] {msg}")


def criar_arquivos_se_nao_existirem():
    """Cria arquivos JSON necessários com [] se não existirem."""
    debug("Executando a função criar_arquivos_se_nao_existirem()")
    for filename in (TAREFAS_FILE, TAREFAS_ARQUIVADAS_FILE):
        if not os.path.exists(filename):
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                print(f"Arquivo criado automaticamente: {filename}")
            except Exception as e:
                print(f"Erro ao criar {filename}: {e}")


def carregar_dados():
    """Carrega tarefas e arquivadas; ajusta id_contador para evitar duplicação."""
    global tarefas, tarefas_arquivadas, id_contador
    debug("Executando a função carregar_dados()")
    criar_arquivos_se_nao_existirem()

    try:
        with open(TAREFAS_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            tarefas = [d for d in dados if isinstance(d, dict)]
    except Exception as e:
        print(f"Erro lendo {TAREFAS_FILE}: {e}")
        tarefas = []

    try:
        with open(TAREFAS_ARQUIVADAS_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            tarefas_arquivadas = [d for d in dados if isinstance(d, dict)]
    except Exception as e:
        print(f"Erro lendo {TAREFAS_ARQUIVADAS_FILE}: {e}")
        tarefas_arquivadas = []

    max_id = 0
    for lista in (tarefas, tarefas_arquivadas):
        for t in lista:
            try:
                tid = int(t.get("ID", 0))
                if tid > max_id:
                    max_id = tid
            except Exception:
                continue
    id_contador = max_id + 1


def salvar_dados():
    """Salva listas em JSON (tarefas e tarefas_arquivadas)."""
    debug("Executando a função salvar_dados()")
    try:
        with open(TAREFAS_FILE, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {TAREFAS_FILE}: {e}")

    try:
        with open(TAREFAS_ARQUIVADAS_FILE, "w", encoding="utf-8") as f:
            json.dump(tarefas_arquivadas, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {TAREFAS_ARQUIVADAS_FILE}: {e}")


def validar_opcao(mensagem: str, opcoes: List[str]) -> str:
    """Solicita entrada e valida entre as opções (case-insensitive)."""
    debug("Executando a função validar_opcao()")
    mapa = {o.lower(): o for o in opcoes}
    while True:
        entrada = input(f"{mensagem} (Opções: {', '.join(opcoes)}): ").strip()
        chave = entrada.lower()
        if chave in mapa:
            return mapa[chave]
        print(f"Entrada inválida. Opções válidas: {', '.join(opcoes)}")


def encontrar_tarefa_por_id(tarefa_id: int) -> Optional[Dict]:
    """Retorna tarefa ativa pelo ID ou None se não existir."""
    debug("Executando a função encontrar_tarefa_por_id()")
    for t in tarefas:
        try:
            if int(t.get("ID")) == tarefa_id:
                return t
        except Exception:
            continue
    return None


def mostrar_tarefa(t: Dict):
    """Imprime campos de uma tarefa de forma legível (com formatação de datas)."""
    debug("Executando a função mostrar_tarefa()")
    print(f"ID: {t.get('ID')}")
    print(f"Título: {t.get('Título')}")
    print(f"Descrição: {t.get('Descrição')}")
    print(f"Prioridade: {t.get('Prioridade')}")
    print(f"Origem: {t.get('Origem')}")
    print(f"Status: {t.get('Status')}")
    dc = t.get("Data de Criação")
    if dc:
        try:
            dtc = datetime.datetime.fromisoformat(dc)
            print(f"Data de Criação: {dtc.strftime('%d/%m/%Y %H:%M')}")
        except Exception:
            print(f"Data de Criação: {dc}")
    dcon = t.get("Data de Conclusão")
    if dcon:
        try:
            dtc = datetime.datetime.fromisoformat(dcon)
            print(f"Data de Conclusão: {dtc.strftime('%d/%m/%Y %H:%M')}")
        except Exception:
            print(f"Data de Conclusão: {dcon}")


def calcular_tempo_execucao(t: Dict) -> Optional[datetime.timedelta]:
    """Se tarefa concluída, retorna timedelta entre conclusão e criação."""
    debug("Executando a função calcular_tempo_execucao()")
    if t.get("Status") != "Concluída":
        return None
    try:
        dt_inicio = datetime.datetime.fromisoformat(t.get("Data de Criação"))
        dt_fim = datetime.datetime.fromisoformat(t.get("Data de Conclusão"))
        return dt_fim - dt_inicio
    except Exception:
        return None


def existe_tarefa_em_fazendo() -> Optional[Dict]:
    """Retorna a tarefa com status 'Fazendo' se existir, caso contrário None."""
    debug("Executando a função existe_tarefa_em_fazendo()")
    for t in tarefas:
        if t.get("Status") == "Fazendo":
            return t
    return None


def atualizar_id_contador_automatico():
    """Recalcula id_contador com base nos IDs presentes nos arquivos."""
    global id_contador
    debug("Executando a função atualizar_id_contador_automatico()")
    max_id = 0
    for lista in (tarefas, tarefas_arquivadas):
        for t in lista:
            try:
                tid = int(t.get("ID", 0))
                if tid > max_id:
                    max_id = tid
            except Exception:
                continue
    id_contador = max_id + 1


def criar_tarefa():
    """Cria tarefa pedindo título (obrigatório), descrição, prioridade e origem."""
    global tarefas, id_contador
    debug("Executando a função criar_tarefa()")

    titulo = input("Título da tarefa (obrigatório): ").strip()
    if not titulo:
        print("Título é obrigatório. Operação cancelada.")
        return

    descricao = input("Descrição (opcional): ").strip()
    prioridade = validar_opcao("Escolha a prioridade", PRIORIDADES)
    origem = validar_opcao("Escolha a origem", ORIGENS)

    tarefa = {
        "ID": id_contador,
        "Título": titulo,
        "Descrição": descricao,
        "Prioridade": prioridade,
        "Origem": origem,
        "Status": "Pendente",
        "Data de Criação": datetime.datetime.now().isoformat(),
        "Data de Conclusão": None
    }

    tarefas.append(tarefa)
    print(f"Tarefa criada com sucesso! ID = {id_contador}")
    id_contador += 1


def verificar_tarefa():
    """Seleciona a maior prioridade pendente (FIFO) e marca 'Fazendo'."""
    debug("Executando a função verificar_tarefa()")

    em_exec = existe_tarefa_em_fazendo()
    if em_exec:
        print(f"Já existe uma tarefa em execução: {em_exec.get('Título')} (ID: {em_exec.get('ID')})")
        return

    pendentes = [t for t in tarefas if t.get("Status") == "Pendente"]
    if not pendentes:
        print("Nenhuma tarefa pendente encontrada.")
        return

    prioridade_index = {p: i for i, p in enumerate(PRIORIDADES)}

    def chave_ordenacao(t):
        p = t.get("Prioridade", "Média")
        idx = prioridade_index.get(p, len(PRIORIDADES))
        try:
            dt = datetime.datetime.fromisoformat(t.get("Data de Criação"))
        except Exception:
            dt = datetime.datetime.min
        return (idx, dt)

    pendentes.sort(key=chave_ordenacao)
    escolhida = pendentes[0]
    escolhida["Status"] = "Fazendo"
    print(f"Iniciando tarefa: {escolhida.get('Título')} (ID: {escolhida.get('ID')}, Prioridade: {escolhida.get('Prioridade')})")


def atualizar_prioridade():
    """Atualiza prioridade de uma tarefa por ID (valida nova prioridade)."""
    debug("Executando a função atualizar_prioridade()")
    try:
        tid = int(input("Digite o ID da tarefa: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    tarefa = encontrar_tarefa_por_id(tid)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    print(f"Tarefa: {tarefa.get('Título')} | Prioridade atual: {tarefa.get('Prioridade')}")
    nova = validar_opcao("Nova prioridade", PRIORIDADES)
    tarefa["Prioridade"] = nova
    print("Prioridade atualizada com sucesso.")


def concluir_tarefa():
    """Conclui tarefa em 'Fazendo', registra data de conclusão e muda status."""
    debug("Executando a função concluir_tarefa()")
    try:
        tid = int(input("Digite o ID da tarefa a ser concluída: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    tarefa = encontrar_tarefa_por_id(tid)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    if tarefa.get("Status") != "Fazendo":
        print("Somente tarefas com status 'Fazendo' podem ser concluídas.")
        return

    tarefa["Status"] = "Concluída"
    tarefa["Data de Conclusão"] = datetime.datetime.now().isoformat()
    print(f"Tarefa '{tarefa.get('Título')}' concluída com sucesso.")


def excluir_tarefa():
    """Marca tarefa como 'Excluída' (exclusão lógica)."""
    debug("Executando a função excluir_tarefa()")
    try:
        tid = int(input("Digite o ID da tarefa a ser excluída: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    tarefa = encontrar_tarefa_por_id(tid)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    confirmado = input(f"Tem certeza que deseja marcar '{tarefa.get('Título')}' como Excluída? (S/N): ").strip().upper()
    if confirmado != "S":
        print("Exclusão cancelada.")
        return

    tarefa["Status"] = "Excluída"
    print("Tarefa marcada como 'Excluída' (exclusão lógica).")


def relatorio():
    """Imprime relatório geral com tempo de execução para concluídas."""
    debug("Executando a função relatorio()")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for t in tarefas:
        print("-" * 60)
        mostrar_tarefa(t)
        tempo = calcular_tempo_execucao(t)
        if tempo is not None:
            dias = tempo.days
            horas, resto = divmod(tempo.seconds, 3600)
            minutos = resto // 60
            print(f"Tempo de execução: {dias} dias, {horas} horas, {minutos} minutos")
    print("-" * 60)


def relatorio_arquivados():
    """Imprime tarefas arquivadas (histórico), sem exibir itens 'Excluída'."""
    debug("Executando a função relatorio_arquivados()")
    try:
        with open(TAREFAS_ARQUIVADAS_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro lendo {TAREFAS_ARQUIVADAS_FILE}: {e}")
        dados = []

    filtrado = [d for d in dados if d.get("Status") != "Excluída"]
    if not filtrado:
        print("Nenhuma tarefa arquivada para exibir.")
        return

    for t in filtrado:
        print("-" * 60)
        mostrar_tarefa(t)
        tempo = calcular_tempo_execucao(t)
        if tempo:
            dias = tempo.days
            horas, resto = divmod(tempo.seconds, 3600)
            minutos = resto // 60
            print(f"Tempo de execução: {dias} dias, {horas} horas, {minutos} minutos")
    print("-" * 60)


def arquivar_tarefas_antigas():
    """Move tarefas concluídas há >7 dias do ativo para o histórico (tarefas_arquivadas)."""
    global tarefas, tarefas_arquivadas
    debug("Executando a função arquivar_tarefas_antigas()")
    agora = datetime.datetime.now()
    limite = agora - datetime.timedelta(days=7)

    para_arquivar = []
    restantes = []

    for t in tarefas:
        if t.get("Status") == "Concluída":
            data_conc = t.get("Data de Conclusão")
            try:
                dt_conc = datetime.datetime.fromisoformat(data_conc) if data_conc else None
            except Exception:
                dt_conc = None
            if dt_conc and dt_conc < limite:
                t_copy = t.copy()
                t_copy["Status"] = "Arquivado"
                para_arquivar.append(t_copy)
                continue
        restantes.append(t)

    if not para_arquivar:
        return

    ids_arquivados = {a.get("ID") for a in tarefas_arquivadas}
    adicionadas = 0
    for item in para_arquivar:
        if item.get("ID") not in ids_arquivados:
            tarefas_arquivadas.append(item)
            adicionadas += 1

    tarefas = restantes

    if adicionadas > 0:
        print(f"{adicionadas} tarefa(s) arquivada(s) automaticamente.")


def menu():
    """Imprime o menu principal (lista as opções)."""
    debug("Executando a função menu()")
    print("\n--- MENU ---")
    print("1. Criar Tarefa")
    print("2. Verificar Tarefa (Iniciar próxima)")
    print("3. Atualizar Prioridade")
    print("4. Concluir Tarefa")
    print("5. Relatório Geral")
    print("6. Relatório Arquivadas")
    print("7. Excluir Tarefa (Exclusão Lógica)")
    print("8. Salvar e Sair")


def opcao_valida(opcao: str) -> bool:
    """Valida opções 1..8 do menu."""
    debug("Executando a função opcao_valida()")
    return opcao in [str(i) for i in range(1, 9)]


def main():
    """Fluxo principal: carrega dados, atualiza id, loop do menu e salva ao sair."""
    global tarefas, tarefas_arquivadas, id_contador
    debug("Executando a função main()")
    carregar_dados()
    atualizar_id_contador_automatico()

    while True:
        arquivar_tarefas_antigas()
        menu()
        opcao = input("Escolha uma opção: ").strip()
        if not opcao_valida(opcao):
            print("Opção inválida. Tente novamente.")
            continue

        if opcao == "1":
            criar_tarefa()
        elif opcao == "2":
            verificar_tarefa()
        elif opcao == "3":
            atualizar_prioridade()
        elif opcao == "4":
            concluir_tarefa()
        elif opcao == "5":
            relatorio()
        elif opcao == "6":
            relatorio_arquivados()
        elif opcao == "7":
            excluir_tarefa()
        elif opcao == "8":
            arquivar_tarefas_antigas()
            salvar_dados()
            print("Dados salvos. Saindo do programa...")
            exit()


if __name__ == "__main__":
    main()
