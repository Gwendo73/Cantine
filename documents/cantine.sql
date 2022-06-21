-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : jeu. 02 juin 2022 à 15:11
-- Version du serveur :  5.7.34
-- Version de PHP : 7.4.21


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
DROP TABLE TypeDeClasse;
DROP TABLE Compte;
DROP TABLE Classe;
DROP TABLE Repas;
DROP TABLE Representant;
DROP TABLE Tarif;
DROP TABLE Enfant;
DROP TABLE Enseignant;
DROP TABLE Enseigne;
DROP TABLE Formule;
DROP TABLE Jour;
DROP TABLE Mange;
DROP TABLE EstAllergiqueA;
DROP TABLE Allergie;
DROP TABLE Conge;
--
-- Base de données : `cantine`
--

-- --------------------------------------------------------
--
-- Structure de la table `Classe`
--

CREATE TABLE IF NOT EXISTS Classe (
  code_classe integer primary key autoincrement,
  nom_classe TEXT NOT NULL,
  code_type integer NOT NULL,
  FOREIGN KEY(code_type) REFERENCES TypeDeClasse(code_type)
);

-- --------------------------------------------------------
--
-- Structure de la table `Type`
--

CREATE TABLE IF NOT EXISTS TypeDeClasse (
  code_type integer primary key autoincrement,
  type_classe TEXT NOT NULL,
  niveau_classe TEXT NOT NULL
);

-- --------------------------------------------------------

--
-- Structure de la table `Formule`
--

CREATE TABLE IF NOT EXISTS Formule (
  code_formule integer primary key autoincrement,
  nom_formule TEXT NOT NULL
);

-- --------------------------------------------------------
--
-- Structure de la table `Compte`
--

CREATE TABLE IF NOT EXISTS Compte (
  identifiant TEXT primary key,
  mot_de_passe TEXT NOT NULL,
  type_compte TEXT NOT NULL
);

-- --------------------------------------------------------

--
-- Structure de la table `Jour`
--

CREATE TABLE IF NOT EXISTS Jour (
  code_jour integer PRIMARY KEY,
  jour TEXT NOT NULL
);


-- --------------------------------------------------------

--
-- Structure de la table `Enfant`
--

CREATE TABLE IF NOT EXISTS Enfant (
  code_enfant integer primary key autoincrement,
  nom_enfant TEXT NOT NULL,
  prenom_enfant TEXT NOT NULL,
  code_tarif integer NOT NULL,
  code_classe integer NOT NULL,
  code_representant integer NOT NULL,
  code_formule integer NOT NULL,
  FOREIGN KEY (code_tarif) REFERENCES Tarif(code_tarif),
  FOREIGN KEY (code_classe) REFERENCES Classe(code_classe),
  FOREIGN KEY (code_representant) REFERENCES Representant(code_representant)
  FOREIGN KEY (code_formule) REFERENCES Formule(code_formule)
);

-- --------------------------------------------------------

--
-- Structure de la table `Mange`
--

CREATE TABLE IF NOT EXISTS Mange (
  code_jour integer,
  code_enfant integer,
  PRIMARY KEY(code_jour, code_enfant),
  FOREIGN KEY (code_jour) REFERENCES Jour(code_jour),
  FOREIGN KEY (code_enfant) REFERENCES Enfant(code_enfant)
);

-- --------------------------------------------------------

--
-- Structure de la table `Repas`
--

CREATE TABLE IF NOT EXISTS Repas (
  code_repas integer primary key autoincrement,
  date_repas date NOT NULL,
  code_enfant integer NOT NULL,
  FOREIGN KEY (code_enfant) REFERENCES Enfant(code_enfant)
);

-- --------------------------------------------------------

--
-- Structure de la table `Representant`
--

CREATE TABLE IF NOT EXISTS Representant (
  code_representant integer primary key autoincrement,
  nom_representant TEXT NOT NULL,
  prenom_representant TEXT NOT NULL,
  telephone TEXT,
  email TEXT,
  identifiant TEXT NOT NULL,
  FOREIGN KEY (identifiant) REFERENCES Compte(identifiant)
);

