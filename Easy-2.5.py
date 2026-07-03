import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import random
import string
import os

# メモリと状態の管理
variables = {}
items = []  # 所持アイテムリスト
output_widget = None
SAVE_FILE_NAME = "my_code.txt"  # コードを保存するファイル名
current_theme = "dark"  # 初期設定はダークモード

# ハイライト対象のキーワードリスト
KEYWORDS = [
    "計算", "calc", "HP", "hp", "得点", "score", "音楽", "bgm", "音楽停止", "bgm_stop",
    "もし", "if", "それとも", "elif", "その他", "else", "終わり", "endif",
    "AI", "ai", "チャット", "chat", "ランダム", "random", "カウントダウン", "countdown",
    "表示", "print", "待つ", "wait", "警告", "alert", "アニメ", "type", "消去", "clear",
    "音", "beep", "アプリ終了", "close", "アイテム", "item", "名前入力", "input_name", "効果音", "se"
]

# --- 多言語メッセージの設定 ---
LANG_TEXTS = {
    "日本語": {
        "title": "コードエディタ", 
        "label": "", 
        "btn": "▶ 実行する", 
        "output": "ログ:",
        "btn_save": "保存",
        "btn_load": "読込",
        "btn_close": "❌ 終了",
        "sample": "名前入力 プレイヤー名\nチャット ナビゲーター プレイヤー名 を登録しました。\n\n計算 得点 = 0\n得点 得点\n\nアイテム 伝説の剣\n効果音 1\n\n表示 運試しをします！\nランダム 補正値 30 80\n計算 得点 = 得点 + 補正値\n得点 得点\n\nカウントダウン 3\n表示 ゲームクリア！"
    },
    "English": {
        "title": "Code Editor", 
        "label": "", 
        "btn": "▶ RUN", 
        "output": "Log:",
        "btn_save": "Save",
        "btn_load": "Load",
        "btn_close": "❌ CLOSE",
        "sample": "input_name player_name\nchat Navigator Registered player_name.\n\ncalc score = 0\nscore score\n\nitem Excalibur\nse 1\n\nprint Roll the dice!\nrandom bonus 30 80\ncalc score = score + bonus\nscore score\n\ncountdown 3\nprint Game Clear!"
    }
}

# --- 画面（GUI）の構築 ---
root = tk.Tk()
root.title("Code Editor")
root.geometry("440x700")
APP_FONT = ("Helvetica", 11)

# テーマカラー定義（視認性を向上）
THEMES = {
    "dark": {
        "bg": "#1e1e1e", "fg": "#ffffff", "editor_bg": "#2d2d2d", "editor_fg": "#ffffff",
        "log_bg": "#2d2d2d", "log_fg": "#eceff1", "keyword": "#69f0ae", "frame_fg": "#90caf9",
        "btn_text": "[ L ]"  # 次はLightモードにするという意味
    },
    "light": {
        "bg": "#f5f5f5", "fg": "#000000", "editor_bg": "#ffffff", "editor_fg": "#000000",
        "log_bg": "#ffffff", "log_fg": "#333333", "keyword": "#0d47a1", "frame_fg": "#1565c0",
        "btn_text": "[ D ]"  # 次はDarkモードにするという意味
    }
}

style = ttk.Style()
style.theme_use("default")

# --- UIパーツ配置 ---
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=5)

lang_combo = ttk.Combobox(frame_top, values=list(LANG_TEXTS.keys()), state="readonly", width=8, font=APP_FONT)
lang_combo.set("日本語")
lang_combo.pack(side="left")

# 文字化けしないテキストボタンに変更
btn_theme = tk.Button(frame_top, text="[ L ]", font=("Helvetica", 9, "bold"), bd=1, padx=5)
btn_theme.pack(side="left", padx=5)

btn_save_file = tk.Button(frame_top, text="", font=("Helvetica", 9), bd=0, padx=8, pady=2)
btn_save_file.pack(side="left", padx=5)

btn_load_file = tk.Button(frame_top, text="", font=("Helvetica", 9), bd=0, padx=8, pady=2)
btn_load_file.pack(side="left", padx=5)

frame_game_ui = tk.LabelFrame(root, font=("Helvetica", 9, "bold"), bd=1)
frame_game_ui.pack(fill="x", padx=10, pady=5)

label_hp_title = tk.Label(frame_game_ui, text="HP:", font=("Helvetica", 10, "bold"))
label_hp_title.pack(side="left", padx=(5, 2))

progress_hp = ttk.Progressbar(frame_game_ui, orient="horizontal", length=150, mode="determinate")
progress_hp.pack(side="left", padx=5, pady=5)
progress_hp["value"] = 100

label_score = tk.Label(frame_game_ui, text="SCORE: 0", font=("Helvetica", 11, "bold"))
label_score.pack(side="right", padx=10)

