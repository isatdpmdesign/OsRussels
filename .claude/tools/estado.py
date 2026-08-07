#!/usr/bin/env python3
"""
estado.py — o estado do projeto, DERIVADO dos arquivos.

Por que existe: seis meses de disciplina notável não bastaram para manter
MANIFESTO, RETOMADA, ficha, bíblia, sinopse e diretrizes sincronizados
entre si. Chegaram a divergir em doze capítulos. A lição não é "faltou
cuidado" — é que **estado de produção não deve ser um arquivo que alguém
mantém à mão.** Deve ser uma view, calculada toda vez que se olha.

Isto é o motor da ideia. No OpenBooks, é a tela inicial do projeto.

Uso:
    python3 .claude/tools/estado.py --projeto "Os Russels"
    python3 .claude/tools/estado.py --projeto "Os Russels" --md > ESTADO.md
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from collections import Counter

try:
    import yaml
except ImportError:
    sys.exit("Falta pyyaml. Rode: pip install pyyaml")


def achar_projeto(inicio: str) -> str:
    d = os.path.abspath(inicio)
    if os.path.isfile(d):
        d = os.path.dirname(d)
    while True:
        if os.path.isfile(os.path.join(d, "livro.yaml")):
            return d
        pai = os.path.dirname(d)
        if pai == d:
            sys.exit(f"Não achei livro.yaml acima de {inicio!r}.")
        d = pai


def ler_capitulos(base: str, cfg: dict) -> list[dict]:
    caps = []
    for caminho in sorted(glob.glob(os.path.join(base, cfg["caminhos"]["capitulos"]))):
        nome = os.path.basename(caminho)
        m = re.match(r"capitulo-(\d+)-(.+?)-([a-z]+)\.md$", nome)
        if not m:
            continue
        texto = open(caminho, encoding="utf-8").read()
        linhas = texto.splitlines()
        caps.append({
            "n": int(m.group(1)),
            "slug": m.group(2).replace("-", " "),
            "pov": m.group(3),
            "palavras": len(texto.split()),
            "linhas": len(linhas),
            "maxcol": max((len(l) for l in linhas), default=0),
            "cabecalho": linhas[0] if linhas else "",
            "rodape": "Continua no Capítulo" in texto,
            "caminho": caminho,
        })
    return caps


# Guias que acompanham o andamento dos capítulos. Perfil de voz e de
# estilo não rastreiam capítulo nenhum — citar o cap 25 numa regra de
# hard wrap não os torna desatualizados.
GUIAS_QUE_RASTREIAM = {"canon", "ficha", "sinopse", "decisoes",
                       "diretrizes", "errata"}


def frescor_dos_guias(base: str, cfg: dict, ultimo: int) -> list[tuple[str, int, str]]:
    """Compara o capítulo mais alto citado em cada guia com o que existe."""
    saida = []
    for chave, rel in cfg["caminhos"].items():
        if chave not in GUIAS_QUE_RASTREIAM:
            continue
        caminho = os.path.join(base, rel)
        if not os.path.isfile(caminho):
            continue
        texto = open(caminho, encoding="utf-8").read()
        nums = [int(n) for n in
                re.findall(r"(?:[Cc]ap\.?|[Cc]apítulo)\s*(\d{1,2})\b", texto)]
        nums += [int(n) for n in re.findall(r"capitulo-(\d{2})", texto)]
        maior = max(nums) if nums else 0
        atraso = ultimo - maior
        if maior == 0:
            estado = "não cita capítulos"
        elif atraso > 2:
            estado = f"⚠️  {atraso} capítulos atrás"
        else:
            estado = "ok"
        saida.append((rel, maior, estado))
    return saida


def mil(n: int) -> str:
    """12345 -> 12.345 (sem estragar o resto da linha)."""
    return f"{n:,}".replace(",", ".")


def blocos(cfg: dict) -> list[tuple[str, int, int]]:
    return [(a["nome"], a["capitulos"][0], a["capitulos"][1])
            for a in cfg.get("estrutura", {}).get("atos", [])]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--projeto", default=".")
    ap.add_argument("--md", action="store_true", help="saída em markdown")
    args = ap.parse_args()

    base = achar_projeto(args.projeto)
    cfg = yaml.safe_load(open(os.path.join(base, "livro.yaml"), encoding="utf-8"))
    caps = ler_capitulos(base, cfg)
    if not caps:
        sys.exit("Nenhum capítulo encontrado.")

    conv = cfg["convencoes"]
    largura = conv.get("hard_wrap")
    desde = conv.get("hard_wrap_a_partir_de", 0)
    cabecalho_ok = conv.get("cabecalho_esperado")
    faixa = conv.get("palavras_por_capitulo", {})
    ultimo = max(c["n"] for c in caps)

    p = print
    p(f"\n# Estado — {cfg['projeto']['titulo']} · {cfg['projeto']['obra']}\n")
    total = sum(c["palavras"] for c in caps)
    p(f"**{len(caps)} capítulos · {mil(total)} palavras · "
      f"média {mil(total // len(caps))} por capítulo**")
    p(f"\nEstado declarado: {cfg.get('estrutura', {}).get('estado', '—')}\n")

    # ── Por ato ────────────────────────────────────────────────
    p("## Ritmo por ato\n")
    p("| Ato | Caps | Média | Mín | Máx | POV |")
    p("|---|---|---|---|---|---|")
    for nome, ini, fim in blocos(cfg):
        bloco = [c for c in caps if ini <= c["n"] <= fim]
        if not bloco:
            continue
        pal = [c["palavras"] for c in bloco]
        pov = Counter(c["pov"] for c in bloco)
        pov_txt = " ".join(f"{k}×{v}" for k, v in pov.most_common())
        p(f"| {nome} | {ini}–{fim} | {mil(sum(pal)//len(pal))} | "
          f"{mil(min(pal))} | {mil(max(pal))} | {pov_txt} |")
    p("")

    # ── Alertas ────────────────────────────────────────────────
    alertas = []
    for c in caps:
        if cabecalho_ok and c["cabecalho"] != cabecalho_ok:
            alertas.append((c["n"], "template", f"cabeçalho: {c['cabecalho'][:44]!r}"))
        if not c["rodape"] and c["n"] != ultimo:
            alertas.append((c["n"], "template", "sem rodapé de continuação"))
        if largura and c["n"] >= desde and c["maxcol"] > largura:
            alertas.append((c["n"], "wrap", f"linha de {c['maxcol']} caracteres "
                                           f"(limite {largura})"))
        if faixa.get("minimo") and c["palavras"] < faixa["minimo"]:
            alertas.append((c["n"], "curto", f"{c['palavras']} palavras "
                                            f"(mínimo {faixa['minimo']})"))
        if faixa.get("alerta_acima_de") and c["palavras"] > faixa["alerta_acima_de"]:
            alertas.append((c["n"], "longo", f"{c['palavras']} palavras — "
                                            f"candidato a desdobrar"))
    if alertas:
        p(f"## Alertas ({len(alertas)})\n")
        for n, tipo, det in sorted(alertas):
            p(f"- **cap {n:>2}** · `{tipo}` — {det}")
        p("")

    # ── Frescor dos guias ──────────────────────────────────────
    p("## Frescor dos guias\n")
    p(f"Último capítulo escrito: **{ultimo}**\n")
    p("| Guia | Cap. mais alto citado | |")
    p("|---|---|---|")
    for rel, maior, estado in frescor_dos_guias(base, cfg, ultimo):
        p(f"| `{rel}` | {maior or '—'} | {estado} |")
    p("")

    # ── POV ────────────────────────────────────────────────────
    pov_total = Counter(c["pov"] for c in caps)
    p("## POV no livro inteiro\n")
    for k, v in pov_total.most_common():
        p(f"- **{k}**: {v} capítulos ({v * 100 // len(caps)}%)")
    p("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