-- --------------------------------------------------------

--
-- Structure de la table `Tarif`
--

CREATE TABLE IF NOT EXISTS Tarif (
  code_tarif integer primary key autoincrement,
  nom_tarif TEXT NOT NULL,
  tarif float NOT NULL
);


-- --------------------------------------------------------

--
-- Structure de la table `Enseignant`
--

CREATE TABLE IF NOT EXISTS Enseignant (
  code_enseignant integer primary key autoincrement,
  nom_enseignant TEXT NOT NULL,
  prenom_enseignant TEXT NOT NULL,
  identifiant TEXT NOT NULL,
  FOREIGN KEY (identifiant) REFERENCES Compte(identifiant)
);

-- --------------------------------------------------------

--
-- Structure de la table `Enseigne`
--

CREATE TABLE IF NOT EXISTS Enseigne (
  code_enseignant integer,
  code_classe integer,
  PRIMARY KEY (code_enseignant, code_classe),
  FOREIGN KEY (code_enseignant) REFERENCES Enseignant(code_enseignant),
  FOREIGN KEY (code_classe) REFERENCES Classe(code_classe)
);

-- --------------------------------------------------------

--
-- Structure de la table `Allergie`
--

CREATE TABLE IF NOT EXISTS Allergie (
  code_allergie integer PRIMARY KEY AUTOINCREMENT,
  nom_allergie TEXT NOT NULL
);

-- --------------------------------------------------------

--
-- Structure de la table `EstAllergiqueA`
--

CREATE TABLE IF NOT EXISTS EstAllergiqueA (
  code_allergie integer,
  code_enfant integer,
  PRIMARY KEY (code_allergie, code_enfant),
  FOREIGN KEY (code_allergie) REFERENCES Allergie(code_allergie),
  FOREIGN KEY (code_enfant) REFERENCES Enfant(code_enfant)
);

----------------------------------------------------------

--
-- Structure de la table `Conge`
--

CREATE TABLE IF NOT EXISTS Conge (
  date_conge date PRIMARY KEY
);

----------------------------------------------------------

-- Compte Admin
INSERT INTO Compte VALUES ('admin', 'admin', 'Admin');

-- Comptes Représentants
INSERT INTO Compte VALUES ('gartalle', 'test', 'Representant');
INSERT INTO Compte VALUES ('smic', 'smic', 'Representant');
INSERT INTO Compte VALUES ('Z', 'Z', 'Representant');
INSERT INTO Compte VALUES ('caro', 'julien', 'Representant');
INSERT INTO Compte VALUES ('senlis', 'senlis', 'Representant');
INSERT INTO Compte VALUES ('jdore', 'jdore', 'Representant');
INSERT INTO Compte VALUES ('jbc', 'tb10', 'Representant');
INSERT INTO Compte VALUES ('vdoppel', 'vdoppel', 'Representant');
INSERT INTO Compte VALUES ('cdouche', 'cdouche', 'Representant');
INSERT INTO Compte VALUES ('julien', 'caro', 'Representant');
INSERT INTO Compte VALUES ('maestro', 'maestro', 'Representant');
INSERT INTO Compte VALUES ('lgbtqq+', 'lgbtqq+', 'Representant');
INSERT INTO Compte VALUES ('mgrim', 'mgrim', 'Representant');
INSERT INTO Compte VALUES ('churson', 'churson', 'Representant');
INSERT INTO Compte VALUES ('lilianne', 'feria', 'Representant');
INSERT INTO Compte VALUES ('arnaud', 'arnaud', 'Representant');
INSERT INTO Compte VALUES ('tonio', 'tonio', 'Representant');
INSERT INTO Compte VALUES ('faou', 'faou', 'Representant');
INSERT INTO Compte VALUES ('amontreuil', 'amontreuil', 'Representant');
INSERT INTO Compte VALUES ('kr', 'kr', 'Representant');
INSERT INTO Compte VALUES ('louisp', 'A350frvr', 'Representant');
INSERT INTO Compte VALUES ('pelota', 'pelota', 'Representant');
INSERT INTO Compte VALUES ('victine', 'victine', 'Representant');
INSERT INTO Compte VALUES ('renard', 'agent', 'Representant');
INSERT INTO Compte VALUES ('peppapig', 'basicfit<3', 'Representant');
INSERT INTO Compte VALUES ('mtellier', 'mtellier', 'Representant');
INSERT INTO Compte VALUES ('mtesta', 'mtesta', 'Representant');
INSERT INTO Compte VALUES ('gendarme', 'gendarme', 'Representant');

