import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 13})

models = [
    "CodeBert",
    "LineVul",
]
model_order = dict(zip(models, range(len(models))))

def getplot(df):
    df = df.replace({
    "buffer_overflow": "Buffer overflow",
    "input_validation": "Input validation error",
    "privilege_escalation_authorization": "Privilege escalation",
    "resource_allocation_free": "Resource error",
    "value_propagation_errors": "Value error",
    "mixed": "All bug types",
    })
    df["Model"] = df["Model"].apply(lambda x: f"{model_order[x]}{x}")
    df = df.sort_values(["Model", "training", "evaluation"]).reset_index()
    df = pd.concat((df, pd.DataFrame([{"Model": m, "training": "filler", "evaluation": "filler", "f1": float('-inf')} for m in df["Model"].unique()])))
    df = pd.concat((df, pd.DataFrame([{"Model": m, "training": "filler", "evaluation": "filler2", "f1": float('-inf')} for m in df["Model"].unique()])))

    df = df.sort_values(["Model", "training"]).reset_index(drop=True)
    df["index"] = df.index.to_series()

    sets = df["training"].dropna().drop_duplicates().sort_values().tolist()
    sets.remove("All bug types")
    sets.append("All bug types")
    sets.remove("filler")
    sets.append("filler")
    sets.append("filler2")
    palette = dict(zip(sets, sns.color_palette("tab10")))
    plt.figure(figsize=(12, 4), dpi=80)
    ax = plt.gca()
    df["model_training"] = df["Model"].str.cat(df["training"])
    sns.barplot(
        data=df[df["training"] == df["evaluation"]],
        x="model_training",
        y="f1",
        hue="training",
        palette=palette,
        linewidth=1,
        edgecolor="k",
        dodge=False,
        ax=ax,
    )
    sns.stripplot(
        data=df[(df["training"] != df["evaluation"]) & (df["evaluation"] != "All bug types")],
        x="model_training",
        y="f1",
        hue="evaluation",
        palette=palette,
        linewidth=1,
        edgecolor="k",
        ax=ax,
    )
    h, l = ax.get_legend_handles_labels()
    # print(h)
    # print(l)
    h, l = h[0:1]+h[-6:-1], l[0:1]+l[-6:-1]  # include only items from barplot legend
    # plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))  # on the right
    # plt.legend(loc="lower left", mode="expand", ncol=3, bbox_to_anchor=(0, 1.02, 1, 0.2))  # on top
    plt.legend(
        h,
        l,
        title="Bug type",
        # loc="lower left",
        # mode="expand",
        # ncol=2,
        # bbox_to_anchor=(0, 1.12, 1, 0.2),
        loc="center left",
        bbox_to_anchor=(1.04, 0.5),
    )

    plt.ylim((0, 100))
    plt.xlabel("Training dataset")
    plt.ylabel("$F_1$ on test dataset")


    labels = []
    labels.append("")
    models = df["Model"].dropna().drop_duplicates().sort_values().tolist()
    models = [m for m in models if m]
    for m in models:
        labels.append(m[1:])
        labels.append("")

    num_bars = len(df.drop_duplicates(["Model", "training"]))-1
    plt.xlim(-1, num_bars)
    plt.xticks(np.linspace(-1, num_bars, len(labels)), labels)
    plt.xlabel("Model")

    plt.tight_layout()
    plt.savefig(f"plot_bug_types.pdf")
    plt.show()
