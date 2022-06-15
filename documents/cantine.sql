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

INSERT INTO Compte VALUES ('admin', 'admin', 'Admin');
INSERT INTO Compte VALUES ('gartalle', 'test', 'Representant');
INSERT INTO Compte VALUES ('clem', 'test', 'Representant');
INSERT INTO Compte VALUES ('churson', 'churson', 'Representant');
INSERT INTO Compte VALUES ('ajacquemin', 'test', 'Enseignant');
INSERT INTO Compte VALUES ('jneymar', 'jneymar', 'Enseignant');

INSERT INTO Enseignant VALUES (1, 'JACQUEMIN', 'Alexis', 'ajacquemin');
INSERT INTO Enseignant VALUES (2, 'NEYMAR', 'Jean', 'jneymar');

INSERT INTO Representant VALUES (1, 'ARTALLE', 'Gwendal', '0647396010', 'gwendal.artalle73@gmail.com', 'gartalle');
INSERT INTO Representant VALUES (2, 'PHILIPPE', 'Clementine', '0655108310', 'clemclem@gmail.com', 'clem');
INSERT INTO Representant VALUES (3, 'HURSON', 'Cesar', '0625408670', 'cesar.hurson@dgac.fr', 'churson');

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

INSERT INTO Enfant VALUES (1, 'ARTALLE', 'Pierre', 1, 1, 1, 1);
INSERT INTO Enfant VALUES (2, 'ARTALLE', 'Paul', 1, 1, 1, 1);
INSERT INTO Enfant VALUES (3, 'ARTALLE', 'Jacques', 1, 1, 1, 2);

INSERT INTO Mange VALUES (1, 1);
INSERT INTO Mange VALUES (2, 2);
INSERT INTO Mange VALUES (3, 3);
INSERT INTO Mange VALUES (4, 3);

INSERT INTO Enseigne VALUES (1, 1);

INSERT INTO Repas VALUES (1, '2022-06-16', 1);
INSERT INTO Repas VALUES (2, '2022-06-16', 2);
INSERT INTO Repas VALUES (3, '2022-06-16', 3);
INSERT INTO Repas VALUES (4, '2022-06-17', 1);

INSERT INTO Allergie VALUES (1, 'Gluten');
INSERT INTO Allergie VALUES (2, 'Arachides');
INSERT INTO Allergie VALUES (3, 'Fruits de mer');
INSERT INTO Allergie VALUES (4, 'Lactose');
INSERT INTO Allergie VALUES (5, 'Oeufs');
INSERT INTO Allergie VALUES (6, 'Fruits');

INSERT INTO EstAllergiqueA VALUES (1, 1);

INSERT INTO Conge VALUES ('2022-06-23')
