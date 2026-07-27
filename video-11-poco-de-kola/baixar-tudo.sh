#!/usr/bin/env bash
# =============================================================================
# BAIXAR TODOS OS ARQUIVOS DO VÍDEO 11 — "O Buraco Mais Fundo do Mundo"
# =============================================================================
# COMO USAR (no SEU computador, não no Claude):
#   1. Abra o terminal na pasta onde quer os arquivos
#   2. bash baixar-tudo.sh
#
# No Windows: instale o Git Bash e rode o mesmo comando.
# Alternativa sem terminal: os links estão no README.md desta pasta.
#
# Resultado: pasta imagens/ com 64 PNGs numerados por parte (p1-01 ... p8-08)
#            pasta audios/ com 8 WAVs (parte-1 ... parte-8)
# =============================================================================

set -u
B="https://d8j0ntlcm91z4.cloudfront.net/user_3GKIAKgYOSQKEUc441wzOg8x9ZW"
mkdir -p imagens audios

echo "==> Baixando 64 imagens..."

# ---------- PARTE 1 — GANCHO ----------
curl -sSL "$B/hf_20260727_174632_0051ce2c-6dbe-44bd-a287-cb8e881b2894.png" -o imagens/p1-01-tampa-soldada-neve.png
curl -sSL "$B/hf_20260727_174708_72151936-609d-4e09-829a-9bfb29fb9025.png" -o imagens/p1-02-boca-do-poco.png
curl -sSL "$B/hf_20260727_174724_29198447-5202-40ac-a588-65efb5bc1ede.png" -o imagens/p1-03-corte-terra-linha-fina.png
curl -sSL "$B/hf_20260727_174731_61702e7f-4555-4f03-beb5-a6a2dda4d272.png" -o imagens/p1-04-torre-abandonada.png
curl -sSL "$B/hf_20260727_174734_a3667f96-135a-4a5f-aa75-e3ba200657d1.png" -o imagens/p1-05-sala-controle-abandonada.png
curl -sSL "$B/hf_20260727_174742_54959c59-0fa4-491b-a028-d987ad203863.png" -o imagens/p1-06-mao-na-tampa.png
curl -sSL "$B/hf_20260727_174745_c79ee685-1380-42d3-b851-c6d64533da4b.png" -o imagens/p1-07-aerea-complexo-isolado.png
curl -sSL "$B/hf_20260727_174747_4c99be9e-2460-4655-8ec3-4f13e41c16cf.png" -o imagens/p1-08-escadas-congeladas.png

# ---------- PARTE 2 — A CORRIDA PARA BAIXO ----------
curl -sSL "$B/hf_20260727_174750_3d714fc4-a38f-40a6-8d8f-c9d0e672f2c7.png" -o imagens/p2-01-foguete-guerra-fria.png
curl -sSL "$B/hf_20260727_174816_151739bc-dc16-4c5a-943a-ea0d77cd4d84.png" -o imagens/p2-02-engenheiros-sovieticos.png
curl -sSL "$B/hf_20260727_174820_bffc04a2-cc31-4d89-aea3-cafe0df688aa.png" -o imagens/p2-03-montagem-da-torre.png
curl -sSL "$B/hf_20260727_174824_98e19c7c-1e1b-4050-8d41-c50ae71c0cf3.png" -o imagens/p2-04-calendario-1970.png
curl -sSL "$B/hf_20260727_174830_b4f80a1a-efe2-4d3e-b0c1-6359ec8a791f.png" -o imagens/p2-05-navio-perfuracao-eua.png
curl -sSL "$B/hf_20260727_174856_31dae169-4abb-4430-abac-00e849764728.png" -o imagens/p2-06-mapa-guerra-fria.png
curl -sSL "$B/hf_20260727_174921_6ef2e12f-6516-49b2-b233-6abcc736fa00.png" -o imagens/p2-07-broca-nova.png
curl -sSL "$B/hf_20260727_174925_a815f3c8-fff9-4391-9346-2b091f778b59.png" -o imagens/p2-08-trabalhadores-neve.png

