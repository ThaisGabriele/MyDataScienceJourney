## Learning SQL
 
* Chapter 3 - 
 
 [Query mechanics]
 
 * In MySQL, each time a query is sent to the server, the server checks the following statements:
 
   * Do you have permission to execute the statement?
   * Do you have permission to access the desired data?
   * Is your statement syntax correct?
   
  If everything ok -> query optimizer (whose job it is to determine the most efficient way to execute your query)
  Once the server has finished execute your query -> result set
  
   [Query clauses]
  
   **Select statement**
   
   You will usually include at least two or three of the *six* available clauses.

    - select
    - from
    - where: **filters out unwanted data** 
    - group by: used to **group rows together** by commom column values
    - having: filters out **unwanted groups**
    - order by: sorts the row of the **final result** set by one or more columns
   
   