-- Comptes Enseignants
INSERT INTO Compte VALUES ('jkan', 'jkan', 'Enseignant');
INSERT INTO Compte VALUES ('jneymar', 'jneymar', 'Enseignant');
INSERT INTO Compte VALUES ('sdi', 'sdi', 'Enseignant');
INSERT INTO Compte VALUES ('aterieur', 'aterieur', 'Enseignant');
INSERT INTO Compte VALUES ('jcelere', 'jcelere', 'Enseignant');
INSERT INTO Compte VALUES ('tdesavoie', 'tdesavoie', 'Enseignant');
INSERT INTO Compte VALUES ('pchtron', 'pchtron', 'Enseignant');
INSERT INTO Compte VALUES ('lbar', 'lbar', 'Enseignant');
INSERT INTO Compte VALUES ('tlouest', 'tlouest', 'Enseignant');
INSERT INTO Compte VALUES ('aere', 'aere', 'Enseignant');

INSERT INTO Enseignant VALUES (1, 'KAN', 'Jerry', 'jkan');
INSERT INTO Enseignant VALUES (2, 'NEYMAR', 'Jean', 'jneymar');
INSERT INTO Enseignant VALUES (3, 'DI', 'Sam', 'sdi');
INSERT INTO Enseignant VALUES (4, 'TERIEUR', 'Alain', 'aterieur');
INSERT INTO Enseignant VALUES (5, 'CELERE', 'Jacques', 'jcelere');
INSERT INTO Enseignant VALUES (6, 'DE SAVOIE', 'Tom', 'tdesavoie');
INSERT INTO Enseignant VALUES (7, 'CHTRON', 'Paul', 'pchtron');
INSERT INTO Enseignant VALUES (8, 'BAR', 'Lenny', 'lbar');
INSERT INTO Enseignant VALUES (9, 'LOUEST', 'Thea', 'tlouest');
INSERT INTO Enseignant VALUES (10, 'ERE', 'Axel', 'aere');

