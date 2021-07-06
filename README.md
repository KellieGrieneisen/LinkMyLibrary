
<h1>Link My Library</h1>
<p>Keeping track of your books can be tough. And if you're anything like me, keeping track of your 'to be read' list is even tougher!</p>
<p>Link My Library is a safe space to keep track of the books on your shelves, and your ever expanding 'to be read'. 
As well as some bonus features, such as finding book recommendations based off the books/genres previously saved into your library!</p>

<h1><u>Table of Contents</u></h1>
<ul>
<li><a href="#tech-stack">Tech Stack</a></li>
<li><a href="#Features">Features</a></li>
  <ul>
  <li><a href="#homepage">Home</a></li>
  <li><a href="#addBooks">Search for Books</a></li>
  <li><a href="#tbr">To Be Read</a></li>
  <li><a href="#bookRecs">Book Recs</a></li>
  </ul>
<li><a href="#instructions">Installation</a></li>
</ul>

<h1>About Me</h1>
<p>Prior to studying a Hackbright Academy, Kellie was a student pursuing her Bachelors in Computer Science.</p> 
<p>When the pandemic hit and school became online only, mainstream academics became harder for students to showcase what they've learned through online testing.</p>
<p>While Kellie still wanted to further her education, her mainstream academics simply did not feel like the right choice to pursue at the current time.
This prompted Kellie to look into coding bootcamps, as this was the field she was interested in pursuing at the completion of her Bachelors Degree.</p>
<p>Taking this path allowed her to not only strengthen her software development skills, but also to grow in a 
new community and discover new paths and opportunities.</p>
<p>Outside of work and school, Kellie's favorite hobby is...you guessed it! Reading! This passion was the catalyst behind the creation of this project.</p>

<a name="tech-stack"></a>
<h1>Tech Stack</h1>
<ul>
<li>Python</li>
<li>HTML</li>
<li>Jinja2</li>
<li>Flask</li>
<li>PostgreSQL</li>
<li>SQLAlchemy</li>
<li>JavaScript</li>
<li>AJAX</li>
<li>JQuery</li>
<li>CSS</li>
<li>Bootstrap</li>
</ul>

<a name="features"></a>
<h1>Features</h1>
<h3>Link My Library's landing page.</h3>
<p>From the landing page users can login or navigate to the registration form.</p>
<img src="https://media.giphy.com/media/x2uG19pnWWjw7n1cpZ/giphy.gif">

<a name="homepage"></a>
<h3>Users Homepage/Library</h3>
<p>After logging in, You are immediatly brought to your main bookshelf. From here you can:</p>
<p>➜View all of your saved books </p>
<img src="https://media.giphy.com/media/iuprk6NB4O2JlkUPJv/giphy.gif">
<p>➜Click to view summaries </p>
<img src="https://media.giphy.com/media/K1svZvhqHTCZX1V82d/giphy.gif">
➜Adjust your tbr list by checking/unchecking the 'have you read this?' checkbox.
<img src="https://media.giphy.com/media/JNTkgJBfhD13FqOX8W/giphy.gif">

<a name="nav"></a>
<h3>Navigation</h3>
<p>The Navigation Bar allows easy access to:</p>
<p>➜Home ➜Add Books ➜To Be Read ➜Book Recommendations ➜Logout </p>

<a name="addBooks"></a>
<h3>Search For Books</h3>
<p>Enter the title, author or topic you wish to receive book results for.</p> 
<p>You are then re-routed to the search results, which contains two pages worth of book options to be added to your library.</p>
<img src="https://media.giphy.com/media/iyJRrY0gL5iH5W9CJt/giphy.gif">
<p> You can view the summaries, and author by clicking the magnifying glass.</p>
<img src="https://media.giphy.com/media/NU24aOiUV9XqksYytT/giphy.gif">

<a name="tbr"></a>
<h3>To Be Read</h3>
<p>View your updated tbr list.</p>
<img src="https://media.giphy.com/media/LcG4WNLvsT2JygI5fe/giphy.gif">

<a name="bookRecs"></a>
<h3>Book Recommendations</h3>
<p>Search through your personalized genre list to find book recommendations based off of saved books in your library!</p>
<p> By selecting a genre to search, you recieve 20+ book recommendations with similar topics to choose from and add to your shelves.</p>
<img src="https://media.giphy.com/media/YKs5eoGJD8XT9Ya47z/giphy.gif">


<a name="instructions"></a>
<h1> Installing Link My Library...</h1>
Clone this repo into your computers directory:
<pre>
  <code>https://github.com/KellieGrieneisen/LinkMyLibrary.git</code>
</pre>
Create your virtual environment inside your LinkMyLibrary Directory:
<pre>
  <code>virtualenv env</code>
</pre>
Activate the environment:
<pre>
  <code>source env/bin/activate</code>
</pre>
Install the Dependacies:
<pre>
  <code>pip install -r requirements.txt</code>
</pre>
<p>Sign up to use the <a href="https://developers.google.com/books/docs/overview">Google Books API</a></p>
Save your API Key in a file named <i>secrets.sh</i> in the following format:
<pre>
  <code>export GOOGLEBOOKS_API_KEY="YOURKEY"</code>
</pre>
Source your key from your <i>secrets.sh</i> file into your virtual env:
<pre>
  <code>source secrets.sh</code>
</pre>
Create your database(db):
<pre>
  <code>createdb library</code>
  <code>python3 model.py
       >>db.create_all()</code>
</pre>
Run the application:
<pre>
  <code>python3 server.py</code>
</pre>
You can now access Link My Library at 'localhost:5000/' and start creating your library!


