-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Wersja serwera:               10.3.39-MariaDB-0+deb10u1 - Debian 10
-- Serwer OS:                    debian-linux-gnu
-- HeidiSQL Wersja:              12.2.0.6576
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Zrzut struktury bazy danych RFID
CREATE DATABASE IF NOT EXISTS `RFID` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `RFID`;

-- Zrzut struktury tabela RFID.konta
CREATE TABLE IF NOT EXISTS `konta` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `login` tinytext NOT NULL,
  `haslo` text NOT NULL,
  `uprawnienia` smallint(6) NOT NULL DEFAULT 0,
  `departments` tinytext DEFAULT NULL,
  `rm_emp` tinyint(4) DEFAULT NULL,
  `add_emp` tinyint(4) DEFAULT NULL,
  `rm_ent` tinyint(4) DEFAULT NULL,
  `add_ent` tinyint(4) DEFAULT NULL,
  `cities` tinytext DEFAULT NULL,
  `id_baza` smallint(6) DEFAULT NULL,
  `tl` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID.konta: ~13 rows (około)
INSERT IGNORE INTO `konta` (`id`, `login`, `haslo`, `uprawnienia`, `departments`, `rm_emp`, `add_emp`, `rm_ent`, `add_ent`, `cities`, `id_baza`, `tl`) VALUES
	(1, 'admin', '506d87a8610c2ec49bf06d99ec60108cd1653807bc5c57e32b339a1cf37ca56c', 777, '1,3,4,5,6,7,9,11,13', 1, 1, 1, 1, NULL, 2, 0),

-- Zrzut struktury tabela RFID.nadgodziny
CREATE TABLE IF NOT EXISTS `nadgodziny` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pracownik` smallint(6) NOT NULL DEFAULT 0,
  `data` date NOT NULL DEFAULT curdate(),
  `nadgodziny` smallint(6) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1967 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzut struktury tabela RFID.obecnosc
CREATE TABLE IF NOT EXISTS `obecnosc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pracownik` smallint(6) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `action` tinyint(4) NOT NULL,
  `komentarz` text DEFAULT NULL,
  `edit` tinytext DEFAULT NULL,
  `edit_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102076 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzut struktury tabela RFID.pracownicy
CREATE TABLE IF NOT EXISTS `pracownicy` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `imie` tinytext NOT NULL,
  `nazwisko` tinytext NOT NULL,
  `palacz` tinyint(4) DEFAULT NULL,
  `dzial` tinyint(4) DEFAULT NULL,
  `lokalizacja` tinyint(4) DEFAULT NULL,
  `teamleader` tinyint(4) DEFAULT NULL,
  `karta` char(50) DEFAULT NULL,
  `umowa` tinyint(4) NOT NULL,
  `firma` tinyint(4) NOT NULL,
  `stanowisko` smallint(6) NOT NULL,
  `unixlogin` char(50) DEFAULT NULL,
  `uprawnienia` tinyint(4) DEFAULT NULL,
  `rcp_h` tinyint(4) NOT NULL DEFAULT 0,
  `active` tinyint(4) DEFAULT NULL,
  `email` tinytext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=734 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID.pracownicy: ~146 rows (około)
INSERT IGNORE INTO `pracownicy` (`id`, `imie`, `nazwisko`, `palacz`, `dzial`, `lokalizacja`, `teamleader`, `karta`, `umowa`, `firma`, `stanowisko`, `unixlogin`, `uprawnienia`, `rcp_h`, `active`, `email`) VALUES
	(1, 'Janusz', 'Testowy', 1, 5, 1, 3, '0002179188', 1, 1, 54, 'jtestowy', 10, 0, 1, 'jtestowy@psm.pl'),
	(2, 'Pan', 'Admin', 0, 11, 1, 3, '0006669188', 1, 1, 54, 'padmin', 10, 0, 1, 'padmin@psm.pl');
	
