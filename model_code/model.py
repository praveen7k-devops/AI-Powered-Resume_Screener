import pandas as pd
from pycaret.classification import *

#1. Import the data set
data = pd.read_csv('ai_resume_screening.csv')
print(data)

s = setup(data, session_id=1101, target='shortlisted', normalize=True, normalize_method='minmax')
print(s)

# top_3 = compare_models()
# print(top_3)

#stacking gives better performance than blending
#best = stack_models(top_3)
best = compare_models()
print(best)

#plot_model(best, plot='feature')
#evaluate_model(best)

# save model
save_model(best, 'ai_resume_screener_model')
#create_api(best, api_name='ai_resume_screener')

#create_docker('ai_resume_screener')

#fine tune the model for hyperparameter tuning to optimize the model performance targeting n_estimators, learning_rate, and max_depth
#tuned_gbc = tune_model(gbc, optimize='AUC', n_iter=5)

# Step 3: Calibrate the model for reliable probability predictions
#calibrated_gbc = calibrate_model(tuned_gbc)