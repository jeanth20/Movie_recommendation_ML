var tinderContainer = document.querySelector('.tinder');

function initCards() {
  var allCards = document.querySelectorAll('.tinder--card');
  var newCards = document.querySelectorAll('.tinder--card:not(.removed)');
  newCards.forEach(function(card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });
  tinderContainer.classList.add('loaded');
}

function createCard(movie) {
  var card = document.createElement('div');
  card.classList.add('tinder--card');
  card.id = movie.id;

  var img = document.createElement('img');
  img.src = movie.imageSrc;
  card.appendChild(img);

  var title = document.createElement('h2');
  title.textContent = movie.title;
  card.appendChild(title);

  var genre = document.createElement('h4');
  genre.textContent = movie.genre;
  card.appendChild(genre);

  var runtime = document.createElement('h2');
  runtime.textContent = "runtime: "+movie.runtime;
  card.appendChild(runtime);

  var vote_count = document.createElement('h4');
  vote_count.textContent = movie.vote_count;
  card.appendChild(vote_count);

  var ranking = document.createElement('h4');
  ranking.textContent = movie.ranking;
  card.appendChild(ranking);

  var rating = document.createElement('h4');
  rating.textContent = movie.rating;
  card.appendChild(rating);

  var tinderContainer = document.querySelector('.tinder--cards');
  tinderContainer.appendChild(card);
}

function fetchCards() {
  $.ajax({
    url: '/get_movie_data',
    method: 'GET',
    success: function(data) {
      data.forEach(function(movie) {
        createCard(movie);
      });

      initCards();

      var allCards = document.querySelectorAll('.tinder--card');
      allCards.forEach(function(el) {
        var hammertime = new Hammer(el);
        hammertime.get('pan').set({ direction: Hammer.DIRECTION_ALL });

        hammertime.on('pan', function (event) {
          el.classList.add('moving');
          // if (event.deltaX === 0) return;
          // if (event.center.x === 0 && event.center.y === 0) return;
          tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
          tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);
          tinderContainer.classList.toggle('tinder_gold', event.deltaY < 0);
          
          var xMulti = event.deltaX * 0.03;
          var yMulti = event.deltaY / 80;
          var rotate = xMulti * yMulti;
          
          // console.log(event.deltaX)
          event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
        });

        hammertime.on('panend', function (event) {
          el.classList.remove('moving');
          tinderContainer.classList.remove('tinder_love', 'tinder_nope', 'tinder_gold');
        
          var moveOutWidth = document.body.clientWidth;
          // var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;
          var keep = Math.abs(event.deltaX) < el.clientWidth / 2 || Math.abs(event.velocityX) < 0.5;
        
          event.target.classList.toggle('removed', !keep);
        
          if (keep) {
            event.target.style.transform = '';
          } else {
            var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
            var toX = event.deltaX > 0 ? endX : -endX;
            var endY = Math.abs(event.velocityY) * moveOutWidth;
            var toY = event.deltaY > 0 ? endY : -endY;
            var xMulti = event.deltaX * 0.03;
            var yMulti = event.deltaY / 80;
            var rotate = xMulti * yMulti;
            event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
            initCards();

            var swipeDirection = event.deltaX > 0 ? 'right' : 'left';
            var card = document.querySelector('.tinder--card');
            var cardId = card.getAttribute('id');
            // console.log(cardId);
            var username = 'test_user';
            // console.log(username);
            handleSwipeAction(cardId, username, swipeDirection);
            // console.log(swipeDirection);

          }
        });

      });
    },
    error: function() {
      console.error('Error fetching movie data.');
    }
  });
}

fetchCards();


function createButtonListener(love) {
  return function (event) {
    var cards = document.querySelectorAll('.tinder--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');

    if (love) {
      card.style.transform = 'translate(' + moveOutWidth + 'px, 100px) rotate(60deg)';
      
      var swipeDirection = event.deltaX > 0 ? 'right' : 'left';
      var card = document.querySelector('.tinder--card');
      var cardId = card.getAttribute('id');
      // console.log(cardId);
      var username = 'test_user';
      // console.log(username);
      handleSwipeAction(cardId, username, swipeDirection);
      // console.log("love");
    } else {
      card.style.transform = 'translate(-' + moveOutWidth + 'px, 100px) rotate(-60deg)';
      
      var swipeDirection = event.deltaX > 0 ? 'right' : 'left';
      var card = document.querySelector('.tinder--card');
      var cardId = card.getAttribute('id');
      // console.log(cardId);
      var username = 'test_user';
      // console.log(username);
      handleSwipeAction(cardId, username, swipeDirection);
      // console.log("nope");
    }

    initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);
nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);


function handleSwipeAction(id, username, swipeDirection) {
  var url = 'http://localhost:8000/counter/';
  // Send the POST request
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: id,
      username: username,
      swipeDirection: swipeDirection
    })
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response data
      console.log('Counter updated:', data);
    })
    .catch(error => {
      console.error('Error updating counter:', error);
    });
}
