import inspect
from collections import namedtuple
from words import words_array

# патч для сучасних Python
if not hasattr(inspect, "getargspec"):
    ArgSpec = namedtuple("ArgSpec", "args varargs keywords defaults")

    def getargspec(func):
        spec = inspect.getfullargspec(func)
        return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)

    inspect.getargspec = getargspec

from table import MorphologyTable

# Only entered word + lemma row
mt1 = MorphologyTable(show_forms=False)
#print(mt1.generate_table(words_array))

# Entered word + lemma + all word forms
mt2 = MorphologyTable(show_forms=True)
print(mt2.generate_table(words_array))