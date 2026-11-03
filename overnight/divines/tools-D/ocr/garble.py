import re
OK = [r"[IVXLC]+:?", r"\d+[:,.;]?", r"[IVXL]+:\d+\*?", r"\(?\d{3,4}[-–—]\d{2,4}\)?[,.;]?",
      r"\$\d[\d,.]*", r"[\*†]?\d+\*?", r"\d{1,3}(,\d{3})+", r"Ma?c[A-Z][a-z]+[,.;]?", r"\d+(st|nd|rd|th|d)", r"&c?\.?", r"£\d[\d,.]*", r"£", r"\d{1,2}[-–]\d{1,2}", r"\d+mo", r"([A-Z]\.){2,}"]

def strict(t):
    core = t.strip('.,;:!?"\'()[]{}“”‘’-—*♦†‡§')
    if not core:
        return False
    if any(re.fullmatch(p, core) for p in OK) or any(re.fullmatch(p, t) for p in OK):
        return False
    return bool(re.search(r"[^A-Za-zÀ-ÖØ-öø-ÿŒœ\u0370-\u03FF\u1F00-\u1FFF'’\-]", core)) or bool(re.search(r"[a-z][A-Z]", core))

GOOGLE=r"(by)?[VG]?[jo]?[O0Q]{2}[gQ]l[eC]|Dgtze[cd]C?[yb]?|Di[gq]iti[sz]ed|//books|books\.google\.com/?|com/|.*(Dgtz|D,g,t|Di[gq]iti[sz]ed|[Gg]'?oo[gq][lI]e).*"
def noise(t):
    """a token made only of the marks OCR makes from ornaments and pictures
    (carets, slashes, bullets, blocks); real punctuation is never touched"""
    if re.fullmatch(GOOGLE, t): return True          # the "Digitized by Google" footer of Google scans
    return bool(re.fullmatch(r"[\^\\/•■♦»«<>|_~]+[.,'*\"-]*", t)) and "^" in t or bool(re.fullmatch(r"[\\/•■♦|_~]{1,3}", t))

def rulefix(t):
    u = re.sub(r"(?<=[A-Za-z])[\*\^]s\b", "’s", t)        # Barnum*s, Barnum^s -> Barnum’s
    u = re.sub(r"^tl(?=\d)", "†1", u)
    u = re.sub(r"^t(?=\d)", "†", u)                        # index dagger marks
    if re.fullmatch(r"[\dio]{2,4}[,.;]?", u) and re.search(r"\d", u):
        u = u.replace("i", "1").replace("o", "0")           # i8 -> 18, 6o -> 60 (old-style figures)
    u = re.sub(r"^\^+(?=[A-Za-z\d'‘“])", "", u)             # stray caret before a word
    u = re.sub(r"(?<=[A-Za-z])\^+$", "", u)                 # stray caret after a word
    u = re.sub(r"(?<=[A-Za-z])\^(?=[a-z])", "", u)          # im^mediate -> immediate
    u = re.sub(r"(?<=[a-z.!?,])/\*$", "”", u)               # village/* -> village”
    u=re.sub(r"^[■•▼]+(?=[A-Za-z])", "", u)                # ■was -> was
    u=re.sub(r"^iE(?=[a-z])", "Æ", u)                       # iEschylus -> Æschylus
    if re.fullmatch(r"\d[\dGS]*[GS][\dGS]*[.,;:)]?|[GS]\d+[.,;:)]?", u) and sum(ch.isdigit() for ch in u)>=1 and len(u.rstrip('.,;:)'))>=2:
        u = u.replace("G","6").replace("S","8")              # 1G7 -> 167, 7S -> 78
    u=re.sub(r"(?<=[A-Za-z])¬$", "-", u)                    # this OCR's sign for a line-end hyphen
    if re.fullmatch(r"[1l][7-9S][\dSOo]{2}[.,;:)]?", u) and re.search(r"[SOol]", u):
        u = u[0].replace("l","1") + u[1:].replace("S","8").replace("O","0").replace("o","0")   # 1S68 -> 1868
    return u
