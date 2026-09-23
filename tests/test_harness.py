import pytest
from src.task_analyzer import analyze_tasks, TaskValidationError


def test_cenario_1_sucesso_calculos_completos():
    """Cenário 1: Validação dos cálculos de métricas com sucesso."""
    tasks = [
        {
            "id": 1,
            "prioridade": "ALTA",
            "status": "CONCLUIDA",
            "data_criacao": "2026-03-01T10:00:00",
            "data_conclusao": "2026-03-01T12:00:00",  # 2 horas de duração
            "data_vencimento": "2026-03-01T15:00:00"  # Entregue no prazo
        },
        {
            "id": 2,
            "prioridade": "MEDIA",
            "status": "CONCLUIDA",
            "data_criacao": "2026-03-01T10:00:00",
            "data_conclusao": "2026-03-01T14:00:00",  # 4 horas de duração
            "data_vencimento": "2026-03-01T11:00:00"  # Entregue com atraso
        },
        {
            "id": 3,
            "prioridade": "ALTA",
            "status": "PENDENTE",
            "data_criacao": "2026-03-01T10:00:00",
            "data_conclusao": None,
            "data_vencimento": "2026-03-02T10:00:00"
        }
    ]

    resultado = analyze_tasks(tasks)

    assert resultado["total_tarefas"] == 3
    assert resultado["total_concluidas"] == 2
    assert resultado["total_pendentes"] == 1
    assert resultado["tempo_medio_conclusao_horas"] == 3.0  # (2 + 4) / 2
    assert resultado["tempo_medio_por_prioridade"]["ALTA"] == 2.0
    assert resultado["tempo_medio_por_prioridade"]["MEDIA"] == 4.0
    assert resultado["taxa_atraso_percentual"] == 50.0  # 1 tarefa atrasada de 2 concluídas


def test_cenario_2_excecao_data_inconsistente():
    """Cenário 2: Validação de data_conclusao anterior à data_criacao."""
    tasks = [
        {
            "id": 1,
            "prioridade": "BAIXA",
            "status": "CONCLUIDA",
            "data_criacao": "2026-03-02T10:00:00",
            "data_conclusao": "2026-03-01T10:00:00",  # Data inconsistente
            "data_vencimento": "2026-03-03T10:00:00"
        }
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tasks)


def test_casos_de_borda_lista_vazia_e_apenas_pendentes():
    """Valida resiliência numérica evitando divisão por zero."""
    # Lista vazia
    res_vazia = analyze_tasks([])
    assert res_vazia["total_tarefas"] == 0
    assert res_vazia["tempo_medio_conclusao_horas"] == 0.0
    assert res_vazia["taxa_atraso_percentual"] == 0.0

    # Apenas tarefas pendentes
    tasks_pendentes = [
        {
            "id": 1,
            "prioridade": "ALTA",
            "status": "PENDENTE",
            "data_criacao": "2026-03-01T10:00:00",
            "data_conclusao": None,
            "data_vencimento": "2026-03-02T10:00:00"
        }
    ]
    res_pendentes = analyze_tasks(tasks_pendentes)
    assert res_pendentes["total_pendentes"] == 1
    assert res_pendentes["tempo_medio_conclusao_horas"] == 0.0
