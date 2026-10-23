import re
OK = [r"[IVXLC]+:?", r"\d+[:,.;]?", r"[IVXL]+:\d+\*?", r"\(?\d{3,4}[-–—]\d{2,4}\)?[,.;]?",
      r"\$\d[\d,.]*", r"[\*†]?\d+\*?", r"\d{1,3}(,\d{3})+", r"Ma?c[A-Z][a-z]+[,.;]?"]

def strict(t):
    core = t.strip('.,;:!?"\'()[]{}“”‘’-—*♦†‡§')
    if not core:
        return False
    if any(re.fullmatch(p, core) for p in OK) or any(re.fullmatch(p, t) for p in OK):
        return False
    return bool(re.search(r"[^A-Za-z'’\-]", core)) or bool(re.search(r"[a-z][A-Z]", core))

def noise(t):
    """a token made only of the marks OCR makes from ornaments and pictures
    (carets, slashes, bullets, blocks); real punctuation is never touched"""
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
    return u
