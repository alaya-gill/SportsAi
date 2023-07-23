# %%
"""
# Scraping Transfermarkt
"""

# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# %%
"""
## Function that scrapes a list of Team Webpage Links
"""

# %%
#top_league(n) returns a list of links to the webpages of every club within the top n European leagues.
#i.e. Passing 1 as an argument will return links to the no.1 league in Europe- England. Passing 2 as an argument will return links of clubs in the 2 best leagues.
def top_league(n):

    headers = {'User-Agent': 'Mozilla/5.0'}

    page = "https://www.transfermarkt.co.uk/wettbewerbe/europa"
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    links = pageSoup.find_all("tr")

    site = 'https://www.transfermarkt.co.uk'
    s20_string = "/plus/?saison_id=2023"

    top_leagues = []
    for a in list(range(2,((n*2)+1),2)):
        top_leagues.append((site+(str(links[a]).split('href="',5)[2].split('"')[0])+s20_string))

    teams = []

    for a in top_leagues:
        page = a
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        tds = pageSoup.find_all("td",{"class":"hauptlink no-border-links"})
        links2 = []
        for i in tds:
            links2.append(i.a)
        site = 'https://www.transfermarkt.co.uk'
        s21_string = "/plus/?saison_id=2024"

        if a=="https://www.transfermarkt.co.uk/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023" or a=="https://www.transfermarkt.co.uk/liga-portugal-bwin/startseite/wettbewerb/PO1/plus/?saison_id=2023" or a=="'https://www.transfermarkt.co.uk/eredivisie/startseite/wettbewerb/NL1/plus/?saison_id=2023'":
            for link in links2:
                teams.append(site+link['href'])
        elif a== 'https://www.transfermarkt.co.uk/premier-liga/startseite/wettbewerb/GB1/plus/?saison_id=2023':
            for link in links2:
                teams.append(site+link['href'])
        else:
            for link in links2:
                teams.append(site+link['href'])
    return teams

# %%
"""
## Function that scrapes a list of Individual Player Webpage Links
"""

# %%
#top_league_player(n) returns a list of links to the individual profile webpage for every player participating in Europe's top n number of leagues.
def top_league_player(n):

    headers = {'User-Agent': 'Mozilla/5.0'}

    page = "https://www.transfermarkt.co.uk/wettbewerbe/europa"
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    links = pageSoup.find_all("tr")

    site = 'https://www.transfermarkt.co.uk'
    s20_string = "/plus/?saison_id=2023"

    top_leagues = []
    for a in list(range(2,((n*2)+1),2)):
        top_leagues.append((site+(str(links[a]).split('href="',5)[2].split('"')[0])+s20_string))

    teams = []

    for a in top_leagues:
        page = a
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        
        tds = pageSoup.find_all("td",{"class":"hauptlink no-border-links"})
        links2 = []
        for i in tds:
            links2.append(i.a)
        
        site = 'https://www.transfermarkt.co.uk'
        s21_string = "/plus/?saison_id=2024"

        if a=="https://www.transfermarkt.co.uk/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023" or a=="https://www.transfermarkt.co.uk/liga-portugal-bwin/startseite/wettbewerb/PO1/plus/?saison_id=2023" or a=="'https://www.transfermarkt.co.uk/eredivisie/startseite/wettbewerb/NL1/plus/?saison_id=2023'":
            for link in links2:
                teams.append(site+link['href'])
        elif a=='https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2023':
            for link in links2:
                teams.append(site+link['href'])
        else:
            for link in links2:
                teams.append(site+link['href'])
    player_links = []
    for a in teams[0:1]:
        page = a
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        site = 'https://www.transfermarkt.co.uk'

        tds = pageSoup.find_all("td",{"class":"hauptlink"})
        for link in tds:
            try:
                player_links.append(site+link.a['href'])
            except:
                continue

    return player_links
    

# %%
"""
## Scraping Player Contract Length Data
"""

# %%
"""
Contract dataframe: contract scrape from individual player pages. #Warning: IT MAY TAKE HOURS TO RUN but it WORKS!!!
"""

