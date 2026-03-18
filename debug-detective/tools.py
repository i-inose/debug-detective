import json
from strands import tool


@tool
def analyze_stacktrace(error_log: str) -> str:
    """エラーログからスタックトレースを解析し、構造化された捜査資料を作成します。

    Args:
        error_log: 分析対象のエラーログ
    """
    lines = error_log.strip().split("\n")

    # エラータイプの抽出
    error_type = "不明"
    error_message = "不明"
    file_locations = []

    for line in lines:
        # Python系エラー
        if "Error:" in line or "Exception:" in line:
            parts = line.split(":", 1)
            error_type = parts[0].strip().split(".")[-1]
            error_message = parts[1].strip() if len(parts) > 1 else ""
        # ファイル位置の抽出
        if 'File "' in line:
            file_locations.append(line.strip())
        # JavaScript系エラー
        if "at " in line and ("/" in line or "\\" in line):
            file_locations.append(line.strip())

    # 捜査資料の組み立て
    report = "【鑑識報告書】\n"
    report += f"エラータイプ（凶器）: {error_type}\n"
    report += f"エラーメッセージ（犯行声明）: {error_message}\n"
    report += f"関連ファイル数（現場数）: {len(file_locations)}箇所\n"

    if file_locations:
        report += "\n【現場一覧】\n"
        for i, loc in enumerate(file_locations, 1):
            report += f"  現場{i}: {loc}\n"

    report += f"\n総行数: {len(lines)}行の証拠を確認済み"
    return report


@tool
def search_error(error_type: str) -> str:
    """よくあるエラーパターンのデータベースを検索し、過去の捜査記録を返します。

    Args:
        error_type: 検索するエラーの種類（例: TypeError, ImportError）
    """
    # 過去の「事件簿」
    case_files = {
        "TypeError": {
            "common_causes": [
                "Noneに対してメソッドを呼び出している",
                "文字列と数値を混ぜて演算している",
                "関数の引数の数が合っていない",
            ],
            "severity": "中程度 -- 初犯が多い",
            "tip": "型を意識したコーディングを心がけろ。TypeScriptなら未然に防げた事件だ",
        },
        "ImportError": {
            "common_causes": [
                "パッケージがインストールされていない",
                "仮想環境が有効化されていない",
                "モジュール名のタイポ",
            ],
            "severity": "軽微 -- よくある迷子事件",
            "tip": "requirements.txt を整備しておけ。証拠隠滅（環境の再現不能）を防げる",
        },
        "KeyError": {
            "common_causes": [
                "辞書に存在しないキーでアクセスしている",
                "JSONレスポンスの構造が想定と違う",
                "環境変数が設定されていない",
            ],
            "severity": "中程度 -- 思い込み捜査の典型",
            "tip": ".get() メソッドを使え。存在確認なしにドアを蹴破るな",
        },
        "ConnectionError": {
            "common_causes": [
                "APIエンドポイントのURLが間違っている",
                "ネットワークに接続されていない",
                "対象サーバーがダウンしている",
            ],
            "severity": "状況次第 -- 現場に到達できない系",
            "tip": "リトライ処理とタイムアウト設定は捜査の基本装備だ",
        },
        "AttributeError": {
            "common_causes": [
                "Noneオブジェクトのメソッドを呼び出している",
                "クラスに存在しない属性にアクセスしている",
                "変数名のタイポ",
            ],
            "severity": "中程度 -- 人違い事件",
            "tip": "hasattr() で事前確認するか、Optional型を意識しろ",
        },
        "IndexError": {
            "common_causes": [
                "空のリストにアクセスしている",
                "ループのインデックスが範囲外",
                "オフバイワンエラー",
            ],
            "severity": "軽微 -- 数え間違い事件",
            "tip": "len() で長さを確認してからアクセスしろ。基本中の基本だ",
        },
    }

    # 部分一致で検索
    for key, case in case_files.items():
        if key.lower() in error_type.lower():
            report = f"【過去の事件簿】{key}\n"
            report += f"危険度: {case['severity']}\n"
            report += "よくある原因（常習犯リスト）:\n"
            for i, cause in enumerate(case["common_causes"], 1):
                report += f"  容疑者{i}: {cause}\n"
            report += f"\nベテランの教訓: {case['tip']}"
            return report

    return f"【事件簿】{error_type} に一致する過去の捜査記録はない。初めての事件かもしれないな..."