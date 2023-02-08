

### Introdução

1. Banco de Dados -> Database
2. Tabela -> Table
3. Colunas -> Columns, features, atributes
4. Diagrama Entidade Relacionamento ->  **Entity Relationship Diagrams**
5. **Statments** -> dizem ao banco de dados o que você gostaria de fazer com os dados

4. Diagrama Entidade Relacionamento
	É um método comum para visualizar dados de uma banco de dados. Através dele podemos visualizar o nome das tabelas, as colunas de cada tabela e como as tabelas trabalham entre si.
	O pé de galinha (crow’s foot) - indica que uma tabela se relaciona com todas as colunas da outra tabela

Qual a vantagem do SQL? 
- O SQL nos permite responder questões mais complexas
- Integridade
- Acessado e compartilhado facilmente

```bash
$ createdb parch 
$ psql parch < parch_and_posey.sql
```

- SQL Basics
    - ORDER BY
    - LIMIT
    - LIKE
    - IN | NOT IN
    - LOGICAL OPERATORS
    - BETWEEN
    ```sql
    SELECT id, account_id, total_amt_usd
    FROM orders
    ORDER BY account_id, total_amt_usd DESC
    
    SELECT id, account_id, total_amt_usd
    FROM orders
    ORDER BY  total_amt_usd DESC, account_id ASC;
    
    SELECT *
    FROM orders
    WHERE gloss_amt_usd >= 1000
    LIMIT 5
    
    SELECT *
    FROM orders
    WHERE total_amt_usd < 500
    LIMIT 10
    
    # derived column
    
    SELECT id, (standard_amt_usd/total_amt_usd)*100 AS std_percent, total_amt_usd
    FROM orders
    LIMIT 10;
    
    SELECT id, account_id, (standard_amt_usd / standard_qty) as unit_price
    FROM orders 
    LIMIT 10
    
    SELECT id, account_id, 
       poster_amt_usd/(standard_amt_usd + gloss_amt_usd + poster_amt_usd) AS post_per
    FROM orders
    LIMIT 10;
    
    SELECT name
    FROM accounts
    WHERE name LIKE 'C%'
    
    SELECT name
    FROM accounts
    WHERE name LIKE '%one%'
    
    SELECT name
    FROM accounts
    WHERE name LIKE '%s'
    
    SELECT name, primary_poc, sales_rep_id
    FROM accounts
    WHERE name IN ('Walmart','Target','Nordstrom')
    
    SELECT *
    FROM web_events
    WHERE channel IN ('organic','adwords')
    
    ****SELECT name, primary_poc, sales_rep_id
    FROM accounts
    WHERE name NOT IN ('Walmart','Target','Nordstrom')
    
    SELECT *
    FROM web_events
    WHERE channel NOT IN ('organic','adwords')
    
    SELECT standard_qty, poster_qty, gloss_qty
    FROM orders
    WHERE standard_qty < 1000 AND poster_qty = 0 AND gloss_qty = 0
    
    SELECT name
    FROM accounts
    WHERE name NOT LIKE 'C%' AND name LIKE '%s'
    
    SELECT occurred_at, gloss_qty
    FROM orders
    WHERE gloss_qty BETWEEN 24 and 29
    
    SELECT *
    FROM web_events
    WHERE channel IN ('organic','adwords')
    AND occurred_at BETWEEN '2016-01-01' AND '2017-01-01'
    ORDER BY occurred_at DESC
    
    SELECT id
    FROM orders
    WHERE gloss_qty > 4000 OR poster_qty > 4000
    
    SELECT *
    FROM orders
    WHERE standard_qty = 0 AND (poster_qty < 1000) OR (gloss_qty < 1000)
    
    SELECT *
    FROM accounts
    WHERE (name LIKE 'C%' OR name LIKE 'W%') AND
    ((primary_poc LIKE '%ana%') OR (primary_poc LIKE '%Ana%')
    AND primary_poc NOT LIKE '%eana%')
    ```   
- SQL Joins
    - **A primary key exists in every table, and it is a column that has a unique value for every row.**
    - **Foreign Key (FK):** A **foreign key** is a column in one table that is a primary key in a different table. We can see in the Parch & Posey ERD that the foreign keys are:
    - region_id é linkado ao id na outra tabela. na tabela region tenho vários desses ids
    - outros tipos de join, são usados quando não existe o mesmo dado em ambas as tabelas
    - SELECT * FROM left table LEFT JOIN right table
    - JOIN (INNER JOIN technically), we only get rows that show up in both tables
    
    ```sql
    SELECT *
    FROM orders
    JOIN accounts
    ON orders.account_id = accounts.id
    
    SELECT orders.standard_qty, 
    	   orders.gloss_qty,
    	   orders.poster_qty, 
           accounts.website, 
           accounts.primary_poc
    FROM orders
    JOIN accounts
    ON orders.account_id = accounts.id
    LIMIT 10
    
    SELECT a.primary_poc, a.name, w.occurred_at, w.channel
    FROM web_events w
    JOIN accounts a
    ON w.account_id = a.id
    WHERE a.name = 'Walmart'
    
    SELECT r.name region_name, s.name sales_name, a.name account_name
    FROM sales_reps s
    JOIN region r
    ON s.region_id = r.id
    JOIN accounts a
    ON s.id = a.sales_rep_id
    ORDER BY a.name
    
    SELECT 
    	 r.name region_name, 
         a.name accounts_name, 
         (o.total_amt_usd / (o.total_amt_usd + 0.01)) unit_price 
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    JOIN sales_reps s
    ON s.id = a.sales_rep_id
    JOIN region r
    ON r.id = s.region_id
    
    ```
