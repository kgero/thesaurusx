
var embeddings = {
  'GoogleNews': 'GoogleNews-vectors-negative300', 
  'Wikipedia+Gigaword': 'glove-6B-200d', 
  'Twitter': 'glove-twitter-27B-50d',
  'Food Reviews': 'food',
  'Poetry Magazine': 'poetry',
  'Joyce': 'joyce',
  'Dickens': 'dickens',
  'Darwin': 'darwin',
  'Sherlock': 'sherlock'
};

function set_up_old() {
  console.log('making new divs...');
  for (var key in embeddings) {
    var p = $('<p>');
    p.append('<strong>' + key + '</strong>');
    var div = $('<div>');
    div.addClass('style');
    div.attr('id', embeddings[key]);
    $('.main').append(p).append(div);
  }
}

function set_up() {
  console.log('making new divs...');
  var dl = $("<dl>");
  dl.addClass('dl-horizontal');
  var dt = $('<dt>');
  dt.append('Regular').addClass('norm').addClass('style');
  var dd = $('<dd>');
  dd.addClass('normal').addClass('norm').addClass('style');
  dl.append(dt).append(dd);
  for (var key in embeddings) {
    var dt = $('<dt>');
    dt.append(key);
    dt.addClass(embeddings[key]).addClass('style');
    var dd = $('<dd>');
    dd.addClass(embeddings[key]).addClass('style');
    dd.attr('id', embeddings[key]);
    dl.append(dt).append(dd);
  }
  $('.main').append(dl);
}

function update_styles() {
  $('.style').hide();
  $("input[type=checkbox]:checked").each(function() {
    key = $(this).val();
    console.log( key );
    $('.' + key).show();
  });
}

function get_words_algo() {

  for (var key in embeddings) {
    console.log('#' + embeddings[key]);
    $('#' + embeddings[key]).empty();
    console.log('querying', key);
    var data = {
      keyword: $('#keyword').val(),
      embd: embeddings[key]
    };
    // console.log('get_words_algo():');
    // console.log('data:', data);

    $.post('get_words_algo?', data, function(json, status) {
      console.log('algo response:', json);
      if (json.hasOwnProperty('error')) {
        $('#' + json.embd).append('<p>' + json.error);
        return;
      }

      var words = json.words;
      var p = $("<p>");
      $.each(words, function(i, text) {
        if (i >= 10) { return false; }
        p.append(text).append(', ');
      });
      console.log('appending to', json.embd);
      $('#' + json.embd).append(p);
    });
  }
}

function get_words_simple() {
  console.log('get_words_simple');
  $('.normal').empty();
  var data = {
    keyword: $('#keyword').val()
  };
  console.log('get_words_simple():');
  console.log('data:', data);
  $.post('get_words_simple?', data, function(json, status) {
    console.log('simple response:', json);
    if (json.hasOwnProperty('error')) {
      $('.normal').append('<p>' + json.error);
      return;
    }

    var words = json.words;
    var p = $("<p>");
    $.each(words, function(i, text) {
      if (i >= 10) { return false; }
      p.append(text).append(', ');
    });
    $('.normal').append(p);
  });
}



$(document).ready( function() {

  console.log('booting up...');

  set_up();

  update_styles();

  $('.get_words').click( function() { 
    get_words_algo(); 
    get_words_simple(); 
  });

  $('.update_styles').click( function() { 
    update_styles();  
  });

});
