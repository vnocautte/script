import os
import sys
import time
import random
import shutil
import math

# ══════════════════════════════════════════
#   МЕНЯЙ ТОЛЬКО ЭТУ СТРОКУ:
TEXT = "VNOCAUTTE"
# ══════════════════════════════════════════

CHARS = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789"

# Шрифт 5 строк высотой — крупный, читабельный
FONT = {
    'A': ["  █  ","  █  "," █ █ ","█████","█   █"],
    'B': ["████ ","█   █","████ ","█   █","████ "],
    'C': [" ████","█    ","█    ","█    "," ████"],
    'D': ["████ ","█   █","█   █","█   █","████ "],
    'E': ["█████","█    ","████ ","█    ","█████"],
    'F': ["█████","█    ","████ ","█    ","█    "],
    'G': [" ████","█    ","█  ██","█   █"," ████"],
    'H': ["█   █","█   █","█████","█   █","█   █"],
    'I': ["█████","  █  ","  █  ","  █  ","█████"],
    'J': ["█████","   █ ","   █ ","█  █ "," ██  "],
    'K': ["█   █","█  █ ","███  ","█  █ ","█   █"],
    'L': ["█    ","█    ","█    ","█    ","█████"],
    'M': ["█   █","██ ██","█ █ █","█   █","█   █"],
    'N': ["█   █","██  █","█ █ █","█  ██","█   █"],
    'O': [" ███ ","█   █","█   █","█   █"," ███ "],
    'P': ["████ ","█   █","████ ","█    ","█    "],
    'Q': [" ███ ","█   █","█ █ █","█  ██"," ████"],
    'R': ["████ ","█   █","████ ","█  █ ","█   █"],
    'S': [" ████","█    "," ███ ","    █","████ "],
    'T': ["█████","  █  ","  █  ","  █  ","  █  "],
    'U': ["█   █","█   █","█   █","█   █"," ███ "],
    'V': ["█   █","█   █"," █ █ "," █ █ ","  █  "],
    'W': ["█   █","█   █","█ █ █","██ ██","█   █"],
    'X': ["█   █"," █ █ ","  █  "," █ █ ","█   █"],
    'Y': ["█   █"," █ █ ","  █  ","  █  ","  █  "],
    'Z': ["█████","   █ ","  █  "," █   ","█████"],
    ' ': ["     ","     ","     ","     ","     "],
}

def build_text_mask(text, term_w, term_h):
    text = text.upper()
    # ── ИЗМЕНЕНИЕ 2: было rows=["","",""] и range(3), стало 5 строк ──
    rows = ["", "", "", "", ""]
    for ch in text:
        glyph = FONT.get(ch, FONT[' '])
        for i in range(5):
            rows[i] += glyph[i] + " "
    # ─────────────────────────────────────────────────────────────────
    art_w = max(len(r) for r in rows)
    start_col = max(0, (term_w - art_w) // 2)
    start_row = max(0, (term_h - 5) // 2)
    mask = {}
    for row_idx, row in enumerate(rows):
        for col_idx, ch in enumerate(row):
            if ch == '█':
                r = start_row + row_idx
                c = start_col + col_idx
                if 0 <= r < term_h and 0 <= c < term_w:
                    mask[(r, c)] = random.choice(CHARS)
    return mask

def color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

BOLD = "\033[1m"
RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR = "\033[2J\033[H"

def move(r, c):
    return f"\033[{r+1};{c+1}H"

def main():
    os.system("")
    sys.stdout.write(HIDE_CURSOR + CLEAR)
    sys.stdout.flush()

    try:
        term_w, term_h = shutil.get_terminal_size((80, 24))
        drops = [random.randint(-term_h, 0) for _ in range(term_w)]
        speeds = [random.randint(1, 3) for _ in range(term_w)]
        grid = [[' '] * term_w for _ in range(term_h)]
        age  = [[0] * term_w for _ in range(term_h)]
        drop_flash = {}
        mask = build_text_mask(TEXT, term_w, term_h)
        text_chars = {pos: random.choice(CHARS) for pos in mask}
        text_timer = {pos: random.randint(5, 20) for pos in mask}
        frame = 0

        while True:
            term_w2, term_h2 = shutil.get_terminal_size((80, 24))
            if term_w2 != term_w or term_h2 != term_h:
                term_w, term_h = term_w2, term_h2
                drops = [random.randint(-term_h, 0) for _ in range(term_w)]
                speeds = [random.randint(1, 3) for _ in range(term_w)]
                grid = [[' '] * term_w for _ in range(term_h)]
                age  = [[0] * term_w for _ in range(term_h)]
                drop_flash = {}
                mask = build_text_mask(TEXT, term_w, term_h)
                text_chars = {pos: random.choice(CHARS) for pos in mask}
                text_timer = {pos: random.randint(5, 20) for pos in mask}

            # Дыхание надписи
            pulse = 0.6 + 0.4 * math.sin(frame * 0.05)
            text_g = int(160 + 95 * pulse)

            # Мерцание символов надписи
            for pos in mask:
                text_timer[pos] -= 1
                if text_timer[pos] <= 0:
                    text_chars[pos] = random.choice(CHARS)
                    text_timer[pos] = random.randint(8, 30)

            out = []
            for c in range(min(term_w, len(drops))):
                if frame % max(1, speeds[c]) != 0:
                    continue
                drop_r = drops[c]

                for r in range(term_h):
                    if age[r][c] > 0:
                        age[r][c] += 1

                if 0 <= drop_r < term_h:
                    grid[drop_r][c] = random.choice(CHARS)
                    age[drop_r][c] = 1
                    if (drop_r, c) in mask:
                        drop_flash[(drop_r, c)] = 6

                for r in range(term_h):
                    ch = grid[r][c]
                    a = age[r][c]
                    pos = (r, c)
                    in_mask = pos in mask

                    if in_mask:
                        flash = drop_flash.get(pos, 0)
                        if flash > 0:
                            drop_flash[pos] = flash - 1
                            out.append(move(r, c) + color(200, 255, 200) + ch)
                        else:
                            out.append(move(r, c) + BOLD + color(0, text_g, 30) + text_chars[pos])
                    else:
                        if a == 0:
                            continue
                        elif a == 1:
                            out.append(move(r, c) + color(100, 200, 100) + ch)
                        elif a < 5:
                            out.append(move(r, c) + color(0, 100, 15) + ch)
                        elif a < 10:
                            out.append(move(r, c) + color(0, 50, 8) + ch)
                        elif a < 16:
                            out.append(move(r, c) + color(0, 20, 3) + ch)
                        else:
                            out.append(move(r, c) + color(0, 0, 0) + ' ')
                            grid[r][c] = ' '
                            age[r][c] = 0

                drops[c] += 1
                if drops[c] > term_h + random.randint(5, 20):
                    drops[c] = random.randint(-term_h, -5)
                    speeds[c] = random.randint(1, 3)

            sys.stdout.write(''.join(out) + RESET)
            sys.stdout.flush()
            frame += 1
            time.sleep(0.04)

    except KeyboardInterrupt:
        sys.stdout.write(SHOW_CURSOR + CLEAR + RESET)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
