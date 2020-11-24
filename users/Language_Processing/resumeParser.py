#!/usr/bin/env python
from pprint import pprint

import code
import glob
import nltk
import os
import pandas as pd
import re
import spacy
import subprocess
import sys
import traceback
# import ner
from nltk.corpus import stopwords
from spacy.matcher import Matcher

from testingAuth_wsvincent2.settings import BASE_DIR
from users.models import *
from .convertDocxToText import convertDocxToText
from .convertPDFToText import convertPDFToText


# from convertRtfToText import convertRtfToText


class exportToCSV:
    def __init__(self, fileName='resultsCSV.txt', resetFile=False):
        headers = ['FILE NAME',
                   'NAME',
                   'EMAIL1', 'EMAIL2', 'EMAIL3', 'EMAIL4',
                   'PHONE1', 'PHONE2', 'PHONE3', 'PHONE4',
                   'INSTITUTES1', 'YEARS1',
                   'INSTITUTES2', 'YEARS2',
                   'INSTITUTES3', 'YEARS3',
                   'INSTITUTES4', 'YEARS4',
                   'INSTITUTES5', 'YEARS5',
                   'EXPERIENCE',
                   'DEGREES',
                   ]
        if not os.path.isfile(fileName) or resetFile:
            # Will create/reset the file as per the evaluation of above condition
            fOut = open(fileName, 'w')
            fOut.close()
        fIn = open(fileName)  ########### Open file if file already present
        inString = fIn.read()
        fIn.close()
        if len(inString) <= 0:  ######### If File already exsists but is empty, it adds the header
            fOut = open(fileName, 'w')
            fOut.write(','.join(headers) + '\n')
            fOut.close()

    def write(self, infoDict):
        fOut = open('resultsCSV.txt', 'a+')
        # Individual elements are dictionaries
        writeString = ''
        try:
            writeString += str(infoDict['fileName']) + ','
            writeString += str(infoDict['name']) + ','

            if infoDict['email']:
                writeString += str(','.join(infoDict['email'][:4])) + ','
            if len(infoDict['email']) < 4:
                writeString += ',' * (4 - len(infoDict['email']))
            if infoDict['phone']:
                writeString += str(','.join(infoDict['phone'][:4])) + ','
            if len(infoDict['phone']) < 4:
                writeString += ',' * (4 - len(infoDict['phone']))
            writeString += str(infoDict['%sinstitute' % 'c\\.?a']) + ","
            writeString += str(infoDict['%syear' % 'c\\.?a']) + ","
            writeString += str(infoDict['%sinstitute' % 'b\\.?com']) + ","
            writeString += str(infoDict['%syear' % 'b\\.?com']) + ","
            writeString += str(infoDict['%sinstitute' % 'icwa']) + ","
            writeString += str(infoDict['%syear' % 'icwa']) + ","
            writeString += str(infoDict['%sinstitute' % 'm\\.?com']) + ","
            writeString += str(infoDict['%syear' % 'm\\.?com']) + ","
            writeString += str(infoDict['%sinstitute' % 'mba']) + ","
            writeString += str(infoDict['%syear' % 'mba']) + ","
            writeString += str(infoDict['experience']) + ','
            writeString += str(infoDict['degree']) + '\n'  # For the remaining elements
            fOut.write(writeString)
        except:
            fOut.write('FAILED_TO_WRITE\n')
        fOut.close()


