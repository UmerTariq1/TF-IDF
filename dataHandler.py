
import string
import xml.etree.ElementTree as ET
from stemming.porter2 import stem


class Data_Handler:
    def read_and_process_data(self, filePath ,isLowercase=True, isPunctuationRemoved=True, isStemming=True):
        '''
        This function first reads the data from the file and then processes it.
        processing includes removing punctuation, lower casing and stemming

        @args:
            filePath: string :  path to the file from which data is to be read
            isLowercase: boolean : if True, then the text will be lower cased
            isPunctuationRemoved: boolean : if True, then the punctuation will be removed
            isStemming: boolean : if True, then the words will be stemmed
        @returns:
            data : dictionary. key will be the doc_id (id from corpus , and value will be a dictionary with index, headline and text            
        '''


        xtree = ET.parse(filePath)
        xroot = xtree.getroot()

        DOC_TAG = 'DOC'
        ID_TAG = 'id'
        HEADLINE_TAG = "HEADLINE"
        TEXT_TAG = "TEXT/P"
        ALTERNATE_TEXT_TAG = "TEXT"

        #data : dictionary. key will be the doc_id (id from corpus , and value will be a dictionary with index, headline and text
        # headline will the headline from corpus and will be an empty list if there is no headline. otherwise it will be a list of words in the headline
        # text will be a list of lists. of all the text in p tag from corpus.

        data = {}
        for index, each_doc in enumerate(xroot.findall(DOC_TAG)):
            doc_id = each_doc.get(ID_TAG)

            headline = each_doc.find(HEADLINE_TAG).text if each_doc.find(HEADLINE_TAG) is not None else ""
            headline = headline.split()
            
            text = [i.text for i in each_doc.findall(TEXT_TAG)] #this text is a list of all the text in p tag for ith document document
            if len(text) == 0: #if there is p tag in text, then the text will be in the TEXT tag itself.
                text = [i.text for i in each_doc.findall(ALTERNATE_TEXT_TAG)] #this text is a list of all the text in p tag for ith document document

            # convert this text into a list of list of words. where outer list is for each p tag and inner list is for each word in that p tag
            text = [i.split() for i in text]

            if isPunctuationRemoved:
                # call remove_punctuation function to remove punctuation from headline and text
                # call to be made on each word in headline and text
                headline = [self.remove_punctuation(i) for i in headline]
                text = [[self.remove_punctuation(j) for j in i] for i in text]

            if isLowercase:                
                #lower case 
                headline = [self.lower_case(i) for i in headline]
                text = [[self.lower_case(j) for j in i] for i in text]

            # remove any leading or trailing spaces in both headline and text
            headline = [i.strip() for i in headline]
            text = [[j.strip() for j in i] for i in text]
            

            if isStemming:
                #stem the tokens using the porter2 stemmer
                # use it like this : stemmedWord = stem(word)
                # call to be made on each word in headline and text
                headline = [stem(i) for i in headline]
                text = [[stem(j) for j in i] for i in text]

            
            data[doc_id] = {"index": index, "headline": headline, "text": text}
        return data
    

    def remove_punctuation(self, text):
        '''
        given a string text / word in a sentence, remove the punctuation marks from it. return the empty string if the text is None or empty after removing the punctuation marks

        @args:
            text: string : the text from which punctuation is to be removed
        @returns:
            string : the text after removing the punctuation marks
        '''

        if text is None or text == "":
            return ""
        else:
            temp = text.translate(str.maketrans('', '', string.punctuation))
            return temp
    
    def lower_case(self, text):
        '''
            given a string text / word in a sentence, convert it to lower case. return the empty string if the text is None or empty after converting it to lower case
        @args:
            text: string : the text which is to be converted to lower case
        @returns:
            string : the text after converting it to lower case
        '''

        return text.lower()

    def preprocess_query(self, query_terms, isLowercase=True, isPunctuationRemoved=True, isStemming=True):
        '''
        do all the preprocessing on the query terms which was done on the corpus
        lower case, punctuation removal and stemming
        
        @args:
            query_terms: list[string] : list of query terms
            isLowercase: boolean : if True, then the text will be lower cased
            isPunctuationRemoved: boolean : if True, then the punctuation will be removed
            isStemming: boolean : if True, then the words will be stemmed
        @returns:
            query_terms : list[string] : list of query terms after preprocessing

        '''

        if isPunctuationRemoved:
            query_terms = [self.remove_punctuation(i) for i in query_terms]
        if isLowercase:
            query_terms = [self.lower_case(i) for i in query_terms]
        query_terms = [i.strip() for i in query_terms]
        if isStemming:
            query_terms = [stem(i) for i in query_terms]
        return query_terms
    
    def save_dict(self, my_dict, file_name):
        '''
        functio to save tf or idf dictionaries only.
        for idf the save formate is : doc_id \t term \t idf
        for tf the save format is : doc_id \t term \t tf

        @args:
            my_dict: dictionary : the dictionary to be saved
            file_name: string : the name of the file in which the dictionary is to be saved
        @returns:
            None 
        '''

        #get the list of keys and sort them alphabetically
        dict_keys_list = list(my_dict.keys())
        dict_keys_list.sort()

        #open the file in write mode
        file = open(file_name, "w")

        #write the key value pairs in the file , tab separated
        for index, key in enumerate(dict_keys_list):
            if isinstance(my_dict[key], dict):  #for tf , the value is a dictionary
                inner_dict_keys_list = list(my_dict[key].keys())
                inner_dict_keys_list.sort()
                for index2, inner_key in enumerate(inner_dict_keys_list): #inner_key is the term
                    if (not str(inner_key).isspace()) and len(inner_key)!=0:
                        file.write(key + "\t" + inner_key + "\t" + str(my_dict[key][inner_key]) + "\n")
            
            else:   #for idf, the value is a float
                if (not str(key).isspace()) and len(key)!=0:
                    file.write(key + "\t" + str(my_dict[key]) + "\n")
        file.close()

    def read_tf(self, file_name):
        '''
        read the tf file and populate the self.tf dictionary
        the structure of the file is : doc_id \t term \t tf
        doc_id is the document id and its a string
        term is the term within the doc_id and its a string
        tf is the term frequency of the term in the doc_id and its a float value

        @args:
            file_name: string : the name of the file from which the tf is to be read
        @returns:
            ret_tf: dictionary : the tf dictionary. the structure is : {doc_id: {term: tf}}
        
        '''

        ret_tf = {}
        file=open(file_name, "r")

        for line in file:
            line = line.strip()
            doc_id, term, tf = line.split("\t")
            tf = float(tf)
            if doc_id not in ret_tf:
                ret_tf[doc_id] = {}
            ret_tf[doc_id][term] = tf
        return ret_tf

    def read_idf(self, file_name):
        '''
        read the idf file and populate the self.idf dictionary
        the structure of the file is : term \t idf
        term is the term and its a string
        idf is the inverse document frequency of the term and its a float value
        
        @args:
            file_name: string : the name of the file from which the idf is to be read
        @returns:
            ret_idf: dictionary : the idf dictionary. the structure is : {term: idf}

        '''

        ret_idf = {}
        file = open(file_name, "r")
        for line in file:
            line = line.strip()
            term, idf = line.split("\t")
            idf = float(idf)
            ret_idf[term] = idf
        return ret_idf
    
