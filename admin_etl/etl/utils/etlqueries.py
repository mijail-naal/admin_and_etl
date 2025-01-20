FILM = """
    SELECT id as fw_id, title, description, rating,
    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6TZH') AS updated_at
    FROM content.film_work
    WHERE updated_at > %s
    ORDER BY updated_at
"""

PERSON = """
    SELECT id,
    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6TZH') as updated_at
    FROM content.person
    WHERE updated_at > %s
    ORDER BY updated_at LIMIT 100
"""

GENRE = """
    SELECT id,
    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6TZH') as updated_at
    FROM content.genre
    WHERE updated_at > %s
    ORDER BY updated_at LIMIT 2
"""

PERSON_FILM = """
    SELECT fw.id, fw.updated_at
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    WHERE pfw.person_id IN %s ORDER BY fw.updated_at LIMIT 100
"""

GENRE_FILM = """
    SELECT fw.id, fw.updated_at
    FROM content.film_work fw
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    WHERE gfw.genre_id IN %s ORDER BY fw.updated_at LIMIT 2
"""

FILM_PERSON_GENRE = """
    SELECT
        fw.id as fw_id, fw.title, fw.description, fw.rating, fw.type,
        TO_CHAR(fw.updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6TZH') as updated_at,
        TO_CHAR(p.updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6TZH') as person_updated_at,
        TO_CHAR(g.updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6TZH') as genre_updated_at,
        pfw.role, p.id, p.full_name, g.name as genre
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.id IN %s
"""
