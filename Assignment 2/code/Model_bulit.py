# ============================================
# FIFA 1930–2022 | Logistic Regression & Random Forest (VS Code Final)
# ============================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# ---------- Step 1: Check working directory ----------
print("Current working folder:", os.getcwd())
print("Files here:", os.listdir())

# ---------- Step 2: Load dataset ----------
file_path = "fifa_data.csv"      # rename your file to fifa_data.csv and keep in same folder
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"\nCSV file not found!\nExpected here:\n{os.path.join(os.getcwd(), file_path)}\n"
        "→ Move the CSV into this folder or update file_path with the full path."
    )

df = pd.read_csv(file_path)
df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

# ---------- Step 3: Prepare data ----------
required = ['home_team','away_team','home_team_goals','away_team_goals']
for c in required:
    if c not in df.columns:
        raise ValueError(f"Missing column: {c}")

df['result'] = np.where(df['home_team_goals']>df['away_team_goals'],2,
                np.where(df['home_team_goals']<df['away_team_goals'],0,1))

# ---------- Step 4: Compute team stats ----------
teams = sorted(set(df['home_team']).union(df['away_team']))
rows=[]
for t in teams:
    home=df[df.home_team==t]; away=df[df.away_team==t]
    n=len(home)+len(away)
    if n==0: continue
    scored=home.home_team_goals.sum()+away.away_team_goals.sum()
    conceded=home.away_team_goals.sum()+away.home_team_goals.sum()
    wins=len(home[home.home_team_goals>home.away_team_goals]) + len(away[away.away_team_goals>away.home_team_goals])
    rows.append({'team':t,'avg_scored':scored/n,'avg_conceded':conceded/n,'win_rate':wins/n})
team_stats=pd.DataFrame(rows).set_index('team')

# ---------- Step 5: Build features ----------
X,y=[],[]
for _,r in df.iterrows():
    if r.home_team in team_stats.index and r.away_team in team_stats.index:
        ht,at=team_stats.loc[r.home_team],team_stats.loc[r.away_team]
        X.append([ht.avg_scored,at.avg_scored,ht.avg_conceded,at.avg_conceded,ht.win_rate,at.win_rate])
        y.append(r.result)
X,y=np.array(X),np.array(y)

# ---------- Step 6: Split ----------
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

# ---------- Step 7: Train models ----------
scaler=StandardScaler()
X_train_s=scaler.fit_transform(X_train); X_test_s=scaler.transform(X_test)

lr=LogisticRegression(multi_class='multinomial',max_iter=1000,random_state=42)
lr.fit(X_train_s,y_train)

rf=RandomForestClassifier(n_estimators=200,random_state=42,class_weight='balanced')
rf.fit(X_train,y_train)

# ---------- Step 8: Evaluate ----------
y_pred_lr=lr.predict(X_test_s); y_pred_rf=rf.predict(X_test)
print("\nLogistic Regression Accuracy:",round(accuracy_score(y_test,y_pred_lr),3))
print("Random Forest Accuracy:",round(accuracy_score(y_test,y_pred_rf),3))

print("\nLR Report:\n",classification_report(y_test,y_pred_lr))
print("\nRF Report:\n",classification_report(y_test,y_pred_rf))

# ---------- Step 9: Confusion matrices ----------
fig,ax=plt.subplots(1,2,figsize=(12,5))
sns.heatmap(confusion_matrix(y_test,y_pred_lr),annot=True,fmt='d',cmap='Blues',ax=ax[0])
ax[0].set_title('Logistic Regression Confusion Matrix')
sns.heatmap(confusion_matrix(y_test,y_pred_rf),annot=True,fmt='d',cmap='Greens',ax=ax[1])
ax[1].set_title('Random Forest Confusion Matrix')
plt.tight_layout(); plt.show()

# ---------- Step 10: Save models ----------
joblib.dump(lr,'logistic_regression_model.pkl')
joblib.dump(rf,'random_forest_model.pkl')
print("\nSaved model files:", [f for f in os.listdir() if f.endswith('.pkl')])