-  JOIN PRACTICING
	* Provide a table that provides the **region** for each **sales_rep** along with their associated **accounts**. This time only for the `Midwest` region. Your final table should include three columns: the region **name**, the sales rep **name**, and the account **name**. Sort the accounts alphabetically (A-Z) according to account name.
        
        ```sql
        SELECT r.name as RegionName, 
        			 s.name as SalesRepName, 
               a.name as AccountsName
        FROM sales_reps s
        		 JOIN region r
        		 ON s.region_id = r.id
        JOIN accounts a
        		ON s.id = a.sales_rep_id 
        WHERE r.name = 'Midwest'
        ORDER BY a.name 
        ```
        
        - Provide a table that provides the **region** for each **sales_rep** along with their associated **accounts**. This time only for accounts where the sales rep has a first name starting with `S` and in the `Midwest` region. Your final table should include three columns: the region **name**, the sales rep **name**, and the account **name**. Sort the accounts alphabetically (A-Z) according to account name.
        
        ```sql
        SELECT r.name as RegionName, 
               s.name as SalesRepName, 
               a.name as AccountsName
        FROM sales_reps s
        	JOIN region r
        	ON s.region_id = r.id
        JOIN accounts a
        	ON s.id = a.sales_rep_id 
        WHERE s.name LIKE 'S%' and r.name = 'Midwest' 
        ORDER BY a.name
        ```
        
        - Provide a table that provides the **region** for each **sales_rep** along with their associated **accounts**. This time only for accounts where the sales rep has a **last** name starting with `K` and in the `Midwest` region. Your final table should include three columns: the region **name**, the sales rep **name**, and the account **name**. Sort the accounts alphabetically (A-Z) according to account name.
        
        ```sql
        SELECT r.name as RegionName, 
               s.name as SalesRepName, 
               a.name as AccountsName
        FROM sales_reps s
        	JOIN region r
        	ON s.region_id = r.id
        JOIN accounts a
        	ON s.id = a.sales_rep_id 
        WHERE s.name LIKE '%_K%' and r.name = 'Midwest' 
        ORDER BY a.name
        ```
        
        - Provide the **name** for each region for every **order**, as well as the account **name** and the **unit price** they paid (total_amt_usd/total) for the order. However, you should only provide the results if the **standard order quantity** exceeds `100`. Your final table should have 3 columns: **region name**, **account name**, and **unit price**. In order to avoid a division by zero error, adding .01 to the denominator here is helpful total_amt_usd/(total+0.01).
        
        ```sql
        SELECT r.name as RegionName, 
               a.name as AccountsName,
        			 (o.total_amt_usd/ (o.total + 0.01))  as unit_price
        FROM sales_reps s
        	JOIN region r
        	ON s.region_id = r.id
        JOIN accounts a
        	ON s.id = a.sales_rep_id 
        JOIN orders o
        	ON o.account_id = a.id
        WHERE o.standard_qty > 100
        ```
        
        - Provide the **name** for each region for every **order**, as well as the account **name** and the **unit price** they paid (total_amt_usd/total) for the order. However, you should only provide the results if the **standard order quantity** exceeds `100` and the **poster order quantity** exceeds `50`. Your final table should have 3 columns: **region name**, **account name**, and **unit price**. Sort for the smallest **unit price** first. In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).
        
        ```sql
        SELECT r.name as RegionName, 
               a.name as AccountsName,
        			 (o.total_amt_usd/ (o.total + 0.01))  as unit_price
        FROM sales_reps s
        	JOIN region r
        	ON s.region_id = r.id
        JOIN accounts a
        	ON s.id = a.sales_rep_id 
        JOIN orders o
        	ON o.account_id = a.id
        WHERE o.standard_qty > 100 and o.poster_qty > 50
        ORDER BY unit_price
        ```
        
        - Provide the **name** for each region for every **order**, as well as the account **name** and the **unit price** they paid (total_amt_usd/total) for the order. However, you should only provide the results if the **standard order quantity** exceeds `100` and the **poster order quantity** exceeds `50`. Your final table should have 3 columns: **region name**, **account name**, and **unit price**. Sort for the largest **unit price** first. In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).
        
        ```sql
        SELECT r.name as RegionName, 
               a.name as AccountsName,
        			 (o.total_amt_usd/ (o.total + 0.01))  as unit_price
        FROM sales_reps s
        	JOIN region r
        	ON s.region_id = r.id
        JOIN accounts a
        	ON s.id = a.sales_rep_id 
        JOIN orders o
        	ON o.account_id = a.id
        WHERE o.standard_qty > 100 and o.poster_qty > 50
        ORDER BY unit_price DESC
        ```
        
        - What are the different **channel**s used by **account id** `1001`? Your final table should have only 2 columns: **account name** and the different **channel**s. You can try **SELECT DISTINCT** to narrow down the results to only the unique values.
        
        ```sql
        SELECT DISTINCT a.name as AccountName, w.channel 
        FROM accounts a
        JOIN web_events w
        ON a.id = w.account_id
        and a.id = 1001
        ```
        
        - Find all the orders that occurred in `2015`. Your final table should have 4 columns: **occurred_at**, **account name**, **order total**, and **order total_amt_usd**.
            
            ```sql
            SELECT o.occurred_at, a.name, o.total, o.total_amt_usd
            FROM orders o
            JOIN accounts a
            ON a.id = o.account_id
            WHERE o.occurred_at BETWEEN '01-01-2015' and
            '01-01-2016'
            ORDER BY o.occurred_at DESC
            ```