# %%
#iterating through every link in the list provided to it and then returns a dataframe of player data from the given webpages.
#top_league_player(5) returns a list of links to the individual profile webpage for every player participating in Europe's top 5 leagues.

site = 'https://www.transfermarkt.co.uk'
PlayerList = []
ContractList = []

headers = {'User-Agent': 'Mozilla/5.0'}

for a in top_league_player(1)[:10]:

    page = a
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    Player = pageSoup.find_all("meta",{"property":"og:title"})
    Contract = pageSoup.find_all("span",{"class":"dataValue"})

    PlayerList.append(str(Player).split('content="')[1].split(" - ")[0])
    try:
        ContractList.append((int(str(Contract[-1]).split(", ")[1].split("</span>")[0])-2021))
    except IndexError:
        ContractList.append("fail")

contract_df = pd.DataFrame({"Player":PlayerList,"Contract Years Left":ContractList})

# %%
#Observing what our contract df looks like
contract_df

# %%
"""
## Function that Scrapes and builds a dataframe of all Players' data
"""

# %%
#This function works when providing links of individual club pages.
#It iterates through every link in the list provided to it and then returns a dataframe of player data from the given webpages.
def build_df(links):

    PlayersList = []
    AgeList=[]
    NationList=[]
    ValuesList = []
    PositionsList=[]
    ClubList = []

    for a in links[0:1]:

        headers = {'User-Agent': 'Mozilla/5.0'}
        page = a
        if "startseite" in a:
            page = a.replace("startseite", "kader") + "/plus/1"
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        tbody = pageSoup.find_all('tbody')[1]
        rows = tbody.find_all('tr' , {"class": "odd"}) + tbody.find_all('tr' , {"class": "even"})
        Players = []
        AgeList = []
        NationList = []
        ValuesList = []
        Positions = []
        ClubList = []
        for row in rows:
            try:
                Players.append(row.find("img", {"class": "bilderrahmen-fixed lazy lazy"}))
                data = row.find_all('td', {"class": "zentriert"})[1:]
                value = row.find('td', {"class": "rechts hauptlink"})
                AgeList.append(data[0].text)
                NationList.append(data[1].img['alt'])
                ValuesList.append(value.text)
                Positions.append(row.find("td", {"class": ["zentriert rueckennummer bg_Torwart","zentriert rueckennummer bg_Abwehr","zentriert rueckennummer bg_Mittelfeld","zentriert rueckennummer bg_Sturm"]}))
                ClubList.append(pageSoup.find("h2",{"class":"content-box-headline"}).text)
            except: 
                continue

        for i in range(0,len(Players)):
            PlayersList.append(str(Players[i]).split('" class',1)[0].split('<img alt="',1)[1])

        for i in range(0,len(Positions)):
            PositionsList.append(str(Positions[i]).split('title="',1)[1].split('"><div')[0])


            

    #Initial uncleaned dataframe initiated
    df= pd.DataFrame({"Players":PlayersList,"Club":ClubList,"Position":PositionsList, "Date of birth / Age":AgeList, "Nationality":NationList,"Values":ValuesList,})

    #Missing Transfer Values were stored as '\xa0'. The line below replaces them as None values
    df.loc[(df.Values == '\xa0'),'Values']= None

    #Dataframe without missing transfer values
    df_droppednull = df.dropna()

    #Converting the Transfer Values data to float            
    transfer_values = [a[1:len(a)-2] for a in df_droppednull['Values']]

    cleaned_values=[]
    for a in list(range(len(transfer_values))):
        if transfer_values[a].endswith('m'):
            cleaned_values.append(float(transfer_values[a][:len(transfer_values[a])-1])*1000000)
        elif transfer_values[a].endswith('Th.'):
            cleaned_values.append(float(transfer_values[a][:len(transfer_values[a])-3])*1000)
        else:
            cleaned_values.append(float(a))

    #Constructing the Final Dataframe   
    final_df= pd.DataFrame({"Player":df_droppednull['Players'],"Club":df_droppednull['Club'],
                    "Date of birth / Age":df_droppednull['Date of birth / Age'],"Position":df_droppednull['Position'],
                    "Nation":df_droppednull['Nationality'],"Value":cleaned_values})

    #df ranked by transfer value
    ranked_df = final_df.sort_values('Value',ascending=False)
    
    return ranked_df

