#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 上午11:15
# @Author  : Aries
# @Site    : 
# @File    : advice.py.py
# @Software: PyCharm Community Edition


class Advices(object):

    def __init__(self):
        self.message = []

    def spasi_message(self, spasi_score):
        message = "您目前的银屑病病情属于"
        if spasi_score == 0:
            message = "您目前没有银屑病皮损。"
        elif 1 <= spasi_score <= 7:
            message = message + "轻度。"
        elif 8 <= spasi_score <= 14:
            message = message + "中度。"
        elif 15 <= spasi_score <= 72:
            message = message + "重度。"
        else:
            message = ""
        self.append_message(message)

    def qol_message(self, qol_score):
        message = "您的病情对您%s影响。"
        if qol_score == 0:
            message = message % '没有'
        elif qol_score == 1:
            message = message % '轻微的'
        elif qol_score == 2:
            message = message % '相当程度'
        elif qol_score == 3:
            message = message % '十分严重'
        elif qol_score == 4:
            message = message % '极度严重'
        else:
            message = ''
        self.append_message(message)

    def qol_sapasi_message(self, qol_score, spasi_score):
        qsm = SapasiQolMessage()
        taget = getattr(qsm, 'qol_' + str(qol_score), qsm.qol_not_match())
        taget(spasi_score)
        self.message = self.message + qsm.message

    def pest_message(self, pest_score):
        if 0 <= pest_score <= 1:
            message = '您目前患银屑病关节炎的可能性较小，请继续注意关节症状。'
        elif pest_score >= 2:
            message = '您目前患银屑病性关节炎的可能性较大，建议您找专业医生进行诊治。'
        else:
            message = ''
        self.append_message(message)

    def pas_message(self, pas_score):
        if 0 < pas_score < 1:
            message = "您目前没有诊断银屑病性关节炎，且您未来8年内患关节炎风险不大。"
        elif pas_score >= 1:
            message = "您未来患银屑病性关节炎的风险是常人的%s倍。请注意对风险因素的防控。" % str(pas_score)
        else:
            message = ''
        self.append_message(message)

    def append_message(self, message):
        if message:
            self.message.append(message)


class SapasiQolMessage(object):

    def __init__(self):
        self.message = []

    def qol_0(self, sapai_score):
        if sapai_score == 0:
            message = "您不需要任何治疗。"
        elif 1 <= sapai_score <= 7:
            message = "建议您适当的治疗疾病。"
        elif 8 <= sapai_score <= 14:
            message = "建议您积极的治疗疾病。"
        elif 15 <= sapai_score <= 72:
            message = "建议您十分积极的治疗疾病。"
        else:
            message = ""
        self.append_message(message)

    def append_message(self, message):
        if message:
            self.message.append(message)

    def qol_1(self, sapai_score):
        if sapai_score == 0:
            message = "您不需要任何治疗。"
        elif 1 <= sapai_score <= 7:
            message = "建议您适当的治疗疾病。"
        elif 8 <= sapai_score <= 14:
            message = "建议您积极的治疗疾病。"
        elif 15 <= sapai_score <= 72:
            message = "建议您十分积极的治疗疾病。"
        else:
            message = ""
        self.append_message(message)

    def qol_2(self, sapai_score):
        if sapai_score == 0:
            message = "您不需要治疗，但可能需要注意一下疾病对您心理造成的负担。"
        elif 1 <= sapai_score <= 7:
            message = "您需要适当的治疗疾病。也可能需要注意一下疾病对您心理造成的负担。"
        elif 8 <= sapai_score <= 14:
            message = "您需要积极的治疗疾病。也需要注意一下疾病对您心理造成的负担。"
        elif 15 <= sapai_score <= 72:
            message = "您需要十分积极的治疗疾病。也需要注意一下疾病对您心理造成的负担。"
        else:
            message = ""
        self.append_message(message)

    def qol_3(self, sapai_score):
        if sapai_score == 0:
            message = "您不需要治疗，但您可能对您的疾病担心过度了，请多了解银屑病，必要时找医生咨询一下。"
        elif 1 <= sapai_score <= 7:
            message = "您需要适当的治疗疾病。同时可以找医生谈一下疾病对您的心理影响。"
        elif 8 <= sapai_score <= 14:
            message = "您需要积极的治疗疾病。同时可以找医生谈一下疾病对您的心理影响。"
        elif 15 <= sapai_score <= 72:
            message = "您需要十分积极的治疗疾病。同时可以找医生谈一下疾病对您的心理影响。"
        else:
            message = ""
        self.append_message(message)

    def qol_4(self, sapai_score):
        if sapai_score == 0:
            message = "您不需要治疗，但疾病可能给您带来了太大的精神困扰，您可能需要心理/精神专业医师的帮助。"
        elif 1 <= sapai_score <= 7:
            message = "您需要适当的治疗疾病。疾病可能给您带来了太大的精神困扰，您可能需要心理/精神专业医师的帮助。"
        elif 8 <= sapai_score <= 14:
            message = "您需要积极的治疗疾病。您可能还需要心理/精神专业医师的帮助。"
        elif 15 <= sapai_score <= 72:
            message = "您需要十分积极的治疗疾病。您可能还需要心理/精神专业医师的帮助。"
        else:
            message = ""
        self.append_message(message)

    def qol_not_match(self, sapai_score=0):
        pass


if __name__ == '__main__':
    ac = Advices()
    ac.pas_message(1)
    ac.qol_message(3)
    ac.qol_sapasi_message(3, 5)
    ac.pest_message(6)
    ac.pas_message(9)
    print(ac.message)