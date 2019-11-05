import nltk
import nltk.data
import re
import os
import spacy


def move_noise(file):

    with open(file) as f:
        content = f.read()

    #print(len(content))

    content_without_non_character = re.sub(r'\[\d+\]', '', content)
    content_without_non_character = re.sub(r'\(\d+\)', '', content_without_non_character)
    content_without_non_character  = re.sub(r'[*]','', content_without_non_character)

    content_without_non_character = re.sub(r"<A.*?>.*?</A>", '', content_without_non_character)
    content_without_non_character = re.sub(r"<a.*?>.*?</a>", '', content_without_non_character)

    content_without_non_character = content_without_non_character.replace('^', '')
    content_without_non_character = content_without_non_character.replace('/', '')
    content_without_non_character = content_without_non_character.replace(',.', ',')
    content_without_non_character = content_without_non_character.replace('!.', '!')
    content_without_non_character = content_without_non_character.replace('！.', '!')
    content_without_non_character = content_without_non_character.replace('!.', '!')
    content_without_non_character = content_without_non_character.replace(';.', ';')
    content_without_non_character = content_without_non_character.replace(':.', ':')
    content_without_non_character = content_without_non_character.replace('?.', '?')
    content_without_non_character = content_without_non_character.replace('?.', '?')
    content_without_non_character = content_without_non_character.replace('/.', '.')
    content_without_non_character = content_without_non_character.replace(' .', '.')



    '''
    content_without_non_character = content_without_non_character.replace('....', '.')
    content_without_non_character = content_without_non_character.replace('...', '.')
    content_without_non_character = content_without_non_character.replace('..', '.')  # remove all '..'
    content_without_non_character = content_without_non_character.replace('..', '.')  # remove all '..'
    '''



    '''
    # following is the process to get the step 2 texts
    content_without_non_character  = content_without_non_character.replace('.','. ')	# Add space after each dot.

    content_without_non_character = content_without_non_character.replace('›', '')
    content_without_non_character = content_without_non_character.replace('‹', '')
    content_without_non_character = content_without_non_character.replace('> ', '')
    content_without_non_character = content_without_non_character.replace('<', '')
    content_without_non_character = re.sub(r'»', '', content_without_non_character)
    content_without_non_character = re.sub(r'«', '', content_without_non_character)
    content_without_non_character = content_without_non_character.replace('«»', '« »')
    content_without_non_character = content_without_non_character.replace('«.»', '« »')
    content_without_non_character = content_without_non_character.replace('«.–»', '« »')
    content_without_non_character = content_without_non_character.replace('«–.»', '« »')
    content_without_non_character = content_without_non_character.replace('[', '')
    content_without_non_character = content_without_non_character.replace(']', '')
    content_without_non_character = content_without_non_character.replace('(', '')
    content_without_non_character = content_without_non_character.replace(')', '')
    content_without_non_character = content_without_non_character.replace(' "', '')
    content_without_non_character = content_without_non_character.replace('".', '"')
    content_without_non_character = content_without_non_character.replace(' "', '"')
    content_without_non_character = content_without_non_character.replace('– ', '')
    content_without_non_character = content_without_non_character.replace('–', '')
    content_without_non_character = content_without_non_character.replace('/', '')
    content_without_non_character = content_without_non_character.replace(',.', ',')
    content_without_non_character = content_without_non_character.replace(';.', ';')
    content_without_non_character = content_without_non_character.replace(' ... ', '.')
    content_without_non_character = content_without_non_character.replace('...', '.')
    content_without_non_character  = content_without_non_character.replace('..','.')	# remove all '..'
    content_without_non_character  = content_without_non_character.replace('..','.')	# remove all '..'
    '''

    return content_without_non_character



def NLTK_splitSentence_write(paragraph, written_file):
    tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
    sentences = tokenizer.tokenize(paragraph)

    txt = []
    for i in sentences:
        # print(i)
        if i == '.':
            a = i.strip('.').strip(' ').strip()
            txt.append(a)
        elif i == ' ' or i == '\n' or i == '\r':
            a=i.strip()
            txt.append(a)
        else:
            a = i.strip('–').strip()+ '\n'
            txt.append(a)

    return txt



def Spacy_set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == '...':
            doc[token.i+1].is_sent_start = True
    return doc



def Spacy_splitSentence_write(paragraph, written_file):
    #tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
    #sentences = tokenizer.tokenize(paragraph)

    nlp = spacy.load('de')

    nlp.add_pipe(Spacy_set_custom_boundaries, before='parser')    # segment by '...' instead of '.'
    sbd = nlp.create_pipe('sentencizer')  # segment by '.','?','!',etc
    nlp.add_pipe(sbd)

    doc = nlp(paragraph)

    txt = []
    for i in doc.sents:
        #print(i)
        txt.append(i.text.strip('\n').strip('-')  + '\n')


        with open(written_file, 'w+') as f:
            f.writelines(txt)




def Own_splitSentence_write(content_without_non_character, written_file):
    cutLineFlag = ["?", "!", ";", ".", "...", ".."]
    sentenceList = []
    oneSentence = ''

    for word in content_without_non_character:

        if word not in cutLineFlag:
            oneSentence = oneSentence + word
        else:
            oneSentence = oneSentence + word
            sentenceList.append(oneSentence.strip(' \n').strip('-')  + "\n")
            oneSentence = ''

    with open(written_file, "w+") as resultFile:
        resultFile.writelines(sentenceList)