- SQL Aggregations
    
    NULL -  When identifying **NULL**s in a **WHERE** clause, we write **IS NULL** or **IS NOT NULL.** We don't use `=`, because **NULL** isn't considered a value in SQL. Rather, it is a property of the data.**COUNT** does not consider rows that have **NULL** values. Therefore, this can be useful for quickly identifying which rows have missing data.
    
    COUNT()
    
    SUM()
    
    MIN(), MAX() - . Depending on the column type, **MIN**
     will return the lowest number, earliest date, or non-numerical value as early in the alphabet as possible. As you might suspect, **MAX** does the opposite—it returns the highest number, the latest date, or the non-numerical value closest alphabetically to “Z.”
    
    AVG() -  that is the sum of all of the values in the column divided by the number of values in a column. This aggregate function again ignores the **NULL** values in both the numerator and the denominator.
    
    GROUP  BY - The **GROUP BY** always goes between **WHERE** and **ORDER BY**.
    
    **DISTINCT -** is always used in **SELECT** statements, and it provides the unique rows for all columns written in the **SELECT** statement. Therefore, you only use **DISTINCT** once in any particular **SELECT** statement. It’s worth noting that using **DISTINCT** , particularly in aggregations, can slow your queries down quite a bit.
    
    ```sql
    SELECT SUM(poster_qty) as n_poster_paper_ordered
    FROM orders
    
    SELECT SUM(standard_qty) as n_standard_paper_ordered
    FROM orders
    
    SELECT SUM(total_amt_usd)
    FROM orders
    
    SELECT SUM(standard_amt_usd) as total_standard_usd, SUM(gloss_amt_usd) total_gloss_usd
    FROM orders
    
    SELECT SUM(standard_amt_usd) / SUM(standard_qty) AS standard_per_unit
    FROM orders
    
    SELECT min(occurred_at)
    FROM orders
    
    SELECT occurred_at
    FROM orders
    ORDER BY occurred_at 
    LIMIT 1
    
    SELECT max(occurred_at)
    FROM web_events
    
    SELECT occurred_at
    FROM web_events
    ORDER BY occurred_at DESC
    LIMIT 1
    
    SELECT AVG(standard_qty) standard_paper_avg, 
           AVG(gloss_qty) gloss_paper_avg, 
           AVG(poster_qty) poster_paper_avg,
           AVG(standard_amt_usd) standard_amt_avg,
           AVG(gloss_amt_usd) gloss_amt_avg ,
           AVG(poster_amt_usd) poster_amt_avg
    FROM orders
    LIMIT 5
    
    SELECT *
    FROM (SELECT total_amt_usd
          FROM orders
          ORDER BY total_amt_usd
          LIMIT 3457) AS Table1
    ORDER BY total_amt_usd DESC
    LIMIT 2;
    
    SELECT a.name, o.occurred_at
    FROM accounts a 
    JOIN orders o
    ON o.account_id = a.id
    ORDER BY occurred_at 
    LIMIT 1
    
    SELECT a.name, SUM(o.total_amt_usd) total_usd
    FROM accounts a 
    JOIN orders o
    ON o.account_id = a.id
    GROUP BY a.name
    ORDER BY a.name
    
    SELECT w.occurred_at, w.channel, a.name
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    ORDER BY w.occurred_at DESC
    LIMIT 1
    
    SELECT  channel, count(channel) channel_count
    FROM web_events 
    GROUP BY channel
    
    SELECT a.primary_poc, w.occurred_at
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    ORDER BY w.occurred_at
    LIMIT 1
    
    SELECT a.name, o.total_amt_usd
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    ORDER BY o.total_amt_usd
    
    SELECT r.name, count(r.id) num_sales_reps
    FROM region r
    JOIN sales_reps s
    ON r.id = s.region_id
    GROUP BY r.name
    ORDER BY num_sales_reps
    
    SELECT a.name, 
    	     avg(o.standard_qty) std_avg_amount, 
           avg(o.gloss_qty) gloss_avg_amount,
           avg(o.poster_qty) poster_avg_amount 
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.name
    
    SELECT a.name, 
    	     avg(o.standard_qty) std_avg_amount, 
           avg(o.gloss_qty) gloss_avg_amount,
           avg(o.poster_qty) poster_avg_amount 
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.name, o.account_id
    
    #refazer a c
    SELECT s.name, w.channel, COUNT(*) num_events
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    JOIN sales_reps s
    ON s.id = a.sales_rep_id
    GROUP BY s.name, w.channel
    ORDER BY num_events DESC;
    
    SELECT r.name, w.channel, COUNT(*) num_events
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    JOIN sales_reps s
    ON s.id = a.sales_rep_id
    JOIN region r
    ON r.id = s.region_id
    GROUP BY r.name, w.channel
    ORDER BY num_events DESC;
    
    SELECT a.id, a.sales_rep_id, s.region_id, r.name
    FROM accounts a
    JOIN sales_reps s
    ON a.sales_rep_id = s.id
    JOIN region r
    ON s.region_id = r.id
    
    SELECT a.id as "account id", r.id as "region id", 
    a.name as "account name", r.name as "region name"
    FROM accounts a
    JOIN sales_reps s
    ON s.id = a.sales_rep_id
    JOIN region r
    ON r.id = s.region_id;
    
    SELECT DISTINCT a.id as "account id", 
    	   a.sales_rep_id,
           s.id
    FROM accounts a
    JOIN sales_reps s
    ON s.id = a.sales_rep_id;
    
    SELECT s.id, s.name, COUNT(*) num_accounts
    FROM accounts a
    JOIN sales_reps s
    ON s.id = a.sales_rep_id
    GROUP BY s.id, s.name
    ORDER BY id;
    
    SELECT DISTINCT id, name
    FROM sales_reps;
    ```
	  
	**HAVING** is the “clean” way to filter a query that has been aggregated, but this is also commonly done using a [subquery](https://community.modeanalytics.com/sql/tutorial/sql-subqueries/). Essentially, any time you want to perform a **WHERE** on an element of your query that was created by an aggregate, you need to use **HAVING** instead.
    
    ```sql
    
    # How many of the sales reps have more than 5 accounts that they manage?
    
    SELECT s.id, s.name, count (*) n_accounts
    FROM accounts a
    JOIN sales_reps s
    ON a.sales_rep_id = s.id
    GROUP BY s.id, s.name
    HAVING count(*) > 5
    ORDER BY n_accounts;
    
    # How many accounts have more than 20 orders?
    
    SELECT o.account_id, count(*) n_orders
    FROM accounts a
    JOIN orders o
    ON o.account_id = a.id
    GROUP BY o.account_id
    HAVING count(*) > 20
    ORDER BY n_orders DESC;
    
    # Which account has the most orders?
    
    SELECT o.account_id, a.name, count(*) n_orders
    FROM accounts a
    JOIN orders o
    ON o.account_id = a.id
    GROUP BY o.account_id, a.name
    ORDER BY n_orders DESC
    LIMIT 1;
    
    #Which accounts spent more than 30,000 usd total across all orders?
    
    SELECT a.id, a.name, SUM(o.total_amt_usd) total_spent
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.id, a.name
    HAVING SUM(o.total_amt_usd) > 30000
    ORDER BY total_spent;
    
    Which accounts spent less than 1,000 usd total across all orders?
    
    SELECT a.id, a.name, SUM(o.total_amt_usd) total_spent
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.id, a.name
    HAVING SUM(o.total_amt_usd) < 1000
    ORDER BY total_spent;
    
    Which account has spent the most with us?
    
    SELECT a.id, a.name, SUM(o.total_amt_usd) total_spent
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.id, a.name
    ORDER BY total_spent DESC
    LIMIT 1;
    
    Which account has spent the least with us?
    
    SELECT a.id, a.name, SUM(o.total_amt_usd) total_spent
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.id, a.name
    ORDER BY total_spent DESC
    LIMIT 1;
    
    Which accounts used facebook as a channel to contact customers more than 6 times?
    
    SELECT a.id, 
    	   a.name, 
           w.channel, 
           COUNT(*) n_fb_as_channel
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    WHERE w.channel LIKE '%facebook%'
    GROUP BY a.id, a.name, w.channel
    HAVING count(*) > 6
    ORDER BY n_fb_as_channel DESC
    
    Which account used facebook most as a channel?
    
    SELECT a.id, 
    	   a.name, 
           w.channel, 
           COUNT(*) n_fb_as_channel
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    WHERE w.channel LIKE '%facebook%'
    GROUP BY a.id, a.name, w.channel
    ORDER BY n_fb_as_channel DESC
    LIMIT 1
    
    Which channel was most frequently used by most accounts?
    
    SELECT w.channel, 
           COUNT(*) n_channel
    FROM accounts a
    JOIN web_events w
    ON a.id = w.account_id
    GROUP BY  w.channel
    ORDER BY n_channel DESC
    LIMIT 1
    ```    
- DATE
    
    **DATE_PART** can be useful for pulling a specific portion of a date, but notice pulling `month` or day of the week (`dow`) means that you are no longer keeping the years in order. Rather you are grouping for certain components regardless of which year they belonged in.
    
    **DATE_TRUNC** allows you to truncate your date to a particular part of your date-time column. Common trunctions are `day`, `month`, and `year`. [https://mode.com/blog/date-trunc-sql-timestamp-function-count-on/](https://mode.com/blog/date-trunc-sql-timestamp-function-count-on/)
    
    1. Find the sales in terms of total dollars for all orders in each year, ordered from greatest to least. Do you notice any trends in the yearly sales totals?
    *  When we look at the yearly totals, you might notice that 2013 and 2017 have much smaller totals than all other years. If we look further at the monthly data, we see that for `2013` and `2017` there is only one month of sales for each of these years (12 for 2013 and 1 for 2017). Therefore, neither of these are evenly represented. Sales have been increasing year over year, with 2016 being the largest sales to date. At this rate, we might expect 2017 to have the largest sales.
    
    ```sql
    SELECT date_part('year', occurred_at) as year,
    	   date_part('month', occurred_at) as month,
    	   SUM(total_amt_usd) as total_spent
    FROM orders
    GROUP BY 1, 2
    ORDER BY 1
    
    SELECT date_part('year', occurred_at) as year,
    	   SUM(total_amt_usd) as total_spent
    FROM orders
    GROUP BY 1
    ORDER BY 2 
    ```

    2.Which **month** did Parch & Posey have the greatest sales in terms of total dollars? Are all months evenly represented by the dataset?
    
    The greatest sales amounts occur in December (12).
    
    ```sql
    SELECT date_part('month', occurred_at) as month,
    	   SUM(total_amt_usd) as total_spent
    FROM orders
    WHERE occurred_at BETWEEN '2014-01-01' AND '2017-01-01'
    GROUP BY 1
    ORDER BY 1 DESC
    ```
    
    3.Which **year** did Parch & Posey have the greatest sales in terms of total number of orders? Are all years evenly represented by the dataset?
    
    The greatest sales in terms of amount of orders were made in 2016. In lastest four years the amount has incresead.
    
    Again, 2016 by far has the most amount of orders, but again 2013 and 2017 are not evenly represented to the other years in the dataset.
    
    ```sql
    SELECT DATE_PART('year', occurred_at) ord_year,  COUNT(*) total_sales
    FROM orders
    GROUP BY 1
    ORDER BY 2 DESC;
    ```
    
    1. Which **month** did Parch & Posey have the greatest sales in terms of total number of orders? Are all months evenly represented by the dataset?
    
    December still has the most sales, but interestingly, November has the second most sales (but not the most dollar sales. To make a fair comparison from one month to another 2017 and 2013 data were removed.
    
    ```sql
    SELECT DATE_PART('month', occurred_at) ord_month, COUNT(*) total_sales
    FROM orders
    WHERE occurred_at BETWEEN '2014-01-01' AND '2017-01-01'
    GROUP BY 1
    ORDER BY 2 DESC;
    ```
    
    1. In which **month** of which **year** did `Walmart`spend the most on gloss paper in terms of dollars?
    
    May 2016 was when Walmart spent the most on gloss paper.
    
    ```sql
    SELECT date_part('month', o.occurred_at) as month,
    date_part('year', o.occurred_at) as year,
    	   SUM(o.gloss_amt_usd) as gloss_paper_usd
    FROM orders o
    JOIN accounts a
    ON a.id = o.account_id
    WHERE a.name = 'Walmart'
    GROUP BY 1,2
    ORDER BY 3 DESC
    ```
- **CASE - Expert Tip**
	- The CASE statement always goes in the SELECT clause.
	- CASE must include the following components: WHEN, THEN, and END. ELSE is an optional component to catch cases that didn’t meet any of the other previous CASE conditions.
	- You can make any conditional statement using any conditional operator (like [WHERE](https://mode.com/resources/sql-tutorial/sql-where)) between WHEN and THEN. This includes stringing together multiple conditional statements using AND and OR.
	- You can include multiple WHEN statements, as well as an ELSE statement again, to deal with any unaddressed conditions.
	
		```sql 
	SELECT account_id,
				 CASE WHEN standard_qty = 0 OR standard_qty IS NULL THEN 0
				 ELSE standard_amt_usd/standard_qty END AS unit_price
	FROM orders
	LIMIT 10;
	
	SELECT CASE WHEN total > 500 THEN 'Over 500'
				 ELSE '500 or under' END AS total_group,
			   COUNT(*) AS order_count
	FROM orders
	
	```

 1. Write a query to display for each order, the account ID, total amount of the order, and the level of the order - ‘Large’ or ’Small’ - depending on if the order is $3000 or more, or smaller than $3000.
 ```sql
	SELECT account_id, 
				 total_amt_usd, 
				 CASE WHEN total_amt_usd >= 3000 THEN 'Large' ELSE 'Small' END AS level_order
	FROM orders
	```
	
	2. Write a query to display the number of orders in each of three categories, based on the `total` number of items in each order. The three categories are: 'At Least 2000', 'Between 1000 and 2000' and 'Less than 1000'.
	
```sql
	SELECT
			 CASE 
				 WHEN total >= 2000 then 'At least 2000'
				 WHEN total >= 1000 and total < 2000 then 'Between 1000 and 2000'
		     ELSE 'Less than 1000'
			END AS order_cat,
			 count(*) order_count
	FROM orders
	GROUP BY 1
	```
	
We would like to understand 3 different levels of customers based on the amount associated with their purchases. The top level includes anyone with a Lifetime Value (total sales of all orders) `greater than 200,000` usd. The second level is between `200,000 and 100,000` usd. The lowest level is anyone `under 100,000` usd. Provide a table that includes the **level** associated with each **account**. You should provide the **account name**, the **total sales of all orders** for the customer, and the **level**. Order with the top spending customers listed first.

```sql
	SELECT
				a.name,
				SUM(o.total_amt_usd),
				CASE 
					WHEN SUM(o.total_amt_usd) > 200000 THEN 'top'
					WHEN SUM(o.total_amt_usd) > 100000 THEN 'middle'
					ELSE 'low'
					END AS level
	FROM accounts a
	JOIN orders o
	ON a.id = o.account_id
	GROUP BY a.name
	ORDER BY 2 DESC
	```
	
We would now like to perform a similar calculation to the first, but we want to obtain the total amount spent by customers only in `2016` and `2017`. Keep the same **level**s as in the previous question. Order with the top spending customers listed first.
		
```sql
	SELECT
				a.name,
				SUM(o.total_amt_usd) as total_usd,
				CASE 
					WHEN SUM(o.total_amt_usd) > 200000 THEN 'top'
					WHEN SUM(o.total_amt_usd) > 100000 THEN 'middle'
					ELSE 'low'
					END AS level
	FROM accounts a
	JOIN orders o
	ON a.id = o.account_id
	WHERE occurred_at > '2015-12-31'
	GROUP BY 1
	ORDER BY 2 DESC
	```
	
We would like to identify top performing **sales reps** ,which are sales reps associated with more than 200 orders. Create a table with the **sales rep name**, the total number of orders, and a column with `top` or `not`depending on if they have more than 200 orders. Place the top sales people first in your final table.

```sql
	SELECT s.name, count(*) as n_orders,
			CASE WHEN count(*) > 200 THEN 'top'
	        ELSE 'not' END as level_sales
	FROM orders o
	JOIN accounts a
	ON o.account_id = a.id 
	JOIN sales_reps s
	ON s.id = a.sales_rep_id
	GROUP BY s.name
	ORDER BY 2 DESC;
	```
	
The previous didn't account for the middle, nor the dollar amount associated with the sales. Management decides they want to see these characteristics represented as well. We would like to identify top performing **sales reps**, which are sales reps associated with more than `200` orders or more than `750000` in total sales. The `middle` group has any **rep** with more than 150 orders or `500000` in sales. Create a table with the **sales rep name**, the total number of orders, total sales across all orders, and a column with `top`, `middle`, or `low` depending on this criteria. Place the top sales people based on dollar amount of sales first in your final table. You might see a few upset sales people by this criteria!

```sql
	SELECT s.name, 
	       COUNT(*), 
	     SUM(o.total_amt_usd) total_spent, 
	     CASE 
			  WHEN COUNT(*) > 200 OR SUM(o.total_amt_usd) > 750000 THEN 'top'
	     WHEN COUNT(*) > 150 OR SUM(o.total_amt_usd) > 500000 THEN 'middle'
	     ELSE 'low' END AS sales_rep_level
	FROM orders o
	JOIN accounts a
	ON o.account_id = a.id 
	JOIN sales_reps s
	ON s.id = a.sales_rep_id
	GROUP BY s.name
	ORDER BY 3 DESC;
	```
- #### SQL Subqueries & Temporary Tables

     **subqueries** and **table expressions** are methods for being able to write a query that creates a table, and then write a query that interacts with this newly created table. Sometimes the question you are trying to answer doesn't have an answer when working directly with existing tables in database.
    
    ```sql
    SELECT channel, 
    	   AVG(n_events) as avg_event_count
    FROM
    ( SELECT date_trunc('day', occurred_at) as day,
    		channel,
            count(*) as n_events
    FROM web_events
    GROUP BY 1,2
    ORDER BY n_events DESC ) sub
    GROUP BY 1
    ORDER BY 2 DESC
    
    ```
    
    Quizzes
    
	1)Provide the **name** of the **sales_rep** in each **region** with the largest amount of **total_amt_usd** sales.
	
	```sql
	# t1 soma o total amt e agrupa em por nome e regiao
	# selecionar região o valor máximo
	# join com a query retornando rep name, region nam e a soma
	# no fim t2 + t3
	    SELECT t3.rep_name, t3.region_name, t3.total_amt
	    FROM(SELECT region_name, MAX(total_amt) total_amt
	         FROM(SELECT s.name rep_name, r.name region_name, SUM(o.total_amt_usd) total_amt
	                 FROM sales_reps s
	                 JOIN accounts a
	                 ON a.sales_rep_id = s.id
	                 JOIN orders o
	                 ON o.account_id = a.id
	                 JOIN region r
	                 ON r.id = s.region_id
	                 GROUP BY 1, 2) t1
	         GROUP BY 1) t2
	    JOIN (SELECT s.name rep_name, r.name region_name, SUM(o.total_amt_usd) total_amt
	         FROM sales_reps s
	         JOIN accounts a
	         ON a.sales_rep_id = s.id
	         JOIN orders o
	         ON o.account_id = a.id
	         JOIN region r
	         ON r.id = s.region_id
	         GROUP BY 1,2
	         ORDER BY 3 DESC) t3
	    ON t3.region_name = t2.region_name AND t3.total_amt = t2.total_amt;
	```
    
    2)For the region with the largest (sum) of sales **total_amt_usd**, how many **total**
     (count) orders were placed?

		seleciona a região com o valor maximo e usa o having pra selecionar somente ela pelo valor e assim contar a quantidade de pedidos
	```sql
	SELECT r.name, COUNT(o.total) total_orders
	FROM sales_reps s
	JOIN accounts a
	ON a.sales_rep_id = s.id
	JOIN orders o
	ON o.account_id = a.id
	JOIN region r
	ON r.id = s.region_id
	GROUP BY r.name
	HAVING SUM(o.total_amt_usd) =
			(SELECT MAX(total_amt)
			    FROM (SELECT r.name region_name, sum(o.total_amt_usd) total_amt
				      FROM sales_reps s
					  JOIN accounts a
					  ON a.sales_rep_id = s.id
					  JOIN orders o
					  ON o.account_id = a.id
					  JOIN region r
					  ON r.id = s.region_id
					  GROUP BY 1) sub
			)
```
	**3) How many accounts** had more **total** purchases than the account **name** which has bought the most **standard_qty** paper throughout their lifetime as a customer?
	
	```sql
	
	SELECT count(*) n_accounts
		FROM (SELECT o.account_id
		FROM orders o
		JOIN accounts a
		ON a.id = o.account_id
		GROUP BY 1
		HAVING SUM(o.total) >
					(SELECT total
					 FROM ( SELECT a.name acc_name , 
							SUM(o.standard_qty) total_std_qty, 
							SUM(o.total) total 
							FROM orders o
							JOIN accounts a
							ON a.id = o.account_id
							GROUP BY 1
							ORDER BY 2 DESC
							LIMIT 1) t1)
		) sub
	```

4) For the customer that spent the most (in total over their lifetime as a customer) **total_amt_usd**, how many **web_events** did they have for each channel?

	```sql
	
	#descobre o maior
	#pega o id
	
			SELECT a.name, w.channel, COUNT(*)
			FROM accounts a
			JOIN web_events w
			ON a.id = w.account_id AND a.id =  (SELECT id
			                     FROM (SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
			                           FROM orders o
			                           JOIN accounts a
			                           ON a.id = o.account_id
			                           GROUP BY a.id, a.name
			                           ORDER BY 3 DESC
			                           LIMIT 1) inner_table)
			GROUP BY 1, 2
			ORDER BY 3 DESC;
		```

 5) What is the lifetime average amount spent in terms of **total_amt_usd** for the top 10 total spending **accounts**?
