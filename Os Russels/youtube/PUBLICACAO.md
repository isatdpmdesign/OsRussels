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
- Cap 7: agendado 21/11 18:07 (playlist pendente)
- Próximo: cap 8. Ritmo de publicação: a definir.
