def unique_argmax(arr):
    max_val = max(arr)
    argmax = [i for i, v in enumerate(arr) if v == max_val]
    if len(argmax) > 1:
        raise ValueError()
    else:
        return argmax[0]
    
    
    