# ---------- PARTE 3 — 24 ANOS DESCENDO ----------
curl -sSL "$B/hf_20260727_174932_5161d265-1c6a-48c1-8f17-1239a4a2fbab.png" -o imagens/p3-01-tubos-de-aco.png
curl -sSL "$B/hf_20260727_174957_a694e1ab-006f-4a22-873f-3cc4f3cb388b.png" -o imagens/p3-02-broca-na-rocha.png
curl -sSL "$B/hf_20260727_175012_5d66e8ea-6d3a-43bb-9fb8-58ba554001da.png" -o imagens/p3-03-testemunho-rocha.png
curl -sSL "$B/hf_20260727_175020_bba46ef0-8da2-4840-b8d4-d07d28490c62.png" -o imagens/p3-04-medidor-profundidade.png
curl -sSL "$B/hf_20260727_175041_3172b988-2e6a-474e-a8c3-c2fb1cd1cdec.png" -o imagens/p3-05-diagrama-ramificacoes.png
curl -sSL "$B/hf_20260727_175059_f9a2e44e-fe76-48c2-a5ed-4f8df937144f.png" -o imagens/p3-06-comemoracao-1989.png
curl -sSL "$B/hf_20260727_175110_0bdb42fa-6ddc-498d-b39b-5e83db482aa4.png" -o imagens/p3-07-tubos-empilhados.png
curl -sSL "$B/hf_20260727_175138_ac41af24-a40e-4ffd-9936-c06cde7980fb.png" -o imagens/p3-08-guincho-gigante.png

# ---------- PARTE 4 — AS TRÊS DESCOBERTAS ----------
curl -sSL "$B/hf_20260727_175215_93bff169-9ddb-4078-b3f9-9a5c68b0dc32.png" -o imagens/p4-01-livro-geologia.png
curl -sSL "$B/hf_20260727_175228_3293eb48-6da8-43a9-a121-77466f7e4260.png" -o imagens/p4-02-granito-com-agua.png
curl -sSL "$B/hf_20260727_175233_7b41e53f-2e99-4b39-91d5-c9309462d7b8.png" -o imagens/p4-03-agua-dos-cristais.png
curl -sSL "$B/hf_20260727_175317_bfb5356b-bcd7-4a00-951d-36c0b1b5b6c7.png" -o imagens/p4-04-microfosseis.png
curl -sSL "$B/hf_20260727_175340_00284ca6-e356-4fb8-bfe3-734eb1f737c6.png" -o imagens/p4-05-lama-hidrogenio.png
curl -sSL "$B/hf_20260727_175345_201d830e-6a67-4c8e-933b-58ffbd80fd1c.png" -o imagens/p4-06-cientistas-confusos.png
curl -sSL "$B/hf_20260727_175427_53c12ef1-4781-4735-a87d-f2a717e7eb9a.png" -o imagens/p4-07-amostra-2-bilhoes-anos.png
curl -sSL "$B/hf_20260727_175601_9a1cf712-66ec-482a-8d1c-9f74c4e41381.png" -o imagens/p4-08-laboratorio-amostras.png

# ---------- PARTE 5 — POR QUE PARARAM ----------
curl -sSL "$B/hf_20260727_175640_865103c3-d42a-4872-95f2-3ed3f87c35cc.png" -o imagens/p5-01-medidor-no-vermelho.png
curl -sSL "$B/hf_20260727_175801_a18157ce-3738-4eb1-b1ff-a23ac0a35ef2.png" -o imagens/p5-02-rocha-incandescente.png
curl -sSL "$B/hf_20260727_175806_116d97d6-e34b-4bd9-85c2-4c36f0392611.png" -o imagens/p5-03-rocha-plastica.png
curl -sSL "$B/hf_20260727_175812_dc6c9c3c-61b6-4f30-9b5e-762111c38061.png" -o imagens/p5-04-broca-quebrada.png
curl -sSL "$B/hf_20260727_175834_b0df1ef8-a5d3-4ab0-a2d5-90e05b9f4f9e.png" -o imagens/p5-05-poco-se-fechando.png
curl -sSL "$B/hf_20260727_180019_6ac9944b-0d90-4618-a9d0-9db58fa4a3c0.png" -o imagens/p5-06-bandeira-sovietica-1991.png
curl -sSL "$B/hf_20260727_180023_67345060-982b-4d55-9685-4d5106e8db9d.png" -o imagens/p5-07-instalacao-abandonada.png
curl -sSL "$B/hf_20260727_180026_c603e4cd-d967-4147-b5a3-670be2dff830.png" -o imagens/p5-08-ultima-luz-apagando.png

