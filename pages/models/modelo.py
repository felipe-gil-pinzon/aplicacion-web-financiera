class Modelo:
    def __init__(self, modelo):
        self.modelo = modelo
        self.umbral = 0.11730232425863889
        self.prediccion = []

    def predict(self, X):
        self.prediccion = []
        y_pred = self.modelo.predict_proba(X)[:,1]
        for i in y_pred:
            if i >= self.umbral:
                self.prediccion.append(1)
            else:
                self.prediccion.append(0)
        return self.prediccion