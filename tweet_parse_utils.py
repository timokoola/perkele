from operator import itemgetter


def strip_by_indices(text, indices):
    indices.sort(key=itemgetter(0))

    ret = [text[i[1]:j[0]].strip() for i, j in zip([[None,0]]+indices, indices+[[None]])]
    ret = filter(None, ret)

    return " ".join(ret)


def get_entity_indice_list(entities_dict):
    indices = []

    for entity_type in entities_dict.values():
        for entity in entity_type:
            indices.append(entity["indices"])

    return indices


def fix_html_entities(text):
    return text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

