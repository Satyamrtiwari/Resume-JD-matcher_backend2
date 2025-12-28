import requests

HF_API_URL = "https://satyamtiwarir10-resume.hf.space/predict"


def get_similarity_from_hf(resume_text: str, job_text: str) -> float:
    payload = {
        "resume": resume_text,
        "job": job_text
    }

    try:
        response = requests.post(
            HF_API_URL,
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        return float(data["score"])

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"HF Space request failed: {e}")
    except KeyError:
        raise RuntimeError(f"Unexpected HF response format: {response.text}")
