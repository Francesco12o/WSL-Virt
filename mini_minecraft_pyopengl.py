
import os
from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label

class VideoLauncher(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        Window.size = (800, 600)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(current_dir, "video.mp4")
        print("Calea video:", video_path)

        if os.path.exists(video_path):
            video = Video(source=video_path, options={'eos': 'loop'})
            layout.add_widget(video)

            # Redare automată după adăugare în layout
            def play_video(*args):
                video.state = 'play'
            from kivy.clock import Clock
            Clock.schedule_once(play_video, 0.5)
        else:
            layout.add_widget(Label(text="Fișierul video.mp4 nu a fost găsit!"))

        return layout

if __name__ == "__main__":
    VideoLauncher().run()
