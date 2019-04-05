import json
import re
import spacy
import heapq
import jsonpickle

def parse_data(name):
    regex = re.compile('([a-zA-Z]\"[a-zA-Z])', re.S)
    file_name = name + "_output.txt"
    output_file = name + "_parsed.txt"
    counter = 0
    with open(output_file, 'w') as outfile:
        with open(file_name, 'r') as inf:
            for tweet in inf:
                sentence_temp = re.sub(r'b\'RT ', "", tweet.rstrip())
                sentence_temp_2 = re.sub('b\'', "", sentence_temp)
                sentence_temp_3 = re.sub('\\\\\w*', "", sentence_temp_2)
                sentence_temp_4 = re.sub('b\"\@\w*', "", sentence_temp_3)
                sentence_temp_5 = re.sub('\@\w*', "", sentence_temp_4)
                sentence_temp_6 = re.sub('b\"', "", sentence_temp_5)
                sentence_temp_7 = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "", sentence_temp_6)
                sentence_temp_8 = re.sub(r'\\', "", sentence_temp_7)
                sentence_temp_9 = re.sub('\"+', "", sentence_temp_8)
                sentence = re.sub("RT", "", sentence_temp_9)
                counter += 1
                outfile.write(jsonpickle.encode(sentence, unpicklable=False) +
                                '\n')

        print("finished parsing %d tweets" % (counter))
        # outs = open(output_file, 'w')
        # for tweet in tweets:
        #     outs.write(sentence)

        #tweet = json.loads(line)
        #print(json.dumps(tweet, indent=4))

def analyze(name):
    data = []
    file_name = name + "_parsed.txt"
    tweets = ""

    with open(file_name, 'r') as ins:
        counter = 0
        for tweet in ins:
            if(counter == 3000):
                data.append(tweets)
                counter = 0
                tweets = ""
            tweets += tweet
            counter += 1

    adjective_count = {}
    for tweets in data:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(tweets)
        adj = [token.text for token in doc if token.is_stop != True and token.is_punct != True and token.pos_ == "ADJ"]
        for text in adj:
            text_lower = text.lower()
            if name not in text_lower:
                if text_lower in adjective_count.keys():
                    adjective_count[text_lower] += 1
                else:
                    adjective_count[text_lower] = 1

    priority_queue = []
    for key, val in adjective_count.items():
        heapq.heappush(priority_queue, (val, key))
    return heapq.nlargest(20, priority_queue)

def main():
    name = input("which document do you want to analyze?")
    parse_data(name)
    print(analyze(name))


if __name__ == '__main__':
    main()