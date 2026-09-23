# Regras de Governança e Contexto (IA)

1. **Runtime**: Implementação em Python 3.11+.
2. **Tipagem**: Type Hints em 100% das funções e retornos.
3. **Exceções**: Lançar `TaskValidationError` para erros de regras de negócio.
4. **Resiliência**: Prevenção contra divisão por zero, retornando `0.0` em médias/taxas vazias.