# ---------- PARTE 6 — A LENDA DO POÇO DO INFERNO ----------
curl -sSL "$B/hf_20260727_180207_6b586166-e9dc-4f89-a580-d15e7e43298d.png" -o imagens/p6-01-microfone-descendo.png
curl -sSL "$B/hf_20260727_180315_e1126989-78f4-4e97-8b9f-9a99c6d56180.png" -o imagens/p6-02-gravador-de-rolo.png
curl -sSL "$B/hf_20260727_180318_740b945f-37bb-4069-b96f-d38a0737cd6b.png" -o imagens/p6-03-jornal-tabloide.png
curl -sSL "$B/hf_20260727_180322_35cd57be-1e64-4c66-953f-8cb5b059c4db.png" -o imagens/p6-04-projetor-filme-terror.png
curl -sSL "$B/hf_20260727_180332_65527ac4-87ed-4f7f-b9cc-c7c3658c5e0c.png" -o imagens/p6-05-computadores-anos-90.png
curl -sSL "$B/hf_20260727_180340_a3a0b542-2410-4917-b589-720b9be3aec4.png" -o imagens/p6-06-carimbo-falso.png
curl -sSL "$B/hf_20260727_180346_d8504c4c-0c98-4be7-8707-ed988c611e16.png" -o imagens/p6-07-fita-cassete.png
curl -sSL "$B/hf_20260727_180439_14be4ef3-c1e9-41ac-b539-f53f8ec42e84.png" -o imagens/p6-08-ouvindo-com-medo.png

# ---------- PARTE 7 — A VIAGEM AO CENTRO ----------
curl -sSL "$B/hf_20260727_180757_260026ce-d645-4138-bf16-98265418581f.png" -o imagens/p7-01-crosta-para-manto.png
curl -sSL "$B/hf_20260727_180851_e7e5cfa7-8e43-481f-864b-b83d8bcbe970.png" -o imagens/p7-02-rocha-derretida.png
curl -sSL "$B/hf_20260727_180854_c6d018c2-4fca-42bd-a109-d09f2467abe5.png" -o imagens/p7-03-oceano-metal-liquido.png
curl -sSL "$B/hf_20260727_181112_8e99d414-3aed-4285-9c2d-7ced1158bdf2.png" -o imagens/p7-04-nucleo-interno.png
curl -sSL "$B/hf_20260727_181142_afa0df79-d2fe-44ed-ae63-47fbeea763ec.png" -o imagens/p7-05-superficie-do-sol.png
curl -sSL "$B/hf_20260727_181145_85d0a507-f554-4444-9002-c3ebeaf22e1b.png" -o imagens/p7-06-nucleo-girando.png
curl -sSL "$B/hf_20260727_181148_9a2e878c-7bd8-4500-83e3-b1c5f7c8a504.png" -o imagens/p7-07-corte-completo-terra.png
curl -sSL "$B/hf_20260727_181204_26caed1e-84b0-49ff-b650-17ff9b4c0d4e.png" -o imagens/p7-08-escala-lua-nucleo.png

# ---------- PARTE 8 — A REVELAÇÃO + TEASER ----------
curl -sSL "$B/hf_20260727_181208_5ded1b4b-f851-4c12-9915-48fb507722d7.png" -o imagens/p8-01-campo-magnetico.png
curl -sSL "$B/hf_20260727_181210_956b29b3-6bc6-433f-9359-2145f2e01740.png" -o imagens/p8-02-vento-solar-desviado.png
curl -sSL "$B/hf_20260727_181230_bd903814-755d-484d-b05a-1457adc1051c.png" -o imagens/p8-03-aurora-boreal.png
curl -sSL "$B/hf_20260727_181233_a0a5d486-4c68-4a73-9069-06aa8a37cf7b.png" -o imagens/p8-04-marte-morto.png
curl -sSL "$B/hf_20260727_181235_ff6b7eb0-4ae9-4592-9439-1e970b165684.png" -o imagens/p8-05-ceu-protegido.png
curl -sSL "$B/hf_20260727_181241_3d0ed8b7-2c2e-47d7-bc11-31af3720a396.png" -o imagens/p8-06-teaser-chernobyl.png
curl -sSL "$B/hf_20260727_181446_8610de75-9780-437f-b525-7e23871ad075.png" -o imagens/p8-07-terra-viva.png
curl -sSL "$B/hf_20260727_181455_e12e6866-0acf-4164-b748-4dc314da31a3.png" -o imagens/p8-08-tampa-com-aurora.png

echo "==> Baixando 8 áudios da narração..."
# Os links dos áudios estão no README.md (seção ÁUDIOS) — cole-os abaixo se
# este bloco estiver vazio, ou baixe direto pelo higgsfield.ai > Generations.
while IFS='|' read -r nome url; do
  [ -z "${url:-}" ] && continue
  curl -sSL "$url" -o "audios/${nome}.wav"
done < audios-lista.txt 2>/dev/null || echo "    (use audios-lista.txt ou baixe pelo README)"

echo ""
echo "==> PRONTO!"
echo "    imagens/  -> $(ls imagens 2>/dev/null | wc -l) arquivos"
echo "    audios/   -> $(ls audios 2>/dev/null | wc -l) arquivos"
