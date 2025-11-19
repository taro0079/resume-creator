# 日本語履歴書生成 MCPサーバー

このプロジェクトは、Model Context Protocol (MCP) を使用した日本語履歴書(JIS標準)PDF生成サーバーです。Claude や他の MCP 互換クライアントから履歴書を生成できます。

## 概要

- **プロジェクト名**: resume-creator
- **Python バージョン**: 3.13+
- **パッケージマネージャー**: [uv](https://github.com/astral-sh/uv)
- **主な依存関係**: FastMCP, ReportLab
- **機能**: JSON形式の入力から JIS標準の日本語履歴書 PDF を生成

## セットアップ

### 1. 前提条件

- **uv** のインストール: https://docs.astral.sh/uv/getting-started/installation/
- **Python 3.13+**

### 2. プロジェクトのセットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd resume-creator

# 依存関係をインストールして仮想環境を構築
uv sync
```

### 3. MCPサーバーの実行

```bash
uv run python main.py
```

サーバーは MCP プロトコルで待ち受け状態になります。

## MCPサーバーの使い方

### Claude Desktop での設定

#### 設定ファイルの編集

Claude Desktop の設定ファイルを開きます:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### MCP サーバーを追加

以下の設定を `mcpServers` セクションに追加します。`/path/to/resume-creator` は実際のプロジェクトパスに置き換えてください:

```json
{
  "mcpServers": {
    "resume-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/resume-creator",
        "run",
        "main.py"
      ]
    }
  }
}
```

#### Claude Desktop の再起動

設定ファイルを保存して Claude Desktop を再起動すると、「resume-creator」ツールが利用可能になります。

### VS Code / Cursor での設定

#### 設定ファイルの編集

VS Code または Cursor で MCP サーバーを使用する場合は、`mcp.json` 設定ファイルを開きます:

**Cursor の場合:**
- **macOS**: `~/.cursor/mcp.json`
- **Windows**: `%APPDATA%\Cursor\mcp.json`
- **Linux**: `~/.config/Cursor/mcp.json`

**VS Code の場合:**
1. コマンドパレット(command + shift + p)から「MCP: ユーザ構成を開く」
2. 以下の内容を追加して保存

> **注意**: VS Code の場合は、使用している拡張機能によって設定ファイルの場所が異なる場合があります。MCP 対応の拡張機能のドキュメントを確認してください。

#### MCP サーバーを追加

`mcp.json` ファイルに以下の設定を追加します。`/path/to/resume-creator` は実際のプロジェクトパスに置き換えてください:

```json
{
  "mcpServers": {
    "resume-creator": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/resume-creator",
        "run",
        "main.py"
      ]
    }
  }
}
```

> **重要**: `type: "stdio"` を指定することで、標準入出力（stdio）経由でMCPサーバーと通信します。これがVSCode/Cursorでの標準的な設定方法です。

#### VS Code / Cursor の再起動

設定ファイルを保存して VS Code または Cursor を再起動すると、「resume-creator」ツールが利用可能になります。

### API リクエストの例

MCP サーバーは `generate_resume_pdf` というツールを公開しています。以下のペイロードで呼び出します:

```json
{
  "name": "山田 太郎",
  "kana": "やまだ たろう",
  "gender": "男",
  "birth_date": "1995年 5月 15日",
  "address": "東京都千代田区丸の内 1-1-1",
  "phone": "090-1234-5678",
  "email": "yamada@example.com",
  "education_work_history": [
    "2011 04 ○○高等学校 入学",
    "2014 03 ○○高等学校 卒業",
    "2014 04 △△大学 入学",
    "2018 03 △△大学 卒業",
    "2018 04 株式会社□□ 入社",
    "2023 12 株式会社□□ 退社"
  ],
  "motivation": "私の強みは継続的な学習意欲です。貴社の技術力に魅力を感じ、自身のスキルを活かして貢献したいと考えております。",
  "output_filename": "resume.pdf"
}
```

### パラメータの説明

| パラメータ | 型 | 説明 | 必須 |
|-----------|-----|------|------|
| `name` | string | 氏名 | ✓ |
| `kana` | string | 氏名のふりがな(カタカナ) | ✓ |
| `gender` | string | 性別(男/女) | ✓ |
| `birth_date` | string | 生年月日(例: 1995年 5月 15日) | ✓ |
| `address` | string | 現住所 | ✓ |
| `phone` | string | 電話番号 | ✓ |
| `email` | string | メールアドレス | ✓ |
| `education_work_history` | array | 学歴・職歴のリスト(形式: "YYYY MM 説明") | ✓ |
| `motivation` | string | 志望動機・自己PR | ✓ |
| `output_filename` | string | 出力ファイル名(デフォルト: resume.pdf) | ✗ |

