# Android 자체 미디어 기능으로 음성 추출

[목차로](index.md) · [전사와 싱크](전사와-싱크.md)

영상 전체를 PC로 복사하지 않고, 폴드에서 Android `MediaExtractor`와 `MediaMuxer`를 이용해 AAC 음성 트랙을 M4A로 추출한다. FFmpeg와 Termux는 필요 없다. 제공된 [ExtractAudio.java](android/ExtractAudio.java)는 첫 번째 AAC 트랙을 재인코딩 없이 복사한다. AAC가 없으면 오류로 종료하므로 해당 영상은 별도의 변환 도구로 처리한다. 다른 언어의 AAC 트랙이 여러 개면 첫 번째 트랙이 원하는 음성인지 먼저 확인한다.

## 빌드와 설치

PC에 JDK, Android SDK 플랫폼의 `android.jar`, SDK 빌드 도구의 `d8`, ADB가 필요하다. 아래는 SDK 36 경로의 예시다. 이 문서의 폴더에서 실행하고 실제 SDK 경로와 기기 ID에 맞춰 바꾼다.

```bash
sdk_dir="$HOME/Library/Android/sdk"
build_dir="$(mktemp -d)"
mkdir -p "$build_dir/classes" "$build_dir/dex"
javac -source 8 -target 8 -cp "$sdk_dir/platforms/android-36/android.jar" -d "$build_dir/classes" android/ExtractAudio.java
"$sdk_dir/build-tools/36.0.0/d8" --lib "$sdk_dir/platforms/android-36/android.jar" --output "$build_dir/dex" "$build_dir/classes/ExtractAudio.class"
(cd "$build_dir/dex" && jar cf "$build_dir/extract-audio.jar" classes.dex)
adb -s "PHONE_ID" push "$build_dir/extract-audio.jar" /data/local/tmp/extract-audio.jar
```

`/data/local/tmp`의 도구는 영구 설치가 아니므로 초기화 등으로 없어지면 다시 빌드하고 전송한다. Wi-Fi 또는 USB의 실제 `adb devices -l` 기기 ID를 사용한다.

## 추출

실제 파일명을 지정하고, 기존 출력이 있으면 덮어쓰지 않도록 먼저 확인한다. 입력과 출력이 모두 폰에 있어야 한다. 따옴표와 경로는 실제 파일명에 맞춘다.

```bash
adb -s "PHONE_ID" shell 'mkdir -p /sdcard/Download/subtitle_audio; test ! -e "/sdcard/Download/subtitle_audio/movie.m4a" && CLASSPATH=/data/local/tmp/extract-audio.jar app_process /system/bin ExtractAudio "/sdcard/Download/Netfile/movie.mp4" "/sdcard/Download/subtitle_audio/movie.m4a"'
```

성공하면 AAC 샘플 수와 원본 트랙 정보가 출력된다. 추출된 파일의 코덱, 채널, 샘플레이트와 길이를 확인하고 처음·중간·끝을 재생해 누락 여부를 확인한다. 컨테이너의 패딩이나 시작 시각에 따라 길이나 싱크가 조금 달라질 수 있으므로 실제 영상과 자막 기준 시각도 대조한다. 원본 영상과 추출 음성은 별도로 보관한다.

## 확인한 사례

SDAB-357에서 Android 16 폴드로 추출한 결과 원본·M4A 모두 AAC, 44.1kHz, 스테레오였다. 원본 오디오 길이는 9,990.038초, 추출본은 9,990.0838초였으며 샘플 430,237개를 기록했다. 이 확인은 해당 파일에 대한 코덱·길이 확인이며 전체 청취 검수는 별도다.
