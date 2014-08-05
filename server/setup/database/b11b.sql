DROP TABLE IF EXISTS b11b_aust_lga_short;

CREATE TABLE b11b_aust_lga_short(
region_id character(8),
P_SOL_SE_Tot_2001_2005 numeric,
P_SOL_SE_Tot_2006 numeric,
P_SOL_SE_Tot_2007 numeric,
P_SOL_SE_Tot_2008 numeric,
P_SOL_SE_Tot_2009 numeric,
P_SOL_SE_Tot_2010 numeric,
P_SOL_SE_Tot_2011 numeric,
P_SOL_SE_Tot_arrival_ns numeric,
P_SOL_SE_Tot_Total numeric,
P_L_prof_Eng_ns_bf1996 numeric,
P_L_prof_Eng_ns_1996_2000 numeric,
P_L_prof_Eng_ns_2001_2005 numeric,
P_L_prof_Eng_ns_2006 numeric,
P_L_prof_Eng_ns_2007 numeric,
P_L_prof_Eng_ns_2008 numeric,
P_L_prof_Eng_ns_2009 numeric,
P_L_prof_Eng_ns_2010 numeric,
P_L_prof_Eng_ns_2011 numeric,
P_L_prof_Eng_ns_arrival_ns numeric,
P_L_prof_Eng_ns_Total numeric,
P_Tot_bf1996 numeric,
P_Tot_1996_2000 numeric,
P_Tot_2001_2005 numeric,
P_Tot_2006 numeric,
P_Tot_2007 numeric,
P_Tot_2008 numeric,
P_Tot_2009 numeric,
P_Tot_2010 numeric,
P_Tot_2011 numeric,
P_Tot_Yr_arrival_not_stated numeric,
P_Tot_Total numeric
)
WITH(OIDS=FALSE);
\copy b11b_aust_lga_short from 'census2011/2011Census_B11B_AUST_LGA_short.csv' with (format csv, header);
-- todo kill the unwanted columns
