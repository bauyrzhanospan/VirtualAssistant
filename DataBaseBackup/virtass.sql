-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Дек 11 2017 г., 17:47
-- Версия сервера: 5.7.20-0ubuntu0.16.04.1
-- Версия PHP: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `virtass`
--

-- --------------------------------------------------------

--
-- Структура таблицы `cases`
--
-- Создание: Ноя 28 2017 г., 22:09
--

CREATE TABLE `cases` (
  `id` int(11) NOT NULL,
  `usertypeIN` varchar(15) DEFAULT NULL,
  `usertypeOUT` varchar(15) DEFAULT NULL,
  `reasonIN` varchar(15) DEFAULT NULL,
  `reasonOUT` varchar(15) DEFAULT NULL,
  `output` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `cases`
--

INSERT INTO `cases` (`id`, `usertypeIN`, `usertypeOUT`, `reasonIN`, `reasonOUT`, `output`) VALUES
(0, 'adult', 'adult', 'energy', 'entertainment', 1),
(1, 'adult', 'adult', 'energy', 'health', 0),
(2, 'adult', 'adult', 'energy', 'work', 0),
(3, 'adult', 'adult', 'entertainment', 'energy', 0),
(4, 'adult', 'adult', 'entertainment', 'health', 0),
(5, 'adult', 'adult', 'food', 'energy', 1),
(6, 'adult', 'adult', 'food', 'entertainment', 1),
(7, 'adult', 'adult', 'food', 'food', 0),
(8, 'adult', 'adult', 'food', 'health', 0),
(9, 'adult', 'adult', 'food', 'work', 0),
(10, 'adult', 'adult', 'health', 'energy', 1),
(11, 'adult', 'adult', 'health', 'entertainment', 1),
(12, 'adult', 'adult', 'health', 'food', 1),
(13, 'adult', 'adult', 'health', 'health', 0),
(14, 'adult', 'adult', 'health', 'security', 1),
(15, 'adult', 'adult', 'health', 'work', 1),
(16, 'adult', 'adult', 'security', 'energy', 1),
(17, 'adult', 'adult', 'security', 'food', 1),
(18, 'adult', 'adult', 'security', 'health', 1),
(19, 'adult', 'adult', 'security', 'work', 1),
(20, 'adult', 'adult', 'work', 'energy', 1),
(21, 'adult', 'adult', 'work', 'entertainment', 1),
(22, 'adult', 'adult', 'work', 'food', 1),
(23, 'adult', 'adult', 'work', 'health', 0),
(24, 'adult', 'adult', 'work', 'security', 0),
(25, 'adult', 'adult', 'work', 'work', 0),
(26, 'adult', 'young', 'energy', 'energy', 1),
(27, 'adult', 'young', 'energy', 'entertainment', 1),
(28, 'adult', 'young', 'energy', 'food', 1),
(29, 'adult', 'young', 'energy', 'health', 0),
(30, 'adult', 'young', 'energy', 'security', 1),
(31, 'adult', 'young', 'entertainment', 'energy', 1),
(32, 'adult', 'young', 'entertainment', 'entertainment', 1),
(33, 'adult', 'young', 'entertainment', 'food', 1),
(34, 'adult', 'young', 'entertainment', 'health', 0),
(35, 'adult', 'young', 'entertainment', 'work', 1),
(36, 'adult', 'young', 'food', 'energy', 1),
(37, 'adult', 'young', 'food', 'entertainment', 1),
(38, 'adult', 'young', 'food', 'food', 1),
(39, 'adult', 'young', 'food', 'health', 0),
(40, 'adult', 'young', 'food', 'security', 1),
(41, 'adult', 'young', 'food', 'work', 1),
(42, 'adult', 'young', 'health', 'energy', 1),
(43, 'adult', 'young', 'health', 'health', 1),
(44, 'adult', 'young', 'health', 'security', 1),
(45, 'adult', 'young', 'health', 'work', 1),
(46, 'adult', 'young', 'security', 'energy', 1),
(47, 'adult', 'young', 'security', 'entertainment', 1),
(48, 'adult', 'young', 'security', 'food', 1),
(49, 'adult', 'young', 'security', 'health', 1),
(50, 'adult', 'young', 'security', 'security', 1),
(51, 'adult', 'young', 'security', 'work', 1),
(52, 'adult', 'young', 'work', 'energy', 1),
(53, 'adult', 'young', 'work', 'entertainment', 1),
(54, 'adult', 'young', 'work', 'food', 1),
(55, 'adult', 'young', 'work', 'health', 0),
(56, 'adult', 'young', 'work', 'security', 1),
(57, 'adult', 'young', 'work', 'work', 1),
(58, 'adult', 'elder', 'energy', 'energy', 1),
(59, 'adult', 'elder', 'energy', 'entertainment', 1),
(60, 'adult', 'elder', 'energy', 'health', 0),
(61, 'adult', 'elder', 'energy', 'security', 1),
(62, 'adult', 'elder', 'energy', 'work', 1),
(63, 'adult', 'elder', 'entertainment', 'energy', 1),
(64, 'adult', 'elder', 'entertainment', 'entertainment', 1),
(65, 'adult', 'elder', 'entertainment', 'food', 1),
(66, 'adult', 'elder', 'entertainment', 'health', 0),
(67, 'adult', 'elder', 'entertainment', 'security', 1),
(68, 'adult', 'elder', 'entertainment', 'work', 1),
(69, 'adult', 'elder', 'food', 'food', 1),
(70, 'adult', 'elder', 'food', 'health', 0),
(71, 'adult', 'elder', 'food', 'security', 1),
(72, 'adult', 'elder', 'food', 'work', 1),
(73, 'adult', 'elder', 'health', 'energy', 1),
(74, 'adult', 'elder', 'health', 'entertainment', 1),
(75, 'adult', 'elder', 'health', 'food', 1),
(76, 'adult', 'elder', 'health', 'health', 1),
(77, 'adult', 'elder', 'health', 'security', 1),
(78, 'adult', 'elder', 'health', 'work', 1),
(79, 'adult', 'elder', 'security', 'energy', 1),
(80, 'adult', 'elder', 'security', 'food', 1),
(81, 'adult', 'elder', 'security', 'health', 1),
(82, 'adult', 'elder', 'security', 'security', 1),
(83, 'adult', 'elder', 'work', 'energy', 1),
(84, 'adult', 'elder', 'work', 'entertainment', 1),
(85, 'adult', 'elder', 'work', 'food', 1),
(86, 'adult', 'elder', 'work', 'health', 0),
(87, 'adult', 'elder', 'work', 'security', 1),
(88, 'adult', 'elder', 'work', 'work', 1),
(89, 'young', 'adult', 'energy', 'energy', 0),
(90, 'young', 'adult', 'energy', 'health', 0),
(91, 'young', 'adult', 'energy', 'security', 0),
(92, 'young', 'adult', 'energy', 'work', 0),
(93, 'young', 'adult', 'entertainment', 'energy', 0),
(94, 'young', 'adult', 'entertainment', 'entertainment', 0),
(95, 'young', 'adult', 'entertainment', 'food', 0),
(96, 'young', 'adult', 'entertainment', 'health', 0),
(97, 'young', 'adult', 'entertainment', 'security', 0),
(98, 'young', 'adult', 'entertainment', 'work', 0),
(99, 'young', 'adult', 'food', 'food', 0),
(100, 'young', 'adult', 'food', 'health', 0),
(101, 'young', 'adult', 'food', 'security', 0),
(102, 'young', 'adult', 'food', 'work', 0),
(103, 'young', 'adult', 'health', 'energy', 1),
(104, 'young', 'adult', 'health', 'entertainment', 1),
(105, 'young', 'adult', 'health', 'food', 1),
(106, 'young', 'adult', 'health', 'health', 0),
(107, 'young', 'adult', 'health', 'security', 1),
(108, 'young', 'adult', 'health', 'work', 1),
(109, 'young', 'adult', 'security', 'energy', 0),
(110, 'young', 'adult', 'security', 'entertainment', 0),
(111, 'young', 'adult', 'security', 'food', 0),
(112, 'young', 'adult', 'security', 'health', 1),
(113, 'young', 'adult', 'security', 'security', 0),
(114, 'young', 'adult', 'work', 'energy', 0),
(115, 'young', 'adult', 'work', 'entertainment', 0),
(116, 'young', 'adult', 'work', 'food', 0),
(117, 'young', 'adult', 'work', 'health', 0),
(118, 'young', 'adult', 'work', 'work', 0),
(119, 'young', 'elder', 'energy', 'entertainment', 0),
(120, 'young', 'elder', 'energy', 'food', 0),
(121, 'young', 'elder', 'energy', 'health', 0),
(122, 'young', 'elder', 'energy', 'security', 0),
(123, 'young', 'elder', 'entertainment', 'energy', 0),
(124, 'young', 'elder', 'entertainment', 'entertainment', 0),
(125, 'young', 'elder', 'entertainment', 'food', 0),
(126, 'young', 'elder', 'entertainment', 'health', 0),
(127, 'young', 'elder', 'food', 'energy', 0),
(128, 'young', 'elder', 'food', 'entertainment', 0),
(129, 'young', 'elder', 'food', 'food', 0),
(130, 'young', 'elder', 'food', 'health', 0),
(131, 'young', 'elder', 'food', 'security', 0),
(132, 'young', 'elder', 'health', 'energy', 1),
(133, 'young', 'elder', 'health', 'entertainment', 1),
(134, 'young', 'elder', 'health', 'health', 0),
(135, 'young', 'elder', 'health', 'security', 1),
(136, 'young', 'elder', 'health', 'work', 1),
(137, 'young', 'elder', 'security', 'energy', 0),
(138, 'young', 'elder', 'security', 'food', 0),
(139, 'young', 'elder', 'security', 'health', 1),
(140, 'young', 'elder', 'security', 'work', 0),
(141, 'young', 'elder', 'work', 'energy', 0),
(142, 'young', 'elder', 'work', 'entertainment', 0),
(143, 'young', 'elder', 'work', 'food', 0),
(144, 'young', 'elder', 'work', 'health', 0),
(145, 'elder', 'adult', 'energy', 'energy', 0),
(146, 'elder', 'adult', 'energy', 'entertainment', 0),
(147, 'elder', 'adult', 'energy', 'food', 0),
(148, 'elder', 'adult', 'energy', 'health', 0),
(149, 'elder', 'adult', 'energy', 'security', 0),
(150, 'elder', 'adult', 'energy', 'work', 0),
(151, 'elder', 'adult', 'entertainment', 'energy', 0),
(152, 'elder', 'adult', 'entertainment', 'entertainment', 0),
(153, 'elder', 'adult', 'entertainment', 'health', 0),
(154, 'elder', 'adult', 'entertainment', 'security', 0),
(155, 'elder', 'adult', 'entertainment', 'work', 0),
(156, 'elder', 'adult', 'food', 'energy', 0),
(157, 'elder', 'adult', 'food', 'entertainment', 0),
(158, 'elder', 'adult', 'food', 'food', 0),
(159, 'elder', 'adult', 'food', 'health', 0),
(160, 'elder', 'adult', 'food', 'work', 0),
(161, 'elder', 'adult', 'health', 'entertainment', 1),
(162, 'elder', 'adult', 'health', 'food', 1),
(163, 'elder', 'adult', 'health', 'security', 1),
(164, 'elder', 'adult', 'security', 'energy', 0),
(165, 'elder', 'adult', 'security', 'food', 0),
(166, 'elder', 'adult', 'security', 'health', 1),
(167, 'elder', 'adult', 'security', 'security', 0),
(168, 'elder', 'adult', 'security', 'work', 0),
(169, 'elder', 'adult', 'work', 'energy', 0),
(170, 'elder', 'adult', 'work', 'entertainment', 0),
(171, 'elder', 'adult', 'work', 'food', 0),
(172, 'elder', 'adult', 'work', 'health', 0),
(173, 'elder', 'adult', 'work', 'security', 0),
(174, 'elder', 'adult', 'work', 'work', 0),
(175, 'elder', 'young', 'energy', 'energy', 1),
(176, 'elder', 'young', 'energy', 'entertainment', 1),
(177, 'elder', 'young', 'energy', 'health', 0),
(178, 'elder', 'young', 'energy', 'work', 1),
(179, 'elder', 'young', 'entertainment', 'energy', 1),
(180, 'elder', 'young', 'entertainment', 'entertainment', 1),
(181, 'elder', 'young', 'entertainment', 'food', 1),
(182, 'elder', 'young', 'entertainment', 'health', 0),
(183, 'elder', 'young', 'entertainment', 'security', 1),
(184, 'elder', 'young', 'entertainment', 'work', 1),
(185, 'elder', 'young', 'food', 'energy', 1),
(186, 'elder', 'young', 'food', 'entertainment', 1),
(187, 'elder', 'young', 'food', 'food', 1),
(188, 'elder', 'young', 'food', 'health', 0),
(189, 'elder', 'young', 'food', 'work', 1),
(190, 'elder', 'young', 'health', 'energy', 1),
(191, 'elder', 'young', 'health', 'entertainment', 1),
(192, 'elder', 'young', 'health', 'food', 1),
(193, 'elder', 'young', 'health', 'health', 1),
(194, 'elder', 'young', 'health', 'security', 1),
(195, 'elder', 'young', 'health', 'work', 1),
(196, 'elder', 'young', 'security', 'entertainment', 1),
(197, 'elder', 'young', 'security', 'food', 1),
(198, 'elder', 'young', 'security', 'security', 1),
(199, 'elder', 'young', 'work', 'energy', 1),
(200, 'elder', 'young', 'work', 'entertainment', 1),
(201, 'elder', 'young', 'work', 'food', 1),
(202, 'elder', 'young', 'work', 'health', 0),
(203, 'elder', 'young', 'work', 'security', 1),
(204, 'elder', 'young', 'work', 'work', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `eval`
--
-- Создание: Дек 07 2017 г., 22:48
-- Последнее обновление: Дек 11 2017 г., 17:44
--

CREATE TABLE `eval` (
  `id` int(11) NOT NULL,
  `user` varchar(20) DEFAULT NULL,
  `otheruser` varchar(20) DEFAULT NULL,
  `ordertype` varchar(20) DEFAULT NULL,
  `rulereason` varchar(20) DEFAULT NULL,
  `reason` varchar(20) DEFAULT NULL,
  `orderraw` varchar(80) DEFAULT NULL,
  `orderdef` varchar(20) DEFAULT NULL,
  `reasonraw` varchar(80) DEFAULT NULL,
  `reasondef` varchar(20) DEFAULT NULL,
  `output` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `eval`
--

INSERT INTO `eval` (`id`, `user`, `otheruser`, `ordertype`, `rulereason`, `reason`, `orderraw`, `orderdef`, `reasonraw`, `reasondef`, `output`) VALUES
(1, 'adult', 'young', 'LampOn', 'health', 'work', 'turn on the lamp, please', NULL, 'I am ill today', NULL, 1),
(2, 'adult', 'elder', 'KettleOff', 'entertainment', 'security', 'turn off the kettle', 'KettleOff', 'i will have a party', 'Entertainment', 1),
(3, 'adult', 'elder', 'KettleOff', 'security', 'entertainment', NULL, NULL, NULL, NULL, NULL),
(4, 'adult', 'young', 'LampOn', 'security', 'health', 'faggot, turn the lamp on', 'LampOn', 'i broke my leg', 'Health', 1),
(5, 'adult', 'adult', 'KettleOn', 'entertainment', 'health', 'turn on the kettle', 'KettleOn', 'I have a flu', 'Health', 1),
(6, 'elder', 'young', 'LampOff', 'health', 'work', 'turn off that lamp', 'LampOff', 'I have a project', 'Work', 1),
(7, 'young', 'adult', 'KettleOff', 'security', 'entertainment', 'iawduyawuyfawf', NULL, NULL, NULL, NULL),
(8, 'adult', 'adult', 'KettleOn', 'energy', 'work', 'Turn off the pot', 'KettleOff', NULL, NULL, NULL),
(9, 'young', 'young', 'LampOn', 'food', 'health', NULL, NULL, NULL, NULL, NULL),
(10, 'adult', 'young', 'LampOn', 'food', 'security', NULL, NULL, NULL, NULL, NULL),
(11, 'adult', 'young', 'LampOn', 'security', 'energy', NULL, NULL, NULL, NULL, NULL),
(12, 'young', 'young', 'LampOn', 'food', 'health', NULL, NULL, NULL, NULL, NULL),
(13, 'elder', 'adult', 'LampOn', 'health', 'energy', NULL, NULL, NULL, NULL, NULL),
(14, 'elder', 'adult', 'KettleOn', 'entertainment', 'work', NULL, NULL, NULL, NULL, NULL),
(15, 'adult', 'adult', 'KettleOn', 'energy', 'entertainment', NULL, NULL, NULL, NULL, NULL),
(16, 'adult', 'young', 'LampOn', 'security', 'food', NULL, NULL, NULL, NULL, NULL),
(17, 'elder', 'adult', 'LampOn', 'health', 'work', NULL, NULL, NULL, NULL, NULL),
(18, 'adult', 'elder', 'KettleOn', 'work', 'health', NULL, NULL, NULL, NULL, NULL),
(19, 'young', 'adult', 'LampOn', 'entertainment', 'health', NULL, NULL, NULL, NULL, NULL),
(20, 'adult', 'adult', 'KettleOn', 'security', 'security', 'turn the kettle on', 'KettleOn', 'i need to kill a spider', NULL, NULL),
(21, 'young', 'adult', 'KettleOn', 'energy', 'entertainment', 'turn me kettle', 'KettleOn', 'i have guests', NULL, NULL),
(22, 'adult', 'young', 'KettleOff', 'entertainment', 'work', 'turn it off', 'KettleOff', 'its sound disturbs my work', NULL, NULL),
(23, 'young', 'adult', 'LampOn', 'work', 'health', 'turn on the light', 'LampOn', 'too dark for my eyes', 'Health', 1),
(24, 'young', 'elder', 'LampOff', 'entertainment', 'energy', 'switch off the lamp', 'LampOff', NULL, NULL, NULL),
(25, 'young', 'elder', 'LampOff', 'energy', 'entertainment', 'lamp off', 'LampOff', 'i am watching a movie', 'Entertainment', 1),
(26, 'adult', 'adult', 'KettleOn', 'work', 'entertainment', 'kettle on', 'KettleOn', 'i have chocolate', 'Health', 1),
(27, 'young', 'elder', 'LampOn', 'entertainment', 'work', 'lights on', 'LampOn', 'i am studying ', 'Work', 1),
(28, 'adult', 'young', 'LampOff', 'work', 'security', NULL, NULL, NULL, NULL, NULL),
(29, 'elder', 'adult', 'KettleOn', 'work', 'health', 'teapot on', 'KettleOn', 'I am ill', 'Health', 1),
(30, 'elder', 'adult', 'LampOn', 'entertainment', 'security', 'lights on', 'LampOn', 'killer is walking near home', 'Security', 1),
(31, 'elder', 'young', 'LampOn', 'food', 'entertainment', 'light on', 'LampOn', 'I will have a party with jack and casino', 'Entertainment', 1),
(32, 'elder', 'adult', 'KettleOff', 'food', 'entertainment', NULL, NULL, NULL, NULL, NULL),
(33, 'adult', 'elder', 'KettleOff', 'energy', 'security', NULL, NULL, NULL, NULL, NULL),
(34, 'adult', 'elder', 'LampOn', 'food', 'security', NULL, NULL, NULL, NULL, NULL),
(35, 'adult', 'elder', 'KettleOff', 'work', 'energy', NULL, NULL, NULL, NULL, NULL),
(36, 'elder', 'adult', 'KettleOff', 'entertainment', 'energy', NULL, NULL, NULL, NULL, NULL),
(37, 'adult', 'adult', 'KettleOff', 'security', 'entertainment', NULL, NULL, NULL, NULL, NULL),
(38, 'young', 'adult', 'KettleOff', 'food', 'security', NULL, NULL, NULL, NULL, NULL),
(39, 'adult', 'young', 'LampOn', 'security', 'food', NULL, NULL, NULL, NULL, NULL),
(40, 'young', 'elder', 'KettleOff', 'energy', 'food', NULL, NULL, NULL, NULL, NULL),
(41, 'adult', 'young', 'LampOn', 'health', 'energy', NULL, NULL, NULL, NULL, NULL),
(42, 'adult', 'young', 'KettleOff', 'work', 'entertainment', 'turn off the kitchen', 'KettleOff', 'I want to watch TV', 'Entertainment', 1),
(43, 'adult', 'adult', 'LampOn', 'entertainment', 'work', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `preferences`
--
-- Создание: Ноя 28 2017 г., 21:56
--

CREATE TABLE `preferences` (
  `id` int(11) NOT NULL,
  `user` varchar(15) DEFAULT NULL,
  `usertype` varchar(15) DEFAULT NULL,
  `energy` int(11) DEFAULT NULL,
  `entertainment` int(11) DEFAULT NULL,
  `food` int(11) DEFAULT NULL,
  `health` int(11) DEFAULT NULL,
  `security` int(11) DEFAULT NULL,
  `work` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `preferences`
--

INSERT INTO `preferences` (`id`, `user`, `usertype`, `energy`, `entertainment`, `food`, `health`, `security`, `work`) VALUES
(0, 'father', 'adult', 4, 5, 3, 1, 0, 2),
(1, 'mother', 'adult', 4, 5, 3, 1, 0, 2),
(2, 'grandpa', 'elder', 3, 4, 2, 0, 1, 5),
(3, 'son', 'young', 5, 2, 4, 3, 0, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `rules`
--
-- Создание: Дек 04 2017 г., 17:15
-- Последнее обновление: Дек 11 2017 г., 17:44
--

CREATE TABLE `rules` (
  `id` int(11) NOT NULL,
  `start` time DEFAULT NULL,
  `stop` time DEFAULT NULL,
  `reason` varchar(15) DEFAULT NULL,
  `user` varchar(15) DEFAULT NULL,
  `device` varchar(15) DEFAULT NULL,
  `status` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `rules`
--

INSERT INTO `rules` (`id`, `start`, `stop`, `reason`, `user`, `device`, `status`) VALUES
(0, '00:00:00', '23:59:00', 'entertainment', 'adult', 'lamp', 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `cases`
--
ALTER TABLE `cases`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `eval`
--
ALTER TABLE `eval`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Индексы таблицы `preferences`
--
ALTER TABLE `preferences`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `rules`
--
ALTER TABLE `rules`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `eval`
--
ALTER TABLE `eval`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
