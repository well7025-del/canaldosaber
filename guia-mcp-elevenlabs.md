# GUIA — CONECTAR O CLAUDE DESKTOP AO ELEVENLABS (MCP)

Este guia é para o **Claude Desktop instalado no seu computador**. Depois de
configurado, você pede a narração direto no chat ("gera o áudio da parte 3 do
roteiro do Poço de Kola") e o Claude chama o ElevenLabs sozinho.

É um caminho diferente do `scripts/narrar.py`, e os dois podem conviver:

| | MCP no Claude Desktop | `scripts/narrar.py` |
|---|---|---|
| Como usa | conversando no chat | comando no terminal |
| Bom para | testar vozes, gerar trechos soltos | gerar o vídeo inteiro em partes numeradas |
| Controle de cota | você acompanha na conversa | `--simular` calcula antes de gastar |
| Saída | onde você pedir | `audio/<roteiro>/parte-01.mp3`, em ordem |

Para produzir um vídeo completo, o script continua sendo o caminho mais
seguro — ele numera as partes na ordem do CapCut e não gasta crédito à toa.

---

## 1. Pré-requisitos

**Claude Desktop** instalado.

**Chave da API** do ElevenLabs: painel > ícone do perfil (canto inferior
esquerdo) > API Keys. Se a chave antiga já apareceu em alguma conversa ou
print, apague e crie outra antes de continuar.

**Gerenciador `uv`** (o servidor MCP do ElevenLabs roda com ele):

```bash
# Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Feche e reabra o terminal depois de instalar, senão o `uvx` não é encontrado.
Confirme com `uvx --version`.

## 2. Abrir o arquivo de configuração

1. Abra o Claude Desktop.
2. Menu **Claude** (Mac) ou ícone de engrenagem (Windows) > **Settings**.
3. **Developer** > **Edit Config**. O `claude_desktop_config.json` abre no seu
   editor de texto.

No Windows, se a aba Developer não aparecer: menu **Help** > ative
**Enable Developer Mode**.

## 3. Adicionar o servidor

Cole o bloco `ElevenLabs` dentro de `"mcpServers"`. Se o arquivo já tiver
outros servidores, **acrescente** — não apague o que já está lá.

```json
{
  "mcpServers": {
    "ElevenLabs": {
      "command": "uvx",
      "args": ["elevenlabs-mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "SUA_CHAVE_AQUI"
      }
    }
  }
}
```

Troque `SUA_CHAVE_AQUI` pela chave real. Salve e **feche o Claude Desktop por
completo** (no Mac, `Cmd+Q` — fechar a janela não basta), depois abra de novo.

Deu certo quando aparece o ícone de ferramentas na caixa de mensagem, com as
ferramentas do ElevenLabs listadas.

## 4. Se der erro

**`uvx` não encontrado (Windows)** — troque `"command": "uvx"` pelo caminho
completo. Descubra com `where uvx` no CMD e use barras duplas:

```json
"command": "C:\\Users\\SeuUsuario\\.local\\bin\\uvx.exe"
```

No Mac/Linux o equivalente é `which uvx` (costuma ser
`/Users/seunome/.local/bin/uvx`).

**O servidor não aparece** — quase sempre é vírgula faltando ou sobrando no
JSON. Cole o arquivo inteiro num validador de JSON antes de desistir.

**Erro de autenticação** — chave errada, com espaço no começo/fim, ou já
revogada no site.

---

## Cuidado com a cota

O MCP gera áudio a cada pedido, sem avisar quanto vai custar. No plano free são
cerca de 10 mil caracteres por mês — um vídeo do canal consome quase tudo.
Antes de mandar gerar um roteiro inteiro pelo chat, rode:

```bash
python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --simular
```

para saber o tamanho, e `python3 scripts/narrar.py --saldo` para ver o que
ainda resta no mês.

## Atenção à chave no arquivo

A chave fica em texto puro dentro do `claude_desktop_config.json`. Esse arquivo
vive no seu computador e **não pertence a este repositório** — nunca copie o
conteúdo dele para cá, nem para prints ou conversas.
