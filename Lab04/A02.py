import pandas as pd
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

SEED = 42


def main():
    df = pd.read_csv("dataset.csv")
    df_red = pd.read_csv("reduced_dataset.csv")

    print(f"shape dataset:\t\t{df.shape}")
    print(f"shape dataset reduced:\t{df_red.shape}")

    # Split in features and label
    X, y = df[df.columns[1:]], df[df.columns[0]]
    X_red, y_red = df_red[df_red.columns[1:]], df_red[df_red.columns[0]]

    # 1. Split in train and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )
    X_train_red, X_test_red, y_train_red, y_test_red = train_test_split(
        X_red, y_red, test_size=0.2, random_state=SEED
    )

    # 2. Standardize
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_train_red = scaler.fit_transform(X_train_red)
    X_test_red = scaler.transform(X_test_red)

    # 3. Dimensionality reduction on non-reduced dataset
    pca = PCA(n_components=80)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    # 4. Train KNN
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train_pca, y_train)

    # 5. Test KNN
    y_pred = knn.predict(X_test_pca)

    # 6. Implement performance metrics
    tp = sum((y_test == "Luminal A    ") & (y_pred == "Luminal A    "))
    fp = sum((y_test == "Luminal B    ") & (y_pred == "Luminal A    "))
    fn = sum((y_test == "Luminal A    ") & (y_pred == "Luminal B    "))

    accuracy = (y_pred == y_test).mean()
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * precision * recall / (precision + recall)
    print(
        f"\n*** scores by hand ***\naccuracy:\t{accuracy}\n"
        f"precision:\t{precision}\nrecall:\t\t{recall}\nf1_score:\t{f1_score}"
    )

    # 6. Use scikit-learn metrics
    accuracy_sklearn = metrics.accuracy_score(y_test, y_pred)
    precision_sklearn = metrics.precision_score(
        y_test, y_pred, pos_label="Luminal A    "
    )
    recall_sklearn = metrics.recall_score(
        y_test, y_pred, pos_label="Luminal A    "
    )
    f1_score_sklearn = metrics.f1_score(
        y_test, y_pred, pos_label="Luminal A    "
    )
    print(
        f"\n*** scikit-learn scores ***\naccuracy:\t{accuracy_sklearn}"
        f"\nprecision:\t{precision_sklearn}\nrecall:\t\t{recall_sklearn}"
        f"\nf1_score:\t{f1_score_sklearn}"
    )

    # 7. Train and test KNN onto reduced dataset
    knn.fit(X_train_red, y_train_red)
    y_pred_red = knn.predict(X_test_red)

    # 8. Compare performances
    accuracy_sklearn = metrics.accuracy_score(y_test_red, y_pred_red)
    precision_sklearn = metrics.precision_score(
        y_test_red, y_pred_red, pos_label="Luminal A    "
    )
    recall_sklearn = metrics.recall_score(
        y_test_red, y_pred_red, pos_label="Luminal A    "
    )
    f1_score_sklearn = metrics.f1_score(
        y_test_red, y_pred_red, pos_label="Luminal A    "
    )
    print(
        f"\n*** scikit-learn scores (reduced) ***\n"
        f"accuracy:\t{accuracy_sklearn}"
        f"\nprecision:\t{precision_sklearn}\nrecall:\t\t{recall_sklearn}"
        f"\nf1_score:\t{f1_score_sklearn}\n"
    )

    # 9. Train and test SVM, Random Forest, NB
    models = [
        ("SVM", SVC()),
        ("RF", RandomForestClassifier()),
        ("GNB", GaussianNB()),
    ]
    results = {
        "Model": [],
        "Accuracy": [],
        "Precision": [],
        "Recall": [],
        "F1_score": [],
    }

    for name, model in models:
        model.fit(X_train_red, y_train_red)
        y_pred = model.predict(X_test_red)

        results["Model"].append(name)
        results["Accuracy"].append(metrics.accuracy_score(y_test, y_pred))
        results["Precision"].append(
            metrics.precision_score(y_test, y_pred, pos_label="Luminal A    ")
        )
        results["Recall"].append(
            metrics.recall_score(y_test, y_pred, pos_label="Luminal A    ")
        )
        results["F1_score"].append(
            metrics.f1_score(y_test, y_pred, pos_label="Luminal A    ")
        )

    # 10. Compare results
    print(pd.DataFrame(results))


if __name__ == "__main__":
    main()
