import warnings
import pymorphy2
from tabulate import tabulate

warnings.filterwarnings("ignore")

CASE_MAP = {
    "nomn": "Називний",
    "gent": "Родовий",
    "datv": "Давальний",
    "accs": "Знахідний",
    "ablt": "Орудний",
    "loct": "Місцевий",
    "voct": "Кличний"
}

NUMBER_MAP = {
    "sing": "Однина",
    "plur": "Множина"
}

GENDER_MAP = {
    "masc": "Чоловічий",
    "femn": "Жіночий",
    "neut": "Середній",
    "Com": "Спільний"
}

POS_MAP = {
    "NOUN": "Іменник",
    "VERB": "Дієслово",
    "INFN": "Інфінітив",
    "ADJF": "Прикметник (повний)",
    "ADJS": "Прикметник (скорочений)",
    "PRTF": "Дієприкметник (повний)",
    "PRTS": "Дієприкметник (скорочений)",
    "GRND": "Дієприслівник",
    "NUMR": "Числівник",
    "ADVB": "Прислівник",
    "CONJ": "Сполучник",
    "PRCL": "Частка",
    "INTJ": "Вигук",
    "PREP": "Прийменник",
    "NPRO": "Займенник"
}

ASPECT_MAP = {
    "perf": "Доконаний",
    "impf": "Недоконаний"
}

TENSE_MAP = {
    "past": "Минулий",
    "pres": "Теперішній",
    "futr": "Майбутній"
}

PERSON_MAP = {
    "1per": "1-ша",
    "2per": "2-га",
    "3per": "3-тя"
}
class MorphologyTable:
    def __init__(self, show_forms: bool = True):
        """
        :param show_forms: If True, include all word forms in the table;
                           if False, only show the entered word and the lemma row.
        """
        self.morph = pymorphy2.MorphAnalyzer(lang='uk')
        self.show_forms = show_forms

    def _map_tag(self, tag):
        return (
            CASE_MAP.get(tag.case, tag.case or "-"),
            NUMBER_MAP.get(tag.number, tag.number or "-"),
            GENDER_MAP.get(tag.gender, tag.gender or "-"),
            ASPECT_MAP.get(tag.aspect, tag.aspect or "-"),
            TENSE_MAP.get(tag.tense, tag.tense or "-"),
            PERSON_MAP.get(tag.person, tag.person or "-")
        )

    def _map_pos(self, pos):
        return POS_MAP.get(pos, pos or "")

    def generate_table(self, words):
        rows = []

        for word in words:
            parses = self.morph.parse(word)
            parse = parses[0]

            # Морфологія введеного слова
            (word_case, word_number, word_gender,
             word_aspect, word_tense, word_person) = self._map_tag(parse.tag)

            rows.append([
                word,
                parse.normal_form,
                self._map_pos(parse.tag.POS),
                word,
                word_case,
                word_number,
                word_gender,
                word_aspect,
                word_tense,
                word_person
            ])

            # Нормальна форма з позначкою +
            (lemma_case, lemma_number, lemma_gender,
             lemma_aspect, lemma_tense, lemma_person) = self._map_tag(parse.tag)
            rows.append([
                "",
                "+",
                "",
                parse.normal_form,
                lemma_case,
                lemma_number,
                lemma_gender,
                lemma_aspect,
                lemma_tense,
                lemma_person
            ])

            # Усі форми леми (тільки якщо show_forms=True)
            if self.show_forms:
                for f in parse.lexeme:
                    (f_case, f_number, f_gender,
                     f_aspect, f_tense, f_person) = self._map_tag(f.tag)
                    rows.append([
                        "",
                        "",
                        "",
                        f.word,
                        f_case,
                        f_number,
                        f_gender,
                        f_aspect,
                        f_tense,
                        f_person
                    ])

        table = tabulate(
            rows,
            headers=[
                "Введене слово", "Лема", "Частина мови",
                "Форма слова", "Відмінок", "Число", "Рід", "Вид", "Час", "Особа"
            ],
            tablefmt="grid"
        )
        return table
