# Publicação no YouTube — O Afilhado

Canal: Romance no bolso. Playlist **O Afilhado** (podcast): `PLMzOeRZnDZOg`.

## Fluxo por capítulo
1. Prompt da imagem → a autora gera no Higgsfield e devolve.
2. `gerar-video.py` (vídeo 1080p) + `gerar-thumb.py` (miniatura 1280×720) + `textos/capNN.md`.
3. MP4 e miniatura vão para `youtube/videos/` e `youtube/miniaturas/`; o link raw do GitHub é a mídia do Metricool.
4. Metricool `createScheduledPost` (marca isa.fabricadelps, blogId 7677720, rede youtube; não é para crianças; categoria ENTERTAINMENT; isAiGeneratedContent true, porque a imagem e a voz são geradas por IA).
5. Depois de publicado: Windsor `add_video_to_playlist` (conector youtube, conta 112008) com a playlist acima.

## Estado
- Caps 1–3: a autora subiu manualmente.
- Cap 4: publicado 21/11 — https://www.youtube.com/watch?v=DE9zqrxmdx4 (na playlist)
- Cap 5: publicado 21/11 — https://www.youtube.com/watch?v=z0fiYUIBIgg (na playlist)
- Cap 6: publicado 21/11 — https://www.youtube.com/watch?v=D0l_NUrR-IA (na playlist)
- Cap 7: publicado 21/11 — https://www.youtube.com/watch?v=HAcKwL9mHpA (na playlist)
- Cap 8: agendado 24/11 13:16 (imagem gerada pelo Claude no Higgsfield)
- Próximo: cap 9. Ritmo de publicação: a definir.

## Imagens no Higgsfield (Claude gera direto)
Modelo `nano_banana_pro`, 4:3, ~2 créditos. Elementos travados (`<<<id>>>` no prompt):
- Josh rosto oficial `07fcd21e-caf9-455a-b304-813544cd7bf0` · Josh-jardim `e515bff3-…` · Josh_cidade `cbcad873-…` · Josh-noite `5815d835-…` · Josh-festa `cc8e489a-…`
- Aurora: vestido-amarelo `3d4a2dfb-…` · camisola `a09de102-…` · baile `73ed125e-…` · vestido-azul `822cb596-…` · vestido-bordô `0f48bed4-…` · meio-luto `2d72509b-…`
- Raj `4d6094ff-…` · Eleonora `2a0e54f4-…` · Cassandra `bb5a228c-…` · Erik Mortensen `380f5cc5-…`
- Ambientes: Jardim-em-junho `7e840311-…` · Cozinha-Svensson-6h `dbc203b3-…` · Quarto-leste `126847f2-…` · Sala de música dos Holst `5e8749a0-…` · Celeiro em festa `807f7b1e-…` · Depósito com luar `de36eda5-…`
(IDs completos: elements_search no Higgsfield.)
