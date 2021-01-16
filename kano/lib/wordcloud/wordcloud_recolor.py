from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager, rc
from matplotlib import colors as cols
from kano.engine.dao import DAO
rc('font',family='malgun gothic')


class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

class Wordcloud_recolor:
    def __init__(self,word_dict,wc):
        self.word_dict = word_dict
        self.wc = wc

    def recolor_kbf(self):
        patches = None
        color_list = ['royalblue','seagreen','darkred','orange','purple','brown','pink','olive','peru','cyan','gold']
        self.default_color = 'grey'
        plt_info_list=[]
        self.color_to_words = {}
        dao = DAO()
        kbf_nouns = dao.select_kbf(11)
        for index,(kbf_key,word_list) in enumerate(kbf_nouns.items()):
            plt_info_list.append({"keyword":kbf_key,"color": cols.to_rgba(color_list[index])})
            self.color_to_words[color_list[index]] = word_list
            patches = [mpatches.Patch(color=plt_info['color'], label="{}".format(plt_info['keyword'])) for plt_info in plt_info_list]


        # # Words that are not in any of the color_to_words values
        # # will be colored with a grey single color function
        # # Create a color function with single tone
        grouped_color_func = SimpleGroupedColorFunc(self.color_to_words, self.default_color)

        #
        # # Create a color function with multiple tones
        # # grouped_color_func = GroupedColorFunc(self.color_to_words, self.default_color)
        #
        # # Apply our color function
        self.wc.recolor(color_func=grouped_color_func)
        #
        return self.wc,patches


        # #legend
        # plt_info_list = [{'keyword':'헤어케어','color':cols.to_rgba('royalblue')},{'keyword':'건조속도','color':cols.to_rgba('seagreen')}]
        # patches = [mpatches.Patch(color=plt_info['color'], label="{}".format(plt_info['keyword']))
        #            for plt_info in
        #            plt_info_list]
        # # Plot
        # plt.figure()
        # plt.imshow(self.wc, interpolation="bilinear")
        # plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=30)
        # plt.axis("off")
        # plt.show()
        # plt.close()
