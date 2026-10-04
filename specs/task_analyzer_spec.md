# Especificação Técnica SDD - TaskAnalyzer

## Contrato de Entrada (Inputs)
A função `analyze_tasks` recebe uma lista de dicionários (`list[dict]`), onde cada tarefa possui:
- `id` (str / int): Identificador único da tarefa.
- `titulo` (str): Título descritivo.
- `prioridade` (str): Estritamente "baixa", "media", ou "alta".
- `data_criacao` (str ISO-8601): Data/hora de criação (ex: "2026-08-01T09:00:00").
- `data_limite` (str ISO-8601): Prazo limite para conclusão.
- `data_conclusao` (str ISO-8601 / None): Data de conclusão (opcional).
- `status` (str): Estritamente "concluida" ou "pendente".

## Saídas de Dados (Outputs - dict)
- `total_tarefas`: int
- `total_concluidas`: int
- `tempo_medio_conclusao_dias`: float (Média em dias)
- `taxa_atraso_percentual`: float (0.0 a 100.0)
- `metricas_por_prioridade`: dict (Contendo totais, tempo médio em dias e taxa de atraso para baixa, media e alta)

## Regras de Negócio e Exceções
- Se `data_conclusao` < `data_criacao` ou se a data não estiver em formato ISO 8601 válido, lançar `TaskValidationError`.
- Em caso de lista vazia ou zero concluídas, todos os valores numéricos de média/taxa devem retornar estritamente `0.0`.
