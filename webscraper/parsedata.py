from bs4 import BeautifulSoup
import requests

###  Outline:
# url = 'https://www.rottentomatoes.com/m/the_invisible_man_2020#contentReviews'
# response = get(url)
# content = BeautifulSoup(response.content, "html.parser")

url = 'https://www.rottentomatoes.com/m/mulan_2020'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

movieTitle = content.findAll('h1', attrs={"class" : "mop-ratings-wrap__title mop-ratings-wrap__title--top"})
movieTitle = str(movieTitle)
print("\nOriginal String:"+movieTitle)
first = movieTitle.find('>')
movieTitle = movieTitle[first+1:len(movieTitle)]
last = movieTitle.find('<')
movieTitle = movieTitle[0:last]
print("\nTitle: " + movieTitle+"\n")


movieRating = content.findAll('div', attrs={"class" : "meta-value"})

print("INFO:")
print(movieRating)

'''
TODO: to extract:

    MPAA Film Rating: 
        G(General Audiences), PG(Parental Guidance Suggested) PG-13(Parents Strongly Cautioned),
        R(Restricted), NC-17(Adults Only)  

    Directed By:
        <names> (Can it be multiple?)

    Written By:
        <names> (Can be anywhere from 1 - n people)

    In Theaters:
        <Jan 10, 2020>  <release type> (wide, all I could find)
    
    Studio:
        <studio name>

    Actors: ( All possible )
        <actor names>

'''




# html:

# <ul class="content-meta info">
                
#                     <li class="meta-row clearfix">
#                         <div class="meta-label subtle">Rating: </div>
#                         <div class="meta-value">NR</div>
#                     </li>
                
                
#                     <li class="meta-row clearfix">
#                         <div class="meta-label subtle">Genre: </div>
#                         <div class="meta-value">
                            
#                                 <a href="/browse/opening/?genres=1">Action &amp; Adventure</a>, 
                             
#                                 <a href="/browse/opening/?genres=9">Drama</a>, 
                             
#                                 <a href="/browse/opening/?genres=11">Kids &amp; Family</a>
                             
#                         </div>
#                     </li>   
#                     <li class="meta-row clearfix">
#                         <div class="meta-label subtle">Directed By: </div>
#                         <div class="meta-value">
#                                 <a href="/celebrity/niki_caro">Niki Caro</a>  
#                         </div>
#                     </li>   
#                     <li class="meta-row clearfix">
#                         <div class="meta-label subtle">Written By: </div>
#                         <div class="meta-value">
#                                 <a href="/celebrity/rick_jaffa">Rick Jaffa</a>, 
#                                 <a href="/celebrity/amanda_silver">Amanda Silver</a>, 
#                                 <a href="/celebrity/elizabeth_martin">Elizabeth Martin</a>, 
#                                 <a href="/celebrity/lauren_hynek">Lauren Hynek</a>            
#                         </div>
#                     </li>
#                     <li class="meta-row clearfix">
#                         <div class="meta-label subtle">In Theaters: </div>
#                         <div class="meta-value">
#                             <time datetime="2020-03-26T17:00:00-07:00">Mar 27, 2020</time>
#                             <span style="text-transform:capitalize">&nbsp;wide</span>
#                         </div>
#                     </li>
#                     <li class="meta-row clearfix">
#                     <div class="meta-label subtle">Studio: </div>
#                     <div class="meta-value">
#                         Walt Disney Pictures
#                     </div>
#             </li></ul>