INSERT INTO Representant VALUES (1, 'ARTALLE', 'Gwendal', '0647396010', 'gwendal.artalle73@gmail.com', 'gartalle');
INSERT INTO Representant VALUES (2, 'BEAUBOIS', 'Smic', '0625408670', 'smic@cannes.com', 'smic');
INSERT INTO Representant VALUES (3, 'BERTOLONE', 'Darlann', '0625408670', 'darlann@flyinstinct.com', 'Z');
INSERT INTO Representant VALUES (4, 'CHABAUD', 'Caro', '0625408580', 'pepita@orange.fr', 'caro');
INSERT INTO Representant VALUES (5, 'CHAMBREY', 'Louis', '', 'lchambrey@boeing.us', 'senlis');
INSERT INTO Representant VALUES (6, 'CLUZEL', 'Alexis', '', '', 'jdore');
INSERT INTO Representant VALUES (7, 'COLIN', 'JB', '0625408670', 'jb_c@capgemini.com', 'jbc');
INSERT INTO Representant VALUES (8, 'DOPPEL', 'Victor', '', '', 'vdoppel');
INSERT INTO Representant VALUES (9, 'DOUCHE-UN', 'Clément', '', 'clement@airbus.fr', 'cdouche');
INSERT INTO Representant VALUES (10, 'DUNEZ', 'Julien', '', 'pepito@acmtp.fr', 'julien');
INSERT INTO Representant VALUES (11, 'GANDJY', 'Shayan', '', 'cesar.hurson@dgac.fr', 'maestro');
INSERT INTO Representant VALUES (12, 'GIBERT', 'Timmy', '', 'timmy@lgbtqq.com', 'lgbtqq+');
INSERT INTO Representant VALUES (13, 'GRIMONT', 'Mina', '', '', 'mgrim');
INSERT INTO Representant VALUES (14, 'HURSON', 'Cesar', '0625408670', 'cesar.hurson@dgac.fr', 'churson');
INSERT INTO Representant VALUES (15, 'JOUVE', 'Ilian', '0698708670', 'lilianne.jouve@wanadoo.fr', 'lilianne');
INSERT INTO Representant VALUES (16, 'MONTE-LA-GARDE', 'Arnaud', '', 'arnaud@biereandsurf.fr', 'arnaud');
INSERT INTO Representant VALUES (17, 'LEBRETON', 'Antoine', '', 'antoine@morbihan.bretagne', 'tonio');
INSERT INTO Representant VALUES (18, 'MAMMERI', 'Faou', '', '', 'faou');
INSERT INTO Representant VALUES (19, 'MONTREUIL', 'Alisée', '', '', 'amontreuil');
INSERT INTO Representant VALUES (20, 'NGOUPAYOU', 'Kay-Rhane', '', '', 'kr');
INSERT INTO Representant VALUES (21, 'PECHENAIR', 'Louis', '0635089457', 'pechenair@gmail.com', 'louisp');
INSERT INTO Representant VALUES (22, 'PÉLOS', 'Alice', '0678910112', 'pelotpal@hotmail.fr', 'pelota');
INSERT INTO Representant VALUES (23, 'PHILIPPE', 'Clémentine', '0677735003', 'viclem@enac.com', 'victine');
INSERT INTO Representant VALUES (24, 'RATVEAU', 'Chloé', '0625408670', 'chloé.ratveau@enac.fr', 'renard');
INSERT INTO Representant VALUES (25, 'ROUYER', 'Jarry', '0625438670', 'jeremy.muscle@basic-fit.com', 'peppapig');
INSERT INTO Representant VALUES (26, 'TELLIER', 'Sylvie', '', '', 'mtellier');
INSERT INTO Representant VALUES (27, 'TESTARODE', 'Mathieu', '', '', 'mtesta');
INSERT INTO Representant VALUES (28, 'ZAMPIN', 'Piero', '', '', 'gendarme');

INSERT INTO Tarif VALUES (1, 'Tarif de Base', 3.5);
INSERT INTO Tarif VALUES (2, 'Tarif CAF', 2.8);
INSERT INTO Tarif VALUES (3, 'Tarif DGAC', 0.01);

INSERT INTO TypeDeClasse VALUES (1, 'Maternelle', 'PS');
INSERT INTO TypeDeClasse VALUES (2, 'Maternelle', 'MS');
INSERT INTO TypeDeClasse VALUES (3, 'Maternelle', 'GS');
INSERT INTO TypeDeClasse VALUES (4, 'Primaire', 'CP');
INSERT INTO TypeDeClasse VALUES (5, 'Primaire', 'CE1');
INSERT INTO TypeDeClasse VALUES (6, 'Primaire', 'CE2');
INSERT INTO TypeDeClasse VALUES (7, 'Primaire', 'CM1');
INSERT INTO TypeDeClasse VALUES (8, 'Primaire', 'CM2');

INSERT INTO Classe VALUES (1, 'PS', 1);
INSERT INTO Classe VALUES (2, 'MS', 2);
INSERT INTO Classe VALUES (3, 'GS', 3);
INSERT INTO Classe VALUES (4, 'CP', 4);
INSERT INTO Classe VALUES (5, 'CE1', 5);
INSERT INTO Classe VALUES (6, 'CE2', 6);
INSERT INTO Classe VALUES (7, 'CM1', 7);
INSERT INTO Classe VALUES (8, 'CM2', 8);

INSERT INTO Formule VALUES (1, '1J');
INSERT INTO Formule VALUES (2, '2J');
INSERT INTO Formule VALUES (3, '3J');
INSERT INTO Formule VALUES (4, '4J');
INSERT INTO Formule VALUES (5, 'Occasionnel');

