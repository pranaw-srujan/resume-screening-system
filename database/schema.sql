-- ============================================
-- AI-Powered Resume Screening System
-- Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS resume_screening_db;
USE resume_screening_db;

-- ============================================
-- Table 1: candidates
-- Stores extracted candidate information
-- ============================================
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(20),
    skills TEXT,
    education TEXT,
    experience TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Table 2: resumes
-- Stores the uploaded file details, linked to a candidate
-- ============================================
CREATE TABLE IF NOT EXISTS resumes (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    file_path VARCHAR(255),
    original_filename VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
        ON DELETE CASCADE
);

-- ============================================
-- Table 3: job_descriptions
-- Stores job descriptions entered by recruiters
-- ============================================
CREATE TABLE IF NOT EXISTS job_descriptions (
    jd_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150),
    description_text TEXT,
    required_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Table 4: match_results
-- Stores the matching score between a candidate and a JD
-- ============================================
CREATE TABLE IF NOT EXISTS match_results (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    jd_id INT,
    match_score FLOAT,
    missing_skills TEXT,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
        ON DELETE CASCADE,
    FOREIGN KEY (jd_id) REFERENCES job_descriptions(jd_id)
        ON DELETE CASCADE
);
