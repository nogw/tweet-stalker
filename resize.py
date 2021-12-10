def resize(max, text):
    breaked = ""
    striped = text.split()
    line = 0

    for (i, c) in enumerate(striped):
        line += len(c)
        if line > max:
            line = 0
            breaked += (f"{striped[i - 1]}\n") 
        else: breaked += (f"{c} ")

    print(striped)
    print(breaked)

resize(40, "@kazuhapeitos @ghostlytofu eh brincadeira por favo deixa eu ficar tirando fotinha")