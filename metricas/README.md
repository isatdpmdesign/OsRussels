# Métricas — arquivo permanente

O Windsor (trial) só devolve os últimos 30 dias. Este diretório e o painel do Notion
("📊 Painel de métricas — Dora & O Afilhado", na wiki Romance no Bolso) são o histórico.

## Protocolo semanal (Claude)
1. Puxar no Windsor, sempre com `date_preset: last_29dT`. Com `last_30d` ou mais, o trial recusa.
   - instagram: diário (`reach, views, follower_count, accounts_engaged, total_interactions, likes, comments, saves, shares, replies`), seguidores e não seguidores (`reach_followers, reach_non_followers, views_followers, views_non_followers`), posts (`media_*`), `followers_count`, gênero/idade e cidade.
   - youtube: por vídeo (`video, video_title, views, estimated_minutes_watched, average_view_duration, average_view_percentage, subscribers_gained`), diário do canal, `traffic_source`, `device_type` e a curva de retenção (`elapsed_video_time_ratio, audience_watch_ratio, relative_retention_performance` com filtro `video eq <id>`).
2. Salvar tudo, sem resumo, em `brutos/AAAA-MM-DD.json`.
3. Criar uma linha nova no painel do Notion: propriedades de resumo, mais as tabelas completas no corpo da página.
4. Comparar com a semana anterior e escrever uma "Decisão".

## Contas
- Instagram `dora.escreve`: conector `instagram`, conta 17841431680176074
- YouTube "Romance no Bolso": conector `youtube`, conta 112008. Playlist O Afilhado: `PLMzOeRZnDZOg`
- Cap 1 antigo: HFEVakugfaQ. Quando o novo for publicado, anotar o ID aqui.
