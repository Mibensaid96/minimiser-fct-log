from itertools import product

def generate_truth_table(func, num_vars):
    truth_table = {}
    for inputs in product([0, 1], repeat=num_vars):
        output = func(*inputs)
        truth_table[inputs] = output
    return truth_table

def min_terms_from_karnaugh_map(map):
    rows, cols = len(map), len(map[0])
    min_terms = set()

    for i in range(rows):
        for j in range(cols):
            if map[i][j] == 1:
                min_terms.add((i, j))

    return min_terms

def simplify_terms(terms):
    simplified_terms = []
    for term1 in terms:
        for term2 in terms:
            if term1 != term2:
                xor = term1 ^ term2
                if bin(xor).count('1') == 1:  # Check if only one bit is different
                    mask = 1 << (len(bin(xor)) - bin(xor).rfind('1') - 2)
                    if (term1 & mask) == 0:  # Check if both terms differ on same variable
                        simplified_term = term1 & ~mask  # Simplify term by removing differing variable
                        if simplified_term not in simplified_terms:
                            simplified_terms.append(simplified_term)
    return simplified_terms

def min_func_from_terms(terms, num_vars):
    min_func = ""
    for term in terms:
        variables = []
        for i in range(num_vars):
            if term & (1 << (num_vars - i - 1)):
                variables.append(chr(65 + i))  # Convert 0-based index to variable name
            else:
                variables.append(chr(65 + i) + "'")  # Complement variable name if necessary
        min_func += "+".join(variables) + " "
    return min_func

# Example function: F(A, B, C) = A'B' + A'C + AB
def example_func(A, B, C):
    return (not A) and (not B) or A and C or A and B

def main():
    num_vars = 3  # Number of variables in the function
    truth_table = generate_truth_table(example_func, num_vars)

    # Convert truth table to Karnaugh map
    k_map = [[truth_table[(A, B, C)] for C in range(2)] for B in range(2) for A in range(2)]
    k_map = [k_map[i:i + 2] for i in range(0, len(k_map), 2)]

    min_terms = min_terms_from_karnaugh_map(k_map)
    simplified_terms = simplify_terms(min_terms)
    min_func = min_func_from_terms(simplified_terms, num_vars)

    print("Function minimized using Karnaugh Map:")
    print(min_func)

if __name__ == "__main__":
    main()
