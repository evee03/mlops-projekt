import optuna
print(optuna.__version__)

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier

# Wczytanie zbioru danych i podzial 80/20 z zachowaniem proporcji klas
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Model bazowy z domyslnymi hiperparametrami
baseline = RandomForestClassifier(random_state=42)
baseline_cv = cross_val_score(baseline, X_train, y_train, cv=5, scoring="accuracy")
print(f"Baseline, dokladnosc CV: {baseline_cv.mean():.4f} (odch. std. {baseline_cv.std():.4f})")

# Trening na calym zbiorze treningowym i ocena na zbiorze testowym
baseline.fit(X_train, y_train)
baseline_test_acc = baseline.score(X_test, y_test)
print(f"Baseline, dokladnosc na zbiorze testowym: {baseline_test_acc:.4f}")

import optuna

def objective(trial):
    # Definicja przestrzeni przeszukiwania
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 400),
        "max_depth": trial.suggest_int("max_depth", 2, 20),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20)
    }
    # Budowa i ocena modelu
    model = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").mean()
    return score

# Utworzenie badania i uruchomienie optymalizacji
study = optuna.create_study(direction="maximize", study_name="rf_tuning")
study.optimize(objective, n_trials=50)

print("Najlepsza wartosc funkcji celu (dokladnosc CV):", study.best_value)
print("Najlepsza konfiguracja hiperparametrow:", study.best_params)


best_model = RandomForestClassifier(**study.best_params, random_state=42, n_jobs=-1)
best_model.fit(X_train, y_train)
tuned_test_acc = best_model.score(X_test, y_test)

print(f"Model strojony, dokladnosc na zbiorze testowym: {tuned_test_acc:.4f}")
print(f"Model bazowy, dokladnosc na zbiorze testowym: {baseline_test_acc:.4f}")