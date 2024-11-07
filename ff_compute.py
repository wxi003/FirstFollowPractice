import sys
from collections import defaultdict

# Global dictionaries for EPS, FIRST, and FOLLOW
EPS = {}
FIRST = {}
FOLLOW = {}

def parse_grammar(file_name):
    global EPS, FIRST, FOLLOW  # Use the global variables within this function
    productions = defaultdict(list)  # Store production rules for each nonterminal

    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip().replace(" ", "")
            if line:
                head, body = line.split('->')
                if not body:
                    productions[head].append('')  # Use an empty string for epsilon
                else:
                    # Add spaces between each symbol in the body
                    spaced_body = ' '.join(body)
                    productions[head].append(spaced_body)  # Store RHS with spaces

    # Initialize EPS, FIRST, and FOLLOW based on nonterminals in productions
    for nonterminal in productions.keys():
        EPS[nonterminal] = False  # By default, assume no epsilon derivation
        FIRST[nonterminal] = set()  # Initialize FIRST set as empty set
        FOLLOW[nonterminal] = set()  # Initialize FOLLOW set as empty set

    # Augment grammar with start symbol S' -> S $$
    productions["S'"] = ["S $$"]  # Add augmented start production in the desired format
    EPS["S'"] = False
    FIRST["S'"] = set()
    FOLLOW["S'"] = set()

    return productions


# Function to compute EPS(X) for each nonterminal
def compute_eps(productions):
    # Initially set EPS for terminals as False
    for X in productions.keys():
        EPS[X] = any(production == '' for production in productions[X])

    # Iteratively check each production to compute EPS for nonterminals
    progress = True
    while progress:
        progress = False
        for X, prods in productions.items():
            if not EPS[X]:  # Only check if not yet epsilon
                for production in prods:
                    if all(EPS.get(symbol, False) for symbol in production.split()):
                        EPS[X] = True
                        progress = True
                        break

# Function to compute FIRST(X)
def compute_first(productions):
    # Start by adding terminals directly to their FIRST sets in reverse order
    for X in productions:
        for production in reversed(productions[X]):
            if production.islower() and production != '':
                FIRST[X].add(production[0])

    # Perform backward pass (from the end of each production list)
    for X, prods in productions.items():
        for production in reversed(prods):  # Start from the last production
            symbols = production.split()
            for symbol in symbols:
                if symbol.isupper():
                    FIRST[X].update(FIRST[symbol])  # Add FIRST of nonterminal symbol to FIRST(X)
                    if EPS[symbol]:
                        continue  # Continue if the symbol can derive epsilon
                else:
                    FIRST[X].add(symbol)  # Add terminal symbol directly
                break  # Stop if we add a terminal or non-epsilon-producing symbol

    # Perform forward pass (from the beginning of each production list)
    progress = True
    while progress:
        progress = False
        for X, prods in productions.items():
            for production in prods:  # Start from the first production
                symbols = production.split()
                for symbol in symbols:
                    if symbol.isupper():
                        before_update = FIRST[X].copy()
                        FIRST[X].update(FIRST[symbol])
                        if FIRST[X] != before_update:
                            progress = True  # Set progress to True if FIRST set changes
                        if EPS[symbol]:
                            continue  # Continue if the symbol can derive epsilon
                    else:
                        if symbol not in FIRST[X]:  # Check if symbol is not already in FIRST(X)
                            FIRST[X].add(symbol)
                            progress = True
                        break  # Stop if we add a terminal or non-epsilon-producing symbol
    
    # # Special handling for S'
    if EPS.get('S', False):  # Only add $$ to FIRST(S') if S can derive epsilon
        FIRST["S'"].add("$$")
    else:
        FIRST["S'"].discard("$$")  # Ensure $$ is not in FIRST(S') if S cannot derive epsilon
# Function to compute FOLLOW(X)
def compute_follow(productions, start_symbol="S'"):
    # FOLLOW[start_symbol].add('$$')  # Add end-of-input symbol to start symbol
    progress = True
    while progress:
        progress = False
        for X, prods in productions.items():
            for production in prods:
                symbols = production.split()  # Split symbols in the production
                for i, B in enumerate(symbols):
                    if B.isupper():  # B is a nonterminal
                        beta = symbols[i+1:] if i + 1 < len(symbols) else []
                        # Add FIRST(beta) - {epsilon} to FOLLOW(B)
                        if beta:
                            beta_first = set()
                            for symbol in beta:
                                if symbol.isupper():
                                    beta_first.update(FIRST[symbol] - {''})
                                    if not EPS[symbol]:
                                        break
                                else:
                                    beta_first.add(symbol)
                                    break
                            before_update = FOLLOW[B].copy()
                            FOLLOW[B].update(beta_first)
                            if FOLLOW[B] != before_update:
                                progress = True
                        # If beta is empty or EPS(beta) is true, add FOLLOW(X) to FOLLOW(B)
                        if not beta or all(EPS.get(symbol, False) for symbol in beta):
                            before_update = FOLLOW[B].copy()
                            FOLLOW[B].update(FOLLOW[X])
                            if FOLLOW[B] != before_update:
                                progress = True


def write_output(nonterminals, first_sets, follow_sets, output_file):
    with open(output_file, 'w') as f:
        for nonterminal in nonterminals:
            f.write(f"{nonterminal}\n")
            
            # Format and write the FIRST set with "$$" last
            first_set = sorted(x for x in first_sets[nonterminal] if x and x != "$$")
            if "$$" in first_sets[nonterminal]:
                first_set.append("$$")
            first_formatted = ', '.join(first_set)
            f.write(first_formatted + '\n')
            
            # Format and write the FOLLOW set with "$$" last
            follow_set = sorted(x for x in follow_sets[nonterminal] if x and x != "$$")
            if "$$" in follow_sets[nonterminal]:
                follow_set.append("$$")
            follow_formatted = ', '.join(follow_set)
            f.write(follow_formatted + '\n')


def main(input_file, output_file):
    productions = parse_grammar(input_file)
    compute_eps(productions)
    compute_first(productions)
    compute_follow(productions)

    # Define ordering: `S'` first, followed by the other nonterminals in alphabetical order
    nonterminals = sorted(nt for nt in FIRST.keys() if nt.isupper())
    if "S'" in nonterminals:
        nonterminals.remove("S'")
    nonterminals = ["S'"] + nonterminals

    write_output(nonterminals, FIRST, FOLLOW, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ff_compute.py <input_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])
