# How does Broadway show performance affect its financial performance?

**Problem Statement**

According to The Broadway League, Broadway has a total attendance of 14,768,254, and grosses of US$1,829,312,140 in the 2018–2019 season; furthermore, the attendance and gross has been increasing since the year of 2016. The financial statistics exhibit the stable operations and profitability of Broadway and indicate a sustainably growing market of Broadway show performances. 

Since Broadway provides public online access to its weekly gross information, this project aims to utilize the essential amount of Broadway weekly transaction data and to identify the critical factors that affect Broadway’s financial performance through multivariate data analysis methods. Based on the data scraped from webpages, I conduct an exploratory analysis, Principle Component Analysis, Factor Analysis, and K-Means Clustering to dig into the Broadway show performances.

**Description of the Data**

I scrapped information about Broadway shows from the web pages of www.playbill.com, a monthly U.S. magazine for theatergoers, through web scraping techniques with Python. The consequential broadway2019.csv dataset includes the financial information of any Broadway show that was on show in the year 2019.

The broadway2019.csv dataset contains 17 variables and 1,705 observations. It provides the grosses information of 82 shows run over 52 weeks as a total of 12,424 performances in the year 2019. The definition of each variable is listed below:

*   ID (Identification number of each observation)
*   Show Name
*   Week (The date each grosses week ending on)
*   Theatre (The theater where a show was on show)
*   Gross ($)
*   Gross Difference (From week prior)
*   Gross Potential (%)
*   Average Ticket Price
*   Top Ticket Price
*   Seats Sold
*   Seats in the Theatre 
*   Number of Performances
*   Number of Previews
*   Capacity (%)
*   Capacity Difference (From week prior)
*   Month
*   Season
