with futures.ThreadPoolExecutor() as executor:  # default/optimized number of threads
    list(executor.map(doIt, links))
    for i in range(len(movieList)):
        print(movieList[i].title)
        print(movieList[i].service)
        print(movieList[i].genres)
        print("---------")