
var embeddings = {
  // 'GoogleNews': 'GoogleNews-vectors-negative300', 
  // 'Wikipedia+Gigaword': 'glove-6B-200d', 
  // 'Twitter': 'glove-twitter-27B-50d',
  // 'Food Reviews': 'food',
  // 'GloVe': 'glove-slim',
  'Science': 'arxiv_abs_pos',
  // 'Science (l)': 'arxiv_abs_lemma',
  // 'Joyce': 'joyce',
  'Joyce': 'joyce_pos',
  // 'Dickens': 'dickens',
  'Darwin': 'darwin_pos',
  // 'Sherlock': 'sherlock',
  // 'Poetry Magazine': 'poetry',
  // 'Aretha Tweets': 'aretha',
  // 'Australia Tweets': 'australia',
  // '1B Corpus': 'oneb',
  '1B Corpus': 'oneb_pos',
  // 'Word2Vec': 'word2vec-slim',
  'Gandhi': 'gandhi_pos',
  // 'NYT Science': 'nyt-science',
  // 'Law': 'law'
  // 'Merge Science Big': 'merge-science-big',
  // 'Merge Science Small': 'merge-science-small'
  // 'Darwin Dep': 'darwin-dep',
  // 'Joyce Dep': 'joyce-dep',
  'Oxford': 'rogets'
};

var descriptions = {
  'Science': '40k science abstracts from arXiv.org',
  'Joyce': 'novels by James Joyce',
  'Darwin': 'naturalist books by Charles Darwin',
  '1B Corpus': 'the one billion word benchmark, mostly news articles',
  'Gandhi': 'speeches & letters of Mahatma Gandhi',
  'Oxford': "the Oxford American Writer's Thesaurus"
}

var default_checks = ['rogets', 'arxiv_abs_pos', 'gandhi_pos']

function set_up() {
  console.log('making new divs...');
  var dl = $("<dl>");
  dl.addClass('dl-horizontal');
  var dt = $('<dt>');
  // dt.append('Rogets').addClass('norm').addClass('style');
  // var dd = $('<dd>');
  // dd.addClass('rogets').addClass('norm').addClass('style');
  // dl.append(dt).append(dd);
  for (var key in embeddings) {
    var dt = $('<dt>');
    dt.append(key);
    dt.addClass(embeddings[key]).addClass('style lead').css('font-weight', 300);
    var dd = $('<dd>');
    dd.addClass(embeddings[key]).addClass('style');
    dd.attr('id', embeddings[key]);
    dl.append(dt).append(dd);
  }
  $('.main').append(dl);

  // making checkboxes
  for (var key in embeddings) {
    var lab = $('<label class="checkbox-inline">');
    var box = $('<input type="checkbox">');
    box.attr('id', embeddings[key] + '_box');
    box.val(embeddings[key]);
    lab.append(box).append(key);
    $('.checkboxes').append(lab);
    $('.checkboxes').append("<br />");
    var descrip = $('<small>').addClass('text-muted');
    descrip.append(descriptions[key]);
    $('.checkboxes').append(descrip).append("<br />");
  }

  //check defaults
  $.each(default_checks, function(i, val) {
    $('#' + val + '_box').prop('checked', true);
  });
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
  $('#search-word').empty();
  $('#search-word').append('<h2>'+$('#keyword').val()+'</h2>');

  for (var key in embeddings) {
    $('#' + embeddings[key]).empty();
    var loading = $('<span class="glyphicon glyphicon-refresh" aria-hidden="true">');
    loading.addClass("spin");
    $('#' + embeddings[key]).append(loading);
    var data = {
      keyword: $('#keyword').val(),
      embd: embeddings[key]
    };

    

    if (embeddings[key] == 'rogets') { var endpoint = 'get_words_thes?' } 
    else { var endpoint = 'get_words_algo?'}

    console.log('endpoint, key, data', endpoint, key, data)

    $.post(endpoint, data, function(json, status) {
      $('#' + json.embd).empty();
      console.log('algo response:', json);
      if (json.hasOwnProperty('error')) {
        $('#' + json.embd).append('<p>' + json.error);
        return;
      }
      
      $.each(json.results, function(word) {
        console.log('word iteration', json.embd, word);
        
        if (word.indexOf('_') > -1) { 
          var lead = $("<p>").addClass('lead').css('margin-bottom', '0px');
          var pos = word.split('_')[1].toLowerCase();
          lead.append(pos);
          $('#' + json.embd).append(lead);
        }
        var p = $("<p>");
        $.each(json.results[word], function(i, text) {
          if (i >= 10) { return false; }
          p.append(text).append(', ');
        });
        $('#' + json.embd).append(p);
      });
      
      if (json.hasOwnProperty('note')) {
        if (json.note.length > 1) {
          var p = $("<p>");
          p.text(json.note);
          $('#' + json.embd).append(p);
        }
      }
    }).fail(function(response) {
      console.log('Error: ' + response.responseText);
      var p = $("<p>");
      p.text('error occurred.');
      $('#' + embeddings[key]).append(p);
    });
  }
}


$(document).ready( function() {

  console.log('booting up...');

  set_up();

  update_styles();

  $('#keyword').bind('keyup', function(e) {
    if ( e.keyCode === 13 ) { // 13 is enter key
      get_words_algo(); 
    }
  });

  $('.get_words').click( function() { 
    get_words_algo(); 
  });

  $('.update_styles').click( function() { 
    update_styles();  
  });

});
