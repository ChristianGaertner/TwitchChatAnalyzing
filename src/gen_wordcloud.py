import sys
from wordcloud import WordCloud

text = sys.stdin.read()

# Generate a word cloud image
wc = WordCloud(width=1920, height=1080, font_path='/Library/Fonts/Verdana.ttf', max_font_size=500, relative_scaling=.5)\
    .generate(text)

wc.to_file(sys.argv[1])