-- Zrzut struktury tabela RFID._action
CREATE TABLE IF NOT EXISTS `_action` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `action` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._action: ~19 rows (około)
INSERT IGNORE INTO `_action` (`id`, `action`) VALUES
	(1, 'Start pracy'),
	(2, 'Koniec pracy'),
	(3, 'Start przerwy'),
	(4, 'Koniec przerwy'),
	(5, 'Urlop wypoczynkowy'),
	(6, 'Urlop bezpłatny'),
	(7, 'Urlop na żądanie'),
	(8, 'Zwolnienie lekarskie'),
	(9, 'Nieobecność nieusprawiedliwiona'),
	(10, 'Urlop wychowawczy / macierzyński'),
	(11, 'Nieobecność usprawiedliwiona'),
	(12, 'Home Office'),
	(13, 'Nieobecność upsrawiedliwiona / Oddaje krew'),
	(14, 'Urlop okolicznościowy'),
	(15, 'Opieka nad dzieckiem art. 188kp.'),
	(16, 'Nieobecność usprawiedliwiona - zlecenie'),
	(17, 'Delegacja'),
	(18, 'Wyjście w celach służbowych'),
	(19, 'Odbiór nadgodzin'),
	(20, 'Choroba bezpłatna'),
	(21, 'Choroba w trakcie ciąży'),
	(22, 'Szkolenie'),
	(23, 'Urlop Ojcowski'),
	(24, 'Okazjonalna praca zdalna'),
	(25, 'Praca zdalna'),
	(26, 'Urlop rodzicielski');

-- Zrzut struktury tabela RFID._dzial
CREATE TABLE IF NOT EXISTS `_dzial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dzial` tinytext DEFAULT NULL,
  `lokalizacja` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._dzial: ~9 rows (około)
INSERT IGNORE INTO `_dzial` (`id`, `dzial`, `lokalizacja`) VALUES
	(1, 'Kadry i Ksiegowosc', 1),
	(2, 'Biuro', 1),
	(3, 'Magazyn', 1),
	(4, 'Logistyka', 1),
	(5, 'Serwis', 1),
	(6, 'Zakupy', 1),
	(7, 'Wsparcie sprzedaży', 1),
	(8, 'Sprzedaż', 2),
	(9, 'Marketing', 2),
	(10, 'PdaIT', 2),
	(11, 'Margines', 1),
	(12, 'INNE', 3);

-- Zrzut struktury tabela RFID._firma
CREATE TABLE IF NOT EXISTS `_firma` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `firma` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._firma: ~5 rows (około)
INSERT IGNORE INTO `_firma` (`id`, `firma`) VALUES
	(1, 'Krzak'),
	(2, 'PSM Company');


