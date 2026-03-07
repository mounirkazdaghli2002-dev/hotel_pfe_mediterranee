-- ============================================
-- Hotel Mediterranee - Script SQL Complet
-- Base de donnees pour la gestion des chambres
-- ============================================

-- Table ailes
CREATE TABLE IF NOT EXISTS ailes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(10)
);

-- Table chambres
CREATE TABLE IF NOT EXISTS chambres (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero VARCHAR(10) UNIQUE,
    type ENUM('chambre','appartement'),
    aile_id INT,
    statut ENUM('disponible','occupée','maintenance','nettoyage') DEFAULT 'disponible',
    FOREIGN KEY (aile_id) REFERENCES ailes(id)
);

-- ============================================
-- Insertion des ailes
-- ============================================
INSERT INTO ailes (nom) VALUES ('A');
INSERT INTO ailes (nom) VALUES ('B');

-- ============================================
-- Insertion des appartements
-- ============================================
INSERT INTO chambres (numero, type, aile_id) VALUES 
('A3', 'appartement', 1),
('A4', 'appartement', 1),
('A1', 'apppartement', 2),
('A2', 'appartement', 2);

-- ============================================
-- Insertion automatique des chambres - AILE A (aile_id = 1)
-- ============================================

-- Intervalle 1001 → 1022
INSERT INTO chambres (numero, type, aile_id) VALUES 
('1001', 'chambre', 1),
('1002', 'chambre', 1),
('1003', 'chambre', 1),
('1004', 'chambre', 1),
('1005', 'chambre', 1),
('1006', 'chambre', 1),
('1007', 'chambre', 1),
('1008', 'chambre', 1),
('1009', 'chambre', 1),
('1010', 'chambre', 1),
('1011', 'chambre', 1),
('1012', 'chambre', 1),
('1013', 'chambre', 1),
('1014', 'chambre', 1),
('1015', 'chambre', 1),
('1016', 'chambre', 1),
('1017', 'chambre', 1),
('1018', 'chambre', 1),
('1019', 'chambre', 1),
('1020', 'chambre', 1),
('1021', 'chambre', 1),
('1022', 'chambre', 1);

-- Intervalle 1023 → 1043
INSERT INTO chambres (numero, type, aile_id) VALUES 
('1023', 'chambre', 1),
('1024', 'chambre', 1),
('1025', 'chambre', 1),
('1026', 'chambre', 1),
('1027', 'chambre', 1),
('1028', 'chambre', 1),
('1029', 'chambre', 1),
('1030', 'chambre', 1),
('1031', 'chambre', 1),
('1032', 'chambre', 1),
('1033', 'chambre', 1),
('1034', 'chambre', 1),
('1035', 'chambre', 1),
('1036', 'chambre', 1),
('1037', 'chambre', 1),
('1038', 'chambre', 1),
('1039', 'chambre', 1),
('1040', 'chambre', 1),
('1041', 'chambre', 1),
('1042', 'chambre', 1),
('1043', 'chambre', 1);

-- Intervalle 1044 → 1074
INSERT INTO chambres (numero, type, aile_id) VALUES 
('1044', 'chambre', 1),
('1045', 'chambre', 1),
('1046', 'chambre', 1),
('1047', 'chambre', 1),
('1048', 'chambre', 1),
('1049', 'chambre', 1),
('1050', 'chambre', 1),
('1051', 'chambre', 1),
('1052', 'chambre', 1),
('1053', 'chambre', 1),
('1054', 'chambre', 1),
('1055', 'chambre', 1),
('1056', 'chambre', 1),
('1057', 'chambre', 1),
('1058', 'chambre', 1),
('1059', 'chambre', 1),
('1060', 'chambre', 1),
('1061', 'chambre', 1),
('1062', 'chambre', 1),
('1063', 'chambre', 1),
('1064', 'chambre', 1),
('1065', 'chambre', 1),
('1066', 'chambre', 1),
('1067', 'chambre', 1),
('1068', 'chambre', 1),
('1069', 'chambre', 1),
('1070', 'chambre', 1),
('1071', 'chambre', 1),
('1072', 'chambre', 1),
('1073', 'chambre', 1),
('1074', 'chambre', 1);

