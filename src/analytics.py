import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
import os
from database import Database

class ResumeAnalytics:
    def __init__(self, db: Database):
        self.db = db
        self.setup_style()
    
    @staticmethod
    def setup_style():
        """Set up the visualization style."""
        plt.style.use('seaborn')
        sns.set_palette("husl")
    
    def plot_skill_distribution(self, save_path: str = None):
        """Plot the distribution of skills across all candidates."""
        # Get all candidates and their skills
        candidates = self.db.get_all_candidates()
        all_skills = {}
        
        for candidate in candidates:
            skills = json.loads(candidate['skills'])
            for skill in skills:
                all_skills[skill] = all_skills.get(skill, 0) + 1
        
        # Create DataFrame
        df = pd.DataFrame(list(all_skills.items()), columns=['Skill', 'Count'])
        df = df.sort_values('Count', ascending=False).head(20)
        
        # Create plot
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='Count', y='Skill')
        plt.title('Top 20 Skills Distribution')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def plot_score_distribution(self, job_id: int, save_path: str = None):
        """Plot the distribution of scores for a specific job."""
        screenings = self.db.get_job_candidates(job_id)
        scores = [s['total_score'] for s in screenings]
        
        plt.figure(figsize=(10, 6))
        sns.histplot(scores, bins=20, kde=True)
        plt.title(f'Score Distribution for Job #{job_id}')
        plt.xlabel('Score')
        plt.ylabel('Count')
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def plot_experience_vs_score(self, job_id: int, save_path: str = None):
        """Plot relationship between experience and scores."""
        candidates = self.db.get_job_candidates(job_id)
        
        data = {
            'Experience': [c['experience_years'] for c in candidates],
            'Score': [c['total_score'] for c in candidates]
        }
        df = pd.DataFrame(data)
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Experience', y='Score')
        sns.regplot(data=df, x='Experience', y='Score', scatter=False)
        plt.title(f'Experience vs Score for Job #{job_id}')
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def generate_report(self, job_id: int, output_dir: str = 'reports'):
        """Generate a comprehensive report with visualizations."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate plots
        self.plot_skill_distribution(os.path.join(output_dir, 'skills_distribution.png'))
        self.plot_score_distribution(job_id, os.path.join(output_dir, 'score_distribution.png'))
        self.plot_experience_vs_score(job_id, os.path.join(output_dir, 'experience_vs_score.png'))
        
        # Get job details
        job = self.db.get_job(job_id)
        candidates = self.db.get_job_candidates(job_id)
        
        # Create summary statistics
        stats = {
            'total_candidates': len(candidates),
            'average_score': sum(c['total_score'] for c in candidates) / len(candidates),
            'average_experience': sum(c['experience_years'] for c in candidates) / len(candidates),
            'top_skills': self._get_top_skills(candidates)
        }
        
        # Generate HTML report
        report_html = self._generate_html_report(job, stats)
        with open(os.path.join(output_dir, f'report_job_{job_id}.html'), 'w') as f:
            f.write(report_html)
    
    def _get_top_skills(self, candidates: List[Dict[str, Any]], top_n: int = 10):
        """Get the most common skills among candidates."""
        skill_count = {}
        for candidate in candidates:
            skills = json.loads(candidate['skills'])
            for skill in skills:
                skill_count[skill] = skill_count.get(skill, 0) + 1
        
        return sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def _generate_html_report(self, job: Dict[str, Any], stats: Dict[str, Any]) -> str:
        """Generate HTML report with embedded visualizations."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Screening Report - Job #{job['id']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
                .stat-card {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
                .visualization {{ margin: 40px 0; }}
            </style>
        </head>
        <body>
            <h1>Screening Report - {job['title']}</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Candidates</h3>
                    <p>{stats['total_candidates']}</p>
                </div>
                <div class="stat-card">
                    <h3>Average Score</h3>
                    <p>{stats['average_score']:.2f}</p>
                </div>
                <div class="stat-card">
                    <h3>Average Experience</h3>
                    <p>{stats['average_experience']:.1f} years</p>
                </div>
            </div>
            
            <div class="visualization">
                <h2>Skills Distribution</h2>
                <img src="skills_distribution.png" alt="Skills Distribution">
            </div>
            
            <div class="visualization">
                <h2>Score Distribution</h2>
                <img src="score_distribution.png" alt="Score Distribution">
            </div>
            
            <div class="visualization">
                <h2>Experience vs Score</h2>
                <img src="experience_vs_score.png" alt="Experience vs Score">
            </div>
            
            <h2>Top Skills</h2>
            <ul>
                {chr(10).join(f'<li>{skill}: {count} candidates</li>' for skill, count in stats['top_skills'])}
            </ul>
        </body>
        </html>
        """
