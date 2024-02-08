# ezSimSearch
An easily implemented all in one similarity search. I made this for context retrieval of LLMs, but it could also work for a basic fuzzy search

# Why ezSimSearch?
I have been needing retreival augmented generation for a few of my projects that use LLMs and spent a few hours in the langchain documentation looking for what I needed. I installed alot of packages and tried alot of things and eventually got annoyed(no pun intended) so I built my own similarity search that is alot easier to use. I thought maybe somone else could use it to.

# ezSimSearch Project Documentation

This project, named ezSimSearch, leverages the Annoy (Approximate Nearest Neighbors Oh Yeah) library, SQLite for database management, and OpenAI's API for generating embeddings. It's designed to simplify the process of indexing and searching high-dimensional vectors for similarity searches.

## Core Components

- **AnnoyIndex**: Utilized for fast similarity search and efficient storage of high-dimensional vectors.
- **SQLite**: Provides a lightweight disk-based database that doesn't require a separate server process, for storing and accessing the vectors' metadata.
- **OpenAI Embeddings**: Generates embeddings for text data, facilitating the comparison of textual similarity through vector space modeling.

## Features

- **Implementating**: easy implementation
- **Vectorization**: Convert text to vectors using OpenAI`s powerful embeddings API, enabling semantic search capabilities.
- **Persistence**: Store and retrieve indexed data from a SQLite database, ensuring data longevity and stability.
- **Search**: Perform fast and efficient similarity searches within the indexed data to find the most relevant items.

## Installation

To use ezSimSearch, clone the repository and ensure you have the required dependencies:

- Python 3.x
- Annoy
- SQLite3
- OpenAI Python client (and api key)
  * you can use `pip install --user requirements.txt -r`

## Usage

1. Initialize the ezSimSearch object.
```
from ezSimSearch import ezSimSearch
data = ezSimSearch()
```
2. create/load your data index `data.load_index("myFacts")`
    - Once you do this the module will either load an index and db with that name or create a new one.
    - after the index and db are created the module will create a new object to interact with those databases. eg `data.myFacts` is how you interact with them.
4. add the text data you want to be included `data.myFacts.add("the tower is 300ft tall")`
    - you only have to do this when creating a new db to search from
5. build your db
    - `data.myFacts.build()`
    - again this is only required with new data
6. ask your data `data.myFacts.ask("how tall is the tower")`
    - Currently this will return the 10 nearest vectors and is only changable in the source code via the second parameter on line `results = self.index.get_nns_by_vector(query_vector, 10, -1, True)` in the ask function.
7. it will return an array with data you added that closest matches what you input

for a code example see `example.py`
## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

