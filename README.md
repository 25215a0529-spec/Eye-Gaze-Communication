# LooknVoice - Eye-Gaze Communication System (AAC)

A Windows desktop app that lets a person who cannot speak or use their hands
communicate with the eyes, using only a normal webcam. The person looks at a
picture card, and the sentence is shown on screen, spoken aloud in Telugu, Hindi
or English, and announced with a chime for the caretaker. An always-visible
emergency bell sounds an alarm.

Built at the Assistive Technology Lab, BVRIT Narsapur
(collaborATe 2026 Student Innovation Challenge, project name NayanVaani).

> Prototype for communication support. It is not a certified medical device.

## Features
- Webcam only: no special eye-tracker hardware.
- Three languages: Telugu, Hindi and English. Telugu and Hindi sentences use
  their natural word order (subject-object-verb).
- Picture cards (Mulberry Symbols plus our own drawings) in pastel colours on a
  dark, low-glare theme.
- Main menu: Food, Water, Go, Pain, Help, Yes/No, with NEXT and BACK for more
  phrases. The Yes/No page also has "Change language".
- Emergency bell in the top corner of every screen. Look at it for 1.8 s: a
  siren sounds and the screen flashes red. STOP by touch/keys (caretaker) or by
  looking at the STOP card for 3 s (patient).
- Selection by steady gaze (dwell): a ring fills; cards need 1.3 s. The card
  flashes green and beeps, then the sentence is spoken.
- Guided start: splash screen, calibration instructions, language selection
  (with back buttons).
- Works offline. Voices are pre-recorded clips, with a live-voice fallback.

## Requirements
- Windows, Python 3.11, a webcam
- Install packages:  pip install -r requirements.txt
  (includes PyQt6, MediaPipe, OpenCV, NumPy, pyttsx3, pygame)

## Run
    python run.py

Sit facing a light, about 50-60 cm from the screen, and keep your head fairly
still. Follow the dots with your eyes. The accuracy is shown after calibration.

## How it works
1. Webcam: OpenCV captures video.
2. Landmarks: MediaPipe FaceMesh finds the face and the iris centres.
3. Calibration: 14 dots = 7 screen zones (6 cards + the bell) x 2 visits. One
   visit trains the model and the other tests it, so we can report real
   accuracy.
4. Classifier: LDA and kNN models, using iris offsets and head pose. The best
   model is chosen by testing on a visit it did not train on.
5. Voting: at run time the zone guess is averaged over the last 8 frames, and
   the zone only switches when the new one clearly wins. This stops blinks and
   jitter from changing the answer.
6. Dwell selection: hold gaze on a card 1.3 s, on the bell 1.8 s, on STOP 3 s.
7. Output: sentence shown and spoken, or the alarm sounds.

Calibration accuracy in our tests was about 60-86% (chance is about 17%).
Glasses, dim light and head movement can lower it; recalibrate with C or F5.

## Keys and touch
- C or F5: recalibrate
- F11: toggle full screen
- Esc: quit
- Space / Enter / S: stop the alarm (caretaker)
- Every card and button also works by mouse or touch.

## Folders and main files
- run.py                  start-up: window, stages (splash, calibration, running)
- core/eye_tracker.py     MediaPipe landmarks, calibration order, zone layout
- core/cell_classifier.py LDA / kNN zone classifier (N_CELLS = 7)
- ui/main_window.py       screens, menus, dwell logic, emergency flow
- ui/dwell_card.py        picture cards with the filling ring
- ui/bell_button.py       the emergency bell button
- ui/symbols.py           loads the picture symbols
- assets/symbols/         Mulberry Symbols and our own drawings
- nlp/languages.py        phrases and sentences per language
- nlp/emergency_text.py   emergency screen text per language
- audio/                  voice clips, alarm.py and alarm.wav
- tools/                  scripts that list sentences and create audio clips

## Voice clips
1. python tools/list_sentences.py
2. python tools/make_audio.py   (creates the clips; needs internet once)
3. python tools/make_alarm.py   (re-creates audio/alarm.wav if needed)

If no clip exists, the app falls back to a live voice (pyttsx3 / Windows).
If pygame is missing, clips will not play: run pip install pygame.

## Credits and licences
- Picture symbols: Mulberry Symbols, CC BY-SA 4.0, mulberrysymbols.org
  (Steve Lee). Attribution is required.
- MediaPipe and OpenCV: Apache 2.0. NumPy: BSD. pyttsx3: MPL 2.0.
  pygame: LGPL. PyQt6: GPL v3 or commercial: check before any commercial
  release. Online voices used to create clips: check their terms for
  commercial use.

## Limitations and next steps
- Telugu and Hindi text needs review by native speakers and clinicians.
- Not yet tested with patients; this needs ethics approval and informed consent.
- Planned: alerts to a phone or nurse station, caregiver phrase editor, more
  languages, room control, tablet/phone version.

## Versions
- Tag `gemini-base-v1`: the original first version (Hindi only, 12 dots)
- Branch `claude-version`: the improved version described above