```sql
SELECT AVG(total_amt) avg_amount_total_amt
FROM (SELECT a.id, SUM(o.total_amt_usd) total_amt 
	FROM accounts a
	JOIN orders o
	ON a.id = o.account_id
	GROUP BY 1
	ORDER BY 2 DESC 
	LIMIT 10) t1

```

6) What is the lifetime average amount spent in terms of **total_amt_usd**, including only the companies that spent more per order, on average, than the average of all orders.

```sql
# pega a média geral de todas as contas
SELECT AVG(total_amt_usd) general_avg
FROM orders 

# agrupa as contas, e pega a média das contas


SELECT name, avg(total_amt_usd)
FROM orders 
GROUP BY 1
HAVING avg(total_amt_usd) > (SELECT AVG(total_amt_usd) general_avg
FROM orders) sub

----

SELECT AVG(avg_amt)
FROM (
	SELECT account_id, 
	       avg(total_amt_usd) avg_amt
	FROM orders 
	GROUP BY 1
	HAVING avg(total_amt_usd) > (SELECT AVG(total_amt_usd) general_avg
	                             FROM orders) 
) sub


```

#### WITH 

For long subqueries:

The **WITH** statement is often called a **Common Table Expression** or **CTE**. Though these expressions serve the exact same purpose as subqueries, they are more common in practice, as they tend to be cleaner for a future reader to follow the logic.

