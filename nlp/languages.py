"""
Language data for the AAC gaze interface.
Every sentence is written in full, in Subject-Object-Verb (SOV) order,
so a doctor can review the exact wording here. Edit this file only to
change a sentence or add an item.

NOTE: English is naturally SVO. The English sentences are deliberately
SOV ("I water want") because of the clinical requirement - confirm with
the doctor. Telugu and Hindi are naturally SOV.

Menu entry "type":
    subject   highlight only (the "I / me" card)
    category  opens a sub-menu ("items")
    sentence  speaks "sentence" immediately
"""


def _item(item_id, label, sentence):
    return {"id": item_id, "label": label, "sentence": sentence}


TELUGU = {
    "code": "te",
    "name": "తెలుగు",
    "english_name": "Telugu",
    "locale": "te-IN",
    "voice_keywords": ["telugu", "te-in", "te_in"],
    "ui": {
        "back": "వెనుకకు",
        "next": "తదుపరి",
        "recalibrate": "RE-CALIBRATE",
        "change_language": "భాష మార్చండి",
        "recal_message": "రీ-కాలిబ్రేషన్ మొదలైంది... స్క్రీన్ మధ్యలో చూడండి",
    },
    "menu": [
        {"id": "me", "label": "నాకు", "type": "subject"},
        {"id": "food", "label": "ఆహారం", "type": "category", "items": [
            _item("dal_roti", "పప్పు చపాతీ", "నాకు పప్పు చపాతీ కావాలి"),
            _item("rice_sabzi", "అన్నం కూర", "నాకు అన్నం కూర కావాలి"),
            _item("snack", "అల్పాహారం", "నాకు అల్పాహారం కావాలి"),
            _item("biscuit", "బిస్కెట్", "నాకు బిస్కెట్ కావాలి"),
            _item("dal_bhat", "పప్పు అన్నం", "నాకు పప్పు అన్నం కావాలి"),
            _item("tiffin", "టిఫిన్", "నాకు టిఫిన్ కావాలి"),
            _item("something_else", "ఇంకేదైనా", "నాకు ఇంకేదైనా కావాలి"),
        ]},
        {"id": "water", "label": "నీళ్లు", "type": "sentence",
         "sentence": "నాకు నీళ్లు కావాలి"},
        {"id": "go", "label": "వెళ్లాలి", "type": "category", "items": [
            _item("room", "గదిలోకి", "నేను గదిలోకి వెళ్లాలి"),
            _item("washroom", "బాత్రూంకి", "నేను బాత్రూంకి వెళ్లాలి"),
            _item("bed", "మంచం మీదకి", "నేను మంచం మీదకి వెళ్లాలి"),
            _item("home", "ఇంటికి", "నేను ఇంటికి వెళ్లాలి"),
            _item("outside", "బయటకి", "నేను బయటకి వెళ్లాలి"),
            _item("hospital", "ఆసుపత్రికి", "నేను ఆసుపత్రికి వెళ్లాలి"),
            _item("garden", "తోటలోకి", "నేను తోటలోకి వెళ్లాలి"),
        ]},
        {"id": "pain", "label": "నొప్పి", "type": "category", "items": [
            _item("head", "తలలో", "నాకు తలలో నొప్పిగా ఉంది"),
            _item("stomach", "కడుపులో", "నాకు కడుపులో నొప్పిగా ఉంది"),
            _item("chest", "ఛాతీలో", "నాకు ఛాతీలో నొప్పిగా ఉంది"),
            _item("hand", "చేతిలో", "నాకు చేతిలో నొప్పిగా ఉంది"),
            _item("legs", "కాళ్లలో", "నాకు కాళ్లలో నొప్పిగా ఉంది"),
            _item("back", "వీపులో", "నాకు వీపులో నొప్పిగా ఉంది"),
            _item("somewhere", "ఎక్కడో", "నాకు నొప్పిగా ఉంది"),
        ]},
        {"id": "help", "label": "సహాయం", "type": "sentence",
         "sentence": "నాకు సహాయం కావాలి"},
        {"id": "yes", "label": "అవును", "type": "sentence", "sentence": "అవును"},
        {"id": "no", "label": "కాదు", "type": "sentence", "sentence": "కాదు"},
    ],
}

