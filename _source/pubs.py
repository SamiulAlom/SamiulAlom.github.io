# Publication list for the portfolio. Source: Google Scholar profile read 2026-11-22; DOIs from Crossref
# (data/dois.json, data/dois2.json, title match >= 0.85). Unpublished and under-review work is excluded on purpose.
# fields: title, authors, venue, year, kind (j = journal, c = conference/proceedings), theme (health|vision|nlp),
#         first (Alom is first author), cites (Scholar, 2026-11-22), doi (or None), q (quartile note or "")

PUBS = [
 # journal articles
 ("Stroke Prediction Using Ensemble Machine and Deep Learning Models", "MS Alom, RK Halder, O Haque, SK Gain, MA Talukder, FS Tamim, et al.", "Biomedical Materials & Devices (Springer Nature)", 2025, "j", "health", True, 5, "10.1007/s44174-025-00521-z", "Q1"),
 ("An Explainable Triple-Layered Ensemble Model for Early Prediction of Suicide Risk Using Machine Learning", "MS Alom, MAH Tomal, R Taha, S Parvez, MA Layek, M Mohsin, MA Talukder", "Engineering Reports (Wiley) 8(1), e70574", 2026, "j", "health", True, 1, "10.1002/eng2.70574", "Q2"),
 ("A Novel Dataset of North-Eastern Indian Coins for Machine Learning-Based Classification", "I Al Mamoon, S Kabir, A Islam, G Moula, WH Laisa, A Sufian, et al., MS Alom, et al.", "Data in Brief (Elsevier), 112813", 2026, "j", "vision", False, 1, "10.1016/j.dib.2026.112813", "Q1"),
 ("SkinNet: Explainable Lightweight CNN Model for Skin Disease Classification", "MA Awal, A Rakin, MS Alom, SS Akhi, NH Shouvo, MI Ahamed, et al.", "Foundations of Computing and Decision Sciences 51(3), 337-376", 2026, "j", "vision", False, 0, "10.2478/fcds-2026-0011", "Q3"),
 ("An Explainable and Robust Machine Learning Approach for Autism Spectrum Disorder Prediction", "SS Akhi, MA Rahaman, MS Alom", "Frontiers in Health Informatics 13(8)", 2024, "j", "health", False, 0, "10.63682/fhi2758", ""),
 ("Early Stroke Risk Prediction Using Optimized Machine Learning Models and Balanced Clinical Data", "SS Akhi, MS Alom", "Journal of Computational Analysis & Applications 31(3)", 2023, "j", "health", False, 0, None, ""),
 # conference papers and proceedings
 ("Boosted Forest Soft Ensemble of XGBoost, Gradient Boosting, and Random Forest with Explainable AI for Thyroid Cancer Recurrence Prediction", "SS Akhi, MI Ahamed, MS Alom, A Rakin, A Awal, I Al Mamoon", "IEEE QPAIN", 2025, "c", "health", False, 11, "10.1109/qpain66474.2025.11171854", ""),
 ("Enhanced Heart Disease Prediction Using Advanced Classifiers and Ensemble Learning Techniques", "MS Alom, S Mondal, A Debnath, ASMS Ahamed", "IEEE ECCE", 2025, "c", "health", True, 9, "10.1109/ecce64574.2025.11013799", ""),
 ("Multiclass Detection of Misogynistic Bangla Text from YouTube Using Transformer-Based Models", "S Mondal, MS Alom, MM Alum, KLS Sunjida", "IEEE ECCE", 2025, "c", "nlp", False, 9, "10.1109/ecce64574.2025.11014024", ""),
 ("Extracting Disaster Insights from Bangla News Using Text Categorization", "SM Jeba, MS Alom, ASMS Ahamed, TT Aurpa, A Debnath, SR Dash, et al.", "IEEE QPAIN", 2025, "c", "nlp", False, 8, "10.1109/qpain66474.2025.11172020", ""),
 ("Enhancing Sleep Disorder Diagnosis with a Machine Learning Approach Using Ensemble Neural Networks", "MS Alom, SM Jeba, A Debnath, TT Aurpa, R Siddiqua", "11th Int. Conf. on Networking, Systems, and Security (NSysS)", 2024, "c", "health", True, 8, None, ""),
 ("Recognition of Data Breach Method from Story Using Advanced Deep Learning", "SM Jeba, TT Aurpa, MS Alom, MWM Joy, ASMS Ahamed, SR Dash, et al.", "IEEE INOCON", 2024, "c", "nlp", False, 5, "10.1109/inocon60754.2024.10512191", ""),
 ("A Comprehensive Approach to Fetal Health Prediction Using Machine Learning and Ensemble Models", "MS Alom, ASMS Ahamed, O Haque", "IEEE ICCIT", 2024, "c", "health", True, 3, "10.1109/iccit64611.2024.11022051", ""),
 ("SeaNet: Sentiment Analysis in Social Media Comments on Bengali Mega Project Using Transformer Learning", "FS Tamim, JA Khan, FH Siyam, MS Alom, MM Hoque", "IEEE COMPAS", 2025, "c", "nlp", False, 2, "10.1109/compas67506.2025.11381713", ""),
 ("Federated Machine Learning for Cardiovascular Risk Assessment: A Decentralized XGBoost Approach", "MS Alom, SS Akhi, SN Borsha, N Mia, FS Tamim, JA Nabin", "IEEE QPAIN", 2025, "c", "health", True, 2, "10.1109/qpain66474.2025.11171956", ""),
 ("Explainable Eggplant Leaf Disease Classification Using Vision Transformers and Convolutional Neural Networks", "A Rakin, MS Alom, MI Ahamed, NH Shouvo, I Al Mamoon, MA Awal", "IEEE QPAIN", 2026, "c", "vision", False, 1, "10.1109/qpain69676.2026.11545845", ""),
 ("A Web-Based Blockchain Framework to Prevent Counterfeit Medicines via QR Code Verification", "MS Alom, R Taha, SS Akhi, AR Nath", "IEEE COMPAS", 2025, "c", "health", True, 1, "10.1109/compas67506.2025.11381717", ""),
 ("SMOTE-Enhanced Ensemble Learning for Hepatitis C Risk Stratification with Feature Importance Analysis", "SS Akhi, MS Alom, R Taha, MAH Tomal, FA Jibon", "IEEE COMPAS", 2025, "c", "health", False, 1, None, ""),
 ("A Comparative Analysis of Deep Learning Models with Quantitative Validation of Explainable AI for Pneumonia Detection Utilising Chest X-ray Images", "R Akter, MS Hossain, SN Silika, MS Alom, I Al Mamoon, MA Awal", "IEEE PECCII", 2026, "c", "vision", False, 0, None, ""),
 ("Ensemble Based Classification for Lung Cancer Risk Analysis", "A Rakin, MI Ahamed, MS Alom, NH Shouvo, MA Awal, I Al Mamoon", "IEEE PECCII", 2026, "c", "health", False, 0, "10.1109/peccii70991.2026.11661843", ""),
 ("TomatoNet-R50: A ResNet50-Based Deep Learning Architecture for the Detection of Tomato Leaf Disease", "MS Alom, MI Ahamed, FA Jibon, NH Shouvo, AHM Kamal, A Rakin", "IEEE QPAIN", 2026, "c", "vision", True, 0, "10.1109/qpain69676.2026.11546563", ""),
 ("MangoNet-SA: A Lightweight MobileNetV2-Based Spatial Attention CNN for Robust Mango Leaf Disease Classification", "MS Alom, A Rakin, FA Jibon, NH Shouvo, AHM Kamal, MI Ahamed", "IEEE QPAIN", 2026, "c", "vision", True, 0, None, ""),
 ("Robust AIDS Disease Classification Using a Threshold-Optimized Weighted Ensemble and Class-Balanced Machine Learning", "A Rakin, NH Shouvo, MS Alom, MI Ahamed, WH Hridoy, I Al Mamoon, et al.", "IEEE QPAIN", 2026, "c", "health", False, 0, "10.1109/qpain69676.2026.11546397", ""),
 ("Class-Weighted ResNet50 for Robust Guava Leaf Disease Classification Under Real-Field Conditions", "NH Shouvo, MS Alom, FA Jibon, A Islam, WH Hridoy, A Rakin, MI Ahamed", "IEEE QPAIN", 2026, "c", "vision", False, 0, "10.1109/qpain69676.2026.11546431", ""),
 ("AppleNet-B1: Explainable Auto-Reweighted EfficientNet for Apple Disease Detection", "MS Alom, A Al Rafee, A Rakin, FA Jibon, NH Shouvo, AHM Kamal, et al.", "IEEE QPAIN", 2026, "c", "vision", True, 0, "10.1109/qpain69676.2026.11546512", ""),
 ("Transformer-Based Sentence Reconstruction from Jumbled Words: A Comparative Evaluation Against Sequence Models", "AB Rakib, O Haque, MS Alom, MN Ahmed", "IEEE QPAIN", 2026, "c", "nlp", False, 0, "10.1109/qpain69676.2026.11545863", ""),
 ("Developer-Oriented Classification of Mobile App Reviews Using a Hybrid BERT-XGBoost Ensemble", "MI Ahamed, MS Alom, MA Lameya, A Rakin, WH Hridoy, MA Awal, et al.", "IEEE QPAIN", 2026, "c", "nlp", False, 0, "10.1109/qpain69676.2026.11546035", ""),
 ("A Comparative Deep Learning and Transformer-Based Approach to Contextual Emotion Classification in Bangla Lyrical Verse", "A Rakin, MI Ahamed, MS Alom, MAI Lubna, KS Kushal, MM Alum", "IEEE QPAIN", 2026, "c", "nlp", False, 0, "10.1109/qpain69676.2026.11546189", ""),
 ("BanglaBlend Based Evaluation of Bengali Formal and Colloquial Text Classification", "F Hassin, A Rakin, MS Alom, MI Ahamed, S Mondal, A Islam", "IEEE QPAIN", 2026, "c", "nlp", False, 0, None, ""),
 ("Explainable Stacking Machine Learning Ensemble Model for Liver Disease Prediction", "O Haque, MS Alom, FA Jibon, SK Gain, MM Alum, MAA Linkon, et al.", "IEEE ICECTE", 2026, "c", "health", False, 0, "10.1109/icecte69292.2026.11429201", ""),
 ("A Multi-Class Heart Disease and Stroke Risk Classification Framework for Combined Assessment: A Machine Learning Approach", "A Rakin, MI Ahamed, F Hassin, KS Kushal, N Hasan Shouvo, MS Alom", "E3S Web of Conferences 735, 02004", 2026, "c", "health", False, 0, "10.1051/e3sconf/202673502004", ""),
 ("XSG-Ensemble: A Weighted Voting Ensemble Machine Learning Model for Enhanced Chronic Kidney Disease Prediction", "MI Ahamed, A Rakin, AB Rakib, M Hasan, K Sabik Ahmed, MS Alom, et al.", "E3S Web of Conferences 735, 03003", 2026, "c", "health", False, 0, "10.1051/e3sconf/202673503003", ""),
 ("AI-Assisted PCOS Detection from Ultrasound Scans: Benchmarking VGG16, ResNet50, and EfficientNet", "SS Akhi, MA Hoque Tomal, F Anam Jibon, F Tuz Zohura, MS Alom", "E3S Web of Conferences 735, 03004", 2026, "c", "vision", False, 0, "10.1051/e3sconf/202673503004", ""),
 ("Early Diabetic Detection Using Optimized Ensemble Machine Learning: A Comparative Evaluation", "MS Alom, F Imran, AAY Khan, A Debnath", "Int. Conf. on Computational Intelligence (Springer)", 2026, "c", "health", True, 0, "10.1007/978-3-032-04539-3_11", ""),
 ("An Explainable Machine Learning Approach to Multiclass Diabetes Risk Assessment", "SS Akhi, ASMS Ahamed, MR Miah, MSS Mahin, MS Alom", "IEEE ICCIT", 2025, "c", "health", False, 0, None, ""),
 ("Transformer-Assisted Categorization and Scope Detection of Bangla News Headlines: A Case Study on Politics, Business, and Crime", "MI Ahamed, S Akter, A Rakin, MMU Khan, MS Alom", "IEEE ICCIT", 2025, "c", "nlp", False, 0, "10.1109/iccit68739.2025.11491823", ""),
 ("Transformer-Based Multi-Class Categorization of Suicide Triggers in Bangla Headlines", "A Rakin, MI Ahamed, MS Alom, KS Kushal", "IEEE ICCIT", 2025, "c", "nlp", False, 0, "10.1109/iccit68739.2025.11491209", ""),
 ("Advancing Gastrointestinal Tract Segmentation: Dense-UPerNet and a Benchmark of 18 Encoder-Decoder Models", "SK Mazumder, NI Santo, MS Alom, MA Awal, I Al Mamoon", "IEEE BECITHCON", 2025, "c", "vision", False, 0, "10.1109/becithcon69222.2025.11504046", ""),
 ("Deep Learning Framework for Automated Numismatic Classification and Brahmi Inscription Segmentation of Gupta Archer Coins", "MFA Arnob, NJ Nijhum, MS Alom, I Mamoon", "IEEE SPICSCON", 2025, "c", "vision", False, 0, "10.1109/spicscon69221.2025.11504219", ""),
 ("Optimized Gradient Boosting for Chronic Kidney Disease Detection: A Comprehensive Comparative Framework for Clinical Decision Support", "I Al Mamoon, SS Akhi, MS Alom, FB Alam, A Sharmin, K Nur", "17th Int. Conf. on Information Technology and Electrical Engineering", 2025, "c", "health", False, 0, None, ""),
]