1) Provide the **name** of the **sales_rep** in each **region** with the largest amount of **total_amt_usd** sales.
```sql
my easy sol

WITH t1 AS (
SELECT  s.name rep_name, r.name region_name, SUM(total_amt_usd) total_amt
FROM orders o
JOIN accounts a
ON o.account_id = a.id
JOIN sales_reps s
ON s.id = a.sales_rep_id
JOIN region r
ON r.id = s.region_id
GROUP BY 1, 2
ORDER BY total_amt DESC
),
t2 AS (SELECT region_name, MAX(total_amt) max_amt
FROM t1
GROUP BY 1)

SELECT t1.rep_name, t1.region_name, t1.total_amt
FROM t1
JOIN t2
ON t1.region_name = t2.region_name AND 
t1.total_amt = t2.max_amt


```
2) For the region with the largest sales **total_amt_usd**, how many **total** orders were placed?
```sql
WITH t1 AS (SELECT r.name region_name, SUM(total_amt_usd)
			FROM orders o
				JOIN accounts a
				ON o.account_id = a.id
				JOIN sales_reps s
				ON s.id = a.sales_rep_id
				JOIN region r
				ON r.id = s.region_id
			GROUP BY 1
			ORDER BY 2 DESC
			LIMIT 1
), 
t2 AS ( SELECT r.name region_name, o.account_id, count(*) n_accounts
		FROM orders o
			JOIN accounts a
			ON o.account_id = a.id
			JOIN sales_reps s
			ON s.id = a.sales_rep_id
			JOIN region r
			ON r.id = s.region_id
		GROUP BY 1,2
)

SELECT t2.region_name, sum(n_accounts) total_orders
FROM t2
JOIN t1
ON t1.region_name = t2.region_name 
GROUP BY 1

```

