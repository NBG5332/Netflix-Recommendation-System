import pandas as pd
from flask import Flask, render_template,request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_data(x):
    return str.lower(x.replace(" ", ""))

def create_soup(x):
    return x['title']+ ' ' + x['director'] + ' ' + x['cast'] + ' ' +x['listed_in']+' '+ x['description']
'''
def get_recommendations(title, cosine_sim):
    global result
    title=title.replace(' ','').lower()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    result =  netflix_overall['title'].iloc[movie_indices]
    result = result.to_frame()
    result = result.reset_index()
    del result['index']
    return result
'''

global p, result,test
def get_recommendations_new(titles,cosine_sim):

        try:
            titles=titles.replace(' ','').lower()
            idx = indices[titles] #from this we well get the index of that title in the data set.


            #age_rating = netflix_data['rating'][idx] #from this we get movie rating for age restriction
            #age_req = age_dict[age_rating]

            #if(age_req <= user_age): # comparies user age to required age to watch movie

                # Get the pairwsie similarity scores of all movies with that movie
            sim_scores = list(enumerate(cosine_sim[idx]))

            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the scores of the 10 most similar movies
            sim_scores = sim_scores[1:11]

            # Get the movie indices
            movie_indices = [i[0] for i in sim_scores]
                # Return the top 10 most similar movies
            print("These are Recommended movies based upon your last watch")
            result = netflix_data['title'].iloc[movie_indices]
            #else:
            #    p = print('Your age should be: ',age_req,' but your age is: ', user_age," try with other movies")

            print('this is try loop')
            del result['index']
            test = 0
            print(type(result))
            return  result,test

        except KeyError:
            result_1 = []
            words = [titles]
            global i
            i = 0
            print('this is except loop')
            def check_all(sentence, ws):
                return all(w in sentence for w in ws)

            for sentence in x:
                if any(check_all(sentence.lower(), word.split(' ')) for word in words):
                    print(sentence)
                    result_1.append(sentence)
                    i = 1
            result_1 = pd.DataFrame (result_1, columns = ['Titles'])
            if i>0:
                print("\n","your title matches to these movie name, you can try these suggestions\n")
            else:
                print("entered movie is not at updated or Spelling mistake happened")
            test = 1
            print(type(result_1))
            return result_1,test
netflix_overall = pd.read_csv('netflix_titles.csv')
netflix_data = pd.read_csv('netflix_titles.csv')
netflix_data = netflix_data.fillna('')

x=[]
for i in netflix_overall.title :
    x.append(i)

new_features = ['title', 'director', 'cast', 'listed_in', 'description']
netflix_data = netflix_data[new_features]
for new_features in new_features:
    netflix_data[new_features] = netflix_data[new_features].apply(clean_data)
netflix_data['soup'] = netflix_data.apply(create_soup, axis=1)
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(netflix_data['soup'])
global cosine_sim2

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
netflix_data=netflix_data.reset_index()
indices = pd.Series(netflix_data.index, index=netflix_data['title'])
#get_recommendations('PK', cosine_sim2)



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about',methods=['POST'])
def getvalue():
    moviename = request.form['moviename']
    result , test = get_recommendations_new(moviename,cosine_sim2)
    df=result
    if(test == 0):
        print('corrdct')
    if(test == 1):
        print('wrong')
    print(len(result))
    #d = j
    print("this sfjl;djgkdjzfnkldjbsjlkdzbvkllvjndkzjfvbadfvlkdzvabdfvz",type(df), test)
    #print(get_recommendations_new(moviename,cosine_sim2))
    if (len(result) == 10):
        return render_template('result.html',  tables=[df.to_html(classes='data')] , titles=df.columns.values)
    if (len(result) >10 | len(df) <10) :
        return render_template('result_1.html',  tables=[df.to_html(classes='data')] , titles=df.columns.values)

    #except KeyError: return render_template('index_1.html')
if __name__ == '__main__':
    app.run(debug=False)
