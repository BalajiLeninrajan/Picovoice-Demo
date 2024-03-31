import pveagle
from pvrecorder import PvRecorder


def main() -> int:
    access_key: str
    with open("key.txt") as key_file:
        access_key = key_file.read()

    eagle: pveagle.EagleProfiler = pveagle.create_profiler(
        access_key=access_key,
    )

    recorder: PvRecorder = PvRecorder(
        frame_length=512,
    )

    num_samples: int = eagle.min_enroll_samples // 512

    print("Start talking to enroll")

    try:
        percentage: float = 0
        feedback: pveagle.EagleProfilerEnrollFeedback

        while percentage < 100:
            frames: list[int] = list()
            recorder.start()

            for _ in range(num_samples):
                audio_frame: list[int] = recorder.read()
                frames.extend(audio_frame)

            recorder.stop()
            percentage, feedback = eagle.enroll(frames)
            print(feedback.name)

        print("Recording complete")
        profile: pveagle.EagleProfile = eagle.export()

        with open("profile.txt", "wb") as profile_file:
            profile_file.write(profile.to_bytes())
        print("Saved profile to profile.txt")

    except KeyboardInterrupt:
        print("Exiting, no profile saved")
    finally:
        recorder.stop()
        recorder.delete()
        eagle.delete()

    return 0


if __name__ == "__main__":
    main()
