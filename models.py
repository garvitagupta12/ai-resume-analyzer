from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    candidate_name: str
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]
    certifications: list[str]

class ResumeMatch(BaseModel):
    match_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    relevant_experience: list[str]
    relevant_projects: list[str]
    strengths: list[str]
    areas_for_improvement: list[str]
    explanation: str