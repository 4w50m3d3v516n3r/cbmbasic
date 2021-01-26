import pprint
import re

bool = [ 'v54', 'v55', 'v562', 'v563', 'v726', 'v727', 'v965', 'v966', 'v3102', 'v3103', 'v3875', 'v3876' ]
eightbit = [ 'v2', 'v3', 'v4', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v15', 'v16', 'v17', 'v18', 'v19', 'v20', 'v21', 'v22', 'v23', 'v24', 'v26', 'v29', 'v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v41', 'v42', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49', 'v50', 'v51', 'v52', 'v53', 'v56', 'v57', 'v58', 'v59', 'v60', 'v61', 'v63', 'v64', 'v65', 'v66', 'v67', 'v68', 'v69', 'v70', 'v71', 'v76', 'v77', 'v78', 'v79', 'v80', 'v81', 'v82', 'v83', 'v86', 'v87', 'v88', 'v92', 'v93', 'v94', 'v95', 'v96', 'v97', 'v98', 'v99', 'v100', 'v103', 'v104', 'v105', 'v106', 'v107', 'v108', 'v109', 'v110', 'v111', 'v112', 'v113', 'v114', 'v115', 'v117', 'v118', 'v119', 'v120', 'v121', 'v122', 'v123', 'v124', 'v125', 'v126', 'v127', 'v128', 'v129', 'v130', 'v132', 'v133', 'v134', 'v135', 'v136', 'v138', 'v140', 'v141', 'v142', 'v146', 'v147', 'v148', 'v149', 'v151', 'v152', 'v153', 'v154', 'v157', 'v158', 'v159', 'v162', 'v163', 'v164', 'v165', 'v166', 'v167', 'v168', 'v169', 'v170', 'v171', 'v172', 'v173', 'v174', 'v175', 'v176', 'v177', 'v178', 'v179', 'v180', 'v181', 'v184', 'v185', 'v188', 'v189', 'v190', 'v191', 'v192', 'v193', 'v195', 'v196', 'v197', 'v198', 'v199', 'v200', 'v201', 'v202', 'v203', 'v204', 'v205', 'v206', 'v207', 'v208', 'v209', 'v210', 'v211', 'v212', 'v213', 'v214', 'v216', 'v218', 'v219', 'v220', 'v221', 'v222', 'v223', 'v227', 'v228', 'v229', 'v230', 'v231', 'v232', 'v233', 'v234', 'v235', 'v236', 'v238', 'v239', 'v240', 'v241', 'v242', 'v243', 'v244', 'v245', 'v246', 'v248', 'v249', 'v250', 'v251', 'v252', 'v253', 'v254', 'v255', 'v257', 'v258', 'v259', 'v260', 'v261', 'v262', 'v263', 'v265', 'v267', 'v268', 'v269', 'v270', 'v271', 'v274', 'v275', 'v276', 'v279', 'v280', 'v281', 'v282', 'v283', 'v285', 'v286', 'v287', 'v288', 'v290', 'v291', 'v292', 'v295', 'v296', 'v297', 'v298', 'v299', 'v300', 'v301', 'v302', 'v304', 'v305', 'v306', 'v308', 'v309', 'v310', 'v311', 'v312', 'v313', 'v314', 'v315', 'v317', 'v318', 'v319', 'v320', 'v321', 'v322', 'v323', 'v324', 'v325', 'v326', 'v327', 'v328', 'v329', 'v330', 'v331', 'v332', 'v334', 'v335', 'v336', 'v337', 'v338', 'v339', 'v340', 'v341', 'v342', 'v343', 'v344', 'v345', 'v346', 'v347', 'v348', 'v349', 'v350', 'v351', 'v352', 'v354', 'v355', 'v356', 'v357', 'v358', 'v359', 'v360', 'v361', 'v362', 'v363', 'v364', 'v365', 'v366', 'v367', 'v368', 'v369', 'v370', 'v371', 'v372', 'v373', 'v374', 'v375', 'v376', 'v378', 'v379', 'v380', 'v381', 'v382', 'v383', 'v384', 'v386', 'v387', 'v389', 'v390', 'v391', 'v392', 'v393', 'v394', 'v395', 'v396', 'v397', 'v398', 'v399', 'v400', 'v401', 'v402', 'v403', 'v404', 'v405', 'v406', 'v407', 'v408', 'v410', 'v411', 'v414', 'v415', 'v418', 'v419', 'v420', 'v421', 'v422', 'v424', 'v425', 'v426', 'v427', 'v428', 'v429', 'v431', 'v432', 'v433', 'v437', 'v438', 'v441', 'v442', 'v443', 'v444', 'v445', 'v446', 'v447', 'v448', 'v449', 'v450', 'v451', 'v452', 'v453', 'v454', 'v455', 'v456', 'v457', 'v458', 'v459', 'v462', 'v463', 'v464', 'v466', 'v467', 'v468', 'v469', 'v470', 'v471', 'v472', 'v473', 'v474', 'v475', 'v476', 'v477', 'v478', 'v479', 'v482', 'v486', 'v487', 'v488', 'v489', 'v490', 'v491', 'v492', 'v494', 'v495', 'v496', 'v497', 'v498', 'v499', 'v500', 'v501', 'v502', 'v503', 'v504', 'v505', 'v506', 'v507', 'v508', 'v509', 'v511', 'v512', 'v513', 'v514', 'v515', 'v516', 'v517', 'v518', 'v519', 'v520', 'v521', 'v522', 'v523', 'v524', 'v526', 'v527', 'v528', 'v529', 'v530', 'v531', 'v532', 'v533', 'v535', 'v536', 'v537', 'v540', 'v541', 'v542', 'v543', 'v544', 'v545', 'v548', 'v549', 'v550', 'v551', 'v552', 'v553', 'v554', 'v555', 'v556', 'v557', 'v558', 'v559', 'v560', 'v561', 'v564', 'v565', 'v566', 'v567', 'v568', 'v569', 'v570', 'v571', 'v572', 'v573', 'v574', 'v575', 'v576', 'v577', 'v578', 'v579', 'v581', 'v582', 'v583', 'v584', 'v585', 'v586', 'v588', 'v589', 'v590', 'v591', 'v593', 'v594', 'v595', 'v596', 'v597', 'v598', 'v599', 'v600', 'v601', 'v602', 'v603', 'v604', 'v605', 'v606', 'v607', 'v608', 'v609', 'v610', 'v611', 'v613', 'v614', 'v615', 'v617', 'v618', 'v619', 'v620', 'v622', 'v623', 'v624', 'v625', 'v626', 'v627', 'v629', 'v630', 'v631', 'v634', 'v635', 'v636', 'v637', 'v638', 'v639', 'v642', 'v643', 'v644', 'v645', 'v646', 'v647', 'v648', 'v649', 'v650', 'v651', 'v652', 'v653', 'v654', 'v655', 'v656', 'v657', 'v659', 'v660', 'v661', 'v662', 'v665', 'v666', 'v669', 'v670', 'v671', 'v672', 'v673', 'v674', 'v675', 'v676', 'v677', 'v678', 'v679', 'v682', 'v683', 'v684', 'v685', 'v686', 'v687', 'v689', 'v690', 'v691', 'v692', 'v693', 'v694', 'v696', 'v697', 'v701', 'v702', 'v705', 'v706', 'v707', 'v708', 'v709', 'v710', 'v711', 'v712', 'v713', 'v714', 'v715', 'v716', 'v717', 'v718', 'v719', 'v720', 'v721', 'v722', 'v723', 'v724', 'v725', 'v728', 'v729', 'v730', 'v731', 'v732', 'v733', 'v734', 'v735', 'v736', 'v737', 'v738', 'v739', 'v740', 'v741', 'v743', 'v744', 'v745', 'v746', 'v747', 'v748', 'v749', 'v751', 'v752', 'v753', 'v754', 'v755', 'v756', 'v758', 'v759', 'v760', 'v761', 'v762', 'v763', 'v764', 'v765', 'v766', 'v767', 'v768', 'v771', 'v772', 'v773', 'v774', 'v775', 'v776', 'v777', 'v778', 'v779', 'v780', 'v781', 'v782', 'v783', 'v787', 'v788', 'v789', 'v790', 'v792', 'v793', 'v794', 'v795', 'v796', 'v797', 'v798', 'v800', 'v801', 'v802', 'v803', 'v804', 'v807', 'v808', 'v813', 'v814', 'v816', 'v817', 'v818', 'v823', 'v824', 'v825', 'v828', 'v829', 'v830', 'v831', 'v832', 'v833', 'v834', 'v835', 'v836', 'v837', 'v838', 'v839', 'v841', 'v842', 'v843', 'v844', 'v845', 'v846', 'v847', 'v848', 'v849', 'v850', 'v851', 'v852', 'v853', 'v854', 'v855', 'v856', 'v857', 'v858', 'v859', 'v860', 'v861', 'v862', 'v863', 'v864', 'v865', 'v866', 'v867', 'v869', 'v870', 'v871', 'v872', 'v873', 'v874', 'v875', 'v876', 'v877', 'v878', 'v880', 'v881', 'v882', 'v883', 'v884', 'v885', 'v886', 'v887', 'v888', 'v889', 'v890', 'v891', 'v892', 'v893', 'v894', 'v895', 'v897', 'v898', 'v899', 'v900', 'v901', 'v904', 'v905', 'v906', 'v908', 'v909', 'v911', 'v912', 'v913', 'v914', 'v915', 'v916', 'v917', 'v918', 'v919', 'v920', 'v921', 'v922', 'v923', 'v924', 'v925', 'v928', 'v929', 'v932', 'v933', 'v934', 'v935', 'v936', 'v938', 'v939', 'v940', 'v941', 'v942', 'v945', 'v946', 'v947', 'v948', 'v949', 'v950', 'v951', 'v952', 'v953', 'v955', 'v956', 'v957', 'v958', 'v959', 'v960', 'v961', 'v962', 'v963', 'v964', 'v967', 'v968', 'v969', 'v970', 'v972', 'v973', 'v974', 'v975', 'v976', 'v977', 'v978', 'v979', 'v980', 'v981', 'v982', 'v983', 'v984', 'v985', 'v986', 'v987', 'v989', 'v990', 'v991', 'v992', 'v993', 'v994', 'v998', 'v999', 'v1000', 'v1003', 'v1004', 'v1005', 'v1006', 'v1007', 'v1008', 'v1011', 'v1012', 'v1013', 'v1014', 'v1015', 'v1016', 'v1017', 'v1018', 'v1019', 'v1020', 'v1023', 'v1024', 'v1027', 'v1028', 'v1029', 'v1030', 'v1031', 'v1032', 'v1033', 'v1036', 'v1037', 'v1038', 'v1039', 'v1040', 'v1041', 'v1042', 'v1044', 'v1045', 'v1047', 'v1051', 'v1052', 'v1055', 'v1058', 'v1059', 'v1061', 'v1062', 'v1063', 'v1064', 'v1065', 'v1067', 'v1068', 'v1071', 'v1074', 'v1076', 'v1077', 'v1078', 'v1079', 'v1080', 'v1081', 'v1082', 'v1083', 'v1084', 'v1085', 'v1086', 'v1087', 'v1088', 'v1089', 'v1090', 'v1091', 'v1093', 'v1094', 'v1096', 'v1097', 'v1098', 'v1099', 'v1100', 'v1101', 'v1102', 'v1103', 'v1104', 'v1105', 'v1106', 'v1107', 'v1108', 'v1109', 'v1110', 'v1111', 'v1112', 'v1113', 'v1114', 'v1115', 'v1117', 'v1118', 'v1119', 'v1122', 'v1125', 'v1126', 'v1127', 'v1128', 'v1129', 'v1130', 'v1131', 'v1132', 'v1133', 'v1134', 'v1135', 'v1136', 'v1137', 'v1138', 'v1139', 'v1140', 'v1141', 'v1144', 'v1145', 'v1146', 'v1147', 'v1148', 'v1149', 'v1150', 'v1151', 'v1152', 'v1153', 'v1154', 'v1155', 'v1156', 'v1157', 'v1158', 'v1161', 'v1162', 'v1163', 'v1165', 'v1166', 'v1169', 'v1170', 'v1171', 'v1174', 'v1175', 'v1178', 'v1179', 'v1182', 'v1183', 'v1184', 'v1185', 'v1186', 'v1187', 'v1188', 'v1189', 'v1190', 'v1191', 'v1192', 'v1193', 'v1194', 'v1195', 'v1196', 'v1197', 'v1198', 'v1199', 'v1200', 'v1201', 'v1202', 'v1203', 'v1204', 'v1205', 'v1206', 'v1207', 'v1208', 'v1209', 'v1210', 'v1211', 'v1212', 'v1213', 'v1214', 'v1215', 'v1217', 'v1218', 'v1219', 'v1220', 'v1221', 'v1222', 'v1223', 'v1224', 'v1225', 'v1226', 'v1227', 'v1228', 'v1229', 'v1230', 'v1231', 'v1232', 'v1233', 'v1234', 'v1235', 'v1236', 'v1237', 'v1238', 'v1242', 'v1243', 'v1244', 'v1246', 'v1247', 'v1252', 'v1253', 'v1254', 'v1255', 'v1256', 'v1257', 'v1259', 'v1260', 'v1261', 'v1262', 'v1263', 'v1264', 'v1265', 'v1266', 'v1267', 'v1268', 'v1269', 'v1270', 'v1271', 'v1272', 'v1273', 'v1274', 'v1275', 'v1276', 'v1277', 'v1278', 'v1280', 'v1281', 'v1282', 'v1283', 'v1284', 'v1285', 'v1288', 'v1289', 'v1291', 'v1292', 'v1294', 'v1295', 'v1296', 'v1297', 'v1298', 'v1299', 'v1300', 'v1301', 'v1302', 'v1303', 'v1304', 'v1305', 'v1306', 'v1307', 'v1308', 'v1309', 'v1310', 'v1311', 'v1312', 'v1313', 'v1316', 'v1317', 'v1318', 'v1319', 'v1320', 'v1321', 'v1324', 'v1325', 'v1326', 'v1328', 'v1329', 'v1330', 'v1331', 'v1332', 'v1333', 'v1334', 'v1335', 'v1336', 'v1337', 'v1338', 'v1339', 'v1340', 'v1341', 'v1342', 'v1343', 'v1344', 'v1345', 'v1346', 'v1347', 'v1348', 'v1349', 'v1350', 'v1351', 'v1354', 'v1355', 'v1356', 'v1357', 'v1358', 'v1359', 'v1360', 'v1361', 'v1362', 'v1363', 'v1364', 'v1365', 'v1366', 'v1368', 'v1369', 'v1370', 'v1371', 'v1372', 'v1373', 'v1374', 'v1375', 'v1376', 'v1377', 'v1378', 'v1379', 'v1381', 'v1382', 'v1385', 'v1386', 'v1387', 'v1388', 'v1389', 'v1390', 'v1391', 'v1392', 'v1393', 'v1394', 'v1395', 'v1396', 'v1398', 'v1399', 'v1400', 'v1401', 'v1402', 'v1403', 'v1404', 'v1405', 'v1406', 'v1407', 'v1408', 'v1409', 'v1411', 'v1414', 'v1415', 'v1416', 'v1417', 'v1418', 'v1419', 'v1420', 'v1421', 'v1422', 'v1423', 'v1424', 'v1425', 'v1426', 'v1427', 'v1428', 'v1429', 'v1430', 'v1431', 'v1432', 'v1433', 'v1434', 'v1435', 'v1436', 'v1437', 'v1438', 'v1439', 'v1440', 'v1441', 'v1442', 'v1443', 'v1444', 'v1445', 'v1446', 'v1447', 'v1448', 'v1449', 'v1450', 'v1451', 'v1452', 'v1453', 'v1454', 'v1455', 'v1456', 'v1457', 'v1458', 'v1459', 'v1460', 'v1461', 'v1462', 'v1463', 'v1464', 'v1465', 'v1466', 'v1467', 'v1468', 'v1469', 'v1470', 'v1471', 'v1472', 'v1473', 'v1476', 'v1477', 'v1478', 'v1479', 'v1480', 'v1481', 'v1482', 'v1483', 'v1484', 'v1486', 'v1487', 'v1488', 'v1490', 'v1491', 'v1492', 'v1493', 'v1494', 'v1495', 'v1496', 'v1497', 'v1498', 'v1499', 'v1500', 'v1501', 'v1502', 'v1505', 'v1506', 'v1507', 'v1508', 'v1509', 'v1510', 'v1511', 'v1512', 'v1513', 'v1514', 'v1515', 'v1516', 'v1517', 'v1519', 'v1520', 'v1521', 'v1522', 'v1523', 'v1524', 'v1525', 'v1528', 'v1529', 'v1530', 'v1531', 'v1532', 'v1533', 'v1534', 'v1535', 'v1536', 'v1538', 'v1539', 'v1540', 'v1541', 'v1542', 'v1543', 'v1544', 'v1545', 'v1546', 'v1548', 'v1549', 'v1550', 'v1551', 'v1552', 'v1554', 'v1555', 'v1557', 'v1558', 'v1560', 'v1561', 'v1562', 'v1563', 'v1564', 'v1565', 'v1566', 'v1567', 'v1568', 'v1569', 'v1571', 'v1574', 'v1575', 'v1576', 'v1577', 'v1578', 'v1579', 'v1580', 'v1581', 'v1583', 'v1584', 'v1585', 'v1586', 'v1589', 'v1590', 'v1591', 'v1592', 'v1593', 'v1594', 'v1595', 'v1596', 'v1597', 'v1598', 'v1599', 'v1600', 'v1602', 'v1603', 'v1604', 'v1605', 'v1606', 'v1607', 'v1608', 'v1609', 'v1610', 'v1611', 'v1612', 'v1613', 'v1614', 'v1615', 'v1618', 'v1620', 'v1624', 'v1625', 'v1626', 'v1627', 'v1630', 'v1631', 'v1632', 'v1633', 'v1634', 'v1636', 'v1637', 'v1638', 'v1640', 'v1641', 'v1643', 'v1644', 'v1645', 'v1646', 'v1648', 'v1649', 'v1650', 'v1651', 'v1654', 'v1656', 'v1657', 'v1658', 'v1662', 'v1663', 'v1665', 'v1666', 'v1669', 'v1670', 'v1671', 'v1672', 'v1673', 'v1674', 'v1675', 'v1677', 'v1678', 'v1679', 'v1680', 'v1681', 'v1682', 'v1683', 'v1684', 'v1685', 'v1686', 'v1687', 'v1688', 'v1689', 'v1691', 'v1692', 'v1693', 'v1694', 'v1695', 'v1698', 'v1699', 'v1700', 'v1701', 'v1702', 'v1703', 'v1704', 'v1705', 'v1706', 'v1708', 'v1709', 'v1710', 'v1711', 'v1712', 'v1713', 'v1714', 'v1715', 'v1716', 'v1717', 'v1718', 'v1720', 'v1721', 'v1722', 'v1723', 'v1724', 'v1725', 'v1726', 'v1727', 'v1728', 'v1729', 'v1730', 'v1731', 'v1732', 'v1733', 'v1736', 'v1737', 'v1738', 'v1739', 'v1740', 'v1741', 'v1742', 'v1743', 'v1744', 'v1745', 'v1746', 'v1747', 'v1748', 'v1749', 'v1750', 'v1751', 'v1752', 'v1753', 'v1755', 'v1756', 'v1757', 'v1758', 'v1760', 'v1761', 'v1762', 'v1763', 'v1764', 'v1768', 'v1777', 'v1778', 'v1779', 'v1780', 'v1781', 'v1783', 'v1784', 'v1785', 'v1787', 'v1788', 'v1791', 'v1792', 'v1793', 'v1798', 'v1799', 'v1800', 'v1801', 'v1802', 'v1803', 'v1804', 'v1805', 'v1806', 'v1807', 'v1808', 'v1809', 'v1810', 'v1813', 'v1814', 'v1815', 'v1816', 'v1817', 'v1818', 'v1820', 'v1824', 'v1826', 'v1828', 'v1829', 'v1830', 'v1833', 'v1834', 'v1835', 'v1836', 'v1837', 'v1838', 'v1840', 'v1841', 'v1842', 'v1843', 'v1844', 'v1845', 'v1846', 'v1847', 'v1848', 'v1849', 'v1850', 'v1853', 'v1856', 'v1857', 'v1858', 'v1859', 'v1860', 'v1861', 'v1862', 'v1863', 'v1865', 'v1866', 'v1868', 'v1869', 'v1870', 'v1871', 'v1872', 'v1873', 'v1877', 'v1880', 'v1881', 'v1882', 'v1883', 'v1884', 'v1885', 'v1886', 'v1887', 'v1888', 'v1889', 'v1890', 'v1891', 'v1895', 'v1898', 'v1899', 'v1900', 'v1901', 'v1902', 'v1903', 'v1906', 'v1907', 'v1908', 'v1910', 'v1911', 'v1912', 'v1913', 'v1914', 'v1916', 'v1917', 'v1918', 'v1919', 'v1921', 'v1922', 'v1923', 'v1924', 'v1925', 'v1926', 'v1927', 'v1928', 'v1929', 'v1931', 'v1932', 'v1933', 'v1934', 'v1935', 'v1936', 'v1937', 'v1938', 'v1939', 'v1940', 'v1941', 'v1942', 'v1943', 'v1944', 'v1945', 'v1946', 'v1947', 'v1948', 'v1949', 'v1950', 'v1951', 'v1952', 'v1953', 'v1954', 'v1955', 'v1956', 'v1957', 'v1958', 'v1959', 'v1960', 'v1961', 'v1962', 'v1963', 'v1964', 'v1965', 'v1966', 'v1967', 'v1968', 'v1969', 'v1972', 'v1973', 'v1974', 'v1975', 'v1976', 'v1977', 'v1978', 'v1979', 'v1980', 'v1981', 'v1982', 'v1983', 'v1984', 'v1985', 'v1986', 'v1987', 'v1988', 'v1989', 'v1990', 'v1991', 'v1992', 'v1993', 'v1994', 'v1996', 'v1997', 'v1998', 'v1999', 'v2001', 'v2002', 'v2003', 'v2004', 'v2005', 'v2006', 'v2007', 'v2009', 'v2010', 'v2011', 'v2012', 'v2013', 'v2014', 'v2015', 'v2016', 'v2017', 'v2018', 'v2020', 'v2021', 'v2022', 'v2023', 'v2024', 'v2025', 'v2026', 'v2027', 'v2028', 'v2029', 'v2030', 'v2031', 'v2032', 'v2033', 'v2034', 'v2035', 'v2036', 'v2041', 'v2042', 'v2043', 'v2044', 'v2045', 'v2046', 'v2047', 'v2048', 'v2049', 'v2050', 'v2053', 'v2054', 'v2055', 'v2056', 'v2057', 'v2058', 'v2059', 'v2060', 'v2061', 'v2062', 'v2063', 'v2065', 'v2066', 'v2067', 'v2068', 'v2069', 'v2070', 'v2071', 'v2074', 'v2075', 'v2079', 'v2080', 'v2081', 'v2083', 'v2084', 'v2085', 'v2086', 'v2087', 'v2088', 'v2092', 'v2093', 'v2095', 'v2098', 'v2099', 'v2100', 'v2101', 'v2102', 'v2104', 'v2105', 'v2107', 'v2110', 'v2111', 'v2112', 'v2114', 'v2115', 'v2128', 'v2129', 'v2130', 'v2131', 'v2133', 'v2134', 'v2135', 'v2137', 'v2138', 'v2139', 'v2140', 'v2141', 'v2142', 'v2143', 'v2144', 'v2145', 'v2146', 'v2147', 'v2148', 'v2149', 'v2150', 'v2151', 'v2152', 'v2153', 'v2154', 'v2155', 'v2156', 'v2157', 'v2158', 'v2159', 'v2161', 'v2162', 'v2163', 'v2164', 'v2165', 'v2166', 'v2167', 'v2168', 'v2169', 'v2170', 'v2171', 'v2172', 'v2174', 'v2175', 'v2177', 'v2179', 'v2180', 'v2181', 'v2182', 'v2183', 'v2185', 'v2186', 'v2187', 'v2188', 'v2189', 'v2190', 'v2191', 'v2192', 'v2193', 'v2194', 'v2195', 'v2197', 'v2198', 'v2199', 'v2200', 'v2201', 'v2204', 'v2205', 'v2206', 'v2207', 'v2208', 'v2209', 'v2210', 'v2211', 'v2212', 'v2213', 'v2214', 'v2215', 'v2216', 'v2217', 'v2218', 'v2219', 'v2220', 'v2221', 'v2224', 'v2226', 'v2228', 'v2229', 'v2230', 'v2231', 'v2232', 'v2235', 'v2236', 'v2237', 'v2238', 'v2239', 'v2240', 'v2242', 'v2243', 'v2244', 'v2245', 'v2246', 'v2247', 'v2248', 'v2249', 'v2250', 'v2251', 'v2252', 'v2253', 'v2254', 'v2255', 'v2257', 'v2258', 'v2262', 'v2263', 'v2264', 'v2265', 'v2267', 'v2269', 'v2270', 'v2272', 'v2273', 'v2274', 'v2276', 'v2277', 'v2278', 'v2279', 'v2280', 'v2283', 'v2284', 'v2285', 'v2286', 'v2287', 'v2288', 'v2289', 'v2290', 'v2291', 'v2292', 'v2293', 'v2294', 'v2295', 'v2296', 'v2297', 'v2298', 'v2299', 'v2300', 'v2301', 'v2302', 'v2303', 'v2304', 'v2305', 'v2306', 'v2307', 'v2309', 'v2310', 'v2311', 'v2312', 'v2313', 'v2314', 'v2316', 'v2317', 'v2318', 'v2319', 'v2320', 'v2321', 'v2322', 'v2323', 'v2324', 'v2325', 'v2326', 'v2327', 'v2328', 'v2329', 'v2330', 'v2331', 'v2332', 'v2333', 'v2334', 'v2335', 'v2336', 'v2338', 'v2339', 'v2340', 'v2342', 'v2343', 'v2345', 'v2346', 'v2347', 'v2349', 'v2350', 'v2351', 'v2352', 'v2353', 'v2354', 'v2355', 'v2356', 'v2357', 'v2358', 'v2359', 'v2360', 'v2361', 'v2362', 'v2363', 'v2364', 'v2365', 'v2366', 'v2367', 'v2368', 'v2369', 'v2370', 'v2373', 'v2374', 'v2375', 'v2376', 'v2377', 'v2378', 'v2381', 'v2382', 'v2383', 'v2384', 'v2385', 'v2386', 'v2387', 'v2388', 'v2389', 'v2390', 'v2391', 'v2392', 'v2393', 'v2394', 'v2395', 'v2396', 'v2397', 'v2398', 'v2400', 'v2401', 'v2402', 'v2404', 'v2407', 'v2408', 'v2409', 'v2412', 'v2413', 'v2414', 'v2415', 'v2416', 'v2417', 'v2418', 'v2419', 'v2421', 'v2422', 'v2423', 'v2424', 'v2425', 'v2426', 'v2428', 'v2429', 'v2432', 'v2433', 'v2434', 'v2435', 'v2436', 'v2438', 'v2439', 'v2440', 'v2441', 'v2442', 'v2443', 'v2444', 'v2445', 'v2446', 'v2447', 'v2448', 'v2449', 'v2450', 'v2451', 'v2452', 'v2453', 'v2454', 'v2456', 'v2457', 'v2458', 'v2459', 'v2460', 'v2461', 'v2462', 'v2463', 'v2465', 'v2466', 'v2467', 'v2468', 'v2469', 'v2470', 'v2471', 'v2473', 'v2474', 'v2475', 'v2476', 'v2477', 'v2478', 'v2479', 'v2481', 'v2482', 'v2483', 'v2484', 'v2485', 'v2486', 'v2487', 'v2488', 'v2489', 'v2490', 'v2491', 'v2492', 'v2493', 'v2494', 'v2495', 'v2496', 'v2497', 'v2498', 'v2499', 'v2500', 'v2501', 'v2502', 'v2503', 'v2505', 'v2507', 'v2508', 'v2509', 'v2511', 'v2512', 'v2513', 'v2515', 'v2517', 'v2518', 'v2519', 'v2520', 'v2521', 'v2522', 'v2523', 'v2524', 'v2525', 'v2526', 'v2527', 'v2528', 'v2529', 'v2530', 'v2531', 'v2532', 'v2533', 'v2534', 'v2535', 'v2537', 'v2538', 'v2539', 'v2540', 'v2541', 'v2544', 'v2545', 'v2546', 'v2547', 'v2548', 'v2551', 'v2552', 'v2553', 'v2554', 'v2555', 'v2556', 'v2557', 'v2558', 'v2559', 'v2560', 'v2561', 'v2562', 'v2563', 'v2564', 'v2565', 'v2566', 'v2567', 'v2568', 'v2569', 'v2570', 'v2571', 'v2572', 'v2573', 'v2574', 'v2575', 'v2576', 'v2577', 'v2578', 'v2579', 'v2580', 'v2581', 'v2582', 'v2583', 'v2584', 'v2585', 'v2586', 'v2587', 'v2588', 'v2589', 'v2590', 'v2591', 'v2593', 'v2594', 'v2595', 'v2596', 'v2597', 'v2598', 'v2599', 'v2600', 'v2601', 'v2602', 'v2603', 'v2604', 'v2605', 'v2606', 'v2607', 'v2609', 'v2610', 'v2611', 'v2612', 'v2613', 'v2614', 'v2615', 'v2616', 'v2617', 'v2619', 'v2620', 'v2621', 'v2622', 'v2623', 'v2624', 'v2625', 'v2626', 'v2627', 'v2628', 'v2629', 'v2630', 'v2631', 'v2632', 'v2633', 'v2634', 'v2635', 'v2636', 'v2637', 'v2638', 'v2639', 'v2640', 'v2641', 'v2642', 'v2643', 'v2645', 'v2646', 'v2647', 'v2648', 'v2649', 'v2650', 'v2651', 'v2652', 'v2653', 'v2654', 'v2655', 'v2656', 'v2657', 'v2658', 'v2659', 'v2660', 'v2661', 'v2662', 'v2663', 'v2664', 'v2665', 'v2666', 'v2667', 'v2669', 'v2670', 'v2672', 'v2673', 'v2674', 'v2675', 'v2676', 'v2678', 'v2680', 'v2681', 'v2683', 'v2684', 'v2687', 'v2688', 'v2689', 'v2690', 'v2691', 'v2693', 'v2694', 'v2695', 'v2696', 'v2697', 'v2698', 'v2699', 'v2700', 'v2701', 'v2704', 'v2705', 'v2706', 'v2707', 'v2708', 'v2709', 'v2712', 'v2714', 'v2715', 'v2716', 'v2717', 'v2718', 'v2719', 'v2720', 'v2722', 'v2723', 'v2724', 'v2725', 'v2726', 'v2727', 'v2728', 'v2730', 'v2731', 'v2732', 'v2733', 'v2734', 'v2735', 'v2736', 'v2737', 'v2738', 'v2741', 'v2742', 'v2745', 'v2746', 'v2747', 'v2748', 'v2749', 'v2751', 'v2752', 'v2753', 'v2754', 'v2755', 'v2756', 'v2757', 'v2758', 'v2759', 'v2760', 'v2761', 'v2762', 'v2763', 'v2764', 'v2767', 'v2768', 'v2769', 'v2770', 'v2771', 'v2772', 'v2775', 'v2776', 'v2779', 'v2780', 'v2781', 'v2782', 'v2783', 'v2784', 'v2785', 'v2786', 'v2787', 'v2788', 'v2789', 'v2790', 'v2791', 'v2794', 'v2795', 'v2798', 'v2799', 'v2800', 'v2802', 'v2803', 'v2804', 'v2805', 'v2806', 'v2807', 'v2808', 'v2809', 'v2810', 'v2811', 'v2812', 'v2814', 'v2815', 'v2817', 'v2818', 'v2819', 'v2820', 'v2821', 'v2822', 'v2824', 'v2825', 'v2826', 'v2827', 'v2828', 'v2830', 'v2832', 'v2833', 'v2834', 'v2835', 'v2837', 'v2838', 'v2839', 'v2840', 'v2841', 'v2842', 'v2843', 'v2844', 'v2845', 'v2848', 'v2849', 'v2852', 'v2853', 'v2854', 'v2855', 'v2857', 'v2858', 'v2859', 'v2860', 'v2861', 'v2862', 'v2863', 'v2865', 'v2866', 'v2867', 'v2868', 'v2869', 'v2871', 'v2874', 'v2875', 'v2878', 'v2879', 'v2882', 'v2883', 'v2886', 'v2887', 'v2888', 'v2889', 'v2890', 'v2891', 'v2892', 'v2894', 'v2895', 'v2896', 'v2897', 'v2898', 'v2899', 'v2900', 'v2901', 'v2902', 'v2903', 'v2905', 'v2906', 'v2907', 'v2908', 'v2909', 'v2910', 'v2911', 'v2913', 'v2914', 'v2915', 'v2916', 'v2918', 'v2919', 'v2920', 'v2921', 'v2922', 'v2923', 'v2924', 'v2925', 'v2926', 'v2927', 'v2928', 'v2929', 'v2930', 'v2931', 'v2932', 'v2933', 'v2934', 'v2935', 'v2936', 'v2937', 'v2938', 'v2939', 'v2940', 'v2942', 'v2943', 'v2944', 'v2945', 'v2946', 'v2948', 'v2949', 'v2950', 'v2952', 'v2953', 'v2954', 'v2955', 'v2956', 'v2957', 'v2958', 'v2959', 'v2960', 'v2961', 'v2962', 'v2963', 'v2964', 'v2965', 'v2966', 'v2967', 'v2968', 'v2969', 'v2970', 'v2972', 'v2973', 'v2974', 'v2975', 'v2976', 'v2977', 'v2978', 'v2979', 'v2980', 'v2981', 'v2983', 'v2984', 'v2985', 'v2986', 'v2987', 'v2988', 'v2989', 'v2990', 'v2992', 'v2993', 'v2994', 'v2995', 'v2996', 'v2997', 'v2998', 'v2999', 'v3000', 'v3002', 'v3003', 'v3004', 'v3005', 'v3006', 'v3007', 'v3008', 'v3009', 'v3010', 'v3011', 'v3012', 'v3013', 'v3014', 'v3015', 'v3016', 'v3017', 'v3018', 'v3019', 'v3020', 'v3021', 'v3022', 'v3023', 'v3024', 'v3025', 'v3027', 'v3028', 'v3029', 'v3031', 'v3032', 'v3033', 'v3036', 'v3039', 'v3041', 'v3042', 'v3043', 'v3044', 'v3045', 'v3046', 'v3047', 'v3048', 'v3049', 'v3050', 'v3052', 'v3053', 'v3054', 'v3055', 'v3056', 'v3057', 'v3058', 'v3062', 'v3065', 'v3068', 'v3069', 'v3070', 'v3071', 'v3073', 'v3074', 'v3075', 'v3076', 'v3077', 'v3078', 'v3079', 'v3080', 'v3081', 'v3082', 'v3083', 'v3084', 'v3085', 'v3086', 'v3087', 'v3088', 'v3091', 'v3092', 'v3093', 'v3094', 'v3095', 'v3096', 'v3097', 'v3098', 'v3099', 'v3100', 'v3101', 'v3104', 'v3105', 'v3106', 'v3107', 'v3108', 'v3109', 'v3110', 'v3111', 'v3112', 'v3113', 'v3114', 'v3115', 'v3116', 'v3117', 'v3118', 'v3119', 'v3120', 'v3121', 'v3122', 'v3123', 'v3124', 'v3126', 'v3127', 'v3129', 'v3130', 'v3131', 'v3132', 'v3133', 'v3134', 'v3135', 'v3136', 'v3137', 'v3138', 'v3139', 'v3140', 'v3141', 'v3144', 'v3145', 'v3146', 'v3147', 'v3148', 'v3149', 'v3150', 'v3153', 'v3154', 'v3155', 'v3156', 'v3157', 'v3158', 'v3159', 'v3160', 'v3161', 'v3162', 'v3163', 'v3164', 'v3165', 'v3168', 'v3169', 'v3170', 'v3172', 'v3173', 'v3176', 'v3177', 'v3178', 'v3179', 'v3180', 'v3181', 'v3182', 'v3183', 'v3184', 'v3185', 'v3187', 'v3188', 'v3189', 'v3191', 'v3192', 'v3193', 'v3194', 'v3195', 'v3196', 'v3197', 'v3198', 'v3199', 'v3200', 'v3202', 'v3203', 'v3204', 'v3205', 'v3206', 'v3207', 'v3208', 'v3209', 'v3210', 'v3211', 'v3212', 'v3213', 'v3214', 'v3215', 'v3216', 'v3217', 'v3218', 'v3220', 'v3221', 'v3222', 'v3223', 'v3224', 'v3225', 'v3226', 'v3227', 'v3228', 'v3229', 'v3230', 'v3231', 'v3232', 'v3233', 'v3234', 'v3235', 'v3236', 'v3237', 'v3238', 'v3239', 'v3240', 'v3241', 'v3242', 'v3243', 'v3245', 'v3246', 'v3247', 'v3248', 'v3249', 'v3250', 'v3251', 'v3252', 'v3253', 'v3256', 'v3257', 'v3258', 'v3259', 'v3260', 'v3261', 'v3262', 'v3264', 'v3265', 'v3266', 'v3267', 'v3268', 'v3269', 'v3270', 'v3271', 'v3272', 'v3273', 'v3274', 'v3275', 'v3276', 'v3277', 'v3278', 'v3279', 'v3280', 'v3281', 'v3282', 'v3283', 'v3285', 'v3286', 'v3287', 'v3288', 'v3289', 'v3290', 'v3291', 'v3292', 'v3293', 'v3294', 'v3295', 'v3296', 'v3297', 'v3298', 'v3299', 'v3300', 'v3302', 'v3303', 'v3304', 'v3305', 'v3306', 'v3307', 'v3308', 'v3309', 'v3310', 'v3311', 'v3312', 'v3313', 'v3314', 'v3315', 'v3316', 'v3317', 'v3318', 'v3319', 'v3320', 'v3321', 'v3322', 'v3323', 'v3326', 'v3327', 'v3328', 'v3329', 'v3330', 'v3331', 'v3332', 'v3334', 'v3335', 'v3336', 'v3337', 'v3338', 'v3339', 'v3340', 'v3343', 'v3344', 'v3346', 'v3347', 'v3348', 'v3349', 'v3350', 'v3351', 'v3352', 'v3353', 'v3358', 'v3359', 'v3360', 'v3362', 'v3363', 'v3364', 'v3365', 'v3367', 'v3370', 'v3371', 'v3372', 'v3373', 'v3374', 'v3377', 'v3378', 'v3379', 'v3380', 'v3381', 'v3384', 'v3385', 'v3386', 'v3387', 'v3388', 'v3391', 'v3392', 'v3393', 'v3394', 'v3395', 'v3396', 'v3397', 'v3398', 'v3399', 'v3400', 'v3401', 'v3402', 'v3403', 'v3404', 'v3405', 'v3406', 'v3407', 'v3408', 'v3409', 'v3410', 'v3411', 'v3412', 'v3413', 'v3414', 'v3415', 'v3416', 'v3417', 'v3418', 'v3419', 'v3420', 'v3421', 'v3423', 'v3424', 'v3425', 'v3428', 'v3429', 'v3430', 'v3431', 'v3432', 'v3433', 'v3434', 'v3435', 'v3436', 'v3438', 'v3439', 'v3440', 'v3442', 'v3443', 'v3444', 'v3445', 'v3446', 'v3448', 'v3449', 'v3450', 'v3451', 'v3452', 'v3454', 'v3455', 'v3456', 'v3457', 'v3458', 'v3460', 'v3461', 'v3462', 'v3463', 'v3464', 'v3466', 'v3467', 'v3468', 'v3469', 'v3470', 'v3471', 'v3472', 'v3473', 'v3474', 'v3475', 'v3476', 'v3477', 'v3478', 'v3479', 'v3480', 'v3481', 'v3482', 'v3483', 'v3485', 'v3486', 'v3487', 'v3488', 'v3490', 'v3492', 'v3494', 'v3496', 'v3497', 'v3498', 'v3499', 'v3500', 'v3501', 'v3502', 'v3505', 'v3506', 'v3507', 'v3509', 'v3510', 'v3512', 'v3513', 'v3514', 'v3515', 'v3516', 'v3517', 'v3518', 'v3519', 'v3521', 'v3523', 'v3525', 'v3527', 'v3530', 'v3531', 'v3532', 'v3533', 'v3535', 'v3536', 'v3537', 'v3538', 'v3539', 'v3540', 'v3541', 'v3542', 'v3543', 'v3544', 'v3545', 'v3546', 'v3547', 'v3548', 'v3549', 'v3550', 'v3551', 'v3552', 'v3553', 'v3554', 'v3555', 'v3556', 'v3557', 'v3559', 'v3560', 'v3561', 'v3562', 'v3563', 'v3564', 'v3565', 'v3566', 'v3567', 'v3568', 'v3571', 'v3573', 'v3575', 'v3577', 'v3578', 'v3579', 'v3580', 'v3581', 'v3582', 'v3583', 'v3584', 'v3585', 'v3587', 'v3588', 'v3589', 'v3590', 'v3591', 'v3594', 'v3595', 'v3596', 'v3597', 'v3598', 'v3599', 'v3600', 'v3601', 'v3602', 'v3603', 'v3604', 'v3606', 'v3607', 'v3609', 'v3610', 'v3611', 'v3612', 'v3615', 'v3617', 'v3618', 'v3619', 'v3620', 'v3621', 'v3622', 'v3623', 'v3624', 'v3625', 'v3626', 'v3629', 'v3632', 'v3635', 'v3638', 'v3639', 'v3640', 'v3641', 'v3642', 'v3643', 'v3644', 'v3646', 'v3647', 'v3648', 'v3649', 'v3650', 'v3651', 'v3654', 'v3655', 'v3656', 'v3657', 'v3658', 'v3659', 'v3660', 'v3662', 'v3663', 'v3664', 'v3665', 'v3666', 'v3667', 'v3668', 'v3669', 'v3670', 'v3671', 'v3672', 'v3673', 'v3674', 'v3675', 'v3676', 'v3677', 'v3678', 'v3679', 'v3680', 'v3681', 'v3682', 'v3683', 'v3684', 'v3685', 'v3686', 'v3687', 'v3688', 'v3689', 'v3690', 'v3691', 'v3692', 'v3693', 'v3694', 'v3695', 'v3696', 'v3697', 'v3698', 'v3699', 'v3700', 'v3701', 'v3702', 'v3703', 'v3704', 'v3705', 'v3707', 'v3708', 'v3709', 'v3710', 'v3712', 'v3713', 'v3714', 'v3715', 'v3717', 'v3718', 'v3719', 'v3720', 'v3722', 'v3723', 'v3724', 'v3725', 'v3726', 'v3727', 'v3728', 'v3729', 'v3730', 'v3731', 'v3732', 'v3733', 'v3734', 'v3735', 'v3737', 'v3739', 'v3741', 'v3743', 'v3744', 'v3745', 'v3746', 'v3747', 'v3748', 'v3749', 'v3750', 'v3752', 'v3753', 'v3754', 'v3755', 'v3757', 'v3758', 'v3759', 'v3760', 'v3761', 'v3762', 'v3763', 'v3764', 'v3765', 'v3766', 'v3768', 'v3769', 'v3770', 'v3771', 'v3772', 'v3773', 'v3774', 'v3775', 'v3776', 'v3778', 'v3779', 'v3780', 'v3781', 'v3783', 'v3784', 'v3785', 'v3786', 'v3788', 'v3789', 'v3790', 'v3791', 'v3792', 'v3793', 'v3794', 'v3796', 'v3797', 'v3798', 'v3799', 'v3800', 'v3801', 'v3803', 'v3804', 'v3805', 'v3807', 'v3808', 'v3809', 'v3810', 'v3811', 'v3812', 'v3813', 'v3814', 'v3815', 'v3817', 'v3818', 'v3819', 'v3820', 'v3821', 'v3822', 'v3823', 'v3824', 'v3825', 'v3826', 'v3827', 'v3828', 'v3829', 'v3830', 'v3831', 'v3832', 'v3835', 'v3836', 'v3837', 'v3838', 'v3839', 'v3840', 'v3841', 'v3842', 'v3843', 'v3844', 'v3845', 'v3846', 'v3847', 'v3848', 'v3849', 'v3850', 'v3851', 'v3852', 'v3853', 'v3854', 'v3855', 'v3856', 'v3857', 'v3858', 'v3859', 'v3860', 'v3862', 'v3863', 'v3865', 'v3866', 'v3868', 'v3869', 'v3871', 'v3872', 'v3879', 'v3880', 'v3881', 'v3882', 'v3883', 'v3884', 'v3885', 'v3886', 'v3887', 'v3888', 'v3889', 'v3890', 'v3891', 'v3892', 'v3893', 'v3894', 'v3895', 'v3896', 'v3897', 'v3898', 'v3899', 'v3900', 'v3901', 'v3904', 'v3905', 'v3906', 'v3907', 'v3908', 'v3909', 'v3910', 'v3911', 'v3912', 'v3913', 'v3914', 'v3915', 'v3916', 'v3917', 'v3918', 'v3919', 'v3920', 'v3921', 'v3922', 'v3923', 'v3924', 'v3926', 'v3928', 'v3930', 'v3931', 'v3932', 'v3933', 'v3934', 'v3935', 'v3938', 'v3939', 'v3942', 'v3943', 'v3946', 'v3947', 'v3949', 'v3950', 'v3951', 'v3952', 'v3953', 'v3954', 'v3955', 'v3956', 'v3957', 'v3958', 'v3959', 'v3960', 'v3962', 'v3963', 'v3964', 'v3965', 'v3966', 'v3967', 'v3968', 'v3969', 'v3970', 'v3972', 'v3973', 'v3974', 'v3975', 'v3976', 'v3977', 'v3978', 'v3979', 'v3980', 'v3981', 'v3982', 'v3983', 'v3984', 'v3985', 'v3986', 'v3987', 'v3988', 'v3989', 'v3990', 'v3991', 'v3992', 'v3993', 'v3994', 'v3995', 'v3996', 'v3997', 'v3999', 'v4000', 'v4001', 'v4002', 'v4003', 'v4005', 'v4006', 'v4007', 'v4008', 'v4009', 'v4010', 'v4012', 'v4013', 'v4014', 'v4015', 'v4016', 'v4017', 'v4019', 'v4020', 'v4021', 'v4022', 'v4023', 'v4024', 'v4026', 'v4027', 'v4028', 'v4029', 'v4030', 'v4032', 'v4033', 'v4034', 'v4035', 'v4036', 'v4037', 'v4038', 'v4039', 'v4040', 'v4041', 'v4042', 'v4043', 'v4044', 'v4045', 'v4046', 'v4047', 'v4048', 'v4049', 'v4050', 'v4051', 'v4052', 'v4054', 'v4055', 'v4056', 'v4057', 'v4058', 'v4061', 'v4062', 'v4063', 'v4064', 'v4066', 'v4067', 'v4068', 'v4069', 'v4070', 'v4071', 'v4072', 'v4073', 'v4074', 'v4075', 'v4076', 'v4077', 'v4078', 'v4079', 'v4081', 'v4082', 'v4083', 'v4084', 'v4085', 'v4087', 'v4088', 'v4089', 'v4090', 'v4091', 'v4094', 'v4095', 'v4096', 'v4099', 'v4100', 'v4101', 'v4104', 'v4105', 'v4106', 'v4109', 'v4110', 'v4111', 'v4112', 'v4113', 'v4116', 'v4117', 'v4118', 'v4119', 'v4120', 'v4121', 'v4122', 'v4123', 'v4124', 'v4125', 'v4128', 'v4129', 'v4130', 'v4131', 'v4132', 'v4133', 'v4134', 'v4135', 'v4138', 'v4139', 'v4140', 'v4141', 'v4142', 'v4143', 'v4144', 'v4145', 'v4147', 'v4148', 'v4149', 'v4150', 'v4151', 'v4152', 'v4153', 'v4154', 'v4155', 'v4156', 'v4157', 'v4159', 'v4162', 'v4163', 'v4164', 'v4165', 'v4166', 'v4167', 'v4168', 'v4169', 'v4170', 'v4171', 'v4172', 'v4174', 'v4175', 'v4176', 'v4177', 'v4178', 'v4179', 'v4185', 'v4186', 'v4187', 'v4191', 'v4194', 'v4195', 'v4196', 'v4200', 'v4203', 'v4208', 'v4209', 'v4210', 'v4213', 'v4214', 'v4215', 'v4216', 'v4217', 'v4220', 'v4221', 'v4222', 'v4223', 'v4225', 'v4227', 'v4228', 'v4229', 'v4230', 'v4233', 'v4234', 'v4235', 'v4236', 'v4237', 'v4238', 'v4239', 'v4240', 'v4241', 'v4242', 'v4243', 'v4244', 'v4245', 'v4246', 'v4247', 'v4248', 'v4249', 'v4251', 'v4252', 'v4253', 'v4254', 'v4255', 'v4256', 'v4257', 'v4258', 'v4259', 'v4260', 'v4262', 'v4265', 'v4266', 'v4267', 'v4268', 'v4269', 'v4270', 'v4272', 'v4273', 'v4274', 'v4275', 'v4276', 'v4277', 'v4281', 'v4282', 'v4283', 'v4286', 'v4288', 'v4289', 'v4291', 'v4292', 'v4293', 'v4294', 'v4296', 'v4297', 'v4298', 'v4301', 'v4302', 'v4303', 'v4304', 'v4305', 'v4306', 'v4307', 'v4308', 'v4309', 'v4310', 'v4311', 'v4312', 'v4313', 'v4314', 'v4315', 'v4316', 'v4317', 'v4318', 'v4319', 'v4322', 'v4323', 'v4324', 'v4325', 'v4326', 'v4327', 'v4328', 'v4329', 'v4330', 'v4331', 'v4332', 'v4333', 'v4334', 'v4335', 'v4336', 'v4337', 'v4338', 'v4339', 'v4340', 'v4341', 'v4342', 'v4343', 'v4344', 'v4346', 'v4347', 'v4348', 'v4349', 'v4353', 'v4354', 'v4356', 'v4357', 'v4358', 'v4359', 'v4360', 'v4361', 'v4362', 'v4363', 'v4364', 'v4365', 'v4366', 'v4367', 'v4368', 'v4371', 'v4372', 'v4373', 'v4374', 'v4375', 'v4376', 'v4377', 'v4378', 'v4379', 'v4380', 'v4381', 'v4382', 'v4383', 'v4384', 'v4386', 'v4388', 'v4389', 'v4391', 'v4392', 'v4394', 'v4395', 'v4397', 'v4398', 'v4399', 'v4401', 'v4402', 'v4403', 'v4404', 'v4405', 'v4406', 'v4408', 'v4409', 'v4410', 'v4411', 'v4412', 'v4413', 'v4414', 'v4415', 'v4416', 'v4417', 'v4418', 'v4424', 'v4425', 'v4426', 'v4427', 'v4429', 'v4432', 'v4433', 'v4434', 'v4435', 'v4438', 'v4439', 'v4440', 'v4441', 'v4442', 'v4443', 'v4444', 'v4446', 'v4447', 'v4448', 'v4449', 'v4450', 'v4451', 'v4452', 'v4455', 'v4456', 'v4458', 'v4460', 'v4461', 'v4463', 'v4464', 'v4465', 'v4466', 'v4467', 'v4468', 'v4470', 'v4471', 'v4472', 'v4473', 'v4474', 'v4475', 'v4476', 'v4477', 'v4478', 'v4479', 'v4480', 'v4481', 'v4482', 'v4483', 'v4484', 'v4485', 'v4486', 'v4487', 'v4488', 'v4489', 'v4490', 'v4491', 'v4492', 'v4493', 'v4494', 'v4495', 'v4496', 'v4497', 'v4498', 'v4499', 'v4501', 'v4502', 'v4503', 'v4505', 'v4506', 'v4507', 'v4509', 'v4510', 'v4511', 'v4512', 'v4513', 'v4516', 'v4517', 'v4518', 'v4519', 'v4520', 'v4521', 'v4522', 'v4524', 'v4525', 'v4526', 'v4529', 'v4530', 'v4531', 'v4532', 'v4533', 'v4534', 'v4537', 'v4539', 'v4540', 'v4541', 'v4542', 'v4543', 'v4544', 'v4545', 'v4547', 'v4548', 'v4549', 'v4550', 'v4551', 'v4552', 'v4554', 'v4555', 'v4556', 'v4557', 'v4558', 'v4559', 'v4560', 'v4561', 'v4562', 'v4563', 'v4564', 'v4565', 'v4566', 'v4567', 'v4568', 'v4569', 'v4570', 'v4571', 'v4572', 'v4573', 'v4574', 'v4575', 'v4576', 'v4578', 'v4579', 'v4580', 'v4582', 'v4583', 'v4584', 'v4585', 'v4586', 'v4587', 'v4588', 'v4589', 'v4590', 'v4591', 'v4593', 'v4594', 'v4595', 'v4596', 'v4597', 'v4598', 'v4599', 'v4601', 'v4602', 'v4603', 'v4604', 'v4605', 'v4606', 'v4607', 'v4608', 'v4609', 'v4610', 'v4611', 'v4612', 'v4613', 'v4614', 'v4617', 'v4618', 'v4619', 'v4620', 'v4621', 'v4622', 'v4623', 'v4625', 'v4626', 'v4627', 'v4628', 'v4629', 'v4631', 'v4632', 'v4633', 'v4634', 'v4635', 'v4637', 'v4638', 'v4639', 'v4640', 'v4641', 'v4642', 'v4643', 'v4645', 'v4646', 'v4647', 'v4648', 'v4649', 'v4651', 'v4652', 'v4653', 'v4654', 'v4655', 'v4656', 'v4657', 'v4658', 'v4659', 'v4660', 'v4661', 'v4662', 'v4664', 'v4665', 'v4666', 'v4667', 'v4668', 'v4669', 'v4670', 'v4671', 'v4672', 'v4673', 'v4675', 'v4676', 'v4677', 'v4678', 'v4679', 'v4680', 'v4681', 'v4682', 'v4683', 'v4684', 'v4685', 'v4686', 'v4687', 'v4688', 'v4689', 'v4690', 'v4693', 'v4694', 'v4695', 'v4696', 'v4698', 'v4699', 'v4700', 'v4701', 'v4704', 'v4705', 'v4706', 'v4707', 'v4708', 'v4709', 'v4710', 'v4711', 'v4712', 'v4713', 'v4714', 'v4715', 'v4716', 'v4717', 'v4718', 'v4720', 'v4721', 'v4722', 'v4723', 'v4724', 'v4725', 'v4726', 'v4727', 'v4728', 'v4729', 'v4730', 'v4731', 'v4732', 'v4733', 'v4734', 'v4735', 'v4736', 'v4737', 'v4738', 'v4739', 'v4740', 'v4741', 'v4742', 'v4743', 'v4744', 'v4745', 'v4746', 'v4747', 'v4748', 'v4749', 'v4750', 'v4751', 'v4752', 'v4753', 'v4754', 'v4755', 'v4757', 'v4758', 'v4759', 'v4760', 'v4761', 'v4762', 'v4763', 'v4764', 'v4765', 'v4766', 'v4767', 'v4768', 'v4769', 'v4770', 'v4771', 'v4772', 'v4775', 'v4776', 'v4777', 'v4778', 'v4779', 'v4780', 'v4781', 'v4782', 'v4783', 'v4784', 'v4785', 'v4786', 'v4787', 'v4788', 'v4789', 'v4790', 'v4791', 'v4792', 'v4793', 'v4794', 'v4795', 'v4796', 'v4797', 'v4798', 'v4799', 'v4800', 'v4801', 'v4802', 'v4803', 'v4804', 'v4805', 'v4806', 'v4807', 'v4808', 'v4809', 'v4810', 'v4811', 'v4812', 'v4813', 'v4814', 'v4815', 'v4816', 'v4817', 'v4819', 'v4820', 'v4821', 'v4822', 'v4823', 'v4824', 'v4825', 'v4826', 'v4827', 'v4828', 'v4829', 'v4830', 'v4831', 'v4832', 'v4833', 'v4836', 'v4837', 'v4838', 'v4839', 'v4841', 'v4844', 'v4845', 'v4846', 'v4847', 'v4848', 'v4849', 'v4850', 'v4851', 'v4853', 'v4854', 'v4856', 'v4857', 'v4858', 'v4859', 'v4860', 'v4861', 'v4862', 'v4863', 'v4864', 'v4865', 'v4866', 'v4867', 'v4869', 'v4870', 'v4871', 'v4872', 'v4873', 'v4874', 'v4875', 'v4876', 'v4877', 'v4878', 'v4879', 'v4880', 'v4881', 'v4882', 'v4883', 'v4884', 'v4886', 'v4887', 'v4888', 'v4891', 'v4892', 'v4893', 'v4894', 'v4895', 'v4896', 'v4899', 'v4900', 'v4901', 'v4902', 'v4903', 'v4904', 'v4905', 'v4906', 'v4908', 'v4909', 'v4910', 'v4911', 'v4913', 'v4914', 'v4915', 'v4916', 'v4917', 'v4918', 'v4919', 'v4920', 'v4921', 'v4922', 'v4926', 'v4927', 'v4928' ]

