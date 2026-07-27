# GUIA — GERAR NARRAÇÃO AUTOMÁTICA COM ELEVENLABS

O script `scripts/narrar.py` lê qualquer roteiro do repositório, separa só os
parágrafos de narração (ignora prompts de imagem, tabelas, títulos e notas de
produção) e gera um MP3 por PARTE, prontos para arrastar no CapCut.

Só precisa de Python 3. Não instala nada.

---

## 1. Antes de tudo: troque a sua chave

Uma chave de API é uma senha. Se ela vazou em qualquer conversa, mensagem ou
print, entre em https://elevenlabs.io/app/settings/api-keys, apague a chave
antiga e crie uma nova. Quem tiver a chave gasta os seus créditos.

## 2. Configurar (uma vez só)

Na pasta do repositório, crie um arquivo chamado `.env`:

```bash
cp .env.example .env
```

Abra o `.env` e substitua pela sua chave nova:

```
ELEVENLABS_API_KEY=sk_sua_chave_nova_aqui
```

O `.env` está no `.gitignore` — ele nunca sobe para o GitHub.

Teste a conexão:

```bash
python3 scripts/narrar.py --saldo
```

Deve aparecer o seu plano e quantos caracteres ainda restam no mês.

## 3. Escolher a voz

```bash
python3 scripts/narrar.py --vozes
```

Lista o nome e o ID de cada voz da sua conta. Para o canal, procure uma voz
masculina grave em português. Anote o nome — você vai usar em `--voz`.

## 4. Ver quanto vai custar, sem gastar nada

```bash
python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --simular
```

Mostra as partes encontradas, o total de caracteres e a duração estimada.
Nenhum crédito é consumido. **Sempre rode isso antes de gerar**, principalmente
no plano free (~10 mil caracteres por mês, que dá cerca de um vídeo).

## 5. Gerar o áudio

```bash
python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --voz "Nome da Voz"
```

Os arquivos saem em `audio/roteiro-video-11-poco-de-kola/parte-01.mp3`,
`parte-02.mp3`, e assim por diante.

Para gerar por etapas (útil quando o plano é limitado):

```bash
python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --partes 1-4
python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --partes 5,6,7
```

Partes que já têm MP3 são puladas automaticamente. Se uma parte ficou ruim,
apague o MP3 dela e rode de novo, ou use `--forcar`.

---

## Opções

| Opção | O que faz |
|---|---|
| `--vozes` | lista as vozes da conta |
| `--saldo` | mostra os caracteres restantes no plano |
| `--simular` | mostra o que seria gerado, sem gastar créditos |
| `--voz "Nome"` | escolhe a voz (nome ou ID) |
| `--partes 1-5` | gera só algumas partes (`3`, `1-5` ou `2,4,7`) |
| `--forcar` | regera partes que já têm MP3 |
| `--saida pasta` | muda a pasta de destino (padrão: `audio`) |
| `--estabilidade 0.45` | Stability — mais alto = leitura mais uniforme |
| `--similaridade 0.75` | Similarity |
| `--estilo 0.20` | Style — mais alto = mais dramático, menos previsível |
| `--modelo` | padrão `eleven_multilingual_v2` (melhor para português) |

Os valores padrão de estabilidade, similaridade e estilo são os mesmos
recomendados em `narracao-elevenlabs.md` (45% / 75% / 20%), que é o ajuste de
documentário do canal.

## Quais arquivos funcionam

Qualquer roteiro do repositório:

- `roteiro-video-*.md` — o script pula tudo que vem antes de `# NARRAÇÃO
  COMPLETA` e ignora os blocos `**Prompts CapCut:**`, tabelas e listas.
- `narracao-elevenlabs.md` — separa pelas PARTES 1 a 10.
- `narracao-video-2-continua.txt` — texto puro, gera em bloco único.

Textos longos são cortados automaticamente em blocos menores, sempre no fim de
uma frase. O script passa o `previous_request_ids` entre os blocos da mesma
parte, então o tom da voz não muda no meio.

## Problemas comuns

**`Chave da API não encontrada`** — o `.env` não existe ou está em outra pasta.
Rode o comando de dentro da pasta do repositório.

**`Chave da API inválida ou revogada (401)`** — chave errada, com espaço sobrando
ou já apagada no site.

**`Sem créditos de caracteres no plano (402)`** — acabou a cota do mês. Rode
`--saldo` para confirmar e gere o resto com `--partes` no mês seguinte, ou
complete no texto-para-voz do CapCut como está descrito em
`narracao-elevenlabs.md`.

**Erro 429** — muitas chamadas seguidas. O script já espera e tenta de novo
sozinho (2s, 4s, 8s).
