

class ScoreEngine():

    def __init__(self, score_net, static_weights, use_net):
        self.score_net = score_net
        self.static_weights = static_weights
        self.use_net = use_net

    def get_overall_score(self, stat_techniques, key):
        overall_score = 0
        explanation = ""
        if self.use_net == True and self.score_net is not None:
            #Implement in the future
            pass

        #Use simple static weights
        elif self.static_weights is not None:
            for stat_technique in stat_techniques:
                if self.static_weights[stat_technique.get_name()] is not None:
                    overall_score += stat_technique.get_scores()[key]  * self.static_weights[stat_technique.get_name()]
                    if (stat_technique.get_scores()[key] > (self.static_weights[stat_technique.get_name()] / 2)):
                        explanation += stat_technique.get_name() + ", "
        return [overall_score, explanation[0:len(explanation)-2]]

