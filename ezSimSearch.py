from annoy import AnnoyIndex
import sqlite3
from openai import OpenAI
import os
import traceback

class ezSimSearch:
    class index_template:
        def __init__(self,ezSimSearch,name):
            self.index = False
            self.build_trees = 100
            self.dimensions = 3072
            self.geometry = 'euclidean'
            self.name = name
            self.built = False
            self.vector_build_item_index = 0
            self.ezSimSearch = ezSimSearch
            self.cn = sqlite3.connect('ezSimSearch.db')
            self.client = OpenAI()
            self.saved_to_disk = False
            c = self.cn.cursor()
            c.execute(f"CREATE TABLE IF NOT EXISTS {name} (row_id INTEGER,data VARCHAR);")
            c.execute(f"CREATE INDEX IF NOT EXISTS row_id_idex ON {name} (row_id);")
            self.cn.commit()
        
        def add(self,data):
            try:
                if(self.saved_to_disk):
                    Exception("Must Rebuild index")
                embeddings = self.ezSimSearch.vectorize(data)
                c = self.cn.cursor()
                c.execute(f'''
                INSERT INTO {self.name} (row_id,data) VALUES(?1,?2);
                ''',[self.vector_build_item_index,data])
                self.cn.commit()
                self.index.add_item(self.vector_build_item_index, embeddings)
                self.vector_build_item_index += 1
            except Exception as e:
                print(f"An error occurred in init: {e}")
                traceback.print_exc()
                return False
        def add_vec(self,data,vectors):
            try:
                if(self.saved_to_disk):
                    Exception("Must Rebuild index")
                embeddings = vectors
                c = self.cn.cursor()
                c.execute(f'''
                INSERT INTO {self.name} (row_id,data) VALUES(?1,?2);
                ''',[self.vector_build_item_index,data])
                self.cn.commit()
                self.index.add_item(self.vector_build_item_index, embeddings)
                self.vector_build_item_index += 1
            except Exception as e:
                print(f"An error occurred in init: {e}")
                traceback.print_exc()
                return False

        def build(self):
            self.index.build(self.build_trees)
            self.index.save(f'{self.name}.ann')
            self.built = True

        def ask(self,query):
            try:
                if(not self.built):
                    Exception("You must build or load an index first")
                query_vector = self.ezSimSearch.vectorize(query)
                results = self.index.get_nns_by_vector(query_vector, 10, -1, True)
                ret = []
                for row_id in results[0]:
                    c = self.cn.cursor()
                    c.execute(f'SELECT data FROM {self.name} WHERE row_id = {row_id}')
                    row = c.fetchone()
                    ret.append(row[0])
                return ret
            except Exception as e:
                print(f"An error occurred in init: {e}")
                traceback.print_exc()
                return False
    def __init__(self):
        try:
            self.client = OpenAI()
            self.file_path = os.path.dirname(os.path.abspath(__file__))
            self.verbose = False
            if(self.verbose):
                print("init passed")

        except Exception as e:
            print(f"An error occurred in init: {e}")
            traceback.print_exc()
            return False

    def load_index(self,name,params = {"build_trees": 100,"geometry":"euclidean","dimentions":3072}):
        try:
            if(name == None):
                Exception("The index must be named")
            index = AnnoyIndex(params["dimentions"],params["geometry"])
            if os.path.exists(f"{self.file_path}\\{name}.ann"):
                if(self.verbose):
                    print("Loading data...")
                index.load(f'{name}.ann')
                saved_to_disk = True
            else:
                saved_to_disk = False
                if(self.verbose):
                    print("building data...")
                if(self.verbose):
                    print("Index ready")
            index_obj = self.index_template(self,name)
            index_obj.index = index
            index_obj.saved_to_disk = saved_to_disk
            index_obj.built = saved_to_disk
            setattr(self,name,index_obj)
            
        except Exception as e:
            print(f"An error occurred in new_index: {e}")
            traceback.print_exc()
            return False

    def vectorize(self,text_data):
        text = text_data.replace("\n", " ")
        vectors = self.client.embeddings.create(input = [text], model="text-embedding-3-large").data[0].embedding
        return vectors