# Especificação Técnica SDD - TaskAnalyzer

## Contrato de Entrada
A função `analyze_tasks` recebe uma lista de dicionários (`list[dict]`), onde cada tarefa possui:
- `id` (int/str)
- `prioridade` (str: "ALTA", "MEDIA", "BAIXA")
- `status` (str: "CONCLUIDA", "PENDENTE")
- `data_criacao` (str ISO-8601: "YYYY-MM-DDTHH:MM:SS")
- `data_conclusao` (str ISO-8601 ou None)
- `data_vencimento` (str ISO-8601)

## Regras de Validação
- Se `data_conclusao` < `data_criacao`, lançar `TaskValidationError`.

## Indicadores Requeridos no Retorno (dict)
- `total_tarefas`: int
- `total_concluidas`: int
- `total_pendentes`: int
- `tempo_medio_conclusao_horas`: float (Média global em horas)
- `tempo_medio_por_prioridade`: dict (Ex: `{"ALTA": float, ...}`)
- `taxa_atraso_percentual`: float (Porcentagem de concluídas após o vencimento)
