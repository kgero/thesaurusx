import re
import subprocess

def get_sense_list(word, pprint=False):
    """Return list of synonyms from English Thesaurus on macOS.

    Each item in list is a string of synonyms for a given part-of-speech.
    Each item starts with 'word part-of-speech'.
    Senses within a part of speech start example usage in parentheses.
    Indications of informal synonyms are removed.

    Example returned list for word='model':

    [
        'model noun (1 a working model) replica, copy, representation, mock-up,
        dummy, imitation, duplicate, reproduction, facsimile. (2 the Canadian
        model of health care) prototype, stereotype, archetype, type, ...',

        'model adjective (1 model trains) replica, toy, miniature, dummy,
        imitation, duplicate, reproduction, facsimile. (2 model farms)
        prototypical, prototypal, archetypal. (3 a model teacher) ideal,
        perfect, exemplary, classic, flawless, faultless.'
    ]
    """
    l = len(word)

    res = subprocess.run(
        ['osx-dictionary', '-d', 'English Thesaurus', word],
        stdout=subprocess.PIPE
        )
    res_text = res.stdout.decode('utf-8')
    clean = res_text.split('CHOOSE THE RIGHT WORD')[0].split('PHRASES')[0].split('REFLECTIONS')[0].split('(English Thesaurus)')[1].strip('\n')
    if not clean:  # means macOS didn't have an entry
        return []

    if ':' not in clean:  # has some funky example sentence, just ignore for now
        return []

    if clean.split(' ')[0] != word:  # returned word w diff morphology
        word = clean.split(' ')[0]
    # remove all periods in example sentences...
    clean = re.sub(r'(?<=Mr)\.|(?<=Mrs)\.|(?<=Dr)\.', '', clean)
    clean = re.sub(r'U\.S\.', 'US', clean)
    clean = re.sub(r'\.\.\.', '', clean)
    clean = re.sub(r'option\:', 'option', clean)
    clean = re.sub('1.98', '1', clean)
    clean = re.sub('E.', 'E', clean)
    # then split senses by the period at the end of each sense
    sense = clean.split('.')
    sense_new = []  # convert into senses per part of speech

    pos = ['verb', 'noun', 'adjective', 'adverb', 'preposition', 'conjunction', 'exclamation']

    if pprint:
        print(res_text, '\n')
        print('clean', clean, '\n')
        # print(sense, '\n')

    curr_pos = ''
    for s in sense:
        s = s.strip(' \n')

        if not s or 'ANTONYMS' in s or ':' not in s:  # throw out empty, antonyms, and w/o example
            continue
        elif re.search(r'(?<=\d):(?=\d)', s) is not None:  #looks for times like 5:30 and removes :
            idx = s.index(':')
            s = s[:idx] + s[idx+1:]
        elif word in ['pugilist', 'zapped', 'zap', 'wedding', 'damage']:  #outdated or informal or weird words
            return []
        elif word in ['wont', 'start', 'slate', 'embark', 'quit', 'start', 
            'walkout', 'awake', 'biological', 'supposed', 'promptly', 'occur']:
            idx = s.index(':')
            s = s[:idx] + s[idx+1:]
        if s.count(':') > 1:
            print(word, s)

        s_words = s.split(' ')
        # if starts with the query word, it's the first sense
        if s_words[0] == word:
            try:
                pre, post = s.split(':')
            except:
                print('A. error on', s)
                raise
            pre_words = pre.split(' ')
            word_pos = ' '.join(pre_words[:2])
            example = ' '.join(pre_words[2:])
            s = word_pos + ' (' + example.strip(' ') + ')' + post
        # if starts w pos, it's another sense
        elif s_words[0] in pos:
            sense_new.append(curr_pos)
            curr_pos = ''
            try:
                pre, post = s.split(':')
            except:
                print('B. error on', s)
                raise()
            pre_words = pre.split(' ')
            example = ' '.join(pre_words[1:])
            s = word + ' ' + pre_words[0] + ' (' + example.strip(' ') + ')' + post
        # it's a sense to add to the curr_pos
        else:
            pre, post = s.split(':')
            s = '(' + pre.strip(' ') + ')' + post

        if 'informal' in s:  # special case of stripping informal label
            if s[s.index('informal') + 8] not in [',', '.', ';']:
                s = s.replace('informal', '')

        curr_pos += s + '. '
    sense_new.append(curr_pos[:-2])

    if pprint:
        for s in sense_new:
            print(s)
        print('\n')
    return sense_new

