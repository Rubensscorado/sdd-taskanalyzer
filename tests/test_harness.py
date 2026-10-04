import pytest
from src.task_analyzer import analyze_tasks, TaskValidationError


def test_cenario_1_sucesso_calculos_validos():
    """Valida o cálculo exato de métricas globais e por prioridade em dias."""
    tasks = [
        {
            "id": 1,
            "titulo": "Tarefa A",
            "prioridade": "alta",
            "status": "concluida",
            "data_criacao": "2026-08-01T00:00:00",
            "data_conclusao": "2026-08-03T00:00:00",  # 2 dias
            "data_limite": "2026-08-05T00:00:00",     # No prazo
        },
        {
            "id": 2,
            "titulo": "Tarefa B",
            "prioridade": "media",
            "status": "concluida",
            "data_criacao": "2026-08-01T00:00:00",
            "data_conclusao": "2026-08-05T00:00:00",  # 4 dias
            "data_limite": "2026-08-03T00:00:00",     # Atrasado
        },
        {
            "id": 3,
            "titulo": "Tarefa C",
            "prioridade": "alta",
            "status": "pendente",
            "data_criacao": "2026-08-01T00:00:00",
            "data_conclusao": None,
            "data_limite": "2026-08-10T00:00:00",
        },
    ]

    resultado = analyze_tasks(tasks)

    assert resultado["total_tarefas"] == 3
    assert resultado["total_concluidas"] == 2
    assert resultado["tempo_medio_conclusao_dias"] == 3.0  # (2 + 4) / 2
    assert resultado["taxa_atraso_percentual"] == 50.0      # 1 de 2 concluídas
    assert resultado["metricas_por_prioridade"]["alta"]["tempo_medio_conclusao_dias"] == 2.0
    assert resultado["metricas_por_prioridade"]["media"]["tempo_medio_conclusao_dias"] == 4.0


def test_cenario_2_excecao_datas_invalidas():
    """Lança TaskValidationError em datas inconsistentes ou fora do formato ISO 8601."""
    # Data de conclusão anterior à criação
    task_inconsistente = [
        {
            "id": 1,
            "titulo": "Erro Data",
            "prioridade": "baixa",
            "status": "concluida",
            "data_criacao": "2026-08-05T00:00:00",
            "data_conclusao": "2026-08-01T00:00:00",
            "data_limite": "2026-08-10T00:00:00",
        }
    ]
    with pytest.raises(TaskValidationError):
        analyze_tasks(task_inconsistente)

    # Formato de data inválido
    task_formato_errado = [
        {
            "id": 2,
            "titulo": "Erro Formato",
            "prioridade": "baixa",
            "status": "concluida",
            "data_criacao": "01/08/2026",
            "data_conclusao": "2026-08-02T00:00:00",
            "data_limite": "2026-08-10T00:00:00",
        }
    ]
    with pytest.raises(TaskValidationError):
        analyze_tasks(task_formato_errado)


def test_casos_de_borda_divisao_por_zero():
    """Valida retorno de 0.0 para entradas vazias ou sem tarefas concluídas."""
    res_vazia = analyze_tasks([])
    assert res_vazia["total_tarefas"] == 0
    assert res_vazia["tempo_medio_conclusao_dias"] == 0.0
    assert res_vazia["taxa_atraso_percentual"] == 0.0
