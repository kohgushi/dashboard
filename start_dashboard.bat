@echo off
REM バッチファイルが存在するディレクトリに移動
cd %~dp0

REM conda環境 'streamlit' をアクティベート
CALL conda activate streamlit

REM streamlitアプリケーションを実行
streamlit run dashboard.py

REM コマンドプロンプトを開いたままにする
pause