with open("core.c", "r") as f:
    code = f.readlines()
    code = [x.strip() for x in code]

#print(code)

section = None

sections = {}

# sort into sections

for line in code:
    if line == '':
        continue
    if line.endswith(':'):
        section = line[:-1]
        sections[section] = []
    else:
        sections[section].append(line)

#pprint.pprint(sections)

sections_for_variable = {}
variables_for_section = {}
all_variables = []

for section in sections:
    variables = []
    for line in sections[section]:
        variables += re.findall(r'v[0-9]+', line)
    all_variables += variables
    variables = set(variables)
    variables_for_section[section] = variables
    #pprint.pprint(variables)
    for variable in variables:
        if not variable in sections_for_variable:
            sections_for_variable[variable] = []
        sections_for_variable[variable].append(section)

all_variables = set(all_variables)

#pprint.pprint(sections_for_variable)

# print global variables
#for variable in all_variables:
#    if len(sections_for_variable[variable]) > 1:
#        if variable in eightbit:
#            print('u8 ' + variable + ';')
#        elif variable in bool:
#            print('bool ' + variable + ';')
#        else:
#            print('u16 ' + variable + ';')

# print sections, with local variables

for section in sections:
    print('')
    print(section + ':')
    print('{')
    variables = []
    for variable in variables_for_section[section]:
        if len(sections_for_variable[variable]) == 1:
            variables.append(variable)

    for variable in variables:
        if variable in eightbit:
            print('u8 ' + variable + ';')
    for variable in variables:
        if variable in bool:
            print('bool ' + variable + ';')
    for variable in variables:
        if variable not in eightbit and variable not in bool:
            print('u16 ' + variable + ';')
    for line in sections[section]:
        print(line)
    print('}')









