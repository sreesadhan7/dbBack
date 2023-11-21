# This file containes list of queries and needs string formatting

# 3 filter in mackup_1_1
# country,  agg , and  years range 

mockup_1_1 = """WITH gloabl_atmosphere_temp_yearly AS
    (SELECT country,
        EXTRACT(YEAR FROM time_stamp) as time_stamp,
        ROUND(AVG(temperature_monthly_mean), 2) atm_temp_yearly_mean
    FROM 
        Global_Atmosphere_Temperature 
    GROUP BY 
        country, EXTRACT(YEAR FROM time_stamp)
    ),

surface_and_atmosphere as 
    (SELECT 
        ga.country, 
        EXTRACT(YEAR FROM gs.time_stamp) year,
        atm_temp_yearly_mean atmosphere_temp, 
        temperature surface_temp
    FROM 
        gloabl_atmosphere_temp_yearly ga 
        INNER JOIN 
        Global_Surface_Temperature gs 
        ON ga.country = gs.country AND ga.time_stamp = EXTRACT(YEAR FROM gs.time_stamp)),

year_temps as 
    (SELECT * FROM surface_and_atmosphere WHERE 
        country = '{0}' ORDER BY year
    ),

year_temp_country_code AS
    (
        SELECT 
            cp.c_code_ISO3 country, 
            year, 
            atmosphere_temp, 
            surface_temp 
        FROM 
            year_temps yt 
            INNER JOIN country_prime cp ON yt.country = cp.country_source
    ),

YearGroups AS (
    SELECT 
        year,
        country,
        surface_temp,
        atmosphere_temp,
        ceil(((year - MIN(year-1) OVER ())/{1})) AS year_group
    FROM 
        year_temp_country_code ORDER BY year
)
--SELECT * FROM YearGroups;
SELECT 
    MIN (year) YEAR,
    avg(surface_temp) avg_surface_temp,
    avg(atmosphere_temp) avg_atmosphere_Temp
FROM 
    YearGroups
WHERE
    year > {2} and year <= {3}
GROUP BY
    year_group
ORDER BY
    YEAR"""
# country, agg, year range
#temp = mockup_1_1.format('Afghanistan', 5, 1960, 2022)

#-------------------------------------------------------------------------------------------------------------

# no paraeters in mockup_1_2
mockup_1_2 = """WITH Lag_temperatures AS (
SELECT
    Country, 
    time_stamp,
    EXTRACT(YEAR FROM time_stamp) year,
    temperature_monthly_mean,
    LAG(temperature_monthly_mean,12) OVER(PARTITION BY Country ORDER BY time_stamp)  temp_lag
FROM Global_Atmosphere_Temperature
WHERE  EXTRACT(YEAR FROM time_stamp)>= 1970),

temp_pct_change AS (
SELECT
    country, 
    temperature_monthly_mean,temp_lag, year,
    ABS(ROUND((temp_lag - temperature_monthly_mean)/ABS(temp_lag) *100, 2)) as pct_change
FROM Lag_temperatures),

temperature_shifts as (
SELECT 
    year, country, count(*) anomalous_months
FROM temp_pct_change 
WHERE pct_change > 30 
GROUP BY Year, Country)

SELECT year, COUNT(*) countries_count_experiencing_temp_shifts
FROM temperature_shifts 
WHERE anomalous_months >= 3 AND (Year > {0} AND Year < {1}) 
GROUP BY Year 
Order BY Year""" 
#no parameters 

#-------------------------------------------------------------------------------------------------------------
mockup_1_3  = """WITH temperature_year_extraction AS
(SELECT EXTRACT(YEAR FROM time_stamp) year ,
    Global_Atmosphere_Temperature.*   FROM Global_Atmosphere_Temperature)

SELECT distinct year,
Round(AVG(temperature_monthly_mean) OVER ( PARTITION BY country,year  Order By year, 2)) yearly_temp_mean,
Round(STDDEV(temperature_monthly_mean) OVER ( PARTITION BY country, year Order By year, 2)) yearly_temp_std,
Round(Min(temperature_monthly_mean) OVER ( PARTITION BY country, year Order By year, 2)) yearly_temp_min,
Round(Max(temperature_monthly_mean) OVER ( PARTITION BY country, year Order By year, 2)) yearly_temp_max
FROM temperature_year_extraction 
WHERE country = '{0}' AND (year > {1} AND year < {2})
ORDER BY Year
""" 
# country and year filters
#temp = mockup_1_3.format('Afghanistan',  1960, 2022)

#-------------------------------------------------------------------------------------------------------------
# -- Mockup 2.1
# -- carbon emissions are in million metric tons
# -- parameters N countries, year range (AGG filter can be added if required)
# -- c!

