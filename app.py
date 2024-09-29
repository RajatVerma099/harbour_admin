from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import time

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("harbour-final-firebase-private-key.json")  # Provide the path to your Firebase key here
firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch jobs from Firebase collection "Jobs"
@app.route('/jobs', methods=['GET'])
def get_jobs():
    # print("hello")
    jobs_ref = db.collection("Jobs")
    # print(jobs_ref.list_documents())
    # print(jobs_ref.document("rajat").get())
    jobs = []
    # docs=jobs_ref.stream()
    for doc in jobs_ref.stream():
        job = doc.to_dict()
        # print(job)
        job['id'] = doc.id  # Add document ID for updating purposes
        jobs.append(job)
    return jsonify(jobs)

# Update a specific job in Firebase
@app.route('/update-job', methods=['POST'])
def update_job():
    data = request.json
    job_id = data.get('id')
    # print(data)
    updated_job_data = data.get('jobData')
    # print(updated_job_data)

    if not job_id or not updated_job_data:
        return jsonify({"error": "Invalid data"}), 400
    
    collection_ref = db.collection('Jobs')
    job_ref = collection_ref.document(job_id)
    job_ref.delete()
    time.sleep(1)
    collection_ref.add(updated_job_data,job_id)

    # print(job_ref.get())
    # job_ref.update(updated_job_data)
    return jsonify({"message": "Job updated successfully, kindly refresh the page."})

@app.route('/delete-job', methods=['POST'])
def delete_job():
    data = request.json
    job_id = data.get('id')
    
    collection_ref = db.collection('Jobs')
    job_ref = collection_ref.document(job_id)
    job_ref.delete()
    return jsonify({"message": "Job deleted successfully, kindly refresh the page."})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_data():
    return render_template('admin_data.html')

if __name__ == '__main__':
    app.run(debug=True)


