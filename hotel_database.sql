-- =====================================================
-- SYSTEME DE GESTION HOTEL MEDITERRANEE
-- Base de Donnees Relationnelle SQL
-- =====================================================

-- =====================================================
-- TABLE: ailes
-- =====================================================
CREATE TABLE ailes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom ENUM('A', 'B') NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: chambres
-- =====================================================
CREATE TABLE chambres (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_chambre INT NOT NULL UNIQUE,
    aile_id INT NOT NULL,
    type ENUM('chambre', 'appartement') NOT NULL,
    statut ENUM('disponible', 'occupée', 'maintenance', 'nettoyage') DEFAULT 'disponible',
    etage INT NOT NULL,
    description VARCHAR(255),
    carte_active BOOLEAN DEFAULT TRUE,
    derniere_sync DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aile_id) REFERENCES ailes(id) ON DELETE RESTRICT
);

-- =====================================================
-- TABLE: demandes_maintenance
-- =====================================================
CREATE TABLE demandes_maintenance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chambre_id INT NOT NULL,
    type_probleme ENUM('gaz', 'chauffage', 'climatisation', 'électricité', 'plomberie', 'autre') NOT NULL,
    description TEXT,
    date_signalement DATETIME DEFAULT CURRENT_TIMESTAMP,
    résolu BOOLEAN DEFAULT FALSE,
    date_resolution DATETIME NULL,
    priorité ENUM('basse', 'moyenne', 'haute', 'urgente') DEFAULT 'moyenne',
    agent_assigné VARCHAR(100) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chambre_id) REFERENCES chambres(id) ON DELETE CASCADE
);

-- =====================================================
-- TABLE: utilisateurs
-- =====================================================
CREATE TABLE utilisateurs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    rôle ENUM('admin', 'chef_maintenance', 'réceptionniste') NOT NULL,
    mot_de_pass VARCHAR(255) NOT NULL,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEX POUR PERFORMANCES
-- =====================================================
CREATE INDEX idx_chambres_aile ON chambres(aile_id);
CREATE INDEX idx_chambres_statut ON chambres(statut);
CREATE INDEX idx_demandes_chambre ON demandes_maintenance(chambre_id);
CREATE INDEX idx_demandes_resolu ON demandes_maintenance(résolu);
CREATE INDEX idx_demandes_type ON demandes_maintenance(type_probleme);

-- =====================================================
-- VUES
-- =====================================================

-- Vue: Statut des chambres par aile
CREATE VIEW v_statut_aile AS
SELECT 
    a.nom AS aile,
    c.type,
    c.statut,
    COUNT(*) AS nombre
FROM chambres c
JOIN ailes a ON c.aile_id = a.id
GROUP BY a.nom, c.type, c.statut;

-- Vue: Chambres disponibles
CREATE VIEW v_chambres_disponibles AS
SELECT 
    c.id,
    c.numero_chambre,
    a.nom AS aile,
    c.type,
    c.etage
FROM chambres c
JOIN ailes a ON c.aile_id = a.id
WHERE c.statut = 'disponible'
ORDER BY c.numero_chambre;

-- =====================================================
-- INSERTIONS INITIALES
-- =====================================================

-- Inserer les ailes
INSERT INTO ailes (nom, description) VALUES 
('A', 'Aile Apartments - Appartements de luxe'),
('B', 'Aile Chambres - Chambres standard');

-- Inserer les utilisateurs
INSERT INTO utilisateurs (nom, email, rôle, mot_de_pass) VALUES 
('Admin Principal', 'admin@hotelmediterranee.com', 'admin', 'admin123'),
('Chef Maintenance', 'chef@hotelmediterranee.com', 'chef_maintenance', 'chef123'),
('Receptionniste', 'reception@hotelmediterranee.com', 'réceptionniste', 'reception123');

-- Inserer les chambres
-- Aile A (Appartements) - Chambres 101, 102, 103
INSERT INTO chambres (numero_chambre, aile_id, type, statut, etage, description, carte_active) VALUES 
(101, 1, 'appartement', 'occupée', 1, 'Appartement Suite Deluxe', TRUE),
(102, 1, 'appartement', 'disponible', 1, 'Appartement Standard', TRUE),
(103, 1, 'appartement', 'disponible', 1, 'Appartement Familial', FALSE);

-- Aile B (Chambres normales) - Chambres 201-203, 301-303, 401
INSERT INTO chambres (numero_chambre, aile_id, type, statut, etage, description, carte_active) VALUES 
(201, 2, 'chambre', 'occupée', 2, 'Chambre Double Standard', TRUE),
(202, 2, 'chambre', 'nettoyage', 2, 'Chambre Twin', TRUE),
(203, 2, 'chambre', 'maintenance', 2, 'Chambre Deluxe', TRUE),
(301, 2, 'chambre', 'occupée', 3, 'Chambre Suite', FALSE),
(302, 2, 'chambre', 'disponible', 3, 'Chambre Double Standard', TRUE),
(303, 2, 'chambre', 'nettoyage', 3, 'Chambre Deluxe', TRUE),
(401, 2, 'chambre', 'occupée', 4, 'Chambre Suite Presidentielle', TRUE);

-- Inserer des exemples de demandes de maintenance
INSERT INTO demandes_maintenance (chambre_id, type_probleme, description, priorité, agent_assigné) VALUES 
(3, 'climatisation', 'Le climatiseur ne fonctionne pas correctement', 'haute', 'Ahmed (Clim & Chauffage)'),
(6, 'plomberie', 'Fuite d\'eau dans la salle de bain', 'urgente', 'Karim (Plomberie & Gaz)'),
(7, 'électricité', 'Lumière clignotante dans la chambre', 'moyenne', 'Sami (Electricité & Ménage)'),
(1, 'chauffage', 'Problème de chauffage', 'basse', 'Ahmed (Clim & Chauffage)');

-- =====================================================
-- REQUETES UTILES
-- =====================================================

-- Compter les chambres par statut
SELECT 
    statut,
    COUNT(*) AS nombre
FROM chambres
GROUP BY statut;

-- Compter les chambres par type et par aile
SELECT 
    a.nom AS aile,
    c.type,
    COUNT(*) AS nombre
FROM chambres c
JOIN ailes a ON c.aile_id = a.id
GROUP BY a.nom, c.type;

-- Lister les demandes de maintenance non resolues
SELECT 
    d.id,
    c.numero_chambre,
    a.nom AS aile,
    d.type_probleme,
    d.description,
    d.date_signalement,
    d.priorité
FROM demandes_maintenance d
JOIN chambres c ON d.chambre_id = c.id
JOIN ailes a ON c.aile_id = a.id
WHERE d.résolu = FALSE
ORDER BY FIELD(d.priorité, 'urgente', 'haute', 'moyenne', 'basse'), d.date_signalement;

-- Taux d'occupation par aile
SELECT 
    a.nom AS aile,
    COUNT(*) AS total_chambres,
    SUM(CASE WHEN c.statut = 'occupée' THEN 1 ELSE 0 END) AS occupées,
    ROUND(SUM(CASE WHEN c.statut = 'occupée' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS taux_occupation
FROM chambres c
JOIN ailes a ON c.aile_id = a.id
GROUP BY a.nom;