mockup_2_1 = """WITH top_n_polluters AS (
SELECT 
    country, sum(total) total_emissions 
FROM CO2_Emission 
WHERE EXTRACT ( Year FROM time_stamp) > 1960
GROUP BY Country
ORDER By total_emissions desc
FETCH NEXT {0} ROWs ONLY)

SELECT  
    Extract(Year FROM time_stamp) as year,country,  total co2_emission_million_metric_tons   
FROM CO2_Emission
WHERE country IN ( SELECT country FROM  top_n_polluters)
    AND (EXTRACT ( Year FROM time_stamp) > {1} AND EXTRACT ( Year FROM time_stamp) < {2})
    Order By country, year
"""
# top_n_countries, year range
temp = mockup_2_1.format(10,  1960, 2022)

#-------------------------------------------------------------------------------------------------------------
# -- Mockup 2.2
# -- Mockup 2.2
# -- co2, gdp, surface_temperature
# -- country, year range
# -- Needs dual axis charts
mockup_2_2 = """SELECT 
    Extract(Year From c.time_stamp) as year, 
    c.total co2_emissions, 
    g.gdp/1000000000 gdp_in_billions, 
    gst.temperature surface_temperature
FROM CO2_Emission c
    INNER JOIN GDP g ON c.country = g.country AND g.time_stamp = c.time_stamp
    INNER JOIN Global_Surface_Temperature gst ON c.country = gst.country 
    AND c.time_stamp = gst.time_stamp
WHERE c.country = '{0}'
     AND (EXTRACT ( Year FROM c.time_stamp) > {1} 
     AND EXTRACT ( Year FROM c.time_stamp) < {2})
ORDER BY c.country, year
"""
# country and year filters
temp = mockup_2_2.format('United States', 1960, 2022)

#-------------------------------------------------------------------------------------------------------------
# -- mockup 2.3
# -- carbon intensity vs GDP
# -- dual axis charts
# -- country and year filters
mockup_2_3 = """SELECT 
    EXTRACT(Year FROM c.time_stamp) as year, 
    round(c.total/g.population*1e6, 2) carbon_intensity, 
    g.gdp/1000000000 gdp_in_billions
FROM CO2_Emission c
    INNER JOIN GDP g ON c.country = g.country AND g.time_stamp = c.time_stamp
    INNER JOIN Global_Surface_Temperature gst ON c.country = gst.country 
    AND c.time_stamp = gst.time_stamp
WHERE c.country = '{0}'
     AND (EXTRACT ( Year FROM c.time_stamp) > {1} 
     AND EXTRACT ( Year FROM c.time_stamp) < {2})
ORDER BY Year
"""
# country and year filters
temp = mockup_2_3.format('United States', 1960, 2022)

#-------------------------------------------------------------------------------------------------------------
# -- mockup 2.4
# -- Eco-friendly vs Non-eco friendly Nations
# -- for the given year, if the countries emissions or 
# -- double than the average of all countries, then its non ecofriendly
# -- c3
#-- no parameters
mockup_2_4 = """
WITH co2_emission_year AS (
    SELECT country, Extract(YEAR FROM time_stamp) year, total emissions FROM co2_emission
    WHERE Extract(YEAR FROM time_stamp) > 1990),

Yearly_pollutions as (SELECT distinct year, round(AVG(emissions) 
                        OVER (PARTITION BY year), 2)*1.5 average_year_emissions 
FROM co2_emission_year),

countries_classification AS (SELECT 
    country, year,
        CASE 
     WHEN emissions > (SELECT AVG(average_year_emissions) FROM Yearly_pollutions 
                        WHERE Yearly_pollutions.year = year) THEN 'NF'
     WHEN emissions < (SELECT AVG(average_year_emissions) FROM Yearly_pollutions 
                        WHERE Yearly_pollutions.year = year) THEN 'F'
     ELSE 'N'
     END As Status
     FROM co2_emission_year)
     
SELECT year, count(*) non_eco_friendly_countries
FROM countries_classification 
WHERE Status = 'NF' AND (Year > {0} AND Year < {1}) 
GROUP BY Year
ORDER BY year
"""

#-------------------------------------------------------------------------------------------------------------
# -- Mockup 3.1
# -- parameters top_n_countries row 10, AGG 38 line,  year filter 49 
# -- created a new column clasffication that resembles the country and performed summaries on it
# -- electricity unit Terawatt-hour 
# -- c4

mockup_3_1 = """
WITH Top_n_consumers AS (
    SELECT country, sum(net_consumption) as last_10_year_consumption
    FROM Electricity 
    WHERE EXTRACT(year FROM time_stamp) > 1980
    GROUP BY country
    order by last_10_year_consumption DESC
    FETCH NEXT {0} ROWS ONLY
),

countries_group AS(
    SELECT 
    EXTRACT(year FROM time_stamp) year,
    country,
    net_consumption,

    CASE
        WHEN country in (SELECT country from Top_n_consumers) THEN country
        WHEN country not in (SELECT country from Top_n_consumers) THEN 'rest_of_countries'
        ELSE 'unclassfied'
        END AS classification  
    FROM Electricity
),

countries_agg AS (SELECT 
    year, classification, sum(net_consumption) total_consumption
    FROM countries_group
    GROUP BY classification, year
    ORDER BY Year),

Groupingyears AS (
    SELECT 
        year,
        classification,
        total_consumption,
        ceil(((year - MIN(year-1) OVER ())/{1})) AS year_group
    FROM 
        countries_agg ORDER BY year
)
--SELECT * FROM Groupingyears;
SELECT 
    MIN (year) YEAR,
    classification,
    round(sum(total_consumption), 0) total_consumption
FROM Groupingyears
WHERE year > {2} and year <= {3}
GROUP BY year_group, classification
ORDER BY classification, YEAR 
"""
# top_n_countries  AGG  year 
temp = mockup_3_1.format(10, 1, 1960, 2022)

