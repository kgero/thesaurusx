
var embeddings = {
  // 'GoogleNews': 'GoogleNews-vectors-negative300', 
  // 'Wikipedia+Gigaword': 'glove-6B-200d', 
  // 'Twitter': 'glove-twitter-27B-50d',
  // 'Food Reviews': 'food',
  // 'GloVe': 'glove-slim',
  'Science': 'arxiv_abs',
  'Science (l)': 'arxiv_abs_lemma',
  'Joyce': 'joyce',
  'Joyce (l)': 'joyce_lemma',
  // 'Dickens': 'dickens',
  // 'Darwin': 'darwin',
  // 'Sherlock': 'sherlock',
  // 'Poetry Magazine': 'poetry',
  // 'Aretha Tweets': 'aretha',
  // 'Australia Tweets': 'australia',
  '1B Corpus': 'oneb',
  '1B Corpus (l)': 'oneb_lemma',
  'Word2Vec': 'word2vec-slim',
  // 'Gandhi': 'gandhi',
  // 'NYT Science': 'nyt-science',
  'Law': 'law'
  // 'Merge Science Big': 'merge-science-big',
  // 'Merge Science Small': 'merge-science-small'
  // 'Darwin Dep': 'darwin-dep',
  // 'Joyce Dep': 'joyce-dep'
};

var default_checks = ['glove-slim', 'arxiv_abs', 'joyce', 'darwin']

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
  // var dt = $('<dt>');
  // dt.append('Regular').addClass('norm').addClass('style');
  // var dd = $('<dd>');
  // dd.addClass('normal').addClass('norm').addClass('style');
  // dl.append(dt).append(dd);
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

  // making checkboxes
  // var lab = $('<label class="checkbox-inline">');
  // var box = $('<input type="checkbox" id="norm_box">');
  // box.val('norm');
  // lab.append(box).append('Regular');
  // $('.checkboxes').append(lab);
  for (var key in embeddings) {
    var lab = $('<label class="checkbox-inline">');
    var box = $('<input type="checkbox">');
    box.attr('id', embeddings[key] + '_box');
    box.val(embeddings[key]);
    lab.append(box).append(key);
    $('.checkboxes').append(lab);
    $('.checkboxes').append("<br />");
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

function get_words_algo(partofspeech) {

  for (var key in embeddings) {
    $('#' + embeddings[key]).empty();
    var loading = $('<span class="glyphicon glyphicon-refresh" aria-hidden="true">');
    loading.addClass("spin");
    $('#' + embeddings[key]).append(loading);
    var data = {
      keyword: $('#keyword').val(),
      embd: embeddings[key],
      pos: partofspeech
    };

    console.log('get_words_algo query', key, data)

    $.post('get_words_algo?', data, function(json, status) {
      $('#' + json.embd).empty();
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
      $('#' + json.embd).append(p);

      if (json.hasOwnProperty('closest')) {
        var closest = json.closest;
        var p = $("<p>");
        p.addClass('text-muted');
        $.each(closest, function(i, text) {
          p.append(text).append(', ');
        });
        $('#' + json.embd).append(p);
      }

      if (json.hasOwnProperty('dicterror')) { 
        $('#' + json.embd).append('<p class="text-muted">' + json.dicterror);
      } else if (json.hasOwnProperty('sentence')) {
        var p = $("<p>");
        p.addClass('text-muted');
        var sp = $("<span>");
        sp.addClass("usage").text(json.sentence);
        p.append("usage: ").append(sp);
        $('#' + json.embd).append(p);
      }

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

function get_words_simple() {
  $('.mainerror').empty();
  for (var key in embeddings) { $('#' + embeddings[key]).empty(); }
  var data = {
    keyword: $('#keyword').val()
  };
  console.log('get_words_simple request', data);
  $.post('get_words_simple?', data, function(json, status) {
    console.log('simple response:', json);
    if (json.hasOwnProperty('error')) {
      $('.mainerror').append('<p>' + json.error);
      return;
    }

    var p1 = $("<p>").text('parts of speech: '+json.pos);
    $('#pos').empty().append(p1);

    get_words_algo(json.pos_search);

    // var words = json.words;
    // var p = $("<p>");
    // $.each(words, function(i, text) {
    //   if (i >= 10) { return false; }
    //   p.append(text).append(', ');
    // });
    // $('.normal').append(p);
  });
}



$(document).ready( function() {

  console.log('booting up...');

  set_up();

  update_styles();

  $('#keyword').bind('keyup', function(e) {
    if ( e.keyCode === 13 ) { // 13 is enter key
      // get_words_algo(); 
      get_words_simple(); 
    }
  });

  $('.get_words').click( function() { 
    // get_words_algo(); 
    get_words_simple(); 
  });

  $('.update_styles').click( function() { 
    update_styles();  
  });

});
