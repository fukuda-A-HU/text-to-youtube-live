
import tkinter as tk
from tkinter import messagebox
import requests
import pyaudio

def synthesize_and_play(text, speaker_id=3):
    host = "127.0.0.1"
    port = 50021

    # 音声合成用のクエリ作成
    query_payload = {'text': text, 'speaker': speaker_id}
    query_response = requests.post(f'http://{host}:{port}/audio_query', params=query_payload)

    if query_response.status_code != 200:
        messagebox.showerror("エラー", f"audio_queryエラー: {query_response.text}")
        return

    query = query_response.json()

    # 音声データの生成
    synthesis_payload = {'speaker': speaker_id}
    synthesis_response = requests.post(f'http://{host}:{port}/synthesis', params=synthesis_payload, json=query)

    if synthesis_response.status_code == 200:
        # 音声データの再生
        voice = synthesis_response.content
        pya = pyaudio.PyAudio()

        stream = pya.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=24000,
                          output=True)

        stream.write(voice)
        stream.stop_stream()
        stream.close()
        pya.terminate()
    else:
        messagebox.showerror("エラー", f"synthesisエラー: {synthesis_response.text}")

def on_speak():
    text = text_entry.get()
    if text:
        synthesize_and_play(text)
        text_entry.delete(0, tk.END)
        text_entry.focus()
    else:
        messagebox.showwarning("警告", "テキストを入力してください。")

# GUIのセットアップ
root = tk.Tk()
root.title("VOICEVOX 読み上げアプリ")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

text_label = tk.Label(frame, text="読み上げたいテキスト:")
text_label.pack()

text_entry = tk.Entry(frame, width=50)
text_entry.pack()
text_entry.bind("<Return>", lambda event: on_speak())  # Enterキーで読み上げ

# Quitボタン
quit_button = tk.Button(frame, text="終了", command=root.quit)
quit_button.pack(side=tk.RIGHT)

text_entry.focus()  # 起動時に入力欄にフォーカスをセット

root.mainloop()