ENGLISH = {
    "code": "en",
    "name": "English",
    "english_name": "English",
    "locale": "en-IN",
    "voice_keywords": ["english", "en-in", "en-us", "en-gb", "en_us", "en_gb", "en_in"],
    "ui": {
        "back": "BACK",
        "next": "NEXT",
        "recalibrate": "RE-CALIBRATE",
        "change_language": "Change language",
        "recal_message": "Re-calibrating... look at the center of the screen",
    },
    "menu": [
        {"id": "me", "label": "I", "type": "subject"},
        {"id": "food", "label": "Food", "type": "category", "items": [
            _item("dal_roti", "Dal Roti", "I want dal roti"),
            _item("rice_sabzi", "Rice Curry", "I want rice curry"),
            _item("snack", "Snacks", "I want snacks"),
            _item("biscuit", "Biscuit", "I want a biscuit"),
            _item("dal_bhat", "Dal Rice", "I want dal rice"),
            _item("tiffin", "Tiffin", "I want tiffin"),
            _item("something_else", "Something Else", "I want something else"),
        ]},
        {"id": "water", "label": "Water", "type": "sentence",
         "sentence": "I want water"},
        {"id": "go", "label": "Go", "type": "category", "items": [
            _item("room", "Room", "I want to go to the room"),
            _item("washroom", "Washroom", "I want to go to the washroom"),
            _item("bed", "Bed", "I want to go to bed"),
            _item("home", "Home", "I want to go home"),
            _item("outside", "Outside", "I want to go outside"),
            _item("hospital", "Hospital", "I want to go to the hospital"),
            _item("garden", "Garden", "I want to go to the garden"),
        ]},
        {"id": "pain", "label": "Pain", "type": "category", "items": [
            _item("head", "Head", "I have pain in my head"),
            _item("stomach", "Stomach", "I have pain in my stomach"),
            _item("chest", "Chest", "I have pain in my chest"),
            _item("hand", "Hand", "I have pain in my hand"),
            _item("legs", "Legs", "I have pain in my legs"),
            _item("back", "Back", "I have pain in my back"),
            _item("somewhere", "Anywhere", "I am in pain"),
        ]},
        {"id": "help", "label": "Help", "type": "sentence",
         "sentence": "I want help"},
        {"id": "yes", "label": "Yes", "type": "sentence", "sentence": "Yes"},
        {"id": "no", "label": "No", "type": "sentence", "sentence": "No"},
    ],
}

HINDI = {
    "code": "hi",
    "name": "हिन्दी",
    "english_name": "Hindi",
    "locale": "hi-IN",
    "voice_keywords": ["hindi", "hi-in", "hi_in"],
    "ui": {
        "back": "वापस",
        "next": "अगला",
        "recalibrate": "RE-CALIBRATE",
        "change_language": "भाषा बदलें",
        "recal_message": "री-कैलिब्रेशन शुरू... स्क्रीन के केंद्र में देखें",
    },
    "menu": [
        {"id": "me", "label": "मुझे", "type": "subject"},
        {"id": "food", "label": "खाना", "type": "category", "items": [
            _item("dal_roti", "दाल रोटी", "मुझे खाने में दाल रोटी चाहिए"),
            _item("rice_sabzi", "चावल सब्ज़ी", "मुझे खाने में चावल सब्ज़ी चाहिए"),
            _item("snack", "नाश्ता", "मुझे नाश्ता चाहिए"),
            _item("biscuit", "बिस्कुट", "मुझे बिस्कुट चाहिए"),
            _item("dal_bhat", "दाल भात", "मुझे खाने में दाल भात चाहिए"),
            _item("tiffin", "टिफ़िन", "मुझे टिफ़िन चाहिए"),
            _item("something_else", "कुछ और", "मुझे खाने में कुछ और चाहिए"),
        ]},
        {"id": "water", "label": "पानी", "type": "sentence",
         "sentence": "मुझे पानी चाहिए"},
        {"id": "go", "label": "जाना है", "type": "category", "items": [
            _item("room", "कमरे में", "मुझे कमरे में जाना है"),
            _item("washroom", "वॉशरूम", "मुझे वॉशरूम जाना है"),
            _item("bed", "बिस्तर पर", "मुझे बिस्तर पर जाना है"),
            _item("home", "घर", "मुझे घर जाना है"),
            _item("outside", "बाहर", "मुझे बाहर जाना है"),
            _item("hospital", "अस्पताल", "मुझे अस्पताल जाना है"),
            _item("garden", "बगीचे में", "मुझे बगीचे में जाना है"),
        ]},
        {"id": "pain", "label": "दर्द", "type": "category", "items": [
            _item("head", "सर में", "मुझे सर में दर्द हो रहा है"),
            _item("stomach", "पेट में", "मुझे पेट में दर्द हो रहा है"),
            _item("chest", "छाती में", "मुझे छाती में दर्द हो रहा है"),
            _item("hand", "हाथ में", "मुझे हाथ में दर्द हो रहा है"),
            _item("legs", "पैरों में", "मुझे पैरों में दर्द हो रहा है"),
            _item("back", "पीठ में", "मुझे पीठ में दर्द हो रहा है"),
            _item("somewhere", "कहीं", "मुझे दर्द हो रहा है"),
        ]},
        {"id": "help", "label": "मदद", "type": "sentence",
         "sentence": "मुझे मदद चाहिए"},
        {"id": "yes", "label": "हाँ", "type": "sentence", "sentence": "हाँ"},
        {"id": "no", "label": "नहीं", "type": "sentence", "sentence": "नहीं"},
    ],
}

LANGUAGES = {"te": TELUGU, "en": ENGLISH, "hi": HINDI}

# Order of the cards on the language-selection page (left to right)
LANGUAGE_ORDER = ["te", "en", "hi"]


def find_entry(entries, entry_id):
    """Return the dict in `entries` whose id matches, or None."""
    for entry in entries:
        if entry["id"] == entry_id:
            return entry
    return None