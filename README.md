# Design Ocean

Sistema oficial de identidade da **Ocean Health**, empresa brasileira de planos de saúde.

Este repositório e a fonte de verdade para qualquer material visual, editorial ou digital da marca. Ele reune o manual de marca, os ativos aprovados, os tokens de design e as instrucoes operacionais para agentes e designers.

## Comece aqui

1. Leia o [manual editável](manual/Manual-da-Marca-Ocean-Health.md).
2. Consulte as regras do [agente de design](agent/AGENT-DESIGN.md).
3. Use somente os arquivos de `assets/`.
4. Valide a entrega com o [checklist](agent/design-checklist.md).
5. Para interfaces e automação, consuma os [tokens JSON](agent/brand-tokens.json).

## Estrutura

```text
design-ocean/
|- manual/
|  |- Manual-da-Marca-Ocean-Health.pdf
|  `- Manual-da-Marca-Ocean-Health.md
|- agent/
|  |- AGENT-DESIGN.md
|  |- brand-tokens.json
|  |- design-checklist.md
|  `- prompt-library.md
|- assets/
|  |- logos/
|  |- fonts/
|  |- graphics/
|  |- photography/
|  `- app/
|- AGENTS.md
`- BRAND-ASSET-NOTICE.md
```

## Regras inegociaveis

- O logo branco deve ser usado com fundo transparente em superfícies escuras. Nunca aplicar uma caixa branca atras dele.
- O ciano e sinal de ação e movimento. Ele não deve ser espalhado como decoracao aleatoria.
- A corrente cursiva e um gesto desenhado a mão, horizontal e assimétrico. Nunca substituir por um círculo geométrico perfeito.
- A fotografia mostra pessoas antes de mostrar medicina. Priorizar momentos humanos, luz natural e expressões autênticas.
- Evitar o visual generico de healthtech: degradê roxo-rosa, excesso de cards, bolhas aleatorias, ícones 3D e estetica de banco de imagens.
- Toda peça deve ter uma mensagem dominante e um próximo passo claro.

## Paleta rapida

| Token | HEX | Uso |
|---|---:|---|
| Ocean 700 | `#4800EF` | Marca e ações principais |
| Ocean 900 | `#200077` | Profundidade e fundos escuros |
| Current | `#00DBF9` | Movimento, foco e destaque |
| Sky 050 | `#EFFBFF` | Fundo claro cromatico |
| Ink | `#15192D` | Texto principal |
| Muted | `#484F64` | Texto secundario |
| Line | `#D4DAEC` | Divisores |
| White | `#FFFFFF` | Respiro e contraste |

## Tipografia

- Display: **Gabarito**, pesos 600 a 800.
- Texto e interface: **Albert Sans**, pesos 400 a 700.
- Fallback: Arial, sans-serif.

As fontes estao em `assets/fonts/` e acompanham suas licenças OFL.

## Status

Versão 1.0 - Setembro de 2026.

Os ativos de marca permanecem propriedade de seus titulares. Leia [BRAND-ASSET-NOTICE.md](BRAND-ASSET-NOTICE.md) antes de reutiliza-los.