-- Zrzut struktury tabela RFID._lokalizacja
CREATE TABLE IF NOT EXISTS `_lokalizacja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `miasto` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._lokalizacja: ~2 rows (około)
INSERT IGNORE INTO `_lokalizacja` (`id`, `miasto`) VALUES
	(1, 'Far Far Away'),
	(2, 'Warszawa'),
	(3, 'INNE');

-- Zrzut struktury tabela RFID._palacz
CREATE TABLE IF NOT EXISTS `_palacz` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `stan` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._palacz: ~2 rows (około)
INSERT IGNORE INTO `_palacz` (`id`, `stan`) VALUES
	(0, 'nie'),
	(1, 'tak');

-- Zrzut struktury tabela RFID._stanowisko
CREATE TABLE IF NOT EXISTS `_stanowisko` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `stanowisko` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._stanowisko: ~59 rows (około)
INSERT IGNORE INTO `_stanowisko` (`id`, `stanowisko`) VALUES
	(1, 'Architekt Procesów Biznesowych'),
	(2, 'Asystent Biura'),
	(3, 'Asystent ds. Administracji'),
	(4, 'Asystent Działu Handlowego'),
	(5, 'Asystent Działu Księgowości'),
	(6, 'Asystent Działu Magazynu'),
	(7, 'Asystent Działu Marketingu'),
	(8, 'Asystent Działu Sprzedaży'),
	(9, 'Dyrektor Operacyjny Centrum Serwisowego'),
	(10, 'Dyrektor Sprzedaży i Marketingu'),
	(11, 'Główna Księgowa'),
	(12, 'Artysta Grafik Komputerowy'),
	(13, 'Informatyk'),
	(14, 'IT Project Manager '),
	(15, 'Kierownik ds. Technicznych'),
	(16, 'Kierownik Działu Administracji'),
	(17, 'Kierownik Działu Logistyki'),
	(18, 'Kierownik Działu Marketingu'),
	(19, 'Kierownik Działu Rozwoju'),
	(20, 'Kierownik Działu Sprzedaży'),
	(21, 'Kierownik Działu Zakupów'),
	(22, 'Kierownik Magazynu'),
	(23, 'Kierownik Serwisu'),
	(24, 'Koordynator Administracji'),
	(25, 'Koordynator Działu Logistyki'),
	(26, 'Koordynator Magazynu'),
	(27, 'Koordynator Serwisu i Magazynu'),
	(28, 'Koordynator Sprzedaży'),
	(29, 'Samodzielna Księgowa'),
	(30, 'Marketing Project Manager'),
	(31, 'Młodszy Koordynator Działu Logistyki'),
	(32, 'Młodszy koordynator magazynu'),
	(33, 'Młodszy Koordynator Sprzedaży'),
	(34, 'Młodszy Koordynator Sprzedaży Internetowej'),
	(35, 'Młodszy Serwisant'),
	(36, 'Młodszy Serwisant/QC'),
	(37, 'Młodszy Specjalista ds. Kadr'),
	(38, 'Młodszy Specjalista ds. Zakupów'),
	(39, 'Młodszy Specjalista Marketingu Internetowego'),
	(40, 'P.O Kierownik Serwisu'),
	(41, 'PO Regionalnego Kierownika Sprzedaży'),
	(42, 'Regionalny Kierownik Sprzedaży'),
	(43, 'Sekretarka'),
	(44, 'Serwisant'),
	(45, 'Specjalista ds. Kadr'),
	(46, 'Specjalista ds. Kadr i Płac'),
	(47, 'Specjalista ds. Marketingu '),
	(48, 'Specjalista ds. sprzedaży'),
	(49, 'Specjalista ds. Sprzedaży (Opiekun Platformy B2B)'),
	(50, 'Specjalista ds. Zakupów'),
	(51, 'Specjalista Komunikacji Marketingowej'),
	(52, 'Specjalista Marketingu Internetowego'),
	(53, 'Starszy Koordynator Działu Logistyki'),
	(54, 'Starszy Serwisant'),
	(55, 'Kierownik Zespołu'),
	(56, 'Właściciel firmy'),
	(57, 'Zastępca Kierownika Działu Administracji'),
	(58, 'Zastępca Kierownika Działu Sprzedaży'),
	(59, 'Zastępca Kierownika Logistyki '),
	(60, 'Kierownik Zamieszania'),
	(61, 'CEO PDA UK'),
	(62, 'Inżynier rozwiązań technicznych'),
	(63, 'Praktykant'),
	(64, 'Młodsza Księgowa'),
	(65, 'Samodzielna Księgowa'),
	(66, 'Specjalista ds. Logistyki'),
	(67, 'Zastępca Kierownika Działu Zakupów'),
	(68, 'Project Manager'),
	(69, 'ND'),
	(70, 'Księgowa'),
	(71, 'Project Manager');

-- Zrzut struktury tabela RFID._team
CREATE TABLE IF NOT EXISTS `_team` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `teamleader` char(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._team: ~9 rows (około)
INSERT IGNORE INTO `_team` (`id`, `teamleader`) VALUES
	(1, 'Pan Areczek');


-- Zrzut struktury tabela RFID._umowa
CREATE TABLE IF NOT EXISTS `_umowa` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `rodzaj` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._umowa: ~3 rows (około)
INSERT IGNORE INTO `_umowa` (`id`, `rodzaj`) VALUES
	(1, 'Umowa o pracę'),
	(2, 'Umowa zlecenie'),
	(3, 'Umowa o dzieło'),
	(4, 'Praktyki'),
	(5, 'ND');

-- Zrzut struktury tabela RFID._uprawnienia
CREATE TABLE IF NOT EXISTS `_uprawnienia` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `uprawnienia` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=778 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Zrzucanie danych dla tabeli RFID._uprawnienia: ~16 rows (około)
INSERT IGNORE INTO `_uprawnienia` (`id`, `uprawnienia`) VALUES
	(1, 'Kadry i Ksiegowosc'),
	(2, 'Biuro'),
	(3, 'Magazyn'),
	(4, 'Logistyka'),
	(5, 'Serwis'),
	(9, 'Sprzedaz'),
	(11, 'Marketing'),
	(12, 'PdaIT'),
	(13, 'Margines'),
	(51, 'Team Radek'),
	(52, 'Team Ania'),
	(53, 'Team Jacek'),
	(54, 'Team Norbert'),
	(100, 'FarAway_ALL'),
	(200, 'Warszawa_ALL'),
	(777, 'FULL');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