3) For the account that purchased the most (in total over their lifetime as a customer) **standard_qty** paper, **how many accounts** still had more in **total** purchases?
   ```sql
   
   WITH t1 AS (
	  SELECT a.name account_name, 
	  SUM(o.standard_qty) total_std, SUM(o.total) total
	  FROM accounts a
	  JOIN orders o
	  ON o.account_id = a.id
	  GROUP BY 1
	  ORDER BY 2 DESC
	  LIMIT 1), 
t2 AS (
  SELECT a.name
  FROM orders o
  JOIN accounts a
  ON a.id = o.account_id
  GROUP BY 1
  HAVING SUM(o.total) > (SELECT total FROM t1))
SELECT COUNT(*)
FROM t2;
```
 4) For the customer that spent the most (in total over their lifetime as a customer) **total_amt_usd**, how many **web_events** did they have for each channel?
```sql

  WITH t1 AS (
  SELECT  a.id, a.name, SUM(total_amt_usd) total_amt
  FROM orders o
  JOIN accounts a
  ON a.id = o.account_id
  GROUP BY 1,2
  ORDER BY 3 DESC
  LIMIT 1
  )
  
  SELECT a.name, w.channel, count(*) 
  FROM accounts a
  JOIN web_events w
  ON w.account_id = a.id AND a.id = (SELECT id FROM t1)
  GROUP BY 1, 2 
  ORDER BY 3 DESC
```
 5) What is the lifetime average amount spent in terms of **total_amt_usd** for the top 10 total spending **accounts**?
 ```sql
WITH t1 AS (
   SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
   FROM orders o
   JOIN accounts a
   ON a.id = o.account_id
   GROUP BY a.id, a.name
   ORDER BY 3 DESC
   LIMIT 10)
SELECT AVG(tot_spent)
FROM t1;
```
 6)What is the lifetime average amount spent in terms of **total_amt_usd**, including only the companies that spent more per order, on average, than the average of all orders.
 ```sql
 WITH t1 AS (
   SELECT AVG(o.total_amt_usd) avg_all
   FROM orders o
   JOIN accounts a
   ON a.id = o.account_id),
t2 AS (
   SELECT o.account_id, AVG(o.total_amt_usd) avg_amt
   FROM orders o
   GROUP BY 1
   HAVING AVG(o.total_amt_usd) > (SELECT * FROM t1))
SELECT AVG(avg_amt)
FROM t2;
```