label_code = tk.Label(root, text="", anchor="w", font=APP_FONT)
label_code.pack(fill="x", padx=10, pady=(0, 2))

# エディタエリア
code_entry = tk.Text(root, height=12, font=APP_FONT, bd=1, relief="solid", undo=True)
code_entry.pack(fill="both", expand=True, padx=10, pady=2)

btn_run = tk.Button(root, text="", font=("Helvetica", 12, "bold"), bd=0)
btn_run.pack(fill="x", padx=10, pady=5)

label_out = tk.Label(root, text="", anchor="w", font=APP_FONT)
label_out.pack(fill="x", padx=10, pady=(5, 2))

# ログ表示エリア
output_widget = tk.Text(root, height=6, font=APP_FONT, state="disabled", bd=1, relief="solid")
output_widget.pack(fill="both", expand=True, padx=10, pady=(2, 10))

btn_close = tk.Button(root, text="", font=("Helvetica", 10), bd=0, padx=10)
btn_close.pack(side="right", padx=10, pady=(0, 10))


# --- リアルタイムカラーハイライトシステム ---
def highlight_keywords(event=None):
    code_entry.tag_remove("keyword", "1.0", tk.END)
    content = code_entry.get("1.0", tk.END).split("\n")
    for row, line in enumerate(content, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        first_word = stripped.split()[0]
        if first_word in KEYWORDS:
            start_idx = line.find(first_word)
            end_idx = start_idx + len(first_word)
            code_entry.tag_add("keyword", f"{row}.{start_idx}", f"{row}.{end_idx}")

code_entry.bind("<KeyRelease>", highlight_keywords)


# --- テーマ適用ロジック ---
def apply_theme():
    colors = THEMES[current_theme]
    root.configure(bg=colors["bg"])
    frame_top.configure(bg=colors["bg"])
    
    label_hp_title.configure(bg=colors["bg"], fg=colors["fg"])
    label_score.configure(bg=colors["bg"], fg="#ffb74d" if current_theme == "dark" else "#e65100")
    label_code.configure(bg=colors["bg"], fg=colors["fg"])
    label_out.configure(bg=colors["bg"], fg=colors["fg"])
    frame_game_ui.configure(bg=colors["bg"], fg=colors["frame_fg"], text=" STATUS ")
    
    # ボタンテキストを安全な文字に設定
    btn_theme.configure(text=colors["btn_text"], bg=colors["editor_bg"], fg=colors["fg"])
    btn_save_file.configure(bg="#37474f" if current_theme == "dark" else "#b0bec5", fg=colors["fg"])
    btn_load_file.configure(bg="#3e2723" if current_theme == "dark" else "#d7ccc8", fg=colors["fg"])
    btn_run.configure(bg="#2e7d32" if current_theme == "dark" else "#81c784", fg=colors["fg"])
    btn_close.configure(bg="#c62828" if current_theme == "dark" else "#ef9a9a", fg=colors["fg"])
    
    style.configure("TCombobox", fieldbackground=colors["editor_bg"], background=colors["bg"], foreground=colors["fg"])
    style.configure("Horizontal.TProgressbar", background="#4caf50", troughcolor=colors["editor_bg"])
    
    code_entry.configure(bg=colors["editor_bg"], fg=colors["editor_fg"], insertbackground=colors["fg"])
    output_widget.configure(bg=colors["log_bg"], fg=colors["log_fg"])
    
    code_entry.tag_configure("keyword", foreground=colors["keyword"], font=(APP_FONT[0], APP_FONT[1], "bold"))
    highlight_keywords()

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()

btn_theme.configure(command=toggle_theme)


# --- 言語解析・命令エンジン ---
def evaluate_expression(expr):
    expr = expr.strip()
    if expr in variables:
        return variables[expr]
    try:
        if "." in expr: return float(expr)
        return int(expr)
    except ValueError:
        return expr

def evaluate_condition(condition_str):
    operators = ["==", "!=", ">=", "<=", ">", "<"]
    for op in operators:
        if op in condition_str:
            left_str, right_str = condition_str.split(op, 1)
            left_val = evaluate_expression(left_str)
            right_val = evaluate_expression(right_str)
            try: left_val, right_val = float(left_val), float(right_val)
            except: left_val, right_val = str(left_val), str(right_val)
            if op == "==": return left_val == right_val
            if op == "!=": return left_val != right_val
            if op == ">=": return left_val >= right_val
            if op == "<=": return left_val <= right_val
            if op == ">": return left_val > right_val
            if op == "<": return left_val < right_val
    return False

def get_ai_response(user_text):
    text = user_text.lower().strip()
    if "こんにちは" in text or "hello" in text: return "[AI] こんにちは！何かお手伝いしましょうか？"
    elif "勝てる" in text or "win" in text: return f"[AI] 現在のスコアは {variables.get('得点', variables.get('score', 0))} です。いけます！"
    elif "アイテム" in text or "item" in text: return f"[AI] あなたは今、次のものを持ちきれるはずです: {', '.join(items) if items else 'なし'}"
    else: return random.choice(["[AI] 素晴らしいロジックです！", "[AI] そのまま進めましょう。", "[AI] 応援しています！"])

def run_my_language(code):
    global variables, items
    lines = code.split("\n")
    outputs = []
    if_stack = []

    for line in lines:
        line = line.strip()
        if not line: continue
            
        if line.startswith("もし ") or line.startswith("if "):
            _, cond_str = line.split(" ", 1)
            is_true = evaluate_condition(cond_str)
            parent_executing = if_stack[-1]["executing"] if if_stack else True
            current_exec = parent_executing and is_true
            if_stack.append({"executing": current_exec, "done": current_exec})
            continue
        if line.startswith("それとも ") or line.startswith("elif "):
            _, cond_str = line.split(" ", 1)
            if if_stack:
                parent_executing = if_stack[:-1][-1]["executing"] if len(if_stack) > 1 else True
                if parent_executing and not if_stack[-1]["done"]:
                    is_true = evaluate_condition(cond_str)
                    if_stack[-1]["executing"] = is_true
                    if is_true: if_stack[-1]["done"] = True
                else: if_stack[-1]["executing"] = False
            continue
        if line in ["その他", "else"]:
            if if_stack:
                parent_executing = if_stack[:-1][-1]["executing"] if len(if_stack) > 1 else True
                if parent_executing and not if_stack[-1]["done"]:
                    if_stack[-1]["executing"] = True
                    if_stack[-1]["done"] = True
                else: if_stack[-1]["executing"] = False
            continue
        if line in ["終わり", "endif"]:
            if if_stack: if_stack.pop()
            continue
        if if_stack and not if_stack[-1]["executing"]: continue

        # 名前入力
        if any(line.startswith(cmd + " ") for cmd in ["名前入力", "input_name"]):
            _, var_name = line.split(" ", 1)
            res_name = simpledialog.askstring("Input", "名前を入力してください / Enter Name:")
            variables[var_name.strip()] = res_name if res_name else "No Name"
            outputs.append(f"[INPUT] {var_name.strip()} = {variables[var_name.strip()]}")
            continue

        # アイテム追加
        if any(line.startswith(cmd + " ") for cmd in ["アイテム", "item"]):
            _, item_name = line.split(" ", 1)
            eval_item = str(evaluate_expression(item_name.strip()))
            items.append(eval_item)
            outputs.append(f"[ITEM] アイテムを獲得しました: {eval_item} (全所持: {', '.join(items)})")
            continue

        # 効果音
        if any(line.startswith(cmd + " ") for cmd in ["効果音", "se"]):
            _, type_str = line.split(" ", 1)
            se_type = int(evaluate_expression(type_str.strip()))
            if os.name == "nt":
                import winsound
                if se_type == 1: winsound.MessageBeep(winsound.MB_ICONASTERISK)
                elif se_type == 2: winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                else: winsound.MessageBeep(-1)
            outputs.append(f"[SE] Sound effect triggered: Type {se_type}")
            continue

        # AI・チャット・ランダム・カウントダウン・その他
        if any(line.startswith(cmd + " ") for cmd in ["AI", "ai"]):
            _, ai_msg = line.split(" ", 1)
            response = get_ai_response(str(evaluate_expression(ai_msg.strip())))
            outputs.append(f"__TYPE_EFFECT__:{response}")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["チャット", "chat"]):
            _, rest = line.split(" ", 1)
            parts = rest.strip().split(" ", 1)
            if len(parts) == 2:
                speaker, dialogue = parts
                speaker_val = str(evaluate_expression(speaker.strip()))
                dialogue_val = str(evaluate_expression(dialogue.strip()))
                outputs.append(f"__TYPE_EFFECT__:[{speaker_val}]: {dialogue_val}")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["ランダム", "random"]):
            _, rest = line.split(" ", 1)
            parts = rest.strip().split()
            if len(parts) == 3:
                var_name, min_str, max_str = parts
                v_min = int(evaluate_expression(min_str))
                v_max = int(evaluate_expression(max_str))
                rand_res = random.randint(v_min, v_max)
                variables[var_name.strip()] = rand_res
                outputs.append(f"[RANDOM] {var_name.strip()} = {rand_res}")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["カウントダウン", "countdown"]):
            _, sec_str = line.split(" ", 1)
            seconds = int(evaluate_expression(sec_str.strip()))
            for i in range(seconds, 0, -1): outputs.append(f"■ {i}...")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["HP", "hp"]):
            _, val_str = line.split(" ", 1)
            hp_val = int(evaluate_expression(val_str.strip()))
            hp_val = max(0, min(100, hp_val))
            progress_hp["value"] = hp_val
            root.update(); outputs.append(f"[GAME UI] HP updated to {hp_val}%")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["得点", "score"]):
            _, val_str = line.split(" ", 1)
            score_val = evaluate_expression(val_str.strip())
            label_score.config(text=f"SCORE: {score_val}")
            root.update(); outputs.append(f"[GAME UI] Score updated to {score_val}")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["計算", "calc"]):
            _, rest = line.split(" ", 1)
            var_name, expr_str = rest.split("=", 1)
            parsed_expr = expr_str.strip()
            for v_name, v_val in variables.items(): parsed_expr = parsed_expr.replace(v_name, str(v_val))
            try:
                if all(c in "0123456789+-*/(). " for c in parsed_expr):
                    calc_res = eval(parsed_expr)
                    variables[var_name.strip()] = calc_res
                    outputs.append(f"[CALC] {var_name.strip()} = {calc_res}")
            except: outputs.append("[CALC_ERROR] Failed")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["表示", "print"]):
            _, expr = line.split(" ", 1)
            outputs.append(str(evaluate_expression(expr.strip())))
            continue
        if any(line.startswith(cmd + " ") for cmd in ["待つ", "wait"]):
            time.sleep(float(evaluate_expression(line.split(" ", 1)[1].strip())))
            continue
        if any(line.startswith(cmd + " ") for cmd in ["警告", "alert"]):
            messagebox.showwarning("Alert", str(evaluate_expression(line.split(" ", 1)[1].strip())))
            continue
        if any(line.startswith(cmd + " ") for cmd in ["バイブ", "vibe"]):
            count = int(evaluate_expression(line.split(" ", 1)[1].strip()))
            orig_bg = output_widget.cget("bg")
            for _ in range(min(count, 10)):
                output_widget.config(bg="#d32f2f"); root.update(); time.sleep(0.06)
                output_widget.config(bg=orig_bg); root.update(); time.sleep(0.06)
            continue
        if line in ["消去", "clear"]: outputs = ["CLEAR_SIGNAL"]; continue
        if line in ["音", "beep"]: root.bell(); continue
        if line in ["アプリ終了", "close"]: root.destroy(); return "CLOSED"

    return outputs

