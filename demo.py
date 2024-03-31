import pvporcupine
import pveagle
from pvrecorder import PvRecorder


def main() -> int:
    access_key: str
    with open("key.txt") as key_file:
        access_key = key_file.read()

    porcupine: pvporcupine.Porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=['picovoice'],
    )

    profile: pveagle.EagleProfile
    with open("profile.txt", "rb") as profile_file:
        profile = pveagle.EagleProfile.from_bytes(profile_file.read())

    eagle: pveagle.Eagle = pveagle.create_recognizer(
        access_key=access_key,
        speaker_profiles=profile,
    )

    try:
        recorder: PvRecorder = PvRecorder(
            frame_length=porcupine.frame_length,
        )
        recorder.start()
        print("Recording | ctrl + c to quit")

        print("Listening for wake word")
        while True:
            audio_frame: list[int] = recorder.read()
            result: int = porcupine.process(audio_frame)

            if result == 0:
                print("Wake word detected")
                recorder.stop()
                break

        recorder.delete()
        recorder: PvRecorder = PvRecorder(
            frame_length=eagle.frame_length,
        )
        recorder.start()

        print("Identifing speaker")
        while True:
            audio_frame: list[int] = recorder.read()
            score: float = eagle.process(audio_frame)[0]

            if score > 0.9:
                print("Speaker identified")
                break

        print("Execution Complete")
        print("Exiting ...")

    except KeyboardInterrupt:
        print("\nExiting ...")
    finally:
        recorder.stop()
        recorder.delete()
        porcupine.delete()
        eagle.delete()

    return 0


if __name__ == "__main__":
    main()
