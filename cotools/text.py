def _get_text(d: dict) -> str:
    tdict = d['body_text']
    return ' '.join([x['text'] for x in tdict])

def get_texts(l: list) -> list:
    return [_get_text(x) for x in l]

def _get_abstract(d: dict) -> str:
    l = d['abstract']
    out = '' if len(l) == 0 else l[0]['text']
    return out

def get_abstracts(l: list) -> list:
    return [_get_abstract(x) for x in l]