def write_file(txt, written_file):
    with open(written_file, 'w+') as file:
        file.writelines(txt)
        file.close()


    with open(written_file) as file:
        txt = file.readlines()

        s = [i.strip('– –').strip('-') for i in txt]
        s = [i.strip() for i in s]
        s = [x.strip() for x in s if x.strip() != '']

    with open(written_file, 'w+') as file:
        write_file = []
        for i in s:
            write_file.append(i + '\n')
        file.writelines(write_file)
        file.close()


def deleteBySize(name, minSize):
    """delete all files which size < 15kb"""

    path_all = '/Users/xinsun/Desktop/Audio_Transcripts/2. test_preprocess/'

    files = os.listdir(path_all)  # 列出目录下的文件
    for i in files:
        if i != '.DS_Store':
            path_book = path_all + i + '/transcripts/'
            print('path_book',path_book)

            chapter_list = os.listdir(path_book)
            chapter_list.remove('.DS_Store')
            print('chapter_list', chapter_list)

            if ('processed_not_insentence' or 'processed_insentence') in chapter_list:
                dirname = os.listdir(path_book + name)
                #print('chapter_list', chapter_list)
                #print(len(chapter_list))

                for file_name in dirname:
                    file = path_book + name + file_name

                    if os.path.getsize(file) < minSize:
                        os.remove(file)  # 删除文件
                        print(file_name + ": deleted")

            elif ('processed_not_insentence' and 'processed_insentence') not in chapter_list:
                for i in chapter_list:
                    path_transcripts = path_book + i + '/' + name
                    print('path_transcripts', path_transcripts)
                    dirname = os.listdir(path_transcripts)
                    #dirname.remove('.DS_Store')
                    #print(dirname)

                    for file_name in dirname:
                        file = path_transcripts + file_name

                        if os.path.getsize(file) < minSize:
                            os.remove(file)  # 删除文件
                            print(file_name + ": deleted")

    return



'''
if __name__ == '__main__':

    file = '/Users/xinsun/Desktop/Audio_Transcripts/1.Completed/120.verwandlung_mw_0811_librivox_64kb_mp3/transcripts/III.txt'

    written_file = "/Users/xinsun/PycharmProjects/PycharmEnv/venv/III_pre_prossed.txt"


    content_without_non_character = move_noise(file)
    #print(content_without_non_character)
    split_sent(content_without_non_character, written_file)
'''



#path_all = '/Users/xinsun/Desktop/Audio_Transcripts/2. test_preprocess/'
path_all = '/Users/xinsun/Desktop/Audio-Text-alignments-submitted/Transcripts/'
dirname_audiofiles = os.listdir(path_all)
print(len(dirname_audiofiles))

for i in dirname_audiofiles:
    if i != '.DS_Store':
        path_transcripts = path_all + str(i) + '/transcripts/'
        #print(path_transcripts)

        dirname = os.listdir(path_transcripts)
        #print(dirname)
        #print(len(dirname))

        dirname_transcripts = []
        for k in dirname:
            if k != '.DS_Store' and k != 'pre_processed' and k != 'own_preprocess' and k != 'spacy_preprocess' and k != 'nltk_preprocess' and k != 'processed_insentence' and k != 'processed_not_insentence' and k != 'for_alignments':
                dirname_transcripts.append(k)
        #print(dirname_transcripts)


        if dirname_transcripts[0][-4:-1] == '.tx':
            for j in dirname_transcripts:
                load_file = path_transcripts + str(j)
                print(load_file)

                written_file = path_transcripts + 'processed_not_insentence/' + 'PNS-' + str(j)
                print(written_file)

                content_without_non_character = move_noise(load_file)
                #content_without_non_character = NLTK_splitSentence_write(content_without_non_character, written_file)
                write_file(content_without_non_character, written_file)
                deleteBySize('processed_not_insentence/', 20)


        else:
            for i in dirname_transcripts:
                path_transcripts_second_layer = path_transcripts + i

                dirname = os.listdir(path_transcripts_second_layer)

                dirname_transcripts_second_layer = []
                for k in dirname:
                    # print(k)
                    if k != '.DS_Store' and k != 'pre_processed' and k != 'own_preprocess' and k != 'spacy_preprocess' and k != 'nltk_preprocess' and k != 'processed_insentence' and k != 'processed_not_insentence' and k != 'for_alignments':
                        dirname_transcripts_second_layer.append(k)

                for j in dirname_transcripts_second_layer:
                    load_file = path_transcripts_second_layer + '/' + str(j)
                    print(load_file)


                    written_file = path_transcripts_second_layer + '/' + 'processed_not_insentence/' + 'PNS-' + str(j)
                    print(written_file)

                    content_without_non_character = move_noise(load_file)
                    #content_without_non_character = NLTK_splitSentence_write(content_without_non_character, written_file)
                    write_file(content_without_non_character, written_file)
                    deleteBySize('processed_not_insentence/', 20)


