# Diretrizes de Governança de IA (CONTEXT_RULES)

1. **Runtime**: Uso obrigatório do Python 3.12+.
2. **Tipagem Estática**: Type hints em 100% das funções, parâmetros e retornos.
3. **Padrão e Estilo**: Google Style Docstrings e conformidade total com a PEP 8.
4. **Tratamento de Exceções**: Lançar a exceção customizada `TaskValidationError` para datas inconsistentes ou formatos ISO-8601 inválidos.
5. **Resiliência Numérica**: Prevenção contra divisão por zero, garantindo o retorno estrito de `0.0` em médias e percentuais quando vazios.
6. **Dependências**: Apenas biblioteca padrão do Python e `pytest` para testes.
