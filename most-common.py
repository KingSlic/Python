def most_common(s):
    
    counts = {}
    
    for char in s:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1

    count_char_pairs = []
    for char, count in counts.items():
        count_char_pairs.append((count, char))
        
    count_char_pairs.sort(key=lambda x:x[0], reverse=True)

    result = ""
    for pair in count_char_pairs:
        for x in range(0, pair[0]):
            result += pair[1]
            
    
    return result
