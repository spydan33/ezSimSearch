from ezSimSearch import ezSimSearch
data = ezSimSearch()
data.load_index("myFacts")

def add_data():
    data.myFacts.add("the tower is 300ft tall")
    data.myFacts.add("great white sharks are big")
    data.myFacts.add("the ocean is deep")
    data.myFacts.add("smoking is bad for you")
    data.myFacts.add("vaping is also probably bad for you")
    data.myFacts.add("I like AI")
    data.myFacts.add("Im running out of things to to write")
    data.myFacts.add("toast")
    data.myFacts.add("only the top one is important")
    data.myFacts.add("still reading are you?")
    data.myFacts.add("well stop there is nothing left")
    data.myFacts.build()

def ask_data():
    ret = data.myFacts.ask("how tall is the tower")
    print(ret)

add_data() #You only need to build the data once before it saved to disk in the same file you have ezSimSearch
ask_data()