#### DATA CLEANING

1.  Clean and re-structure messy data.
2.  Convert columns to different data types.
3.  Tricks for manipulating **NULL**s.

##### LEFT, RIGHT, LENGTH

**LEFT** pulls a specified number of characters for each row in a specified column starting at the beginning (or from the left). As you saw here, you can pull the first three digits of a phone number using **LEFT(phone_number, 3)**.  
  
**RIGHT** pulls a specified number of characters for each row in a specified column starting at the end (or from the right). As you saw here, you can pull the last eight digits of a phone number using **RIGHT(phone_number, 8)**.  
  
**LENGTH** provides the number of characters for each row of a specified column. Here, you saw that we could use this to get the length of each phone number as **LENGTH(phone_number)**.

1) In the **accounts** table, there is a column holding the **website** for each company. The last three digits specify what type of web address they are using. A list of extensions (and pricing) is provided [here](https://iwantmyname.com/domains/domain-name-registration-list-of-extensions). Pull these extensions and provide how many of each website type exist in the **accounts** table.

```sql
SELECT RIGHT(website,3) extension_type, count(*)
FROM accounts
GROUP BY 1
```
  2) There is much debate about how much the name [(or even the first letter of a company name)](https://www.quora.com/Does-a-companys-name-matter) matters. Use the **accounts** table to pull the first letter of each company name to see the distribution of company names that begin with each letter (or number).
  ```sql
  SELECT LEFT(name,1) first_letter, count(*) n_companies
	FROM accounts
	GROUP BY 1
	ORDER BY 2 DESC
  
```
  3)Use the **accounts** table and a **CASE** statement to create two groups: one group of company names that start with a number and a second group of those company names that start with a letter. What proportion of company names start with a letter? 
  ```sql

	with t1 as (SELECT name, 
		   CASE WHEN LEFT(UPPER(name),1) IN           ('0','1','2','3','4','5','6','7','8','9') 
				   THEN 1 ELSE 0 END AS num,
			 CASE WHEN LEFT(UPPER(name),1) IN ('0','1','2','3','4','5','6','7','8','9') THEN 0 ELSE 1 END AS letter
	FROM accounts
	)
SELECT sum(num) n_numbers, sum(letter) n_letters
FROM t1
```

 4) 1Consider vowels as `a`, `e`, `i`, `o`, and `u`. What proportion of company names start with a vowel, and what percent start with anything else?
```sql

SELECT SUM(vowels) vowels, SUM(other) other
	FROM (SELECT name, 
		         CASE WHEN LEFT(lower(name),1) IN                         ('a','e','i','o','u') THEN 1 ELSE 0 END AS vowels, 
                 CASE WHEN LEFT(lower(name),1) IN                       ('a','e','i','o','u') THEN 0 ELSE 1 END AS other
    FROM accounts) t1;
```

**POSITION** takes a character and a column, and provides the index where that character is for each row. The index of the first position is 1 in SQL. If you come from another programming language, many begin indexing at 0. Here, you saw that you can pull the index of a comma as **POSITION(',' IN city_state)**. // da a posição da virgula
**STRPOS** provides the same result as **POSITION**, but the syntax for achieving those results is a bit different as shown here: **STRPOS(city_state, ',')**.
Note, both **POSITION** and **STRPOS** are case sensitive, so looking for **A** is different than looking for **a**.  
Therefore, if you want to pull an index regardless of the case of a letter, you might want to use **LOWER** or **UPPER** to make all of the characters lower or uppercase.

