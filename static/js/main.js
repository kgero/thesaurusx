
var embeddings = {
  // '1B Corpus': 'oneb_pos',
  'Darwin': 'darwin_pos',
  'Gandhi': 'gandhi_pos',
  'Gothic': 'gothic_pos',
  'Joyce': 'joyce_pos',
  'Philosophy': 'philosophy_pos',
  'Sci-fi': 'scifi_pos',
  'Science': 'arxiv_abs_pos',
  'Oxford': 'rogets'
};

var descriptions = {
  'Science': '40k science abstracts from arXiv.org',
  'Joyce': 'novels by James Joyce',
  'Darwin': 'naturalist books by Charles Darwin',
  // '1B Corpus': 'the one billion word benchmark, mostly news articles',
  'Gandhi': 'speeches & letters of Mahatma Gandhi',
  'Gothic': 'gothic horror novels',
  'Philosophy': 'philosophy books',
  'Sci-fi': 'pulp 1950s scifi magazines',
  'Oxford': "the Oxford American Writer's Thesaurus"
}

var word_history = [];

var default_checks = ['rogets', 'arxiv_abs_pos', 'gandhi_pos']

function set_up() {
  console.log('making new divs...');

  $('.main').css('visibility', 'hidden'); // hide until first search
  $('.panel').css('visibility', 'hidden'); // hide until first search
  
  // making thesaurus divs
  for (var key in embeddings) {
    var div = $("<div>").addClass("corpus-results").addClass(embeddings[key]);
    var title = $("<p>").addClass("thesaurus-header").append(key);
    var content = $("<div>").attr('id', embeddings[key]);
    div.append(title).append(content);
    $('.main').append(div);
  }
}



function get_words_algo() {
  $('.main').css('visibility', 'visible'); // make sure div is visible
  $('.panel').css('visibility', 'visible'); // make sure div is visible

  word_history.push($('#keyword').val().toString());
  console.log('history', word_history);
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
      // update history
      $(".history").empty();
      $.each(word_history, function(i, word) {
        $('.history').append(word).append("<br>");
      });


      $('#' + json.embd).empty();
      console.log('algo response:', json);
      if (json.hasOwnProperty('error')) {
        $('#' + json.embd).append('<p><i>' + json.error);
        return;
      }

      $.each(json.results, function(word) {
        console.log('word iteration', json.embd, word);

        // make part-of-speech (e.g. adj) span
        if (word.indexOf('_') > -1) {
          var p = $("<p>").addClass("results_p");
          var pos = $("<span>").addClass('pos').css('margin-bottom', '0px');
          var pos_text = word.split('_')[1].toLowerCase();
          pos.append(pos_text).append('. ');
          p.append(pos);
        }
        // add all the synonyms
        $.each(json.results[word], function(i, text) {
          var word_obj = $("<a>").text(text).attr("text", text);
          word_obj.click(function() {
            $('#keyword').val($(this).attr("text"));
            get_words_algo();
          })
          if (i >= 10) { return false; }
          p.append(word_obj);
          if (i < json.results[word].length - 1) { p.append(', '); }
        });
        // add whole p tag to style div
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
