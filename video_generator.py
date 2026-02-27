import requests
from moviepy.editor import concatenate_videoclips, TextClip, AudioFileClip

def generate_ai_video(text_prompt, voice_prompt):
    # 第一步：调用AI视频API生成视频片段
    api_url = "https://api.runwayml.com/v1/video/generate"
    payload = {
        "prompt": text_prompt,
        "duration": 5  # 根据实际API限制
    }
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    resp = requests.post(api_url, json=payload, headers=headers)
    video_url = resp.json()["video_url"]

    # 下载生成的视频
    video_file = '/tmp/generated.mp4'
    r = requests.get(video_url, stream=True)
    with open(video_file, 'wb') as f:
        for chunk in r.iter_content(1024): f.write(chunk)

    # 第二步：生成配音
    audio_url = generate_voice(voice_prompt)
    audio_file = '/tmp/voice.mp3'
    r = requests.get(audio_url, stream=True)
    with open(audio_file, "wb") as f: f.write(r.content)

    # 第三步：合成音频与视频
    from moviepy.editor import VideoFileClip
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    final = video.set_audio(audio)
    final.write_videofile("/tmp/final_video.mp4")

    return "/tmp/final_video.mp4"

def generate_voice(text):
    # 示例调用OpenAI TTS接口
    api_url = "https://api.openai.com/v1/audio/speech"
    resp = requests.post(api_url, json={"text": text, "voice": "alloy"}, headers={"Authorization": "Bearer YOUR_API_KEY"})
    return resp.json()["audio_url"]