-- Intervalle 2001 → 2065
INSERT INTO chambres (numero, type, aile_id) VALUES 
('2001', 'chambre', 1),
('2002', 'chambre', 1),
('2003', 'chambre', 1),
('2004', 'chambre', 1),
('2005', 'chambre', 1),
('2006', 'chambre', 1),
('2007', 'chambre', 1),
('2008', 'chambre', 1),
('2009', 'chambre', 1),
('2010', 'chambre', 1),
('2011', 'chambre', 1),
('2012', 'chambre', 1),
('2013', 'chambre', 1),
('2014', 'chambre', 1),
('2015', 'chambre', 1),
('2016', 'chambre', 1),
('2017', 'chambre', 1),
('2018', 'chambre', 1),
('2019', 'chambre', 1),
('2020', 'chambre', 1),
('2021', 'chambre', 1),
('2022', 'chambre', 1),
('2023', 'chambre', 1),
('2024', 'chambre', 1),
('2025', 'chambre', 1),
('2026', 'chambre', 1),
('2027', 'chambre', 1),
('2028', 'chambre', 1),
('2029', 'chambre', 1),
('2030', 'chambre', 1),
('2031', 'chambre', 1),
('2032', 'chambre', 1),
('2033', 'chambre', 1),
('2034', 'chambre', 1),
('2035', 'chambre', 1),
('2036', 'chambre', 1),
('2037', 'chambre', 1),
('2038', 'chambre', 1),
('2039', 'chambre', 1),
('2040', 'chambre', 1),
('2041', 'chambre', 1),
('2042', 'chambre', 1),
('2043', 'chambre', 1),
('2044', 'chambre', 1),
('2045', 'chambre', 1),
('2046', 'chambre', 1),
('2047', 'chambre', 1),
('2048', 'chambre', 1),
('2049', 'chambre', 1),
('2050', 'chambre', 1),
('2051', 'chambre', 1),
('2052', 'chambre', 1),
('2053', 'chambre', 1),
('2054', 'chambre', 1),
('2055', 'chambre', 1),
('2056', 'chambre', 1),
('2057', 'chambre', 1),
('2058', 'chambre', 1),
('2059', 'chambre', 1),
('2060', 'chambre', 1),
('2061', 'chambre', 1),
('2062', 'chambre', 1),
('2063', 'chambre', 1),
('2064', 'chambre', 1),
('2065', 'chambre', 1);

-- Intervalle 3200 → 3232
INSERT INTO chambres (numero, type, aile_id) VALUES 
('3200', 'chambre', 1),
('3201', 'chambre', 1),
('3202', 'chambre', 1),
('3203', 'chambre', 1),
('3204', 'chambre', 1),
('3205', 'chambre', 1),
('3206', 'chambre', 1),
('3207', 'chambre', 1),
('3208', 'chambre', 1),
('3209', 'chambre', 1),
('3210', 'chambre', 1),
('3211', 'chambre', 1),
('3212', 'chambre', 1),
('3213', 'chambre', 1),
('3214', 'chambre', 1),
('3215', 'chambre', 1),
('3216', 'chambre', 1),
('3217', 'chambre', 1),
('3218', 'chambre', 1),
('3219', 'chambre', 1),
('3220', 'chambre', 1),
('3221', 'chambre', 1),
('3222', 'chambre', 1),
('3223', 'chambre', 1),
('3224', 'chambre', 1),
('3225', 'chambre', 1),
('3226', 'chambre', 1),
('3227', 'chambre', 1),
('3228', 'chambre', 1),
('3229', 'chambre', 1),
('3230', 'chambre', 1),
('3231', 'chambre', 1),
('3232', 'chambre', 1);

-- Intervalle 3033 → 3065
INSERT INTO chambres (numero, type, aile_id) VALUES 
('3033', 'chambre', 1),
('3034', 'chambre', 1),
('3035', 'chambre', 1),
('3036', 'chambre', 1),
('3037', 'chambre', 1),
('3038', 'chambre', 1),
('3039', 'chambre', 1),
('3040', 'chambre', 1),
('3041', 'chambre', 1),
('3042', 'chambre', 1),
('3043', 'chambre', 1),
('3044', 'chambre', 1),
('3045', 'chambre', 1),
('3046', 'chambre', 1),
('3047', 'chambre', 1),
('3048', 'chambre', 1),
('3049', 'chambre', 1),
('3050', 'chambre', 1),
('3051', 'chambre', 1),
('3052', 'chambre', 1),
('3053', 'chambre', 1),
('3054', 'chambre', 1),
('3055', 'chambre', 1),
('3056', 'chambre', 1),
('3057', 'chambre', 1),
('3058', 'chambre', 1),
('3059', 'chambre', 1),
('3060', 'chambre', 1),
('3061', 'chambre', 1),
('3062', 'chambre', 1),
('3063', 'chambre', 1),
('3064', 'chambre', 1),
('3065', 'chambre', 1);

-- ============================================
-- Insertion automatique des chambres - AILE B (aile_id = 2)
-- ============================================

