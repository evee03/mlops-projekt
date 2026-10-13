import optuna
from optuna.trial import TrialState
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

# 1. Wczytanie i podstawowy podzial danych[cite: 20]
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Wydzielenie zbioru walidacyjnego z czesci treningowej[cite: 24]
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train, y_train, test_size=0.25, random_state=42, stratify=y_train
)

# 3. Funkcja celu z przycinaniem[cite: 24]
def objective_pruning(trial):
    params = {
        "n_estimators": 300, # Celowo duza, stala liczba etapow[cite: 25]
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
        "max_depth": trial.suggest_int("max_depth", 2, 8),
    }
    
    model = GradientBoostingClassifier(**params, random_state=42)
    model.fit(X_tr, y_tr)

    # Ocena modelu etapami, po kolejnych drzewach[cite: 25]
    for step, y_pred in enumerate(model.staged_predict(X_val)):
        acc = accuracy_score(y_val, y_pred)
        
        # Raportowanie wyniku posredniego[cite: 25]
        trial.report(acc, step)
        
        # Sprawdzenie decyzji prunera i ewentualne przerwanie proby[cite: 25]
        if trial.should_prune():
            raise optuna.TrialPruned()
            
    return acc

# 4. Utworzenie badania i uruchomienie optymalizacji[cite: 25]
study_pruned = optuna.create_study(
    direction="maximize",
    pruner=optuna.pruners.MedianPruner(
        n_startup_trials=5, # pierwsze piec prob nigdy nie jest przycinanych[cite: 25]
        n_warmup_steps=20,  # zadna proba nie jest przycinana przed dwudziestym krokiem[cite: 25]
    ),
)

study_pruned.optimize(objective_pruning, n_trials=40)

# 5. Zestawienie liczby prob ukonczonych i przycietych[cite: 26]
pruned = [t for t in study_pruned.trials if t.state == TrialState.PRUNED]
complete = [t for t in study_pruned.trials if t.state == TrialState.COMPLETE]

print(f"Proby ukonczone: {len(complete)}, proby przyciete: {len(pruned)}")

from optuna.visualization import plot_optimization_history, plot_param_importances

# Historia optymalizacji
fig1 = plot_optimization_history(study_pruned)
fig1.show()

# Waznosc hiperparametrow[cite: 26]
fig2 = plot_param_importances(study_pruned)
fig2.show()