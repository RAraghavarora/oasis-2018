from .models import StandupSoapboxExtension, GenParticipant

def execute():
    data = [(11, '12', 'NIL', 60, ' 28 June - Bengaluru '), (16, '3', 'None', 67, ' 14 July - Mumbai '), (41, '6 months', 'COME, LAUGHING COCONUT ', 124, ' 28 June - Bengaluru '), (42, '1 year', 'Participated in many open mics organised in jammu city', 125, ' 21 July - Mumbai '), (43, '18', 'Canvas Laugh Club_Twice', 126, ' 5 July - Delhi '), (44, '18', 'Canvas Laugh Club_Twice', 127, ' 5 July - Delhi '), (45, '18', 'Canvas Laugh Club_Twice', 128, ' 5 July - Delhi '), (49, '15', 'Runner up in Funny Side up organised by Vivekananda institute of professional studies', 136, ' 5 July - Delhi '), (50, '9', 'Canvas laugh club open mics', 138, ' 5 July - Delhi '), (51, '3', 'Na', 139, ' 5 July - Delhi '), (52, '5', 'Lsr 2nd prize', 140, ' 5 July - Delhi '), (53, '5', 'Lsr 2nd prize', 141, ' 5 July - Delhi '), (54, '3 months ', 'None', 142, ' 5 July - Delhi '), (55, '3 months ', 'None', 143, ' 5 July - Delhi '), (56, '10 months', 'Clc open mic 3 times ', 144, ' 5 July - Delhi '), (57, '14', 'Lsr,Dcac,DU,Srcc', 145, ' 5 July - Delhi '), (58, '10', 'CLC open mic, the social house ', 146, ' 5 July - Delhi '), (59, '10', 'CLC open mic, the social house ', 147, ' 5 July - Delhi '), (60, '10 months', "Iiit odyssey's 2018 2nd position", 148, ' 5 July - Delhi '), (61, '10 months', "Iiit odyssey's 2018 2nd position", 149, ' 5 July - Delhi '), (62, '24', 'Vio', 150, ' 5 July - Delhi '), (63, '2 months', 'No', 151, ' 5 July - Delhi '), (64, '24', 'ViPs, SRI AURBINDO, ZAKIR HUSSAIN, AMITY NOIDA', 152, ' 5 July - Delhi '), (65, '24', 'ViPs, SRI AURBINDO, ZAKIR HUSSAIN, AMITY NOIDA', 153, ' 5 July - Delhi '), (66, '14 months', 'Jamia hamdard, aryabhatta college (Du), DcAc (Du), ', 154, ' 5 July - Delhi '), (67, '14 months', 'Jamia hamdard, aryabhatta college (Du), DcAc (Du), ', 155, ' 5 July - Delhi '), (68, '12 months', 'NSIT college open mic new Delhi', 157, ' 5 July - Delhi '), (69, '3', 'CLC open mic ,Noida .Dlf Mall of India', 158, ' 5 July - Delhi '), (70, '12months ', '5 open mic at canvas and moodepanti show', 159, ' 5 July - Delhi '), (71, '9', 'MBS fest - 1st Prize', 160, ' 5 July - Delhi '), (72, '15', 'IIt(3rd), ', 162, ' 5 July - Delhi '), (73, '12 months', 'Won canvas open mic 2 times,last year got selected for bits goa competition ', 163, ' 5 July - Delhi '), (74, '12', 'Won at NIT delhi fest  and Miranda house', 164, ' 5 July - Delhi '), (75, '14 months', 'MBS College Of Architecture, Ramanujan college fest by canvas', 165, ' 5 July - Delhi '), (76, '12', 'Won at NIT delhi fest  and Miranda house', 166, ' 5 July - Delhi '), (77, '24 months', 'IIT Delhi, dtu, great Indian Laughter Challenge season 5 Top 7', 167, ' 5 July - Delhi '), (78, '10', 'One of the 3 delhi qualifiers for bits hyderabad, CLC open mics, college competitions', 168, ' 14 July - Mumbai '), (79, '20 months', '1st position at VIPS Spandan and 2nd position at IIT Delhi Randevous', 169, ' 5 July - Delhi '), (80, '6', 'Social house, clc', 170, ' 5 July - Delhi '), (81, '2', 'Na', 172, ' 5 July - Delhi '), (82, '12', 'No', 175, ' 5 July - Delhi '), (83, '12', 'No', 176, ' 5 July - Delhi '), (84, '10 months', 'No competition i have done open mics at clc and playground comedy studio.', 177, ' 5 July - Delhi '), (85, '10 months', 'Clc open mic', 178, ' 5 July - Delhi '), (86, '1', 'Na', 179, ' 5 July - Delhi '), (87, '10', 'No', 180, ' 14 July - Mumbai '), (88, '4 months', 'NA', 181, ' 5 July - Delhi '), (89, '16 months ', '-', 182, ' 21 July - Mumbai '), (90, '16 months ', '-', 183, ' 21 July - Mumbai '), (91, '16 months ', '-', 184, ' 21 July - Mumbai '), (92, '16 months ', '-', 185, ' 21 July - Mumbai '), (93, '12', 'Miranda house,dcac', 187, ' 5 July - Delhi '), (94, '12 months', 'NA', 194, ' 28 June - Bengaluru '), (95, '6', 'na', 195, ' 28 June - Bengaluru '), (96, '6', 'na', 196, ' 28 June - Bengaluru '), (97, '12', 'None', 197, ' 28 June - Bengaluru '), (98, '12', 'None', 198, ' 28 June - Bengaluru '), (99, '8', 'Third place in bits pilani hyderabad pearl 18', 199, ' 28 June - Bengaluru '), (100, '8', 'Third place in bits pilani hyderabad pearl 18', 200, ' 28 June - Bengaluru '), (101, '16months', 'Runner up Bits hyd', 201, ' 28 June - Bengaluru '), (102, '12 months', 'na', 202, ' 28 June - Bengaluru '), (103, '4', 'No', 203, ' 28 June - Bengaluru '), (104, '10', 'None', 204, ' 28 June - Bengaluru '), (105, '10', 'None', 205, ' 28 June - Bengaluru '), (106, '11', 'IIT Hyderabad', 206, ' 28 June - Bengaluru '), (107, '11', 'IIT Hyderabad', 207, ' 28 June - Bengaluru '), (108, '11', 'IIT Hyderabad', 208, ' 28 June - Bengaluru '), (109, '24 months', 'Noop', 209, ' 28 June - Bengaluru '), (110, '24 months', 'Noop', 210, ' 28 June - Bengaluru '), (111, '12 months', 'Have only done shows so far.This is my first competition.', 211, ' 28 June - Bengaluru '), (112, '12 months', 'Have only done shows so far.This is my first competition.', 212, ' 28 June - Bengaluru '), (113, '6 months', 'NA', 215, ' 28 June - Bengaluru '), (114, '6 months', 'NA', 216, ' 28 June - Bengaluru '), (115, '6', 'None', 217, ' 28 June - Bengaluru '), (116, '5 months ', 'No ', 218, ' 28 June - Bengaluru '), (117, '3-4', 'NA', 219, ' 28 June - Bengaluru '), (118, '16-18 months', 'Was runner up of Standup comedy competition organised by tapi brandscan @orian mall banglore.', 220, ' 28 June - Bengaluru '), (119, '10', 'Na', 221, ' 28 June - Bengaluru '), (120, '16-18 months', 'Was runner up of Standup comedy competition organised by tapi brandscan @orian mall banglore. Opened for senior comics like jeeveshu ahluwalia, jagdeesh chaturvedi, mayank parakh. Previous experience: did theatre for 4 years in delhi. Won various titles. One of was the monoacting competition @iit-d fest rendezvous. ', 222, ' 28 June - Bengaluru '), (121, '16-18 months', 'Was runner up of Standup comedy competition organised by tapi brandscan @orian mall banglore. Opened for senior comics like jeeveshu ahluwalia, jagdeesh chaturvedi, mayank parakh. Previous experience: did theatre for 4 years in delhi. Won various titles. One of was the monoacting competition @iit-d fest rendezvous. ', 223, ' 28 June - Bengaluru '), (122, '14', 'Amity stand up (winner) ', 224, ' 28 June - Bengaluru '), (123, '14', 'Amity stand up (winner) ', 225, ' 28 June - Bengaluru '), (124, '10 months', 'Na', 226, ' 28 June - Bengaluru '), (125, '12', 'NA', 229, ' 28 June - Bengaluru '), (126, '8 months', 'no', 230, ' 28 June - Bengaluru '), (127, '9 months', 'Na', 231, ' 28 June - Bengaluru '), (128, '12', 'None', 232, ' 28 June - Bengaluru '), (129, '12', 'None', 233, ' 28 June - Bengaluru '), (130, '4', 'N/A', 238, ' 28 June - Bengaluru '), (131, '3', 'NA', 239, ' 28 June - Bengaluru '), (132, '3', 'NA', 240, ' 28 June - Bengaluru '), (133, '06', 'No', 241, ' 5 July - Delhi '), (134, '06', 'No', 242, ' 5 July - Delhi '), (135, '06', 'No completion won', 243, ' 5 July - Delhi '), (136, '24', 'Jecrc University, Jaipur- 1st prize, Manipal University Jaipur-1st Prize', 256, ' 5 July - Delhi '), (137, '3', 'CLC open mic', 266, ' 5 July - Delhi '), (138, '3', 'CLC open mic', 267, ' 5 July - Delhi '), (139, '0', '0', 268, ' 5 July - Delhi '), (140, '1', '0', 269, ' 5 July - Delhi '), (141, '1', '0', 270, ' 5 July - Delhi '), (142, '10 months', 'No', 285, ' 14 July - Mumbai '), (143, '10 months', 'No', 286, ' 14 July - Mumbai '), (144, '18', 'IIT KHARAGPUR HITCHHIKING - STAND UP (KOLKATA)', 290, ' 28 June - Bengaluru '), (145, 'not yet', "college's society poem writing competition", 300, ' 5 July - Delhi '), (146, '3', '-', 312, ' 5 July - Delhi '), (147, '6', 'no', 322, ' 5 July - Delhi '), (148, '0', 'None', 323, ' 5 July - Delhi '), (149, '4 months', 'Not yet', 325, ' 5 July - Delhi '), (150, '6', 'none', 326, ' 5 July - Delhi '), (151, '7 months', 'Open mics won in canvas club', 329, ' 5 July - Delhi '), (152, '7 months', 'Open mics won in canvas club', 330, ' 5 July - Delhi '), (153, '12', 'No', 331, ' 5 July - Delhi '), (154, '6', 'None', 332, ' 5 July - Delhi '), (155, '6', 'None', 333, ' 5 July - Delhi '), (156, '6', 'None', 334, ' 5 July - Delhi '), (157, '6 months', 'Na', 336, ' 5 July - Delhi '), (158, '6 months', 'Na', 337, ' 5 July - Delhi '), (159, 'No', 'No', 348, ' 5 July - Delhi '), (160, '1 month', 'Attend 15 comedy open mic', 350, ' 5 July - Delhi '), (161, '7 Months', 'No', 366, ' 14 July - Mumbai '), (162, '7 Months', 'No', 367, ' 21 July - Mumbai '), (163, '1 month ', 'First runner up in canvas laugh club ', 370, ' 5 July - Delhi '), (164, '2 years ', 'No', 390, ' 5 July - Delhi '), (165, '13', 'Spring fest 2018, mood indigo 2017', 424, ' 14 July - Mumbai '), (166, '13', 'Spring fest 2018, mood indigo 2017', 425, ' 14 July - Mumbai '), (167, '14', 'Mood indigo,Spring fest', 426, ' 21 July - Mumbai '), (168, '14', 'None', 427, ' 5 July - Delhi '), (169, '14', 'None', 428, ' 14 July - Mumbai '), (170, '14', 'None', 429, ' 21 July - Mumbai '), (171, '14 months', 'Secured 2nd position on tias college and secured 3rd position in rdias', 445, ' 5 July - Delhi '), (172, '8 months ', 'No', 446, ' 14 July - Mumbai '), (173, '16', 'Canvas Laugh Club, twice', 447, ' 5 July - Delhi '), (174, '8 months ', 'No', 448, ' 14 July - Mumbai '), (175, '16', 'Canvas Laugh Club, twice', 449, ' 5 July - Delhi '), (176, '8 months ', 'No', 450, ' 21 July - Mumbai '), (177, '10 months ', 'No', 451, ' 14 July - Mumbai '), (178, '10 months ', 'No', 452, ' 21 July - Mumbai '), (179, '24', 'One Night Stand-Manipal University Jaipur, Stand Up Comedy Competetion-JEcrc University', 457, ' 5 July - Delhi '), (180, '10 months', 'No', 459, ' 21 July - Mumbai '), (181, '1 year', 'Participated in open mic events', 464, ' 5 July - Delhi '), (182, '7', 'Won an open mic at CLC Gurgaon ', 466, ' 5 July - Delhi '), (183, '1 year', 'Won Last year elims of  bits goa ', 467, ' 21 July - Mumbai '), (184, '1 year', 'Won Last year elims of  bits goa ', 468, ' 5 July - Delhi '), (185, '1 year', 'Won Last year elims of  bits goa ', 469, ' 14 July - Mumbai '), (186, '15', 'Canvas laugh club open mic', 470, ' 5 July - Delhi '), (187, '4 months', 'None', 499, ' 5 July - Delhi '), (188, '8', 'I have 2 open mic competitions at canvas laugh club', 502, ' 5 July - Delhi '), (189, '20 months', 'Won a competition having the price to go to London. ', 503, ' 5 July - Delhi '), (190, '24', 'One mic stand- Manipal University, Humour us-Jecrc University.', 504, ' 5 July - Delhi '), (191, '12', 'No', 505, ' 5 July - Delhi '), (192, '12', 'No', 506, ' 5 July - Delhi '), (193, '12', 'No', 507, ' 5 July - Delhi '), (194, '12', 'No', 508, ' 5 July - Delhi '), (195, '12', 'Na', 509, ' 5 July - Delhi '), (196, '12', 'Na', 510, ' 5 July - Delhi '), (197, '3 months', 'Nope', 511, ' 5 July - Delhi '), (198, '3 months', 'Nope', 512, ' 5 July - Delhi '), (199, '15 months', '1. LSR - In hysterics - a stand up comedy competition    2. Pshycogenesis - Kamala nehru - a stand up comedy competition   3.  RJ hunt - indraprastha college for women', 513, ' 5 July - Delhi '), (200, '1 year 3 months', '3rd in iiT delhi', 514, ' 5 July - Delhi '), (201, '12', 'Dcac,miranda house', 515, ' 5 July - Delhi '), (202, '12', 'Dcac,miranda house', 516, ' 5 July - Delhi '), (203, '12', 'Dcac,miranda house', 517, ' 5 July - Delhi '), (204, '12', 'Dcac,miranda house', 518, ' 5 July - Delhi '), (205, '12', 'Dcac,miranda house', 520, ' 5 July - Delhi '), (206, '18', 'Finalist of bits goa 2017, IIFT, DTU', 522, ' 5 July - Delhi '), (207, '18', 'CLC open mic, I choose violence, kamedy carnival', 523, ' 5 July - Delhi '), (208, '18', 'CLC open mic, I choose violence, kamedy carnival', 524, ' 5 July - Delhi '), (209, '18', 'CLC open mic, I choose violence, kamedy carnival', 525, ' 5 July - Delhi '), (210, '10', 'Canvas Laugh Club open mic', 526, ' 5 July - Delhi '), (211, '5 ', 'None', 527, ' 5 July - Delhi '), (212, '24', 'LSR, Hindu, Hansraj, DTu, Mait, etc', 528, ' 5 July - Delhi '), (213, '24', 'LSR, Hindu, Hansraj, DTu, Mait, etc', 529, ' 5 July - Delhi '), (214, '12months', 'None', 530, ' 5 July - Delhi '), (215, '8 month ', 'Clc Maverick and college competition ', 531, ' 5 July - Delhi '), (216, '13 Months ', 'Not ANY', 532, ' 5 July - Delhi '), (217, '8', 'Won 2 open mics at clc Gurgaon', 535, ' 5 July - Delhi '), (218, '6 month', 'Open mic', 536, ' 5 July - Delhi '), (219, '10', 'CLC open mics, College standup competitions', 537, ' 5 July - Delhi '), (220, '10', 'CLC open mics, College standup competitions', 538, ' 5 July - Delhi '), (221, '10', 'CLC open mics, College standup competitions', 539, ' 5 July - Delhi '), (222, '6', '-', 540, ' 5 July - Delhi '), (223, '6', '-', 541, ' 5 July - Delhi '), (224, '30', 'Runner up NDtv rising stars of comedy 2016, winner at Rendezvous 2016', 542, ' 5 July - Delhi '), (225, '30', 'Runner up NDtv rising stars of comedy 2016, winner at Rendezvous 2016', 543, ' 5 July - Delhi '), (226, '10', 'Mba college of architecture first prize', 544, ' 5 July - Delhi '), (227, '11', 'Canvas laugh club open mic', 546, ' 5 July - Delhi '), (228, '3 months', 'I have done 15 open mics', 547, ' 5 July - Delhi '), (229, 'Since berth', 'None', 548, ' 5 July - Delhi '), (230, '14 months', '2nd in TIAS college and 3rd in RDIAS COLLEGE', 549, ' 5 July - Delhi '), (231, '15', 'Runner up in Funny side up, organised by vips', 550, ' 5 July - Delhi '), (232, '18', 'None', 551, ' 5 July - Delhi '), (233, '4', 'Only open mics', 552, ' 5 July - Delhi '), (234, '4', 'Only open mics', 553, ' 5 July - Delhi '), (235, '10 months', 'Iiit d 2nd position', 554, ' 5 July - Delhi '), (236, '10 months', 'Clc open mics thrice', 555, ' 5 July - Delhi '), (237, '18 months', 'Aryabhatt college ( du ), jamia hamdard, dcac ( du )', 556, ' 5 July - Delhi '), (238, '18 months', 'Aryabhatt college ( du ), jamia hamdard, dcac ( du )', 557, ' 5 July - Delhi '), (239, '8', '3 canvas open mics', 558, ' 5 July - Delhi '), (240, '20 months', "1st position at VIPS spandan'17 and 2nd position at IIT Delhi Randevous'17", 559, ' 5 July - Delhi '), (241, '6 months ', 'No ', 564, ' 5 July - Delhi '), (242, '36', 'Radio one LOL champion, kill or die by Nishant tanwar', 565, ' 5 July - Delhi '), (243, '6', 'I only performed in open mics', 566, ' 5 July - Delhi '), (244, '4 months', 'Not yet', 567, ' 5 July - Delhi '), (245, '16', 'None', 568, ' 5 July - Delhi '), (246, '6 months', 'Came second at ClC open mic ', 570, ' 5 July - Delhi '), (247, '6 months', 'Came second at ClC open mic ', 571, ' 5 July - Delhi '), (248, '12', 'Haven’t participated in a competitio:(', 577, ' 5 July - Delhi '), (249, '12 months ', 'Canvas open mic 2 times ,Qualified last year bits compitition', 584, ' 5 July - Delhi '), (250, '12 months ', 'Canvas open mic 2 times ,Qualified last year bits compitition', 585, ' 5 July - Delhi '), (251, '1', 'None', 586, ' 5 July - Delhi '), (252, '1 month', 'Just participation certificate', 587, ' 5 July - Delhi '), (253, '1 month', 'Just participation certificate', 588, ' 5 July - Delhi '), (254, '10 Months', 'Aakar- Stand up comedy fest of MBS school of planning and architecture', 589, ' 5 July - Delhi '), (255, '10 Months', 'Aakar- Stand up comedy fest of MBS school of planning and architecture', 590, ' 5 July - Delhi '), (256, '10 Months', 'Aakar- Stand up comedy fest of MBS school of planning and architecture,', 591, ' 5 July - Delhi '), (257, '10 Months', 'Aakar- Stand up comedy fest of MBS school of planning and architecture,', 592, ' 5 July - Delhi '), (258, '10 Months', 'Aakar- Stand up comedy fest of MBS school of planning and architecture,', 593, ' 5 July - Delhi '), (259, '10 Months', 'Aakar- Stand up comedy fest of MBS school of planning and architecture,', 594, ' 5 July - Delhi '), (260, '10 months', '1st prize in aakar-Stand up comedy fest in mbs school of planning and architecture', 599, ' 5 July - Delhi '), (261, '12', 'Won at NIT delhi fest  and Miranda house', 601, ' 5 July - Delhi '), (262, '12', 'Won at NIT delhi fest  and Miranda house', 602, ' 5 July - Delhi '), (263, '2 years ', 'Iit delhi', 605, ' 5 July - Delhi '), (264, '1 month', 'Just participation certificate', 611, ' 5 July - Delhi '), (265, '6', 'Clc, social house', 630, ' 5 July - Delhi '), (266, '10 months', 'Iiit d 2nd position', 631, ' 5 July - Delhi '), (267, '12', 'Dcac,maitreyi', 632, ' 5 July - Delhi '), (268, '16', 'None', 633, ' 5 July - Delhi '), (269, '12months ', '5 open mic at canvas and moodepanti show', 634, ' 5 July - Delhi '), (270, '7 Months', 'Canvas club open mics ', 635, ' 5 July - Delhi '), (271, '18', 'Canvas ', 636, ' 5 July - Delhi '), (272, '14', 'Runners up at a local college fest stand up competition ', 637, ' 14 July - Mumbai '), (273, '14', 'Runners up at a local college fest stand up competition ', 638, ' 14 July - Mumbai '), (274, '6 months', 'Won first prize in zakir hussain college (Du), won first prize in nss shivaji college (du)', 639, ' 5 July - Delhi '), (275, '6 months', 'Won first prize in zakir hussain college (Du), won first prize in nss shivaji college (du)', 640, ' 5 July - Delhi '), (276, '36', 'Whooooookkk', 641, ' 5 July - Delhi '), (277, '9', 'None', 642, ' 5 July - Delhi '), (278, '11 months', "Winner of standup comedy Competitio in the fest 'Genesis' of Maharaja Surajmal institute", 643, ' 5 July - Delhi '), (279, '20 months', 'Qualified for Bits Hyderabad from Delhi. Going to London after winning a show. 2 open mics won in Canvas Laugh Club.', 644, ' 5 July - Delhi '), (280, '5 ', 'NA', 645, ' 5 July - Delhi '), (281, '12 months', 'Canvas Laugh Club Gurgaon', 646, ' 5 July - Delhi '), (282, '9 months', 'won 2 open mic competitions at canvas laugh club', 647, ' 5 July - Delhi '), (283, '1', 'no', 658, ' 5 July - Delhi '), (284, '1', 'no', 659, ' 5 July - Delhi '), (285, '1', 'no', 660, ' 5 July - Delhi '), (286, '5', 'NA', 661, ' 5 July - Delhi '), (287, '5', 'NA', 662, ' 5 July - Delhi '), (288, '6 months', 'Never', 684, ' 14 July - Mumbai '), (289, '19 months', 'Clc, classic comic hunt for Pune comedy festival, few open mics in mumbai', 690, ' 14 July - Mumbai '), (290, '12 months and more', 'Canvas Laugh Club open mic.', 691, ' 14 July - Mumbai '), (291, '15', 'Laughing coconut, come', 692, ' 21 July - Mumbai '), (292, '5', 'No', 693, ' 21 July - Mumbai '), (293, '18', 'No', 694, ' 21 July - Mumbai '), (294, '15', 'COMe', 695, ' 14 July - Mumbai '), (295, '21', 'CLC, Laughing coconut', 696, ' 14 July - Mumbai '), (296, '2', 'none (yet!)', 697, ' 14 July - Mumbai '), (297, '1 year', '1 in canvas 1 in laughing coconut', 698, ' 14 July - Mumbai '), (298, '9', 'CLC, wtf, backstage, come, onenest', 699, ' 14 July - Mumbai '), (299, '16', 'Won 4 open mics in Canvas laugh club ', 700, ' 21 July - Mumbai '), (300, '16', 'Won 4 open mics in Canvas laugh club ', 702, ' 21 July - Mumbai '), (301, '16 months', 'Finalist PEARL 2017, Won twice at Canvas laugh club, top 30 of gREAT iNDIAN LAUGHTER CHALLENGE', 706, ' 21 July - Mumbai '), (302, '16 months', 'Finalist PEARL 2017, Won twice at Canvas laugh club, top 30 of gREAT iNDIAN LAUGHTER CHALLENGE', 708, ' 21 July - Mumbai '), (303, '18', 'Come open mic, laughing coconut, a participant in the great Indian laughter challenge', 709, ' 21 July - Mumbai '), (304, '18', 'Come open mic, laughing coconut, a participant in the great Indian laughter challenge', 710, ' 21 July - Mumbai '), (305, '3 months', 'None', 711, ' 14 July - Mumbai '), (306, '3 months', 'No.', 712, ' 14 July - Mumbai '), (307, '18 months', 'Mood indigo iit bombay , canvas laugh club three times , comedy ladser two times , laughing coconut three times , come grand slam once , tunning fork one time', 713, ' 21 July - Mumbai '), (308, '18', 'Canvas openmic', 714, ' 14 July - Mumbai '), (309, '15', 'Clc', 715, ' 21 July - Mumbai '), (310, '06', 'No', 716, ' 14 July - Mumbai '), (311, '06', 'No', 717, ' 14 July - Mumbai '), (312, 'One and Half year', 'Come ladder', 718, ' 14 July - Mumbai '), (313, '10', 'Canvas laugh club, laughing coconut, habitat', 719, ' 14 July - Mumbai '), (314, '18 months', "Semi finalist on a stand up tv show 'Queens of Comedy'", 720, ' 21 July - Mumbai '), (315, '24', '2 open mics ', 721, ' 21 July - Mumbai '), (316, '24', '2 open mics ', 722, ' 21 July - Mumbai '), (317, '18 months ', 'Mood indigo, sm shetty annual College fest ', 723, ' 14 July - Mumbai '), (318, '18 months ', 'Mood indigo, sm shetty annual College fest ', 724, ' 14 July - Mumbai '), (319, '18 months ', 'Mood indigo, sm shetty annual College fest ', 725, ' 14 July - Mumbai '), (320, '8', 'No', 726, ' 21 July - Mumbai '), (321, '8 Months', 'None', 727, ' 21 July - Mumbai '), (322, '8 Months', 'None', 728, ' 21 July - Mumbai '), (323, '6 months eh.', "I win a lot of aww's.", 729, ' 14 July - Mumbai '), (324, '3 months', 'None', 730, ' 14 July - Mumbai '), (325, '3 months', 'None', 731, ' 14 July - Mumbai '), (326, '14', 'Opened for Sorabh pant at the annual cultural Festival of IISER Pune last year', 734, ' 21 July - Mumbai '), (327, '18', 'Classic comic hunt pune', 751, ' 21 July - Mumbai '), (328, '12', '2 praiz in akhil bhartiya kavi sammelan indore', 766, ' 14 July - Mumbai '), (329, '12', '2 praiz in akhil bhartiya kavi sammelan indore', 767, ' 14 July - Mumbai '), (330, '4', 'No', 785, ' 14 July - Mumbai '), (331, '4', 'No', 786, ' 14 July - Mumbai '), (332, '10', '2 Laughing coconut', 787, ' 21 July - Mumbai '), (333, '12', 'second position, come (comedy open mic evening) #50', 824, ' 21 July - Mumbai '), (334, '15', 'Come', 842, ' 21 July - Mumbai '), (335, '24', '2 open mics ', 843, ' 21 July - Mumbai '), (336, '24', '2 open mics ', 844, ' 21 July - Mumbai '), (337, '18', 'CLC, COME SET GOLD, LAUGHING COCONUT, ISB&M STAND UP COMPETITION, STAND UP FEVER, ETC. ', 845, ' 21 July - Mumbai '), (338, '12', 'Canvas laugh club', 846, ' 14 July - Mumbai '), (339, '13 months', 'Tuning fork open mics, COme open mics', 847, ' 21 July - Mumbai '), (340, '15 months ', "None. I'm an Underdog. ", 848, ' 21 July - Mumbai '), (341, '18 months', 'Mood indigo iit bombay , tunning fork once , comedy ladder twice , comedy grand slam once , laughing coconut thrice ,canvas laugh club thrice', 849, ' 21 July - Mumbai '), (342, '8 months', 'None', 850, ' 14 July - Mumbai '), (343, '8 months', 'None', 851, ' 14 July - Mumbai '), (344, '10', 'Canvas laugh club, laughing coconut, habitat', 852, ' 14 July - Mumbai '), (345, '11 months', 'Preformed in the great indian laughter challenge', 853, ' 14 July - Mumbai '), (346, '36 months ', 'Canvas Laugh Club, laughing coconut open mics ', 854, ' 14 July - Mumbai '), (347, '11 months', 'Preformed in the great indian laughter challenge', 855, ' 14 July - Mumbai '), (348, '1 year', '1 in canvas 1 in laughing coconut', 856, ' 14 July - Mumbai '), (349, '12 months and more', 'Canvas Laugh Club open mic.', 857, ' 14 July - Mumbai '), (350, '8', '3 times clc runner up', 858, ' 21 July - Mumbai '), (351, '8', '3 times clc runner up', 859, ' 21 July - Mumbai '), (352, '17', 'Come open mic, laughing coconut, participant in the great Indian laughter challenge season 5', 860, ' 14 July - Mumbai '), (353, '12', 'Bakstage open mic', 861, ' 14 July - Mumbai '), (354, '3 months', 'None', 862, ' 21 July - Mumbai '), (355, '11 months', 'Comedy Ladder open mics - Twice', 863, ' 14 July - Mumbai '), (356, '11 months', 'Comedy Ladder open mics - Twice', 864, ' 14 July - Mumbai '), (357, '6', 'Runners up at canvas laugh club', 865, ' 21 July - Mumbai '), (358, '6', 'Runners up at canvas laugh club', 866, ' 21 July - Mumbai '), (359, '8Months', 'No', 875, ' 21 July - Mumbai '), (360, '12', 'Open Mics in Mumbai', 879, ' 21 July - Mumbai '), (361, '12', 'Comedy ladder ', 882, ' 21 July - Mumbai '), (362, '3', 'Comics Unplugged Vol.10 by Frontline comedy', 883, ' 14 July - Mumbai '), (363, '3', 'Comics Unplugged Vol.10 by Frontline comedy', 884, ' 21 July - Mumbai '), (364, '1 month ', 'No', 885, ' 21 July - Mumbai '), (365, '11 month', 'Half baked', 886, ' 14 July - Mumbai '), (366, '11 month', 'Half baked', 887, ' 14 July - Mumbai '), (367, 'Coming as audience', 'None', 888, ' 14 July - Mumbai '), (368, '12 months', 'Open mic in social house, Delhi', 891, ' 21 July - Mumbai '), (369, '2 months', 'NA', 892, ' 21 July - Mumbai '), (370, '10 months', 'No', 911, ' 21 July - Mumbai ')]

    for entry in data:
        participant = GenParticipant.objects.get(id=entry[3])
        StandupSoapboxExtension.objects.create(id=entry[0], participant=participant, time_doing_standup=entry[1], previous_competition=entry[2], city_of_participation=entry[4])