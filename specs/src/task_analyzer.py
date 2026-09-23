from datetime import datetime
from typing import Any, Dict, List


class TaskValidationError(Exception):
    """Exceção customizada para erros de validação de regras de negócio."""
    pass


def _parse_iso(date_str: str | None) -> datetime | None:
    if not date_str:
        return None
    return datetime.fromisoformat(date_str)


def analyze_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analisa uma lista de tarefas e retorna métricas consolidadas.
    Segue estritamente as CONTEXT_RULES e a especificação SDD.
    """
    total_tarefas = len(tasks)
    total_concluidas = 0
    total_pendentes = 0
    tarefas_atrasadas = 0

    tempos_conclusao_global: List[float] = []
    tempos_por_prioridade: Dict[str, List[float]] = {
        "ALTA": [],
        "MEDIA": [],
        "BAIXA": []
    }

    for task in tasks:
        status = task.get("status")
        prioridade = task.get("prioridade", "BAIXA")

        if status == "PENDENTE":
            total_pendentes += 1
            continue

        if status == "CONCLUIDA":
            total_concluidas += 1
            dt_criacao = _parse_iso(task.get("data_criacao"))
            dt_conclusao = _parse_iso(task.get("data_conclusao"))
            dt_vencimento = _parse_iso(task.get("data_vencimento"))

            if dt_criacao and dt_conclusao:
                # Regra de validação: Data de conclusão anterior à criação
                if dt_conclusao < dt_criacao:
                    raise TaskValidationError(
                        f"Data de conclusão ({dt_conclusao}) anterior à data de criação ({dt_criacao})."
                    )

                duracao_horas = (dt_conclusao - dt_criacao).total_seconds() / 3600.0
                tempos_conclusao_global.append(duracao_horas)

                if prioridade in tempos_por_prioridade:
                    tempos_por_prioridade[prioridade].append(duracao_horas)

            # Verificação de atraso
            if dt_conclusao and dt_vencimento and dt_conclusao > dt_vencimento:
                tarefas_atrasadas += 1

    # Prevenção contra divisão por zero para listas vazias ou sem tarefas concluídas
    tempo_medio_global = (
        sum(tempos_conclusao_global) / len(tempos_conclusao_global)
        if tempos_conclusao_global else 0.0
    )

    media_prioridades: Dict[str, float] = {}
    for prio, lista_tempos in tempos_por_prioridade.items():
        media_prioridades[prio] = (
            sum(lista_tempos) / len(lista_tempos) if lista_tempos else 0.0
        )

    taxa_atraso = (
        (tarefas_atrasadas / total_concluidas) * 100.0
        if total_concluidas > 0 else 0.0
    )

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "tempo_medio_conclusao_horas": round(tempo_medio_global, 2),
        "tempo_medio_por_prioridade": {
            k: round(v, 2) for k, v in media_prioridades.items()
        },
        "taxa_atraso_percentual": round(taxa_atraso, 2)
    }
