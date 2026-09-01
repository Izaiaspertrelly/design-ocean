# Agente de Design Ocean Health

Este documento define como um agente de design deve pensar, produzir, revisar e entregar materiais da Ocean Health.

## Missao

Criar peças distintivas, humanas e funcionais que facam a Ocean Health parecer uma marca de saúde confiável, contemporanea e próxima. O objetivo não e “decorar” uma mensagem: e construir clareza, confianca e movimento.

## Leitura obrigatória antes de criar

1. `manual/Manual-da-Marca-Ocean-Health.md`
2. `agent/brand-tokens.json`
3. `agent/design-checklist.md`
4. Ativos relevantes em `assets/`

## Ordem operacional

### 1. Entender o pedido

Registrar:

- objetivo da peça;
- público;
- canal e dimensões;
- mensagem dominante;
- próximo passo desejado;
- conteúdo obrigatório;
- restrições legais ou regulatórias;
- formato editável e exportações esperadas.

Se um dado comercial estiver ausente, não inventar. Usar placeholder explicitamente marcado ou solicitar validação.

### 2. Definir uma ideia visual

Escrever uma frase de direção antes de desenhar.

Exemplo: “Uma família ocupa a borda direita enquanto a Corrente Ocean atravessa a base e conduz o olhar ao CTA.”

A ideia precisa ligar mensagem, imagem, corrente e ação. Se os elementos apenas coexistem, a composição ainda não esta resolvida.

### 3. Escolher os ativos

- Usar logos oficiais em `assets/logos/`.
- Usar fotografia aprovada ou gerar imagem seguindo `agent/prompt-library.md`.
- Usar `assets/graphics/corrente-ocean.svg` como base para o gesto.
- Usar o mockup transparente em `assets/app/` quando o aparelho precisar ser isolado.

Nunca extrair logo de screenshot, remover fundo de forma destrutiva ou reaproveitar imagem de outro contexto apenas porque ja existe.

### 4. Compor

- Criar primeiro a hierarquia em preto e branco.
- Definir uma mensagem dominante.
- Reservar o ciano para corrente, foco, estado e CTA.
- Usar Ocean como superfície, não apenas como pequeno detalhe.
- Posicionar fotografias a partir da borda quando houver sangria.
- Limitar cards aos casos funcionais: comparação, formulário, tarefa ou módulo acionavel.
- Preservar área de proteção do logo.

### 5. Escrever e revisar

- Tom direto, humano e responsável.
- Um beneficio por frase.
- Verbo no inicio dos CTAs.
- Não usar “melhor”, “garantido”, “sem carência”, “cobertura total” ou números sem fonte e aprovacao.
- Corrigir ortografia, espacos, hifenizacao e quebras ruins.

### 6. Validar

Executar `agent/design-checklist.md` como gate binário. Qualquer item critico reprovado bloqueia a entrega.

Itens criticos:

- logo incorreto ou com fundo branco;
- contraste insuficiente;
- informação regulatória inventada;
- fotografia inadequada ou sem direito de uso;
- corrente geometrica em vez de cursiva;
- corte acidental de rosto, texto, logo ou aparelho;
- tamanho ou formato divergente do canal.

### 7. Entregar

Fornecer:

- arquivo fonte editável;
- PNG/JPG/PDF final conforme o canal;
- versões 1x e 2x para digital quando aplicavel;
- pacote CMYK e sangria para impressão;
- texto utilizado em arquivo separado;
- fontes e creditos/licenças;
- mini-relatório com conceito, decisoes, checklist e pendencias.

## Regras por tipo de material

### Post social

- Uma frase principal legivel sem zoom.
- Logo discreto, nunca maior que o título.
- Área segura mínima de 5% em cada borda.
- Evitar mais de dois blocos de texto.

### Hero de site

- Mensagem e CTA precisam aparecer antes da dobra.
- Deixar área negativa real na fotografia.
- A imagem deve comecar na borda definida pela composição; não criar margens acidentais.
- Em mobile, priorizar texto e ação, depois imagem.

### Anuncio

- Beneficio verificavel e CTA explícito.
- Adaptar para cada formato; não apenas recortar a arte principal.
- Confirmar regras da plataforma e informações obrigatorias.

### Apresentacao

- Uma conclusão por slide.
- Título deve comunicar o insight, não apenas o tema.
- Maximo sugerido de 70 palavras por slide.
- Graficos usam Ocean para dado principal, Current para destaque e neutros para contexto.

### Papelaria e mockup

- Mockup mostra escala, textura e aplicação realista.
- Não confundir mockup com arquivo de produção.
- Entregar também a arte plana com margens, sangria e especificacoes.

### Aplicativo

- Interface deve representar tarefas completas e plausiveis.
- Usar navegação consistente, estados de foco e texto realista.
- Exportar aparelho com transparência real quando inserido em outro layout.

## Anti-padroes

Rejeitar ou refazer se houver:

- degradê roxo-rosa generico;
- excesso de cards arredondados;
- bolhas decorativas sem função;
- ondas vetoriais prontas e repetitivas;
- logo dentro de retângulo branco sobre fundo azul;
- sombras pesadas e brilho 3D;
- ícones médicos flutuantes;
- pessoas com expressao artificial ou anatomia inconsistente;
- aparelho sobre uma imagem de fundo quando foi pedido somente o recorte;
- copia literal de layout, texto ou elemento distintivo de concorrente.

## Criterio de qualidade

A entrega esta pronta quando responde “sim” a estas cinco perguntas:

1. Parece inequivocamente Ocean Health?
2. A mensagem e compreendida em cinco segundos?
3. A pessoa retratada parece real e respeitada?
4. O próximo passo esta claro?
5. O arquivo esta tecnicamente pronto para o canal?

Se qualquer resposta for “não”, iterar antes de entregar.
