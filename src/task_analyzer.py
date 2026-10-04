from datetime import datetime
from typing import Any, Dict, List


class TaskValidationError(Exception):
    """Exceção customizada para erros de validação e regras de negócio."""
    pass


def _parse_iso(date_str: str | None) -> datetime | None:
    """Converte string ISO-8601 para datetime. Lança TaskValidationError em formato inválido."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError) as exc:
        raise TaskValidationError(f"Formato de data inválido (esperado ISO-8601): {date_str}") from exc


def analyze_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analisa um lote de tarefas e retorna indicadores de produtividade.

    Args:
        tasks (List[Dict[str, Any]]): Lista de dicionários contendo tarefas.

    Returns:
        Dict[str, Any]: Dicionário contendo métricas consolidadas globais e por prioridade.

    Raises:
        TaskValidationError: Se houver datas inconsistentes ou fora do padrão ISO-8601.
    """
    total_tarefas = len(tasks)
    total_concluidas = 0
    tarefas_atrasadas_global = 0
    tempos_conclusao_dias_global: List[float] = []

    metricas_prio: Dict[str, Dict[str, Any]] = {
        "baixa": {"total": 0, "concluidas": 0, "atrasadas": 0, "tempos_dias": []},
        "media": {"total": 0, "concluidas": 0, "atrasadas": 0, "tempos_dias": []},
        "alta": {"total": 0, "concluidas": 0, "atrasadas": 0, "tempos_dias": []},
    }

    for task in tasks:
        prio = str(task.get("prioridade", "baixa")).lower()
        if prio not in metricas_prio:
            prio = "baixa"

        metricas_prio[prio]["total"] += 1
        status = str(task.get("status", "")).lower()

        if status == "concluida":
            total_concluidas += 1
            metricas_prio[prio]["concluidas"] += 1

            dt_criacao = _parse_iso(task.get("data_criacao"))
            dt_conclusao = _parse_iso(task.get("data_conclusao"))
            dt_limite = _parse_iso(task.get("data_limite"))

            if dt_criacao and dt_conclusao:
                if dt_conclusao < dt_criacao:
                    raise TaskValidationError(
                        f"Data de conclusão ({dt_conclusao}) anterior à criação ({dt_criacao})."
                    )

                duracao_dias = (dt_conclusao - dt_criacao).total_seconds() / 86400.0
                tempos_conclusao_dias_global.append(duracao_dias)
                metricas_prio[prio]["tempos_dias"].append(duracao_dias)

            if dt_conclusao and dt_limite and dt_conclusao > dt_limite:
                tarefas_atrasadas_global += 1
                metricas_prio[prio]["atrasadas"] += 1

    tempo_medio_global = (
        sum(tempos_conclusao_dias_global) / len(tempos_conclusao_dias_global)
        if tempos_conclusao_dias_global else 0.0
    )

    taxa_atraso_global = (
        (tarefas_atrasadas_global / total_concluidas) * 100.0
        if total_concluidas > 0 else 0.0
    )

    detalhe_prioridades: Dict[str, Dict[str, float | int]] = {}
    for p_nome, p_dados in metricas_prio.items():
        conc_prio = p_dados["concluidas"]
        tempos_prio = p_dados["tempos_dias"]

        media_prio = sum(tempos_prio) / len(tempos_prio) if tempos_prio else 0.0
        taxa_prio = (p_dados["atrasadas"] / conc_prio) * 100.0 if conc_prio > 0 else 0.0

        detalhe_prioridades[p_nome] = {
            "total": p_dados["total"],
            "concluidas": conc_prio,
            "tempo_medio_conclusao_dias": round(media_prio, 2),
            "taxa_atraso_percentual": round(taxa_prio, 2),
        }

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "tempo_medio_conclusao_dias": round(tempo_medio_global, 2),
        "taxa_atraso_percentual": round(taxa_atraso_global, 2),
        "metricas_por_prioridade": detalhe_prioridades,
    }
