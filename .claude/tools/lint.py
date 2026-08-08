#!/usr/bin/env python3
"""
lint.py — passe mecânico determinístico sobre capítulos.

Este arquivo é MOTOR: não sabe nada sobre Josh, Aurora nem a Dinamarca
de 1830. Ele lê o `livro.yaml` do projeto e aplica as regras que
estiverem lá. Trocar de livro = trocar o yaml.

Por que existe: pedir a um modelo que ache interrogação faltando custa
dinheiro e às vezes erra. Isto custa zero e nunca alucina. Tudo que for
verificável por máquina mora aqui, e não numa skill.

Detalhe que importa: as regras trabalham por PARÁGRAFO, não por linha.
Os greps por linha da antiga `revisao-pontuacao` perdiam qualquer coisa
em capítulo com hard wrap — uma fala quebrada em oito linhas passava
inteira. A partir do cap 25 isso é o livro todo.

Uso:
    python3 .claude/tools/lint.py                       # todos os capítulos
    python3 .claude/tools/lint.py CAMINHO.md ...        # arquivos específicos
    python3 .claude/tools/lint.py --resumo              # tabela por capítulo
    python3 .claude/tools/lint.py --regra interrogacao  # uma regra só
    python3 .claude/tools/lint.py --strict              # código 1 se achar algo
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

TRAVESSAO = "—"

# Palavras que não contam como eco (funcionais, frequentes por natureza).
IGNORAR_ECO = {
    "aquilo", "alguma", "alguém", "alguns", "algumas", "aquele", "aquela",
    "aqueles", "aquelas", "porque", "quando", "também", "depois", "antes",
    "ainda", "sempre", "nunca", "então", "assim", "mesmo", "mesma", "outro",
    "outra", "outros", "outras", "primeiro", "primeira", "segundo", "coisa",
    "coisas", "pessoa", "pessoas", "durante", "enquanto", "através",
    "contra", "sobre", "estava", "estavam", "tinha", "tinham", "queria",
    "podia", "fazia", "parecia", "sabia", "disse", "falou", "olhou",
    "ficou", "vinha", "voltou", "deixou", "olhos", "cabeça", "porta",
    "casa", "noite", "manhã", "homem", "menina",
}


# ─────────────────────────────────────────────────────────────  util ──

def achar_projeto(inicio: str) -> str:
    """Sobe diretórios até achar um livro.yaml."""
    d = os.path.abspath(inicio)
    if os.path.isfile(d):
        d = os.path.dirname(d)
    while True:
        if os.path.isfile(os.path.join(d, "livro.yaml")):
            return d
        pai = os.path.dirname(d)
        if pai == d:
            sys.exit("Não achei livro.yaml acima de "
                     f"{inicio!r}. Use --projeto CAMINHO.")
        d = pai


def num_capitulo(caminho: str) -> int | None:
    m = re.search(r"capitulo-(\d+)", os.path.basename(caminho))
    return int(m.group(1)) if m else None


def paragrafos(linhas: list[str]):
    """Agrupa linhas em parágrafos. Devolve (linha_inicial, texto)."""
    buf: list[str] = []
    inicio = 0
    for i, ln in enumerate(linhas, 1):
        if ln.strip():
            if not buf:
                inicio = i
            buf.append(ln.strip())
        elif buf:
            yield inicio, " ".join(buf)
            buf = []
    if buf:
        yield inicio, " ".join(buf)


def e_dialogo(texto: str) -> bool:
    return texto.startswith(TRAVESSAO)


# ───────────────────────────────────────────────────────────  regras ──

def r_template(cfg, cap, linhas, paras, achados):
    conv = cfg["convencoes"]
    esperado = conv.get("cabecalho_esperado")
    if esperado and linhas and linhas[0].rstrip("\n") != esperado:
        achados.append((1, "template",
                        f"cabeçalho difere do padrão: {linhas[0].rstrip()!r}"))
    ultimo = cfg.get("estrutura", {}).get("total_capitulos")
    if cap is not None and cap == ultimo:
        return  # o último capítulo não continua em lugar nenhum
    if "Continua no Capítulo" not in "".join(linhas):
        achados.append((len(linhas), "template",
                        "sem rodapé '*Continua no Capítulo N...*'"))


def r_wrap(cfg, cap, linhas, paras, achados):
    conv = cfg["convencoes"]
    largura = conv.get("hard_wrap")
    desde = conv.get("hard_wrap_a_partir_de", 0)
    if not largura or cap is None or cap < desde:
        return
    excedentes = [(i, len(l.rstrip("\n")))
                  for i, l in enumerate(linhas, 1)
                  if len(l.rstrip("\n")) > largura]
    if excedentes:
        pior = max(e[1] for e in excedentes)
        achados.append((excedentes[0][0], "wrap",
                        f"{len(excedentes)} linhas acima de {largura} "
                        f"caracteres (maior: {pior})"))


def _varre_interrogativas(cfg, paras, achados, chave, rotulo):
    aberturas = cfg["revisao"].get(chave) or []
    if not aberturas:
        return
    padrao = re.compile(r"^(?:%s)\b" % "|".join(re.escape(a) for a in aberturas),
                        re.IGNORECASE)
    verbos = r"disse|perguntou|respondeu|murmurou|completou|falou|repetiu|" \
             r"continuou|acrescentou|insistiu|cortou"
    for ini, texto in paras:
        if not e_dialogo(texto):
            continue
        # Neutraliza intercaladas de narração (— disse ele —).
        fala = re.sub(rf"{TRAVESSAO}[^{TRAVESSAO}]*?(?:{verbos})"
                      rf"[^{TRAVESSAO}]*?(?:{TRAVESSAO}|$)", " | ", texto)
        for frase in re.split(r"(?<=[.!?])\s+|\s*\|\s*", fala):
            frase = frase.strip().lstrip(TRAVESSAO).strip()
            if len(frase) < 3:
                continue
            if padrao.match(frase) and not frase.rstrip().endswith(("?", "!")):
                achados.append((ini, rotulo, frase[:70]))


def r_interrogacao(cfg, cap, linhas, paras, achados):
    """Pergunta com abertura inequívoca terminando sem '?'.

    Erro nº 1 do projeto. Só aberturas de alta confiança entram aqui —
    o livro usa constatação de propósito ("Você vai casar com ele."),
    então abertura verbal ambígua vira ruído e mora na regra irmã.
    """
    _varre_interrogativas(cfg, paras, achados,
                          "inicios_interrogativos", "interrogacao")


def r_interrogacao_ambigua(cfg, cap, linhas, paras, achados):
    """Aberturas verbais que podem ser pergunta ou constatação.

    Fora do passe padrão: precisa de olho humano frase a frase.
    """
    _varre_interrogativas(cfg, paras, achados,
                          "inicios_interrogativos_ambiguos",
                          "interrogacao-ambigua")


def r_travessao_narracao(cfg, cap, linhas, paras, achados):
    """Travessão em parágrafo de narração pura (proibido neste projeto)."""
    if not cfg["convencoes"].get("travessao_so_em_fala", True):
        return
    for ini, texto in paras:
        if e_dialogo(texto) or texto.startswith("#") or texto.startswith("---"):
            continue
        if TRAVESSAO in texto:
            pos = texto.index(TRAVESSAO)
            achados.append((ini, "travessao-narracao",
                            "…" + texto[max(0, pos - 35):pos + 35] + "…"))


def r_blacklist(cfg, cap, linhas, paras, achados):
    for item in cfg["revisao"].get("blacklist", []):
        if cap is not None and cap in (item.get("permitido_em") or []):
            continue
        rx = re.compile(item["termo"], re.IGNORECASE)
        for ini, texto in paras:
            for m in rx.finditer(texto):
                trecho = texto[max(0, m.start() - 30):m.end() + 30]
                achados.append((ini, "blacklist",
                                f"{m.group(0)!r} — …{trecho}…"))


def r_formulas(cfg, cap, linhas, paras, achados):
    rx = re.compile(cfg["revisao"]["formulas"], re.IGNORECASE)
    cota = cfg["revisao"].get("cota_formulas", 10)
    total = sum(len(rx.findall(t)) for _, t in paras)
    if total > cota:
        achados.append((1, "formulas",
                        f"{total} fórmulas 'como quem / do jeito que' "
                        f"(cota: {cota})"))


def r_autorreferencia(cfg, cap, linhas, paras, achados):
    """O personagem não sabe que está num livro."""
    rx = re.compile(r"\b(?:cap\.?|capítulo)\s*\d+", re.IGNORECASE)
    for ini, texto in paras:
        if texto.startswith("#") or texto.startswith("*Continua"):
            continue
        if rx.search(texto):
            achados.append((ini, "autorreferencia", texto[:70]))


def r_sujeira(cfg, cap, linhas, paras, achados):
    for i, ln in enumerate(linhas, 1):
        s = ln.rstrip("\n")
        if re.search(r"\S\s+[,.;:!?](?!\.)", s):
            achados.append((i, "sujeira", "espaço antes de pontuação"))
        if re.search(r"[,;:!?]{2,}", s):
            achados.append((i, "sujeira", "pontuação duplicada"))
        if "  " in s.strip():
            achados.append((i, "sujeira", "espaço duplo"))


# Antes de um nome próprio, estas palavras indicam que ele é sujeito ou
# complemento — não vocativo. Sem isso a regra acusa "— disse Aurora." e
# "com o Josh." e vira ruído puro.
ANTES_NAO_E_VOCATIVO = (
    r"disse|perguntou|respondeu|murmurou|completou|falou|repetiu|"
    r"continuou|acrescentou|insistiu|cortou|gritou|sussurrou|pensou|"
    r"[oa]s?|d[oa]s?|pr[oa]s?|com|de|em|n[oa]s?|ao|à|pel[oa]s?|"
    r"e|ou|que|se|até|contra|sobre|entre|por|sem|tia|tio|senhorita|senhor|"
    r"sou|é|era|foi|são|somos|eram|seja|virou|chamava|chama"
)


def r_vocativo(cfg, cap, linhas, paras, achados):
    """Nome próprio no fim de fala sem a vírgula do vocativo."""
    nomes = "|".join(cfg["personagens"]["protagonistas"]
                     + cfg["personagens"]["elenco"])
    rx = re.compile(rf"\b(?!(?:{ANTES_NAO_E_VOCATIVO})\b)"
                    rf"([a-zà-ú]+)\s+({nomes})\s*[.?!]")
    for ini, texto in paras:
        if not e_dialogo(texto):
            continue
        for m in rx.finditer(texto):
            achados.append((ini, "vocativo",
                            "…" + texto[max(0, m.start() - 30):m.end()]))


def r_artigo(cfg, cap, linhas, paras, achados):
    """Sem artigo antes dos protagonistas em narração (em fala, pode)."""
    if cfg["convencoes"].get("artigo_antes_de_nome_em_narracao", False):
        return
    alvos = cfg["personagens"]["protagonistas"]
    rx = re.compile(r"\b([oOaA])\s+(%s)\b" % "|".join(alvos))
    for ini, texto in paras:
        if e_dialogo(texto) or texto.startswith("#"):
            continue
        for m in rx.finditer(texto):
            art, nome = m.group(1).lower(), m.group(2)
            concorda = (art == "o" and nome == "Josh") or \
                       (art == "a" and nome == "Aurora")
            if concorda:
                achados.append((ini, "artigo",
                                "…" + texto[max(0, m.start() - 30):m.end() + 20] + "…"))


def r_eco(cfg, cap, linhas, paras, achados):
    """Mesma palavra longa repetida 3+ vezes no mesmo parágrafo."""
    nomes = {n.lower() for n in cfg["personagens"]["protagonistas"]
             + cfg["personagens"]["elenco"]}
    for ini, texto in paras:
        palavras = [w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{7,}", texto)]
        palavras = [w for w in palavras
                    if w not in IGNORAR_ECO and w not in nomes]
        for palavra, n in Counter(palavras).items():
            if n >= 3:
                achados.append((ini, "eco", f"{palavra!r} ×{n} no parágrafo"))


REGRAS = {
    "template": r_template,
    "wrap": r_wrap,
    "interrogacao": r_interrogacao,
    "interrogacao-ambigua": r_interrogacao_ambigua,
    "travessao-narracao": r_travessao_narracao,
    "blacklist": r_blacklist,
    "formulas": r_formulas,
    "autorreferencia": r_autorreferencia,
    "sujeira": r_sujeira,
    "vocativo": r_vocativo,
    "artigo": r_artigo,
    "eco": r_eco,
}

# Regras que rodam por padrão. As de fora são caras de olhar (muito
# falso positivo) e só valem quando se está varrendo um capítulo fino.
REGRAS_PADRAO = [r for r in REGRAS if r not in {"interrogacao-ambigua"}]


# ──────────────────────────────────────────────────────────────  main ──

def analisar(caminho: str, cfg: dict, regras: list[str]):
    with open(caminho, encoding="utf-8") as fh:
        linhas = fh.readlines()
    paras = list(paragrafos(linhas))
    cap = num_capitulo(caminho)
    achados: list[tuple[int, str, str]] = []
    for nome in regras:
        REGRAS[nome](cfg, cap, linhas, paras, achados)
    achados.sort(key=lambda a: (a[0], a[1]))
    return achados


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivos", nargs="*")
    ap.add_argument("--projeto", default=None)
    ap.add_argument("--regra", action="append", choices=sorted(REGRAS))
    ap.add_argument("--resumo", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    ancora = args.projeto or (args.arquivos[0] if args.arquivos else ".")
    base = achar_projeto(ancora)
    with open(os.path.join(base, "livro.yaml"), encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    arquivos = args.arquivos or sorted(
        glob.glob(os.path.join(base, cfg["caminhos"]["capitulos"])))
    if not arquivos:
        sys.exit("Nenhum capítulo encontrado.")

    regras = args.regra or REGRAS_PADRAO
    total = 0
    tabela = []

    for caminho in arquivos:
        achados = analisar(caminho, cfg, regras)
        total += len(achados)
        rel = os.path.relpath(caminho, base)
        if args.resumo:
            tabela.append((rel, len(achados), Counter(a[1] for a in achados)))
            continue
        if not achados:
            continue
        print(f"\n{rel}  ({len(achados)} achados)")
        for linha, regra, detalhe in achados:
            print(f"  {linha:>5}  [{regra}] {detalhe}")

    if args.resumo and tabela:
        vistas = sorted({r for _, _, c in tabela for r in c})
        larg = max(len(t[0]) for t in tabela)
        cab = " ".join(f"{r[:8]:>8}" for r in vistas)
        print(f"{'capítulo':<{larg}} {'tot':>5}  {cab}")
        print("-" * (larg + 7 + len(cab)))
        for rel, n, por in tabela:
            cels = " ".join(f"{por.get(r, 0):>8}" for r in vistas)
            print(f"{rel:<{larg}} {n:>5}  {cels}")

    print(f"\n{total} achados em {len(arquivos)} arquivo(s).")
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    sys.exit(main())
