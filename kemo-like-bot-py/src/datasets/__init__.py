import logging
import re
from bayesian import Bayes

# Setup basic logging
logger = logging.getLogger('classification')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def classify(instance, classes_instances, extractor=str.split, priors=None):
    priors = priors or {class_: 1.0 for class_ in classes_instances}
    model = Bayes.extract_events_odds(classes_instances, data_extractor)
    bayes_res = Bayes(priors)
    bayes_res.update_from_events(extractor(instance), model)
    #logger.debug("Result '%s' for '%s'", to_str(b), extractor(instance))
    #b.most_likely()
    return bayes_res


def to_str(bayes):
    items = []
    for label, item in zip(bayes.labels, bayes.normalized()):
        items.append('{}: {}%'.format(label, round(item * 100, 2)))
    return '{}'.format(', '.join(items))


def data_extractor(content):
    return filter(lambda word: len(word) > 2, re.split(' |;|,|\*|\n|:|\[|\]|{|}|\(|\)', content))
