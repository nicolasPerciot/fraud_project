# Le bon

class node_bean:
    def __init__ (self, clt, id=0, depth=0) :

        self.__clt = clt
        self.__features_name = dict()
        for i, name in enumerate(list(clt.feature_names_in_)):
            self.__features_name[i] = name
        self.__features_name[-2] = 'isFraud'

        self.__n_nodes = clt.tree_.node_count
        self.__children_left = clt.tree_.children_left
        self.__children_right = clt.tree_.children_right
        self.__features = clt.tree_.feature
        self.__threshold = clt.tree_.threshold
        self.features_user = dict()

        self.parent = 0
        self.id = id
        self.depth = depth
        self.seuil = self.__threshold[id]
        self.ch_l = self.__children_left[id]
        self.ch_r = self.__children_right[id]
        self.feature = self.__features[id]
        self.feature_name = self.__features_name[self.__features[id]]
    
    def reponse(self, value):
        if value <= self.parent.seuil:
            return False # Non fraud
        else :
            return True # Fraud
    
    def set_self(self, id, depth) :
        self.parent = node_bean(self.__clt, self.id, self.depth)
        self.id = id
        self.depth = depth
        self.seuil = self.__threshold[id]
        self.ch_l = self.__children_left[id]
        self.ch_r = self.__children_right[id]
        self.feature = self.__features[id]
        self.feature_name = self.__features_name[self.__features[id]]
        
    def node_next(self, value=""):
        if value != "":
            if not self.feature in self.features_user :
                self.features_user[self.feature] = value
            if value <= self.seuil :
                self.set_self(self.ch_l, (self.depth + 1))
            else :
                self.set_self(self.ch_r, (self.depth + 1))

            if self.feature in self.features_user :
                value = self.features_user[self.feature]
                self.node_next(value)
                
            if self.ch_l == self.ch_r or self.feature == -2:
                return self.reponse(value)

        return self.feature_name