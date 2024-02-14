import time
import uuid

from flask import Flask, jsonify, request, url_for
from threading import Thread

app = Flask(__name__)

jobs: dict = {}


def example_job(job_id, items) -> None:
    """
        This function starts a QR job, updates its status, and processes the items.

        Args:
            job_id (str): The unique identifier of the job.
            items (int): The number of items to process.

        Returns:
            None
    """
    print('QR job started')
    jobs[job_id]['status'] = 'Processing'
    for i in range(items):
        time.sleep(1)
        print(f"Process: {i + 1}/{items}")
        jobs[job_id]['items_Processing'] = f"{i + 1}/{items}"
    print('QR job finished')
    jobs[job_id]['status'] = 'Finalized'


@app.route('/execute', methods=['POST'])
def executed():
    """
       This route starts a QR job and returns a success message along with the job ID.

       Returns:
           json: A JSON object containing the operation status, a message, and the job ID.
    """
    data = request.get_json()
    items = data.get('items')
    if items is None:
        return jsonify({"success": False, "msg": "Items not found"}), 400
    job_id: str = str(uuid.uuid4())
    jobs[job_id] = {'status': 'Created'}
    Thread(target=example_job, args=(job_id, items,)).start()
    return jsonify({
        "success": True,
        "msg": "The job has started correctly",
        "job_id": job_id,
        "links": {
            "job_url": url_for('find_job_by_id', job_id=job_id, _external=True),
            "all_jobs_url": url_for('find_all', _external=True)
        },
    }), 200


@app.route('/jobs/<job_id>', methods=['GET'])
def find_job_by_id(job_id: str):
    """
       This route returns the status of a specific job.

       Args:
           job_id (str): The unique identifier of the job.

       Returns:
           json: A JSON object containing the operation status and the job status.
    """
    job = jobs.get(job_id)
    if job is None:
        return jsonify({"success": False, "msg": "Job not found"}), 404
    return jsonify({
        "success": True,
        "status": job['status'],
        "items_Processing": job['items_Processing'],
        "links": {
            "job_url": url_for('find_job_by_id', job_id=job_id, _external=True),
            "all_jobs_url": url_for('find_all', _external=True)
        },
    }), 200


@app.route('/jobs', methods=['GET'])
def find_all():
    """
    This route returns the status of all jobs.

    Returns:
        json: A JSON object containing the operation status and a list with the status of all jobs.
    """
    data = []
    for job_id, job in jobs.items():
        data.append({
            "job_id": job_id,
            "status": job['status'],
            "items_Processing": job['items_Processing'],
            "links": {
                "job_url": url_for('find_job_by_id', job_id=job_id, _external=True),
                "all_jobs_url": url_for('find_all', _external=True)
            },
        })
    return jsonify({"success": True, "data": data}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
