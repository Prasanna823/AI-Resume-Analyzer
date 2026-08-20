import sqlite3
import os


DATABASE = "database.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            resume_name TEXT NOT NULL,

            job_role TEXT NOT NULL,

            ats_score INTEGER NOT NULL,

            match_percentage INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)

    connection.commit()

    connection.close()


def create_user(name, email, password):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (name, email, password)
        VALUES (?, ?, ?)
    """, (
        name,
        email,
        password
    ))

    user_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return user_id


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    return user


def save_analysis(
    user_id,
    resume_name,
    job_role,
    ats_score,
    match_percentage
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analyses
        (
            user_id,
            resume_name,
            job_role,
            ats_score,
            match_percentage
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        resume_name,
        job_role,
        ats_score,
        match_percentage
    ))

    connection.commit()

    connection.close()


def get_user_analyses(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))

    analyses = cursor.fetchall()

    connection.close()

    return analyses