# --- ボタン処理等各種イベント用 ---
def animate_text(target_widget, text_line, delay=0.03):
    for char in text_line:
        target_widget.insert(tk.END, char); target_widget.see(tk.END); target_widget.update(); time.sleep(delay)
    target_widget.insert(tk.END, "\n")

def press_run_code():
    global variables, items
    user_code = code_entry.get("1.0", tk.END)
    variables = {}
    items = []
    progress_hp["value"] = 100
    label_score.config(text="SCORE: 0")
    
    results = run_my_language(user_code)
    if results == "CLOSED": return
        
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)
    for res in results:
        if res.startswith("__TYPE_EFFECT__:"):
            animate_text(output_widget, res.replace("__TYPE_EFFECT__:", ""))
        else:
            output_widget.insert(tk.END, res + "\n")
    output_widget.see(tk.END)
    output_widget.config(state="disabled")

def press_save_file():
    try:
        with open(SAVE_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(code_entry.get("1.0", tk.END).strip())
        messagebox.showinfo("Success", "Saved!")
    except Exception as e: messagebox.showerror("Error", str(e))

def press_load_file():
    if not os.path.exists(SAVE_FILE_NAME): return
    try:
        with open(SAVE_FILE_NAME, "r", encoding="utf-8") as f: content = f.read()
        code_entry.delete("1.0", tk.END)
        code_entry.insert("1.0", content)
        highlight_keywords()
    except Exception as e: messagebox.showerror("Error", str(e))

def on_language_change(event=None):
    lang = lang_combo.get()
    text = LANG_TEXTS[lang]
    root.title(text["title"])
    label_code.config(text=text["label"])
    btn_run.config(text=text["btn"])
    label_out.config(text=text["output"])
    btn_save_file.config(text=text["btn_save"])
    btn_load_file.config(text=text["btn_load"])
    btn_close.config(text=text["btn_close"])
    code_entry.delete("1.0", tk.END)
    code_entry.insert("1.0", text["sample"])
    highlight_keywords()

btn_save_file.configure(command=press_save_file)
btn_load_file.configure(command=press_load_file)
btn_run.configure(command=press_run_code)
btn_close.configure(command=lambda: root.destroy())
lang_combo.bind("<<ComboboxSelected>>", on_language_change)

on_language_change()
apply_theme()
root.mainloop()