INSERT INTO Jour VALUES (1, 'Lundi');
INSERT INTO Jour VALUES (2, 'Mardi');
INSERT INTO Jour VALUES (3, 'Jeudi');
INSERT INTO Jour VALUES (4, 'Vendredi');

INSERT INTO Enfant VALUES (1, 'ARTALLE', 'Pierre', 1, 1, 1, 5);
INSERT INTO Enfant VALUES (2, 'ARTALLE', 'Paul', 1, 1, 1, 5);
INSERT INTO Enfant VALUES (3, 'ARTALLE', 'Jacques', 1, 1, 1, 5);
INSERT INTO Enfant VALUES (4, 'PHILIPPE', 'Kevin', 2, 8, 22, 5);
INSERT INTO Enfant VALUES (5, 'PHILIPPE', 'Bryan', 2, 2, 22, 5);
INSERT INTO Enfant VALUES (6, 'PHILIPPE', 'Dylan', 2, 4, 22, 5);
INSERT INTO Enfant VALUES (7, 'PHILIPPE', 'Brandon', 5, 1, 22, 5);
INSERT INTO Enfant VALUES (8, 'PHILIPPE', 'Tony', 2, 3, 22, 5);
INSERT INTO Enfant VALUES (9, 'KROGMANN', 'Vanessa', 2, 2, 22, 5);
INSERT INTO Enfant VALUES (10, 'KROGMANN', 'Ashley', 2, 1, 22, 5);
INSERT INTO Enfant VALUES (11, 'KROGMANN', 'Brenda', 2, 6, 22, 5);
INSERT INTO Enfant VALUES (12, 'KROGMANN', 'Cindy', 2, 4, 22, 5);
INSERT INTO Enfant VALUES (13, 'KROGMANN', 'Samanta', 2, 1, 22, 5);
INSERT INTO Enfant VALUES (14, 'DUNEZ', 'Pépito', 1, 2, 10, 5);
INSERT INTO Enfant VALUES (15, 'CHABAUD', 'Pépita', 1, 8, 4, 5);
INSERT INTO Enfant VALUES (16, 'HURSON', 'Petit', 1, 4, 14, 5);
INSERT INTO Enfant VALUES (17, 'HURSON', 'Winnie', 1, 2, 14, 5);
INSERT INTO Enfant VALUES (18, 'CHAMBREY', 'Senlis', 1, 7, 5, 5);
INSERT INTO Enfant VALUES (19, 'CHAMBREY', 'Heineken', 1, 2, 5, 5);
INSERT INTO Enfant VALUES (20, 'CHAMBREY', 'Bud', 1, 7, 5, 5);
INSERT INTO Enfant VALUES (21, 'COLIN', 'Jean-Louis-Eude', 1, 2, 7, 5);
INSERT INTO Enfant VALUES (22, 'COLIN', 'Marie-Eugenie-Sophie', 1, 7, 7, 5);
INSERT INTO Enfant VALUES (23, 'PELOS', 'Jules', 1, 7, 22, 5);

INSERT INTO Enseigne VALUES (1, 1);
INSERT INTO Enseigne VALUES (2, 2);
INSERT INTO Enseigne VALUES (3, 3);
INSERT INTO Enseigne VALUES (4, 4);
INSERT INTO Enseigne VALUES (5, 5);
INSERT INTO Enseigne VALUES (6, 6);
INSERT INTO Enseigne VALUES (7, 7);
INSERT INTO Enseigne VALUES (8, 8);

INSERT INTO Allergie VALUES (1, 'Gluten');
INSERT INTO Allergie VALUES (2, 'Arachides');
INSERT INTO Allergie VALUES (3, 'Fruits de mer');
INSERT INTO Allergie VALUES (4, 'Lactose');
INSERT INTO Allergie VALUES (5, 'Oeufs');
INSERT INTO Allergie VALUES (6, 'Fruits');

INSERT INTO Conge VALUES ('2022-06-30')