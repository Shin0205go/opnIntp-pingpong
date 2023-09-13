import interpreter

interpreter.system_message = "あなたはエージェントです。相手はプログラマです。あなたが言ったことに対して環境構築やプログラムのテストを実施します。時々エラーになるので、それを修正させていくのがあなたの仕事です。"
# interpreter.system_message += """
# Run shell commands with -y so the user doesn't have to confirm them.
# """
print(interpreter.system_message)