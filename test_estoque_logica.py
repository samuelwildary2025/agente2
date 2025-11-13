#!/usr/bin/env python3
"""
Teste específico da função de estoque
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Simular os dados que vêm da API
dados_api = {
    "id_loja": 1,
    "id_produto": 2108,
    "codigo_ean": 7896220900359,
    "produto": "ARROZ BRANCO ALTEZA 1kg",
    "vl_produto": 5.69,
    "vl_produto_normal": 5.69,
    "qtd_produto": 21.0,
    "qtd_movimentacao": 1.0,
    "ativo": True
}

# Copiar a lógica do código
STOCK_QTY_KEYS = {
    "estoque", "qtd", "qtde", "qtd_estoque", "quantidade", "quantidade_disponivel",
    "quantidadeDisponivel", "qtdDisponivel", "qtdEstoque", "estoqueAtual", "saldo",
    "qty", "quantity", "stock", "amount", "qtd_produto", "qtd_movimentacao"
}

def _has_positive_qty(d):
    for k in STOCK_QTY_KEYS:
        if k in d:
            v = d.get(k)
            print(f"Campo encontrado: {k} = {v} (tipo: {type(v)})")
            try:
                n = float(str(v).replace(",", "."))
                print(f"  Convertido para float: {n}")
                if n > 0:
                    print(f"  ✅ Valor positivo! Retornando True")
                    return True
                else:
                    print(f"  ❌ Valor não é positivo")
            except Exception as e:
                print(f"  ❌ Erro na conversão: {e}")
    print("Nenhum campo válido encontrado")
    return False

print("🔍 Testando lógica de estoque...")
print(f"Dados: {dados_api}")
print()

tem_estoque = _has_positive_qty(dados_api)
print(f"\nResultado: Tem estoque positivo? {tem_estoque}")