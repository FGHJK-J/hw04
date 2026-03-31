#!/usr/bin/env python3
"""
开源语音识别实现
使用Vosk库实现音频文件识别和麦克风实时识别
"""

import json
import wave
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np

def recognize_audio_file(audio_path, model_path=None):
    """
    识别音频文件
    :param audio_path: 音频文件路径
    :param model_path: 模型路径（可选）
    :return: 识别结果
    """
    try:
        # 加载模型
        if model_path:
            model = Model(model_path)
        else:
            model = Model(lang="zh-cn")  # 默认加载中文模型
        
        # 打开音频文件
        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            print("音频格式必须是16kHz、16位、单声道")
            return None
        
        # 初始化识别器
        recognizer = KaldiRecognizer(model, wf.getframerate())
        
        # 识别过程
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                results.append(result.get("text", ""))
        
        # 获取最终结果
        final_result = json.loads(recognizer.FinalResult())
        results.append(final_result.get("text", ""))
        
        return " ".join(results)
    
    except Exception as e:
        print(f"识别失败: {e}")
        return None

def recognize_microphone(model_path=None):
    """
    麦克风实时识别
    :param model_path: 模型路径（可选）
    """
    try:
        # 加载模型
        if model_path:
            model = Model(model_path)
        else:
            model = Model(lang="zh-cn")  # 默认加载中文模型
        
        # 初始化识别器
        recognizer = KaldiRecognizer(model, 16000)
        
        print("开始录音，按Ctrl+C停止...")
        
        def callback(indata, frames, time, status):
            """音频回调函数"""
            if status:
                print(status)
            if recognizer.AcceptWaveform(indata.tobytes()):
                result = json.loads(recognizer.Result())
                print(f"识别结果: {result.get('text', '')}")
        
        # 开始录音
        with sd.InputStream(callback=callback, channels=1, samplerate=16000, dtype=np.int16):
            while True:
                pass
    
    except KeyboardInterrupt:
        print("录音结束")
    except Exception as e:
        print(f"识别失败: {e}")

def main():
    """
    主函数
    """
    print("开源语音识别系统")
    print("1. 识别音频文件")
    print("2. 麦克风实时识别")
    
    choice = input("请选择功能 (1/2): ")
    
    if choice == "1":
        audio_path = input("请输入音频文件路径: ")
        result = recognize_audio_file(audio_path)
        if result:
            print(f"识别结果: {result}")
    
    elif choice == "2":
        recognize_microphone()
    
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
