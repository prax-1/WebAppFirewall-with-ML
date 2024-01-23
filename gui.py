import tkinter as tk
from tkinter import ttk
import joblib

rf_model = joblib.load('random_forest_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')


def classify_url():
    url = entry.get()
    url_vectorized = vectorizer.transform([url])

    prediction = rf_model.predict(url_vectorized)[0]
    result_label.config(text=f"Classification: {'Malicious' if prediction == 1 else 'Safe'}")


root = tk.Tk()
root.title("Malicious URL Detector")
root.geometry("400x200")

style = ttk.Style()
style.configure("TButton", padding=(10, 5), font=('Helvetica', 12))

header_label = ttk.Label(root, text="Malicious URL Detector", font=('Helvetica', 16, 'bold'))
header_label.pack(pady=10)

entry = ttk.Entry(root, width=40, font=('Helvetica', 12))
entry.pack(pady=10)

classify_button = ttk.Button(root, text="Classify URL", command=classify_url)
classify_button.pack()

result_label = ttk.Label(root, text="", font=('Helvetica', 14))
result_label.pack(pady=10)

developed_by_label = ttk.Label(root, text="Developed By: Prakhar Gupta", font=('Helvetica', 10, 'italic'))
developed_by_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
