# stanza_morph_table.py
import stanza
from tabulate import tabulate

# Завантаження моделі української мови (тільки раз)
stanza.download('uk', processors='tokenize,pos,lemma', verbose=False)

# Ініціалізація пайплайну
nlp = stanza.Pipeline(lang='uk', processors='tokenize,pos,lemma', verbose=False)

# Мапи тегів
CASE_MAP = {
    "Nom": "Називний",
    "Gen": "Родовий",
    "Dat": "Давальний",
    "Acc": "Знахідний",
    "Ins": "Орудний",
    "Loc": "Місцевий",
    "Voc": "Кличний"
}

NUMBER_MAP = {
    "Sing": "Однина",
    "Plur": "Множина"
}

GENDER_MAP = {
    "Masc": "Чоловічий",
    "Fem": "Жіночий",
    "Neut": "Середній",
    "Com": "Спільний"
}

TENSE_MAP = {
    "Past": "Минулий",
    "Pres": "Теперішній",
    "Fut": "Майбутній"
}

ASPECT_MAP = {
    "Perf": "Доконаний",
    "Imp": "Недоконаний"
}

PERSON_MAP = {
    "1": "1-ша",
    "2": "2-га",
    "3": "3-тя"
}

POS_MAP = {
    "NOUN": "Іменник",
    "VERB": "Дієслово",
    "ADJ": "Прикметник",
    "ADV": "Прислівник",
    "PRON": "Займенник",
    "NUM": "Числівник",
    "CONJ": "Сполучник",
    "PART": "Частка",
    "INTJ": "Вигук",
    "ADP": "Прийменник",
    "PROPN": "Іменник власний"
}

class StanzaMorphologyTable:
    def __init__(self):
        self.nlp = nlp

    def _map_feats(self, feats_str):
        """Повертає українські назви відмінку, числа, роду, виду, часу, особи"""
        case, number, gender, aspect, tense, person = "-", "-", "-", "-", "-", "-"
        if feats_str and feats_str != "_":
            for feat in feats_str.split("|"):
                if feat.startswith("Case="):
                    case = CASE_MAP.get(feat.split("=")[1], feat.split("=")[1])
                elif feat.startswith("Number="):
                    number = NUMBER_MAP.get(feat.split("=")[1], feat.split("=")[1])
                elif feat.startswith("Gender="):
                    gender = GENDER_MAP.get(feat.split("=")[1], feat.split("=")[1])
                elif feat.startswith("Tense="):
                    tense = TENSE_MAP.get(feat.split("=")[1], feat.split("=")[1])
                elif feat.startswith("Aspect="):
                    aspect = ASPECT_MAP.get(feat.split("=")[1], feat.split("=")[1])
                elif feat.startswith("Person="):
                    person = PERSON_MAP.get(feat.split("=")[1], feat.split("=")[1])
        return case, number, gender, aspect, tense, person

    def _map_pos(self, pos):
        return POS_MAP.get(pos, pos)

    def generate_table(self, words):
        rows = []
        for word in words:
            doc = self.nlp(word)
            for sent in doc.sentences:
                for w in sent.words:
                    case, number, gender, aspect, tense, person = self._map_feats(w.feats)
                    rows.append([
                        w.text,
                        w.lemma,
                        self._map_pos(w.upos),
                        w.text,
                        case,
                        number,
                        gender,
                        aspect,
                        tense,
                        person
                    ])
        table = tabulate(
            rows,
            headers=["Введене слово", "Лема", "Частина мови",
                     "Форма слова", "Відмінок", "Число", "Рід", "Вид", "Час", "Особа"],
            tablefmt="grid"
        )
        return table
