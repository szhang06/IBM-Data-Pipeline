-- Create a grouping set for the columns year, quartername, sum(billedamount).

SELECT YEAR, quartername, SUM(billedamount)
FROM factbilling 
LEFT JOIN dimmonth ON factbilling.monthid = dimmonth.monthid
LEFT JOIN dimcustomer ON factbilling.customerid = dimcustomer.customerid
GROUP BY GROUPING SETS (YEAR, quartername, billedamount);

-- By using GROUPING SETS, you can generate a result set that includes subtotals 
-- and grand totals in a single query, without having to run multiple queries and combine the results.



-- Create a rollup for the columns country, category, sum(billedamount).

select country, category, sum(billedamount) as totalbilledamount
from factbilling
left join dimcustomer
on factbilling.customerid = dimcustomer.customerid
left join dimmonth
on factbilling.monthid=dimmonth.monthid
group by rollup(country,category )
;



-- Create a cube for the columns year,country, category, sum(billedamount).


select year, country, category, sum(billedamount) as totalbilledamount
from factbilling
left join dimcustomer
on factbilling.customerid = dimcustomer.customerid
left join dimmonth
on factbilling.monthid=dimmonth.monthid
group by cube(year,country, category)
;


-- Create an MQT named average_billamount with columns year, quarter, category, country, average_bill_amount.


CREATE TABLE average_billamount (year,quarter,category,country, average_bill_amount) AS
    (select year,quarter,category,country, avg(billedamount) as average_bill_amount
    from factbilling
    left join dimcustomer
    on factbilling.customerid = dimcustomer.customerid
    left join dimmonth
    on factbilling.monthid=dimmonth.monthid
    group by year,quarter,category,country
    )
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM;


