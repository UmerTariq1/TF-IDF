
'''
Introduction to Python Programming (aka Programmierkurs I, aka Python I)
Software Assignment
'''

import time
from TFIDF import TFIDF_custom_class
from dataHandler import Data_Handler


# COLLECTION_NAME = "nyt199501"
COLLECTION_NAME = "nytsmall"


BASE_DIR = "/Users/umer/Desktop/UdS winter 22-23/intro to python/project/"
TOP_N = 10
DATA_DIR = BASE_DIR + "data/"
# OUTPUT_DIR = BASE_DIR + ""
OUTPUT_DIR = BASE_DIR + "output/"

nyt199501_dataPath = DATA_DIR + "nyt199501.xml" 
nysmall_dataPath = DATA_DIR + "nytsmall.xml"
nysmall_updated_dataPath = DATA_DIR + "nytsmall_updated.xml"
PROCESS_HEADLINE = True



class SearchEngine:

    def executeQuery(self, query_terms, top_n = TOP_N):
        '''
        query_terms : list of terms of query : 

        Calculate the similarity score between the query and each document
        Use the formula:

        similarity(query, document) = (inner product of query terms and document terms ) / (length of query vector * length of document vector)

        The upper part of the fraction is the inner product or dot product of the vectors (check out the Wikipedia article if you are not familiar with this). It is computed by multiplying the two weights for the same terms (one weight comes from each vector), and adding these products together.
        The denominator contains the product of the norms of the two vectors. The norm of a vector is computed by creating the sum of all squares of each weight inside the vector, and taking the square root in the end.
        and where the length of a vector is the square root of the sum of the squares of the vector elements.
        '''

        '''
        Input to this function: List of query terms

        Returns the 10 highest ranked documents together with their
        tf.idf-sum scores, sorted score. For instance,

        [('NYT_ENG_19950101.0001', 0.07237004260325626),
         ('NYT_ENG_19950101.0022', 0.013039249597972629), ...]

        May be less than 10 documents if there aren't as many documents
        that contain the terms.
        '''

        #i covnert the query terms back to a single string because i wanted to make TFIDF class generic, but the requirements of the assignment are to use the
        # exact function arguments as given in the assignment description and query terms is a list of strings as given in the assignment description
        # so i convert the list of strings to a single string and then pass it to the TFIDF class where its taken apart again and then the rest of the code

        single_string_query = ' '.join(query_terms)

        top_docs_and_scores = self.tfidf_obj.get_topN_results(single_string_query, top_n)

        return top_docs_and_scores
                   
    def executeQueryConsole(self):
        '''
        When calling this, the interactive console should be started,
        ask for queries and display the search results, until the user
        simply hits enter.
        '''

        query = input("Please enter query, terms separated by whitespace: ")
        while query != "":
            
            top_docs_and_scores = self.executeQuery(query.split())
            if len(top_docs_and_scores) == 0:
                print("Sorry, I didn’t find any documents for this term.")
            else:
                print("I found the following documents:")
                for doc_id, score in top_docs_and_scores:
                    print(doc_id , " \t (", end="")
                    print(str(score).strip(), end="")
                    print(")")
            
            query = input("Please enter query, terms separated by whitespace: ")
                
    def __init__(self, collectionName, create):
        '''
        Initialize the search engine, i.e. create or read in index. If
        create=True, the search index should be created and written to
        files. If create=False, the search index should be read from
        the files. The collectionName points to the filename of the
        document collection (without the .xml at the end). Hence, you
        can read the documents from <collectionName>.xml, and should
        write / read the idf index to / from <collectionName>.idf, and
        the tf index to / from <collectionName>.tf respectively. All
        of these files must reside in the same folder as THIS file. If
        your program does not adhere to this "interface
        specification", we will subtract some points as it will be
        impossible for us to test your program automatically!
        '''

        
        #define the path of the file
        if collectionName == "nytsmall":
            filePath = nysmall_dataPath
        if collectionName == "nytsmall_updated":
            filePath = nysmall_updated_dataPath
        elif collectionName == "nyt199501":
            filePath = nyt199501_dataPath
        
        #read the data
        self.data_handler = Data_Handler()

        data = self.data_handler.read_and_process_data(filePath) #this takes time and its necessary in both create cases because get_scores_for_query takes self.data

        if create:
            print("Creating tf and idf files...")
            self.tfidf_obj = TFIDF_custom_class(data = data)
            self.tfidf_obj.createTfandIDF(processHeadline=PROCESS_HEADLINE, saveFile=True, collectionName=collectionName, output_dir = OUTPUT_DIR)

        else:
            print("Reading tf and idf files...")
            filename_without_extension = OUTPUT_DIR + collectionName

            tf  = self.data_handler.read_tf(filename_without_extension+".tf")
            idf = self.data_handler.read_idf(filename_without_extension+".idf")

            self.tfidf_obj = TFIDF_custom_class(data=data, tf = tf, idf = idf)

        self.tfidf_obj.compute_tfidf()        
        print("Done.")


if __name__ == '__main__':
    '''
    write your code here:
    * load index / start search engine
    * start the loop asking for query terms
    * program should quit if users enters no term and simply hits enter
    '''

    searchEngine = SearchEngine(COLLECTION_NAME, create=True)
    searchEngine.executeQueryConsole()



    #Commented code for future purposes. this code shows how to run all cases and time them
    # Example for how we might test your program:
    # Should also work with nyt199501 !

    # start = time.time()
    # searchEngine = SearchEngine(COLLECTION_NAME, create=True)
    # searchEngine = SearchEngine(COLLECTION_NAME, create=False)
    # end = time.time()
    # print("Time taken in seconds to initialize the search engine for nytsmall : ", end-start)

    # # print(searchEngine.executeQuery(['hurricane', 'philadelphia']))
    # searchEngine.executeQueryConsole()



#I have used the above code to time the initialization of the index and the reading of the index

# Time taken in seconds to initialize the index for nyt199501: 148.6
# Time taken in seconds to read the index for nyt199501: 5.09

# Time taken in seconds to initialize the index for nytsmall: 1.606261968612671
# Time taken in seconds to read the index for nytsmall: 0.06537294387817383
