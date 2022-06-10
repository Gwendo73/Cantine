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
  type_classe TEXT NOT NULL
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
-- Structure de la table `Enfant`
--

CREATE TABLE IF NOT EXISTS Enfant (
  code_enfant integer primary key autoincrement,
  nom_enfant TEXT NOT NULL,
  prenom_enfant TEXT NOT NULL,
  code_tarif integer NOT NULL,
  code_classe integer NOT NULL,
  code_representant integer NOT NULL,
  FOREIGN KEY (code_tarif) REFERENCES Tarif(code_tarif),
  FOREIGN KEY (code_classe) REFERENCES Classe(code_classe),
  FOREIGN KEY (code_representant) REFERENCES Representant(code_representant)
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
  FOREIGN KEY (code_classe) REFERENCES Enseigne(code_classe)
);

INSERT INTO Compte VALUES ('admin', 'admin', 'Admin');
INSERT INTO Compte VALUES ('gartalle', 'test', 'Representant');
INSERT INTO Compte VALUES ('bdarties', 'test', 'Enseignant');

INSERT INTO Enseignant VALUES (1, 'DARTIES', 'Benoit', 'bdarties');
INSERT INTO Representant VALUES (1, 'ARTALLE', 'Gwendal', '0647396010', 'gwendal.artalle73@gmail.com', 'gartalle');

INSERT INTO Tarif VALUES (1, 3.5);

INSERT INTO TypeDeClasse VALUES (1, 'Primaire');
INSERT INTO TypeDeClasse VALUES (2, 'Maternelle');

INSERT INTO Classe VALUES (1, 'CP', 1);

INSERT INTO Enfant VALUES (1, 'ARTALLE', 'Pierre', 1, 1, 1);
INSERT INTO Enfant VALUES (2, 'ARTALLE', 'Paul', 1, 1, 1);
INSERT INTO Enfant VALUES (3, 'ARTALLE', 'Jacques', 1, 1, 1);

INSERT INTO Repas VALUES (1, '2022-06-07', 1);
