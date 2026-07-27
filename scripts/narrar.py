#!/usr/bin/env python3
"""
Gera a narração dos roteiros do canal usando a API do ElevenLabs.

Só usa a biblioteca padrão do Python — não precisa instalar nada.

Exemplos:
    python3 scripts/narrar.py --saldo
    python3 scripts/narrar.py --vozes
    python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --simular
    python3 scripts/narrar.py roteiro-video-11-poco-de-kola.md --voz "Nome da Voz"
    python3 scripts/narrar.py narracao-elevenlabs.md --partes 1-5

A chave da API vem da variável de ambiente ELEVENLABS_API_KEY ou do arquivo
.env na raiz do repositório (que NÃO é versionado).
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
RAIZ = Path(__file__).resolve().parent.parent

# Modelo multilíngue: é o que entrega português natural.
MODELO_PADRAO = "eleven_multilingual_v2"
FORMATO_PADRAO = "mp3_44100_128"

# Valores recomendados em narracao-elevenlabs.md (documentário, voz grave).
VOZ_PADRAO_CONFIG = {
    "stability": 0.45,
    "similarity_boost": 0.75,
    "style": 0.20,
    "use_speaker_boost": True,
}

# A API aceita mais que isso, mas blocos menores falham menos e permitem
# refazer só um pedaço quando a leitura sai ruim.
MAX_CARACTERES_BLOCO = 2500


# --------------------------------------------------------------------------
# Chave da API
# --------------------------------------------------------------------------

def carregar_env():
    """Lê o .env da raiz para o ambiente, sem sobrescrever o que já existe."""
    env = RAIZ / ".env"
    if not env.exists():
        return
    for linha in env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        os.environ.setdefault(chave.strip(), valor.strip().strip("'\""))


def pegar_chave():
    carregar_env()
    chave = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not chave:
        sys.exit(
            "Chave da API não encontrada.\n"
            "Crie um arquivo .env na raiz do repositório com a linha:\n"
            "  ELEVENLABS_API_KEY=sua_chave_aqui\n"
            "ou rode: export ELEVENLABS_API_KEY=sua_chave_aqui"
        )
    return chave


# --------------------------------------------------------------------------
# Chamadas HTTP
# --------------------------------------------------------------------------

def requisitar(caminho, chave, dados=None, binario=False, tentativas=4):
    """GET (dados=None) ou POST JSON. Repete em erro temporário."""
    url = caminho if caminho.startswith("http") else API + caminho
    corpo = json.dumps(dados).encode("utf-8") if dados is not None else None
    espera = 2

    for tentativa in range(1, tentativas + 1):
        req = urllib.request.Request(url, data=corpo)
        req.add_header("xi-api-key", chave)
        if corpo:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                conteudo = resp.read()
                id_req = resp.headers.get("request-id", "")
                return (conteudo, id_req) if binario else json.loads(conteudo)
        except urllib.error.HTTPError as erro:
            detalhe = erro.read().decode("utf-8", "replace")[:400]
            if erro.code == 401:
                sys.exit("Chave da API inválida ou revogada (401).")
            if erro.code == 402:
                sys.exit(f"Sem créditos de caracteres no plano (402). {detalhe}")
            temporario = erro.code == 429 or erro.code >= 500
            if not temporario or tentativa == tentativas:
                sys.exit(f"Erro {erro.code} em {url}\n{detalhe}")
            print(f"  ! erro {erro.code}, tentando de novo em {espera}s")
        except urllib.error.URLError as erro:
            if tentativa == tentativas:
                sys.exit(f"Falha de rede ao chamar {url}: {erro.reason}")
            print(f"  ! rede instável ({erro.reason}), nova tentativa em {espera}s")
        time.sleep(espera)
        espera *= 2


# --------------------------------------------------------------------------
# Leitura dos roteiros
# --------------------------------------------------------------------------

# Linhas que são produção, não narração: prompts de imagem, tabelas, listas,
# títulos, blocos de código, avisos em negrito.
RUIDO = re.compile(r"^(#|\||>|---|\*\*|```|\d+\.\s|[-*]\s)")


def limpar(texto):
    """Tira marcação markdown que o TTS leria em voz alta."""
    texto = re.sub(r"`([^`]*)`", r"\1", texto)
    texto = re.sub(r"\*\*([^*]*)\*\*", r"\1", texto)
    texto = re.sub(r"\*([^*]*)\*", r"\1", texto)
    texto = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texto)
    return re.sub(r"\s+", " ", texto).strip()


def extrair_partes(caminho):
    """Devolve [(numero, titulo, texto)] com só os parágrafos de narração."""
    linhas = Path(caminho).read_text(encoding="utf-8").splitlines()

    # Se o arquivo tem uma seção "NARRAÇÃO", tudo antes dela é produção.
    inicio, fim = 0, len(linhas)
    for i, linha in enumerate(linhas):
        if linha.startswith("#") and "NARRA" in _sem_acento(linha).upper():
            inicio = i + 1
            for j in range(inicio, len(linhas)):
                # Um novo título de nível 1 encerra a narração.
                if re.match(r"^#\s", linhas[j]):
                    fim = j
                    break
            break

    partes = []
    numero, titulo, buffer = 0, "Narração", []
    dentro_de_codigo = False
    pulando = False  # ignora o resto de um bloco de produção até a linha em branco

    for linha in linhas[inicio:fim]:
        crua = linha.strip()

        if crua.startswith("```"):
            dentro_de_codigo = not dentro_de_codigo
            continue
        if dentro_de_codigo:
            continue

        if not crua:
            pulando = False
            continue

        cabecalho = re.match(r"^##+\s*PARTE\s*(\d+)\s*[—\-–:]*\s*(.*)$", crua, re.I)
        if cabecalho:
            if buffer:
                partes.append((numero, titulo, "\n\n".join(buffer)))
            numero = int(cabecalho.group(1))
            titulo = limpar(cabecalho.group(2)) or f"Parte {numero}"
            buffer = []
            pulando = False
            continue

        # Um bloco de produção (nota em negrito, lista de prompts, tabela)
        # costuma ocupar várias linhas seguidas: descarta até o parágrafo acabar.
        if RUIDO.match(crua):
            pulando = True
            continue
        if pulando:
            continue

        texto = limpar(linha)
        if texto:
            buffer.append(texto)

    if buffer:
        partes.append((numero, titulo, "\n\n".join(buffer)))

    partes = [p for p in partes if p[2].strip()]

    # Se o arquivo tem "PARTE N", o texto solto antes da parte 1 é cabeçalho.
    if any(p[0] > 0 for p in partes):
        partes = [p for p in partes if p[0] > 0]
    elif partes:
        # Arquivo sem cabeçalhos "PARTE": vira uma parte única.
        partes = [(1, partes[0][1], "\n\n".join(p[2] for p in partes))]

    return partes


def dividir_em_blocos(texto, limite):
    """Quebra em blocos <= limite, cortando entre parágrafos ou frases."""
    blocos, atual = [], ""
    for paragrafo in texto.split("\n\n"):
        pedacos = [paragrafo]
        if len(paragrafo) > limite:
            pedacos, frase = [], ""
            for parte in re.split(r"(?<=[.!?])\s+", paragrafo):
                if len(frase) + len(parte) + 1 > limite and frase:
                    pedacos.append(frase.strip())
                    frase = ""
                frase += parte + " "
            if frase.strip():
                pedacos.append(frase.strip())

        for pedaco in pedacos:
            if len(atual) + len(pedaco) + 2 > limite and atual:
                blocos.append(atual.strip())
                atual = ""
            atual += pedaco + "\n\n"

    if atual.strip():
        blocos.append(atual.strip())
    return blocos


def _sem_acento(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def apelido(caminho):
    nome = Path(caminho).stem
    nome = _sem_acento(nome).lower()
    return re.sub(r"[^a-z0-9]+", "-", nome).strip("-")


# --------------------------------------------------------------------------
# Vozes e conta
# --------------------------------------------------------------------------

def listar_vozes(chave):
    return requisitar("/voices", chave).get("voices", [])


def resolver_voz(chave, pedida):
    vozes = listar_vozes(chave)
    if not vozes:
        sys.exit("Nenhuma voz encontrada na conta.")

    if not pedida:
        return vozes[0]["voice_id"], vozes[0]["name"]

    for voz in vozes:
        if voz["voice_id"] == pedida or voz["name"].lower() == pedida.lower():
            return voz["voice_id"], voz["name"]

    for voz in vozes:
        if pedida.lower() in voz["name"].lower():
            return voz["voice_id"], voz["name"]

    disponiveis = ", ".join(v["name"] for v in vozes)
    sys.exit(f"Voz '{pedida}' não existe na sua conta.\nDisponíveis: {disponiveis}")


def mostrar_saldo(chave):
    conta = requisitar("/user/subscription", chave)
    usado = conta.get("character_count", 0)
    total = conta.get("character_limit", 0)
    print(f"Plano:          {conta.get('tier', 'desconhecido')}")
    print(f"Caracteres:     {usado:,} de {total:,} usados".replace(",", "."))
    print(f"Ainda disponível: {max(total - usado, 0):,} caracteres".replace(",", "."))
    return max(total - usado, 0)


# --------------------------------------------------------------------------
# Geração
# --------------------------------------------------------------------------

def gerar_parte(chave, voz_id, texto, destino, config, modelo, formato, limite):
    blocos = dividir_em_blocos(texto, limite)
    audio = bytearray()
    anteriores = []

    for i, bloco in enumerate(blocos, 1):
        corpo = {
            "text": bloco,
            "model_id": modelo,
            "voice_settings": config,
        }
        # Mantém o mesmo tom entre blocos da mesma parte.
        if anteriores:
            corpo["previous_request_ids"] = anteriores[-3:]

        print(f"    bloco {i}/{len(blocos)} ({len(bloco)} caracteres)")
        conteudo, id_req = requisitar(
            f"/text-to-speech/{voz_id}?output_format={formato}",
            chave, dados=corpo, binario=True,
        )
        audio.extend(conteudo)
        if id_req:
            anteriores.append(id_req)

    destino.write_bytes(bytes(audio))
    return len(audio)


def main():
    ap = argparse.ArgumentParser(
        description="Gera a narração dos roteiros do canal no ElevenLabs.",
    )
    ap.add_argument("arquivo", nargs="?", help="roteiro .md ou .txt a narrar")
    ap.add_argument("--voz", help="nome ou ID da voz (padrão: a primeira da conta)")
    ap.add_argument("--vozes", action="store_true", help="lista as vozes da conta e sai")
    ap.add_argument("--saldo", action="store_true", help="mostra os caracteres restantes e sai")
    ap.add_argument("--partes", help="quais partes gerar, ex: 3 ou 1-5 ou 2,4,7")
    ap.add_argument("--saida", default="audio", help="pasta de destino (padrão: audio)")
    ap.add_argument("--simular", action="store_true", help="mostra o que seria gerado sem gastar créditos")
    ap.add_argument("--forcar", action="store_true", help="regera partes cujo MP3 já existe")
    ap.add_argument("--modelo", default=MODELO_PADRAO)
    ap.add_argument("--formato", default=FORMATO_PADRAO)
    ap.add_argument("--estabilidade", type=float, default=VOZ_PADRAO_CONFIG["stability"])
    ap.add_argument("--similaridade", type=float, default=VOZ_PADRAO_CONFIG["similarity_boost"])
    ap.add_argument("--estilo", type=float, default=VOZ_PADRAO_CONFIG["style"])
    ap.add_argument("--max-bloco", type=int, default=MAX_CARACTERES_BLOCO)
    args = ap.parse_args()

    if args.saldo:
        mostrar_saldo(pegar_chave())
        return

    if args.vozes:
        for voz in listar_vozes(pegar_chave()):
            rotulo = voz.get("labels", {})
            extras = ", ".join(f"{k}: {v}" for k, v in rotulo.items()) or voz.get("category", "")
            print(f"{voz['name']:<28} {voz['voice_id']}  {extras}")
        return

    if not args.arquivo:
        ap.error("informe o arquivo do roteiro (ou use --vozes / --saldo)")

    caminho = Path(args.arquivo)
    if not caminho.is_absolute():
        caminho = RAIZ / caminho
    if not caminho.exists():
        sys.exit(f"Arquivo não encontrado: {caminho}")

    partes = extrair_partes(caminho)
    if not partes:
        sys.exit("Nenhum parágrafo de narração encontrado nesse arquivo.")

    if args.partes:
        escolhidas = set()
        for trecho in args.partes.split(","):
            if "-" in trecho:
                ini, fim = trecho.split("-")
                escolhidas.update(range(int(ini), int(fim) + 1))
            else:
                escolhidas.add(int(trecho))
        partes = [p for p in partes if p[0] in escolhidas]
        if not partes:
            sys.exit(f"Nenhuma parte corresponde a '{args.partes}'.")

    total_caracteres = sum(len(p[2]) for p in partes)
    print(f"Arquivo: {caminho.name}")
    print(f"Partes:  {len(partes)}")
    print(f"Total:   {total_caracteres:,} caracteres".replace(",", "."))
    print(f"Duração estimada: ~{total_caracteres / 900:.0f} minutos de narração\n")

    if args.simular:
        for numero, titulo, texto in partes:
            blocos = dividir_em_blocos(texto, args.max_bloco)
            print(f"  PARTE {numero:>2} — {titulo}")
            print(f"     {len(texto):,} caracteres em {len(blocos)} bloco(s)".replace(",", "."))
            print(f"     início: {texto[:90]}...\n")
        print("Simulação: nenhum crédito foi gasto.")
        return

    chave = pegar_chave()
    restante = mostrar_saldo(chave)
    print()
    if restante < total_caracteres:
        print(
            f"AVISO: faltam {total_caracteres - restante:,} caracteres no plano. "
            "Use --partes para gerar por etapas.\n".replace(",", ".")
        )

    voz_id, voz_nome = resolver_voz(chave, args.voz)
    config = {
        "stability": args.estabilidade,
        "similarity_boost": args.similaridade,
        "style": args.estilo,
        "use_speaker_boost": True,
    }
    print(f"Voz: {voz_nome} ({voz_id})")
    print(f"Modelo: {args.modelo}\n")

    pasta = RAIZ / args.saida / apelido(caminho)
    pasta.mkdir(parents=True, exist_ok=True)

    gerados = 0
    for numero, titulo, texto in partes:
        destino = pasta / f"parte-{numero:02d}.mp3"
        if destino.exists() and not args.forcar:
            print(f"  PARTE {numero:>2} — já existe, pulando ({destino.name})")
            continue

        print(f"  PARTE {numero:>2} — {titulo}")
        tamanho = gerar_parte(
            chave, voz_id, texto, destino, config,
            args.modelo, args.formato, args.max_bloco,
        )
        print(f"    -> {destino.relative_to(RAIZ)} ({tamanho / 1024:.0f} KB)\n")
        gerados += 1

    print(f"Pronto: {gerados} parte(s) gerada(s) em {pasta.relative_to(RAIZ)}/")
    if gerados:
        print("Importe os MP3 no CapCut na ordem das partes.")


if __name__ == "__main__":
    main()