class Parse():
    # List (of dictionaries) that will store all of the values
    # For processing purposes
    information = []
    inputString = ''
    tokens = []
    lines = []
    sentences = []

    def __init__(self, verbose=False, files=[]):
        print('Starting Programme')
        fields = ["name", "address", "email", "phone", "mobile", "telephone", "residence status", "experience",
                  "degree", "cainstitute", "cayear", "caline", "b.cominstitute", "b.comyear", "b.comline",
                  "icwainstitue", "icwayear", "icwaline", "m.cominstitute", "m.comyear", "m.comline", "mbainstitute",
                  "mbayear", "mbaline"]

        # Glob module matches certain patterns
        doc_files = glob.glob("resumes/*.doc")
        docx_files = glob.glob("resumes/*.docx")
        pdf_files = glob.glob("resumes/*.pdf")
        rtf_files = glob.glob("resumes/*.rtf")
        text_files = glob.glob("resumes/*.txt")

        # files = set(doc_files + docx_files + pdf_files + rtf_files + text_files)
        # files = list(files)
        # print ("%d files identified" %len(files))

        for f in files:
            print("Reading File %s" % f)
            # info is a dictionary that stores all the data obtained from parsing
            info = {}

            self.inputString, info['extension'] = self.readFile(f)
            info['fileName'] = f

            self.getEmail(self.inputString, info)

            self.getPhone(self.inputString, info)

            self.getName(self.inputString, info)

            self.Qualification(self.inputString, info)

            self.getExperience(self.inputString, info, debug=False)

            self.getSkills(self.inputString, info, debug=False)

            self.rank_resumes(info)

            csv = exportToCSV()
            csv.write(info)
            self.information.append(info)

    def readFile(self, fileName):
        '''
        Read a file given its name as a string.
        Modules required: os
        UNIX packages required: antiword, ps2ascii
        '''
        extension = fileName.split(".")[-1]
        if extension == "txt":
            f = open(fileName, 'r')
            string = f.read()
            f.close()
            return string, extension
        elif extension == "doc":
            # Run a shell command and store the output as a string
            # Antiword is used for extracting data out of Word docs. Does not work with docx, pdf etc.
            return \
            subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[
                0], extension
        elif extension == "docx":
            try:
                return convertDocxToText(fileName), extension
            except:
                return ''
                pass
        # elif extension == "rtf":
        #    try:
        #        return convertRtfToText(fileName), extension
        #    except:
        #        return ''
        #        pass
        elif extension == "pdf":
            # ps2ascii converst pdf to ascii text
            # May have a potential formatting loss for unicode characters
            # return os.system(("ps2ascii %s") (fileName))
            try:
                return convertPDFToText(fileName), extension
            except:
                return ''
                pass
        else:
            print('Unsupported format')
            return '', ''

    def preprocess(self, document):
        '''
        Information Extraction: Preprocess a document with the necessary POS tagging.
        Returns three lists, one with tokens, one with POS tagged lines, one with POS tagged sentences.
        Modules required: nltk
        '''
        try:
            # Try to get rid of special characters
            try:
                document = document.decode('ascii', 'ignore')
            except:
                document = document.encode('ascii', 'ignore')
            # Newlines are one element of structure in the data
            # Helps limit the context and breaks up the data as is intended in resumes - i.e., into points
            try:
                lines = [el.strip() for el in document.split("\n") if len(el) > 0]  # Splitting on the basis of newlines
            except TypeError:
                lines = [el.strip() for el in document.split(b"\n") if
                         len(el) > 0]  # Splitting on the basis of newlines

            try:
                lines = [nltk.word_tokenize(el) for el in lines]  # Tokenize the individual lines
            except TypeError:
                lines = [nltk.word_tokenize(str(el)) for el in lines]
            lines = [nltk.pos_tag(el) for el in lines]  # Tag them
            # Below approach is slightly different because it splits sentences not just on the basis of newlines, but also full stops 
            # - (barring abbreviations etc.)
            # But it fails miserably at predicting names, so currently using it only for tokenization of the whole document
            try:
                sentences = nltk.sent_tokenize(document)  # Split/Tokenize into sentences (List of strings)
            except TypeError:
                sentences = nltk.sent_tokenize(str(document))
            sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Split/Tokenize sentences into words (List of lists of strings)
            tokens = sentences
            sentences = [nltk.pos_tag(sent) for sent in sentences]  # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
            # Next 4 lines convert tokens from a list of list of strings to a list of strings; basically stitches them together
            dummy = []
            for el in tokens:
                dummy += el
            tokens = dummy
            # tokens - words extracted from the doc, lines - split only based on newlines (may have more than one sentence)
            # sentences - split on the basis of rules of grammar
            return tokens, lines, sentences
        except Exception as e:
            print(e)

    def getEmail(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for emails. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        email = None
        try:
            pattern = re.compile(r'\S*@\S*')
            matches = pattern.findall(inputString)  # Gets all email addresses as a list
            email = matches
        except Exception as e:
            print(e)

        infoDict['email'] = email

        if debug:
            print("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return email

    def getPhone(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for phone numbers. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        number = None
        try:
            pattern = re.compile(
                r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
            # Understanding the above regex
            # +91 or (91) -> [+(]? \d+ -?
            # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
            # hyphen has to be escaped inside the character class if you're not incidication a range
            # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
            # Amendment to above - some also have (0000) 00 00 00 kind of format
            # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
            match = pattern.findall(inputString)
            # match = [re.sub(r'\s', '', el) for el in match]
            # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
            # substitute the characters we don't want just for the purpose of checking
            match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el)) > 6]
            # Taking care of years, eg. 2001-2004 etc.
            match = [re.sub(r'\D$', '', el).strip() for el in match]
            # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
            match = [el for el in match if len(re.sub(r'\D', '', el)) <= 15]
            # Remove number strings that are greater than 15 digits
            try:
                for el in list(match):
                    # Create a copy of the list since you're iterating over it
                    if len(el.split('-')) > 3: continue  # Year format YYYY-MM-DD
                    for x in el.split("-"):
                        try:
                            # Error catching is necessary because of possibility of stray non-number characters
                            # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                            if x.strip()[-4:].isdigit():
                                if int(x.strip()[-4:]) in range(1900, 2100):
                                    # Don't combine the two if statements to avoid a type conversion error
                                    match.remove(el)
                        except:
                            pass
            except:
                pass
            number = match
        except:
            pass

        infoDict['phone'] = number

        if debug:
            print("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return number

    def getName(self, inputString, infoDict, debug=False):
        # '''
        #
        # Given an input string, returns possible matches for names. Uses regular expression based matching.
        # Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        # Modules required: clock from time, code.
        # '''
        #
        # # Reads Indian Names from the file, reduce all to lower case for easy comparision [Name lists]
        file_addr = os.path.join(BASE_DIR, 'users', 'Language_Processing', "allNames.txt")
        indianNames = open(file_addr, "r").read().lower()
        # Lookup in a set is much faster
        indianNames = set(indianNames.split())
        otherNameHits = []
        nameHits = []
        name = None

        try:
            tokens, lines, sentences = self.preprocess(inputString)
            # Try a regex chunk parser
            # grammar = r'NAME: {<NN.*><NN.*>|<NN.*><NN.*><NN.*>}'
            grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'
            # Noun phrase chunk is made out of two or three tags of type NN. (ie NN, NNP etc.) - typical of a name. {2,3} won't work, hence the syntax
            # Note the correction to the rule. Change has been made later.
            chunkParser = nltk.RegexpParser(grammar)
            for tagged_tokens in lines:
                # Creates a parse tree
                if len(tagged_tokens) == 0: continue  # Prevent it from printing warnings
                chunked_tokens = chunkParser.parse(tagged_tokens)
                for subtree in chunked_tokens.subtrees():
                    #  or subtree.label() == 'S' include in if condition if required
                    if subtree.label() == 'NAME':
                        for ind, leaf in enumerate(subtree.leaves()):
                            if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                                # Case insensitive matching, as indianNames have names in lowercase
                                # Take only noun-tagged tokens
                                # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                                # Pick upto 3 noun entities
                                hit = " ".join([el[0] for el in subtree.leaves()[ind:ind + 3]])
                                # Check for the presence of commas, colons, digits - usually markers of non-named entities
                                if re.compile(r'[\d,:]').search(hit): continue
                                nameHits.append(hit)
                                # Need to iterate through rest of the leaves because of possible mis-matches
            # Going for the first name hit
            if len(nameHits) > 0:
                nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits]
                name = " ".join([el[0].upper() + el[1:].lower() for el in nameHits[0].split() if len(el) > 0])
                otherNameHits = nameHits[1:]
        except Exception as e:
            print(traceback.format_exc())
            print(e)

        infoDict['name'] = name
        infoDict['otherNameHits'] = otherNameHits

        if debug:
            print("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return name, otherNameHits

    def getExperience(self, inputString, infoDict, debug=False):
        experience = []
        try:
            for sentence in self.lines:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
                if re.search('experience', sen):
                    sen_tokenised = nltk.word_tokenize(sen)
                    tagged = nltk.pos_tag(sen_tokenised)
                    entities = nltk.chunk.ne_chunk(tagged)
                    for subtree in entities.subtrees():
                        for leaf in subtree.leaves():
                            if leaf[1] == 'CD':
                                experience = leaf[0]
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        if experience:
            infoDict['experience'] = experience
        else:
            infoDict['experience'] = 0
        if debug:
            print("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return infoDict['experience']

    def Qualification(self, inputString, infoDict, debug=False):
        # load pre-trained model
        nlp = spacy.load('en_core_web_sm')
        nlp_text = nlp(inputString)
        tokens = [token.text for token in nlp_text if not token.is_stop]  # removing stop words and implementing word tokenization
        data = pd.read_csv("name_of_degrees.csv")  # reading the csv file
        degree = list(data.columns.values)  # extract values
        degree_set = []

        for token in tokens:  # check for one-grams (example: python)
            if token.lower() in degree:
                degree_set.append(token)

        for token in nlp_text.noun_chunks:  # check for bi-grams and tri-grams (example: machine learning)
            token = token.text.lower().strip()
            if token in degree:
                degree_set.append(token)

        lowercased_degree_list = [x.lower() for x in degree_set]
        duplicates_removed = list(dict.fromkeys(lowercased_degree_list))

        infoDict['degree'] = duplicates_removed
        return infoDict['degree']




    # https://www.omkarpathak.in/2018/12/18/writing-your-own-resume-parser/#fifth-step
    def getSkills(self, inputString, infoDict, debug=False):
        nlp = spacy.load('en_core_web_sm')  # load pre-trained model
        nlp_text = nlp(inputString)
        tokens = [token.text for token in nlp_text if not token.is_stop]  # removing stop words and implementing word tokenization
        data = pd.read_csv("skills.csv")  # reading the csv file
        skills = list(data.columns.values)  # extract values
        skillset = []

        for token in tokens:  # check for one-grams (example: python)
            if token.lower() in skills:
                skillset.append(token)

        for token in nlp_text.noun_chunks:  # check for bi-grams and tri-grams (example: machine learning)
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)

        lowercased_skill_list = [x.lower() for x in skillset]
        duplicates_removed = list(dict.fromkeys(lowercased_skill_list))

        infoDict['skills'] = duplicates_removed
        return infoDict['skills']

    def rank_resumes(self, infoDict):
        Job_Detail = Job_Post.objects.all()
        Application = AppliedJobs.objects.all()
        skills = Job_Skill.objects.all()

        sk_extract = [] # for extracting skills out of users_job_skills table
        for i in range(len(Job_Detail)):    # extract contents from Job Post table
            for j in range(len(Application)):   # extract contents from Applied jobs table
                if Application[j].job_id == Job_Detail[i].id:   # collecting all applications against a job
                    for k in range(len(skills)):
                        if skills[k].job_id == Job_Detail[i].id:    # collecting all skills in particular job post that candidate applied for
                            sk_extract.append(skills[k].title)
                        k+=1
                j+=1
            i+=1

        new_list = [] # collecting names of all matching skills
        parser_skills_lower_case = [x.lower() for x in infoDict['skills']] # for removing case insensitivity, lowercasing skills from PARSER
        sk_extract_lower_case = [x.lower() for x in sk_extract] # same as above - performing for skills from DB
        for parser_skills in parser_skills_lower_case:
            if parser_skills in sk_extract_lower_case:     # collecting matches between skills extracted from parser and skills extracted from job post from DB
                new_list.append(parser_skills)

        infoDict['matching_skills'] = new_list
        infoDict['no_of_matching_skills'] = str(len(new_list))

        return infoDict


if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)