#-------------------------------------------------------------------------------------------------------------
# -- Mockup 3.2
# -- Filter country and years
mockup_3_2 = """
SELECT
    EXTRACT(year FROM e.time_stamp) year,
    round(e.net_consumption, 0) electricity_consumption,
    round(c.total, 0) toatl_co2_emissions
FROM Electricity e INNER JOIN co2_emission c 
    ON e.country = c.country AND e.time_stamp = c.time_stamp
WHERE e.country = '{0}' AND
    (EXTRACT(year FROM e.time_stamp)> {1} 
    AND EXTRACT(year FROM e.time_stamp)< {2})
"""

temp = mockup_3_2.format('United States', 1960, 2022)

#-------------------------------------------------------------------------------------------------------------
# -- Mockup 4.1
# -- Filter years
# -- ranks can be calulated based on gdp per capita or total gdp
# -- possible c5

mockup_4_1 = """WITH GDP_year AS (
    SELECT country, gdp gross, 
    EXTRACT(year FROM time_stamp) year
    FROM GDP
),
gdp_rank_cte AS (
SELECT 
    year, 
    country, 
    DENSE_RANK() OVER ( PARTITION BY Year ORDER BY gross DESC ) as gdp_rank  
FROM GDP_year
WHERE Year > {1} and year < {2}
)
SELECT year, country, gdp_rank
FROM gdp_rank_cte
WHERE gdp_rank <= {0}
ORDER BY  Country, Year
"""
# only year filters
#temp = mockup_4_1.format( 1960, 2022)


#-------------------------------------------------------------------------------------------------------------
# -- Mockup 4.2
# -- Filter years, top N
# -- calculations based on gdp per capita

mockup_4_2 = """
WITH Top_n_gdp_per_capita AS (
    SELECT country, avg(gdp_per_capita) as last_10_year_per_capita_avg
    FROM GDP 
    WHERE EXTRACT(year FROM time_stamp) > 2005
    GROUP BY country
    order by last_10_year_per_capita_avg DESC
    FETCH NEXT {0} ROWS ONLY
),

countries_group AS(
    SELECT 
    EXTRACT(year FROM time_stamp) year,
    country,
    gdp_per_capita,
    
    CASE
        WHEN country in (SELECT country from Top_n_gdp_per_capita) THEN country
        WHEN country not in (SELECT country from Top_n_gdp_per_capita) THEN 'rest_of_countries'
        ELSE 'unclassfied'
        END AS classification  
    FROM GDP
)

SELECT 
    year, classification country, 
    round(avg(gdp_per_capita)/1000, 1) total_consumption
    FROM countries_group
    WHERE year > {1} AND year < {2}
    GROUP BY classification, year
    ORDER BY classification,Year
"""
# number of  countries and year filter
#temp = mockup_4_2.format( 10, 1960, 2022)


#-------------------------------------------------------------------------------------------------------------
# -- Mockup 5
# -- Filter years and country
# -- growth rate of internet users
# -- c5

mockup_5 = """
WITH internet_year AS(
    SELECT  country, 
            EXTRACT(year FROM time_stamp) year,
            internet_users_percent iup
    FROM    Internet
    ),

internet_lag AS (SELECT 
    country,
    year,
    iup,
    LAG(iup, 1) OVER(PARTITION BY country ORDER BY year) as previous_year_iup
    FROM internet_year)

SELECT year, iup,  
    CASE 
    WHEN previous_year_iup =0 THEN 0
    WHEN previous_year_iup > 0 THEN round(((iup/previous_year_iup) - 1)*100, 1)
    ELSE 0
    END AS  growth_rate 
    FROM internet_lag 
    WHERE Country = '{0}'
        AND (Year > {1} AND Year < {2})
    ORDER BY Year
"""

# country and years
#temp = mockup_5.format('India', 1990, 2022)

records_count = """
SELECT  (SELECT COUNT(*) FROM country_prime) + 
        (SELECT COUNT(*) FROM Global_Surface_Temperature) +
        (SELECT COUNT(*) FROM Electricity) +
        (SELECT COUNT(*) FROM GDP) +
        (SELECT COUNT(*) FROM Global_Atmosphere_Temperature) +
        (SELECT COUNT(*) FROM CO2_Emission) +
        (SELECT COUNT(*) FROM Internet) as num_records
FROM Dual"""











