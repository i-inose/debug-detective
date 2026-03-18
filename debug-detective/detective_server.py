from bedrock_agentcore.runtime import BedrockAgentCoreApp
from agent import detective

# AgentCore Runtime用のエントリポイント
app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    """AgentCore Runtimeからの呼び出しを処理する"""
    user_message = payload.get("prompt", "")
    response = detective(user_message)
    return {"result": str(response)}


if __name__ == "__main__":
    app.run()