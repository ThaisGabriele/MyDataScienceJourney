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
   
   In select clause you can include things such as:
   
    -  Literals, such as numbers or strings. Ex SELECT 'COMMON' language_usage 
    -  Expressions. Ex: SELECT language_id * 3.1415927 lang_pi_value
    -  Built-in function calls, such as ROUND(transaction.amount, 2) 
    -  User-defined function calls. Ex: SELECT upper(name) language_name
    
    *you can use AS before the alias name*
    
     Removing Duplicates
     
     * DISTINCT after SELECT.
     
     The from Clause
     
     *"The from clause defines the tables used by a query, along with the means of linking thetables together."
     
     - Derived (subquery-generated) tables
     - Temporary tables
     - Views
     - Table Links     
     
    
   
   
