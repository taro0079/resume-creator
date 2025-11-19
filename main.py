import os
from pathlib import Path
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# PDF生成ライブラリ
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  # ここが重要
from reportlab.lib.units import mm

mcp = FastMCP("Japanese Resume Generator")

# --- フォント設定 (ダウンロード不要版) ---
FONT_NAME = "HeiseiKakuGo-W5"  # PDF標準の日本語ゴシック体
pdfmetrics.registerFont(UnicodeCIDFont(FONT_NAME))


@mcp.tool()
def generate_resume_pdf(
    name: str,
    kana: str,
    gender: str,
    birth_date: str,
    address: str,
    phone: str,
    email: str,
    education_work_history: list[str],
    motivation: str,
    output_filename: str = "resume.pdf",
) -> str:
    """
    日本の履歴書(JIS規格風)のPDFを生成します。
    フォントのダウンロードは行わず、PDF標準フォントを使用します。
    """

    # PDFの設定
    c = canvas.Canvas(output_filename, pagesize=A4)

    # --- 描画用ヘルパー関数 ---
    def draw_rect(x, y, w, h):
        c.setLineWidth(1)
        c.rect(x * mm, y * mm, w * mm, h * mm)

    # テキスト描画ヘルパー。baseline調整でより正確に配置
    def draw_text(x, y, text, size=10, align="left", baseline_offset_factor=0.3):
        c.setFont(FONT_NAME, size)
        # フォントサイズに基づいてベースラインを調整
        # ReportLabのdrawStringは文字列の左下を基準にするため、中央寄せや行内の中央にしたい場合は調整が必要
        adjusted_y = y * mm - (size * baseline_offset_factor)

        if align == "center":
            c.drawCentredString(x * mm, adjusted_y, text)
        elif align == "right":
            c.drawRightString(x * mm, adjusted_y, text)
        else:
            c.drawString(x * mm, adjusted_y, text)

    # タイトル
    draw_text(105, 280, "履 歴 書", 18, align="center", baseline_offset_factor=0.35)
    current_date = datetime.now().strftime("%Y年 %m月 %d日 現在")
    draw_text(195, 280, current_date, 10, align="right")

    # 1. 基本情報エリア
    top_y = 270

    # 写真枠
    draw_rect(155, top_y - 40, 30, 40)
    # 写真枠内のテキストを中央揃えに調整
    draw_text(170, top_y - 18, "写真を貼る位置", 8, align="center")
    draw_text(170, top_y - 23, "(縦40mm 横30mm)", 6, align="center")

    # 氏名枠
    draw_rect(15, top_y - 25, 130, 25)
    # ふりがなのラベルとデータ
    draw_text(20, top_y - 6, "ふりがな", 6)  # ラベルは少し左寄りに
    draw_text(40, top_y - 6, kana, 10)  # データは適切な位置に
    # 氏名のラベルとデータ
    draw_text(20, top_y - 18, "氏 名", 8)  # ラベルは少し左寄りに
    draw_text(40, top_y - 20, name, 16)  # データは大きなフォントで適切に配置

    # 生年月日・性別
    draw_rect(15, top_y - 35, 130, 10)
    draw_text(20, top_y - 32, "生年月日", 8)  # ラベルは左寄せ
    draw_text(45, top_y - 32, f"{birth_date}生", 10)
    draw_text(100, top_y - 32, "性別", 8)  # ラベルは中央寄りに
    draw_text(120, top_y - 32, gender, 10)  # データは適切な位置に

    # 住所・連絡先
    current_y = top_y - 35
    draw_rect(15, current_y - 20, 170, 15)  # 住所枠
    draw_text(20, current_y - 10, "現住所", 8)  # ラベルは左寄せ
    draw_text(40, current_y - 12, address, 10)

    draw_rect(15, current_y - 30, 170, 10)  # 電話・Email
    draw_text(20, current_y - 27, "電話", 8)  # ラベルは左寄せ
    draw_text(40, current_y - 27, phone, 10)
    draw_text(85, current_y - 27, "E-mail", 8)  # ラベルは電話データと被らない位置に
    draw_text(105, current_y - 27, email, 10)

    # 2. 学歴・職歴エリア
    history_top_y = current_y - 35
    draw_text(105, history_top_y + 2, "学歴・職歴", 10, align="center")

    # テーブルヘッダー
    header_y = history_top_y
    row_height = 7
    draw_rect(15, header_y - row_height, 20, row_height)
    draw_text(25, header_y - 5, "年", 8, align="center")  # 中央寄せ
    draw_rect(35, header_y - row_height, 10, row_height)
    draw_text(40, header_y - 5, "月", 8, align="center")  # 中央寄せ
    draw_rect(45, header_y - row_height, 140, row_height)
    draw_text(115, header_y - 5, "学歴・職歴", 8, align="center")  # 中央寄せ

    # 履歴の行を描画
    current_row_y = header_y - row_height
    max_rows = 18

    for i in range(max_rows):
        draw_rect(15, current_row_y - row_height, 20, row_height)  # 年
        draw_rect(35, current_row_y - row_height, 10, row_height)  # 月
        draw_rect(45, current_row_y - row_height, 140, row_height)  # 内容

        if i < len(education_work_history):
            content = education_work_history[i]
            parts = content.split(" ", 2)
            if len(parts) == 3:
                draw_text(
                    25, current_row_y - 5, parts[0], align="center"
                )  # 年は中央寄せ
                draw_text(
                    40, current_row_y - 5, parts[1], align="center"
                )  # 月は中央寄せ
                draw_text(48, current_row_y - 5, parts[2])  # 内容は左寄せ
            else:
                draw_text(48, current_row_y - 5, content)

        current_row_y -= row_height

    # 3. 志望動機エリア
    motivation_y = current_row_y - 10
    box_height = 35
    draw_rect(15, motivation_y - box_height, 170, box_height)
    draw_text(18, motivation_y - 5, "志望動機・特技・アピールポイントなど", 8)

    # 志望動機のテキスト折り返し処理
    # ReportLabのtextobjectの基準座標は行の開始位置、drawStringとは異なる
    text_obj = c.beginText(18 * mm, (motivation_y - 10 - 0.5) * mm)  # 微調整
    text_obj.setFont(FONT_NAME, 8)

    char_limit = 50
    lines = []
    current_line = ""
    for char in motivation:
        current_line += char
        if len(current_line) >= char_limit or char == "\n":
            lines.append(current_line)
            current_line = ""
    if current_line:
        lines.append(current_line)

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)

    # ファイル保存
    try:
        c.save()
        abs_path = str(Path(output_filename).resolve())
        return f"履歴書PDFを生成しました。\n保存先: {abs_path}"
    except Exception as e:
        return f"PDFの保存中にエラーが発生しました: {e}"


if __name__ == "__main__":
    mcp.run()