1) Use the `accounts` table to create **first** and **last** name columns that hold the first and last names for the `primary_poc`.
 ```sql
with t1 as (SELECT primary_poc, LEFT(primary_poc, POSITION(' ' in primary_poc)) as first     
FROM accounts)

SELECT primary_poc, first, RIGHT(primary_poc, LENGTH(primary_poc) - LENGTH(first)) as last
FROM t1
 
```
2) Now see if you can do the same thing for every rep `name` in the `sales_reps` table. Again provide **first** and **last** name columns.
 ```sql
SELECT LEFT(name, STRPOS(name, ' ') -1 ) first_name, 
       RIGHT(name, LENGTH(name) - STRPOS(name, ' ')) last_name
FROM sales_reps;
```

**CONCAT(first_name, ' ', last_name)** or with piping as **first_name || ' ' || last_name**.

1) Each company in the `accounts` table wants to create an email address for each `primary_poc`. The email address should be the first name of the **primary_poc** `.` last name **primary_poc** `@` company name `.com`.
```sql

with  t1 as (
  SELECT name,
  LEFT(primary_poc, STRPOS(primary_poc, ' ') - 1 ) as first_name, 
  RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) as last_name
FROM accounts
)
             
SELECT first_name, 
       last_name, 
       CONCAT(first_name, '.', last_name, '@', name, '.com') as email 
FROM t1

```
3) You may have noticed that in the previous solution some of the company names include spaces, which will certainly not work in an email address. See if you can create an email address that will work by removing all of the spaces in the account `name`, but otherwise your solution should be just as in question `1`. Some helpful documentation is [here](https://www.postgresql.org/docs/8.1/static/functions-string.html).
```sql
with  t1 as (
  SELECT name,
  LEFT(primary_poc, STRPOS(primary_poc, ' ') - 1 ) as first_name, 
  RIGHT(primary_poc, LENGTH(primary_poc) -    STRPOS(primary_poc, ' ')) as last_name
FROM accounts
)
             
SELECT name, first_name, 
       last_name, 
       CONCAT(first_name, '.', last_name, '@', REPLACE(name,' ',''), '.com') as email 
FROM t1 

```
3)  We would also like to create an initial password, which they will change after their first log in. The first password will be the first letter of the `primary_poc`'s first name (lowercase), then the last letter of their first name (lowercase), the first letter of their last name (lowercase), the last letter of their last name (lowercase), the number of letters in their first name, the number of letters in their last name, and then the name of the company they are working with, all capitalized with no spaces.
  ```sql
  WITH t1 AS (
 SELECT LEFT(primary_poc,   STRPOS(primary_poc, ' ') -1 ) first_name,  RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name, name
 FROM accounts)
 
SELECT first_name, last_name, CONCAT(first_name, '.', last_name, '@', name, '.com'), LEFT(LOWER(first_name), 1) || RIGHT(LOWER(first_name), 1) || LEFT(LOWER(last_name), 1) || RIGHT(LOWER(last_name), 1) || LENGTH(first_name) || LENGTH(last_name) || REPLACE(UPPER(name), ' ', '')
FROM t1;
```

* TO DATE:  **DATE_PART('month', TO_DATE(month, 'month'))** here changed a month name into the number associated with that particular month.
* CAST: Then you can change a string to a date using **CAST**. **CAST** is actually useful to change lots of column types. Commonly you might be doing as you saw here, where you change a `string` to a `date` using **CAST(date_column AS DATE)**.
* Casting with :: : **CAST(date_column AS DATE)**, you can use **date_column::DATE**
* **LEFT**, **RIGHT**, and **TRIM** are all used to select only certain elements of strings, but using them to select elements of a number or date will treat them as strings for the purpose of the function.
* https://www.postgresql.org/docs/9.1/functions-string.html

 ```sql
 SELECT SUBSTR(date,1,10) as date,
(SUBSTR(date, 7,4) || '-' || SUBSTR(date, 1,2) || '-' || SUBSTR(date, 4,2))::DATE new_date                                                     FROM sf_crime_data
```

 **COALESCE** returns the first non-NULL value passed for each row.
 
 ```sql

SELECT COALESCE(o.id, a.id) filled_id, a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, o.*
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;



SELECT COALESCE(o.id, a.id) filled_id, a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, COALESCE(o.account_id, a.id) account_id, o.occurred_at, o.standard_qty, o.gloss_qty, o.poster_qty, o.total, o.standard_amt_usd, o.gloss_amt_usd, o.poster_amt_usd, o.total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;



SELECT COALESCE(o.id, a.id) filled_id, a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, COALESCE(o.account_id, a.id) account_id, o.occurred_at, COALESCE(o.standard_qty, 0) standard_qty, COALESCE(o.gloss_qty,0) gloss_qty, COALESCE(o.poster_qty,0) poster_qty, COALESCE(o.total,0) total, COALESCE(o.standard_amt_usd,0) standard_amt_usd, COALESCE(o.gloss_amt_usd,0) gloss_amt_usd, COALESCE(o.poster_amt_usd,0) poster_amt_usd, COALESCE(o.total_amt_usd,0) total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;


SELECT COUNT(*)
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id;


SELECT COALESCE(o.id, a.id) filled_id, a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, COALESCE(o.account_id, a.id) account_id, o.occurred_at, COALESCE(o.standard_qty, 0) standard_qty, COALESCE(o.gloss_qty,0) gloss_qty, COALESCE(o.poster_qty,0) poster_qty, COALESCE(o.total,0) total, COALESCE(o.standard_amt_usd,0) standard_amt_usd, COALESCE(o.gloss_amt_usd,0) gloss_amt_usd, COALESCE(o.poster_amt_usd,0) poster_amt_usd, COALESCE(o.total_amt_usd,0) total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id;

```

*REFS*
https://www.w3schools.com/sql/sql_isnull.asp
https://mode.com/sql-tutorial/sql-string-functions-for-cleaning/

### SQL Window functions

Introducing Window Functions

https://www.postgresql.org/docs/9.1/tutorial-window.html