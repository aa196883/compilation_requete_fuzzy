import re

def extract_notes_from_query(query):
    '''Extract the notes from a given query.'''

    # Regex to find note details within the query
    note_pattern = re.compile(r"\{class:'(\w+|None)', octave:(\d+|None), dur:(\d+\.\d+|\d+|None)\}\)")

    # Extract all matches
    matches = note_pattern.findall(query)

    # Convert extracted values into a list of tuples (class, octave, duration)
    notes = []
    for match in matches:
        if match[0] == 'None':
            class_ = None
        else:
            class_ = match[0].lower()

        if match[1] == 'None':
            octave = None
        else:
            octave = int(match[1])

        if match[2] == 'None':
            duration = None
        else:
            duration = 1 / float(match[2])

        notes.append((class_, octave, duration))

    return notes

def extract_fuzzy_parameters(query):
    '''
    Extract parameters from a fuzzy query using regular expressions.

    In :
        - query : the *fuzzy* query ;

    Out :
        pitch_distance(float), duration_factor(float), duration_gap(float), alpha(float), allow_transposition(bool), fixed_notes(bool[]), collections(str[] | None)
    '''

    # Extracting the parameters from the augmented query
    pitch_distance_re = re.search(r'TOLERANT pitch=(\d+\.\d+|\d+)', query)
    duration_factor_re = re.search(r'duration=(\d+\.\d+|\d+)', query)
    duration_gap_re = re.search(r'gap=(\d+\.\d+|\d+)', query)
    alpha_re = re.search(r'ALPHA (\d+\.\d+)', query)

    pitch_distance = 0.0 if pitch_distance_re == None else float(pitch_distance_re.group(1))
    duration_factor = 1.0 if duration_factor_re == None else float(duration_factor_re.group(1))
    duration_gap = 0.0 if duration_gap_re == None else float(duration_gap_re.group(1))
    alpha = 0.0 if alpha_re == None else float(alpha_re.group(1))

    # Check for the ALLOW_TRANSPOSITION keyword
    allow_transposition = bool(re.search(r'ALLOW_TRANSPOSITION', query))

    # Check for collections filter
    filter_collections = len(re.compile(r'COLLECTIONS .*\n').findall(query)) > 0
    if filter_collections:
        collection_line = re.compile(r'COLLECTIONS .*\n').findall(query)[0]
        collections = [s.strip('"') for s in re.compile(r'"\w+"').findall(collection_line)]
    else:
        collections = None

    # Extract fixed notes information
    note_pattern = r"\{class:'(\w+|None)', octave:(\d+|None), dur:(\d+\.\d+|\d+|None)\}\)( FIXED)?"
    matches = re.findall(note_pattern, query)
    fixed_notes = [bool(fixed) for _, _, _, fixed in matches]

    return pitch_distance, duration_factor, duration_gap, alpha, allow_transposition, fixed_notes, collections


if __name__ == "__main__":
    # Get the query
    with open('fuzzy_query.cypher', 'r') as file:
        augmented_query = file.read()
    
    print(extract_fuzzy_parameters(augmented_query))
