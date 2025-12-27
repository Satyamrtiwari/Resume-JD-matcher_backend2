import requests

HF_API_URL = "https://satyamtiwarir10-resume.hf.space/run/predict"

def get_similarity_from_hf(resume_text: str, job_text: str) -> float:
    payload = {"data": [resume_text, job_text]}

    try:
        response = requests.post(HF_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return float(result["data"][0])
    except Exception as e:
        raise RuntimeError(f"HF Space error: {e}")