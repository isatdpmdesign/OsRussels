param([Parameter(Mandatory=$true)][string]$Path)

$files = if (Test-Path -LiteralPath $Path -PathType Container) {
    Get-ChildItem -LiteralPath $Path -Filter '*.md' -File -Recurse
} else { Get-Item -LiteralPath $Path }

$patterns = [ordered]@{
    'terapia-moderna' = '\b(processar|vulnerabilidade|dar espaço|se permitir|limites emocionais|conexão emocional)\b'
    'cliche-corporal' = 'sangue gelar|boca seca|tempo parou|arrepio (subiu|percorreu)|respiração que não sabia'
    'moldura-abstrata' = '\b(como quem|do jeito que|a forma como|o modo como|a precisão com que)\b'
    'simetria' = '\bnão (era|foi|estava|tinha)\b.{0,100}\b(era|foi|estava|tinha)\b'
    'explicacao' = '\bporque\b'
    'palavra-banida' = '\b(peso|pesar|pesava|pesou|pesad\w*)\b'
}

foreach ($file in $files) {
    $lines = Get-Content -LiteralPath $file.FullName -Encoding UTF8
    foreach ($name in $patterns.Keys) {
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match $patterns[$name]) {
                [PSCustomObject]@{arquivo=$file.FullName; linha=$i+1; categoria=$name; trecho=$lines[$i].Trim()}
            }
        }
    }
}
