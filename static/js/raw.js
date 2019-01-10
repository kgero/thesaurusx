
function get_words_algo() {
  $('.aresults').empty();
  $('.data').empty();

  var data = {
    keyword: $('#keyword').val(),
    base: $('#base').val(),
    goal: $('#goal').val(),
    style: $('#style').val(),
    embd: $('input[name=embOptions]:checked').val()
  };
  console.log('get_words_algo():');
  console.log('data:', data);

  $.post('get_words_algo?', data, function(json, status) {
    console.log('algo response:', json);
    if (json.hasOwnProperty('error')) {
      $('.aresults').append('<p>' + json.error);
      return;
    }

    var words = json.words;
    $.each(words, function(i, text) {
      var p = $("<p>");
      if (i == 10) { p.append("<br /><br />"); }
      if (i >= 10) { p.addClass("text-muted"); }
      p.append(text);
      $('.aresults').append(p);
    });
  });
}

function get_words_simple() {
  console.log('get_words_simple');
  $('.tresults').empty();
  var data = {
    keyword: $('#keyword').val(),
    embd: $('input[name=embOptions]:checked').val()
  };
  console.log('get_words_simple():');
  console.log('data:', data);
  $.post('get_words_simple?', data, function(json, status) {
    console.log('simple response:', json);
    if (json.hasOwnProperty('error')) {
      $('.tresults').append('<p>' + json.error);
      return;
    }

    var words = json.words;
    $.each(words, function(i, text) {
      var p = $("<p>");
      if (i == 10) { p.append("<br /><br />"); }
      if (i >= 10) { p.addClass("text-muted"); }
      p.append(text);
      $('.tresults').append(p);
    });
  });
}

$(document).ready( function() {

  console.log('booting up...');

  $('.get_words').click( function() { 
    get_words_algo(); 
    get_words_simple(); 
  });

});
