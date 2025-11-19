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
      "args": ["run", "/path/to/resume-creator/main.py"]
    }
  }
}
```

#### Claude Desktop の再起動

設定ファイルを保存して Claude Desktop を再起動すると、「resume-creator」ツールが利用可能になります。

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

## VSCode での設定

### 1. VSCode 拡張機能の推奨設定

`.vscode/settings.json` をプロジェクトに作成して、以下を追加します:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python"
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/*.egg-info": true
  }
}
```

### 2. VSCode でのデバッグ設定

`.vscode/launch.json` を作成してデバッグ設定を追加:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "MCP Server",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true,
      "justMyCode": true,
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
```

デバッグを開始: `F5` キーを押すか、実行メニューから「デバッグの開始」を選択

### 3. VSCode で uv の仮想環境を使用

VSCode が `uv` で作成した仮想環境を自動認識するようにするには:

1. VSCode をプロジェクトディレクトリで開く
2. Python インタープリターを選択: `Cmd + Shift + P` → "Python: Select Interpreter"
3. `.venv/bin/python` (uv が作成した環境) を選択

## よく使うコマンド

```bash
# 依存関係を同期（環境構築）
uv sync

# サーバーを起動
uv run python main.py

# Python スクリプトを実行
uv run python <script.py>

# 新しい依存関係を追加
uv add <package-name>

# 開発用依存関係を追加
uv add --dev <package-name>

# 依存関係をロック
uv lock

# 仮想環境のクリア
uv venv --clear
```

## トラブルシューティング

### MCP サーバーが起動しない

```bash
# 依存関係を確認・再構築
uv sync

# Python バージョン確認
python --version  # 3.13+ であることを確認

# サーバーを手動実行してエラーを確認
uv run python main.py
```

### Claude Desktop でサーバーが認識されない

1. `claude_desktop_config.json` のパスが正しいか確認
2. `uv run python` コマンドが実行可能か確認:
   ```bash
   uv run python --version
   ```
3. JSON の文法が正しいか確認（オンライン JSON バリデータで検証）
4. Claude Desktop を完全に再起動

### PDF 生成エラー

- 日本語文字列が正しくエンコードされているか確認
- ファイルパスに日本語が含まれていないか確認
- ReportLab がインストールされているか確認:
  ```bash
  uv run python -c "import reportlab; print(reportlab.__version__)"
  ```

## ライセンス

MIT License

## 参考資料

- [Model Context Protocol (MCP) ドキュメント](https://modelcontextprotocol.io)
- [uv ドキュメント](https://docs.astral.sh/uv/)
- [ReportLab ドキュメント](https://www.reportlab.com/docs/reportlab-userguide.pdf)