# public repo -> exact paper title it belongs to (None = listed in Code only)
REPOS = [
 ("Suicide-prediction", "Suicide-risk ensemble with SHAP and LIME", "An Explainable Triple-Layered Ensemble Model for Early Prediction of Suicide Risk Using Machine Learning"),
 ("Thyroid-cancer-prediction", "Thyroid cancer recurrence, boosted forest soft ensemble", "Boosted Forest Soft Ensemble of XGBoost, Gradient Boosting, and Random Forest with Explainable AI for Thyroid Cancer Recurrence Prediction"),
 ("Hepatics-C-Prediction-", "Hepatitis C risk with SMOTE-enhanced ensembles", "SMOTE-Enhanced Ensemble Learning for Hepatitis C Risk Stratification with Feature Importance Analysis"),
 ("Liver-Disease-Prediction-", "Liver disease, explainable stacking ensemble", "Explainable Stacking Machine Learning Ensemble Model for Liver Disease Prediction"),
 ("fetal-health", "Fetal health prediction with ensemble models", "A Comprehensive Approach to Fetal Health Prediction Using Machine Learning and Ensemble Models"),
 ("sleep-disorder", "Sleep disorder diagnosis with ensemble neural networks", "Enhancing Sleep Disorder Diagnosis with a Machine Learning Approach Using Ensemble Neural Networks"),
 ("Hate-speech", "Bangla text classification with BERT and LSTM", "Multiclass Detection of Misogynistic Bangla Text from YouTube Using Transformer-Based Models"),
 ("Gastrointestinal", "GI tract segmentation, Dense-UPerNet", "Advancing Gastrointestinal Tract Segmentation: Dense-UPerNet and a Benchmark of 18 Encoder-Decoder Models"),
 ("News-Classification", "News text classification", None),
]
