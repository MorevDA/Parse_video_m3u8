import requests
import m3u8
from multiprocessing import Process

from config_video import atr_video

sess = requests.session()

response = sess.get(
    atr_video.url,
    params=atr_video.params,
    headers=atr_video.headers,

)

master = m3u8.loads(response.text)

playlist = [video_url['uri'] for video_url in master.data["segments"]]

mean = len(playlist) // 2
first_urls, second_urls = playlist[:mean], playlist[mean:]


def load_video(session: object, list_urls: list, file_name: str, par: dict, head: dict, procc: int):
    print(f"start process {procc}")
    with open(file_name, 'wb') as file:
        for x, urls in enumerate(list_urls):
            resp = session.get(urls, headers=head, params=par)
            file.write(resp.content)
            if x % 100 == 0:
                print(procc, x)


if __name__ == "__main__":
    p1 = Process(target=load_video, kwargs={"session": sess, "list_urls": first_urls,
                                            "file_name": "video_2_1.ts", "par": atr_video.params,
                                            "head": atr_video.headers, "procc": 1},
                 daemon=True)
    p2 = Process(target=load_video, kwargs={"session": sess, "list_urls": second_urls,
                                            "file_name": "video_2_2.ts", "par": atr_video.params,
                                            "head": atr_video.headers, "procc": 2},
                 daemon=True)

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    with open("video_2_1.ts", "ab") as main_file:
        with open("video_2_2.ts", "rb") as f:
            for line in f:
                main_file.write(line)
            print("mission complete")
