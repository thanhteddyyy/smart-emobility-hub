from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Tong_hop_Methods_Test_Case.md"
OUTPUT = ROOT / "methods_testcases.tex"


def escape_latex(text):
    replacements = {
        "\\\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "|": r"\textbar{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def render_inline(text):
    text = text.strip()
    text = re.sub(r"^(?:<br\s*/?>\s*)+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(?:\s*<br\s*/?>)+$", "", text, flags=re.IGNORECASE)
    parts = re.split(r"(<br\s*/?>)", text, flags=re.IGNORECASE)
    rendered = []
    for part in parts:
        if re.fullmatch(r"<br\s*/?>", part, flags=re.IGNORECASE):
            rendered.append(r"\newline ")
            continue
        cursor = 0
        for match in re.finditer(r"(\*\*.*?\*\*|`.*?`)", part):
            rendered.append(escape_latex(part[cursor:match.start()]))
            token = match.group(0)
            if token.startswith("**"):
                rendered.append(r"\textbf{" + escape_latex(token[2:-2]) + "}")
            else:
                rendered.append(r"\texttt{" + escape_latex(token[1:-1]) + "}")
            cursor = match.end()
        rendered.append(escape_latex(part[cursor:]))
    return "".join(rendered).strip()


def clean_heading(text, level):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = text.replace("_", "").strip()
    if level == 1:
        if text.startswith("I."):
            return "Đặc tả phương thức (Methods Description)"
        if text.startswith("II."):
            return "Kịch bản kiểm thử (Test Cases)"
    return re.sub(r"^\d+(?:\.\d+)+\.\s*", "", text)


def split_row(line):
    cells = line.strip().strip("|").split("|")
    if len(cells) == 1:
        return ["", cells[0]]
    if len(cells) > 2:
        cells = [cells[0], r"\textbar{}".join(cells[1:])]
    return cells


def is_separator(line):
    return all(
        re.fullmatch(r"\s*:?-+:?\s*", cell)
        for cell in split_row(line)
    )


def render_table(rows):
    data_rows = [row for row in rows if not is_separator(row)]
    if not data_rows:
        return []

    normalized = []
    for row in data_rows:
        cells = split_row(row)
        if len(cells) < 2:
            cells.append("")
        normalized.append([render_inline(cells[0]), render_inline(cells[1])])

    output = [
        r"\begin{longtable}{|L{0.24\textwidth}|L{0.70\textwidth}|}",
        r"\hline",
        f"{normalized[0][0]} & {normalized[0][1]} \\\\",
        r"\hline",
        r"\endfirsthead",
        r"\hline",
        f"{normalized[0][0]} & {normalized[0][1]} \\\\",
        r"\hline",
        r"\endhead",
    ]
    for left, right in normalized[1:]:
        output.append(f"{left} & {right} \\\\")
        output.append(r"\hline")
    output.extend([r"\end{longtable}", r"\vspace{-0.5\baselineskip}"])
    return output


def convert(markdown):
    lines = markdown.splitlines()
    output = [r"\small", r"\renewcommand{\arraystretch}{1.12}"]
    index = 0
    while index < len(lines):
        line = lines[index]
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            title = escape_latex(clean_heading(heading.group(2), level))
            command = {1: "section", 2: "subsection", 3: "subsubsection"}[level]
            output.append(f"\\{command}{{{title}}}")
            index += 1
            continue
        if (
            line.strip().startswith("|")
            and index + 1 < len(lines)
            and is_separator(lines[index + 1])
        ):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(lines[index])
                index += 1
            output.extend(render_table(rows))
            continue
        index += 1
    output.append(r"\normalsize")
    return "\n".join(output) + "\n"


OUTPUT.write_text(convert(SOURCE.read_text(encoding="utf-8")), encoding="utf-8")