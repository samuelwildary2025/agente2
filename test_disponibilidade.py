#!/usr/bin/env python3
"""
Teste específico da função de disponibilidade completa
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

BOOL_AVAIL_KEYS = ("disponibilidade", "disponivel", "available", "in_stock", "em_estoque", "ativo")
STATUS_KEYS = ("situacao", "situacaoEstoque", "status", "statusEstoque")

def _has_positive_qty(d):
    for k in STOCK_QTY_KEYS:
        if k in d:
            v = d.get(k)
            try:
                n = float(str(v).replace(",", "."))
                if n > 0:
                    return True
            except Exception:
                pass
    return False

def _is_available(d):
    # Verifica booleanos explícitos
    for k in BOOL_AVAIL_KEYS:
        if k in d:
            v = d.get(k)
            if isinstance(v, bool):
                print(f"Campo {k} = {v} (bool) -> {v}")
                return v
            # valores textuais como "true"/"false"
            if isinstance(v, str) and v.strip().lower() in {"true", "sim", "yes"}:
                print(f"Campo {k} = {v} (str positivo) -> True")
                return True
    # Verifica quantidade positiva
    if _has_positive_qty(d):
        print("Tem quantidade positiva -> True")
        return True
    return False

print("🔍 Testando lógica de disponibilidade completa...")
print(f"Dados: {dados_api}")
print()

disponivel = _is_available(dados_api)
print(f"\nResultado: Produto está disponível? {disponivel}")

# Testar também extração de preço
PRICE_KEYS = (
    "vl_produto",
    "vl_produto_normal",
    "preco",
    "preco_venda",
    "valor",
    "valor_unitario",
    "preco_unitario",
    "atacadoPreco",
)

def _parse_float(val):
    try:
        s = str(val).strip()
        if not s:
            return None
        # aceita formato brasileiro
        s = s.replace(".", "").replace(",", ".") if s.count(",") == 1 and s.count(".") > 1 else s.replace(",", ".")
        return float(s)
    except Exception:
        return None

def _extract_price(d):
    for k in PRICE_KEYS:
        if k in d:
            val = _parse_float(d.get(k))
            if val is not None:
                print(f"Preço encontrado no campo {k}: R$ {val}")
                return val
    return None

print("\n💰 Testando extração de preço...")
preco = _extract_price(dados_api)
print(f"Preço extraído: R$ {preco}")