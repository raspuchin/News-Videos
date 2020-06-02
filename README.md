# News-Videos
By entering a headline and article text (ideally summarized) the program will generate a video that speaks out the text with relevant pictures in the background

# How to use
Install requirements (duh), place chromedriver for selenium wherever it needs to be on your system
you also need to have ffmpeg on your command line, for ubuntu you can use 'sudo apt install ffmpeg' to download it
In the working directory make a folder called 'images' and another called 'outputs'
Inside outputs create another folder called 'singles'
In the main directory create another folder called 'temp' and inside that create folders called 'audio', 'images' and 'video'

Now enter all paths inside the files:
GettingImages : Enter selenium path and images folder path
VideoMaker : Change all forward slashes to double back slashes if you are on windows else leave it

In Run.py you can now enter in the headline and the text in head and summ and you can run
it should spit out the result in outputs/singles. The file will be named <your-heading>.mp4
  

# Explaing those scripts

## KeywordExtraction.py
I'm not gonna explain it here
Basically trained a CountVectorizer, TF-IDF Transformer and found a bunch of stopwords using this article : https://www.freecodecamp.org/news/how-to-extract-keywords-from-text-with-tf-idf-and-pythons-scikit-learn-b2a0f3d7e667/
I saved those objects, I load them up to use here
I did use the entire CNN-DM dataset to train this corpus but it doesn't behave like I expect it to but I've included vector.pickel in case you wanna play with it
The functions that we care about are:
1. load()
  loads the variables from the files
2. getKeywordList()
  Finds the keywords in the articles and ensures non repeating ones are passed on
  to explain: using tf-idf, say, I got the following keywords : airtel, jio, alex, jeffords, alex jeffords
  it would return : airtel, jio, alex jeffords
  this is not a perfect method as it can find wierd strings as keywords that dont do well in google images
  also I noticed that the word 'however' counted as a keyword one time so it might need fixing up a little


## GettingImages.py

GettingImages has 3 functions defined:
1. gettingImagesFromGoogle(keywords)
  this expects a list of strings containing keywords in lower case letters (it doesn't affect this function if they are in upper case but   you'll see why later on) 
  so for this example keywords = ['banana split', 'chicken']
  using a selenium instance we will download 5 images for each of the keyword sets and store them as banana_split1.jpg, etc
  I download the images displayed on google itself so they are of bad quality, I tried a few other techniques but none worked for me, theres one with opencv that I am yet to try
2. checkIfImageExists(keyword)
  This function just expects a string as an input and returns true or false based on if images exist based on the keyword (this is why   lower case letters as formatting is easy)
3. getImage(keywords)
  expects a list of strings in the same format as gettingImagesFromGoogle
  if imageExists for a keyword then no new images are gotten for it (a kind of caching if you will)
  if no imageExists then use selenium and do its job

## VideoMaker.py

Probably the easiest to explain
The functions defined are as follows:
1. clear_temp()
  deletes all the files in all the temp folders
2. get_speech(summary)
  summary is the article text, uses google text to speech to get an audio file of the same
3. get_images(keywords)
  gets a picture for each keyword, picture for the keyword is chosen at random using randint(1,5) 
  all files are stored as temp-<num>.jpg as ffmpeg will require that we use this
4. get_video()
  gets a video without any audio using all pictures as frames (framerate is set to 1)
  saved as output.mp4
5. makevideo(summary, keywords, heading)
  calls functions numbered 2,3 and 4
  adds the audio to the video, video is looped over and over to fit the audios time and saved as uncut.mp4
  the uncut.mp4 is usually much longer than it needs to be so we cut it and store it as <heading>.mp4 in outputs/singles/
  
## Run.py

I was lying
This is the easiest to explain
the function run() takes in article text as summ and headline as head
it then runs getKeywords(), getImage() and then makeVideo(), it then finally deletes everything in the temp folders to keep it clean


# Issues
1. GettingImages.py : 
a. Selenium is too slow
b. Pictures are too low res and very ugly
2. KeywordExtraction.py :
a. Non-keywords like 'however' are marked as keywords once in a while
b. Removing duplicate keywords from the list make for bad image queries
3. VideoMaker.py
a. Absolutely no idea how ffmpeg works (I mean some idea but nowhere near acceptable)
b. gTTS voice needs to be better
c. Images are displayed in loop so thats useless, make properly formatted videos

# To-Do (LOL)
1. outputs/proper/ folder to hold multiple articles worth of video in one video
2. to 'proper' add stock features, format the image to one side of the frame to use the rest of it to display better
3. add subtitles
