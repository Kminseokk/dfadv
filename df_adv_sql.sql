-- 데이터베이스 선택
USE df_adv;

CREATE TABLE adventure_name (
    id INT AUTO_INCREMENT PRIMARY KEY,
    character_uid VARCHAR(255) UNIQUE,
    character_server VARCHAR(255),
    character_name VARCHAR(255),
    character_job_root VARCHAR(255),
    character_job_name VARCHAR(255),
    item_level_sum INT,
    character_fame INT,
    dungeondeal_val VARCHAR(255),
    mistGear_count INT,
    Custom_epic INT,
    enchant VARCHAR(255),
    queen_creature VARCHAR(255),
    fashionista_aurora VARCHAR(255),
    title VARCHAR(255),
    dark_land_count INT
);

-- 테스트용
UPDATE adventure_name
SET character_server = 'NewServer'
WHERE character_uid = '067250a765ea6463afc44c1d57f20401';
