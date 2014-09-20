--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: api_attribute; Type: TABLE DATA; Schema: public; Owner: django
--

COPY api_attribute (id, name, column_name, description) FROM stdin;
1	Total Population	tot_p_p	The number of people who were in a particular region during census night.
39	Age 80-89 years	agep_80_89_years	AGEP 80-89 years\r\n
38	Age 70-79 years	agep_70_79_years	Age 70-79 years\r\n
37	AGEP 60-69 years	agep_60_69_years	Age 60-69 years\r\n
36	Age 50-59 years	agep_50_59_years	AGEP 50-59 years\r\n
4	Islam	relp_islam	All subsets of islam are only available in this one category.
35	Age 40-49 years	agep_40_49_years	Age 40-49 years\r\n
34	Age 30-39 years	agep_30_39_years	Age 30-39 years\r\n
33	AGE 20-29 years	agep_20_29_years	Age 20-29 years\r\n
32	Age 10-19	agep_10_19_years	Age 10-19 years\r\n
31	Age  0-9	agep_0_9_years	Age  0-9
30	Female	sexp_female	Female Sex
29	Male	sexp_male	Male Sex
28	Orthodox	relp_orthodox_tot	Orthodox Christians including Oriental Orthodox, Armenian Apostolic, Coptic Orthodox Church, Syrian Orthodox Church, Ethiopian Orthodox Church, Assyrian Apostolic, Assyrian Church of the East, Ancient Church of the East, Assyrian Apostolic, Eastern Orthodox, Albanian Orthodox, Antiochian Orthodox, Greek Orthodox, Macedonian Orthodox, Romanian Orthodox, Russian Orthodox, Serbian Orthodox, Ukrainian Orthodox, and Eastern Orthodox\r\n
27	Jehovah's Witnesses	relp_jehovah_s_witnesses	Jehovah's Witnesses\r\n
26	Churches of Christ (Conference)	relp_churches_of_christ_conference_	Churches of Christ
25	Church of Jesus Christ of LDS (Mormons)	relp_church_of_jesus_christ_of_lds_mormons_	Mormonism
24	Lutheran	relp_lutheran	Lutheran
23	Macedonian Orthodox	relp_macedonian_orthodox	Macedonian Orthodox
22	Greek Orthodox	relp_greek_orthodox	Greek Orthodox
21	Presbyterian	relp_presbyterian	Presbyterian\r\n
20	Uniting Church	relp_uniting_church	Uniting Church
19	Zoroastrianism	relp_zoroastrianism	Zoroastrianism
18	Jainism	relp_jainism	Jainism
17	No Religion	relp_no_religion_tot	No religion including rationalism, humanism, atheism, agnosticism and no religion.
16	Caodaism	relp_caodaism	Caodaism
15	Spiritualism	relp_spiritualism	Spiritualism
14	Sikhism	relp_sikhism	Sikhism
13	Witchcraft	relp_wiccan_witchcraft	Witchcraft
12	Pantheism	relp_pantheism	Pantheism
11	Paganism	relp_paganism	Paganism
10	Druse	relp_druse	Druse
9	Taoism	relp_taoism	Chinese Taoism
8	Baha'i	relp_baha_i	Baha'i\r\n
7	Australian Aboriginal Traditional Religions	relp_australian_aboriginal_traditional_religions	All Australian Aboriginal Traditional Religions
6	Hinduism	relp_hinduism	All Hindu traditions.
5	Judaism	relp_judaism	All Jewish denominations
3	Anglican	relp_anglican_church_of_australia	The Anglican church is wide-spread in australia
2	Roman Catholic	relp_western_catholic	The Roman Catholic Church is associated with the Vatican.
\.


--
-- Name: api_attribute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('api_attribute_id_seq', 39, true);


--
-- PostgreSQL database dump complete
--