# %%
"""
Building the dataframe of players from every Club Page
"""

# %%
#Building a dataframe by scraping information of the 98 teams from Europe's top 5 leagues - i.e. England, Spain, Italy, Germany & France
first_df = build_df(top_league(5))

# %%
"""
### Seeing what our scraped dataset looks like
"""

# %%
#Seeing what our dataframe looks like
first_df

# %%
"""
## Merging the contract length data onto the above dataframe
"""

# %%
#merging our dataframe with contract information
merged_df = pd.merge(first_df, contract_df, on='Player')

# %%
"""
## Adding a League Column
"""

# %%
#Grouping Clubs by individual Leagues and making a separate "League" column.

England = ['Manchester City','Liverpool FC','Crystal Palace','Chelsea FC','Fulham FC','Brighton &amp; Hove Albion','West Bromwich Albion','Newcastle United','Leeds United','Aston Villa','Sheffield United','Manchester United','West Ham United','Leicester City','Tottenham Hotspur','Burnley FC','Southampton FC','Arsenal FC','Wolverhampton Wanderers','Everton FC']
Spain = ['SD Eibar','CA Osasuna','Athletic Bilbao','Real Betis Balompié','Valencia CF','Celta de Vigo','Levante UD','Cádiz CF','FC Barcelona','Villarreal CF','SD Huesca','Sevilla FC','Getafe CF','Deportivo Alavés','Real Valladolid CF','Granada CF','Real Madrid','Elche CF','Atlético de Madrid','Real Sociedad']
Italy = ['US Sassuolo','AC Milan','Juventus FC','Udinese Calcio','Genoa CFC','Cagliari Calcio','Inter Milan','FC Crotone','Hellas Verona','Benevento Calcio','Parma Calcio 1913','SSC Napoli','AS Roma','Bologna FC 1909','Torino FC','UC Sampdoria','SS Lazio','ACF Fiorentina','Atalanta BC','Spezia Calcio']
Germany = ['Bayern Munich','Hertha BSC','Borussia Dortmund','VfB Stuttgart','1.FSV Mainz 05','Arminia Bielefeld','Bayer 04 Leverkusen','SV Werder Bremen','1. FC Köln','FC Augsburg','VfL Wolfsburg','TSG 1899 Hoffenheim','RB Leipzig','SC Freiburg','1.FC Union Berlin','FC Schalke 04','Borussia Mönchengladbach','Eintracht Frankfurt']
France = ['AS Monaco','Montpellier HSC','FC Girondins Bordeaux','Paris Saint-Germain','Olympique Marseille','OGC Nice','Nîmes Olympique','FC Nantes','Stade Reims','FC Lorient','Stade Brestois 29','LOSC Lille','Stade Rennais FC','Dijon FCO','RC Strasbourg Alsace','RC Lens','AS Saint-Étienne','FC Metz','Olympique Lyon','SCO Angers']

LeagueList = []
for a in merged_df['Club']:
    if a in England:
        LeagueList.append('Premier League')
    elif a in Spain:
        LeagueList.append('La Liga')
    elif a in Italy:
        LeagueList.append('Serie A')
    elif a in Germany:
        LeagueList.append('Bundesliga')
    elif a in France:
        LeagueList.append('Ligue 1')
    else:
        LeagueList.append("UNKNOWN")
        
merged_df['League'] = LeagueList

# %%
#looking at our dataframe with contract information appended.
merged_df

# %%
#There are some duplicate rows
merged_df.drop_duplicates(keep="first",inplace=True)

# %%
merged_df

# %%
"""
## Exporting the Dataset
"""

# %%
# Install gitpath below if not already available on your environment.
#! pip install git+https://github.com/maxnoe/python-gitpath
#Getting the file path for the data file.
file_path = './transfermarkt_scrape_latest.xlsx'

# %%
#Exporting data to .csv format in the repo's data folder.
merged_df.to_excel(file_path,index=False)