-- Intervalle 1060 → 1111
INSERT INTO chambres (numero, type, aile_id) VALUES 
('1060', 'chambre', 2),
('1061', 'chambre', 2),
('1062', 'chambre', 2),
('1063', 'chambre', 2),
('1064', 'chambre', 2),
('1065', 'chambre', 2),
('1066', 'chambre', 2),
('1067', 'chambre', 2),
('1068', 'chambre', 2),
('1069', 'chambre', 2),
('1070', 'chambre', 2),
('1071', 'chambre', 2),
('1072', 'chambre', 2),
('1073', 'chambre', 2),
('1074', 'chambre', 2),
('1075', 'chambre', 2),
('1076', 'chambre', 2),
('1077', 'chambre', 2),
('1078', 'chambre', 2),
('1079', 'chambre', 2),
('1080', 'chambre', 2),
('1081', 'chambre', 2),
('1082', 'chambre', 2),
('1083', 'chambre', 2),
('1084', 'chambre', 2),
('1085', 'chambre', 2),
('1086', 'chambre', 2),
('1087', 'chambre', 2),
('1088', 'chambre', 2),
('1089', 'chambre', 2),
('1090', 'chambre', 2),
('1091', 'chambre', 2),
('1092', 'chambre', 2),
('1093', 'chambre', 2),
('1094', 'chambre', 2),
('1095', 'chambre', 2),
('1096', 'chambre', 2),
('1097', 'chambre', 2),
('1098', 'chambre', 2),
('1099', 'chambre', 2),
('1100', 'chambre', 2),
('1101', 'chambre', 2),
('1102', 'chambre', 2),
('1103', 'chambre', 2),
('1104', 'chambre', 2),
('1105', 'chambre', 2),
('1106', 'chambre', 2),
('1107', 'chambre', 2),
('1108', 'chambre', 2),
('1109', 'chambre', 2),
('1110', 'chambre', 2),
('1111', 'chambre', 2);

-- Intervalle 1112 → 1135
INSERT INTO chambres (numero, type, aile_id) VALUES 
('1112', 'chambre', 2),
('1113', 'chambre', 2),
('1114', 'chambre', 2),
('1115', 'chambre', 2),
('1116', 'chambre', 2),
('1117', 'chambre', 2),
('1118', 'chambre', 2),
('1119', 'chambre', 2),
('1120', 'chambre', 2),
('1121', 'chambre', 2),
('1122', 'chambre', 2),
('1123', 'chambre', 2),
('1124', 'chambre', 2),
('1125', 'chambre', 2),
('1126', 'chambre', 2),
('1127', 'chambre', 2),
('1128', 'chambre', 2),
('1129', 'chambre', 2),
('1130', 'chambre', 2),
('1131', 'chambre', 2),
('1132', 'chambre', 2),
('1133', 'chambre', 2),
('1134', 'chambre', 2),
('1135', 'chambre', 2);

-- Intervalle 2020 → 2035
INSERT INTO chambres (numero, type, aile_id) VALUES 
('2020', 'chambre', 2),
('2021', 'chambre', 2),
('2022', 'chambre', 2),
('2023', 'chambre', 2),
('2024', 'chambre', 2),
('2025', 'chambre', 2),
('2026', 'chambre', 2),
('2027', 'chambre', 2),
('2028', 'chambre', 2),
('2029', 'chambre', 2),
('2030', 'chambre', 2),
('2031', 'chambre', 2),
('2032', 'chambre', 2),
('2033', 'chambre', 2),
('2034', 'chambre', 2),
('2035', 'chambre', 2);

-- Intervalle 3040 → 3073
INSERT INTO chambres (numero, type, aile_id) VALUES 
('3040', 'chambre', 2),
('3041', 'chambre', 2),
('3042', 'chambre', 2),
('3043', 'chambre', 2),
('3044', 'chambre', 2),
('3045', 'chambre', 2),
('3046', 'chambre', 2),
('3047', 'chambre', 2),
('3048', 'chambre', 2),
('3049', 'chambre', 2),
('3050', 'chambre', 2),
('3051', 'chambre', 2),
('3052', 'chambre', 2),
('3053', 'chambre', 2),
('3054', 'chambre', 2),
('3055', 'chambre', 2),
('3056', 'chambre', 2),
('3057', 'chambre', 2),
('3058', 'chambre', 2),
('3059', 'chambre', 2),
('3060', 'chambre', 2),
('3061', 'chambre', 2),
('3062', 'chambre', 2),
('3063', 'chambre', 2),
('3064', 'chambre', 2),
('3065', 'chambre', 2),
('3066', 'chambre', 2),
('3067', 'chambre', 2),
('3068', 'chambre', 2),
('3069', 'chambre', 2),
('3070', 'chambre', 2),
('3071', 'chambre', 2),
('3072', 'chambre', 2),
('3073', 'chambre', 2);

-- ============================================
-- Verification
-- ============================================
SELECT 'Aile A - Total:' AS info, COUNT(*) AS total FROM chambres WHERE aile_id = 1;
SELECT 'Aile B - Total:' AS info, COUNT(*) AS total FROM chambres WHERE aile_id = 2;
SELECT 'Appartements Aile A:' AS info, COUNT(*) AS total FROM chambres WHERE numero IN ('A3', 'A4');
SELECT 'Appartements Aile B:' AS info, COUNT(*) AS total FROM chambres WHERE numero IN ('A1', 'A2');