def get_syn_words(thes_string):
    """Return list of synonyms from a thesaurus string.

    Example of thes_string:

    'model adjective (1 model trains) replica, toy, miniature, dummy,
    imitation, duplicate, reproduction, facsimile. (2 model farms)
    prototypical, prototypal, archetypal. (3 a model teacher) ideal,
    perfect, exemplary, classic, flawless, faultless.'

    Example returned list:

    ['']
    """
    syn_list = []
    senses = thes_string.split('(')[1:]
    for s in senses:
        word_string = s.split(')')[-1]
        words = [w.strip('. ') for w in re.split(r';|,', word_string)]
        syn_list += words
    return syn_list

def get_wordlist(mobythes_path):
    """Return list of words from moby thesaurus file."""
    allwords = set()
    with open(mobythes_path, 'r') as fle:
        for line in fle:
            words = [w.strip('\n') for w in line.split(',') if ' ' not in w]
            allwords.update(set(words))
    return list(allwords)

def create_macos_thes(wordlist, outpath, tmpfle='tmp/thes.txt', verbose=False):
    """Write thesaurus textfile to outpath.

    Query every word in wordlist to the macOS English Thesaurus.

    If verbose, include sense information.
    Else just write all words for a given part of speech.
    """
    found_words = set()
    with open(outpath, 'r') as fle:
        for line in fle:
            word = line.split(' ')[0]
            found_words.add(word)
    with open(tmpfle, 'r') as fle:
        text = fle.read()
        words = line.split(' ')
        found_words.add(word)

    print('found_words', len(found_words))
    print('wordlist', len(wordlist))
    wcount = 0  # count through wordlist
    with open(outpath, 'a') as fle:
        for w in wordlist:
            wcount += 1
            if wcount % 1000 == 0:
                print(wcount, 'of', len(wordlist), 'in wordlist')

            if w in found_words:
                continue

            senses = get_sense_list(w)
            if not senses:
                with open(tmpfle, 'a') as outfle:
                    outfle.write(w + ' ')
                continue
            if senses[0].split(' ')[0] in found_words:
                continue

            found_words.add(w)
            for s in senses:
                word_pos = ' '.join(s.split(' ')[:2])
                if len(word_pos) == 0:
                    print('found empty:', w)
                    return
                if word_pos[0] == '(':
                    print('found weird:', w, word_pos, s)
                    return
                syn_list = get_syn_words(s)
                line = ', '.join(syn_list)
                fle.write(word_pos + ':' + line + '\n')
            
            with open(tmpfle, 'a') as outfle:
                outfle.write(w + ' ')
    return count


def run_test():
    test_words = ['adapt', 'adopt', 'model', 'expect', 'love', 'unofficial', 'poeticule']
    test_words = ['model', 'hinder', 'love', 'vitally', 'ride']
    test_words = ['spirits', 'trapping', 'impugned']
    test_words = ['adapt', 'unfortunately']

    #ugh, some words return 'jell, gel' or 'tradesman, tradeswoman'... :(:(
    # test_words = ['gel', 'tradesman']

    for word in test_words:
        print(word.upper())
        mysenses = get_sense_list(word, pprint=True)
        print(mysenses)
        for s in mysenses:
            # print(s)
            print(get_syn_words(s))
        print('\n\n')


def make_thes():
    wordlist = get_wordlist('dat/other/mthesaur.txt')
    print(len(wordlist))
    print(wordlist[:100])

    count = create_macos_thes(wordlist, 'dat/other/mac_thes.txt')
    print(count, 'words')



# run_test()
make_thes()
