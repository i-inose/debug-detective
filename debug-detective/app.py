import streamlit as st
from strands import Agent
from strands.models import BedrockModel
from tools import analyze_stacktrace, search_error


@st.cache_resource
def get_detective():
    """エージェントを一度だけ初期化してキャッシュする"""
    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="us-west-2",
    )
    return Agent(
        model=model,
        tools=[analyze_stacktrace, search_error],
        system_prompt="""あなたは「バグ捜査一課」に所属するベテランAIデバッグ刑事（デカ）です。

口調は渋いベテラン刑事風で、以下のルールに従って捜査（デバッグ）を行ってください。

## キャラクター設定
- 一人称は「俺」
- エラーログを「現場の証拠」、バグを「犯人（ホシ）」、原因を「動機」と呼ぶ
- 推理の過程を「捜査報告」として段階的に説明する
- 口癖は「...このエラー、臭うな」「ホシはこいつだ」「動機が見えてきたぜ」

## 捜査の手順（厳守）
1. 現場検証 -- まずエラーログ全体を俯瞰し、「事件の概要」を述べる
2. 証拠分析 -- analyze_stacktrace ツールを使ってスタックトレースを分析する
3. 聞き込み -- search_error ツールでエラーメッセージの一般的な原因を調べる
4. 推理 -- 証拠を総合して「犯人（ホシ）」と「動機」を特定する
5. 捜査報告 -- 修正案を具体的なコード付きで提示する

## 出力ルール
- 各セクションは簡潔に。1-2文で収める
- コード例は最小限の修正箇所のみ
- 冗長な説明は禁止。テンポよく

## 出力形式
捜査報告は以下の形式で出力する:

【事件概要】（1-2文で簡潔に）

【捜査結果】
犯人（ホシ）: （原因を1文で）
動機: （なぜ起きたか1文で）

【処方箋】（修正コードを短く）

【ベテランの一言】（一言アドバイス）
""",
    )


detective = get_detective()

# UI
st.title("バグ捜査一課")
st.caption("AIデバッグ刑事（デカ）にエラーログを通報しよう")

error_log = st.text_area(
    "エラーログを貼り付けてください",
    height=200,
    placeholder="Traceback (most recent call last):\n  File ...",
)

if st.button("捜査開始", type="primary"):
    if not error_log.strip():
        st.warning("エラーログが入力されていません。")
    else:
        with st.spinner("デカが捜査中..."):
            response = detective(error_log)
            st.markdown("---")
            st.markdown(str(response))