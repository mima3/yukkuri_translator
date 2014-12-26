#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MeCab
import jctconv
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8') (sys.stdout)


connect_o = [
    '花',
    '帽子',
    '歌',
    '空'
]

converter = {
    '食べる' : 'むーしゃむーしゃする',
    '食べ' : 'むーしゃむーしゃし',
    '寝る' : 'すーやすーやする',
    '眠る' : 'すーやすーやする',
    '寝' : 'すーやすーやし',
    '眠' : 'すーやすーやし',
    '糞' : 'うんうん',
    '大便' : 'うんうん',
    '便' : 'うんうん',
    '尿' : 'しーしー',
    '小便' : 'しーしー',
    '太陽' : 'おひさま',
    '制裁' : 'せいっさい',
    '菓子' : 'あまあま',
    '飴' : 'あまあま',
    '砂糖' : 'あまあま',
    'ジュース' : 'あまあま',
    'コーディネート' : 'こーでぃねーと',
    'セックス' : 'すっきり',
    '妊娠' : 'にんっしんっ'
}



class MarisaTranslator:
    def __init__(self, user_dic):
        self.mecab = MeCab.Tagger("-u " + user_dic)

    def _check_san(self, n):
        """
        「さん」をつけるかどうかの判定
        """
        f = n.feature.split(',')
        if f[0] == '名詞':
            if f[1] == '固有名詞' or f[1] == '一般':
                if n.next:
                    # 次の単語のチェック
                    nf = n.next.feature.split(',')
                    if nf[0] in ['名詞', '助動詞']:
                        # 名詞が続く場合は、ここでは「さん」をつけない
                        return False
                    else:
                        if n.surface.endswith('さん'):  # さんでおわる場合は付与しない
                            return False
                        if n.surface == '様' or n.surface == 'さま':  # 様でおわる場合は付与しない
                            return False
                        return True
                else:
                    return True
        return False


    def _check_separator(self, n):
        """
        「、」をつけるかどうかの判定
        """
        f = n.feature.split(',')
        if f[0] == '助詞':
            if n.next:
                # 次の単語のチェック
                nf = n.next.feature.split(',')
                if nf[0] in ['記号', '助詞']:
                    return False
                return True
        return False


    def _get_gobi(self, n):
        if n.next:
            f_next = n.next.feature.split(',')
            if n.next.surface == '、':
                return None
            if f_next[0] == 'BOS/EOS' or f_next[0] == '記号':
                f = n.feature.split(',')
                if f[0] in ['助詞', '名詞', '記号', '感動詞']:
                    return None
                if f[5] in ['命令ｅ', '連用形']:
                    return None
                if n.surface in ['だ']:
                    return 'なのぜ'
                else:
                    return n.surface + 'のぜ'
        return None

    def translate(self, src):
        n = self.mecab.parseToNode(src)
        text = ''
        pre_node = None
        while n:
            f = n.feature.split(',')
            if n.surface in converter:
                text += converter[n.surface]
            elif len(f) > 8:
                gobi = self._get_gobi(n)
                if gobi is not None:
                    text += gobi
                elif f[8] != '*':
                    text += f[8]
                else:
                    text += n.surface
            else:
                text += n.surface
            if self._check_san(n):
                text += 'さん'
            elif self._check_separator(n):
                text += '、'
            n = n.next
            pre_node = n
        return jctconv.kata2hira(text.decode('utf-8')).encode('utf-8')
